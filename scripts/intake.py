"""Material intake: scan what the user supplied, classify it, normalise media, and list what is still missing.

Usage:
  python intake.py materials/ --out build/ [--ffmpeg ffmpeg] [--no-transcode]

What it does
  images   → size, alpha, role guess (logo / desktop / phone / figure), suggested `base` for win()
             (captures ≥ 2400 px wide are treated as 2× → base = size / 2)
  videos   → duration/size/fps; transcoded to build/clips/<name>.webm (VP9, ≤1920 wide, 30 fps, no audio)
             because Playwright's Chromium cannot decode H.264 and WebM seeks frame-exactly
  audio    → duration; music converted to build/audio/<name>.wav (48 kHz); files named *vo*/*voice*/*narration*
             are flagged as user-recorded voice-over (then skip TTS)
  text     → brief.md / brief.json / brand.json / *.md / *.txt / *.pdf / *.docx are listed as copy sources
Writes build/manifest.json and prints a checklist. Role guesses are heuristics: confirm them with the user.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('materials'); ap.add_argument('--out', default='build')
ap.add_argument('--ffmpeg', default='ffmpeg'); ap.add_argument('--no-transcode', action='store_true')
a = ap.parse_args()
src, out = Path(a.materials), Path(a.out)
(out / 'clips').mkdir(parents=True, exist_ok=True); (out / 'audio').mkdir(parents=True, exist_ok=True)
IMG, VID = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tif', '.tiff'}, {'.mp4', '.mov', '.m4v', '.webm', '.mkv', '.avi'}
AUD, DOC = {'.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg'}, {'.md', '.txt', '.pdf', '.docx', '.json', '.pptx'}


def probe(path):
    r = subprocess.run([a.ffmpeg, '-hide_banner', '-i', str(path)], capture_output=True, text=True)
    info = r.stderr
    d = re.search(r'Duration: (\d+):(\d+):([\d.]+)', info)
    dur = int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3)) if d else None
    v = re.search(r'Video: .*?, (\d{2,5})x(\d{2,5})', info)
    fps = re.search(r'([\d.]+) fps', info)
    return {'duration': round(dur, 2) if dur else None, 'size': [int(v.group(1)), int(v.group(2))] if v else None, 'fps': float(fps.group(1)) if fps else None}


items = []
for f in sorted(p for p in src.rglob('*') if p.is_file() and not p.name.startswith('.')):
    ext, rel = f.suffix.lower(), str(f.relative_to(src))
    if ext in IMG:
        im = Image.open(f); w, h = im.size
        alpha = im.mode in ('RGBA', 'LA') and im.getextrema()[-1][0] < 250
        ar = w / h
        if alpha and 0.8 < ar < 1.25 and w <= 2048: role = 'logo'
        elif ar < 0.75: role = 'phone'
        elif ar > 1.45 and w >= 1200: role = 'desktop'
        else: role = 'figure'
        scale = 2 if w >= 2400 else 1
        if role == 'phone': scale = 3 if w >= 1000 else (2 if w >= 700 else 1)
        items.append({'file': rel, 'kind': 'image', 'role': role, 'size': [w, h], 'alpha': bool(alpha), 'base': [round(w / scale), round(h / scale)]})
    elif ext in VID:
        info = probe(f)
        it = {'file': rel, 'kind': 'video', **info}
        if not a.no_transcode:
            dst = out / 'clips' / (f.stem + '.webm')
            vf = 'scale=min(1920\\,iw):-2,fps=30'
            subprocess.run([a.ffmpeg, '-y', '-loglevel', 'error', '-i', str(f), '-an', '-vf', vf, '-c:v', 'libvpx-vp9', '-crf', '32', '-b:v', '0', '-row-mt', '1', '-pix_fmt', 'yuv420p', str(dst)], check=True)
            it['webm'] = str(dst)
        items.append(it)
    elif ext in AUD:
        info = probe(f)
        voice = bool(re.search(r'(^|[_\-\s])(vo|voice|narration|旁白|配音)', f.stem, re.I))
        it = {'file': rel, 'kind': 'audio', 'role': 'voice' if voice else 'music', 'duration': info['duration']}
        dst = out / 'audio' / (f.stem + '.wav')
        subprocess.run([a.ffmpeg, '-y', '-loglevel', 'error', '-i', str(f), '-ar', '48000', '-ac', '2', str(dst)], check=True)
        it['wav'] = str(dst)
        items.append(it)
    elif ext in DOC:
        items.append({'file': rel, 'kind': 'text', 'role': 'brief' if 'brief' in f.stem.lower() else ('brand' if 'brand' in f.stem.lower() else 'reference')})
    else:
        items.append({'file': rel, 'kind': 'other'})

json.dump({'materials': str(src.resolve()), 'items': items}, open(out / 'manifest.json', 'w'), ensure_ascii=False, indent=1)
count = lambda k, r=None: sum(1 for i in items if i['kind'] == k and (r is None or i.get('role') == r))
print(f"images {count('image')} (desktop {count('image', 'desktop')}, phone {count('image', 'phone')}, figure {count('image', 'figure')}, logo {count('image', 'logo')})"
      f" · videos {count('video')} · music {count('audio', 'music')} · voice {count('audio', 'voice')} · texts {count('text')}")
missing = []
if not count('image', 'logo'): missing.append('logo (transparent PNG) — ask the user, or use the app icon from the repo (e.g. build/icon.png)')
if not count('audio', 'music'): missing.append('music — ask for a licensed track (or use one the user owns); never pick one yourself from the web')
if count('image', 'desktop') + count('image', 'phone') + count('video') < 4: missing.append('real UI material — fewer than 4 screens/clips: capture more with capture_kit.mjs if the product can run')
if not count('text', 'brief'): missing.append('brief — fill templates/brief.example.json with the user (name, one-liner, features, differentiators, contacts, style)')
print('missing:' if missing else 'nothing obviously missing')
for m in missing: print('  -', m)
print('manifest →', out / 'manifest.json')
