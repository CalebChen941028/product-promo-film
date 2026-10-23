#!/usr/bin/env python3
"""How accurate are highlight boxes, before and after snapping — on interfaces from no particular product.

  node evals/rects/gen_ui.mjs evals/runs/rects 40 7      (random interfaces with the true box of every target)
  python3 evals/rects/bench.py evals/runs/rects [--guesses 4] [--seed 1]

A guess imitates a mid-sized model writing coordinates by eye: the right area, off by 10–40 % in place and size, rounded
to tens. Each guess is scored by its overlap (IoU) with the true box, raw and after scripts/snap.py, with the page's own
element boxes (an app captured by capture_app.mjs) and with pixels only (any screenshot from anywhere).
Accurate = IoU ≥ 0.7 (the box visibly frames the element); missed = IoU < 0.4.
"""
import argparse, json, random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / 'scripts'))
import snap  # noqa: E402


def guess(r, rnd):
    x, y, w, h = r
    sw, sh = w * rnd.uniform(0.7, 1.4), h * rnd.uniform(0.7, 1.4)
    cx, cy = x + w / 2 + rnd.gauss(0, 0.18) * w, y + h / 2 + rnd.gauss(0, 0.18) * h
    return [round((cx - sw / 2) / 10) * 10, round((cy - sh / 2) / 10) * 10, round(sw / 10) * 10, round(sh / 10) * 10]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('dir'); ap.add_argument('--guesses', type=int, default=4); ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args()
    rnd = random.Random(a.seed)
    rows = {'raw': [], 'snap · elements': [], 'snap · pixels only': []}
    by_kind = {}
    for t in sorted(Path(a.dir).glob('ui-*.truth.json')):
        T = json.load(open(t)); base = T['base']
        png = t.with_name(t.name.replace('.truth.json', '.png'))
        reg = json.load(open(t.with_name(t.name.replace('.truth.json', '.regions.json'))))
        dom, pix = snap.candidates(png, base, reg)
        for tg in T['targets']:
            for _ in range(a.guesses):
                g = guess(tg['rect'], rnd)
                v_raw = snap.iou(g, tg['rect'])
                b1, _, _ = snap.snap(g, dom, pix); b2, _, _ = snap.snap(g, [], pix)
                unpad = lambda b: [b[0] + 6, b[1] + 6, b[2] - 12, b[3] - 12] if b is not g else b
                v1, v2 = snap.iou(unpad(b1), tg['rect']), snap.iou(unpad(b2), tg['rect'])
                rows['raw'].append(v_raw); rows['snap · elements'].append(v1); rows['snap · pixels only'].append(v2)
                by_kind.setdefault(tg['kind'], []).append((v_raw, v1, v2))
    def line(name, v):
        n = len(v) or 1
        return f'{name:20s} mean IoU {sum(v) / n:.2f}   accurate (≥0.7) {sum(x >= 0.7 for x in v) / n:5.0%}   missed (<0.4) {sum(x < 0.4 for x in v) / n:5.0%}'
    print(f'{len(rows["raw"])} guesses on {len(list(Path(a.dir).glob("ui-*.truth.json")))} interfaces')
    for k, v in rows.items(): print(line(k, v))
    print('by kind (accurate: raw → elements → pixels):')
    for k, v in sorted(by_kind.items()):
        n = len(v)
        print(f'  {k:8s} {n:4d}  {sum(x[0] >= 0.7 for x in v) / n:4.0%} → {sum(x[1] >= 0.7 for x in v) / n:4.0%} → {sum(x[2] >= 0.7 for x in v) / n:4.0%}')


if __name__ == '__main__':
    main()
