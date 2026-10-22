#!/usr/bin/env python3
"""The director's look: which style (and the motion that goes with it) fits THIS product's materials. No default and no
lookup table: every style is scored on evidence, and the reasons are returned so the crew can check them.

Evidence, in order of weight:
  1. the pictures: screens or photos, a light or dark UI, how saturated, how dense, charts, the dominant hue's warmth
  2. what the product is (its genre's character) and what the docs say (tone words), counted, capped
  3. the user's own words for the feel (--mood / brief "tone"), which count triple

  choose(items, src, genre_id, text, mood='') -> {'style', 'motion', 'ranked': [(style, score)], 'why': [lines]}
"""
import re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

STYLES = {   # what each look is for
    'midnight-tech':  'dark navy stage, glow, 3D windows: light UI screens glow like lit pages',
    'neon-cyber':     'synthwave neon, glitch cuts: loud, for dark saturated UIs and play',
    'keynote-light':  'bright, airy keynote: calm, for light low-saturation products and devices',
    'paper-academic': 'warm paper, serif, journal plates: evidence and figures as the hero',
    'editorial-mono': 'magazine grid, hard wipes, monochrome: a point of view, graphic and photographic',
    'luxe-noir':      'quiet luxury: black, one warm light, dark or sensual photography',
    'natural-fresh':  'daylight, linen, warm: human, organic, photographed things and places',
    'aurora-glass':   'colourful gradient and frosted glass: young, playful, saturated apps',
}
STYLE_MOTION = {'aurora-glass': 'playful-pop', 'editorial-mono': 'editorial-type', 'luxe-noir': 'gentle-story', 'keynote-light': 'gentle-story',
                'midnight-tech': 'cinematic-3d', 'natural-fresh': 'gentle-story', 'paper-academic': 'precision-data', 'neon-cyber': 'kinetic-launch'}
# what kind of product a genre is: its character, as weights on the looks (shared by every look listed; no order)
GENRE_CHARACTER = {
    'software-saas': {'midnight-tech': 1, 'keynote-light': 1, 'editorial-mono': 0.6},
    'developer-ai': {'neon-cyber': 1, 'midnight-tech': 1, 'editorial-mono': 0.6},
    'science-data': {'midnight-tech': 0.8, 'paper-academic': 1, 'keynote-light': 0.8},
    'finance-fintech': {'midnight-tech': 1, 'keynote-light': 0.8, 'paper-academic': 0.6},
    'mobile-consumer-app': {'aurora-glass': 1, 'keynote-light': 0.8, 'natural-fresh': 0.6},
    'consumer-electronics': {'keynote-light': 1, 'midnight-tech': 0.8, 'luxe-noir': 0.8},
    'fashion-beauty-luxury': {'luxe-noir': 1, 'editorial-mono': 1, 'natural-fresh': 0.6},
    'food-beverage': {'natural-fresh': 1, 'luxe-noir': 0.6, 'keynote-light': 0.6},
    'health-wellness': {'keynote-light': 1, 'natural-fresh': 1, 'paper-academic': 0.6},
    'education-learning': {'keynote-light': 1, 'paper-academic': 0.8, 'aurora-glass': 0.6},
    'mobility-industrial': {'midnight-tech': 1, 'editorial-mono': 0.8, 'luxe-noir': 0.6},
    'travel-hospitality-living': {'natural-fresh': 1, 'luxe-noir': 0.8, 'keynote-light': 0.6},
    'game-entertainment-event': {'neon-cyber': 1, 'aurora-glass': 0.8, 'editorial-mono': 0.6},
    'kids-family': {'aurora-glass': 1, 'natural-fresh': 0.8, 'keynote-light': 0.6},
    'brand-mission': {'editorial-mono': 1, 'keynote-light': 0.6, 'luxe-noir': 0.6},
}
WORDS = {   # the feel in words (user's, brief's, docs'): Chinese and English
    'midnight-tech': r'大气|科技|未来|商业|发布|tech|future|cinematic|premium|bold|launch|深色|夜',
    'neon-cyber': r'赛博|霓虹|游戏|电竞|极客|cyber|neon|game|hacker|energetic|炫酷',
    'keynote-light': r'简洁|清爽|明亮|干净|苹果|keynote|clean|bright|airy|minimal|simple|轻盈|克制',
    'paper-academic': r'论文|期刊|学术|严谨|journal|paper|academic|rigor|scholar|出版',
    'editorial-mono': r'杂志|编辑|瑞士|黑白|editorial|swiss|magazine|mono|manifesto|宣言|态度',
    'luxe-noir': r'奢|高级感|典雅|珠宝|luxury|elegant|noir|refined|couture',
    'natural-fresh': r'自然|温暖|治愈|有机|生活|natural|warm|organic|fresh|human|handmade|田园|人文|亲和',
    'aurora-glass': r'活泼|年轻|彩色|社交|aurora|playful|young|colorful|fun|创意|潮',
}


def _stats(path):
    """Brightness, colourfulness and density of one picture, plus the warmth of its dominant hue."""
    import numpy as np
    from PIL import Image
    import director as DIR, palette as PAL
    a = DIR.analyze(path)
    if not a: return None
    im = np.asarray(Image.open(path).convert('RGB').resize((96, 96))).astype(float) / 255
    mx, mn = im.max(2), im.min(2)
    sat = float(np.where(mx > 0.05, (mx - mn) / np.maximum(mx, 1e-6), 0).mean())
    hue = None
    try:
        h = PAL.hues_of(path, top=1)
        hue = h[0][0] if h and h[0][1] >= 0.08 else None
    except Exception: pass
    return {'bright': a['bright'], 'density': a['density'], 'chart': a.get('chart', False), 'sat': sat, 'hue': hue}


