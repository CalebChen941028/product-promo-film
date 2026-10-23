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
STYLE_ALIASES = {'keynote-light': 'clean-light'}   # the style's earlier name: old film.json files keep working
STYLES = ['midnight-tech', 'clean-light', 'editorial-mono', 'aurora-glass', 'neon-cyber', 'paper-academic', 'luxe-noir', 'natural-fresh']
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
    # motion graphics built in code (story glue; no materials): a journey map, many-into-one, kinetic type, a real chart
    'footage': (2, ['media'], {}),   # real camera footage (.webm from intake), full-bleed or framed
    'custom': (1, ['fn'], {}),       # the director's cut: a scene the film writes itself (film.json "scripts"; references/custom-scenes.md)
    'flow': (2, ['steps'], {'steps': 5}), 'hub': (3, ['items'], {'items': 6}), 'type': (2, ['lines'], {'lines': 4}), 'chart': (3, ['data'], {'data': 8}),
    'mg': (1, ['layers'], {'layers': 24}),   # motion graphics designed in film.json: layers with beat keyframes (references/custom-scenes.md)
}


def resolve_flow(spec):
    """A flow with "steps": "chapters" maps the film's own chapters (in order, once each), so the map always agrees."""
    chs, seen = [], set()
    for sc in spec.get('scenes', []):
        c = sc.get('chapter')
        if c and c[0] not in seen: seen.add(c[0]); chs.append({'zh': c[1], 'en': c[2]})
    for sc in spec.get('scenes', []):
        if sc.get('type') == 'flow' and sc.get('steps') == 'chapters':
            sc['steps'] = chs[:5]
            sc['_from_chapters'] = True
GENRES = json.load(open(Path(__file__).resolve().parent.parent / 'templates' / 'genres.json'))['genres']
def rest_bars(bpm):
    """End-card length when the music is composed: about 8 s (3–4 bars), plus one ring-out bar. Longer is dead air."""
    return max(3, round(8 / (240 / float(bpm or 100))))
MOODS = ['cold', 'neutral', 'peak', 'warm', 'night']
sys.path.insert(0, str(Path(__file__).resolve().parent))
import director as DIR   # noqa: E402  (the shot plan: layouts, camera moves, cuts — scripts/director.py)
CUT_TYPES, CAMERAS, LAYOUTS, FEATURE_W = DIR.CUT_TYPES, DIR.CAMERAS, DIR.LAYOUTS, DIR.FEATURE_W
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


KF_FIELDS = {'x', 'y', 'z', 's', 'rx', 'ry', 'rz', 'o', 'blur', 'bright'}
REVEALS = {'left', 'right', 'up', 'down', 'circle', 'center'}


def resolve_keyframes(spec):
    """A scene's "camera" / "cut" may be a keyframe object instead of a name: register it as cameras/cuts "_cam<i>"/"_cut<i>"."""
    cams, cuts = spec.setdefault('cameras', {}), spec.setdefault('cuts', {})
    for i, sc in enumerate(spec.get('scenes', [])):
        if isinstance(sc.get('camera'), dict): cams[f'_cam{i}'] = sc['camera']; sc['camera'] = f'_cam{i}'
        if isinstance(sc.get('cut'), dict): cuts[f'_cut{i}'] = sc['cut']; sc['cut'] = f'_cut{i}'
    if not cams: spec.pop('cameras')
    if not cuts: spec.pop('cuts')


def check_mg(spec, base_dir):
    kinds = {'text', 'rect', 'circle', 'line', 'path', 'number', 'image'}
    keyf = {'x', 'y', 's', 'sx', 'sy', 'rz', 'o', 'blur'}
    for i, sc in enumerate(spec.get('scenes', [])):
        if sc.get('type') != 'mg': continue
        for k, L in enumerate(sc.get('layers') or []):
            w = f'scenes[{i}].layers[{k}]'
            if L.get('kind', 'text') not in kinds: err(f'{w}.kind = {L.get("kind")!r}', f'use one of {sorted(kinds)}'); continue
            for key in L.get('keys') or []:
                if not (isinstance(key, list) and len(key) >= 2 and isinstance(key[0], (int, float)) and isinstance(key[1], dict)):
                    err(f'{w}.keys: {key!r}', 'each key is [beat, {x, y, s, sx, sy, rz, o, blur}, "ease"?]'); break
                bad = set(key[1]) - keyf
                if bad: err(f'{w}.keys: unknown field(s) {sorted(bad)}', f'use {sorted(keyf)}'); break
            if L.get('kind') == 'image' and not (L.get('media') and (base_dir / L['media']).exists()):
                err(f'{w}: image media not found: {L.get("media")}', 'an mg image is a real material; paths are relative to film.json')
            if L.get('kind') == 'number' and not isinstance(L.get('value'), (int, float, str)):
                err(f'{w}: number without a value', 'give the true value from the docs')


