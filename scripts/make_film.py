"""One-command film pipeline: film.json → checked spec → film page → voice-over → layout QA → video → mix → delivery.

Usage
  python make_film.py film.json                 # all stages
  python make_film.py film.json --stage check   # validate only (fast; run this after every edit of film.json)
  python make_film.py film.json --draft         # fast preview: no motion blur, quick encode (look, then go final)
  stages: check build vo qa render finish  (each needs the previous ones; `all` runs them in order)

Every problem is printed as  ERROR/WARN … followed by  FIX: …  — do exactly what FIX says, then rerun.
Outputs (in spec["out"], default ./film_out):
  film/            self-contained film page (open film/film.html?t=12 to look at second 12 in a browser)
  qa/              qa_report.json + contact sheets (sheet*.jpg) — read them before rendering
  final/<name>-1080p.mp4, <name>-cover-4k.png, <name>-cover-1280.jpg, <name>.{bilingual,zh,en}.srt
See references/film-spec.md for every field. Requires: python3 (numpy, Pillow), node + playwright, ffmpeg.
"""
import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
TPL = SKILL / 'templates'
STYLES = ['midnight-tech', 'keynote-light', 'editorial-mono', 'aurora-glass', 'neon-cyber', 'paper-academic', 'luxe-noir', 'natural-fresh']
MOTIONS = ['cinematic-3d', 'precision-data', 'kinetic-launch', 'gentle-story', 'playful-pop', 'editorial-type']
# minimum bars, required keys, list limits per scene type
TYPES = {
    'cover': (3, [], {}), 'pain': (3, [], {'items': 4}), 'feature': (3, ['media', 'points'], {'points': 4}),
    'carousel': (2, ['panels'], {'panels': 6}), 'numbers': (2, ['stats'], {'stats': 3, 'chips': 12}),
    'gallery': (2, ['items'], {'items': 8}), 'clip': (2, ['media'], {}), 'phone': (2, ['media'], {}),
    'compare': (3, ['rows'], {'rows': 6}), 'statement': (1, ['zh'], {}), 'finale': (4, ['media'], {}), 'endcard': (4, [], {}),
    # any product: photographs, cut-outs (transparent PNG), people and places
    'photo': (2, ['media'], {}), 'hero': (3, ['media'], {}), 'detail': (2, ['media'], {'crops': 4}),
    'lineup': (2, ['items'], {'items': 6}), 'quote': (2, ['zh', 'who'], {}),
}
GENRES = json.load(open(Path(__file__).resolve().parent.parent / 'templates' / 'genres.json'))['genres']
REST_BARS = 5   # legacy constant; use rest_bars(bpm)


def rest_bars(bpm):
    """End-card length when the music is composed: about 8 s (3–4 bars), plus one ring-out bar. Longer is dead air."""
    return max(3, round(8 / (240 / float(bpm or 100))))
MOODS = ['cold', 'neutral', 'peak', 'warm', 'night']
CUT_TYPES = ['style', 'whip', 'push']
LOOKS = ['teal-night', 'clean-bright', 'bleach-print', 'pastel-glow', 'neon-night', 'warm-print', 'noir-gold', 'sunlit', 'teal-orange', 'none']
errors, warns = [], []


def style_profile(style):
    """Read a style's defaults (motionDefault, grade, bloom, grain) from templates/styles/<id>.js."""
    src = (TPL / 'styles' / f'{style}.js').read_text() if (TPL / 'styles' / f'{style}.js').exists() else ''
    out = {}
    for k in ('motionDefault', 'grade'):
        m = re.search(k + r"\s*:\s*'([\w-]+)'", src); out[k] = m.group(1) if m else None
    for k in ('bloom', 'grain', 'xf'):
        m = re.search(k + r'\s*:\s*([\d.]+)', src); out[k] = float(m.group(1)) if m else 0.0
    return out


def resolve_look(spec):
    """Fill style/motion from the genre when they are "auto" or missing (genres.json), in place."""
    g = GENRES.get(spec.get('genre') or '', None)
    if spec.get('style') in (None, '', 'auto'):
        spec['style'] = g['style'][0] if g else 'midnight-tech'
    if spec.get('motion') in (None, 'auto'):
        spec['motion'] = g['motion'] if g else ''
    return spec


def has_alpha(path):
    try:
        from PIL import Image
        im = Image.open(path)
        return im.mode in ('RGBA', 'LA') and im.getextrema()[-1][0] < 250
    except Exception:
        return False


def music_mood(spec):
    """Underscore mood for a composed track: the genre's, else one that suits the style/motion."""
    gen = (spec.get('music') or {}).get('generate') or {}
    if gen.get('mood') not in (None, '', 'auto'): return gen['mood'], gen.get('bpm')
    g = GENRES.get(spec.get('genre') or '')
    if g: return g['music']['mood'], gen.get('bpm') or g['music']['bpm']
    by_style = {'luxe-noir': 'luxe-lounge', 'natural-fresh': 'warm-acoustic'}
    by_motion = {'cinematic-3d': 'cinematic-pulse', 'precision-data': 'minimal-electronic', 'kinetic-launch': 'minimal-electronic',
                 'gentle-story': 'warm-piano', 'playful-pop': 'bright-pop', 'editorial-type': 'warm-piano'}
    mo = spec.get('motion') or style_profile(spec['style'])['motionDefault'] or 'cinematic-3d'
    return by_style.get(spec['style'], by_motion.get(mo, 'cinematic-pulse')), gen.get('bpm')


def cinema_spec(spec):
    """film.json "cinema": "auto" (default) | "off" | {grade, grade_strength, bloom, grain, motion_blur, sfx, sfx_gain_db, lens}."""
    c = spec.get('cinema', 'auto')
    if c == 'off' or c is False:
        return {'on': False}
    c = {} if c in ('auto', True, None) else dict(c)
    sp = style_profile(spec.get('style', 'midnight-tech'))
    g = c.get('grade', 'auto')
    return {'on': True, 'grade': sp['grade'] or 'none' if g == 'auto' else g, 'grade_strength': float(c.get('grade_strength', 0.5)),
            'bloom': sp['bloom'] if c.get('bloom', 'auto') == 'auto' else float(c['bloom']),
            'grain': sp['grain'] if c.get('grain', 'auto') == 'auto' else float(c['grain']),
            'motion_blur': int(c.get('motion_blur', 4)), 'sfx': c.get('sfx', 'auto'), 'sfx_gain_db': float(c.get('sfx_gain_db', -2)),
            'lens': c.get('lens', {}), 'motion': spec.get('motion') or sp['motionDefault'] or 'cinematic-3d'}


