"""The director: reads the materials, then designs every scene's frame, camera move and cut — before anything is made.

Usage:
  python3 scripts/director.py film.json            → prints the shot plan (storyboard) with the reason for each choice
  (autofilm.py writes the plan into film.json and treatment.md §6; make_film.py --stage check re-checks it)

What it looks at, per picture (cached): what it is (screen, chart, photo, cut-out), how dense it is, which side is busy
and which is quiet, where the subject sits, how bright it is; per scene: how many boxed points there are and where the
boxes sit, how many items, whether crops are labelled; per film: the motion language (its palette), chapters, the hero,
and what the last scenes already used. Every choice carries a "why" so a person can read the storyboard and overrule it.
A scene's own "layout" / "camera" / "cut" / "motion" in film.json always wins.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = HERE.parent / 'templates'

MOTIONS = ['cinematic-3d', 'precision-data', 'kinetic-launch', 'gentle-story', 'playful-pop', 'editorial-type']
CUT_TYPES = ['style', 'whip', 'push', 'slide-up', 'wipe', 'iris', 'zoom', 'blur', 'dip', 'doors', 'light', 'rack']
CAMERAS = ['none', 'orbit', 'punch', 'dolly', 'sway', 'push', 'pull', 'pan-l', 'pan-r', 'crane', 'tilt', 'arc', 'vertigo', 'handheld', 'reveal']
LAYOUTS = {   # per scene type: the layouts the scene library draws (templates/patterns.js, library.js)
    'feature': ['center', 'split', 'split-r', 'full', 'soft', 'stickers', 'editorial'],
    'photo': ['left', 'right', 'bottom', 'center', 'split'], 'footage': ['left', 'right', 'bottom', 'center', 'split'], 'gallery': ['coverflow', 'grid', 'strip'],
    'carousel': ['menu', 'stack'], 'detail': ['macro', 'split'],
}
LIST_LAYOUTS = ('split', 'split-r', 'editorial')
FEATURE_W = {'center': 1320, 'split': 1120, 'split-r': 1120, 'full': 1400, 'soft': 1120, 'stickers': 1180, 'editorial': 1000}
# per motion language: the layouts, camera moves and cuts that keep the film's grammar while letting each scene find its
# own frame. First = the language's signature; later ones are the variations, in order of preference.
SHOT_PALETTE = {
    'cinematic-3d':   {'feature': ['center', 'split', 'split-r', 'full'], 'camera': ['orbit', 'push', 'arc', 'crane', 'vertigo', 'pull'], 'cuts': ['push', 'zoom', 'rack', 'iris', 'doors', 'slide-up']},
    'precision-data': {'feature': ['split', 'split-r', 'center', 'full'], 'camera': ['none', 'push', 'pan-l', 'pan-r', 'pull', 'reveal'], 'cuts': ['wipe', 'slide-up', 'rack', 'push', 'doors', 'zoom']},
    'kinetic-launch': {'feature': ['full', 'center', 'split-r', 'split'], 'camera': ['punch', 'push', 'pan-l', 'pan-r', 'vertigo'], 'cuts': ['whip', 'zoom', 'slide-up', 'doors', 'push', 'light']},
    'gentle-story':   {'feature': ['soft', 'split', 'center', 'split-r'], 'camera': ['dolly', 'handheld', 'crane', 'pan-l', 'pan-r', 'reveal', 'pull'], 'cuts': ['blur', 'light', 'dip', 'rack', 'wipe', 'zoom']},
    'playful-pop':    {'feature': ['stickers', 'center', 'full', 'split-r'], 'camera': ['sway', 'push', 'arc', 'punch', 'handheld'], 'cuts': ['whip', 'iris', 'slide-up', 'doors', 'zoom', 'light']},
    'editorial-type': {'feature': ['editorial', 'split', 'split-r', 'full'], 'camera': ['none', 'pan-l', 'pan-r', 'push', 'reveal'], 'cuts': ['wipe', 'slide-up', 'doors', 'dip', 'push', 'rack']},
}
VARIETY = {'calm': 2, 'balanced': 3, 'rich': 9}   # how many palette entries the director may use
MEDIA_EXT = ('.png', '.jpg', '.jpeg', '.webp')


def style_motion(style):
    p = TPL / 'styles' / f'{style}.js'
    m = re.search(r"motionDefault\s*:\s*'([\w-]+)'", p.read_text()) if p.exists() else None
    return m.group(1) if m else 'cinematic-3d'


_CACHE = {}


def analyze(path):
    """What a picture is and where its weight sits. None if it cannot be read (a clip, a missing file)."""
    path = Path(path)
    if path in _CACHE: return _CACHE[path]
    out = None
    try:
        import numpy as np
        from PIL import Image
        im = Image.open(path)
        w, h = im.size
        rgba = np.asarray(im.convert('RGBA').resize((192, max(1, round(192 * h / w)))))
        alpha = rgba[..., 3] > 200
        g = np.asarray(Image.fromarray(rgba[..., :3]).convert('L')).astype(float)
        e = np.zeros_like(g)
        e[:, 1:] = np.abs(np.diff(g, axis=1)); e[1:, :] = np.maximum(e[1:, :], np.abs(np.diff(g, axis=0)))
        e[~alpha] = 0
        H, W = e.shape
        tot = e.sum() + 1e-9
        ys, xs = np.mgrid[0:H, 0:W]
        third = lambda a: a.sum() / tot
        out = {
            'size': [w, h], 'aspect': w / h, 'cutout': bool(0.15 < alpha.mean() < 0.9),
            'density': float((e > 14).mean()), 'bright': float(g[alpha].mean() / 255) if alpha.any() else 0.5,
            'sx': float((xs * e).sum() / tot / W), 'sy': float((ys * e).sum() / tot / H),   # where the detail (the subject) sits, 0–1
            'left': float(third(e[:, :W // 3])), 'right': float(third(e[:, -W // 3:])), 'bottom': float(third(e[-H // 3:, :])),
        }
        try:
            sys.path.insert(0, str(HERE)); import suggest_rects
            out['chart'] = bool(suggest_rects.is_chart(path))
        except Exception:
            out['chart'] = False
    except Exception:
        out = None
    _CACHE[path] = out
    return out


def _media(sc):
    m = sc.get('media') if isinstance(sc.get('media'), str) else (sc.get('image') if isinstance(sc.get('image'), str) else None)
    return m if m and m.lower().endswith(MEDIA_EXT) else None


def plan_shots(spec, base_dir, roles=None):
    """[{layout, camera, cut, motion, why, auto}] per scene, plus a list of design warnings (a set choice that no longer
    fits the scene). roles: intake's role per resolved media path ('photo', 'desktop', 'figure', …), when known."""
    base_dir = Path(base_dir); roles = roles or {}
    mo = spec.get('motion') or style_motion(spec.get('style', '')) or 'cinematic-3d'
    own = (spec.get('motions') or {}).get(mo) or {}
    pal = SHOT_PALETTE.get(mo) or SHOT_PALETTE.get(own.get('like'), SHOT_PALETTE['cinematic-3d'])
    if own.get('palette'):   # a film's own language may bring its own palette of layouts, moves and cuts
        pal = {**pal, **{k: v for k, v in own['palette'].items() if isinstance(v, list) and v}}
    d = spec.get('direction') or {}
    var = d.get('variety', 'balanced') if isinstance(d, dict) else 'balanced'
    k = VARIETY.get(var, 3)
    feats, cams, cuts = pal['feature'][:k], pal['camera'][:max(2, k)], pal['cuts'][:max(2, k)]
    scenes = spec.get('scenes', [])
    plan, warns, last, used = [], [], {}, {}
    strong_left = {'calm': 0.25, 'balanced': 0.45, 'rich': 0.7}.get(var, 0.45) * max(1, len(scenes))
    prev_ch, pan_i = None, 0
    hero_i = next((i for i, sc in enumerate(scenes) if sc.get('hit') == 'hero'), None)
    if hero_i is None: hero_i = next((i for i, sc in enumerate(scenes) if sc.get('type') == 'finale'), None)

    def pick(options, avoid, score=lambda o: 0, kind=''):
        """Best fit for the material, then the least used, then palette order; the option used last time is held back
        (a penalty of 3) unless the material clearly asks for it. Counted, so a long film works through the palette instead of ping-ponging between two."""
        if not options: return None
        ranked = sorted(options, key=lambda o: (-(score(o) - (3 if o == avoid else 0) - 0.6 * used.get((kind, o), 0)), options.index(o)))
        used[(kind, ranked[0])] = used.get((kind, ranked[0]), 0) + 1
        return ranked[0]

    def nearest(want, options):   # the wanted layout if the palette has it, else the closest relative
        if want in options: return want
        fam = {'split': ['split', 'split-r', 'editorial'], 'split-r': ['split-r', 'split', 'editorial'], 'full': ['full', 'center', 'soft'],
               'center': ['center', 'full', 'soft']}.get(want, [want])
        return next((o for o in fam if o in options), options[0] if options else want)

    for i, sc in enumerate(scenes):
        t = sc.get('type')
        m = _media(sc)
        a = analyze(base_dir / m) if m else None
        role = roles.get(str((base_dir / m).resolve())) if m else None
        is_photo = sc.get('frame') == 'photo' or role in ('photo', 'cutout') or (a and a['cutout'])
        why = []
        # layout ------------------------------------------------------------------------------------------------
        layout, auto = sc.get('layout'), not sc.get('layout')
        pts = sc.get('points', []) or []
        boxed = [b for b in (rect_of(base_dir, m, p_.get('rect')) for p_ in pts if p_.get('rect')) if b]
        bw = (sc.get('base') or (a['size'] if a and is_photo else [1920, 1080]))[0]
        if t == 'feature':
            chart = bool(a and a.get('chart'))
            # the material decides first (a fit of 6–7 outweighs the no-repeat penalty of 3); variety only breaks ties
            if is_photo or chart or not boxed:
                fit = lambda o: 6 if o in ('full', 'center', 'soft', 'stickers') else 0
                why_l = ('a photograph' if is_photo else 'a chart' if chart else 'no boxed region') + ': the whole frame carries it'
            else:
                cx = sum(r[0] + r[2] / 2 for r in boxed) / len(boxed) / bw
                side = 'split' if cx >= 0.5 else 'split-r'   # the list sits on the side of the boxes: the eye travels a short way from number to badge
                dense = bool(a and a['density'] > 0.12)
                if len(boxed) >= 3 or dense:
                    want = nearest(side, feats)
                    fit = lambda o: 7 if o == want else 3 if o in LIST_LAYOUTS else 0
                    why_l = f'{len(boxed)} boxed points{" on a dense screen" if dense else ""}, boxes on the {"right" if cx >= 0.5 else "left"}: a numbered list beside them'
                else:
                    fit = lambda o: 6 if o in ('center', 'full', 'soft', 'stickers') else 2
                    why_l = f'{len(boxed)} boxed point(s) on a calm screen: the screen carries it'
            if auto: layout = pick(feats, last.get('feature'), fit, 'feature'); why.append(f'{why_l} → {layout}')
            elif layout in LIST_LAYOUTS and len(pts) < 2:
                warns.append((i, f'layout "{layout}" is a numbered list, but the scene has {len(pts)} point', 'use "center" or "full", or remove "layout" and let the director choose'))
        elif t in ('photo', 'footage'):
            if t == 'footage' and not a and sc.get('poster'): a = analyze(base_dir / sc['poster'])   # a still from the clip
            if auto and sc.get('side'): layout = sc['side']; why.append('"side" set in film.json')
            elif auto:
                opts = ['left', 'right', 'bottom', 'center', 'split'][:max(3, k + 1)]
                if a:
                    quiet = min(('left', a['left']), ('right', a['right']), ('bottom', a['bottom']), key=lambda x: x[1])
                    busy_all = min(a['left'], a['right'], a['bottom']) > 0.3
                    if busy_all and 'split' in opts: want, why_l = 'split', 'busy everywhere: the picture framed, the line on clean space'
                    else: want, why_l = quiet[0], f'the {quiet[0]} is the quiet part of the picture (subject at {a["sx"]:.0%} across): the line goes there'
                    layout = pick(opts, last.get('photo'), lambda o: 7 if o == want else 0, 'photo'); why.append(f'{why_l} → {layout}')
                else:
                    layout = pick(opts, last.get('photo'), kind='photo')
                last['photo'] = layout
            elif a and layout in ('left', 'right', 'bottom') and a[layout] > 0.42:
                warns.append((i, f'the line sits on the busiest part of the photo ({layout})', 'use the quiet side, "split", or remove "layout" and let the director choose'))
        elif t == 'gallery' and auto:
            items = sc.get('items', [])
            an = [analyze(base_dir / it['media']) for it in items if isinstance(it, dict) and it.get('media')]
            charts = sum(1 for x in an if x and x.get('chart'))
            opts = ['coverflow', 'grid', 'strip'][:max(1, k)]
            fit = lambda o: (2 if o == 'grid' and len(items) <= 4 else 0) + (2 if o == 'strip' and len(items) >= 3 and charts >= len(items) / 2 else 0)
            layout = pick(opts, last.get('gallery'), fit, 'gallery')
            why.append(f'{len(items)} items{f", {charts} charts" if charts else ""} → {layout}')
        elif t == 'carousel' and auto:
            layout = pick(['menu', 'stack'][:max(1, k - 1)], last.get('carousel'), kind='carousel')
            why.append('breadth; alternates menu and stack')
        elif t == 'detail' and auto:
            crops = sc.get('crops', [])
            labelled = sum(1 for c in crops if c.get('zh'))
            small = [c['rect'] for c in crops if c.get('rect') and c['rect'][2] < 0.35 * bw]
            if is_photo or not labelled or k < 3: layout, w_ = 'macro', 'a texture or unlabelled crops → full-frame close-ups'
            else: layout, w_ = ('split', 'small labelled regions of a screen → the whole with a box, the region magnified') if small else ('macro', 'large labelled regions → full-frame close-ups')
            last['detail'] = layout; why.append(w_)
        if layout: last[t] = layout
        # camera ------------------------------------------------------------------------------------------------
        camera = sc.get('camera')
        if not camera:
            toward = None
            if a and is_photo and abs(a['sx'] - 0.5) > 0.08: toward = 'pan-l' if a['sx'] > 0.5 else 'pan-r'   # the frame drifts toward the subject
            if t in ('photo', 'hero') and 'handheld' in cams:
                camera = 'handheld'; why.append('photograph breathes (handheld)')
            elif t == 'photo' and toward and k >= 3:
                camera = toward; why.append(f'drifts toward the subject ({a["sx"]:.0%} across)')
            elif t in ('cover', 'endcard', 'finale', 'hero', 'photo', 'detail', 'clip', 'phone', 'flow', 'hub', 'type', 'chart', 'footage', 'custom', 'mg'):
                camera = None   # these move inside the frame already (push-ins, reveals): the language's own camera
            elif t in ('statement', 'quote'):
                camera = 'push' if k >= 3 else None
                if camera: why.append('a slow push on the line')
            elif t in ('carousel', 'gallery'):
                camera = ['pan-l', 'pan-r'][pan_i % 2] if k >= 3 else None; pan_i += camera is not None
                if camera: why.append('lateral drift with the slides')
            else:
                camera = pick(cams, last.get('camera_' + t) or last.get('camera'), kind='camera')
                if camera in ('pan-l', 'pan-r'): camera = ['pan-l', 'pan-r'][pan_i % 2]; pan_i += 1
                last['camera_' + t] = camera
            if camera: last['camera'] = camera
        # cut into this scene -----------------------------------------------------------------------------------
        cut = sc.get('cut')
        ch = (sc.get('chapter') or [None])[0]
        new_ch = bool(ch and ch != prev_ch)
        if ch: prev_ch = ch
        if not cut:
            if i == 0 or t == 'endcard': cut = 'style'
            elif i == hero_i: cut = cuts[0]; why.append('the hero takes the signature cut')
            elif i > 0 and scenes[i - 1].get('type') == 'pain': cut = 'push' if 'push' in cuts or k >= 3 else cuts[0]; why.append('out of the pain')
            elif t == 'statement' and strong_left >= 1:
                cut = 'dip' if 'dip' in pal['cuts'] else ('light' if 'light' in pal['cuts'] else ('blur' if k >= 3 else 'style'))
                if cut != 'style': why.append('into a breath')
            elif (new_ch or (not prev_ch and i % 3 == 0)) and strong_left >= 1:
                cut = pick(cuts[1:] or cuts, last.get('cut'), kind='cut'); why.append('a new chapter' if new_ch else 'a turn in the story')
            else: cut = 'style'
        if cut != 'style': strong_left -= 1; last['cut'] = cut
        plan.append({'layout': layout, 'camera': camera, 'cut': cut, 'motion': sc.get('motion'), 'why': '; '.join(why), 'auto': auto,
                     'size': shot_size(sc, layout, a)})
    # 景别 rhythm: never three shots of the same size in a row (graphics and cards do not count)
    run, prev = 0, None
    for i, p_ in enumerate(plan):
        sz = p_['size'].split('→')[-1] if p_['size'] not in ('graphic', 'card') else None
        run = run + 1 if sz and sz == prev else (1 if sz else 0); prev = sz
        if run == 3:
            warns.append((i, f'three {sz} shots in a row (景别 {SIZE_NAMES.get(sz, sz)})', 'vary the size: a wider context or a closer detail between them (a detail scene, a photo, a crop), or a breath'))
    return plan, warns


