"""Pick the best moment of a clip for a scene: sharp, steadily moving, well exposed — never a shaky, blurred or black stretch.

Usage: python3 footage.py <clip> --seconds 4.5 [--ffmpeg PATH]   → prints {"offset": s, "score": 0–1, "notes": [...]}
autofilm.py calls best() for every footage beat and writes "offset" into the scene; check the note when the score is low.

How: 4 frames a second at 320 px. Per frame: sharpness (variance of a Laplacian), exposure, and motion (mean change from
the frame before). A window of the scene's length scores well when it is sharp, exposed, and moves — but not too much
(a whip or a shake reads as an accident in a calm film). Glitchy AI-generated stretches (sudden sharpness collapses,
flicker) score low by the same measures.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

FPS = 4


def frames(clip, ffmpeg):
    import numpy as np
    from PIL import Image
    with tempfile.TemporaryDirectory() as d:
        subprocess.run([ffmpeg, '-v', 'error', '-i', str(clip), '-vf', f'fps={FPS},scale=320:-2', str(Path(d) / '%05d.png')], check=True)
        return [np.asarray(Image.open(p).convert('L')).astype(float) for p in sorted(Path(d).glob('*.png'))]


def best(clip, seconds, ffmpeg='ffmpeg'):
    import numpy as np
    fs = frames(clip, ffmpeg)
    if not fs: return {'offset': 0.0, 'score': 0.0, 'notes': ['no frames could be read']}
    lap = lambda g: float(np.var(g[1:-1, 1:-1] * 4 - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]))
    sharp = np.array([lap(g) for g in fs])
    expo = np.array([1.0 - min(1.0, abs(g.mean() - 120) / 110) for g in fs])            # 0 = black or blown out
    motion = np.array([0.0] + [float(np.abs(fs[k] - fs[k - 1]).mean()) for k in range(1, len(fs))])
    s_n = sharp / (np.percentile(sharp, 90) + 1e-9)
    # motion: some is life, a lot is a shake or a whip; the band is relative to this clip
    lo, hi = np.percentile(motion, 30), np.percentile(motion, 85) + 1e-9
    m_ok = np.clip(1 - np.maximum(0, motion - hi) / (hi + 1e-9), 0, 1) * (0.7 + 0.3 * np.clip(motion / (lo + 1e-9), 0, 1))
    per = np.clip(s_n, 0, 1.2) * 0.5 + expo * 0.25 + m_ok * 0.25
    n = max(1, int(round(seconds * FPS)))
    if len(per) <= n:
        return {'offset': 0.0, 'score': round(float(per.mean()), 2), 'notes': [f'the clip ({len(fs) / FPS:.1f} s) is not longer than the scene ({seconds:.1f} s): it plays from the start']}
    win = np.convolve(per, np.ones(n) / n, mode='valid')
    # a window that contains a collapse (a frame far blurrier than its neighbours) is a glitch, not a moment
    collapse = np.array([s_n[k:k + n].min() < 0.25 * np.median(s_n[k:k + n]) for k in range(len(win))])
    win = win - collapse * 0.3
    k = int(np.argmax(win))
    notes = []
    if collapse.all(): notes.append('every stretch has a blur or flicker collapse — look at the clip; it may be glitchy (AI-generated?)')
    if win[k] < 0.45: notes.append('even the best stretch is soft, dark or shaky — consider leaving the clip out')
    return {'offset': round(k / FPS, 2), 'score': round(float(win[k]), 2), 'notes': notes}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('clip'); ap.add_argument('--seconds', type=float, default=4.0); ap.add_argument('--ffmpeg', default='ffmpeg')
    a = ap.parse_args()
    print(json.dumps(best(a.clip, a.seconds, a.ffmpeg), ensure_ascii=False))
