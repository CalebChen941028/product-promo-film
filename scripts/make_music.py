"""Original underscore music, composed to the film's structure. Used when the user brings no track.

Not a song: a tasteful, restrained bed in the style of a commercial underscore (pads, piano or plucks, bass,
light drums), arranged bar by bar from the film's energy plan so sections change exactly on scene cuts.
It has one hero hit with a half-beat of silence before it, and a ring-out ending. Pure numpy (additive
synthesis, FFT-filtered percussion, FFT convolution reverb), seeded and reproducible, royalty-free.

Usage:
  python make_music.py --plan plan.json --out music.wav --grid grid.json
  python make_music.py --mood warm-piano --bars 40 --bpm 88 --out demo.wav --grid grid.json    # quick listen
  python make_music.py --list

plan.json = {"mood": "cinematic-pulse", "bpm": 104, "energy": [0,0,0,1,1,1,2,2,...], "hero_bar": 28, "seed": 3}
  energy per bar: 0 = intro/outro (pads), 1 = verse (pads + rhythm instrument + bass), 2 = chorus (+ drums),
  3 = peak (+ top line, bigger drums). The last bars of the film should be 0 (the end card rings out).
grid.json has the same shape as beat_grid.py output (bpm, first_beat, bar_seconds, bars[…hi…]).
"""
import argparse
import json
import wave

import numpy as np

SR = 48000
G0 = 0.1      # first downbeat (s)

# mood → key (MIDI root), chord progression (semitones from key, quality), instruments, groove, reverb
MOODS = {
    'cinematic-pulse': dict(key=57, prog=[(0, 'madd9'), (8, 'Madd9'), (3, 'M'), (10, 'M')], bpm=104, lead='piano',
                            rhythm='ostinato', drums='cinematic', pad_bright=0.55, rt=2.6, desc='minor, pulsing ostinato, low toms — tech, hardware, industrial'),
    'minimal-electronic': dict(key=62, prog=[(0, 'm7'), (10, 'M'), (8, 'Mmaj7'), (10, 'M')], bpm=120, lead='bell',
                               rhythm='arp16', drums='four', pad_bright=0.5, rt=1.9, sidechain=True, desc='clean plucked 16ths, four-on-the-floor — dev tools, data, fintech, events'),
    'warm-piano': dict(key=60, prog=[(0, 'Madd9'), (7, 'M'), (9, 'm7'), (5, 'Mmaj7')], bpm=88, lead='bell',
                       rhythm='piano', drums='soft', pad_bright=0.35, rt=2.5, desc='piano and strings, gentle — care, education, mission'),
    'bright-pop': dict(key=67, prog=[(0, 'M'), (7, 'M'), (9, 'm'), (5, 'Madd9')], bpm=118, lead='glock',
                       rhythm='offbeat', drums='pop', pad_bright=0.6, rt=1.6, desc='bright plucks on the offbeat, claps — consumer apps, kids'),
    'luxe-lounge': dict(key=62, prog=[(0, 'm9'), (5, 'dom9'), (0, 'm9'), (10, 'maj9')], bpm=90, lead='bell',
                        rhythm='epiano', drums='brush', pad_bright=0.3, rt=2.2, desc='electric piano, deep bass, brushed groove — fashion, beauty, luxury'),
    'ambient-air': dict(key=63, prog=[(0, 'Madd9'), (7, 'M'), (9, 'm7'), (5, 'Madd9')], bpm=86, lead='bell',
                        rhythm='bells', drums='none', pad_bright=0.45, rt=3.4, desc='airy pads and bells, almost no drums — travel, living, wellness'),
    'warm-acoustic': dict(key=55, prog=[(0, 'M'), (9, 'm7'), (5, 'Madd9'), (7, 'M')], bpm=98, lead='glock',
                          rhythm='strum', drums='folk', pad_bright=0.35, rt=1.8, desc='strummed plucks, shaker, warm bass — food, lifestyle, handmade'),
}
CHORD = {'M': [0, 4, 7], 'm': [0, 3, 7], 'M7': [0, 4, 7, 11], 'Mmaj7': [0, 4, 7, 11], 'maj9': [0, 4, 7, 11, 14], 'm7': [0, 3, 7, 10],
         'm9': [0, 3, 7, 10, 14], 'dom9': [0, 4, 10, 14], 'Madd9': [0, 4, 7, 14], 'madd9': [0, 3, 7, 14]}
