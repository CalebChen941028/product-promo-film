"""Sound design, synthesised: whooshes, impacts, risers, shimmers, ticks — no samples, no downloads, no licences.

Commercials are half sound design: a whoosh sells a camera move, a sub-impact sells a reveal, a riser builds the
last chorus. Every sound here is generated from noise and sine waves with a fixed seed, so it is reproducible
and royalty-free.

Usage:
  python sfx.py cues.json out.wav --duration 66.5 [--gain-db 0]
  python sfx.py --demo out.wav            # every sound once, 1.5 s apart (for a listening check)

cues.json: [{"t": 12.43, "kind": "whoosh", "gain_db": 0}, ...]
  kinds: whoosh whip swell paper (cuts) · impact thud (hits) · riser (ends AT t, "len" s) ·
         shimmer chime (logo) · tick pop type (small items)
A whoosh/whip/swell/paper PEAKS at t (centred on the cut); every other sound STARTS at t.
"""
import argparse
import json
import wave

import numpy as np

SR = 48000
rng = np.random.default_rng(11)
# Peak levels before the mix. Kept low on purpose: sound design should be felt under the music, not heard over it.
PEAK_DB = {'impact': -9, 'thud': -14, 'whoosh': -18, 'whip': -16, 'swell': -21, 'paper': -21, 'riser': -17,
           'shimmer': -21, 'chime': -19, 'tick': -27, 'pop': -21, 'type': -26}


def env_exp(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))


def svf(x, fc, q=0.7, mode='bp'):
    """State-variable filter with a per-sample cutoff array (Chamberlin)."""
    fc = np.broadcast_to(np.asarray(fc, dtype=float), x.shape)
    f = 2 * np.sin(np.pi * np.clip(fc, 20, SR / 6) / SR)
    lo = bp = 0.0; out = np.empty_like(x); d = 1 / q
    for i in range(len(x)):
        hi = x[i] - lo - d * bp; bp += f[i] * hi; lo += f[i] * bp
        out[i] = bp if mode == 'bp' else (lo if mode == 'lp' else hi)
    return out


def norm(x, db):
    return x / (np.abs(x).max() + 1e-9) * 10 ** (db / 20)


def pan(mono, p0, p1):
    p = np.linspace(p0, p1, len(mono))            # -1 left … +1 right, equal-power
    return np.stack([mono * np.cos((p + 1) * np.pi / 4), mono * np.sin((p + 1) * np.pi / 4)], 1)


def whoosh(len_s=0.8, f0=250, f1=3200, peak=0.62, bright=1.0):
    n = int(len_s * SR); u = np.linspace(0, 1, n)
    e = np.where(u < peak, (u / peak) ** 2.2, np.exp(-(u - peak) / (1 - peak) * 4))
    fc = np.where(u < peak, f0 + (f1 - f0) * (u / peak) ** 1.5, f1 - (f1 - f0 * 2) * ((u - peak) / (1 - peak)))
    x = svf(rng.standard_normal(n), fc * bright, q=1.2) * e
    return pan(x, -0.7, 0.7), int(peak * n)


def impact(size=1.0):
    n = int(2.2 * SR); t = np.arange(n) / SR
    f = 38 + 30 * np.exp(-t * 9)                   # sub that drops in pitch
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 0.55 * size)
    body = svf(rng.standard_normal(n), 180, q=0.8, mode='lp') * env_exp(n, 0.12 * size) * 1.8
    click = svf(rng.standard_normal(n), 3500, q=0.7, mode='lp') * env_exp(n, 0.006) * 1.2
    tail = svf(rng.standard_normal(n), 900, q=0.6, mode='lp') * env_exp(n, 0.7) * 0.12 * np.clip(t / 0.05, 0, 1)
    x = sub * 1.0 + body + click + tail
    return pan(x, 0, 0), 0


def thud():
    n = int(0.6 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * np.cumsum(70 + 40 * np.exp(-t * 25)) / SR) * env_exp(n, 0.12) + svf(rng.standard_normal(n), 2500, mode='lp') * env_exp(n, 0.008)
    return pan(x, 0, 0), 0