SIZE_NAMES = {'ECU': '大特写', 'CU': '特写', 'MS': '中景', 'WS': '全景'}


def shot_size(sc, layout, a):
    """The shot size (景别) a scene lands on: ECU / CU / MS / WS, 'A→B' when the scene moves between them, 'graphic' for
    type, maps and charts, 'card' for the name and the end card."""
    t = sc.get('type')
    if t in ('flow', 'hub', 'type', 'chart', 'statement', 'numbers', 'compare', 'pain', 'quote'): return 'graphic'
    if t == 'mg': return sc.get('size') or 'graphic'
    if t == 'endcard': return 'card'
    if t == 'custom': return sc.get('size') or 'free'   # the director's cut sets its own frame
    if t == 'cover':
        if sc.get('focus'): return 'CU→WS' if sc.get('frame') == 'photo' else 'WS→CU'
        return 'WS'
    if t == 'feature':
        boxed = any(p_.get('rect') for p_ in sc.get('points', []))
        return ('WS→CU' if layout == 'full' else 'MS→CU') if boxed else 'MS'
    if t == 'detail':
        base = sc.get('base') or (a['size'] if a else [1920, 1080])
        crops = [c['rect'] for c in sc.get('crops', []) if isinstance(c.get('rect'), list)]   # "@name" crops resolve later
        small = crops and min(c[2] for c in crops) < 0.25 * base[0]
        return 'MS+CU' if layout == 'split' else ('ECU' if small or not crops else 'CU')
    if t in ('photo', 'footage'): return 'MS' if sc.get('focus') else 'WS'
    if t == 'hero': return 'MS'
    if t == 'finale': return 'CU' if sc.get('hero') in ('rise', 'result') else 'WS'
    if t in ('carousel', 'gallery', 'phone', 'clip'): return 'MS'
    if t == 'lineup': return 'WS'
    return 'MS'


