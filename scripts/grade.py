"""Film finish: colour-grade LUTs (.cube) + an ffmpeg filter chain for LUT, bloom and film grain.

A colourist grades every commercial. Here each look is a small, documented colour transform written to a 33³
3D LUT and applied by ffmpeg (lut3d), blended with the original by `strength`, so UI text stays legible.

Usage:
  python grade.py --list
  python grade.py teal-night out.cube [--strength 0.6]
  python grade.py teal-night look.cube --preview in.png out.png [--bloom 0.2]   # grade one still (cover, checks)

Looks (default style in brackets):
  teal-night   [midnight-tech]  cool teal shadows, clean warm-neutral highlights, gentle S-curve
  clean-bright [keynote-light]  neutral, slightly warm whites, soft contrast: keynote / product page
  bleach-print [editorial-mono] bleach-bypass: lower saturation, punchy contrast, print-like blacks
  pastel-glow  [aurora-glass]   lifted blacks, violet shadows, peach highlights, juicy mid saturation
  neon-night   [neon-cyber]     crushed blacks, magenta shadows, cyan highlights, strong contrast
  warm-print   [paper-academic] warm paper, lifted blacks, low contrast, slightly muted colour
  noir-gold    [luxe-noir]      deep blacks, warm golden highlights, slightly muted colour
  sunlit       [natural-fresh]  warm daylight highlights, soft lifted shadows, a touch of green in the mids
  teal-orange  (any)            the blockbuster split-tone, used lightly
  none                          identity (grade off)
"""
import argparse
import subprocess

import numpy as np


def s_curve(x, k):
    return x + k * (x * x * (3 - 2 * x) - x)


def look(rgb, name):
    r = rgb.copy()
    L = (0.2126 * r[..., 0] + 0.7152 * r[..., 1] + 0.0722 * r[..., 2])[..., None]
    sh, hi = (1 - L) ** 2, L ** 2          # shadow / highlight weights

    def sat(x, s):
        l = (0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2])[..., None]
        return l + (x - l) * s

    if name == 'teal-night':
        r = s_curve(r, 0.22) + sh * np.array([-0.02, 0.025, 0.05]) + hi * np.array([0.025, 0.012, -0.012])
        r = sat(r, 1.05)
    elif name == 'clean-bright':
        r = s_curve(r, 0.12) + hi * np.array([0.012, 0.006, -0.006]); r = sat(r, 1.03)
    elif name == 'bleach-print':
        r = s_curve(r, 0.38); r = sat(r, 0.72); r = r * 0.98 + 0.005
    elif name == 'pastel-glow':
        r = r * 0.95 + 0.035 + sh * np.array([0.03, -0.005, 0.05]) + hi * np.array([0.03, 0.012, -0.01]); r = sat(r, 1.12)
    elif name == 'neon-night':
        r = np.clip((r - 0.025) / 0.975, 0, 1); r = s_curve(r, 0.3) + sh * np.array([0.035, -0.01, 0.055]) + hi * np.array([-0.02, 0.015, 0.03]); r = sat(r, 1.14)
    elif name == 'warm-print':
        r = r * 0.95 + 0.04; r = s_curve(r, 0.1) + np.array([0.022, 0.01, -0.022]); r = sat(r, 0.9)
    elif name == 'noir-gold':
        r = np.clip((r - 0.02) / 0.98, 0, 1); r = s_curve(r, 0.25) + sh * np.array([0.01, 0.005, -0.005]) + hi * np.array([0.035, 0.02, -0.015]); r = sat(r, 0.88)
    elif name == 'sunlit':
        r = r * 0.96 + 0.03; r = s_curve(r, 0.1) + hi * np.array([0.025, 0.015, -0.01]) + sh * np.array([0.0, 0.012, 0.0]); r = sat(r, 1.04)
    elif name == 'teal-orange':
        r = s_curve(r, 0.2) + sh * np.array([-0.03, 0.02, 0.05]) + hi * np.array([0.05, 0.02, -0.04]); r = sat(r, 1.04)
    elif name != 'none':
        raise SystemExit(f'unknown look {name!r}; see --list')
    return np.clip(r, 0, 1)


LOOKS = ['teal-night', 'clean-bright', 'bleach-print', 'pastel-glow', 'neon-night', 'warm-print', 'noir-gold', 'sunlit', 'teal-orange', 'none']


def write_cube(name, path, strength=0.6, n=33):
    g = np.linspace(0, 1, n)
    b, gg, rr = np.meshgrid(g, g, g, indexing='ij')          # .cube order: red fastest
    rgb = np.stack([rr, gg, b], -1).reshape(-1, 3)
    out = rgb + (look(rgb, name) - rgb) * float(strength)
    with open(path, 'w') as f:
        f.write(f'TITLE "{name} {strength}"\nLUT_3D_SIZE {n}\n')
        f.writelines(f'{x:.6f} {y:.6f} {z:.6f}\n' for x, y, z in out)
    return path


def vf_chain(cube, bloom=0.2, grain=0.3, still=False):
    """ffmpeg -filter_complex for: LUT → bloom (bright-pass, wide blur, screen) → grain (temporal, luma only)."""
    esc = str(cube).replace('\\', '/').replace(':', '\\:').replace("'", "\\'")
    parts = [f"[0:v]lut3d=file='{esc}':interp=tetrahedral,format=gbrp"]
    if bloom > 0:
        parts[-1] += ',split[a][b]'
        parts.append("[b]curves=all='0/0 0.8/0 1/1',gblur=sigma=40,gblur=sigma=14[g]")
        parts.append(f'[a][g]blend=all_mode=screen:all_opacity={min(0.45, bloom * 0.7):.3f},format=yuv444p')
    else:
        parts[-1] += ',format=yuv444p'
    if grain > 0 and not still:
        parts[-1] += f',noise=c0s={grain * 9:.1f}:c0f=t'
    parts[-1] += ',format=yuv420p' if not still else ',format=rgb24'
    return ';'.join(parts) + '[v]'


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('look', nargs='?'); ap.add_argument('out', nargs='?')
    ap.add_argument('--strength', type=float, default=0.6); ap.add_argument('--list', action='store_true')
    ap.add_argument('--preview', nargs=2, metavar=('IN', 'OUT')); ap.add_argument('--bloom', type=float, default=0.2)
    ap.add_argument('--ffmpeg', default='ffmpeg')
    a = ap.parse_args()
    if a.list or not a.look:
        print(__doc__); raise SystemExit
    write_cube(a.look, a.out, a.strength)
    if a.preview:
        subprocess.run([a.ffmpeg, '-y', '-loglevel', 'error', '-i', a.preview[0], '-filter_complex', vf_chain(a.out, a.bloom, 0, still=True), '-map', '[v]', a.preview[1]], check=True)
    print('wrote', a.out)
