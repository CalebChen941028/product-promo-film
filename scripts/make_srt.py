"""SRT files from the voice-over timing (same text as the burned-in captions).

Usage: python make_srt.py vo_dir/vo_timing.json out_dir/ <basename> [--skip tagline,motto]
Writes <basename>.bilingual.srt, .zh.srt, .en.srt. --skip leaves out lines that are typeset on screen
instead of captioned (keep it in sync with ONSCREEN in config.js), or keep them for accessibility.
"""
import argparse
import json
import os

ap = argparse.ArgumentParser()
ap.add_argument('timing'); ap.add_argument('out_dir'); ap.add_argument('base')
ap.add_argument('--skip', default='')
a = ap.parse_args()
skip = set(filter(None, a.skip.split(',')))
items = [c for c in json.load(open(a.timing)) if c['id'] not in skip]


def ts(s):
    ms = round(s * 1000)
    return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'


os.makedirs(a.out_dir, exist_ok=True)
for name, f in [('bilingual', lambda c: f"{c['zh']}\n{c['en']}"), ('zh', lambda c: c['zh']), ('en', lambda c: c['en'])]:
    with open(os.path.join(a.out_dir, f'{a.base}.{name}.srt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(f"{i + 1}\n{ts(c['s'])} --> {ts(c['e'] + 0.3)}\n{f(c)}\n" for i, c in enumerate(items)))
print(len(items), 'captions')
