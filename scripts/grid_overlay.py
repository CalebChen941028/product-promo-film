"""Overlay a labelled coordinate grid (CSS px of a 1920×1080 viewport) on 2× captures, to read crop/highlight rects.

Usage: python grid_overlay.py out_dir shots/variables.png shots/tt_result.png ...
Look at the JPGs: red vertical lines every 100 px (bold every 500) with x labels, blue horizontal likewise.
Rects in the film are [x, y, w, h] in these CSS px, whatever the capture's pixel size.
"""
import os
import sys

from PIL import Image, ImageDraw

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for path in sys.argv[2:]:
    im = Image.open(path).convert('RGB').resize((1440, 810))
    d = ImageDraw.Draw(im)
    s = 1440 / 1920
    for x in range(0, 1920, 100):
        d.line([(x * s, 0), (x * s, 810)], fill=(255, 0, 0) if x % 500 == 0 else (255, 150, 150), width=1)
        d.text((x * s + 2, 2), str(x), fill=(200, 0, 0))
    for y in range(0, 1080, 100):
        d.line([(0, y * s), (1440, y * s)], fill=(0, 0, 255) if y % 500 == 0 else (150, 150, 255), width=1)
        d.text((2, y * s + 2), str(y), fill=(0, 0, 200))
    im.save(os.path.join(out, os.path.splitext(os.path.basename(path))[0] + '.jpg'), quality=80)
