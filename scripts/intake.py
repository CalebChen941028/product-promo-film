"""Material intake: scan what the user supplied, classify it, normalise media, and list what is still missing.

Usage:
  python intake.py materials/ --out build/ [--ffmpeg ffmpeg] [--no-transcode]

What it does
  images   → size, alpha, role guess (logo / desktop / phone / photo / cutout / figure), suggested `base` for win()
             photo = natural photograph; cutout = product on a transparent background (hero/lineup scenes)
             (captures ≥ 2400 px wide are treated as 2× → base = size / 2)
  videos   → duration/size/fps; transcoded to build/clips/<name>.webm (VP9, ≤1920 wide (screen recordings ≤3840), 30 fps, no audio)
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


def look(im, jpeg=False):
    """'photo' (natural image), 'ui' (screen/flat graphic) or 'cutout' (object on transparency), from pixel statistics.
    Screens are lossless and mostly pixel-identical (> 95 %); a JPEG between the extremes is a photo or an illustration."""
    import numpy as np
    a = np.asarray(im.convert('RGBA'))
    alpha = a[..., 3]
    if 0.15 < (alpha > 200).mean() < 0.85:
        return 'cutout'
    h, w = alpha.shape
    c = a[h // 4: h // 4 + min(512, h // 2), w // 4: w // 4 + min(512, w // 2), :3].astype(int)   # native-resolution centre patch
    d = np.abs(np.diff(c, axis=1)).sum(axis=2)
    same, edges = (d == 0).mean(), (d > 60).mean()     # screens: pixel-identical areas + sharp text edges; photos: neither
    if same < 0.25: return 'photo'
    if same > 0.95: return 'ui'
    if jpeg: return 'photo'
    if same > 0.9 or (same > 0.6 and edges > 0.004): return 'ui'
    return 'ui' if edges > 0.015 else 'photo'


items = []
for f in sorted(p for p in src.rglob('*') if p.is_file() and not p.name.startswith('.')):
    ext, rel = f.suffix.lower(), str(f.relative_to(src))
    if ext in IMG:
        im = Image.open(f); w, h = im.size
        alpha = im.mode in ('RGBA', 'LA') and im.getextrema()[-1][0] < 250
        ar = w / h
        kind = look(im, ext in ('.jpg', '.jpeg'))
        hint = f.stem.lower()
        if re.search(r'screen|screenshot|截图|界面|\bui\b|dashboard', hint): kind = 'ui'
        elif re.search(r'photo|lifestyle|shot|scene|product|实拍|照片|场景', hint) and kind != 'cutout': kind = 'photo'
        if alpha and 0.8 < ar < 1.25 and w <= 1200 and re.search(r'logo|icon|mark|标志', f.stem, re.I): role = 'logo'
        elif alpha and kind == 'cutout': role = 'cutout'            # product shot on a transparent background
        elif alpha and 0.8 < ar < 1.25 and w <= 1200: role = 'logo'
        elif kind == 'photo': role = 'photo'                         # photograph: lifestyle, product, people, place
        elif re.search(r'phone|mobile|ios|android|手机', hint): role = 'phone'
        elif ar < 0.75 and not re.search(r'plot|chart|graph|curve|figure|table|report|roc|km|forest|docx|pdf|图|表|报告', hint): role = 'phone'
        elif 1.45 < ar < 3 and w >= 1200: role = 'desktop'          # a very wide strip (a cropped table row) is a figure, not a screen
        else: role = 'figure'                                         # charts, cropped dialogs, tables, report pages
        scale = 2 if w >= 2400 else 1
        if role == 'phone': scale = 3 if w >= 1000 else (2 if w >= 700 else 1)
        if role in ('photo', 'cutout'): scale = max(1, w / 1920)          # photos: base ≈ 1920 wide
        it = {'file': rel, 'kind': 'image', 'role': role, 'size': [w, h], 'alpha': bool(alpha), 'base': [round(w / scale), round(h / scale)]}
        if role == 'photo' and not alpha:   # a packshot: the product on a plain near-white background (border bright and flat)
            import numpy as np
            g = np.asarray(im.convert('L').resize((240, max(1, round(240 * h / w))))).astype(float)
            bd = np.concatenate([g[:6].ravel(), g[-6:].ravel(), g[:, :6].ravel(), g[:, -6:].ravel()])
            if bd.mean() > 238 and bd.std() < 8 and g[g.shape[0] // 4: -g.shape[0] // 4, g.shape[1] // 4: -g.shape[1] // 4].std() > 12:
                it['packshot'] = True
        items.append(it)
    elif ext in VID:
        info = probe(f)
        it = {'file': rel, 'kind': 'video', **info}
        # screen recording or real footage? one frame from the middle, judged like a still (pixel-identical areas = a screen)
        try:
            mid = max(0.0, (info.get('duration') or 0) / 2)
            fr = out / 'clips' / (f.stem + '.poster.png'); fr.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run([a.ffmpeg, '-y', '-loglevel', 'error', '-ss', f'{mid:.2f}', '-i', str(f), '-frames:v', '1', str(fr)], check=True)
            it['role'] = 'screen' if look(Image.open(fr)) == 'ui' else 'footage'
            it['poster'] = str(fr)
        except Exception:
            it['role'] = 'footage' if re.search(r'film|shot|footage|broll|b-roll|product|实拍|视频', f.stem, re.I) else 'screen'
        if re.search(r'screen|record|录屏|界面|demo', f.stem, re.I): it['role'] = 'screen'
        if not a.no_transcode:
            dst = out / 'clips' / (f.stem + '.webm')
            cap = 3840 if it.get('role') == 'screen' else 1920   # a 4K screen recording keeps its pixels: the film zooms into the UI
            vf = f'scale=min({cap}\\,iw):-2,fps=30'
            # crf 20: text in a screen recording and texture in footage stay crisp (32 smeared both)
            subprocess.run([a.ffmpeg, '-y', '-loglevel', 'error', '-i', str(f), '-an', '-vf', vf, '-c:v', 'libvpx-vp9', '-crf', '20', '-b:v', '0', '-row-mt', '1', '-pix_fmt', 'yuv420p', str(dst)], check=True)
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

# a desktop product's tall crop (an AI panel, a side bar) is not a phone: with 3+ desktop screens and no phone in the name,
# a portrait UI is a figure (shown as a crop, never inside a phone frame)
if sum(1 for i in items if i.get('role') == 'desktop') >= 3:
    for i in items:
        if i.get('role') == 'phone' and not re.search(r'phone|mobile|ios|android|手机', Path(i['file']).stem, re.I):
            w, h = i['size']; sc = 2 if w >= 2400 else 1
            i['role'], i['base'] = 'figure', [round(w / sc), round(h / sc)]
json.dump({'materials': str(src.resolve()), 'items': items}, open(out / 'manifest.json', 'w'), ensure_ascii=False, indent=1)
count = lambda k, r=None: sum(1 for i in items if i['kind'] == k and (r is None or i.get('role') == r))
print(f"images {count('image')} (desktop {count('image', 'desktop')}, phone {count('image', 'phone')}, photo {count('image', 'photo')}, cutout {count('image', 'cutout')}, figure {count('image', 'figure')}, logo {count('image', 'logo')})"
      f" · videos {count('video')} · music {count('audio', 'music')} · voice {count('audio', 'voice')} · texts {count('text')}")
missing = []
packs = [i['file'] for i in items if i.get('packshot')]
if packs: missing.append(f'packshot on white ({", ".join(packs)}): used framed as the hero; for a cut-out hero or lineup, ask for a transparent PNG (no automatic masking: a white product on white cannot be cut out reliably)')
if not count('image', 'logo'): missing.append('logo (transparent PNG) — ask the user, or use the app icon from the repo (e.g. build/icon.png)')
if not count('audio', 'music'): missing.append('music — none supplied: make_film.py will compose an original underscore (make_music.py) unless the user provides a licensed track; never pick one from the web')
visual = sum(count('image', r) for r in ('desktop', 'phone', 'photo', 'cutout', 'figure')) + count('video')
if visual < 4: missing.append(f'visual material — only {visual} images/clips: ask for more real product shots or screens (software: capture_app.mjs; physical products: photos, ideally cut-outs on transparency)')
if not count('text', 'brief'): missing.append('brief — fill templates/brief.example.json with the user (name, one-liner, features, differentiators, contacts, style)')
print('missing:' if missing else 'nothing obviously missing')
for m in missing: print('  -', m)
print('manifest →', out / 'manifest.json')