def shot_table(spec, plan):
    rows = []
    for i, (sc, p_) in enumerate(zip(spec.get('scenes', []), plan)):
        frame = ' · '.join(x for x in [p_['layout'] or '', f"cam {p_['camera']}" if p_['camera'] else '', f"cut {p_['cut']}" if p_['cut'] != 'style' else ''] if x)
        note = p_['why'] or (f"proposal: {sc['_shot']}" if sc.get('_shot') else 'your choice' if not p_['auto'] else '')
        rows.append(f"  {i:>2} {sc.get('type', ''):<10} {p_['size']:<8} {frame or '(defaults)':<36} {note}"
                    + (f"  [motion {p_['motion']}]" if p_['motion'] else ''))
    return ('storyboard — the director\'s proposal: size (景别 ECU/CU/MS/WS) · layout · camera · cut · why. Every row is a starting point: '
            'change "layout" / "camera" / "cut" / "motion" on any scene, or write your own scene, move or cut (references/custom-scenes.md):\n' + '\n'.join(rows))


def apply(spec, base_dir, roles=None):
    """Write the plan into the scenes (layout / camera / cut + "_shot" = why). Used by autofilm for the draft."""
    plan, _ = plan_shots(spec, base_dir, roles)
    for sc, p_ in zip(spec.get('scenes', []), plan):
        if p_['layout'] and not sc.get('layout') and sc.get('type') in LAYOUTS: sc['layout'] = p_['layout']
        if p_['camera'] and not sc.get('camera'): sc['camera'] = p_['camera']
        if p_['cut'] != 'style' and not sc.get('cut'): sc['cut'] = p_['cut']
        if p_['why']: sc['_shot'] = p_['why']
    return plan


