"""The colour director: picks the film's accent colours from colour psychology, the brand and the materials.

Usage:
  python3 scripts/palette.py <materials folder> --genre food-beverage --style natural-fresh [--logo logo.png]
      → prints {"accent": "#…", "accent2": "#…", "why": "…"}; autofilm.py writes it into film.json "palette"

How it chooses, in order:
  1. The brand comes first. A clear colour in the logo is the accent (brand consistency beats any table), tuned only in
     lightness so it reads on the style's background.
  2. Otherwise colour psychology for the product type (GENRE_COLOURS): each genre lists the hues that carry its feeling
     (food: appetite and warmth → amber, tomato, olive; medicine and science: trust and calm precision → teal, blue)
     and the hues to avoid (blue suppresses appetite; red reads as alarm in a clinical product).
  3. Harmony with the materials: the candidates are scored against the dominant hue of the pictures, which fill most of
     every frame. Analogous (≤ 40°) echoes them; near-complementary (150–210°) makes the accent pop for products that
     want energy; the clashing band (60–120° away) is avoided.
  4. Taste and legibility: lightness and saturation are set for the style (bright and clear on a dark ground, deeper on
     a light one, muted for luxury and editorial), and the accent must reach 3:1 contrast with the background (WCAG
     non-text). The second accent is analogous for calm products and split-complementary for lively ones.
  5. 60-30-10: the style keeps the background (60) and the ink (30); the accent is the 10 — one accent per frame.
"""
import argparse
import colorsys
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = HERE.parent / 'templates'

# hue in degrees; feeling; what to avoid (hue ranges) and why. Energy: calm products take analogous second accents.
GENRE_COLOURS = {
    'software-saas':            {'hues': [215, 255, 175], 'feel': 'clarity and trust (blue), modern craft (violet)', 'avoid': [], 'energy': 'calm'},
    'developer-ai':             {'hues': [265, 190, 85], 'feel': 'intelligence (violet), signal (cyan), a spark of energy (lime)', 'avoid': [], 'energy': 'lively'},
    'science-data':             {'hues': [172, 205, 220], 'feel': 'trust, calm and precision (teal, blue)', 'avoid': [(345, 20, 'red reads as alarm or error in a clinical, data product')], 'energy': 'calm'},
    'finance-fintech':          {'hues': [150, 220, 45], 'feel': 'growth (green), trust (navy blue), value (gold)', 'avoid': [(350, 15, 'red means loss in money')], 'energy': 'calm'},
    'mobile-consumer-app':      {'hues': [12, 45, 200], 'feel': 'friendly warmth (coral), optimism (sun), ease (sky)', 'avoid': [], 'energy': 'lively'},
    'consumer-electronics':     {'hues': [210, 25, 190], 'feel': 'precision (steel blue), a signal of power (orange)', 'avoid': [], 'energy': 'lively'},
    'fashion-beauty-luxury':    {'hues': [40, 350, 15], 'feel': 'value and warmth (muted gold), intimacy (blush), richness (oxblood)', 'avoid': [(90, 200, 'cool greens and cyans read clinical, not luxurious')], 'energy': 'calm'},
    'food-beverage':            {'hues': [32, 12, 80], 'feel': 'appetite and warmth (amber, tomato), freshness and nature (olive)', 'avoid': [(200, 290, 'blue and purple suppress appetite')], 'energy': 'calm'},
    'health-wellness':          {'hues': [140, 172, 22], 'feel': 'calm and recovery (sage), care (soft teal), human warmth (peach)', 'avoid': [(350, 10, 'pure red reads as alarm')], 'energy': 'calm'},
    'education-learning':       {'hues': [45, 210, 130], 'feel': 'curiosity and optimism (yellow), focus (blue), growth (green)', 'avoid': [], 'energy': 'lively'},
    'mobility-industrial':      {'hues': [25, 210, 50], 'feel': 'safety and action (orange), engineering (steel blue)', 'avoid': [], 'energy': 'lively'},
    'travel-hospitality-living': {'hues': [16, 38, 200, 140], 'feel': 'hearth and welcome (terracotta, sand), water and air (lake blue), nature (forest)', 'avoid': [], 'energy': 'calm'},
    'game-entertainment-event': {'hues': [320, 230, 90], 'feel': 'excitement (magenta), depth (electric blue), play (acid green)', 'avoid': [], 'energy': 'lively'},
    'kids-family':              {'hues': [30, 200, 110], 'feel': 'joy (tangerine), safety (sky), growing (leaf) — soft, never neon', 'avoid': [], 'energy': 'lively'},
    'brand-mission':            {'hues': [150, 215, 20], 'feel': 'conviction (deep green), trust (blue), warmth (terracotta)', 'avoid': [], 'energy': 'calm'},
}
MUTED_STYLES = {'luxe-noir', 'editorial-mono', 'paper-academic', 'natural-fresh'}
NAMES = [(15, 'red'), (40, 'orange'), (65, 'amber'), (90, 'yellow-green'), (150, 'green'), (190, 'teal'), (230, 'blue'), (275, 'violet'), (330, 'magenta'), (360, 'red')]


