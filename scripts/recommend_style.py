"""Recommend a look + motion language from what the product IS (genre) and, if given, the music's tempo.

Usage: python recommend_style.py brief.json [--grid grid.json] [--manifest build/manifest.json] [--docs materials/] [--text "…"]
Thin wrapper over genres.py (templates/genres.json, 15 product genres → style, motion, music, arc).
Music: ≥ 128 BPM or very punchy favours kinetic-launch / playful-pop; ≤ 95 BPM favours gentle-story / precision-data.
Prints the top 3 and the lines to paste into film.json. Confirm with the user when the top two are close.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import genres as G  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('brief'); ap.add_argument('--grid'); ap.add_argument('--manifest'); ap.add_argument('--docs'); ap.add_argument('--text', default='')
a = ap.parse_args()
b = json.load(open(a.brief)) if Path(a.brief).exists() else {}
b = {k: v for k, v in b.items() if k not in ('contacts', 'voice', 'music', 'style', '_how')}
text = json.dumps(b, ensure_ascii=False) + ' ' + a.text + ' ' + G.read_docs(a.docs)
man = json.load(open(a.manifest)) if a.manifest and Path(a.manifest).exists() else None
rows, mats = G.classify(text, man)
note = ''
if a.grid:
    g = json.load(open(a.grid)); bpm = g.get('bpm', 110)
    hi = [x['hi'] for x in g.get('bars', [])]; punch = (max(hi) - sorted(hi)[len(hi) // 2]) if hi else 0
    fast, slow = bpm >= 128 or punch > 0.45, bpm <= 95
    for r in rows:
        if fast and r['motion'] in ('kinetic-launch', 'playful-pop'): r['score'] += 1.5
        if slow and r['motion'] in ('gentle-story', 'precision-data'): r['score'] += 1.5
    rows.sort(key=lambda r: -r['score'])
    note = f'music {bpm:.0f} BPM' + (' (fast/punchy)' if fast else ' (calm)' if slow else ' (mid-tempo)')
print('Recommended (confirm with the user):' + (f'  [{note}]' if note else ''))
for i, r in enumerate(rows[:3]):
    print(f"{i + 1}. {r['genre']:26s} → style {r['style'][0]:14s} motion {r['motion']:15s} score {r['score']:.1f}  because: {', '.join(r['hits'][:6]) or 'materials'}")
best = rows[0]
print('\nPaste into film.json:\n  "genre": "%s",\n  "style": "%s",\n  "motion": "%s",' % (best['genre'], best['style'][0], best['motion']))
print('Alternatives for the same genre:', ', '.join(best['style'][1:]))