if __name__ == '__main__':
    f = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else sys.exit(__doc__)
    spec = json.load(open(f))
    plan, warns = plan_shots(spec, f.parent)
    print(shot_table(spec, plan))
    for i, msg, fix in warns: print(f'WARN  scenes[{i}]: {msg}\n  FIX: {fix}')


# ---------------------------------------------------------------- shot wishlist (for the user or a real crew)
SOFTWARE = {'software-saas', 'developer-ai', 'science-data', 'finance-fintech', 'mobile-consumer-app'}
SPECS = ('4K (3840×2160) or more, 30 fps (60 fps for slow motion), shutter about 1/60 (double the frame rate), locked exposure '
         'and white balance, a neutral or log profile; stills as RAW or best-quality JPEG; a transparent PNG for every cut-out')


def wishlist(genre, counts, name='the product'):
    """Markdown: the shots that would lift this film most, marked covered (✓) or missing (✗) from the materials' counts
    {screens, outputs, photos, footage, cutouts, macro, packshot, recordings}. AI prompts only for atmosphere shots."""
    c = counts
    if genre in SOFTWARE:
        shots = [
            ('CU', 'the one output that matters, enlarged (a plot, a report, the result), captured at 2×', c.get('outputs', 0) >= 3, 'capture_app.mjs: open it full screen or "enlarge" before the shot'),
            ('MS', 'a screen recording of the core action, 5–8 s, one smooth pass, no cursor wandering', c.get('recordings', 0) >= 1, 'macOS: ⌘⇧5 · record one window; or capture_app.mjs "seq"'),
            ('WS', f'{name} on a real device in a real place (a laptop on a desk by a window)', c.get('photos', 0) + c.get('footage', 0) >= 1, 'soft window light from the side, the screen bright, nothing else on the desk'),
            ('MS', 'hands at work with it (keyboard, trackpad, a phone in hand), the face out of frame or with consent', c.get('footage', 0) >= 1, 'a slow slide or locked-off; 5–10 s'),
        ]
    else:
        shots = [
            ('MS', f'the hero: {name} at a three-quarter angle on a clean ground (seamless paper)', c.get('packshot', 0) + c.get('cutouts', 0) >= 1, 'key light 45° and soft, a rim light behind for the edge, a white card for fill'),
            ('ECU', 'the texture: material, finish, stitching, glaze, grain — the detail only the product has', c.get('macro', 0) >= 1, 'macro lens, raking light across the surface'),
            ('MS', 'in use: hands doing the one thing it is for (pour, press, wear, open)', c.get('footage', 0) >= 1 or c.get('photos', 0) >= 2, 'eye level, shallow depth of field, 5–10 s of motion'),
            ('WS', 'in its place: where it lives (a kitchen, a desk, a trail, a room)', c.get('photos', 0) >= 1, 'golden hour or window light; the product small in the frame'),
            ('MS', 'the moment it works (it turns on, steam rises, it fits) — the hero of the film in motion', c.get('footage', 0) >= 1, 'a slow push or a locked-off shot; real time or 60 fps for slow motion'),
            ('CU', 'a person\'s reaction or hands (with consent): the feeling, not a pose', False, 'natural light; never a stock smile'),
        ]
    rows = '\n'.join(f'| {"✓" if have else "✗"} | {sz} ({SIZE_NAMES.get(sz, sz)}) | {what} | {how} |' for sz, what, have, how in shots)
    missing = [w for _, w, have, _ in shots if not have]
    place = 'a calm, real-looking place that fits ' + name if genre not in SOFTWARE else 'a quiet desk by a window in soft morning light'
    prompts = [
        f'Cinematic establishing shot of {place}, slow dolly in, shallow depth of field, soft natural light, muted palette, no people, no logos, no text, no product, photorealistic, 16:9',
        'Macro b-roll of light moving across a natural surface (wood, linen or stone), slow, soft focus falloff, no text, no logos, no product, photorealistic, 16:9',
    ]
    return (f'# Shot wishlist · 补拍清单 — {name}\n\n'
            'What would lift this film most, from what the materials already have (✓) and lack (✗). Shoot the ✗ rows if you can; '
            'the film is made either way, and autofilm puts any new footage or photos to work when you rerun it.\n\n'
            '| | size · 景别 | shot | how |\n| --- | --- | --- | --- |\n' + rows + '\n\n'
            f'**Specs:** {SPECS}.\n\n'
            '**AI-generated mood shots (optional, atmosphere only).** Never generate the product, its screens or its results: a fake '
            'product is a false claim. Use these only for places and light, label them as AI-generated in the report, and replace them '
            'with real footage when you can:\n\n' + '\n'.join(f'- `{p}`' for p in prompts) + '\n\n'
            + (f'Missing now: {"; ".join(missing)}.\n' if missing else 'Nothing essential is missing.\n'))


