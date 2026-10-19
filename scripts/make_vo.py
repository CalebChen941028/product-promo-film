"""Voice-over with Kokoro (Apache-2.0, commercial use OK): one WAV per narration line + timing for captions.

Usage:
  KOKORO_ESPEAK_DATA=~/.cache/kes HF_HUB_DISABLE_XET=1 \
  python make_vo.py --narration narration.json --out vo/ --js vo_timing.js --grid 0.4876 --bar 2.0 \
                    [--voice am_michael] [--lang a] [--max-speed 1.12]

narration.json: [{"id", "bar", "end_bar", "en", "zh", "cap"?}, ...] in time order.
  bar / end_bar  = where the line may start / should end, in bars of the music (fractions allowed).
  en             = what is SPOKEN (write numbers as words if the voice should say them).
  cap            = optional caption text when it should differ from what is spoken (e.g. "300 or 600 DPI").
  zh             = the Chinese caption line.
Each line may run until the next line starts (or end_bar + 0.8 s). Lines that don't fit are sped up to
--max-speed; anything still too long is printed as OVER — shorten the sentence rather than speeding more.
Voices: am_michael (deep US male), af_heart (warm US female), bf_emma (British female), am_fenrir, bm_george …
Lang codes: a = American English, b = British English, z = Mandarin, j = Japanese (see Kokoro docs).
"""
import argparse
import json
import os
from pathlib import Path

import numpy as np
import soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument('--narration', required=True)
ap.add_argument('--out', required=True)
ap.add_argument('--js', required=True)
ap.add_argument('--grid', type=float, required=True)
ap.add_argument('--bar', type=float, required=True)
ap.add_argument('--voice', default='am_michael')
ap.add_argument('--lang', default='a')
ap.add_argument('--max-speed', type=float, default=1.12)
a = ap.parse_args()

# espeak-ng (used by Kokoro for unknown words) silently ignores data paths longer than its buffer, and
# phonemizer resolves symlinks — so point it at a SHORT REAL COPY of espeakng_loader's espeak-ng-data.
import misaki.espeak  # noqa: E402,F401
from phonemizer.backend.espeak.wrapper import EspeakWrapper  # noqa: E402
if os.environ.get('KOKORO_ESPEAK_DATA'):
    EspeakWrapper.set_data_path(os.path.expanduser(os.environ['KOKORO_ESPEAK_DATA']))
from kokoro import KPipeline  # noqa: E402

SR = 24000
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
lines = json.loads(Path(a.narration).read_text())
pipe = KPipeline(lang_code=a.lang)


def trim(x):
    idx = np.where(np.abs(x) > 0.01)[0]
    return x[max(0, idx[0] - 240): idx[-1] + 2400]


timing = []
for i, ln in enumerate(lines):
    start = a.grid + a.bar * ln['bar']
    nxt = a.grid + a.bar * lines[i + 1]['bar'] if i + 1 < len(lines) else a.grid + a.bar * ln['end_bar']
    window = min(nxt, a.grid + a.bar * ln['end_bar'] + 0.8) - start - 0.25
    speed = 1.0
    for _ in range(5):
        audio = trim(np.concatenate([np.asarray(x) for _, _, x in pipe(ln['en'], voice=a.voice, speed=speed)]))
        dur = len(audio) / SR
        if dur <= window or speed >= a.max_speed:
            break
        speed = min(a.max_speed, speed * dur / window + 0.005)
    sf.write(out / f"{ln['id']}.wav", audio, SR)
    timing.append({'id': ln['id'], 's': round(start, 3), 'e': round(start + dur, 3), 'zh': ln.get('zh', ''), 'en': ln.get('cap', ln['en']), 'speed': round(speed, 3), 'fits': dur <= window})
    print(f"{ln['id']:10s} start {start:7.2f} dur {dur:5.2f} window {window:5.2f} speed {speed:.2f}{'' if dur <= window else '  OVER'}")
Path(a.js).write_text('const VO = ' + json.dumps(timing, ensure_ascii=False, indent=1) + ';\nif (typeof window !== "undefined") window.VO = VO;\n')
json.dump(timing, open(out / 'vo_timing.json', 'w'), ensure_ascii=False, indent=1)