mtof = lambda m: 440.0 * 2 ** ((m - 69) / 12)


class Mix:
    def __init__(self, n):
        self.n = n; self.bus = {k: np.zeros((n, 2)) for k in ('pad', 'keys', 'bass', 'drums', 'lead', 'fx')}

    def add(self, bus, t, x, gain=1.0, pan=0.0):
        i0 = int(round(t * SR))
        if i0 >= self.n or len(x) == 0: return
        if i0 < 0: x = x[-i0:]; i0 = 0
        x = x[: self.n - i0] * gain
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        self.bus[bus][i0:i0 + len(x), 0] += x * l * 1.414; self.bus[bus][i0:i0 + len(x), 1] += x * r * 1.414


def env(n, a=0.005, r=0.05, sus=1.0):
    e = np.full(n, sus); na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    e[:na] = np.linspace(0, sus, na); e[-nr:] *= np.linspace(1, 0, nr)
    return e


def tone(f, dur, partials, rel=0.3, a=0.004, rng=None):
    """Additive voice: partials = [(ratio, amp, decay_tau or None)]."""
    n = int((dur + rel) * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for ratio, amp, tau in partials:
        fr = f * ratio
        if fr > SR / 2.4: continue
        ph = rng.uniform(0, 2 * np.pi) if rng is not None else 0
        x += amp * np.sin(2 * np.pi * fr * t + ph) * (np.exp(-t / tau) if tau else 1)
    return x * env(n, a, rel)


def piano(f, dur, vel=0.8, rng=None):
    B = 0.0004; p = [(n * np.sqrt(1 + B * n * n), (1 / n ** 1.25) * (0.6 if n > 1 else 1), max(0.08, 2.4 / (1 + 0.45 * n) * (220 / max(f, 110)) ** 0.35)) for n in range(1, 11)]
    return tone(f, min(dur, 3.5), p, rel=0.35, a=0.003, rng=rng) * vel


def pluck(f, dur, bright=1.0, rng=None):
    p = [(n, 1 / n ** (1.1 / bright), 0.45 / n ** 0.7) for n in range(1, 13)]
    return tone(f, min(dur, 1.6), p, rel=0.12, a=0.002, rng=rng)


def bell(f, dur, rng=None):
    p = [(1, 1, 1.6), (2.0, 0.35, 0.9), (3.01, 0.22, 0.6), (4.16, 0.14, 0.4), (5.43, 0.08, 0.3)]
    return tone(f, min(dur, 2.8), p, rel=0.6, a=0.002, rng=rng)


def glock(f, dur, rng=None):
    return tone(f, 1.2, [(1, 1, 0.8), (2.76, 0.4, 0.3), (5.4, 0.2, 0.12)], rel=0.3, a=0.001, rng=rng)


def epiano(f, dur, vel=0.8):
    n = int((min(dur, 3.0) + 0.4) * SR); t = np.arange(n) / SR
    idx = 1.4 * np.exp(-t / 0.35) + 0.25
    x = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t)) * np.exp(-t / 2.2)
    x += 0.12 * np.sin(2 * np.pi * f * 14.0 * t) * np.exp(-t / 0.05)       # tine
    return x * env(n, 0.003, 0.4) * vel


def pad(freqs, dur, bright=0.5, rng=None):
    n = int((dur + 1.2) * SR); t = np.arange(n) / SR; x = np.zeros(n)
    cut = 600 + 2600 * bright
    for f in freqs:
        for det in (-0.06, 0.06):
            fd = f * 2 ** (det / 12)
            for k in range(1, 24):
                if fd * k > cut: break
                x += np.sin(2 * np.pi * fd * k * t + rng.uniform(0, 6.28)) / k * np.exp(-(fd * k / cut) ** 2)
    lfo = 1 + 0.06 * np.sin(2 * np.pi * 0.23 * t + rng.uniform(0, 6.28))
    return x * lfo * env(n, 0.45, 1.2) / max(1, len(freqs))


