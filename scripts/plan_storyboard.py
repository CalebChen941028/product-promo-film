"""Draft a storyboard from the music's structure and the brief: which scene goes on which bars.

Usage: python plan_storyboard.py grid.json brief.json --out storyboard.md [--narration narration.skeleton.json]

Heuristic (edit the result — it is a starting point, not a final cut):
  1. Split the bars into sections at the strongest spectral changes (beat_grid.py "changes"), snapped to
     2-bar phrases; label each section low / mid / high by its mean high-band energy (tertiles).
  2. Fixed beats of the story: cover (bars 0–3) → pain (3–7) → reveal (7–10) → features → differentiators
     (2 bars per row) → finale (8 bars) → end card (last 6 bars, through the outro).
  3. Feature slots are equal spans between reveal and the comparison, filled in the brief's (narrative) order.
     A feature whose "energy" (low/mid/high) is two steps away from its slot's music is flagged ⚠ — reorder
     the brief or move that beat. Too many features for the music → DROP rows: extend the music or merge.
  4. Every scene starts on a bar line; narration lines start ~0.15–0.3 bar after their scene starts.
"""
import argparse
import json

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('grid'); ap.add_argument('brief')
ap.add_argument('--out', default='storyboard.md'); ap.add_argument('--narration')
a = ap.parse_args()
g = json.load(open(a.grid)); brief = json.load(open(a.brief))
bars = g['bars']; N = len(bars); bar_s = g['bar_seconds']; G = g['first_beat']
hi = np.array([b['hi'] for b in bars])

# sections: cut at strong changes, snapped to even bars; long sections are split into 8-bar phrases
cuts = sorted({0, N} | {int(round(c['bar'] / 2) * 2) for c in g['changes']})
raw = []
for s, e in zip(cuts[:-1], cuts[1:]):
    if raw and e - raw[-1][0] < 4: raw[-1] = (raw[-1][0], e)
    elif e > s: raw.append((s, e))
secs = []
for s, e in raw:
    while e - s > 12: secs.append((s, s + 8)); s += 8
    secs.append((s, e))
q1, q2 = np.quantile(hi, [1 / 3, 2 / 3])
label = lambda s, e: 'high' if hi[s:e].mean() >= q2 else ('low' if hi[s:e].mean() <= q1 else 'mid')
secs = [(s, e, label(s, e)) for s, e in secs]
rank = {'low': 0, 'mid': 1, 'high': 2}

plan = []  # (start_bar, end_bar, scene, note)
plan.append((0, 3, 'cover', 'logo · name · positioning · platform chips'))
plan.append((3, 7, 'pain', brief.get('pain', {}).get('en', 'the problem, shown as scattered tools')))
plan.append((7, 10, 'reveal', 'hero window — the product in one shot'))
end_len = 6 if N >= 60 else 4
end_start = N - end_len
finale_start = end_start - 8
diffs = brief.get('differentiators', [])
cmp_start = finale_start - (2 * len(diffs) + 2 if diffs else 0)
feats = list(brief.get('features', []))
# feature slots: split bars 10..cmp_start into len(feats) slots on even bars, then match energy wants to slot energy
n = max(1, len(feats))
edges = [10 + round((cmp_start - 10) * k / n / 2) * 2 for k in range(n + 1)]
slots = [(edges[k], edges[k + 1]) for k in range(n) if edges[k + 1] > edges[k]]
slots[-1] = (slots[-1][0], cmp_start) if slots else slots
slot_energy = [hi[s:e].mean() for s, e in slots]
want = lambda f: rank.get(f.get('energy', 'mid'), 1)
for k, (s, e) in enumerate(slots):           # narrative order wins; energy mismatches are flagged, not reordered
    if k >= len(feats): break
    f = feats[k]
    lab = 'high' if slot_energy[k] >= q2 else ('low' if slot_energy[k] <= q1 else 'mid')
    flag = '  ⚠ energy mismatch — reorder features or move this beat' if abs(rank[lab] - want(f)) >= 2 else ''
    plan.append((s, e, f"feature:{f['id']}", f"{f['en']}  [music {lab}; wants {f.get('energy', 'mid')}]{flag}  materials: {', '.join(f.get('materials', []))}"))
for f in feats[len(slots):]:
    plan.append((cmp_start, cmp_start, 'DROP', f"{f['id']} — no room; extend the music or merge features"))
if diffs: plan.append((cmp_start, finale_start, 'compare', f'{len(diffs)} rows, one every 2 bars'))
plan.append((finale_start, end_start, 'finale', 'wall of real screens + tagline'))
plan.append((end_start, N, 'endcard', 'logo · name · motto · contacts · chips (hold through the outro)'))
plan.sort(key=lambda r: r[0])

with open(a.out, 'w') as fh:
    fh.write(f"# Storyboard draft\n\nBPM {g['bpm']} · bar {bar_s} s · G {G} s · {N} bars ({g['duration']} s)\n\n")
    fh.write('## Music sections\n\n| bars | time | energy |\n| --- | --- | --- |\n')
    for s, e, l in secs: fh.write(f'| {s}–{e} | {G + s * bar_s:.1f}–{G + e * bar_s:.1f} s | {l} |\n')
    fh.write('\n## Scenes\n\n| bars | time | scene | note |\n| --- | --- | --- | --- |\n')
    for s, e, name, note in plan: fh.write(f'| {s}–{e} | {G + s * bar_s:.1f} s | {name} | {note} |\n')
print(open(a.out).read())
if a.narration:
    lines = []
    for s, e, name, note in plan:
        if name in ('cover', 'DROP'): continue
        lines.append({'id': name.replace('feature:', ''), 'bar': s + 0.3, 'end_bar': e, 'en': 'TODO — one spoken sentence', 'zh': 'TODO'})
    json.dump(lines, open(a.narration, 'w'), ensure_ascii=False, indent=1)
    print('narration skeleton →', a.narration)