def name_of(h):
    return next(n for lim, n in NAMES if h % 360 <= lim)


def hexc(rgb): return '#%02x%02x%02x' % tuple(max(0, min(255, round(c * 255))) for c in rgb)


def rgb_of(hx): hx = hx.lstrip('#'); return tuple(int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4))


def lum(rgb):
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(c) for c in rgb); return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)


def hue_dist(a, b): d = abs(a - b) % 360; return min(d, 360 - d)


def style_bg(style):
    css = (TPL / 'styles' / f'{style}.css').read_text() if (TPL / 'styles' / f'{style}.css').exists() else ''
    m = re.search(r'--bg-edge:\s*(#[0-9a-fA-F]{6})', css)
    a = re.search(r'--accent:\s*(#[0-9a-fA-F]{6})', css)
    return (m.group(1) if m else '#02060d'), (a.group(1) if a else '#2ee6c5')


def hues_of(path, vivid=False, top=3):
    """Dominant saturated hues of a picture: [(hue, share, sat, light)]. vivid=True (a logo): weight by how vivid a
    colour is, not by area, and ignore near-black and near-white — a logo's signature is its brightest colour, not its
    dark ground."""
    try:
        import numpy as np
        from PIL import Image
        im = Image.open(path).convert('RGBA'); im.thumbnail((160, 160))
        a = np.asarray(im).astype(float) / 255
        keep = a[..., 3] > 0.8
        rgb = a[..., :3][keep]
        if not len(rgb): return []
        hsv = np.array([colorsys.rgb_to_hls(*p) for p in rgb[:: max(1, len(rgb) // 4000)]])   # h, l, s
        lo_l = 0.3 if vivid else 0.15
        sat = (hsv[:, 2] > 0.28) & (hsv[:, 1] > lo_l) & (hsv[:, 1] < 0.88)
        if sat.mean() < 0.03: return []
        h = (hsv[sat, 0] * 360).astype(int) // 15
        w = hsv[sat, 2] * (1 - np.abs(hsv[sat, 1] - 0.55)) if vivid else np.ones(sat.sum())   # vividness: saturated, mid-light
        out = []
        for b in np.argsort(-np.bincount(h, weights=w, minlength=24))[:top]:
            sel = h == b
            if sel.sum() < 0.08 * sat.sum(): continue
            out.append((int(b * 15 + 7), float(sel.sum() / len(hsv)), float(hsv[sat][sel, 2].mean()), float(hsv[sat][sel, 1].mean())))
        return out
    except Exception:
        return []


def tune(h, bg_hex, style, sat=None):
    """The accent at hue h, set for the style: bright on dark, deep on light, muted for quiet styles; ≥ 3:1 contrast."""
    bg = rgb_of(bg_hex); dark = lum(bg) < 0.2
    s = sat if sat is not None else (0.45 if style in MUTED_STYLES else 0.72)
    if style in MUTED_STYLES: s = min(s, 0.55)
    best = None
    # on a light ground take the LIGHTEST tone that still reaches 3:1 (vivid, not muddy); on a dark ground a clear mid-light tone
    for L in ([0.62, 0.66, 0.58, 0.70, 0.54, 0.74] if dark else [0.50, 0.46, 0.42, 0.38, 0.34, 0.30, 0.26]):
        rgb = colorsys.hls_to_rgb((h % 360) / 360, L, s)
        if contrast(rgb, bg) >= 3.0: best = rgb; break
    return best or colorsys.hls_to_rgb((h % 360) / 360, 0.68 if dark else 0.3, s)


def choose(genre, style, logo=None, pictures=(), brand_hex=None):
    g = GENRE_COLOURS.get(genre, GENRE_COLOURS['software-saas'])
    bg_hex, style_accent = style_bg(style)
    why = []
    # what the pictures look like: the hue that fills most frames
    seen = []
    for p in list(pictures)[:12]: seen += hues_of(p)
    dom = max(seen, key=lambda x: x[1]) if seen else None
    if dom and dom[1] < 0.08: dom = None   # the pictures are mostly neutral (UI greys, white): no hue to answer
    brand = hues_of(logo, vivid=True, top=1) if logo else []
    if brand_hex and re.fullmatch(r'#?[0-9a-fA-F]{6}', brand_hex.strip()):   # the user's own brand colour beats any guess
        hl = colorsys.rgb_to_hls(*rgb_of(brand_hex.strip()))
        brand = [(round(hl[0] * 360), 1.0, hl[2], hl[1])]
    avoid = lambda h: next((r for lo, hi, r in g['avoid'] if (hue_dist(h, lo) + hue_dist(h, hi) <= hue_dist(lo, hi) + 1)), None)
    if brand:
        h = brand[0][0]
        acc = tune(h, bg_hex, style, sat=min(0.85, max(0.4, brand[0][2])))
        why.append(f'the brand colour ({"brief" if brand_hex else "logo"}, {name_of(h)} {h}°) is the accent — brand consistency comes first')
        if avoid(h): why.append(f'note: {avoid(h)}; keep it small and let the pictures carry warmth')
    else:
        def score(h):
            sc = 3 - g['hues'].index(h) * 0.6                                   # the genre's first hue is its strongest feeling
            if dom:
                d = hue_dist(h, dom[0])
                if d <= 40: sc += 1.5                                           # echoes the pictures
                elif 150 <= d <= 210: sc += 1.5 if g['energy'] == 'lively' else 0.6   # pops against them
                elif 60 <= d <= 120: sc -= 2                                    # the clashing band
            return sc
        cands = [h for h in g['hues'] if not avoid(h)]
        h = max(cands, key=score)
        acc = tune(h, bg_hex, style)
        why.append(f'{genre}: {g["feel"]} → {name_of(h)} ({h}°)')
        if dom:
            d = hue_dist(h, dom[0])
            rel = 'echoes' if d <= 40 else 'stands out against' if 150 <= d <= 210 else 'sits beside'
            why.append(f'it {rel} the pictures\' dominant {name_of(dom[0])} ({dom[0]}°, {dom[1]:.0%} of the pixels)')
        else:
            why.append('the pictures are mostly neutral, so the accent is the only colour voice')
    if g['avoid']: why.append('avoided: ' + '; '.join(r for _, _, r in g['avoid']))
    h1 = colorsys.rgb_to_hls(*acc)[0] * 360
    # the second accent is another colour of the genre's own feeling, placed by harmony: analogous (20–70°) for calm
    # products, split-complementary (120–180°) for lively ones; a blind ±30° only when the genre offers none
    band = (20, 70) if g['energy'] == 'calm' else (120, 180)
    pool = [h for h in g['hues'] if not avoid(h) and band[0] <= hue_dist(h, h1) <= band[1]]
    if pool: h2, how = pool[0], ('analogous' if g['energy'] == 'calm' else 'split-complementary') + ', from the genre\'s palette'
    else:
        h2 = h1 + (30 if g['energy'] == 'calm' else 150)
        if avoid(h2 % 360): h2 = h1 - 30
        how = 'analogous' if g['energy'] == 'calm' else 'split-complementary'
    acc2 = tune(h2, bg_hex, style, sat=0.5 if g['energy'] == 'calm' else 0.65)
    why.append(f'second accent {name_of(h2 % 360)} ({how}); background and ink stay the style\'s (60-30-10)')
    c = contrast(acc, rgb_of(bg_hex))
    why.append(f'contrast with the background {c:.1f}:1 (≥ 3:1)')
    hue = h1 % 360
    temp = 'warm' if (hue <= 70 or hue >= 330) else 'cool' if 160 <= hue <= 290 else 'neutral'
    return {'accent': hexc(acc), 'accent2': hexc(acc2), 'why': '; '.join(why), 'style_accent': style_accent, 'temperature': temp}


# grades by temperature (templates/cinema.js LUTs): the colorist keeps the look's temperature in line with the palette
WARM_GRADES, COOL_GRADES = {'warm-print', 'noir-gold', 'sunlit', 'pastel-glow'}, {'teal-night', 'neon-night', 'bleach-print'}


def grade_for(temp, style_grade, style):
    """A grade whose temperature agrees with the palette, or None to keep the style's."""
    if temp == 'warm' and style_grade in COOL_GRADES: return 'noir-gold' if style == 'luxe-noir' else 'sunlit'
    if temp == 'cool' and style_grade in WARM_GRADES: return 'clean-bright'
    return None


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('materials'); ap.add_argument('--genre', required=True); ap.add_argument('--style', required=True); ap.add_argument('--logo')
    a = ap.parse_args()
    pics = sorted(p for p in Path(a.materials).rglob('*') if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp') and 'logo' not in p.stem.lower())
    print(json.dumps(choose(a.genre, a.style, a.logo, pics), ensure_ascii=False, indent=1))