def bass(f, dur, sub=False):
    n = int((dur + 0.08) * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + (0 if sub else 0.28 * np.sin(4 * np.pi * f * t) + 0.08 * np.sin(6 * np.pi * f * t))
    return np.tanh(1.3 * x) * env(n, 0.01 if not sub else 0.08, 0.08)


def noise_filtered(n, lo, hi, rng):
    X = np.fft.rfft(rng.standard_normal(n)); fr = np.fft.rfftfreq(n, 1 / SR)
    X *= ((fr >= lo) & (fr <= hi)) * 1.0
    return np.fft.irfft(X, n)


def drum(kind, rng):
    if kind == 'kick':
        n = int(0.45 * SR); t = np.arange(n) / SR
        f = 45 + 110 * np.exp(-t / 0.035)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.16) + 0.25 * noise_filtered(n, 1000, 5000, rng) * np.exp(-t / 0.004)
    if kind == 'tom':
        n = int(0.9 * SR); t = np.arange(n) / SR
        f = 62 + 50 * np.exp(-t / 0.06)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.32) + 0.2 * noise_filtered(n, 200, 1200, rng) * np.exp(-t / 0.05)
    if kind in ('snare', 'rim'):
        n = int(0.3 * SR); t = np.arange(n) / SR
        body = np.sin(2 * np.pi * (190 if kind == 'snare' else 420) * t) * np.exp(-t / (0.06 if kind == 'snare' else 0.02))
        nz = noise_filtered(n, 1500, 9000, rng) * np.exp(-t / (0.12 if kind == 'snare' else 0.015))
        return body * 0.6 + nz
    if kind == 'clap':
        n = int(0.35 * SR); t = np.arange(n) / SR; x = np.zeros(n); base = noise_filtered(n, 900, 6000, rng)
        for d in (0, 0.011, 0.022):
            i = int(d * SR); x[i:] += base[: n - i] * np.exp(-np.arange(n - i) / SR / 0.012)
        return x + base * np.exp(-t / 0.09) * 0.6
    if kind == 'hat':
        n = int(0.08 * SR); t = np.arange(n) / SR
        return noise_filtered(n, 7000, 16000, rng) * np.exp(-t / 0.018)
    if kind == 'ohat':
        n = int(0.35 * SR); t = np.arange(n) / SR
        return noise_filtered(n, 6500, 16000, rng) * np.exp(-t / 0.11)
    if kind == 'shaker':
        n = int(0.12 * SR); t = np.arange(n) / SR
        return noise_filtered(n, 5000, 11000, rng) * np.minimum(t / 0.025, 1) * np.exp(-t / 0.04)
    if kind == 'crash':
        n = int(2.4 * SR); t = np.arange(n) / SR
        return noise_filtered(n, 4000, 15000, rng) * np.exp(-t / 0.9)
    if kind == 'swell':                                     # reverse cymbal into a section
        n = int(1.2 * SR); t = np.arange(n) / SR
        return (noise_filtered(n, 3000, 14000, rng) * np.exp(-t / 0.5))[::-1]
    raise ValueError(kind)


def reverb(x, rt, rng, pre=0.02):
    n = int(rt * 1.2 * SR); t = np.arange(n) / SR
    ir = np.zeros((n, 2))
    for ch in range(2):
        bands = [(0, 600, rt * 1.1), (600, 3000, rt), (3000, 9000, rt * 0.6), (9000, 20000, rt * 0.35)]
        for lo, hi, r in bands:
            ir[:, ch] += noise_filtered(n, lo, hi, rng) * np.exp(-6.9 * t / r)
    ir[: int(pre * SR)] = 0; ir /= np.sqrt((ir ** 2).sum(axis=0) + 1e-9)
    m = len(x) + n; N = 1 << (m - 1).bit_length()
    out = np.stack([np.fft.irfft(np.fft.rfft(x[:, c], N) * np.fft.rfft(ir[:, c], N), N)[:len(x)] for c in range(2)], 1)
    return out


