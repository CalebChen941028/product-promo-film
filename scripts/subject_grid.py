"""Pick the subject of a photograph for the cold open: the film starts on this detail, then reveals the whole frame.

Usage: python subject_grid.py photo.jpg --preview DIR          → DIR/<photo>.grid.jpg with a labelled 4×4 grid (A–D × 1–4)
       python subject_grid.py photo.jpg --cells B2,C3 [--base W H] → prints the focus rect [x, y, w, h] in base units
Look at the grid, name the cell(s) the product or the telling detail sits in, and put the printed rect in the cover's
"focus" (film.json). Base default = the intake rule for photos (about 1920 wide).
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw

COLS, ROWS = 'ABCD', '1234'


def base_of(im, base=None):
    if base: return base
    w, h = im.size
    s = max(1, w / 1920)
    return [round(w / s), round(h / s)]


def rect(cells, base):
    bw, bh = base
    cw, ch = bw / 4, bh / 4
    xs, ys = [], []
    for c in cells:
        c = c.strip().upper()
        col, row = COLS.index(c[0]), ROWS.index(c[1])
        xs += [col * cw, (col + 1) * cw]; ys += [row * ch, (row + 1) * ch]
    return [round(min(xs)), round(min(ys)), round(max(xs) - min(xs)), round(max(ys) - min(ys))]


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('image'); ap.add_argument('--preview'); ap.add_argument('--cells'); ap.add_argument('--base', nargs=2, type=int)
    a = ap.parse_args()
    im = Image.open(a.image).convert('RGB')
    base = base_of(im, a.base)
    if a.preview:
        g = im.copy(); g.thumbnail((1600, 1600)); d = ImageDraw.Draw(g); W, H = g.size
        for k in range(1, 4):
            d.line([(W * k / 4, 0), (W * k / 4, H)], fill=(255, 60, 60), width=3); d.line([(0, H * k / 4), (W, H * k / 4)], fill=(255, 60, 60), width=3)
        for i, c in enumerate(COLS):
            for j, r in enumerate(ROWS):
                x, y = W * i / 4 + 10, H * j / 4 + 8
                d.rectangle([x - 4, y - 2, x + 46, y + 30], fill=(255, 60, 60)); d.text((x + 4, y + 4), c + r, fill='white', font_size=24)
        out = Path(a.preview) / (Path(a.image).stem + '.grid.jpg'); out.parent.mkdir(parents=True, exist_ok=True); g.save(out, quality=85)
        print(f'grid → {out}  (base {base}); then: --cells B2,C2')
    if a.cells:
        print(rect(a.cells.split(','), base))