def riser(len_s=3.0):
    n = int(len_s * SR); u = np.linspace(0, 1, n)
    f = 180 * (8 ** u)
    tone = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.15 + np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR) * 0.2
    air = svf(rng.standard_normal(n), 400 + 6000 * u ** 2, q=0.9) * 1.2
    x = (tone + air) * u ** 2.5
    x[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
    return pan(x, -0.3, 0.3), n                     # ends exactly at the cue time


def shimmer():
    n = int(3.0 * SR); t = np.arange(n) / SR
    x = np.zeros(n)
    for k, f in enumerate([2093, 2637, 3136, 4186, 5274, 6272]):
        x += np.sin(2 * np.pi * f * t + k) * (1 + 0.6 * np.sin(2 * np.pi * (5 + k) * t)) * env_exp(n, 0.5 + k * 0.15) / (1 + k * 0.3)
    x *= np.clip(t / 0.03, 0, 1)
    x += svf(rng.standard_normal(n), 7000, q=1.5) * env_exp(n, 0.4) * 0.3
    return pan(x, -0.4, 0.4), 0


def chime():
    n = int(3.2 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for r, a, tau in [(1, 1, 1.6), (2.76, 0.45, 0.8), (5.4, 0.25, 0.4), (8.93, 0.12, 0.25)]:
        x += np.sin(2 * np.pi * 880 * r * t) * a * env_exp(n, tau)
    return pan(x * np.clip(t / 0.004, 0, 1), 0, 0), 0


def tick():
    n = int(0.05 * SR); t = np.arange(n) / SR
    x = svf(rng.standard_normal(n), 5000, q=1.5) * env_exp(n, 0.004) + np.sin(2 * np.pi * 3200 * t) * env_exp(n, 0.006) * 0.6
    return pan(x, 0, 0), 0


def pop():
    n = int(0.12 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * np.cumsum(260 + 520 * np.exp(-t * 60)) / SR) * env_exp(n, 0.03) * np.clip(t / 0.002, 0, 1)
    return pan(x, 0, 0), 0


def paper():
    n = int(0.3 * SR); u = np.linspace(0, 1, n)
    x = svf(rng.standard_normal(n), 2500 + 3000 * u, q=0.8, mode='hp') * np.where(u < 0.5, u / 0.5, np.exp(-(u - 0.5) * 9))
    return pan(x, 0.4, -0.4), n // 2


def typing():
    n = int(0.16 * SR); x = np.zeros(n)
    for k in (0, int(0.07 * SR)):
        m = int(0.02 * SR); x[k:k + m] += svf(rng.standard_normal(m), 3800, q=2) * env_exp(m, 0.003)
    return pan(x, 0, 0), 0


SYNTH = {'whoosh': lambda c: whoosh(c.get('len', 0.8)), 'whip': lambda c: whoosh(c.get('len', 0.4), 600, 5200, 0.55, 1.0),
         'swell': lambda c: whoosh(c.get('len', 1.4), 150, 1400, 0.6, 0.6), 'paper': lambda c: paper(),
         'impact': lambda c: impact(c.get('size', 1.0)), 'thud': lambda c: thud(), 'riser': lambda c: riser(c.get('len', 3.0)),
         'shimmer': lambda c: shimmer(), 'chime': lambda c: chime(), 'tick': lambda c: tick(), 'pop': lambda c: pop(), 'type': lambda c: typing()}


def render(cues, duration, gain_db=0.0):
    n = int(duration * SR); bus = np.zeros((n, 2)); cache = {}
    for c in cues:
        key = (c['kind'], c.get('len'), c.get('size'))
        if key not in cache:
            x, anchor = SYNTH[c['kind']](c)
            cache[key] = (norm(x, PEAK_DB[c['kind']]), anchor)
        x, anchor = cache[key]
        x = x * 10 ** ((c.get('gain_db', 0) + gain_db) / 20)
        i0 = int(round(c['t'] * SR)) - anchor
        a, b = max(0, i0), min(n, i0 + len(x))
        if b > a: bus[a:b] += x[a - i0:b - i0]
    return bus


def write(path, x):
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.clip(x * 32767, -32768, 32767).astype(np.int16).tobytes())


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cues', nargs='?'); ap.add_argument('out', nargs='?')
    ap.add_argument('--duration', type=float); ap.add_argument('--gain-db', type=float, default=0.0)
    ap.add_argument('--demo')
    a = ap.parse_args()
    if a.demo:
        kinds = list(SYNTH)
        write(a.demo, render([{'t': 1 + i * 1.5 + (2.8 if k == 'riser' else 0), 'kind': k} for i, k in enumerate(kinds)], len(kinds) * 1.5 + 5))
        print('demo', a.demo, kinds)
    else:
        cues = json.load(open(a.cues))
        write(a.out, render(cues, a.duration, a.gain_db))
        print(f'sfx {len(cues)} cues → {a.out}')
