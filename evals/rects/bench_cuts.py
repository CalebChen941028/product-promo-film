#!/usr/bin/env python3
"""Does scripts/snap.py cut_edges() tell a clean crop from one that cuts through content — on interfaces from no product?

  python3 evals/rects/bench_cuts.py evals/runs/rects [--seed 1]
Clean crop: a target element plus a 4 px margin (its own border; a wider margin can catch a neighbour, which IS a cut). Cut crop: the same element with one side pulled 15–35 % inside it.
Reports how many cut crops are caught (recall) and how many clean crops are flagged by mistake (false alarms)."""
import argparse, json, random, sys, tempfile
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / 'scripts'))
import snap  # noqa: E402

ap = argparse.ArgumentParser(); ap.add_argument('dir'); ap.add_argument('--seed', type=int, default=1); a = ap.parse_args()
rnd = random.Random(a.seed); tmp = Path(tempfile.mkdtemp())
caught = clean_flag = n_cut = n_clean = 0
for t in sorted(Path(a.dir).glob('ui-*.truth.json')):
    T = json.load(open(t)); bw, bh = T['base']
    im = Image.open(t.with_name(t.name.replace('.truth.json', '.png'))); k = im.size[0] / bw
    for tg in T['targets']:
        x, y, w, h = tg['rect']
        if w < 120 or h < 60: continue
        m = 4
        clean = [max(0, x - m), max(0, y - m), min(bw, x + w + m), min(bh, y + h + m)]
        side = rnd.choice(['left', 'right', 'top', 'bottom']); f = rnd.uniform(0.15, 0.35)
        cut = [x - m, y - m, x + w + m, y + h + m]
        if side == 'left': cut[0] = x + f * w
        if side == 'right': cut[2] = x + w - f * w
        if side == 'top': cut[1] = y + f * h
        if side == 'bottom': cut[3] = y + h - f * h
        cut = [max(0, cut[0]), max(0, cut[1]), min(bw, cut[2]), min(bh, cut[3])]
        for box, is_cut in ((clean, False), (cut, True)):
            p = tmp / 'c.png'; im.crop([round(v * k) for v in box]).save(p)
            got = snap.cut_edges(p)
            if is_cut: n_cut += 1; caught += side in got
            else: n_clean += 1; clean_flag += bool(got)
print(f'cut crops caught {caught}/{n_cut} = {caught / max(1, n_cut):.0%}   clean crops flagged {clean_flag}/{n_clean} = {clean_flag / max(1, n_clean):.0%}')