def check_keyframes(spec):
    for kind in ('cameras', 'cuts'):
        for name, c in (spec.get(kind) or {}).items():
            if not isinstance(c, dict): err(f'{kind}.{name} must be an object', 'see references/custom-scenes.md (keyframe moves)'); continue
            for side in ('from', 'to'):
                bad = set((c.get(side) or {}).keys()) - KF_FIELDS
                if bad: err(f'{kind}.{name}.{side}: unknown field(s) {sorted(bad)}', f'use {sorted(KF_FIELDS)}')
            if c.get('ease') and c['ease'] not in ('eio', 'eo', 'ex', 'esoft', 'eback', 'linear'): err(f'{kind}.{name}.ease = {c["ease"]!r}', 'use eio, eo, ex, esoft, eback or linear')
            if c.get('at') is not None and not (isinstance(c['at'], list) and len(c['at']) == 2 and all(isinstance(v, (int, float)) for v in c['at'])):
                err(f'{kind}.{name}.at = {c["at"]!r}', 'a stage point [x, y] in px (0–1920, 0–1080)')
            if kind == 'cuts' and c.get('reveal') and c['reveal'] not in REVEALS: err(f'cuts.{name}.reveal = {c["reveal"]!r}', f'use one of {sorted(REVEALS)}')
            if kind == 'cameras':
                to = c.get('to') or {}
                if abs(to.get('s', 1) - 1) > 0.35 or abs(to.get('x', 0)) > 400 or abs(to.get('y', 0)) > 300:
                    warn(f'cameras.{name}: a big move (scale {to.get("s", 1)}, x {to.get("x", 0)}, y {to.get("y", 0)})', 'fine if the film wants it; check the QA sheets that text stays inside the frame')


def snap_rects(spec, base_dir, out_dir=None):
    """Every highlight box lands on a real element (scripts/snap.py): a box written by eye is replaced by the element it
    overlaps most — the page's own element boxes when the shot came from capture_app.mjs, else boxes found in the
    pixels. Product-agnostic; "exact": true on a point or crop keeps it as written. Also draws boxes-<scene>.png."""
    import snap as SN
    from PIL import Image, ImageDraw
    cache, report = {}, []
    def cands(media, base):
        if media not in cache:
            p = base_dir / media
            reg = DIR.regions_for(base_dir, media)
            if reg and reg.get('base') and list(reg['base']) != list(base):   # regions in another coordinate space: scale them
                kx, ky = base[0] / reg['base'][0], base[1] / reg['base'][1]
                reg = {'base': base, 'regions': [{**r, 'rect': [r['rect'][0] * kx, r['rect'][1] * ky, r['rect'][2] * kx, r['rect'][3] * ky]} for r in reg.get('regions', [])]}
            cache[media] = SN.candidates(p, base, reg) if p.exists() else ([], [])
        return cache[media]
    for i, sc in enumerate(spec.get('scenes', [])):
        groups = []
        m = sc.get('media') if isinstance(sc.get('media'), str) else None
        if m and m.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and sc.get('frame') != 'photo':
            groups.append((m, sc.get('base'), [('points', k, p_) for k, p_ in enumerate(sc.get('points') or [])] + [('crops', k, c) for k, c in enumerate(sc.get('crops') or [])]))
        for k, pn in enumerate(sc.get('panels') or []):
            if isinstance(pn.get('media'), str) and isinstance(pn.get('crop'), list): groups.append((pn['media'], pn.get('base'), [('panels', k, {'rect': pn['crop'], '_panel': pn})]))
        for media, base, items in groups:
            if not (base_dir / media).exists(): continue
            if not base:
                import suggest_rects as SR
                base = SR.default_base(*Image.open(base_dir / media).size)
            dom, pix = cands(media, list(base))
            reg_txt = DIR.regions_for(base_dir, media)
            if reg_txt and reg_txt.get('base') and list(reg_txt['base']) != list(base): reg_txt = None   # texts only in the shot's own coordinates
            if not reg_txt:   # any screenshot: the words read from the pixels (OCR) plus the pixel blocks as their cards
                words = SN.ocr_regions(base_dir / media, list(base))
                if words: reg_txt = {'base': list(base), 'regions': words + [{'kind': 'panel', 'text': '', 'rect': c} for c in pix]}
            drawn = []
            for kind, k, it in items:
                r = it.get('rect')
                if not (isinstance(r, list) and len(r) == 4) or it.get('exact'): continue
                new, ov, src = SN.snap_with_text(r, [it.get('zh'), it.get('en')], reg_txt, DIR.find_region, dom, pix) if reg_txt else SN.snap(r, dom, pix)
                if src == 'kept':
                    report.append((i, f'{kind}[{k}] {it.get("zh") or ""}', ov))
                else:
                    x0, y0 = max(0, new[0]), max(0, new[1]); x1, y1 = min(base[0], new[0] + new[2]), min(base[1], new[1] + new[3])
                    new = [round(x0), round(y0), round(x1 - x0), round(y1 - y0)]   # inside the picture
                    if '_panel' in it: it['_panel']['crop'] = new
                    else: it['rect'] = new
                drawn.append((new if src != 'kept' else r, src, it.get('zh') or f'{kind}{k}'))
            if out_dir and drawn:
                try:
                    im = Image.open(base_dir / media).convert('RGB'); sx = im.size[0] / base[0]
                    d = ImageDraw.Draw(im)
                    for n, (r, src, label) in enumerate(drawn):
                        col = (40, 200, 120) if src != 'kept' else (240, 70, 60)
                        d.rectangle([r[0] * sx, r[1] * sx, (r[0] + r[2]) * sx, (r[1] + r[3]) * sx], outline=col, width=max(3, int(4 * sx)))
                        d.text((r[0] * sx + 8, r[1] * sx + 6), f'{n + 1}', fill=col)
                    (out_dir / 'check').mkdir(parents=True, exist_ok=True)
                    im.thumbnail((1600, 1600)); im.save(out_dir / 'check' / f'boxes-{i:02d}.jpg', quality=85)
                except Exception:
                    pass
    for i, what, ov in report:
        warn(f'scenes[{i}].{what}: the box sits on no real element (best overlap {ov:.2f}); it is drawn as written',
             'name the element instead ("rect": "@its text", capture_app shots), or move the box onto the card / table / button it is about '
             '(film_out/check/boxes-*.jpg shows every box: green = on an element, red = as written); "exact": true keeps a box on purpose')
    return report