def choose(items, src, gid, text='', mood=''):
    src = Path(src)
    shots, kinds = [], {'screen': 0, 'photo': 0, 'figure': 0}
    for it in items:
        if it.get('kind') != 'image' or it.get('role') not in ('desktop', 'phone', 'photo', 'cutout', 'figure'): continue
        st = _stats(src / it['file'])
        if not st: continue
        st['role'] = 'photo' if it['role'] in ('photo', 'cutout') else ('figure' if it['role'] == 'figure' else 'screen')
        kinds[st['role']] += 1; shots.append(st)
    n = max(1, len(shots))
    share = {k: v / n for k, v in kinds.items()}
    mean = lambda k, rs=None: (sum(s[k] for s in shots if not rs or s['role'] in rs) / max(1, sum(1 for s in shots if not rs or s['role'] in rs)))
    screens = ('screen', 'figure')
    ui_bright, ui_dens, sat = mean('bright', screens), mean('density', screens), mean('sat')
    photo_bright = mean('bright', ('photo',)) if kinds['photo'] else None
    ns = max(1, sum(1 for s in shots if s['role'] in screens))
    charts = sum(1 for s in shots if s['chart'] and s['role'] in screens) / ns   # a share of the screens, not of the photos
    hues = [s['hue'] for s in shots if s['hue'] is not None]
    warm = (sum(1 for h in hues if h < 70 or h > 330) / len(hues)) if hues else 0.0
    sc, why = {k: 0.0 for k in STYLES}, {k: [] for k in STYLES}
    def add(k, v, r):
        if v: sc[k] += v; why[k].append(f'{r} ({v:+.1f})')
    # 1 · the pictures
    if share['screen'] + share['figure'] >= 0.5:
        add('midnight-tech', 0.8 if ui_bright > 0.55 else 0.5, f'screen-led, UI {"light: white windows glow on the dark stage" if ui_bright > 0.55 else "dark: it blends into the stage"}')
        if ui_bright > 0.6 and sat < 0.12: add('keynote-light', 0.9, 'a light, low-saturation UI sits naturally on a bright stage')
        if ui_bright > 0.7:   # a white UI on either stage: what separates them is how much there is to read
            if ui_dens >= 0.12: add('midnight-tech', 0.2, 'dense small text: highlights and boxes pop hardest against a dark ground')
            else: add('keynote-light', 0.2, 'a sparse, airy UI blends with a bright stage')
        if ui_bright < 0.4 and sat > 0.2: add('neon-cyber', 1.0, 'dark UI with saturated colour')
        if sat > 0.28: add('aurora-glass', 0.9, 'a saturated, colourful UI')
        if charts >= 0.2: add('paper-academic', 0.9, f'{charts:.0%} of the screens are charts and figures: evidence is the hero')
        if ui_dens > 0.2: add('paper-academic', 0.3, 'dense information reads well on a calm ground'); add('keynote-light', 0.2, 'dense information reads well on a calm ground')
    if share['photo'] >= 0.4:
        if photo_bright is not None and photo_bright < 0.38: add('luxe-noir', 1.2, 'dark, moody photography')
        if warm >= 0.4: add('natural-fresh', 1.2, 'warm dominant hues in the photographs')
        if photo_bright is not None and photo_bright >= 0.5 and sat < 0.2: add('keynote-light', 1.0, 'bright, clean, low-saturation product photography')
        if sat < 0.1: add('editorial-mono', 0.9, 'near-monochrome photography')
        if sat > 0.3: add('aurora-glass', 0.6, 'saturated photography')
    # 2 · what the product is, and what the docs say
    for k, w in GENRE_CHARACTER.get(gid, {}).items(): add(k, 1.0 * w, f'a {gid} product')
    for k, kw in WORDS.items():
        hits = min(4, len(re.findall(kw, text.lower(), re.I)))
        add(k, hits * 0.1, f'the docs\' tone words ×{hits}' if hits else '')
    # 3 · the user's own words
    for k, kw in WORDS.items():
        hits = len(re.findall(kw, mood.lower(), re.I))
        add(k, hits * 3, f'you said it: ×{hits}' if hits else '')
    ranked = sorted(sc.items(), key=lambda x: x[1], reverse=True)
    best = ranked[0][0]
    motion = STYLE_MOTION[best]
    mwhy = f'{best} moves like {motion}'
    if best in ('midnight-tech', 'keynote-light') and ui_dens > 0.2 and share['screen'] + share['figure'] >= 0.5 and mood.strip() == '':
        motion, mwhy = 'precision-data', 'dense information on screen: exact, calm snaps read better than 3D drift'
    lines = [f'look {best}: ' + '; '.join(why[best]), f'motion {motion}: {mwhy}']
    for k, v in ranked[1:3]: lines.append(f'  also {k} ({v:.1f}): ' + '; '.join(why[k][:3]))
    facts = f'{kinds["screen"]} screens, {kinds["photo"]} photos, {kinds["figure"]} figures · UI brightness {ui_bright:.2f} · saturation {sat:.2f} · density {ui_dens:.2f} · charts {charts:.0%} · warm hues {warm:.0%}'
    return {'style': best, 'motion': motion, 'ranked': ranked, 'why': lines, 'facts': facts}
