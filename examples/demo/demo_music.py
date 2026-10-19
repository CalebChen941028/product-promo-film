"""Original demo track for the skill's example film (120 BPM, D minor, ~66 s). Released to the public domain (CC0).
Usage: python demo_music.py out.wav   (numpy only).  Structure in bars (2 s each): intro 0–8 · build 8–16 · chorus 16–26 · outro 26–33."""
import sys, wave
import numpy as np
SR, BPM = 48000, 120.0
BEAT = 60 / BPM; BAR = 4 * BEAT; G = 0.5
DUR = G + 33 * BAR
N = int(DUR * SR); L = np.zeros(N); R = np.zeros(N); rng = np.random.default_rng(3)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def add(sig, t0, g=1.0, pan=0.0):
    i = int(t0 * SR); sig = sig[: max(0, N - i)]
    L[i:i + len(sig)] += sig * g * np.sqrt(0.5 * (1 - pan)); R[i:i + len(sig)] += sig * g * np.sqrt(0.5 * (1 + pan))
def saw(f, n, harm=8, bright=3.0):
    t = np.arange(n) / SR; return sum(np.sin(2 * np.pi * f * k * t) / k * np.exp(-k / bright) for k in range(1, harm + 1))
def env(n, a, r):
    t = np.arange(n) / SR; return np.clip(t / a, 0, 1) * np.clip((n / SR - t) / r, 0, 1)
def pad(t0, d, notes, g):
    n = int((d + 1) * SR); add(sum(saw(hz(m), n) + saw(hz(m) * 1.004, n) for m in notes) * env(n, 0.5, 1.0) / len(notes), t0, g)
def pluck(t0, m, g):
    n = int(0.6 * SR); t = np.arange(n) / SR
    add((np.sin(2 * np.pi * hz(m) * t) + 0.4 * np.sin(4 * np.pi * hz(m) * t) * np.exp(-t / 0.08)) * np.exp(-t / 0.2), t0, g, 0.3 * np.sin(t0 * 3))
def kick(t0, g):
    n = int(0.45 * SR); t = np.arange(n) / SR; f = 45 + 90 * np.exp(-t / 0.04); add(np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.2)), t0, g)
def hat(t0, g):
    n = int(0.08 * SR); s = np.diff(rng.standard_normal(n + 1)); add(s * np.exp(-np.arange(n) / SR / 0.02) * 0.4, t0, g, 0.3)
def clap(t0, g):
    n = int(0.25 * SR); add(np.diff(rng.standard_normal(n + 1)) * np.exp(-np.arange(n) / SR / 0.07) * 0.5, t0, g)
def bass(t0, m, d, g):
    n = int(d * SR); t = np.arange(n) / SR; add(np.tanh(1.5 * (np.sin(2 * np.pi * hz(m) * t) + 0.3 * np.sin(4 * np.pi * hz(m) * t))) * env(n, 0.005, 0.05), t0, g)
CH = [([50, 57, 62, 65, 69], 38, [62, 65, 69, 74]), ([46, 53, 58, 62, 65], 34, [58, 62, 65, 70]), ([41, 53, 57, 60, 65], 41, [60, 65, 69, 72]), ([48, 55, 60, 64, 67], 36, [60, 64, 67, 72])]
for b in range(33):
    t0 = G + b * BAR; padn, root, arp = CH[(b // 2) % 4]
    sec = 'intro' if b < 8 else 'build' if b < 16 else 'chorus' if b < 26 else 'outro'
    pad(t0, BAR, padn, 0.05 if sec != 'chorus' else 0.06)
    if sec != 'outro' or b < 29:
        for k in range(16 if sec != 'intro' else 8):
            pluck(t0 + k * BEAT / (4 if sec != 'intro' else 2), arp[[0, 1, 2, 3, 2, 1, 2, 3][k % 8]], 0.05 if sec == 'intro' else 0.06)
    if sec in ('build', 'chorus'):
        for k in range(4):
            if sec == 'chorus' or k % 2 == 0: kick(t0 + k * BEAT, 0.5)
            if sec == 'chorus' and k % 2: clap(t0 + k * BEAT, 0.25)
            hat(t0 + k * BEAT + BEAT / 2, 0.04)
        for k in range(8): bass(t0 + k * BEAT / 2, root, BEAT / 2 * 0.9, 0.18 if sec == 'chorus' else 0.12)
t = np.arange(N) / SR; fade = np.clip((DUR - t) / 4, 0, 1) * np.clip(t / 0.8, 0, 1)
L *= fade; R *= fade; pk = max(abs(L).max(), abs(R).max()); L, R = np.tanh(L / pk * 1.2) * 0.89, np.tanh(R / pk * 1.2) * 0.89
o = np.empty(2 * N, dtype=np.int16); o[0::2] = (L * 32767).astype(np.int16); o[1::2] = (R * 32767).astype(np.int16)
with wave.open(sys.argv[1], 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(o.tobytes())
print('wrote', sys.argv[1], round(DUR, 1), 's')
