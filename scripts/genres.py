"""Product genre classifier: what kind of product is this, so what look, motion, music and story fit it?

Usage:
  python genres.py --brief brief.json [--manifest build/manifest.json] [--text "extra words"] [--docs materials/]
  python genres.py --list

Scores every genre in templates/genres.json:
  text      keyword hits in the brief, the docs (README, *.md, *.txt) and file names (×1 each, Chinese and English)
  materials what the folder contains (desktop UI, phone UI, product cut-outs, photos, clips, figures) × the genre's signal weights
Prints the top 3 with reasons and the film.json lines to use. The agent confirms with the user when the top two are close.
"""
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
GENRES = json.load(open(HERE.parent / 'templates' / 'genres.json'))
TEXT_EXT = {'.md', '.txt', '.json', '.html'}
GENERIC = set(GENRES.get('generic', []))


def read_docs(folder, limit=60000):
    out = []
    if not folder:
        return ''
    for p in sorted(Path(folder).rglob('*')):
        if p.name.endswith('.regions.json'): continue   # capture_app's panel maps: screen geometry, not the product's docs
        if p.is_file() and p.suffix.lower() in TEXT_EXT and p.stat().st_size < 400000 and 'node_modules' not in p.parts:
            try:
                out.append(p.read_text(errors='ignore')[:20000])
            except Exception:
                pass
        if p.is_file():
            out.append(p.stem.replace('_', ' ').replace('-', ' '))
        if sum(map(len, out)) > limit:
            break
    return '\n'.join(out)


def material_counts(manifest):
    c = {}
    for it in (manifest or {}).get('items', []):
        role = it.get('role') if it['kind'] == 'image' else it['kind']
        c[role] = c.get(role, 0) + 1
    c['ui'] = c.get('desktop', 0) + c.get('phone', 0)
    return c


def classify(text='', manifest=None):
    text = (text or '').lower()
    mats = material_counts(manifest)
    rows = []
    for gid, g in GENRES['genres'].items():
        hits = [k for k in g['keywords'] if re.search(r'(?<![a-z])' + re.escape(k.lower()) + r'(?:s|es)?(?![a-z])' if k.isascii() else re.escape(k), text)]
        s_text = sum(0.5 if k.lower() in GENERIC else 1.0 for k in hits)
        s_mat = sum(w * min(mats.get(role, 0), 4) / 4 for role, w in g.get('signals', {}).items())
        rows.append({'genre': gid, 'score': round(s_text * 1.0 + s_mat, 2), 'hits': hits[:8], 'mat': round(s_mat, 2), **{k: g[k] for k in ('style', 'motion', 'music', 'arc', 'voice', 'tone', 'zh', 'en')}})
    rows.sort(key=lambda r: -r['score'])
    return rows, mats


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--brief'); ap.add_argument('--manifest'); ap.add_argument('--docs'); ap.add_argument('--text', default='')
    ap.add_argument('--list', action='store_true'); ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    if a.list:
        for gid, g in GENRES['genres'].items():
            print(f"{gid:28s} {g['en']:44s} {g['style'][0]:15s} {g['motion']:15s} {g['music']['mood']:18s} {g['arc']}")
        raise SystemExit
    text = a.text
    if a.brief and Path(a.brief).exists():
        b = json.load(open(a.brief)); b = {k: v for k, v in b.items() if k not in ('contacts', 'voice', 'music', 'style', '_how')}
        text += ' ' + json.dumps(b, ensure_ascii=False)
    text += ' ' + read_docs(a.docs)
    manifest = json.load(open(a.manifest)) if a.manifest and Path(a.manifest).exists() else None
    rows, mats = classify(text, manifest)
    if a.json:
        print(json.dumps({'ranked': rows[:3], 'materials': mats}, ensure_ascii=False, indent=1)); raise SystemExit
    print('materials:', ', '.join(f'{k} {v}' for k, v in sorted(mats.items())) or 'none')
    for i, r in enumerate(rows[:3]):
        print(f"{i + 1}. {r['genre']:26s} score {r['score']:5.2f}  ({r['en']} · {r['zh']})")
        print(f"   style {r['style'][0]} (or {', '.join(r['style'][1:])}) · motion {r['motion']} · music {r['music']['mood']} {r['music']['bpm']} BPM · arc {r['arc']}")
        print(f"   because: {', '.join(r['hits']) or '—'}{' · materials ' + str(r['mat']) if r['mat'] else ''}")
    best = rows[0]
    if rows[0]['score'] == 0:
        print('\nNO SIGNAL — nothing in the docs or materials points to a genre. Ask the user what the product is (or pass --genre).')
    elif len(rows) > 1 and rows[0]['score'] - rows[1]['score'] < 1.0:
        print(f"\nCLOSE CALL between {rows[0]['genre']} and {rows[1]['genre']} — ask the user which describes the product.")
    print('\nfilm.json:\n  "genre": "%s",\n  "style": "%s",\n  "motion": "%s",\n  "music": {"generate": {"mood": "%s", "bpm": %d}}   (or {"file": "<the user\'s track>"})'
          % (best['genre'], best['style'][0], best['motion'], best['music']['mood'], best['music']['bpm']))