# ---------------------------------------------------------------- named regions: "rect": "@APA 三线表"
def rect_of(base_dir, media, r):
    """A rect as [x, y, w, h], resolving a "@name" through the shot's regions; None if it cannot be resolved."""
    if isinstance(r, list) and len(r) == 4: return r
    if isinstance(r, str):
        reg = regions_for(base_dir, media)
        return find_region(reg, r) if reg else None
    return None


def regions_for(base_dir, media):
    """The exact boxes capture_app.mjs recorded for a shot (<shot>.regions.json next to it), or None."""
    if not media: return None
    p = (Path(base_dir) / media).with_suffix('.regions.json')
    if not p.exists(): p = Path(str(Path(base_dir) / media) + '.regions.json')
    try: return json.load(open(p)) if p.exists() else None
    except Exception: return None


def find_region(reg, name):
    """The box a name points at: the text that matches, grown to the smallest card or panel around it (2–35 % of the
    screen) — a highlight frames the card the point is about, not one line of its label."""
    W, H = reg.get('base', [1920, 1080]); R = reg.get('regions', [])
    want = name.strip().lstrip('@').strip().lower()
    hits = [r for r in R if r['text'] and r['text'].strip().lower() == want] or [r for r in R if want and want in (r['text'] or '').lower()]
    if not hits: return None
    hit = min(hits, key=lambda r: (r['kind'] not in ('heading', 'text', 'button'), r['rect'][2] * r['rect'][3]))
    x, y, w, h = hit['rect']; cx, cy = x + w / 2, y + h / 2
    around = [r for r in R if r['kind'] == 'panel' and r['rect'][0] <= cx <= r['rect'][0] + r['rect'][2] and r['rect'][1] <= cy <= r['rect'][1] + r['rect'][3]
              and 0.02 <= r['rect'][2] * r['rect'][3] / (W * H) <= 0.35]
    if around: return min(around, key=lambda r: r['rect'][2] * r['rect'][3])['rect']
    pad = 12
    return [max(0, x - pad), max(0, y - pad), min(W, w + 2 * pad), min(H, h + 2 * pad)]


