"""Tile review stills into 2×2 contact sheets (1920×1080 each) with file names burned in.

Usage: python contact_sheet.py stills_dir      → stills_dir/sheet0.jpg, sheet1.jpg, …
Read every sheet. Check: UI windows vs the chapter label (top-left), captions vs content (bottom 250 px),
labels/tags overlapping, off-screen edges, transitions that go black, text too small to read at 1080p.
"""
import glob
import os
import sys

from PIL import Image, ImageDraw

d = sys.argv[1]
files = sorted(f for f in glob.glob(os.path.join(d, '*.png')))
for k in range(0, len(files), 4):
    sheet = Image.new('RGB', (1920, 1080))
    for i, f in enumerate(files[k:k + 4]):
        im = Image.open(f).convert('RGB').resize((960, 540))
        ImageDraw.Draw(im).text((10, 10), os.path.basename(f), fill=(255, 255, 0))
        sheet.paste(im, ((i % 2) * 960, (i // 2) * 540))
    sheet.save(os.path.join(d, f'sheet{k // 4}.jpg'), quality=86)
print('sheets:', (len(files) + 3) // 4)