def resolve_look(spec, base_dir=None):
    """Fill style/motion when they are "auto" or missing: the director's look.py on the materials, in place."""
    g = GENRES.get(spec.get('genre') or '', None)
    if spec.get('style') in (None, '', 'auto') or spec.get('motion') in (None, 'auto'):
        lk = None
        try:   # the director reads the materials (scripts/look.py); only when there is nothing to read does the genre's first look stand in
            import look as LOOK, json as _j
            man = Path(base_dir or '.') / 'build' / 'manifest.json'
            m_ = _j.load(open(man)) if man.exists() else {}
            if m_.get('items') and Path(m_.get('materials', '')).is_dir(): lk = LOOK.choose(m_['items'], m_['materials'], spec.get('genre') or '', '', '')
        except Exception:
            lk = None
        if spec.get('style') in (None, '', 'auto'):
            spec['style'] = lk['style'] if lk else (g['style'][0] if g else 'midnight-tech')
        if spec.get('motion') in (None, 'auto'):
            spec['motion'] = lk['motion'] if lk else (g['motion'] if g else '')
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
            'lens': c.get('lens', {}), 'motion': spec.get('motion') or sp['motionDefault'] or 'cinematic-3d',
            'like': ((spec.get('motions') or {}).get(spec.get('motion') or '') or {}).get('like')}


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
    src = None
    try: src = Path((SKILL / '.source').read_text().strip()) / 'node_modules'   # the folder install.sh / install.ps1 copied this skill from
    except Exception: pass
    cand = [spec.get('tools', {}).get('node_modules'), os.environ.get('PLAYWRIGHT_NODE_MODULES'), SKILL / 'node_modules', src, Path.cwd() / 'node_modules']
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


def chart_media(base_dir, sc):
    """A chart (sparse marks) needs no highlight boxes: suggest_rects finds none, and boxes on chart space read as noise."""
    try:
        sys.path.insert(0, str(HERE)); import suggest_rects
        return isinstance(sc.get('media'), str) and suggest_rects.is_chart(base_dir / sc['media'], sc.get('base'))
    except Exception:
        return False


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
def script_names(spec, base_dir, registry):
    """Names the film's own scripts register: CUSTOM.x / CAMERA.x / CUT.x = … (or CUT['x'] = …)."""
    src = ''.join((base_dir / p_).read_text() for p_ in spec.get('scripts', []) or [] if (base_dir / p_).exists())
    return {a or b for a, b in re.findall(registry + r'\s*(?:\.\s*(\w+)|\[\s*[\'"]([\w-]+)[\'"]\s*\])\s*=(?!=)', src)}


def material_roles(base_dir):
    """intake's role per material (desktop/phone/photo/cutout…), when autofilm/intake ran."""
    man = base_dir / 'build' / 'manifest.json'
    if not man.exists(): return {}
    m = json.load(open(man))
    return {str((Path(m['materials']) / it['file']).resolve()): it.get('role') for it in m.get('items', [])}


def pad169(r, base, k=1.0, min_frac=0.0):
    """Python twin of patterns.js padTo169: the 16:9 crop the film actually shows around a region."""
    x, y, w, h = r
    W = min(max(w * k, h * k * 16 / 9, base[0] * min_frac), base[0])
    return W


_PX = {}


def px_width(path):
    if path not in _PX:
        try:
            from PIL import Image
            _PX[path] = Image.open(path).size[0]
        except Exception:
            _PX[path] = None
    return _PX[path]