def named_panels(reg, k=8):
    """The names of the biggest labelled cards and panels on a screen (what a highlight could point at)."""
    if not reg: return []
    W, H = reg.get('base', [1920, 1080]); seen, out = set(), []
    for r in sorted(reg.get('regions', []), key=lambda r: -r['rect'][2] * r['rect'][3]):
        a = r['rect'][2] * r['rect'][3] / (W * H)
        t = (r['text'] or '').strip()
        x, y, w, h = r['rect']
        wordy = len(re.findall(r'[A-Za-z\u4e00-\u9fff]', t)) >= 2                      # a real name, not an icon or a number
        bar = w > 0.7 * W or (y < 0.07 * H and h < 0.1 * H) or (y + h > 0.95 * H and h < 0.1 * H)   # app chrome: top bars, toolbars
        transient = re.search(r'\.\.\.|…|正在|loading', t, re.I)
        if r['kind'] in ('panel', 'heading') and wordy and not bar and not transient and 2 <= len(t) <= 24 and 0.02 <= a <= 0.35 and t not in seen:
            seen.add(t); out.append(t)
        if len(out) >= k: break
    return out


def resolve_rects(spec, base_dir):
    """Replace every "@name" rect / crop / focus with the exact box from the shot's regions file. Returns errors."""
    errs = []
    def res(sc_i, where, media, val):
        reg = regions_for(base_dir, media)
        if reg is None:
            errs.append((f'scenes[{sc_i}]{where}: "{val}" names a region, but {media} has no .regions.json',
                         'named regions come from capture_app.mjs shots; for other images give [x, y, w, h] (suggest_rects.py --preview)')); return None
        r = find_region(reg, val)
        if r is None:
            errs.append((f'scenes[{sc_i}]{where}: no region named "{val}" on {Path(media).name}',
                         'use one of: ' + ', '.join(f'"@{n}"' for n in named_panels(reg, 12)))); return None
        return r
    for i, sc in enumerate(spec.get('scenes', [])):
        m = sc.get('media') if isinstance(sc.get('media'), str) else None
        for j, p_ in enumerate(sc.get('points', []) or []):
            if isinstance(p_.get('rect'), str): p_['rect'] = res(i, f'.points[{j}].rect', m, p_['rect']) or p_.pop('rect', None)
        for j, c in enumerate(sc.get('crops', []) or []):
            if isinstance(c.get('rect'), str): c['rect'] = res(i, f'.crops[{j}].rect', m, c['rect'])
        if isinstance(sc.get('focus'), str): sc['focus'] = res(i, '.focus', m, sc['focus'])
        for j, pn in enumerate(sc.get('panels', []) or []):
            if isinstance(pn.get('crop'), str): pn['crop'] = res(i, f'.panels[{j}].crop', pn.get('media'), pn['crop'])
    return errs


