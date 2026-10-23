#!/usr/bin/env python3
"""Snap a highlight box to the real element under it — for any product, any screenshot.

A model that writes "rect": [x, y, w, h] by eye is usually near the element and rarely on it. The fix is geometric and
product-agnostic: collect the boxes that really exist in the picture and replace the guess with the one it overlaps most.

Candidates, best first:
  1. the page's own element boxes (<shot>.regions.json from capture_app.mjs: panels, tables, buttons, headings)
  2. boxes found in the pixels (any screenshot, any app, a document page): connected blocks of marks at several scales

  python3 snap.py <image> --rect x,y,w,h [--base W,H]     → the snapped box and how sure it is
  python3 snap.py <image> --list [--base W,H]              → every candidate (debugging)
"""
import argparse, json, re, sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ACCEPT = 0.25   # below this overlap the guess points at nothing real: the box is kept as written (benchmark: evals/rects)


def iou(a, b):
    ax, ay, aw, ah = a; bx, by, bw, bh = b
    ix = max(0, min(ax + aw, bx + bw) - max(ax, bx)); iy = max(0, min(ay + ah, by + bh) - max(ay, by))
    i = ix * iy
    return i / (aw * ah + bw * bh - i) if i else 0.0


def _components(mask):
    """Bounding boxes (x0, y0, x1, y1) of 4-connected regions: row runs joined with union-find (numpy only, fast)."""
    H, W = mask.shape
    m = np.pad(mask.astype(np.int8), ((0, 0), (1, 1)))
    d = np.diff(m, axis=1)
    starts = [np.where(d[y] == 1)[0] for y in range(H)]
    ends = [np.where(d[y] == -1)[0] for y in range(H)]
    parent, box, prev = [], [], []
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for y in range(H):
        cur = []
        k = 0
        for s, e in zip(starts[y], ends[y]):
            idx = len(parent); parent.append(idx); box.append([s, y, e, y + 1]); cur.append((s, e, idx))
            while k < len(prev) and prev[k][1] <= s: k += 1
            j = k
            while j < len(prev) and prev[j][0] < e:
                ra, rb = find(idx), find(prev[j][2])
                if ra != rb: parent[rb] = ra
                j += 1
        prev = cur
    out = {}
    for i, b in enumerate(box):
        r = find(i); o = out.get(r)
        out[r] = b[:] if o is None else [min(o[0], b[0]), min(o[1], b[1]), max(o[2], b[2]), max(o[3], b[3])]
    return [tuple(v) for v in out.values()]


def _dilate(m, r):
    """Box dilation by r pixels, separable, with cumulative sums (numpy only)."""
    if r <= 0: return m
    def run(a, axis):
        c = np.cumsum(np.pad(a.astype(np.int32), [(r + 1, r) if ax == axis else (0, 0) for ax in range(2)]), axis=axis)
        hi = np.take(c, range(2 * r + 1, c.shape[axis]), axis=axis); lo = np.take(c, range(0, c.shape[axis] - 2 * r - 1), axis=axis)
        return (hi - lo) > 0
    return run(run(m, 0), 1)


def pixel_candidates(path, base):
    """Blocks of content at several scales: a text line, a card, a table, a column of cards. Works on any screenshot."""
    im = Image.open(path).convert('L')
    W = 640
    H = max(1, round(W * im.size[1] / im.size[0]))
    g = np.asarray(im.resize((W, H), Image.BILINEAR)).astype(float)
    e = np.zeros_like(g)
    e[:, 1:] = np.maximum(e[:, 1:], np.abs(np.diff(g, axis=1)))
    e[1:, :] = np.maximum(e[1:, :], np.abs(np.diff(g, axis=0)))
    sx, sy = base[0] / W, base[1] / H
    out = []
    for th in (3, 8, 18):
        edge = e > th
        edge[:1, :] = edge[-1:, :] = False; edge[:, :1] = edge[:, -1:] = False
        if edge.mean() < 0.0005: continue
        for r in (1, 3, 6, 10, 16):
            for x0, y0, x1, y1 in _components(_dilate(edge, r)):
                w, h = x1 - x0, y1 - y0
                if w < 8 or h < 6 or w * h > 0.7 * W * H: continue
                # undo the dilation so the box hugs the marks, not the halo around them
                x0, y0, x1, y1 = min(x1, x0 + r), min(y1, y0 + r), max(x0, x1 - r), max(y0, y1 - r)
                out.append([x0 * sx, y0 * sy, (x1 - x0) * sx, (y1 - y0) * sy])
        # closed frames (a card's border, a table's rule box) hold blocks of content: their outline is a candidate too
    # also: regions bounded by long straight lines (cards with borders but sparse content)
    out += _frame_candidates(e > 6, sx, sy)
    uniq = []
    for c in sorted(out, key=lambda c: -c[2] * c[3]):
        if all(iou(c, u) < 0.92 for u in uniq): uniq.append([round(v) for v in c])
    return uniq


