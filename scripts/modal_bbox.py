"""Find the bright modal/dialog box on a dimmed background in a 2× capture; prints [x, y, w, h] in CSS px.

Usage: python modal_bbox.py shots/tool_compute.png shots/dl_dialog.png [--thr 236] [--frac 0.25]
Works when the app dims/blurs the page behind a light dialog. If it returns the whole screen, raise --thr
or --frac, or read the rect off grid_overlay.py instead. Always eyeball the crop before using it.
"""
import argparse

import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('images', nargs='+')
ap.add_argument('--thr', type=int, default=236)
ap.add_argument('--frac', type=float, default=0.25)
a = ap.parse_args()
for p in a.images:
    im = np.asarray(Image.open(p).convert('L').resize((960, 540))).astype(int)
    m = im > a.thr
    rows = np.where(m.mean(1) > a.frac)[0]
    cols = np.where(m.mean(0) > a.frac)[0]
    if len(rows) and len(cols):
        x0, x1, y0, y1 = cols.min() * 2, cols.max() * 2, rows.min() * 2, rows.max() * 2
        print(f'{p}: [{x0}, {y0}, {x1 - x0}, {y1 - y0}]')
    else:
        print(f'{p}: no bright region')