def rect_warnings(spec, base_dir):
    """A highlight must frame something: warn when a box sits on near-empty space or is too small to frame a card."""
    out = []
    for i, sc in enumerate(spec.get('scenes', [])):
        m = sc.get('media') if isinstance(sc.get('media'), str) else None
        if sc.get('type') != 'feature' or not m or sc.get('frame') == 'photo': continue
        try:
            import numpy as np
            from PIL import Image
            im = Image.open(Path(base_dir) / m).convert('L')
        except Exception:
            continue
        base = sc.get('base') or [1920, 1080]; k = im.width / base[0]
        g = np.asarray(im).astype(float)
        for j, p_ in enumerate(sc.get('points', []) or []):
            r = p_.get('rect')
            if not isinstance(r, list) or len(r) != 4: continue
            x, y, w, h = r
            if w * h < 0.006 * base[0] * base[1]:
                out.append((i, f'points[{j}] ("{p_.get("zh", "")}") boxes a tiny target ({w}×{h})', 'box the card or panel the point is about (a button reads better inside its panel); the zoom is capped anyway'))
                continue
            a = g[int(y * k):int((y + h) * k), int(x * k):int((x + w) * k)]
            if a.size < 16: continue
            e = np.abs(np.diff(a, axis=1)).mean() + np.abs(np.diff(a, axis=0)).mean()
            if e < 1.2:
                out.append((i, f'points[{j}] ("{p_.get("zh", "")}") boxes a near-empty area', 'the box missed its target: name it instead ("rect": "@<panel name>", from the shot\'s regions) or re-measure with suggest_rects.py --preview'))
    return out
