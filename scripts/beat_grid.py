"""Music analysis for beat-synced editing: tempo, first-beat offset, per-bar energy, section changes.

Usage:
  python beat_grid.py song.mp3 --ffmpeg /path/to/ffmpeg [--bpm-min 70 --bpm-max 180] [--out grid.json]

Output (stdout + optional JSON):
  bpm, first_beat (G, seconds), bar_seconds (4 beats), and per bar: start time, low/mid/high energy,
  plus "changes" = bars where the spectrum shifts strongly (candidate section boundaries).
Scene cuts belong on bar starts: t = G + b * bar_seconds. Choruses = runs of high 'hi' energy;
intros/breaks = low 'hi'. Look for phrases of 8 bars; repeated phrases (same pattern 32/64 s apart)
are where a seamless extension can be spliced (see extend_music.py).
"""
import argparse
import json
import subprocess
import sys

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('audio')
ap.add_argument('--ffmpeg', default='ffmpeg')
ap.add_argument('--bpm-min', type=float, default=70)
ap.add_argument('--bpm-max', type=float, default=180)
ap.add_argument('--out')
a = ap.parse_args()

SR, HOP, WIN = 22050, 256, 2048
raw = subprocess.run([a.ffmpeg, '-v', 'error', '-i', a.audio, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768
n = len(x) // HOP
frames = np.lib.stride_tricks.sliding_window_view(np.pad(x, (0, WIN)), WIN)[::HOP][:n] * np.hanning(WIN)
X = np.abs(np.fft.rfft(frames, axis=1))
L = np.log1p(X * 10)
onset = np.r_[0, np.maximum(0, np.diff(L, axis=0)).sum(1)]
onset = np.maximum(onset - np.convolve(onset, np.ones(32) / 32, 'same'), 0)
fps = SR / HOP

# coarse tempo by autocorrelation, then fine tempo + phase by onset alignment
ac = np.correlate(onset, onset, 'full')[len(onset) - 1:]
best = None
for bpm in np.arange(a.bpm_min, a.bpm_max, 0.25):
    lag = 60 / bpm * fps
    s = sum(np.interp(k * lag, np.arange(len(ac)), ac) for k in (1, 2, 4))
    if best is None or s > best[1]:
        best = (bpm, s)
coarse = best[0]
best = None
for bpm in np.arange(coarse - 0.5, coarse + 0.51, 0.01):
    per = 60 / bpm * fps
    for ph in np.arange(0, per, 0.5):
        idx = np.round(ph + np.arange(int((n - ph) / per)) * per).astype(int)
        s = onset[idx].sum()
        if best is None or s > best[0]:
            best = (s, bpm, ph / fps)
_, bpm, G = best
beat = 60 / bpm
bar = 4 * beat

bars = []
feats = []
b = 0
while G + (b + 1) * bar <= len(x) / SR:
    i0, i1 = int((G + b * bar) * fps), int((G + (b + 1) * bar) * fps)
    spec = X[i0:i1].mean(0)
    feats.append(np.log1p(spec[:400]))
    lo, mid, hi = np.log1p(spec[:12]).mean(), np.log1p(spec[12:150]).mean(), np.log1p(spec[150:]).mean()
    bars.append({'bar': b, 't': round(G + b * bar, 3), 'lo': round(float(lo), 3), 'mid': round(float(mid), 3), 'hi': round(float(hi), 3)})
    b += 1
feats = np.array(feats)
nov = [float(np.linalg.norm(feats[i] - feats[i - 1])) for i in range(1, len(feats))]
thr = np.percentile(nov, 85) if nov else 0
changes = [{'bar': i + 1, 't': round(G + (i + 1) * bar, 3), 'novelty': round(v, 2)} for i, v in enumerate(nov) if v > thr]

res = {'bpm': round(float(bpm), 2), 'first_beat': round(float(G), 4), 'beat_seconds': round(beat, 4), 'bar_seconds': round(bar, 4),
       'duration': round(len(x) / SR, 2), 'bars': bars, 'changes': changes}
print(f"BPM {res['bpm']}  first beat G={res['first_beat']} s  bar={res['bar_seconds']} s  duration={res['duration']} s", file=sys.stderr)
for r in bars:
    print(f"bar {r['bar']:3d}  t {r['t']:7.2f}  hi {r['hi']:5.2f} " + '#' * int(max(0, r['hi']) * 40), file=sys.stderr)
print('section changes at bars:', [c['bar'] for c in changes], file=sys.stderr)
if a.out:
    json.dump(res, open(a.out, 'w'), indent=1)
