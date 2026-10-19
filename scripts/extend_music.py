"""Lengthen a track seamlessly by repeating a span that starts and ends on bar lines (typically a chorus).

Usage:
  python extend_music.py in.wav out.wav --grid 0.4876 --bar 2.0 --repeat-from-bar 56 --repeat-to-bar 72 [--times 1]

The audio plays to the end of bar `repeat-to-bar`, jumps back to bar `repeat-from-bar` (the span is
heard again), then continues from `repeat-to-bar` to the original ending. A 12 ms equal-power crossfade
hides the splice. Pick a span whose last bar flows naturally into its first bar (e.g. chorus end →
chorus start, both downbeats with a strong low hit). Convert MP3 to WAV first:
  ffmpeg -i song.mp3 -ar 48000 song.wav
Check afterwards: the sample-to-sample jump at the seam should be no larger than normal (print below).
"""
import argparse
import wave

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('dst')
ap.add_argument('--grid', type=float, required=True, help='first beat offset G (s)')
ap.add_argument('--bar', type=float, required=True, help='bar length (s)')
ap.add_argument('--repeat-from-bar', type=int, required=True)
ap.add_argument('--repeat-to-bar', type=int, required=True)
ap.add_argument('--times', type=int, default=1)
a = ap.parse_args()

with wave.open(a.src) as w:
    sr, ch = w.getframerate(), w.getnchannels()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, ch).astype(np.float64)
cut = int(round((a.grid + a.repeat_to_bar * a.bar) * sr))
back = int(round((a.grid + a.repeat_from_bar * a.bar) * sr))
xf = int(0.012 * sr)
ramp = np.linspace(0, np.pi / 2, xf)[:, None]
out = x[:cut + xf].copy()
for k in range(a.times):
    seg = x[back:].copy() if k == a.times - 1 else x[back:cut + xf].copy()
    out[-xf:] = out[-xf:] * np.cos(ramp) + seg[:xf] * np.sin(ramp)
    out = np.concatenate([out, seg[xf:]])
seam = cut
d = np.abs(np.diff(out[:, 0]))
print(f'seam jump {d[seam - 2000:seam + 2000].max():.0f} vs typical p99.9 {np.percentile(d, 99.9):.0f}')
with wave.open(a.dst, 'wb') as w:
    w.setnchannels(ch); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(np.clip(out, -32768, 32767).astype(np.int16).tobytes())
print('duration', round(len(out) / sr, 2), 's')