def err(msg, fix): errors.append(f'ERROR {msg}\n  FIX: {fix}')
def _strings(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            if not str(k).startswith('_'): yield from _strings(v, f'{path}.{k}' if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from _strings(v, f'{path}[{i}]')
    elif isinstance(o, str): yield path, o
def warn(msg, fix): warns.append(f'WARN  {msg}\n  FIX: {fix}')
def zhlen(s): return sum(1 for ch in s or '' if '　' <= ch <= '鿿' or '＀' <= ch <= '￯')


def find_ffmpeg(spec):
    cand = [spec.get('tools', {}).get('ffmpeg'), os.environ.get('FFMPEG'), shutil.which('ffmpeg')]
    try:
        import imageio_ffmpeg
        cand.append(imageio_ffmpeg.get_ffmpeg_exe())
    except Exception:
        pass
    for c in cand:
        if c and Path(c).exists():
            return c
    return None


def find_playwright(spec):
    cand = [spec.get('tools', {}).get('node_modules'), os.environ.get('PLAYWRIGHT_NODE_MODULES'), SKILL / 'node_modules', Path.cwd() / 'node_modules']
    try:
        cand.append(subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip())
    except Exception:
        pass
    for c in cand:
        if c and (Path(c) / 'playwright').exists():
            return Path(c)
    return None


KOKORO_REPO = Path(os.path.expanduser(os.environ.get('HF_HOME', '~/.cache/huggingface'))) / 'hub' / 'models--hexgrad--Kokoro-82M'


def kokoro_python(v=None):
    """A Python with kokoro installed: voice.python, $KOKORO_PYTHON, or the standard ~/.venvs/kokoro."""
    for c in [(v or {}).get('python'), os.environ.get('KOKORO_PYTHON'), '~/.venvs/kokoro/bin/python']:
        if c and Path(os.path.expanduser(c)).exists(): return c
    return None


def kokoro_cached():
    """(model downloaded?, [voices already downloaded]) — nothing is downloaded by asking."""
    snaps = list((KOKORO_REPO / 'snapshots').glob('*')) if KOKORO_REPO.exists() else []
    model = any((d / 'kokoro-v1_0.pth').exists() for d in snaps)
    voices = sorted({f.stem for d in snaps for f in (d / 'voices').glob('*.pt')})
    return model, voices


def film_hashes(film):
    """Fingerprints of the files build writes into film_out/film (vo_timing.js is the vo stage's)."""
    import hashlib
    return {f.name: hashlib.sha1(f.read_bytes()).hexdigest()[:16] for f in sorted(film.glob('*.js')) if f.name != 'vo_timing.js'} | \
           {f.name: hashlib.sha1(f.read_bytes()).hexdigest()[:16] for f in film.glob('*.html')}


def guard_generated(out):
    """Stop if someone hand-edited the generated film page: film.json is the only source."""
    b = json.load(open(out / 'build.json'))
    if not b.get('hashes'): return
    now = film_hashes(out / 'film')
    edited = [k for k, h in b['hashes'].items() if now.get(k) != h]
    if edited:
        sys.exit(f"ERROR film_out/film/{edited[0]} was edited by hand ({len(edited)} file(s)).\n  FIX: never edit generated files — put the change in film.json "
                 f"(references/film-spec.md), then rerun --stage build. Hand edits are lost on every build.")


def treatment_gate(spec, spec_path):
    """Hard gate before build: the crew's treatment must pass check_treatment.py against this film.json."""
    t = spec.get('treatment', 'treatment.md')
    if t == 'skip':
        print('WARN  "treatment": "skip" — the crew was skipped. Say so in the report: this is a test cut, not a crew-approved film.'); return
    tp = (spec_path.parent / t)
    if not tp.exists():
        sys.exit(f'ERROR no treatment at {tp} — the crew has not run.\n  FIX: autofilm.py writes treatment.md; play the crew (references/crew.md) to fill it, '
                 f'then rerun. (Only for a throwaway test cut: "treatment": "skip" in film.json.)')
    r = subprocess.run([sys.executable, HERE / 'check_treatment.py', tp, spec_path], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        sys.exit('Build blocked: check_treatment.py must pass first (SKILL.md hard rule 5). Do what each FIX says — '
                 'redo the weak part of the treatment or the copy; never inflate a score — then rerun.')


def run(cmd, **kw):
    print('  $', ' '.join(str(c) for c in cmd)[:220])
    r = subprocess.run([str(c) for c in cmd], **kw)
    if r.returncode != 0:
        sys.exit(f'command failed ({r.returncode}): {cmd[0]} — read the output above')
    return r


# ---------------------------------------------------------------- check
def check(spec, base_dir):
    if spec.get('genre') and spec['genre'] != 'auto' and spec['genre'] not in GENRES:
        err(f"genre '{spec['genre']}' unknown", f'use one of {list(GENRES)} (scripts/genres.py --list)')
    resolve_look(spec)
    if spec.get('style') not in STYLES:
        err(f"style '{spec.get('style')}' unknown", f'use one of {STYLES} (scripts/recommend_style.py suggests one)')
    if spec.get('motion') and spec['motion'] not in MOTIONS:
        err(f"motion '{spec.get('motion')}' unknown", f"use one of {MOTIONS} or leave it empty for the style's default")
    b = spec.get('brand', {})
    for k in ['name', 'logo', 'positioningZh', 'positioningEn']:
        if not b.get(k):
            err(f'brand.{k} missing', 'fill it from the brief (templates/brief.example.json)')
    if b.get('logo') and not (base_dir / b['logo']).exists():
        err(f"brand.logo not found: {b['logo']}", 'path is relative to film.json; put a transparent PNG there')
    mus = (spec.get('music') or {}).get('file')
    if mus and not (base_dir / mus).exists():
        err(f'music.file not found: {mus}', 'fix the path (relative to film.json), or remove "file" to have an original underscore composed')
    if not mus:
        mood, _ = music_mood(spec)
        warns.append(f'NOTE  no music file → an original underscore will be composed ({mood}); a licensed track from the user is still preferred for a hero film')
    todo = [p for p, v in _strings(spec) if 'TODO' in v]
    for p in todo[:20]:
        err(f'copy not written: {p}', 'write it (crew: copywriter, references/crew.md) — or remove the field/scene')
    sys.path.insert(0, str(HERE))
    import lint_copy
    for p, prob, fix in lint_copy.lint(spec)[:25]:
        warn(f'copy {p}: {prob}', fix)
    c = spec.get('cinema', 'auto')
    if isinstance(c, dict):
        if c.get('grade', 'auto') not in LOOKS + ['auto']:
            err(f"cinema.grade '{c.get('grade')}' unknown", f'use auto or one of {LOOKS} (scripts/grade.py --list)')
        if not 0 <= float(c.get('grade_strength', 0.6)) <= 1:
            err('cinema.grade_strength must be 0–1', 'use 0.4–0.7; above 0.8 can hurt UI legibility')
        if int(c.get('motion_blur', 4)) not in range(1, 9):
            err('cinema.motion_blur must be 1–8 samples', 'use 4 (final) or 1 (off); --draft forces 1')
        if c.get('sfx', 'auto') not in ('auto', 'off'):
            err("cinema.sfx must be 'auto' or 'off'", 'sound design cues are generated from the scenes')
    elif c not in ('auto', 'off', True, False, None):
        err(f'cinema = {c!r}', 'use "auto" (default), "off", or an object — see references/director.md')
    scenes = spec.get('scenes', [])
    if not scenes:
        err('no scenes', 'start from templates/film.example.json')
    if scenes and scenes[0].get('type') != 'cover':
        warn('first scene is not a cover', 'put {"type": "cover", "bars": 3} first — the cover frame is also the poster')
    if scenes and scenes[-1].get('type') != 'endcard':
        warn('last scene is not an endcard', 'end with {"type": "endcard", "bars": "rest"}')
    roles = {}   # intake's role per material (desktop/phone/photo/cutout…), when autofilm/intake ran
    man = base_dir / 'build' / 'manifest.json'
    if man.exists():
        m = json.load(open(man))
        roles = {str((Path(m['materials']) / it['file']).resolve()): it.get('role') for it in m.get('items', [])}
    for i, sc in enumerate(scenes):
        t, where = sc.get('type'), f'scenes[{i}] ({sc.get("type")})'
        if t not in TYPES:
            err(f'{where}: unknown type', f'use one of {list(TYPES)}'); continue
        mn, req, lim = TYPES[t]
        if sc.get('mood') and sc['mood'] not in MOODS:
            err(f"{where}: mood '{sc['mood']}' unknown", f'use one of {MOODS} (colour script, references/director.md)')
        if 'hit' in sc and sc['hit'] not in (True, False, 'hero'):
            err(f"{where}: hit = {sc['hit']!r}", 'use true, false, or "hero" (the one biggest beat of the film)')
        if sc.get('cut') and sc['cut'] not in CUT_TYPES:
            err(f"{where}: cut '{sc['cut']}' unknown", f'use one of {CUT_TYPES}')
        bars = sc.get('bars')
        if bars != 'rest' and (not isinstance(bars, (int, float)) or bars < mn):
            err(f'{where}: bars={bars} (minimum {mn})', f'set "bars" to ≥ {mn} (1 bar = 4 beats; 120 BPM → 2 s)')
        if t == 'feature' and isinstance(bars, (int, float)) and bars < 1 + len(sc.get('points', [])):
            err(f'{where}: {len(sc.get("points", []))} points need ≥ {1 + len(sc.get("points", []))} bars', 'add bars or remove points')
        for k in req:
            if not sc.get(k):
                err(f'{where}: "{k}" missing', f'see references/film-spec.md → {t}')
        for k, mx in lim.items():
            if len(sc.get(k, [])) > mx:
                err(f'{where}: {len(sc[k])} {k} (max {mx})', f'keep the {mx} strongest {k}; split into another scene')
        media = []
        for key in ['media']:
            v = sc.get(key)
            media += v if isinstance(v, list) else ([v] if v else [])
        if sc.get('image'): media.append(sc['image'])
        if sc.get('backdrop'): media.append(sc['backdrop'])
        if sc.get('hero') and sc['hero'] not in ('result', 'rise', 'stack', 'wall'):
            err(f'{where}: hero = {sc["hero"]!r}', 'use "result" (one real screen), "rise" (one output rises out of the UI), "stack" (a cascade of outputs) or "wall"')
        media += [p.get('media') for p in sc.get('panels', [])] + [it.get('media') for it in sc.get('items', []) if isinstance(it, dict)]
        for m in filter(None, media):
            if not (base_dir / m).exists():
                err(f'{where}: media not found: {m}', 'path is relative to film.json; run intake.py and use its paths')
            elif t == 'clip' and not m.endswith('.webm'):
                err(f'{where}: clip must be .webm (Chromium cannot decode H.264)', 'run intake.py — it converts videos to build/clips/*.webm')
        basewh = sc.get('base', [1920, 1080])
        # holds that read as empty: silent texture, one object held long, a spec list on a photo card, a cold open on a texture
        if not sc.get('say') and isinstance(bars, (int, float)) and ((t == 'detail' and bars > 2) or (t in ('hero', 'photo', 'feature') and bars > 3)):
            warn(f'{where}: {bars} bars with no voice on one image', 'a silent hold over ~6 s reads as empty: 2 bars, or give it a line')
        if t == 'hero' and isinstance(bars, (int, float)) and bars > 3 and not isinstance(sc.get('media'), list):
            warn(f'{where}: one image held {bars} bars', 'a single-image reveal lands in 3 bars; more angles (a media list) can hold longer')
        if t == 'feature' and sc.get('frame') == 'photo' and len(sc.get('points', [])) > 2:
            warn(f'{where}: {len(sc["points"])} points on a photo', 'a spec list dilutes the idea: keep ≤ 2 points that serve it, or use a "photo" scene with one line')
        if t == 'detail' and not sc.get('say') and not any(c.get('zh') or c.get('en') for c in sc.get('crops', [])):
            warn(f'{where}: a silent texture with no purpose', 'give it a line or a labelled crop (what are we looking at, and why it matters) — or cut it')
        if t == 'cover' and isinstance(sc.get('media'), str) and re.search(r'detail|texture|macro|grain|close|特写|纹理', sc['media'], re.I):
            warn(f'{where}: the cold open is a texture ({sc["media"]})', 'open on an image with a subject (a place, a person, the product in use); textures belong in the detail beat')
        if t == 'feature' and sc.get('frame') == 'photo' and isinstance(sc.get('media'), str) and roles.get(str((base_dir / sc['media']).resolve())) in ('desktop', 'phone', 'figure'):
            err(f'{where}: "frame": "photo" on a screenshot ({sc["media"]})', 'screens get highlight boxes, not a photo frame: remove "frame" and give each point a rect '
                f'(python3 {HERE / "suggest_rects.py"} {sc["media"]} --preview . suggests them)')
        for j, p in enumerate(sc.get('points', [])):
            r = p.get('rect')
            if r is None:
                if sc.get('frame') != 'photo':
                    warn(f'{where}.points[{j}]: no rect → no highlight box', f'python3 {HERE / "suggest_rects.py"} {sc.get("media")} --preview . → copy the numbered rect this point talks about; real photos ("frame": "photo") need none')
            elif len(r) != 4:
                err(f'{where}.points[{j}]: rect must be [x,y,w,h]', 'measure it with grid_overlay.py on the screenshot (base coordinates)')
            elif r[0] < 0 or r[1] < 0 or r[0] + r[2] > basewh[0] + 1 or r[1] + r[3] > basewh[1] + 1:
                err(f'{where}.points[{j}]: rect {r} outside base {basewh}', 'rects are in base units (CSS px of the capture); check base and rect')
            elif r[2] * r[3] > 0.3 * basewh[0] * basewh[1]:
                warn(f'{where}.points[{j}]: rect covers {r[2] * r[3] / (basewh[0] * basewh[1]):.0%} of the screen', 'a box around everything highlights nothing: box only the region this point names (suggest_rects.py --preview)')
            if zhlen(p.get('zh')) > 14:
                warn(f'{where}.points[{j}]: zh label {zhlen(p.get("zh"))} chars', 'keep on-screen labels ≤ 14 Chinese characters')
        for j, s in enumerate(sc.get('say', [])):
            if zhlen(s.get('zh')) > 30:
                warn(f'{where}.say[{j}]: Chinese caption {zhlen(s.get("zh"))} chars (one line fits ~30)', 'shorten the zh line')
            if len(s.get('en', '')) > 110:
                warn(f'{where}.say[{j}]: English line {len(s["en"])} chars', 'shorten to ≤ 110 characters (~18 words)')
            if not s.get('en'):
                err(f'{where}.say[{j}]: "en" missing', 'every narration line needs the spoken English (and zh caption)')
    for k in ('ffmpeg',):
        if not find_ffmpeg(spec):
            err('ffmpeg not found', 'pip install imageio-ffmpeg  (or install ffmpeg)  — then rerun')
    if not find_playwright(spec):
        err('playwright not found', f'cd "{SKILL}" && npm i playwright && npx playwright install chromium')


# ---------------------------------------------------------------- composed music (no track supplied)
ENERGY = {'cover': 0, 'pain': 1, 'statement': 1, 'photo': 1, 'detail': 1, 'quote': 1, 'phone': 1, 'feature': 1, 'clip': 2, 'carousel': 2,
          'numbers': 2, 'gallery': 2, 'compare': 2, 'lineup': 2, 'hero': 2, 'finale': 3, 'endcard': 0}


def compose_music(spec, wav, grid_path):
    """Compose an original underscore bar-for-bar from the scene plan (make_music.py): sections change on the cuts."""
    sys.path.insert(0, str(HERE)); import make_music
    mood, bpm = music_mood(spec)
    gen = (spec.get('music') or {}).get('generate') or {}
    energy, hero, b = [], None, 0
    scenes = spec['scenes']; total = sum(sc['bars'] for sc in scenes if sc.get('bars') != 'rest')
    for i, sc in enumerate(scenes):
        nb = rest_bars(bpm or make_music.MOODS[mood]['bpm']) if sc.get('bars') == 'rest' else int(sc['bars'])
        e = sc.get('energy', ENERGY.get(sc['type'], 1))
        if sc['type'] == 'feature' and 'energy' not in sc and b > total * 0.45: e = 2      # second half of the story lifts
        if (sc['type'] == 'finale' or sc.get('hit') == 'hero') and hero is None: hero = b
        energy += [e] * nb; b += nb
    energy += [0]   # one bar of ring-out after the end card
    x, grid = make_music.compose(mood, float(bpm or make_music.MOODS[mood]['bpm']), energy, hero, int(gen.get('seed', 3)))
    make_music.write(wav, x); json.dump(grid, open(grid_path, 'w'), indent=1)
    print(f'  music: composed {mood} {grid["bpm"]:.0f} BPM, {len(energy)} bars ({len(x) / make_music.SR:.0f} s), hero on bar {hero} — original, royalty-free')


# ---------------------------------------------------------------- build
def build(spec, base_dir, out):
    ff = find_ffmpeg(spec)
    film, aud = out / 'film', out / 'audio'
    for d in (film / 'media', film / 'styles', aud):
        d.mkdir(parents=True, exist_ok=True)
    music_wav = aud / 'music.wav'
    mus = spec.get('music') or {}
    if mus.get('file'):
        run([ff, '-y', '-loglevel', 'error', '-i', base_dir / mus['file'], '-ar', '48000', '-ac', '2', music_wav])
        run([sys.executable, HERE / 'beat_grid.py', music_wav, '--ffmpeg', ff, '--out', aud / 'grid.json'], stderr=subprocess.DEVNULL)
    else:
        compose_music(spec, music_wav, aud / 'grid.json')
    grid = json.load(open(aud / 'grid.json'))
    G, BAR = grid['first_beat'], grid['bar_seconds']
    ext = mus.get('extend')
    final_wav = music_wav
    if ext:
        final_wav = aud / 'music_ext.wav'
        run([sys.executable, HERE / 'extend_music.py', music_wav, final_wav, '--grid', G, '--bar', BAR, '--repeat-from-bar', ext['from_bar'], '--repeat-to-bar', ext['to_bar'], '--times', ext.get('times', 1)])
    import wave
    with wave.open(str(final_wav)) as w:
        dur = w.getnframes() / w.getframerate()
    total_bars = int((dur - G - 1.0) // BAR)
    fixed = sum(sc['bars'] for sc in spec['scenes'] if sc.get('bars') != 'rest')
    rest = [sc for sc in spec['scenes'] if sc.get('bars') == 'rest']
    if fixed > total_bars or (rest and fixed + 4 * len(rest) > total_bars):
        sys.exit(f"ERROR scenes need {fixed} bars but the music has {total_bars} ({dur:.0f} s).\n  FIX: shorten scenes, or extend the music: \"music\": {{\"extend\": {{\"from_bar\": A, \"to_bar\": B}}}} — pick a chorus span from {aud / 'grid.json'} (see references/audio.md).")
    if not rest and total_bars - fixed > 6:
        print(f'WARN  {total_bars - fixed} bars of music left unused — set the last scene to "bars": "rest"')
    each_rest = (total_bars - fixed) // max(1, len(rest))
    if grid.get('generated'):
        each_rest = rest_bars(grid['bpm'])
        dur = min(dur, G + BAR * (fixed + each_rest * len(rest) + 1))   # end on the ring-out bar, not the reverb tail (the mix fades it)
    # hi-energy bars → chorus ranges (background pulse)
    his = [bb['hi'] for bb in grid['bars']]
    q = sorted(his)[int(len(his) * 0.66)] if his else 1
    chorus, cur = [], None
    for i, h in enumerate(his + [0] * 64):
        if i >= total_bars: break
        if h >= q and cur is None: cur = i
        if h < q and cur is not None:
            if i - cur >= 4: chorus.append([cur, i])
            cur = None
    # copy engine + media, lay scenes on bars, collect narration
    for f in ['film.html', 'engine.js', 'cinema.js', 'patterns.js', 'library.js']:
        shutil.copy(TPL / f, film / f)
    for f in (TPL / 'styles').glob('*'):
        shutil.copy(f, film / 'styles' / f.name)
    copied = {}

    def media(p, trim=False):
        if not p: return p
        key = (p, trim)
        if key not in copied:
            src = base_dir / p
            dst = film / 'media' / f'{len(copied):02d}-{"t-" if trim else ""}{Path(p).name}'
            if src.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp'):
                # downscale huge captures: coordinates live in `base` units, so pixels can shrink freely.
                # Keeps every render worker's memory low (4K screenshots × 6 workers swaps a 24 GB machine).
                from PIL import Image
                im = Image.open(src)
                if trim and im.mode in ('RGBA', 'LA') and im.getextrema()[-1][0] < 250:   # hero/lineup only: they ignore `base`
                    bb = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()   # cut-out: trim the empty margin
                    if bb and (bb[2] - bb[0]) * (bb[3] - bb[1]) < 0.8 * im.width * im.height:
                        pad = int(0.04 * max(bb[2] - bb[0], bb[3] - bb[1]))
                        im = im.crop((max(0, bb[0] - pad), max(0, bb[1] - pad), min(im.width, bb[2] + pad), min(im.height, bb[3] + pad)))
                        im.save(dst); copied[key] = 'media/' + dst.name; return copied[key]
                if im.width > 2400 and im.width >= im.height:
                    im = im.resize((2400, round(im.height * 2400 / im.width)), Image.LANCZOS)
                    im.save(dst, quality=92) if dst.suffix.lower() in ('.jpg', '.jpeg') else im.save(dst)
                else:
                    shutil.copy(src, dst)
            else:
                shutil.copy(src, dst)
            copied[key] = 'media/' + dst.name
        return copied[key]
    brand = dict(spec['brand']); brand['logo'] = media(brand['logo'])
    lines, calls, chapters, b0, segs = [], [], [], 0, []
    for i, sc in enumerate(spec['scenes']):
        nb = each_rest if sc.get('bars') == 'rest' else sc['bars']
        b1 = b0 + nb
        segs.append((sc, b0, b1))
        o = {k: v for k, v in sc.items() if k not in ('type', 'bars', 'say', 'chapter', 'mood', 'cut', 'hit', 'energy')}
        if sc['type'] in ('hero', 'lineup') and 'cutout' not in o:   # transparent PNG → stand it on the stage
            first = ([sc.get('media')] if isinstance(sc.get('media'), str) else (sc.get('media') or [])) + [it.get('media') for it in sc.get('items', [])]
            o['cutout'] = bool(first and first[0] and has_alpha(base_dir / first[0]))
        tr = sc['type'] in ('hero', 'lineup') and o.get('cutout')
        if isinstance(o.get('media'), list): o['media'] = [media(m, tr) for m in o['media']]
        elif o.get('media'): o['media'] = media(o['media'], tr)
        if o.get('image'): o['image'] = media(o['image'])
        if o.get('backdrop'): o['backdrop'] = media(o['backdrop'])
        for p in o.get('panels', []): p['media'] = media(p['media'])
        for it in o.get('items', []):
            if isinstance(it, dict) and it.get('media'): it['media'] = media(it['media'], tr)
        calls.append(f"LIB.{sc['type']}(bar({b0}), {'CONFIG.DUR' if i == len(spec['scenes']) - 1 else f'bar({b1})'}, {json.dumps(o, ensure_ascii=False)});")
        if sc.get('chapter'):
            n, zh, en = sc['chapter']; chapters.append([b0, b1, n, zh, en])
        says = sc.get('say', [])
        for k, s in enumerate(says):
            at = s.get('at', 0.3 + k * nb / max(1, len(says)))
            lines.append({'id': s.get('id', f's{i}_{k}'), 'bar': round(b0 + at, 3), 'end_bar': b1, 'en': s['en'], 'zh': s.get('zh', ''), **({'cap': s['cap']} if s.get('cap') else {})})
        b0 = b1
    # merge adjacent chapter entries with the same number
    merged = []
    for c in chapters:
        if merged and merged[-1][2] == c[2] and merged[-1][1] == c[0]: merged[-1][1] = c[1]
        else: merged.append(c)
    onscreen = [l['id'] for l in lines if l['id'] in ('tagline', 'motto')]
    cin = cinema_spec(spec)
    cin_cfg, cues = direct(cin, segs, G, BAR, dur)
    cfg = {'STYLE': spec['style'], 'MOTION': spec.get('motion', ''), 'G': G, 'BAR': BAR, 'DUR': round(dur, 3), 'FADE_OUT': 2.6,
           'CHORUS_BARS': chorus, 'CHAPTERS': merged, 'ONSCREEN': onscreen, 'SHOTS': 'media/', 'ASSETS': 'media/', 'BRAND': brand,
           'CINEMA': cin_cfg}
    json.dump(cues, open(aud / 'sfx_cues.json', 'w'), indent=1)
    (film / 'config.js').write_text('const CONFIG = ' + json.dumps(cfg, ensure_ascii=False, indent=1) + ';\nconst bar = (b) => CONFIG.G + CONFIG.BAR * b;\nObject.assign(window, { CONFIG, bar });\n')
    (film / 'scenes.js').write_text("'use strict';\n// generated by make_film.py from film.json — edit film.json, not this file\n" + '\n'.join(calls) + '\n')
    lines.sort(key=lambda l: l['bar'])
    json.dump(lines, open(out / 'narration.json', 'w'), ensure_ascii=False, indent=1)
    if not (film / 'vo_timing.js').exists():  # captions-only placeholder until the vo stage runs
        est = [{'id': l['id'], 's': G + BAR * l['bar'], 'e': G + BAR * l['bar'] + len(l['en'].split()) / 2.5, 'zh': l['zh'], 'en': l.get('cap', l['en'])} for l in lines]
        (film / 'vo_timing.js').write_text('const VO = ' + json.dumps(est, ensure_ascii=False) + ';\nwindow.VO = VO;\n')
    json.dump({'G': G, 'BAR': BAR, 'DUR': dur, 'music': str(final_wav), 'bars_used': b0, 'bars_total': total_bars, 'cinema': cin,
               'hashes': film_hashes(film)}, open(out / 'build.json', 'w'), indent=1)
    nm = find_playwright(spec)
    link = out / 'node_modules'
    if not link.exists(): link.symlink_to(nm)
    tools = out / 'tools'; tools.mkdir(exist_ok=True)   # node resolves 'playwright' from the script's folder upward
    for f in ['render.mjs', 'cover.mjs', 'qa_check.mjs']:
        shutil.copy(HERE / f, tools / f)
    if cin['on']:
        print(f"cinema: grade {cin['grade']} ×{cin['grade_strength']} · bloom {cin['bloom']} · grain {cin['grain']} · motion blur {cin['motion_blur']} · "
              f"{len(cin_cfg['hits'])} hits · cuts {sum(c != 'style' for c in cin_cfg['cuts'])} camera · {len(cues)} sound cues")
    print(f'built {len(calls)} scenes on {b0} bars · music {dur:.1f} s · BPM {grid["bpm"]} · {len(lines)} narration lines → {film}/film.html')


# ---------------------------------------------------------------- direction (colour script, hits, cuts, light, sound)
AUTO_MOOD = {'pain': 'cold', 'numbers': 'peak', 'finale': 'peak', 'endcard': 'warm', 'quote': 'warm'}
# sound palette per motion language: what a cut, a hit, a logo and a small item sound like
PALETTE = {
    'cinematic-3d':   {'cut': 'whoosh', 'hit': 'impact', 'logo': 'shimmer', 'item': 'tick', 'riser': True},
    'precision-data': {'cut': 'paper',  'hit': 'thud',   'logo': 'chime',   'item': 'tick', 'riser': False},
    'kinetic-launch': {'cut': 'whip',   'hit': 'impact', 'logo': 'shimmer', 'item': 'tick', 'riser': True},
    'gentle-story':   {'cut': 'swell',  'hit': 'swell',  'logo': 'chime',   'item': None,   'riser': False},
    'playful-pop':    {'cut': 'whip',   'hit': 'thud',   'logo': 'shimmer', 'item': 'pop',  'riser': False},
    'editorial-type': {'cut': 'paper',  'hit': 'thud',   'logo': 'chime',   'item': 'type', 'riser': False},
}


def direct(cin, segs, G, BAR, dur):
    """The director's pass: moods, hit points, camera cuts, light rays and the sound-design cue sheet."""
    if not cin['on']:
        return {'on': False}, []
    T = lambda b: round(G + BAR * b, 4)
    mo = cin['motion']; pal = PALETTE.get(mo, PALETTE['cinematic-3d'])
    moods, hits, rays, cuts, cues = [], [], [], [], []
    # restraint: ONE hero moment carries the flare, the impact and the riser; everything else stays quiet
    types = [sc['type'] for sc, _, _ in segs]
    hero_i = next((i for i, (sc, _, _) in enumerate(segs) if sc.get('hit') == 'hero'), None)
    if hero_i is None and 'finale' in types and segs[types.index('finale')][0].get('hit', True) is not False:
        hero_i = types.index('finale')
    prev_ch = None
    for i, (sc, b0, b1) in enumerate(segs):
        t0, t1, typ = T(b0), (round(dur, 3) if i == len(segs) - 1 else T(b1)), sc['type']
        moods.append([0 if i == 0 else t0, t1, sc.get('mood') or AUTO_MOOD.get(typ, 'neutral')])
        auto_hit = typ in ('numbers', 'finale', 'hero') or (i > 0 and segs[i - 1][0]['type'] == 'pain')
        hit = bool(sc.get('hit', auto_hit)) and i > 0
        hero = i == hero_i
        if hit or hero: hits.append(t0)
        ch = (sc.get('chapter') or [None])[0]
        new_ch = bool(ch and ch != prev_ch)
        if i == 0: cut = 'style'
        elif sc.get('cut'): cut = sc['cut']
        elif typ == 'endcard': cut = 'style'
        elif mo == 'kinetic-launch': cut = 'whip' if (hero or new_ch) else 'style'
        elif mo == 'cinematic-3d': cut = 'push' if (hero or (hit and segs[i - 1][0]['type'] == 'pain')) else 'style'
        elif mo == 'playful-pop': cut = 'whip' if hero else 'style'
        else: cut = 'style'
        cuts.append(cut)
        if ch: prev_ch = ch
        if typ == 'cover': rays.append([t0, t1, -150, 0.7]); cues.append({'t': t0 + 0.3, 'kind': pal['logo'], 'gain_db': -4})
        if hero: rays.append([t0, t1, -30, 1])
        if typ == 'endcard': cues.append({'t': t0 + 0.1, 'kind': pal['logo'], 'gain_db': -8})
        # sound only where the picture moves the camera or lands a hit — never a whoosh on every cut
        if i > 0 and (cut != 'style' or hit or hero):
            cues.append({'t': t0, 'kind': pal['cut'], 'gain_db': -2 if cut != 'style' else -6})
        if hero:
            cues.append({'t': t0, 'kind': pal['hit'], 'size': 1.2})
            if pal['riser']:
                cues.append({'t': t0, 'kind': 'riser', 'len': round(min(4.0, BAR * 2), 2), 'gain_db': -4})
        elif hit:
            cues.append({'t': t0, 'kind': 'thud' if pal['hit'] != 'swell' else 'swell', 'gain_db': -8})
        if pal['item'] and typ == 'numbers':
            cues += [{'t': t0 + 0.1 + k * 0.4, 'kind': pal['item'], 'gain_db': -4} for k in range(len(sc.get('stats', [])))]
    if cin['sfx'] == 'off':
        cues = []
    seen, uniq = set(), []
    for c in cues:   # one sound of a kind per moment
        k = (round(c['t'], 2), c['kind'])
        if k not in seen: seen.add(k); uniq.append(c)
    cues = uniq
    cfg = {'on': True, 'moods': moods, 'hits': hits, 'hero': T(segs[hero_i][1]) if hero_i is not None else None, 'rays': rays, 'cuts': cuts, 'cuts_t': [T(b0) for _, b0, _ in segs[1:]],
           'lens': cin['lens'], 'mb': cin['motion_blur']}
    return cfg, sorted(cues, key=lambda c: c['t'])


# ---------------------------------------------------------------- vo
def vo(spec, base_dir, out):
    v = spec.get('voice', {'engine': 'kokoro'})
    b = json.load(open(out / 'build.json'))
    eng = v.get('engine', 'kokoro')
    if eng == 'none':
        print('voice.engine = none → captions only (timing estimated)'); return
    if eng == 'files':  # user recordings: {"files": {"<line id>": "path.wav"}}
        vod = out / 'vo'; vod.mkdir(exist_ok=True)
        ff = find_ffmpeg(spec); timing = []
        for l in json.load(open(out / 'narration.json')):
            src = v.get('files', {}).get(l['id'])
            if not src: continue
            dst = vod / f"{l['id']}.wav"
            run([ff, '-y', '-loglevel', 'error', '-i', base_dir / src, '-ar', '24000', '-ac', '1', dst])
            import wave
            with wave.open(str(dst)) as w: d = w.getnframes() / w.getframerate()
            s = b['G'] + b['BAR'] * l['bar']
            timing.append({'id': l['id'], 's': round(s, 3), 'e': round(s + d, 3), 'zh': l['zh'], 'en': l.get('cap', l['en'])})
        json.dump(timing, open(vod / 'vo_timing.json', 'w'), ensure_ascii=False, indent=1)
        (out / 'film' / 'vo_timing.js').write_text('const VO = ' + json.dumps(timing, ensure_ascii=False) + ';\nwindow.VO = VO;\n')
        return
    py = kokoro_python(v)
    if not py:
        sys.exit('ERROR no Python with kokoro found (voice.python, $KOKORO_PYTHON, ~/.venvs/kokoro).\n  FIX: ask the user before installing (≈ 650 MB, references/audio.md "Kokoro setup") — or set "voice": {"engine": "none"} for captions only.')
    model, cached = kokoro_cached()
    want = v.get('voice', 'am_michael')
    if not v.get('allow_download') and (not model or want not in cached):
        what = 'the Kokoro model (≈ 330 MB)' if not model else f'the voice {want} (≈ 0.5 MB)'
        sys.exit(f'ERROR {what} is not downloaded, and downloads need the user\'s OK (SKILL.md hard rule 3).\n'
                 f'  FIX: use a voice that is already here: {cached or "none"} (set "voice": {{"voice": "{cached[0] if cached else "…"}"}}), '
                 f'or ask the user — name it, source huggingface.co/hexgrad/Kokoro-82M, size — and only after a yes set "allow_download": true. '
                 f'Captions only: "engine": "none".')
    env = dict(os.environ, HF_HUB_DISABLE_XET='1', KOKORO_ESPEAK_DATA=os.path.expanduser(v.get('espeak_data', '~/.cache/kes')))
    if not v.get('allow_download'): env['HF_HUB_OFFLINE'] = '1'
    guard_generated(out)
    run([os.path.expanduser(py), HERE / 'make_vo.py', '--narration', out / 'narration.json', '--out', out / 'vo', '--js', out / 'film' / 'vo_timing.js',
         '--grid', b['G'], '--bar', b['BAR'], '--voice', v.get('voice', 'am_michael'), '--lang', v.get('lang', 'a')], env=env)


# ---------------------------------------------------------------- qa
def qa(spec, out):
    guard_generated(out)
    q = out / 'qa'; q.mkdir(exist_ok=True)
    r = subprocess.run(['node', out / 'tools' / 'qa_check.mjs', out / 'film' / 'film.html', q], cwd=out)
    rep = json.load(open(q / 'qa_report.json'))
    print(f"QA: {len(rep['errors'])} errors, {len(rep['warnings'])} warnings — contact sheets in {q}")
    for e in rep['errors'][:30]: print('  ERROR', e)
    for w in rep['warnings'][:15]: print('  WARN ', w)
    if rep['errors']:
        sys.exit('QA failed. FIX: change film.json (shorter text, fewer points, different scene type, more bars) and rerun --stage build then qa. '
                 'Look at qa/sheet*.jpg if you can read images. Do not render until QA has 0 errors.')


# ---------------------------------------------------------------- render + finish
def render(spec, out, draft=False):
    guard_generated(out)
    rep, bj = out / 'qa' / 'qa_report.json', out / 'build.json'
    if not rep.exists() or rep.stat().st_mtime < bj.stat().st_mtime or json.load(open(rep))['errors']:
        sys.exit('ERROR QA has not passed on this build (run --stage qa after the last build; it must report 0 errors).\n'
                 '  FIX: python3 scripts/make_film.py film.json --stage qa — fix every QA error in film.json, rebuild, re-run qa, then render.')
    b = json.load(open(bj))
    ff = find_ffmpeg(spec)
    workers = str(spec.get('tools', {}).get('workers', max(2, min(6, (os.cpu_count() or 4) - 2))))
    cin = b.get('cinema', {'on': False})
    samples = 1 if draft or not cin['on'] else cin['motion_blur']
    if samples > 1:
        print(f'  motion blur: {samples} samples (180° shutter) on frames that move; still frames render once. Use --draft for quick looks')
    run(['node', out / 'tools' / 'render.mjs', 'video', out / 'film' / 'film.html', out / 'silent', ff, b['DUR'], workers, 30, samples], cwd=out)
    print('render done → NEXT: python3 scripts/make_film.py film.json --stage finish' + (' --draft' if draft else '') + '  (mix, grade, poster, captions; nothing is delivered until finish runs)')


def finish(spec, out, draft=False):
    b = json.load(open(out / 'build.json'))
    ff = find_ffmpeg(spec)
    fin = out / 'final'; fin.mkdir(exist_ok=True)
    name = spec.get('name', 'film')
    vodir = out / 'vo'
    mix = out / 'audio' / 'mix.wav'
    cin = b.get('cinema', {'on': False})
    # sound design bus (synthesised from the cue sheet written by build)
    sfx_args = []
    cues = out / 'audio' / 'sfx_cues.json'
    if cin['on'] and cues.exists() and json.load(open(cues)):
        run([sys.executable, HERE / 'sfx.py', cues, out / 'audio' / 'sfx.wav', '--duration', b['DUR'], '--gain-db', cin.get('sfx_gain_db', 0)])
        sfx_args = ['--sfx', out / 'audio' / 'sfx.wav']
    run([sys.executable, HERE / 'mix_audio.py', b['music'], vodir if (vodir / 'vo_timing.json').exists() else '-', mix, '--duration', b['DUR'], '--ffmpeg', ff, *sfx_args])
    mp4 = fin / f'{name}-1080p.mp4'
    # picture finish: colour grade (LUT) + bloom + film grain, one re-encode
    sys.path.insert(0, str(HERE)); import grade
    if cin['on'] and (cin['grade'] != 'none' or cin['bloom'] > 0 or cin['grain'] > 0):
        cube = grade.write_cube(cin['grade'], out / 'grade.cube', cin['grade_strength'])
        vf = ['-filter_complex', grade.vf_chain(cube, cin['bloom'], 0 if draft else cin['grain']), '-map', '[v]',
              '-c:v', 'libx264', '-preset', 'veryfast' if draft else 'slow', '-crf', '23' if draft else '17', '-pix_fmt', 'yuv420p']
    else:
        cube, vf = None, ['-map', '0:v', '-c:v', 'copy']
    run([ff, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', out / 'silent.list.txt', '-i', mix, *vf, '-map', '1:a',
         '-af', 'loudnorm=I=-14:TP=-1.0:LRA=11', '-ar', '48000', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', '-shortest', mp4])
    cover = fin / f'{name}-cover-4k.png'
    sc0 = spec['scenes'][0]   # poster: the cover's settled title frame (after the cold open), unless cover_t says otherwise
    cover_t = spec.get('cover_t') or (round(b['G'] + b['BAR'] * sc0['bars'] - 1.2, 2) if sc0.get('type') == 'cover' and isinstance(sc0.get('bars'), (int, float)) else 4.2)
    run(['node', out / 'tools' / 'cover.mjs', out / 'film' / 'film.html', cover, cover_t], cwd=out)
    if cube:
        raw = out / 'cover-raw.png'; shutil.move(cover, raw)
        run([ff, '-y', '-loglevel', 'error', '-i', raw, '-filter_complex', grade.vf_chain(cube, cin['bloom'], 0, still=True), '-map', '[v]', cover])
    from PIL import Image
    Image.open(cover).convert('RGB').resize((1280, 720), Image.LANCZOS).save(fin / f'{name}-cover-1280.jpg', quality=92)
    tj = vodir / 'vo_timing.json'
    if not tj.exists() and (out / 'narration.json').exists():   # captions only: SRT from the estimated timing (as on screen)
        vodir.mkdir(exist_ok=True); tj = vodir / 'captions_timing.json'
        json.dump([{'id': l['id'], 's': b['G'] + b['BAR'] * l['bar'], 'e': b['G'] + b['BAR'] * l['bar'] + len(l['en'].split()) / 2.5,
                    'zh': l['zh'], 'en': l.get('cap', l['en'])} for l in json.load(open(out / 'narration.json'))], open(tj, 'w'), ensure_ascii=False, indent=1)
    if tj.exists():
        run([sys.executable, HERE / 'make_srt.py', tj, fin, name])
    print(f'DONE → {mp4}\nTell the user: what is demo/simulated, what you could not verify (you cannot hear the audio), and what they must supply.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('spec'); ap.add_argument('--stage', default='all', choices=['all', 'check', 'build', 'vo', 'qa', 'render', 'finish'])
    ap.add_argument('--draft', action='store_true', help='fast preview: no motion blur or grain, quick encode')
    a = ap.parse_args()
    spec_path = Path(a.spec).resolve()
    spec = json.load(open(spec_path))
    base = spec_path.parent
    out = (base / spec.get('out', 'film_out')).resolve()
    out.mkdir(parents=True, exist_ok=True)
    check(spec, base)
    for w in warns: print(w)
    if errors:
        print('\n'.join(errors)); sys.exit(f'{len(errors)} error(s) in {spec_path.name} — fix them and rerun.')
    print(f'spec OK ({len(spec["scenes"])} scenes, genre {spec.get("genre") or "—"}, style {spec["style"]}, motion {spec.get("motion") or "style default"}, '
          f'music {"file" if (spec.get("music") or {}).get("file") else "composed " + music_mood(spec)[0]})')
    order = ['build', 'vo', 'qa', 'render', 'finish']
    stages = order if a.stage == 'all' else ([] if a.stage == 'check' else [a.stage])
    if 'build' in stages:
        treatment_gate(spec, spec_path)
    for st in stages:
        print(f'== {st}')
        {'build': lambda: build(spec, base, out), 'vo': lambda: vo(spec, base, out), 'qa': lambda: qa(spec, out),
         'render': lambda: render(spec, out, a.draft), 'finish': lambda: finish(spec, out, a.draft)}[st]()
