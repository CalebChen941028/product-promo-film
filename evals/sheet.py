"""Contact sheets for blind scoring: what a critic needs to judge a film without watching it.

Usage: python sheet.py film.mp4 out_prefix [--film film.json]
Writes  <out_prefix>-sheet.jpg    20 frames at exact, evenly spaced times from 1.0 s to the end (never the fade from black)
        <out_prefix>-moments.jpg  dense strips: the hook (0.5–6 s), the hero (finale start −1 s … +5 s) and the last 5 s
Every frame is labelled with its true time. The hero time comes from film.json + film_out/build.json (the finale's first bar).
"""
import argparse
import io
import json
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw

FF = imageio_ffmpeg.get_ffmpeg_exe()


def duration(src):
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', subprocess.run([FF, '-i', src], capture_output=True, text=True).stderr)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def frame(src, t, w=480):
    png = subprocess.run([FF, '-v', 'error', '-ss', f'{t:.3f}', '-i', src, '-frames:v', '1', '-vf', f'scale={w}:-1', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                         capture_output=True).stdout
    return Image.open(io.BytesIO(png)).convert('RGB')


def label(dr, x, y, t, text=None):
    s = text or f'{int(t // 60):02d}:{t % 60:05.2f}'
    dr.rectangle([x + 4, y + 4, x + 8 + 7 * len(s), y + 24], fill='black'); dr.text((x + 8, y + 8), s, fill='yellow')


def hero_time(film_json):
    """Seconds where the finale starts (the hero moment), from film.json bars and film_out/build.json."""
    try:
        spec = json.load(open(film_json)); b = json.load(open(Path(film_json).parent / spec.get('out', 'film_out') / 'build.json'))
        bars = 0
        for sc in spec['scenes']:
            if sc['type'] == 'finale' or sc.get('hit') == 'hero': return b['G'] + b['BAR'] * bars
            bars += sc['bars'] if isinstance(sc.get('bars'), (int, float)) else 0
    except Exception:
        return None


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out'); ap.add_argument('--film')
    a = ap.parse_args()
    d = duration(a.src)
    sheet = Image.new('RGB', (1920, 1350)); dr = ImageDraw.Draw(sheet)
    for i in range(20):
        t = 1.0 + (d - 1.5) * i / 19
        x, y = (i % 4) * 480, (i // 4) * 270
        sheet.paste(frame(a.src, t), (x, y)); label(dr, x, y, t)
    sheet.save(a.out + '-sheet.jpg', quality=85)
    h = hero_time(a.film) if a.film else None
    rows = [('HOOK', [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5])]
    if h: rows.append(('HERO', [h - 1 + k for k in range(7)]))
    rows.append(('END', [d - 5 + k * 0.8 for k in range(7)]))
    W = 7 * 320
    mom = Image.new('RGB', (W, len(rows) * 210 + 10), (24, 24, 24)); dm = ImageDraw.Draw(mom)
    for r, (name, ts) in enumerate(rows):
        dm.text((8, r * 210 + 4), name, fill='white')
        for k, t in enumerate(ts):
            t = max(0.0, min(d - 0.05, t)); x, y = k * 320, r * 210 + 20
            mom.paste(frame(a.src, t, 320), (x, y)); label(dm, x, y, t)
    mom.save(a.out + '-moments.jpg', quality=85)
    print('duration', round(d, 2), 'hero', round(h, 2) if h else '—')
