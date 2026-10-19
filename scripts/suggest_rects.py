"""Suggest highlight rects for a screenshot: finds the cards, panels, charts and tables a viewer's eye goes to.

Usage: python suggest_rects.py shot.png [more.png …] [--base W H] [--n 4] [--preview DIR] [--json]
Prints, per image, up to N rects [x, y, w, h] in BASE units (the coordinates film.json uses), in reading
order, numbered 1…N. --preview writes <DIR>/<image>.rects.jpg with the numbered boxes drawn on the shot:
look at it, then copy the rect of the region each feature point talks about into "points[i].rect".
Base default = the intake rule: captures ≥ 2400 px wide are 2× (base = size / 2), else 1×.

How: edges → dilated into blobs → connected components at two scales → boxes that are neither tiny nor most of
the screen → the best non-overlapping ones (edge-rich, medium-sized). Pure numpy + Pillow. It finds structure,
not meaning: if the point is about a button, a box around its card is right; a box around a blank area is not.
"""
import argparse
import json
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

W = 480   # working width


def default_base(w, h):
    s = 2 if w >= 2400 else 1
    if w / h < 0.75: s = 3 if w >= 1000 else (2 if w >= 700 else 1)   # phone capture (same rule as intake.py)
    return [round(w / s), round(h / s)]


def components(mask):
    """Bounding boxes [x0, y0, x1, y1, pixels] of 4-connected True regions."""
    h, w = mask.shape
    seen = np.zeros_like(mask, bool)
    out = []
    ys, xs = np.nonzero(mask)
    for y, x in zip(ys, xs):
        if seen[y, x]: continue
        q = deque([(y, x)]); seen[y, x] = True
        x0 = x1 = x; y0 = y1 = y; n = 0
        while q:
            cy, cx = q.popleft(); n += 1
            x0, x1, y0, y1 = min(x0, cx), max(x1, cx), min(y0, cy), max(y1, cy)
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True; q.append((ny, nx))
        out.append([x0, y0, x1 + 1, y1 + 1, n])
    return out


def dilate(m, r):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    return inter / ((a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter + 1e-9)


def inside(a, b, tol=0.9):
    """True if most of a lies inside b."""
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    return ix * iy >= tol * (a[2] - a[0]) * (a[3] - a[1])


def suggest(path, base=None, n=4):
    im = Image.open(path).convert('L')
    bw, bh = base or default_base(*im.size)
    H = max(1, round(W * im.size[1] / im.size[0]))
    g = np.asarray(im.resize((W, H), Image.BILINEAR)).astype(float)
    e = np.zeros_like(g)
    e[:, 1:] = np.maximum(e[:, 1:], np.abs(np.diff(g, axis=1)))
    e[1:, :] = np.maximum(e[1:, :], np.abs(np.diff(g, axis=0)))
    edge = e > 3
    edge[:2, :] = edge[-2:, :] = False; edge[:, :2] = edge[:, -2:] = False   # screen border is not content
    area = W * H

    def pick(radii, lo, hi):
        cands = []
        for r in radii:
            for x0, y0, x1, y1, _ in components(dilate(edge, r)):
                bw_, bh_ = x1 - x0, y1 - y0
                fr = bw_ * bh_ / area
                if not (lo <= fr <= hi) or bw_ < 24 or bh_ < 16 or bw_ / bh_ > 9 or bh_ / bw_ > 6: continue
                cands.append([x0, y0, x1, y1, edge[y0:y1, x0:x1].mean() * fr ** 0.35])
        cands.sort(key=lambda c: -c[4])
        out = []
        for c in cands:
            if any(iou(c, p) > 0.15 or inside(c, p) or inside(p, c) for p in out): continue
            out.append(c)
            if len(out) >= n: break
        return out

    picked = pick((2, 5), 0.015, 0.45)
    if len(picked) < 2:   # a chart or a sparse screen: merge harder and allow one large region (the plot area)
        picked = pick((9, 16), 0.03, 0.8)
    picked.sort(key=lambda c: (round(c[1] / (H / 6)), c[0]))   # reading order: rows, then left → right
    sx, sy = bw / W, bh / H
    pad = 8
    rects = []
    for x0, y0, x1, y1, _ in picked:
        x, y = max(0, round(x0 * sx) - pad), max(0, round(y0 * sy) - pad)
        rects.append([x, y, min(bw - x, round((x1 - x0) * sx) + 2 * pad), min(bh - y, round((y1 - y0) * sy) + 2 * pad)])
    return [bw, bh], rects


def preview(path, base, rects, out_dir):
    im = Image.open(path).convert('RGB')
    k = im.size[0] / base[0]
    d = ImageDraw.Draw(im)
    lw = max(3, round(4 * k))
    for i, (x, y, w, h) in enumerate(rects, 1):
        box = [x * k, y * k, (x + w) * k, (y + h) * k]
        d.rectangle(box, outline=(230, 40, 60), width=lw)
        d.rectangle([box[0], box[1], box[0] + 44 * k, box[1] + 40 * k], fill=(230, 40, 60))
        d.text((box[0] + 12 * k, box[1] + 6 * k), str(i), fill='white', font_size=round(28 * k))
    im.thumbnail((1600, 1600))
    dst = Path(out_dir) / (Path(path).stem + '.rects.jpg')
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, quality=85)
    return dst


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('images', nargs='+'); ap.add_argument('--base', nargs=2, type=int); ap.add_argument('--n', type=int, default=4)
    ap.add_argument('--preview'); ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    res = {}
    for p in a.images:
        base, rects = suggest(p, a.base, a.n)
        res[p] = {'base': base, 'rects': rects}
        if a.preview: res[p]['preview'] = str(preview(p, base, rects, a.preview))
    if a.json:
        print(json.dumps(res, indent=1))
    else:
        for p, r in res.items():
            print(f"{p}  base {r['base']}" + (f"  → preview {r['preview']}" if r.get('preview') else ''))
            for i, rc in enumerate(r['rects'], 1): print(f'  {i}: {rc}')
            if not r['rects']: print('  no clear regions — measure with grid_overlay.py, or use "frame": "photo" (no highlight boxes)')