def sharpness(spec, base_dir, plan, roles):
    """How far each picture is enlarged on screen (display px ÷ source px). Above 1.5× it looks soft; a whole dense
    screen shown small cannot be read. Returns warnings (msg, fix)."""
    out = []
    FIX = ('capture at 2× (3840 wide — capture_app.mjs does), give the zoom a wider region, or a layout that shows it '
           'smaller; never upscale a small crop to fill the frame')
    for i, (sc, p_) in enumerate(zip(spec.get('scenes', []), plan)):
        t, base = sc.get('type'), sc.get('base') or [1920, 1080]
        def look(m, disp, crop_w=None, what=''):
            if not m or not str(m).lower().endswith(('.png', '.jpg', '.jpeg', '.webp')): return
            pw = px_width(base_dir / m)
            if not pw: return
            bw = base[0] if sc.get('base') or roles.get(str((base_dir / m).resolve())) in ('desktop', 'figure', 'phone') else pw
            src = pw * (crop_w or bw) / bw
            up = disp / max(1, src)
            if up > 1.5:
                out.append((f'scenes[{i}] ({t}){what}: {Path(m).name} is enlarged {up:.1f}× ({src:.0f} source px fill {disp:.0f} px) — it will look soft', FIX))
        m = sc.get('media') if isinstance(sc.get('media'), str) else None
        if t == 'feature' and m:
            w = FEATURE_W.get(p_['layout'] or '', 1320)
            look(m, w, None, ' whole')
            rects = [pt['rect'] for pt in sc.get('points', []) if pt.get('rect')]
            if rects: look(m, w, min(pad169(r, base, 2.2, 0.42) for r in rects), ' zoomed to a point')
        elif t == 'detail' and m:
            disp = 960 if p_['layout'] == 'split' else 1920
            for c in sc.get('crops', []) or []:
                if c.get('rect'): look(m, disp, pad169(c['rect'], base, 1.0, 0.36), ' close-up')
        elif t == 'cover' and m:
            look(m, 1920, None, ' full frame')
            if sc.get('focus'): look(m, 1920, pad169(sc['focus'], base, 1.0), ' opening on its focus')
        elif t in ('photo', 'hero') and m:
            look(m, 1920, None)
        elif t == 'carousel':
            for j, pnl in enumerate(sc.get('panels', [])):
                c = pnl.get('crop'); pb = pnl.get('base') or [1920, 1080]
                if c: look(pnl.get('media'), min(1000, 680 / c[3] * c[2]), c[2] * base[0] / pb[0], f'.panels[{j}]')
        elif t == 'gallery':
            for j, it in enumerate(sc.get('items', [])):
                mm = it.get('media') if isinstance(it, dict) else None
                if mm and roles.get(str((base_dir / mm).resolve())) == 'desktop' and not chart_media(base_dir, {'media': mm}):
                    out.append((f'scenes[{i}] (gallery).items[{j}]: {Path(mm).name} is a whole dense screen on a small card — its text is unreadable',
                                'a gallery is for outputs (plots, reports, photos); show a dense screen in a feature that zooms, or crop it first'))
    return out


