"""Mix music + voice-over, duck the music under speech, fade out, soft-limit.

Usage: python mix_audio.py music_48k.wav vo_dir/ out.wav --duration 206 [--ffmpeg ffmpeg] [--duck 0.72] [--speech-rms 0.14]

Targets that worked: speech RMS ≈ -17 dBFS (0.14), music ducked ≈ 11 dB (gain 1 − 0.72) under speech,
→ speech sits ~ +10 dB over the music (median). Normalising VO by PEAK instead of RMS left speech at only
+1 dB — unintelligible. Final loudness is set at mux time: ffmpeg -af loudnorm=I=-14:TP=-1.0:LRA=11.
"""
import argparse
import json
import subprocess
import wave
from pathlib import Path

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('music'); ap.add_argument('vo_dir'); ap.add_argument('out')
ap.add_argument('--duration', type=float, required=True)
ap.add_argument('--ffmpeg', default='ffmpeg')
ap.add_argument('--duck', type=float, default=0.72)
ap.add_argument('--speech-rms', type=float, default=0.14)
ap.add_argument('--fade', type=float, default=2.5)
a = ap.parse_args()
SR = 48000


def read(path):
    with wave.open(str(path)) as w:
        ch = w.getnchannels()
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64).reshape(-1, ch) / 32768


music = read(a.music)
n = int(a.duration * SR)
if len(music) < n:
    music = np.vstack([music, np.zeros((n - len(music), music.shape[1]))])
music = music[:n]
if music.shape[1] == 1:
    music = np.repeat(music, 2, axis=1)
vo = np.zeros(n)
for item in json.loads((Path(a.vo_dir) / 'vo_timing.json').read_text()):
    src, tmp = Path(a.vo_dir) / f"{item['id']}.wav", Path(a.vo_dir) / f"{item['id']}_48k.wav"
    subprocess.run([a.ffmpeg, '-y', '-loglevel', 'error', '-i', str(src), '-ar', str(SR), '-ac', '1', str(tmp)], check=True)
    clip = read(tmp)[:, 0]
    clip = np.clip(clip / (np.sqrt(np.mean(clip ** 2)) + 1e-9) * a.speech_rms, -0.95, 0.95)
    i0 = int(item['s'] * SR); end = min(n, i0 + len(clip))
    vo[i0:end] += clip[: end - i0]

env = np.convolve(np.abs(vo), np.ones(int(0.03 * SR)) / int(0.03 * SR), mode='same')
active = env > 0.01
duck = np.empty(n); g = 0.0
att, rel = 64 / (0.08 * SR), 64 / (0.45 * SR)   # 80 ms attack, 450 ms release
for i in range(0, n, 64):
    g = min(1.0, g + att) if active[i] else max(0.0, g - rel)
    duck[i:i + 64] = g
mix = music * (1 - a.duck * duck)[:, None] * 0.82 + vo[:, None]
mix *= np.clip((a.duration - np.arange(n) / SR) / a.fade, 0, 1)[:, None]
peak = np.abs(mix).max()
if peak > 0.97:
    mix = np.tanh(mix / peak * 1.1) / np.tanh(1.1) * 0.97
with wave.open(a.out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(np.clip(mix * 32767, -32768, 32767).astype(np.int16).tobytes())
print('mixed', a.duration, 's; peak before limiting', round(float(peak), 3))
