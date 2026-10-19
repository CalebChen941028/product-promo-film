"""Environment check: everything the pipeline needs, each missing piece with the exact command to fix it.

Usage: python doctor.py            (run from anywhere; exits 1 if something required is missing)
"""
import importlib
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
ok, bad = [], []


def need(cond, label, fix, required=True):
    (ok if cond else bad).append((label, fix, required))


need(sys.version_info >= (3, 9), f'python ≥ 3.9 (have {platform.python_version()})', 'install Python 3.10+')
for mod, pipname in [('numpy', 'numpy'), ('PIL', 'pillow')]:
    try:
        importlib.import_module(mod); need(True, f'python module {pipname}', '')
    except ImportError:
        need(False, f'python module {pipname}', f'{sys.executable} -m pip install {pipname}')
ff = shutil.which('ffmpeg') or os.environ.get('FFMPEG')
if not ff:
    try:
        import imageio_ffmpeg; ff = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass
need(bool(ff), f'ffmpeg ({ff or "missing"})', f'{sys.executable} -m pip install imageio-ffmpeg   (or brew/apt/winget install ffmpeg)')
if ff:
    enc = subprocess.run([ff, '-hide_banner', '-encoders'], capture_output=True, text=True).stdout
    need('libx264' in enc, 'ffmpeg has libx264', 'use a full ffmpeg build (imageio-ffmpeg has it)')
    need('libvpx' in enc, 'ffmpeg has libvpx (WebM clips)', 'use a full ffmpeg build (imageio-ffmpeg has it)', required=False)
node = shutil.which('node')
need(bool(node), 'node ≥ 18', 'install Node.js 18+ (https://nodejs.org)')
pw = None
for c in [os.environ.get('PLAYWRIGHT_NODE_MODULES'), SKILL / 'node_modules', Path.cwd() / 'node_modules']:
    if c and (Path(c) / 'playwright').exists():
        pw = c; break
need(bool(pw), f'playwright ({pw or "missing"})', f'cd "{SKILL}" && npm i playwright && npx playwright install chromium')
# CJK fonts (Linux servers often have none → Chinese renders as boxes)
if platform.system() == 'Linux':
    fc = subprocess.run(['fc-list', ':lang=zh'], capture_output=True, text=True).stdout if shutil.which('fc-list') else ''
    need(bool(fc.strip()), 'CJK font installed', 'sudo apt install fonts-noto-cjk   (Chinese text needs it)')
kp = next((c for c in [os.environ.get('KOKORO_PYTHON'), '~/.venvs/kokoro/bin/python'] if c and Path(os.path.expanduser(c)).exists()), None)
need(bool(kp), f'Kokoro TTS python ({kp or "KOKORO_PYTHON or ~/.venvs/kokoro"})', 'optional — ask the user before installing (references/audio.md "Kokoro setup"); or use "voice": {"engine": "none"|"files"}', required=False)
if kp:
    sys.path.insert(0, str(SKILL / 'scripts'))
    try:
        from make_film import kokoro_cached
        model, voices = kokoro_cached()
        need(model, 'Kokoro model downloaded', 'it downloads on first use (≈ 330 MB): ask the user first', required=False)
        need(bool(voices), f'Kokoro voices downloaded ({", ".join(voices) or "none"})', 'each voice is ≈ 0.5 MB: ask the user first; use a downloaded one when you cannot ask', required=False)
    except Exception:
        pass
need(Path(os.path.expanduser('~/.cache/kes/phontab')).exists(), 'espeak-ng data at ~/.cache/kes', 'optional — cp -R <tts-venv>/lib/python3.*/site-packages/espeakng_loader/espeak-ng-data ~/.cache/kes', required=False)

for label, _, _ in ok:
    print('  ok  ', label)
for label, fix, req in bad:
    print('  MISS' if req else '  opt ', label, '\n        FIX:', fix)
sys.exit(1 if any(r for _, _, r in bad) else 0)