def check(spec, base_dir):
    if spec.get('genre') and spec['genre'] != 'auto' and spec['genre'] not in GENRES:
        err(f"genre '{spec['genre']}' unknown", f'use one of {list(GENRES)} (scripts/genres.py --list)')
    if 'approved' in spec and not spec.get('approved') and not spec.get('_preview'):
        err("the director's proposals are not approved yet",
            'run python3 scripts/proposals.py film.json, show proposals.md and its previews to the user, WAIT for their choice or changes, '
            'then proposals.py film.json --apply <A|B|C> (--by assumed only when the user cannot be asked)')
    resolve_look(spec, base_dir)
    if spec.get('style') not in STYLES:
        err(f"style '{spec.get('style')}' unknown", f'use one of {STYLES} (scripts/look.py picks one from the materials)')
    pal = spec.get('palette')
    if pal:
        import palette as PAL
        bad = [k for k in ('accent', 'accent2') if pal.get(k) and not re.fullmatch(r'#[0-9a-fA-F]{6}', str(pal[k]))]
        if bad: err(f'palette.{bad[0]} = {pal[bad[0]]!r}', 'use a hex colour like "#2ee6c5" (or remove "palette" to keep the style\'s)')
        elif pal.get('accent') and spec.get('style') in STYLES:
            c = PAL.contrast(PAL.rgb_of(pal['accent']), PAL.rgb_of(PAL.style_bg(spec['style'])[0]))
            if c < 3.0: warn(f'palette.accent {pal["accent"]} has {c:.1f}:1 contrast with the {spec["style"]} background (< 3:1)',
                             f'python3 scripts/palette.py <materials> --genre {spec.get("genre") or "<genre>"} --style {spec["style"]} suggests a legible tone of the same hue')
    for p_ in spec.get('css', []) or []:
        if not (base_dir / p_).exists(): err(f'css not found: {p_}', '"css" paths are relative to film.json')
    own_motions = set((spec.get('motions') or {}).keys())
    for mid, m in (spec.get('motions') or {}).items():
        if m.get('like') and m['like'] not in MOTIONS: err(f'motions.{mid}.like = {m["like"]!r}', f'build on one of {MOTIONS}')
    if spec.get('motion') and spec['motion'] not in MOTIONS and spec['motion'] not in own_motions:
        err(f"motion '{spec.get('motion')}' unknown", f"use one of {MOTIONS} or leave it empty for the style's default")
    b = spec.get('brand', {})
    for k in ['name', 'logo', 'positioningZh', 'positioningEn']:
        if not b.get(k):
            err(f'brand.{k} missing', 'fill it from the brief (templates/brief.example.json)')
    if b.get('nameAccent') and b.get('name', '').strip().lower().endswith(b['nameAccent'].strip().lower()):
        err(f"brand.name '{b['name']}' already ends with nameAccent '{b['nameAccent']}' (it would read twice)", 'name = the first word(s), nameAccent = the accented last word: "name": "Aurel", "nameAccent": "Stoneware"')
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
    roles = material_roles(base_dir)
    own_cuts, own_cams = script_names(spec, base_dir, 'CUT') | set(spec.get('cuts') or {}), script_names(spec, base_dir, 'CAMERA') | set(spec.get('cameras') or {})
    check_keyframes(spec)
    check_mg(spec, base_dir)
    plan, design_warns = DIR.plan_shots(spec, base_dir, roles)
    # the same picture in two scenes reads as filler (cover and finale may call each other back)
    uses = {}
    for i, sc in enumerate(scenes):
        if sc.get('type') in ('cover', 'finale', 'endcard'): continue
        ms = [sc.get('media')] if isinstance(sc.get('media'), str) else list(sc.get('media') or []) if isinstance(sc.get('media'), list) else []
        ms += [p_.get('media') for p_ in sc.get('panels', []) or []] + [it.get('media') for it in sc.get('items', []) or [] if isinstance(it, dict)]
        for m in {m for m in ms if isinstance(m, str)}: uses.setdefault(m, []).append(i)
    for m, idx in uses.items():
        if len(idx) > 1:
            warn(f'{Path(m).name} appears in scenes {idx}', 'one picture, one beat: give the later scene another real screen or output (or a different, named crop of it), so no beat repeats')
    # a crop that cuts through content (a word, a table, a frame runs off its edge): any screenshot, any product (scripts/snap.py)
    import snap as SN
    for m in sorted(uses):
        p_ = base_dir / m
        if not p_.exists() or not m.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')): continue
        role = roles.get(str(p_.resolve()))
        try:
            from PIL import Image as _I; w_, h_ = _I.open(p_).size
        except Exception:
            continue
        crop = role == 'figure' or (role in ('desktop', None) and not 1.70 <= w_ / h_ <= 1.82)   # a full window is 16:9 and touches its own edges
        if role in ('photo', 'cutout', 'logo', 'phone') or not crop: continue
        sides = SN.cut_edges(p_)
        if sides:
            warn(f'{p_.name}: the crop cuts through content on the {", ".join(sides)} edge', 'recapture it around the whole element ("clip": "@its text" in the shot list adds a margin), or crop wider so nothing is cut off')
    for i, msg, fix in design_warns: warn(f'scenes[{i}] ({scenes[i].get("type")}): {msg}', fix)
    for msg, fix in sharpness(spec, base_dir, plan, roles): warn(msg, fix)
    for i, msg, fix in DIR.rect_warnings(spec, base_dir): warn(f'scenes[{i}] ({scenes[i].get("type")}): {msg}', fix)
    for i, sc in enumerate(scenes):
        t, where = sc.get('type'), f'scenes[{i}] ({sc.get("type")})'
        if t not in TYPES:
            err(f'{where}: unknown type', f'use one of {list(TYPES)}'); continue
        mn, req, lim = TYPES[t]
        if sc.get('mood') and sc['mood'] not in MOODS:
            err(f"{where}: mood '{sc['mood']}' unknown", f'use one of {MOODS} (colour script, references/director.md)')
        if 'hit' in sc and sc['hit'] not in (True, False, 'hero'):
            err(f"{where}: hit = {sc['hit']!r}", 'use true, false, or "hero" (the one biggest beat of the film)')
        if sc.get('cut') and sc['cut'] not in CUT_TYPES and sc['cut'] not in own_cuts:
            err(f"{where}: cut '{sc['cut']}' unknown", f'use one of {CUT_TYPES}, or define CUT.{sc["cut"]} in a film script (references/custom-scenes.md)')
        if sc.get('camera') and sc['camera'] not in CAMERAS and sc['camera'] not in own_cams:
            err(f"{where}: camera '{sc['camera']}' unknown", f'use one of {CAMERAS}, or define CAMERA.{sc["camera"]} in a film script (references/custom-scenes.md)')
        if sc.get('motion') and sc['motion'] not in MOTIONS and sc['motion'] not in own_motions:
            err(f"{where}: motion '{sc['motion']}' unknown", f'use one of {MOTIONS} (this scene only; the film keeps its own)')
        if sc.get('layout') and sc['layout'] not in LAYOUTS.get(t, []):
            err(f"{where}: layout '{sc['layout']}' unknown for {t}", f'use one of {LAYOUTS.get(t) or "— (this type has one layout)"}')
        bars = sc.get('bars')
        if bars != 'rest' and (not isinstance(bars, (int, float)) or bars < mn):
            err(f'{where}: bars={bars} (minimum {mn})', f'set "bars" to ≥ {mn} (1 bar = 4 beats; 120 BPM → 2 s)')
        if t == 'custom':
            srcs = ''.join((base_dir / p_).read_text() for p_ in spec.get('scripts', []) or [] if (base_dir / p_).exists())
            for p_ in spec.get('scripts', []) or []:
                if not (base_dir / p_).exists(): err(f'script not found: {p_}', '"scripts" paths are relative to film.json')
            if sc.get('fn') and not re.search(r'CUSTOM\s*(?:\.\s*' + re.escape(sc['fn']) + r'|\[\s*[\'"]' + re.escape(sc['fn']) + r'[\'"]\s*\])\s*=', srcs):
                err(f'{where}: custom scene "{sc["fn"]}" is not defined', f'define CUSTOM.{sc["fn"]} = (start, end, o) => {{ scene(start, end, init, update); }} in a file listed in "scripts" (references/custom-scenes.md)')
            for k, v in (sc.get('assets') or {}).items():
                if not (base_dir / v).exists(): err(f'{where}: assets.{k} not found: {v}', 'paths are relative to film.json')
        if t == 'compare' and isinstance(bars, (int, float)) and (bars > 8 or len(sc.get('rows', [])) > 5):
            warn(f'{where}: a comparison of {len(sc.get("rows", []))} rows held {bars} bars reads as a slide',
                 'keep the 3–4 rows that prove the proposition, ≤ 8 bars (a row per bar); the rest belongs in the docs, not the film')
        if t == 'flow' and sc.get('_from_chapters') and len(sc.get('steps', [])) < 2:
            err(f'{where}: "steps": "chapters" but the film has {len(sc.get("steps", []))} chapter(s)', 'give the scenes "chapter" labels, or list the steps')
        if t == 'chart':
            if not all(isinstance(x, dict) and isinstance(x.get('value'), (int, float)) and x.get('label') for x in sc.get('data', [])):
                err(f'{where}: every chart datum needs a "label" and a numeric "value"', 'data: [{"label": "2024", "value": 12}, …] — real numbers from the docs')
            elif len(sc.get('data', [])) < 2:
                err(f'{where}: a chart needs ≥ 2 values', 'show one number with a "numbers" scene instead')
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
            elif t in ('clip', 'footage') and not m.endswith('.webm'):
                err(f'{where}: clip must be .webm (Chromium cannot decode H.264)', 'run intake.py — it converts videos to build/clips/*.webm')
        basewh = sc.get('base', [1920, 1080])
        # holds that read as empty: silent texture, one object held long, a spec list on a photo card, a cold open on a texture
        if not sc.get('say') and isinstance(bars, (int, float)) and ((t == 'detail' and bars > 2) or (t in ('hero', 'photo', 'feature') and bars > 3)):
            warn(f'{where}: {bars} bars with no voice on one image', 'a silent hold over ~6 s reads as empty: 2 bars, or give it a line')
        if t == 'hero' and isinstance(bars, (int, float)) and bars > 3 and not isinstance(sc.get('media'), list):
            warn(f'{where}: one image held {bars} bars', 'a single-image reveal lands in 3 bars; more angles (a media list) can hold longer')
        if t == 'feature' and sc.get('frame') == 'photo' and len(sc.get('points', [])) > 2:
            warn(f'{where}: {len(sc["points"])} points on a photo', 'a spec list dilutes the idea: keep ≤ 2 points that serve it, or use a "photo" scene with one line')
        # legibility: UI text on a whole dense screen is too small at film scale (≥ 18 px at 1080p is the floor)
        is_screen = isinstance(sc.get('media'), str) and roles.get(str((base_dir / sc['media']).resolve())) in ('desktop', 'figure') and not chart_media(base_dir, sc)
        if t == 'feature' and is_screen and sc.get('frame') != 'photo':
            px = 13 * FEATURE_W.get(plan[i]['layout'] or '', 1400) / basewh[0]
            if px < 18 and any(not p.get('rect') and not p.get('focus') for p in sc.get('points', [])):
                warn(f'{where}: a point on the whole screen — UI text renders at ~{px:.0f} px (< 18)', 'give the point a rect (suggest_rects.py) so the beat zooms to a readable region, or a "focus" crop')
        if t == 'carousel':
            for j, pnl in enumerate(sc.get('panels', [])):
                if not pnl.get('crop') and roles.get(str((base_dir / pnl.get('media', '')).resolve())) == 'desktop':
                    warn(f'{where}.panels[{j}]: a whole dense screen as a panel — its text is unreadable at film scale', 'give the panel a "crop" (the region it is about, ≤ 1000 base px wide)')
        if t == 'cover' and is_screen and not sc.get('focus') and sc.get('open') is not False:
            warn(f'{where}: the cold open is a whole dense screen', 'give the cover a "focus" crop (the readable region the hook is about); the open pushes in after a calm second')
        if t in ('clip', 'phone') and not sc.get('say'):
            warn(f'{where}: a silent {t} scene', 'give it one line that serves the idea — or cut it; an extra device or clip is a detour')
        if i and t in ('feature', 'photo', 'detail') and scenes[i - 1].get('type') == t:
            warn(f'{where}: two {t} beats in a row share one shape', 'vary the proof: a zoomed detail, one number, a clip, a before → after, or a calm statement between them')
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
                if sc.get('frame') != 'photo' and not chart_media(base_dir, sc):
                    warn(f'{where}.points[{j}]: no rect → no highlight box', f'python3 {HERE / "suggest_rects.py"} {sc.get("media")} --preview . → copy the numbered rect this point talks about; real photos ("frame": "photo") need none')
            elif len(r) != 4:
                err(f'{where}.points[{j}]: rect must be [x,y,w,h]', 'write it as "@the element\'s words", or [x, y, w, h] in base units from suggest_rects.py --preview (base coordinates)')
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
        err('playwright not found', 'in the Reelwright folder (where you cloned it): npm install && npx playwright install chromium; then python3 scripts/doctor.py')


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
    track_s = dur
    if grid.get('generated'):
        each_rest = rest_bars(grid['bpm'])
        dur = min(dur, G + BAR * (fixed + each_rest * len(rest) + 1))   # end on the ring-out bar, not the reverb tail (the mix fades it)
    elif rest and each_rest > rest_bars(grid['bpm']) + 1:
        # the user's track is longer than the film: the end card never soaks up the rest of the song (it would hold one
        # frame for a minute). It gets ~8 s, the music fades out on the bar after it, and the agent hears the real length.
        each_rest = rest_bars(grid['bpm']) + 1
        dur = min(dur, G + BAR * (fixed + each_rest * len(rest) + 1))
        print(f'WARN  the film is {dur:.0f} s but the track is {track_s:.0f} s: the end card is capped at {each_rest} bars and the music fades out at {dur:.0f} s.\n'
              f'  FIX: if the user asked for a longer film, add scenes (more chapters, more real screens, a breath) until the story fills the track; '
              f'never hold the end card to fill time')
        want = (spec.get('_autofilm') or {}).get('seconds') or spec.get('target_seconds')
        if want and dur < 0.8 * float(want):
            sys.exit(f'ERROR the film is {dur:.0f} s; the user asked for about {float(want):.0f} s.\n'
                     f'  FIX: add scenes until the story reaches the length the user asked for (or ask them whether a shorter film is fine)')
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
    # the film's own look (film.json "css"): copied next to film.html, linked after the style
    css_links = []
    for k, p_ in enumerate(spec.get('css', []) or []):
        dst = film / f'look-{k}-{Path(p_).name}'; shutil.copy(base_dir / p_, dst); css_links.append(dst.name)
    # the director's cut: the film's own scene scripts, after the library (CUSTOM.<name> = (start, end, o) => {…})
    (film / 'custom.js').write_text("'use strict';\n" + '\n'.join(f'// ---- {p}\n' + (base_dir / p).read_text() for p in spec.get('scripts', []) or []) + '\n')
    for f in (TPL / 'styles').glob('*'):
        shutil.copy(f, film / 'styles' / f.name)
    copied = {}

    # pictures the film zooms into (focus, crops, highlight zooms, detail close-ups, the hero's rise): keep full resolution
    zoomed = set()
    for sc in spec['scenes']:
        if sc.get('focus') or sc.get('crop') or sc.get('crops') or sc['type'] in ('detail', 'cover', 'photo', 'hero') or any(p_.get('rect') or p_.get('focus') for p_ in sc.get('points', [])):
            zoomed |= {m for m in ([sc.get('media')] if isinstance(sc.get('media'), str) else []) + [sc.get('image')] if m}
        zoomed |= {p_.get('media') for p_ in sc.get('panels', []) if p_.get('crop')}

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
                cap = 3840 if p in zoomed else 2400   # a zoomed picture keeps its pixels: a 2× capture stays sharp at 2× zoom
                if im.width > cap and im.width >= im.height:
                    im = im.resize((cap, round(im.height * cap / im.width)), Image.LANCZOS)
                    im.save(dst, quality=92) if dst.suffix.lower() in ('.jpg', '.jpeg') else im.save(dst)
                else:
                    shutil.copy(src, dst)
            else:
                shutil.copy(src, dst)
            copied[key] = 'media/' + dst.name
        return copied[key]
    brand = dict(spec['brand']); brand['logo'] = media(brand['logo'])
    lines, calls, chapters, b0, segs = [], [], [], 0, []
    illus = []   # bars where the frame shows a UI redrawn in code: the film labels it on screen
    plan, _ = DIR.plan_shots(spec, base_dir, material_roles(base_dir))
    for i, sc in enumerate(spec['scenes']):
        nb = each_rest if sc.get('bars') == 'rest' else sc['bars']
        b1 = b0 + nb
        segs.append((sc, b0, b1))
        o = {k: v for k, v in sc.items() if k not in ('type', 'bars', 'say', 'chapter', 'mood', 'cut', 'hit', 'energy', 'layout', 'camera', 'motion')}
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
        sh = {k: v for k, v in plan[i].items() if k in ('layout', 'camera', 'motion') and v}
        sh.update({k: sc[k] for k in ('offset', 'rate') if isinstance(sc.get(k), (int, float))})   # where footage plays from
        calls.append(f"shot({json.dumps(sh, ensure_ascii=False)});")
        if sc['type'] == 'mg':
            for L in o.get('layers') or []:
                if L.get('kind') == 'image' and L.get('media'): L['media'] = media(L['media'])   # a real material, copied with the film
        if sc['type'] == 'custom':
            for k, v in list((o.get('assets') or {}).items()): o['assets'][k] = media(v)   # pictures a custom scene uses
            o.pop('fn', None)
            calls.append(f"if (!CUSTOM[{json.dumps(sc['fn'])}]) throw new Error('custom scene {sc['fn']} is not defined in the film\\'s scripts');")
            calls.append(f"CUSTOM[{json.dumps(sc['fn'])}](bar({b0}), {'CONFIG.DUR' if i == len(spec['scenes']) - 1 else f'bar({b1})'}, {json.dumps(o, ensure_ascii=False)});")
        else:
            calls.append(f"LIB.{sc['type']}(bar({b0}), {'CONFIG.DUR' if i == len(spec['scenes']) - 1 else f'bar({b1})'}, {json.dumps(o, ensure_ascii=False)});")
        if sc.get('chapter'):
            n, zh, en = sc['chapter']; chapters.append([b0, b1, n, zh, en])
        if sc.get('illustrative'): illus.append([b0, b1])
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
    cin_cfg, cues = direct(cin, segs, G, BAR, dur, plan)
    print(DIR.shot_table(spec, plan))
    cfg = {'STYLE': spec['style'], 'MOTION': spec.get('motion', ''), 'G': G, 'BAR': BAR, 'DUR': round(dur, 3), 'FADE_OUT': 2.6,
           'CHORUS_BARS': chorus, 'CHAPTERS': merged, 'ILLUSTRATIVE': illus, 'ILLUS_LABEL': spec.get('illustrative_label') or '界面示意 · Illustrative UI', 'ONSCREEN': onscreen, 'SHOTS': 'media/', 'ASSETS': 'media/', 'BRAND': brand,
           'MOTIONS_EXTRA': spec.get('motions') or {}, 'CAMERAS_EXTRA': spec.get('cameras') or {}, 'CUTS_EXTRA': spec.get('cuts') or {}, 'CSS': css_links, 'CINEMA': cin_cfg, 'PALETTE': {k: v for k, v in (spec.get('palette') or {}).items() if k in ('accent', 'accent2')}}
    json.dump(cues, open(aud / 'sfx_cues.json', 'w'), indent=1)
    (film / 'config.js').write_text('const CONFIG = ' + json.dumps(cfg, ensure_ascii=False, indent=1) + ';\nconst bar = (b) => CONFIG.G + CONFIG.BAR * b;\nObject.assign(window, { CONFIG, bar });\n')
    (film / 'scenes.js').write_text("'use strict';\n// generated by make_film.py from film.json — edit film.json, not this file\n" + '\n'.join(calls) + '\nshot({});\n')
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
    print(f'built {len(spec["scenes"])} scenes on {b0} bars · music {dur:.1f} s · BPM {grid["bpm"]} · {len(lines)} narration lines → {film}/film.html')


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


