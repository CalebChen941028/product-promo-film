#!/usr/bin/env python3
"""Do a point's words correct a box written on the wrong element — on interfaces from no product?

  python3 evals/rects/bench_text.py evals/runs/rects [--seed 1] [--wrong 0.5]
A label imitates a mid-sized model: one or two words seen on the target plus filler ("一键", "auto"); the box lands on
the target (noisy) or, with probability --wrong, on another element nearby. Scored: final IoU with the true target
(accurate ≥ 0.7) for geometry only, words from the page's element texts, and words read by OCR (any screenshot)."""
import argparse, json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / 'scripts'))
import snap  # noqa: E402

ap = argparse.ArgumentParser(); ap.add_argument('dir'); ap.add_argument('--seed', type=int, default=1); ap.add_argument('--wrong', type=float, default=0.5)
a = ap.parse_args(); rnd = random.Random(a.seed)
FILL = ['一键', '自动', '清晰', 'at a glance', 'instantly', '实时', 'all in one']
def guess(r):
    x, y, w, h = r; sw, sh = w * rnd.uniform(0.75, 1.3), h * rnd.uniform(0.75, 1.3)
    cx, cy = x + w / 2 + rnd.gauss(0, 0.15) * w, y + h / 2 + rnd.gauss(0, 0.15) * h
    return [cx - sw / 2, cy - sh / 2, sw, sh]
res = {'geometry · elements': [], 'words · elements': [], 'geometry · pixels': [], 'words · OCR': []}; wrongs = []
for t in sorted(Path(a.dir).glob('ui-*.truth.json')):
    T = json.load(open(t)); base = T['base']
    png = t.with_name(t.name.replace('.truth.json', '.png'))
    reg = json.load(open(t.with_name(t.name.replace('.truth.json', '.regions.json'))))
    dom, pix = snap.candidates(png, base, reg)
    ocr = {'base': base, 'regions': snap.ocr_regions(png, base) + [{'kind': 'panel', 'text': '', 'rect': c} for c in pix]}
    tg = [x for x in T['targets'] if x.get('text')]
    for x in tg:
        words = [w for w in x['text'][0].split() if len(w) >= 2]   # the words of the element's own name or first line
        if not words: continue
        label = ' '.join(rnd.sample(words, min(len(words), rnd.choice([1, 2])))) + ' ' + rnd.choice(FILL)
        others = [o for o in tg if o is not x and snap.iou(o['rect'], x['rect']) < 0.3]
        wrong = others and rnd.random() < a.wrong
        g = guess(rnd.choice(others)['rect'] if wrong else x['rect']); wrongs.append(bool(wrong))
        unpad = lambda b: [b[0] + 6, b[1] + 6, b[2] - 12, b[3] - 12]
        b0, _, s0 = snap.snap(g, dom, pix); res['geometry · elements'].append(snap.iou(unpad(b0) if s0 != 'kept' else b0, x['rect']))
        b3, _, s3 = snap.snap(g, [], pix); res['geometry · pixels'].append(snap.iou(unpad(b3) if s3 != 'kept' else b3, x['rect']))
        b1, _, s1 = snap.snap_with_text(g, [label], reg, None, dom, pix); res['words · elements'].append(snap.iou(unpad(b1) if s1 != 'kept' else b1, x['rect']))
        b2, _, s2 = snap.snap_with_text(g, [label], ocr, None, [], pix); res['words · OCR'].append(snap.iou(unpad(b2) if s2 != 'kept' else b2, x['rect']))
n = len(res['geometry · elements'])
print(f'{n} labelled boxes, {a.wrong:.0%} written on the wrong element')
for k, v in res.items():
    r = [i for i, w in zip(v, wrongs) if not w]; wv = [i for i, w in zip(v, wrongs) if w]
    acc = lambda a_: sum(i >= 0.7 for i in a_) / max(1, len(a_))
    print(f'  {k:18s} accurate {acc(v):5.0%}   · box on the right element {acc(r):5.0%}   · box on a wrong element {acc(wv):5.0%}')