def compose(mood, bpm, energy, hero_bar=None, seed=3):
    M = MOODS[mood]; rng = np.random.default_rng(seed)
    beat = 60 / bpm; BAR = 4 * beat; nb = len(energy)
    dur = G0 + nb * BAR + 4.0
    mix = Mix(int(dur * SR))
    key = M['key']
    hits = {k: drum(k, rng) for k in ('kick', 'tom', 'snare', 'rim', 'clap', 'hat', 'ohat', 'shaker', 'crash', 'swell')}
    T = lambda b, beat_i=0: G0 + b * BAR + beat_i * beat
    prev_e = -1
    for b in range(nb):
        e = energy[b]; root, q = M['prog'][b % len(M['prog'])]
        tones = [key + root + i for i in CHORD[q]]
        bass_note = key - 24 + root
        last = b == nb - 1 or (b + 1 < nb and energy[b + 1] == 0 and e == 0 and b > nb - 4)
        hold = BAR * (2.5 if b == nb - 1 else 1)
        # pads: always, brighter with energy
        vo = [tones[0] - 12] + [t if t < key + 12 else t - 12 for t in tones[1:]]
        mix.add('pad', T(b), pad([mtof(m) for m in vo], hold, M['pad_bright'] * (0.6 + 0.2 * e), rng), 0.16 + 0.03 * e)
        if e >= 1 or b == nb - 1:
            mix.add('bass', T(b), bass(mtof(bass_note), hold * (1 if e < 2 else 0.95), sub=e < 2), 0.22)
        # rhythm instrument
        r = M['rhythm']
        if e >= 1:
            if r == 'ostinato':
                for k in range(8):
                    m = [bass_note + 24, bass_note + 31, bass_note + 24, bass_note + 36][k % 4]
                    mix.add('keys', T(b, k * 0.5), pluck(mtof(m), beat * 0.45, 0.7 + 0.15 * e, rng), 0.10 + 0.03 * e, pan=-0.3 if k % 2 else 0.3)
            elif r == 'arp16':
                seq = sorted(tones) + sorted(tones)[1:-1][::-1]
                for k in range(16 if e >= 2 else 8):
                    step = 0.25 if e >= 2 else 0.5
                    m = seq[k % len(seq)] + (12 if (k // len(seq)) % 2 and e >= 3 else 0)
                    mix.add('keys', T(b, k * step), pluck(mtof(m), beat * step, 0.9, rng), 0.085, pan=np.sin(k) * 0.4)
            elif r == 'piano':
                mix.add('keys', T(b), piano(mtof(bass_note + 12), BAR, 0.55, rng), 0.2, pan=-0.15)
                mix.add('keys', T(b, 2), piano(mtof(bass_note + 19), BAR / 2, 0.45, rng), 0.18, pan=-0.15)
                arp = sorted(tones)
                for k in range(8 if e >= 2 else 4):
                    step = 0.5 if e >= 2 else 1.0
                    mix.add('keys', T(b, k * step), piano(mtof(arp[k % len(arp)] + 12 * (k % 2 == 1 and e >= 2)), beat * 1.5, 0.42, rng), 0.16, pan=0.2)
            elif r == 'offbeat':
                for k in range(4):
                    for m in tones[:3]:
                        mix.add('keys', T(b, k + 0.5), pluck(mtof(m + 12), beat * 0.4, 1.2, rng), 0.06, pan=0.25)
            elif r == 'epiano':
                for at, ln in ((0, 1.5), (1.5, 2.5)):
                    for m in tones:
                        mix.add('keys', T(b, at), epiano(mtof(m), beat * ln, 0.5), 0.07, pan=-0.2)
            elif r == 'bells':
                for k in range(4 if e >= 2 else 2):
                    m = sorted(tones)[[0, 2, 1, 3][k % 4] % len(tones)] + 12
                    mix.add('keys', T(b, k * (1 if e >= 2 else 2)), bell(mtof(m), beat * 2, rng), 0.07, pan=[-0.4, 0.4][k % 2])
            elif r == 'strum':
                pat = [0, 1, 1.5, 2.5, 3, 3.5] if e >= 2 else [0, 2]
                for k, at in enumerate(pat):
                    up = (at % 1) != 0
                    strings = sorted(tones + [tones[0] + 12])
                    for j, m in enumerate(strings[::-1] if up else strings):
                        mix.add('keys', T(b, at) + j * 0.012, pluck(mtof(m), beat * 0.9, 0.8, rng), 0.05 * (0.7 if up else 1), pan=-0.1 + j * 0.05)
        # top line in the peak
        if e >= 3:
            line = sorted(tones)[-3:] + [sorted(tones)[-2]]
            inst = {'bell': bell, 'glock': glock, 'piano': lambda f, d, rng=None: piano(f, d, 0.5, rng)}[M['lead']]
            for k, at in enumerate([0, 1.5, 2.5, 3]):
                mix.add('lead', T(b, at), inst(mtof(line[k % len(line)] + 12), beat * 1.2, rng=rng), 0.07, pan=0.3)
        # drums
        d = M['drums']
        if e >= 2 and d != 'none':
            for k in range(4):
                if d == 'four' or (d in ('pop', 'folk', 'soft', 'cinematic') and k in (0, 2)) or (d == 'brush' and k == 0):
                    mix.add('drums', T(b, k), hits['kick'], 0.55 if d != 'soft' else 0.35)
                if d in ('pop', 'four') and k in (1, 3): mix.add('drums', T(b, k), hits['clap'], 0.22)
                if d == 'folk' and k in (1, 3): mix.add('drums', T(b, k), hits['rim'], 0.18)
                if d == 'brush':
                    if k in (1, 3): mix.add('drums', T(b, k), hits['rim'], 0.12)
                    if k == 1: mix.add('drums', T(b, k + 0.5), hits['kick'], 0.3)
                if d == 'cinematic' and e >= 3 and k == 3: mix.add('drums', T(b, k), hits['tom'], 0.5)
            for k in range(8):
                if d == 'four':
                    if k % 2 == 1: mix.add('drums', T(b, k * 0.5), hits['ohat'], 0.05, pan=0.2)
                    elif e >= 3: mix.add('drums', T(b, k * 0.5 + 0.25), hits['hat'], 0.03, pan=-0.2)
                elif d in ('pop', 'cinematic'): mix.add('drums', T(b, k * 0.5), hits['hat'], 0.05 + 0.02 * (k % 2 == 0), pan=0.25)
                elif d in ('folk', 'soft', 'brush'): mix.add('drums', T(b, k * 0.5), hits['shaker'], 0.07, pan=0.3)
        elif e == 1 and d in ('folk', 'soft', 'brush'):
            for k in range(8): mix.add('drums', T(b, k * 0.5), hits['shaker'], 0.04, pan=0.3)
        # section transitions: swell into a higher section, crash on its downbeat
        if b > 0 and e > prev_e and e >= 2:
            mix.add('fx', T(b) - len(hits['swell']) / SR, hits['swell'], 0.06)
            mix.add('fx', T(b), hits['crash'], 0.05 if b != hero_bar else 0.09)
        prev_e = e
    # hero: half a beat of silence before the downbeat, then a full hit
    if hero_bar is not None and 0 < hero_bar < nb:
        th = T(hero_bar); i0, i1 = int((th - beat * 0.5) * SR), int(th * SR)
        for k in mix.bus:
            ramp = np.ones(i1 - i0); ramp[:int(0.03 * SR)] = np.linspace(1, 0, int(0.03 * SR)); ramp[int(0.03 * SR):] = 0
            mix.bus[k][i0:i1] *= ramp[:, None]
        mix.add('drums', th, hits['kick'], 0.8); mix.add('drums', th, hits['tom'], 0.6); mix.add('fx', th, hits['crash'], 0.1)
        mix.add('bass', th, bass(mtof(key - 24 + M['prog'][hero_bar % len(M['prog'])][0]), BAR, sub=True), 0.3)
    # buses → reverb → master
    rt = M['rt']; send = {'pad': 0.35, 'keys': 0.3, 'lead': 0.45, 'bass': 0.0, 'drums': 0.08, 'fx': 0.25}
    dry = sum(mix.bus.values())
    wet = reverb(sum(mix.bus[k] * s for k, s in send.items()), rt, rng)
    out = dry + wet * 0.55
    if M.get('sidechain'):
        pump = np.ones(len(out))
        for b in range(nb):
            if energy[b] >= 2:
                for k in range(4):
                    i = int(T(b, k) * SR); m = min(len(out) - i, int(beat * SR))
                    if m > 0: pump[i:i + m] = np.minimum(pump[i:i + m], 1 - 0.35 * np.exp(-np.arange(m) / SR / (beat * 0.35)))
        out *= pump[:, None]
    # gentle bus compression + soft clip, fade the tail
    win = int(0.05 * SR); p = np.sqrt(np.convolve((out ** 2).mean(axis=1), np.ones(win) / win, mode='same')) + 1e-9
    thr = np.percentile(p, 90) * 0.8; g = np.where(p > thr, (thr / p) ** 0.4, 1.0)
    out *= g[:, None]
    out = np.tanh(out / (np.abs(out).max() + 1e-9) * 1.4) / np.tanh(1.4)
    tail = int(3.0 * SR); out[-tail:] *= np.linspace(1, 0, tail)[:, None] ** 2
    out *= 10 ** (-1 / 20) / (np.abs(out).max() + 1e-9)
    grid = {'bpm': bpm, 'first_beat': G0, 'bar_seconds': BAR, 'generated': mood,
            'bars': [{'bar': b, 't': round(T(b), 3), 'lo': round(0.3 + 0.15 * energy[b], 3), 'mid': round(0.3 + 0.15 * energy[b], 3), 'hi': round(0.15 + 0.25 * energy[b], 3)} for b in range(nb)],
            'changes': [b for b in range(1, nb) if energy[b] != energy[b - 1]]}
    return out, grid


def write(path, x):
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.clip(x * 32767, -32768, 32767).astype(np.int16).tobytes())


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--plan'); ap.add_argument('--mood'); ap.add_argument('--bpm', type=float); ap.add_argument('--bars', type=int)
    ap.add_argument('--out'); ap.add_argument('--grid'); ap.add_argument('--seed', type=int, default=3); ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
    if a.list or not (a.plan or a.mood):
        for k, m in MOODS.items(): print(f"{k:20s} {m['bpm']:4d} BPM  {m['desc']}")
        raise SystemExit
    if a.plan:
        p = json.load(open(a.plan)); mood, bpm, energy, hero, seed = p['mood'], p.get('bpm') or MOODS[p['mood']]['bpm'], p['energy'], p.get('hero_bar'), p.get('seed', a.seed)
    else:
        nb = a.bars or 32; mood = a.mood; bpm = a.bpm or MOODS[mood]['bpm']
        energy = ([0] * 2 + [1] * 6 + [2] * 8 + [1] * 4 + [3] * 8 + [0] * 4)[:nb]; energy += [0] * (nb - len(energy)); hero = 20 if nb > 24 else None; seed = a.seed
    if mood not in MOODS: raise SystemExit(f'ERROR mood {mood!r} unknown — use one of {list(MOODS)}')
    x, grid = compose(mood, float(bpm), energy, hero, seed)
    write(a.out, x)
    if a.grid: json.dump(grid, open(a.grid, 'w'), indent=1)
    print(f'music {mood} {bpm:.0f} BPM · {len(energy)} bars · {len(x) / SR:.1f} s → {a.out}')