def direct(cin, segs, G, BAR, dur, plan=None):
    """The director's pass: moods, hit points, camera cuts, light rays and the sound-design cue sheet."""
    if not cin['on']:
        return {'on': False}, []
    T = lambda b: round(G + BAR * b, 4)
    mo = cin['motion']; pal = PALETTE.get(mo) or PALETTE.get(cin.get('like') or '', PALETTE['cinematic-3d'])
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
        if plan: cut = plan[i]['cut']   # the shot plan (plan_shots) chose every cut
        elif i == 0: cut = 'style'
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
    (q / 'qa_report.json').unlink(missing_ok=True)   # never read a report left by an earlier build
    r = subprocess.run(['node', out / 'tools' / 'qa_check.mjs', out / 'film' / 'film.html', q], cwd=out)
    if r.returncode != 0 or not (q / 'qa_report.json').exists():
        sys.exit('ERROR QA could not run: the film page failed to load or crashed (see the error above).\n'
                 '  FIX: a script error in a custom scene, a keyframe or the engine stops the page; fix it, rebuild, then run --stage qa again')
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
    if not spec.get('cover_t') and sc0.get('name') is False:   # a name-less cold open: the poster is the hero (finale) with the name settled
        fb = 0
        for sc in spec['scenes']:
            if sc.get('type') == 'finale':
                cover_t = round(b['G'] + b['BAR'] * (fb + 0.8 * sc['bars']), 2); break
            fb += sc['bars'] if isinstance(sc.get('bars'), (int, float)) else 0
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
    spec['style'] = STYLE_ALIASES.get(spec.get('style'), spec.get('style'))
    resolve_flow(spec)
    resolve_keyframes(spec)
    base = spec_path.parent
    for msg, fix in DIR.resolve_rects(spec, base): err(msg, fix)   # "rect": "@APA 三线表" → the exact panel box
    snap_rects(spec, base, (base / spec.get('out', 'film_out')).resolve())   # boxes written by eye land on the real element under them
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
    if a.stage == 'check': print(DIR.shot_table(spec, DIR.plan_shots(spec, base, material_roles(base))[0]))
    if 'build' in stages:
        treatment_gate(spec, spec_path)
    for st in stages:
        print(f'== {st}')
        {'build': lambda: build(spec, base, out), 'vo': lambda: vo(spec, base, out), 'qa': lambda: qa(spec, out),
         'render': lambda: render(spec, out, a.draft), 'finish': lambda: finish(spec, out, a.draft)}[st]()