def _frame_candidates(edge, sx, sy):
    """Rectangles drawn by long horizontal and vertical strokes (bordered cards, table frames, dialogs)."""
    H, W = edge.shape
    rows = np.where(edge.mean(1) > 0.25)[0]; cols = np.where(edge.mean(0) > 0.25)[0]
    out = []
    # runs along each strong row: a horizontal border spans [a, b]
    for y in rows[:: max(1, len(rows) // 40)] if len(rows) else []:
        line = edge[y]; xs = np.where(line)[0]
        if len(xs) < 20: continue
        a, b = xs.min(), xs.max()
        below = [y2 for y2 in rows if y2 > y + 8 and edge[y2, a:b].mean() > 0.6]
        if below: out.append([a * sx, y * sy, (b - a) * sx, (below[0] - y) * sy])
    return out


def candidates(path, base, regions=None):
    """All boxes that exist in the picture: the page's own elements first, then pixel blocks."""
    dom = []
    if regions:
        for r in regions.get('regions', []):
            x, y, w, h = r['rect']
            if w >= 12 and h >= 10: dom.append([x, y, w, h])
    return dom, pixel_candidates(path, base) if path and Path(path).exists() else []


def snap(rect, dom, pix):
    """(box, overlap, source): the real element the guess overlaps most. DOM boxes win ties: they are exact."""
    best, bi, src = rect, 0.0, 'kept'
    for c in dom:
        v = iou(rect, c)
        if v > bi: best, bi, src = c, v, 'element'
    for c in pix:
        v = iou(rect, c)
        if v > bi + 0.05: best, bi, src = c, v, 'pixels'   # pixels must clearly beat the page's own boxes
    if bi < ACCEPT: return rect, bi, 'kept'
    pad = 6   # a highlight sits just outside the element, not on its edge
    x, y, w, h = best
    return [x - pad, y - pad, w + 2 * pad, h + 2 * pad], bi, src


def ocr_regions(path, base):
    """Words on a screenshot with their boxes, in base units: macOS Vision (scripts/ocr.swift, compiled once and cached),
    else Tesseract when installed, else nothing (snapping then works on geometry alone). Results are cached per image."""
    import hashlib, os, shutil, subprocess
    path = Path(path)
    try:
        h = hashlib.sha1(path.read_bytes()).hexdigest()[:16]
    except Exception:
        return []
    cache = Path(os.path.expanduser('~/.cache/reelwright')); (cache / 'ocr').mkdir(parents=True, exist_ok=True)
    hit = cache / 'ocr' / f'{h}.json'
    items = None
    if hit.exists():
        try: items = json.load(open(hit))
        except Exception: items = None
    if items is None:
        items = []
        exe = cache / 'pf-ocr'
        if sys.platform == 'darwin' and not exe.exists() and shutil.which('swiftc'):
            subprocess.run(['swiftc', '-O', str(HERE / 'ocr.swift'), '-o', str(exe)], capture_output=True)
        try:
            if exe.exists():
                items = json.loads(subprocess.run([str(exe), str(path)], capture_output=True, text=True, timeout=120).stdout or '[]')
            elif shutil.which('tesseract'):
                tsv = subprocess.run(['tesseract', str(path), '-', '-l', 'chi_sim+eng', 'tsv'], capture_output=True, text=True, timeout=120).stdout
                for line in tsv.splitlines()[1:]:
                    c = line.split('\t')
                    if len(c) == 12 and c[11].strip() and c[0] == '5':
                        items.append({'text': c[11], 'rect': [int(c[6]), int(c[7]), int(c[8]), int(c[9])]})
        except Exception:
            items = []
        json.dump(items, open(hit, 'w'))
    W, H = Image.open(path).size
    kx, ky = base[0] / W, base[1] / H
    return [{'kind': 'text', 'text': it['text'], 'rect': [it['rect'][0] * kx, it['rect'][1] * ky, it['rect'][2] * kx, it['rect'][3] * ky]} for it in items if it.get('text')]


def _norm(t):
    return re.sub(r'[\s:：,，.。;；!！?？()（）\[\]【】"“”\'‘’/|·•\-–—]+', ' ', (t or '').lower()).strip()


def _cjk_overlaps(a, b):
    """Shared CJK runs of 2+ characters between a label token and a screen text ("队列研究" vs "千禧队列研究")."""
    out = []
    for n in range(min(len(a), 6), 2, -1):   # a shared run of 3+ characters (two, like 研究, is everywhere)
        for k in range(0, len(a) - n + 1):
            if a[k:k + n] in b: out.append(a[k:k + n])
        if out: return out
    return out


def text_targets(labels, regions, find=None, rect=None):
    """Cards that carry the point's own words, best first: [(score, box)]. Any product, any screenshot whose words are known
    (the page's element texts, or OCR). Every word of the label found on screen votes for the smallest card around it;
    a card holding more of the label's words wins ("34 个研究条目" → the card with "34个" and "研究条目", not the nav item)."""
    lab = ' '.join(_norm(l) for l in labels if l)
    if not lab or not regions: return []
    lab_ns = lab.replace(' ', '')
    W, H = regions.get('base', [1920, 1080])
    R = regions.get('regions', [])
    # the label's own tokens: CJK runs (2+ characters) and Latin words (3+ letters), without the most generic words
    STOP = {'the', 'and', 'for', 'with', 'your', 'you', 'all', 'one', 'new', 'auto', 'instantly', 'glance', '一键', '自动', '实时', '清晰'}
    toks = [t_ for t_ in re.findall(r'[\u4e00-\u9fff]{2,}|[a-z][a-z0-9\-]{2,}', lab) if t_ not in STOP]
    def match(t):
        tn = t.replace(' ', '')
        if len(tn) < 2 or len(t) > 60 or re.fullmatch(r'[\d\s.,%]+', t): return 0
        if tn in lab_ns and not re.fullmatch(r'[a-z0-9 .\-]{1,2}', t): return len(tn)            # the whole element text is in the label
        sc = 0
        for k in toks:
            if re.fullmatch(r'[a-z][a-z0-9\-]*', k): sc += len(k) if re.search(r'(?<![a-z0-9])' + re.escape(k) + r'(?![a-z0-9])', t) else 0
            else: sc += len(k) if k in tn else (max((len(c) for c in _cjk_overlaps(k, tn)), default=0))
        return sc
    hits = [(match(_norm(r.get('text'))), r['rect']) for r in R if r.get('text')]
    hits = [(w, b) for w, b in hits if w]
    if not hits: return []
    boxes = [r['rect'] for r in R if r.get('kind') == 'panel']
    def container(b):
        x, y, w, h = b; cx, cy = x + w / 2, y + h / 2
        fit = [c for c in boxes if c[0] <= cx <= c[0] + c[2] and c[1] <= cy <= c[1] + c[3] and c[2] * c[3] >= 4 * w * h
               and c[2] * c[3] <= 0.35 * W * H and not (c[2] > 0.7 * W and c[3] < 0.1 * H)]   # no app bars
        if fit:
            if rect:   # a box written by eye is often in the wrong place but the right size: pick the card of that size
                sim = lambda c: min(c[2], rect[2]) / max(c[2], rect[2]) * min(c[3], rect[3]) / max(c[3], rect[3])
                return max(fit, key=sim)
            return min(fit, key=lambda c: c[2] * c[3])
        return [x - 10, y - 8, w + 20, h + 16]
    cards = []
    for _, b in hits:
        c = container(b)
        if all(iou(c, k) < 0.9 for k in cards): cards.append(c)
    inside = lambda b, c: c[0] - 2 <= b[0] + b[2] / 2 <= c[0] + c[2] + 2 and c[1] - 2 <= b[1] + b[3] / 2 <= c[1] + c[3] + 2
    scored = [(sum(w for w, b in hits if inside(b, c)), c) for c in cards]
    out = sorted(scored, key=lambda x: -x[0])
    out_hits = hits
    text_targets.last_hits = out_hits; text_targets.inside = inside
    return out


def snap_with_text(rect, labels, regions, find, dom, pix, min_words=4):
    """Geometry first; the point's words only correct it. If the element the box snapped to holds any of the label's
    words, the box was right and stays. If it holds none and another card carries 4+ characters of the label, the box
    was written on the wrong element: it moves there (a card of about the size that was written)."""
    geo, ov, src = snap(rect, dom, pix)
    tt = text_targets(labels, regions, find, rect)
    if not tt: return geo, ov, src
    hits, inside = text_targets.last_hits, text_targets.inside
    g_unpadded = [geo[0] + 6, geo[1] + 6, geo[2] - 12, geo[3] - 12] if src != 'kept' else geo
    if sum(w for w, b in hits if inside(b, g_unpadded)) > 0: return geo, ov, src   # the box (snapped or as written) already holds the label's words
    top = tt[0][0]
    if top < min_words: return geo, ov, src
    near = [(sc, b) for sc, b in tt if sc >= top - 1]
    sc, best = max(near, key=lambda x: (iou(rect, x[1]), -abs(x[1][0] + x[1][2] / 2 - rect[0] - rect[2] / 2) - abs(x[1][1] + x[1][3] / 2 - rect[1] - rect[3] / 2)))
    x, y, w, h = best
    return [x - 6, y - 6, w + 12, h + 12], iou(rect, best), 'text'

def cut_edges(path, ink_th=14, win_div=48, thr=0.1, depth=9):   # tuned on evals/rects (bench_cuts.py), held-out checked
    """Sides where a crop cuts through content (a word, a table, a chart frame runs into the edge) — any screenshot.
    The side is walked in short windows: a window counts when the outermost strip and the strip just inside it both
    carry marks there (content continues past the edge). Meant for crops; a full window's toolbar touches its edge."""
    try:
        im = Image.open(path).convert('L'); W0, H0 = im.size
        g = np.asarray(im.resize((640, max(1, round(640 * H0 / W0))))).astype(float)
    except Exception:
        return []
    bg = np.median(g)
    ink = np.abs(g - bg) > ink_th                      # a mark: clearly darker or lighter than the background
    out = []
    for name, outer, inner in (('left', ink[:, 0:2].any(1), ink[:, 3:depth].any(1)), ('right', ink[:, -2:].any(1), ink[:, -depth:-3].any(1)),
                               ('top', ink[0:2, :].any(0), ink[3:depth, :].any(0)), ('bottom', ink[-2:, :].any(0), ink[-depth:-3, :].any(0))):
        both = outer & inner
        n = len(both); win = max(6, n // win_div)
        hits = [both[k:k + win].mean() for k in range(0, n - win + 1, win)]
        if any(h > thr for h in hits): out.append(name)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('image'); ap.add_argument('--rect'); ap.add_argument('--base'); ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
    p = Path(a.image)
    base = [int(v) for v in a.base.split(',')] if a.base else list(Image.open(p).size)
    reg = None
    for q in (p.with_suffix('.regions.json'), Path(str(p) + '.regions.json')):
        if q.exists(): reg = json.load(open(q)); break
    dom, pix = candidates(p, base, reg)
    if a.list:
        print(json.dumps({'elements': dom[:200], 'pixels': pix[:200]})); return
    r = [float(v) for v in a.rect.split(',')]
    box, v, src = snap(r, dom, pix)
    print(json.dumps({'rect': [round(x) for x in box], 'overlap': round(v, 2), 'source': src}))


if __name__ == '__main__':
    main()
