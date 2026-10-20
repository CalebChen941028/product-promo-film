"""From a folder of materials to a drafted film — any product type, with or without music.

Usage:
  python autofilm.py <materials folder> [--out <project dir>] [--brief brief.json] [--genre id] [--style id] [--motion id]
                     [--music file|generate] [--seconds 90] [--voice kokoro|none] [--fill-copy]

What it does (all deterministic, nothing downloaded):
  1. intake      classify every file (UI / phone / photo / cut-out / figure / logo / clip / music / voice / docs), convert clips to WebM
  2. understand  read the docs + brief, classify the product genre (templates/genres.json), pick look, motion, music mood, story arc
  3. cast        assign each material to the beat of the arc that suits it (cover, reveal, features, range, proof, finale…)
  4. draft       write <project>/brief.json (if none), film.json and treatment.md, with TODO where a human-quality line is needed
Then the crew (references/crew.md) writes the treatment and every TODO, and make_film.py builds the film.
--fill-copy writes the brief's own words into the TODOs where it can (a quick first cut; the crew should still polish).
"""
import argparse
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(HERE))
import genres as G  # noqa: E402
import make_film as MF  # noqa: E402
import suggest_rects as SR  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('materials'); ap.add_argument('--out'); ap.add_argument('--brief'); ap.add_argument('--genre'); ap.add_argument('--style'); ap.add_argument('--motion')
ap.add_argument('--music', default='auto'); ap.add_argument('--seconds', type=float, default=0); ap.add_argument('--voice', default='auto'); ap.add_argument('--fill-copy', action='store_true')
a = ap.parse_args()
src = Path(a.materials).resolve()
if not src.is_dir(): sys.exit(f'ERROR {src} is not a folder.\n  FIX: pass the folder that holds the screenshots/photos/clips/logo/docs')
proj = Path(a.out).resolve() if a.out else src.parent / (src.name + '-film')
proj.mkdir(parents=True, exist_ok=True)
build = proj / 'build'
ff = MF.find_ffmpeg({}) or sys.exit('ERROR ffmpeg not found.\n  FIX: python3 -m pip install imageio-ffmpeg')
rel = lambda p: os.path.relpath(Path(p).resolve(), proj)
TODO = lambda what: f'TODO {what}'

# 1 · intake ------------------------------------------------------------------------------------------
print('== intake'); subprocess.run([sys.executable, HERE / 'intake.py', src, '--out', build, '--ffmpeg', ff], check=True)
man = json.load(open(build / 'manifest.json'))
items = man['items']
pool = {r: [i for i in items if i['kind'] == 'image' and i.get('role') == r] for r in ('desktop', 'phone', 'photo', 'cutout', 'figure', 'logo')}
pool['video'] = [i for i in items if i['kind'] == 'video' and i.get('webm')]
music_files = [i for i in items if i['kind'] == 'audio' and i['role'] == 'music']
voice_files = [i for i in items if i['kind'] == 'audio' and i['role'] == 'voice']
path_of = lambda it: rel(it['webm']) if it['kind'] == 'video' else rel(src / it['file'])

# 2 · understand -------------------------------------------------------------------------------------
brief_path = Path(a.brief) if a.brief else next((p for p in (src / 'brief.json', proj / 'brief.json') if p.exists()), None)
brief = json.load(open(brief_path)) if brief_path else {}
docs = G.read_docs(src)
text = json.dumps({k: v for k, v in brief.items() if k not in ('contacts', '_how')}, ensure_ascii=False) + ' ' + docs
ranked, mats = G.classify(text, man)
gid = a.genre or brief.get('genre') or ranked[0]['genre']
if gid not in G.GENRES['genres']: sys.exit(f'ERROR genre {gid} unknown.\n  FIX: python3 scripts/genres.py --list')
genre = G.GENRES['genres'][gid]
close = (ranked[0]['score'] == 0 or (len(ranked) > 1 and ranked[0]['score'] - ranked[1]['score'] < 1.0)) and not a.genre and not brief.get('genre')
style = a.style or (brief.get('style') if brief.get('style') not in (None, '', 'auto') else genre['style'][0])
motion = a.motion or genre['motion']
mo = brief.get('motto') or {}
motto = (mo['zh'][:2] if isinstance(mo.get('zh'), list) and len(mo['zh']) >= 2 else [TODO('理念第一行'), TODO('理念第二行')]) + [mo.get('en') or TODO('motto in English')]

# guess name / positioning from docs when there is no brief
def guess_name():
    m = re.search(r'^#\s+(.+)$', docs, re.M)
    return (m.group(1).strip() if m else src.name.replace('-', ' ').replace('_', ' ').title())[:40]

def doc_facts(limit=10):
    """The docs' own bullet points and first paragraph: what the copywriter may say."""
    out = []
    for p in sorted(src.rglob('*')):
        if p.suffix.lower() not in ('.md', '.txt') or not p.is_file(): continue
        for line in p.read_text(errors='ignore').splitlines():
            t = line.strip()
            if t.startswith(('- ', '* ', '• ')): out.append(t[2:].strip())
            elif t and not t.startswith(('#', '(', '[', '!')) and len(out) < 1: out.append(t)
    return out[:limit]


FACTS = doc_facts()
P = brief.get('product', {})
name = P.get('name') or guess_name()
features = brief.get('features') or []
if not features:   # one feature per strong visual (max 3), named after its file
    vis = (pool['desktop'] + pool['photo'] + pool['cutout'] + pool['phone'])[:3]
    features = [{'id': f'f{k}', 'zh': TODO('功能/卖点（≤12字）'), 'en': TODO(f'feature shown in {Path(v["file"]).name}'), 'materials': [v['file']]} for k, v in enumerate(vis)]


MACRO = re.compile(r'detail|texture|macro|close|glaze|material|fabric|grain|特写|细节|质感|纹理', re.I)


def take(roles, used, k=1, prefer=None):
    """Pop up to k unused materials of the given roles (in order of preference)."""
    out = []
    for r in roles:
        for it in pool.get(r, []):
            if it['file'] not in used and (prefer is None or prefer(it)):
                out.append(it); used.add(it['file'])
                if len(out) >= k: return out
    return out


def match(globs):
    hits = []
    for g in globs or []:
        for it in items:
            if it['kind'] in ('image', 'video') and (fnmatch.fnmatch(it['file'], g) or fnmatch.fnmatch(Path(it['file']).name, g)): hits.append(it)
    return hits


def need_ok(need):
    if need == 'none': return True
    if need.startswith('brief:'): return bool(brief.get(need[6:]))
    for alt in need.split('|'):
        role, _, n = alt.partition(':'); n = int(n or 1)
        if role == 'any' and sum(len(v) for k, v in pool.items() if k != 'logo') >= n: return True
        if role == 'ui' and len(pool['desktop']) + len(pool['phone']) >= n: return True
        if len(pool.get(role, [])) >= n: return True
    return False


# 3 · cast: arc beats → scenes ------------------------------------------------------------------------
used, scenes, fill = set(), [], a.fill_copy
logo = pool['logo'][0] if pool['logo'] else None
if logo: used.add(logo['file'])
txt = lambda field, lang, what: (brief.get(field, {}) or {}).get(lang) if fill and isinstance(brief.get(field), dict) and brief[field].get(lang) else TODO(what)
for beat in G.GENRES['arcs'][genre['arc']]:
    t, need = beat['type'], beat['needs']
    if not need_ok(need): continue
    sc = {'type': t, 'bars': beat['bars']}
    if t == 'cover':
        bg = take(['photo', 'desktop', 'figure'], set(), 1, prefer=lambda i: not MACRO.search(i['file'])) or take(['photo', 'desktop', 'figure'], set(), 1)
        if bg:
            sc.update({'media': path_of(bg[0]), 'base': bg[0].get('base', [1920, 1080])})
            if bg[0].get('role') == 'photo': sc['frame'] = 'photo'
        sc['say'] = [{'en': TODO('hook line = treatment §3 Hook line: a tension, a question or a physical detail (≤ 12 words)'), 'zh': TODO('开场钩子（≤ 20 字）'), 'at': 0.6}]
    elif t == 'pain':
        sc['say'] = [{'en': txt('pain', 'en', 'the tension, one sentence'), 'zh': txt('pain', 'zh', '痛点一句话')}]
    elif t == 'statement':
        ins = brief.get('insight') or {}
        sc.update({'zh': ins.get('zh') if fill and ins.get('zh') else TODO('洞察 / 情感真相（≤ 16 字）'), 'en': ins.get('en') if fill and ins.get('en') else TODO('the human truth, one line')})
    elif t == 'photo':
        it = take(['photo'], used, 1, prefer=lambda i: not MACRO.search(i['file'])) or take(['photo'], used, 1)
        if not it: continue
        sc.update({'media': path_of(it[0]), 'base': it[0]['base'], 'title': {'zh': TODO('画面一句（≤ 10 字）'), 'en': TODO('one line over the photo')}})
    elif t == 'detail':
        it = take(['photo', 'cutout'], used, 1, prefer=lambda i: bool(MACRO.search(i['file']))) or take(['photo', 'cutout'], used, 1) or take(['photo', 'cutout'], set(), 1)
        if not it: continue
        sc.update({'media': path_of(it[0]), 'base': it[0]['base']})
    elif t == 'hero':
        its = take(['cutout'], used, 3) or take(['photo'], used, 1)
        if not its: continue
        if len(its) == 1: sc['bars'] = min(sc['bars'], 3)   # one object: a short reveal, not a long hold
        sc.update({'media': [path_of(i) for i in its] if len(its) > 1 else path_of(its[0]), 'base': its[0]['base'],
                   'title': {'zh': (P.get('tagline') or {}).get('zh') if fill and (P.get('tagline') or {}).get('zh') else TODO('揭晓标题（≤ 10 字）'), 'en': name}})
        sc['say'] = [{'en': TODO('the reveal line: the name + one fact from the docs (≤ 12 words)'), 'zh': TODO('揭晓旁白')}]
    elif t == 'feature':
        for k, f in enumerate(features[:4]):
            mats_f = [m for m in match(f.get('materials')) if m['file'] not in used] or take(['desktop', 'photo', 'cutout', 'phone'], used, 1)
            if not mats_f: break
            m0 = mats_f[0]; used.add(m0['file'])
            is_ui = m0.get('role') in ('desktop', 'phone') or m0['kind'] == 'video'
            if m0.get('role') == 'photo':   # a photograph carries a proof beat full-bleed, with one line — not a card with a list
                scenes.append({'type': 'photo', 'bars': beat['bars'], 'media': path_of(m0), 'base': m0.get('base', [1920, 1080]),
                               'title': {'zh': TODO('画面一句：这一拍的事实（≤ 10 字）'), 'en': TODO('the fact of this beat, in a few words')},
                               'say': [{'en': TODO('one fact from the docs, said as what it means for the viewer (not a spec list)'), 'zh': TODO('旁白中文字幕')}]})
                continue
            fs = {'type': 'feature', 'bars': beat['bars'], 'media': path_of(m0), 'base': m0.get('base', [1920, 1080]),
                  'title': {'zh': f['zh'] if fill and 'TODO' not in f.get('zh', 'TODO') else TODO('功能标题（≤ 12 字）'), 'en': f['en'] if fill and 'TODO' not in f.get('en', 'TODO') else TODO('feature title (≤ 42 chars)')},
                  'points': [{'zh': TODO('要点（≤ 12 字）'), 'en': TODO('point')} for _ in range(2)],
                  'say': [{'en': TODO('one fact from the docs, said as what it means for the viewer (not a spec list)'), 'zh': TODO('旁白中文字幕')}]}
            if not is_ui: fs['frame'] = 'photo'
            elif m0['kind'] == 'image':   # screens: pre-suggest the highlight boxes (check them: suggest_rects.py --preview)
                try:
                    _, rects = SR.suggest(src / m0['file'], fs['base'], 2)
                    for pt, rc in zip(fs['points'], rects): pt['rect'] = rc
                    if rects: fs['_rects'] = 'auto-suggested by suggest_rects.py: match each point to the region it names (preview: python3 scripts/suggest_rects.py <image> --preview .)'
                except Exception as e:
                    print(f'  (no rect suggestion for {m0["file"]}: {e})')
            if k == 0 and t == 'feature' and genre['arc'] == 'problem-solution': fs['chapter'] = ['01', TODO('章节'), TODO('CHAPTER')]
            scenes.append(fs)
        continue
    elif t == 'carousel':
        its = take(['desktop'], used, 4)
        if len(its) < 2: continue
        sc['panels'] = [{'zh': TODO('名称'), 'en': TODO('name'), 'media': path_of(i), 'base': i['base']} for i in its]
    elif t == 'gallery':
        its = take(['figure', 'photo'], used, 5)
        if len(its) < 2: continue
        sc['items'] = [{'media': path_of(i), 'zh': TODO('名称'), 'en': TODO('name')} for i in its]
    elif t == 'clip':
        its = take(['video'], used, 1)
        if not its: continue
        sc.update({'media': path_of(its[0]), 'title': {'zh': TODO('录屏标题'), 'en': TODO('clip title')}})
    elif t == 'phone':
        its = take(['phone'], used, 1)
        if not its: continue
        sc.update({'media': path_of(its[0]), 'base': its[0]['base'], 'title': {'zh': TODO('手机端一句'), 'en': TODO('mobile line')}})
    elif t == 'lineup':
        its = take(['cutout'], used, 5) or take(['cutout'], set(), 5)
        if len(its) < 2: continue
        sc['items'] = [{'media': path_of(i), 'zh': TODO('型号/款式'), 'en': TODO('variant')} for i in its]
    elif t == 'numbers':
        sc['stats'] = brief['numbers'][:3]
    elif t == 'compare':
        sc['rows'] = brief['differentiators'][:5]
    elif t == 'quote':
        q = brief['testimonials'][0]
        sc.update({'zh': q.get('zh', ''), 'en': q.get('en', ''), 'who': q.get('who', ''), 'role': q.get('role', '')})
    elif t == 'finale':
        wall = [path_of(i) for i in items if i['kind'] == 'image' and i.get('role') in ('desktop', 'photo', 'cutout', 'figure', 'phone')][:8]
        if not wall: continue
        sc['media'] = wall
        sc['say'] = [{'id': 'tagline', 'en': TODO('hero line = treatment §3 Hero line: the name + the tagline'), 'zh': TODO('口号'), 'at': 1.2}]
    elif t == 'endcard':
        sc['say'] = [{'id': 'motto', 'en': TODO('last line = treatment §3 Last line: a callback to the hook, not logistics'), 'zh': TODO('收尾一句'), 'at': 0.6}]
    scenes.append(sc)

# breathing: never three proof beats in a row — a one-line statement after the second (crew.md §6)
for k in range(len(scenes) - 2):
    if all(x['type'] == 'feature' for x in scenes[k:k + 3]):
        scenes.insert(k + 2, {'type': 'statement', 'bars': 2, 'zh': TODO('一口气：点出感受，不加新事实（≤ 16 字）'), 'en': TODO('a breath between proofs: the feeling, no new fact')})
        break

# hero moment: the finale (make_film.py defaults to it); duration budget
music = None
if a.music not in ('auto', 'generate') and Path(a.music).exists(): music = {'file': rel(a.music)}
elif a.music == 'auto' and music_files: music = {'file': rel(src / music_files[0]['file'])}
if music is None: music = {'generate': {'mood': 'auto'}}
bpm = genre['music']['bpm']; bar_s = 240 / bpm
target = a.seconds or {'problem-solution': 100, 'reveal': 80, 'sensory': 75, 'human-story': 90, 'hype': 70}[genre['arc']]
optional = ['quote', 'lineup', 'gallery', 'carousel', 'phone', 'photo', 'clip', 'compare', 'detail', 'statement']
while sum(s['bars'] for s in scenes if s['bars'] != 'rest') * bar_s + MF.rest_bars(bpm) * bar_s > target + bar_s * 2:
    drop = next((s for t in optional for s in scenes if s['type'] == t), None)
    feats = [s for s in scenes if s['type'] == 'feature']
    if drop is None and len(feats) > 2: drop = feats[-1]
    if drop is None: break
    scenes.remove(drop)

voice = {'engine': 'none', '_note': 'no Kokoro found (references/audio.md "Kokoro setup" — ask the user before installing): captions only'}
kpy = MF.kokoro_python()
if voice_files: voice = {'engine': 'files', 'files': {}, '_how': 'map each say id to one of: ' + ', '.join(v['file'] for v in voice_files)}
elif a.voice in ('auto', 'kokoro') and (kpy or a.voice == 'kokoro'):
    model, cached = MF.kokoro_cached()
    want = genre['voice']
    pick = want if want in cached else (cached[0] if cached else want)
    voice = {'engine': 'kokoro', 'voice': pick, 'lang': 'a', 'python': kpy or '~/.venvs/kokoro/bin/python', 'espeak_data': '~/.cache/kes'}
    if pick != want:
        voice['_note'] = f'the genre suggests {want}; {pick} is used because it is already downloaded. {want} is a ≈ 0.5 MB download: ask the user first, then set "allow_download": true'
    elif not model or want not in cached:
        voice['_note'] = 'the Kokoro model or voice is not downloaded yet: ask the user first, then set "allow_download": true'

film = {
    '_how': 'Drafted by autofilm.py. The crew (references/crew.md) replaces every TODO, then: python3 <skill>/scripts/make_film.py film.json --stage check',
    'name': re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-') + '-film', 'out': 'film_out',
    'materials': rel(src), 'genre': gid, 'style': style, 'motion': motion, 'cinema': 'auto', 'music': music, 'voice': voice,
    'brand': {'name': name, 'nameAccent': P.get('nameAccent', ''), 'logo': path_of(logo) if logo else TODO('transparent PNG logo path'),
              'positioningZh': (P.get('positioning') or {}).get('zh') or TODO('一句话定位'), 'positioningEn': (P.get('positioning') or {}).get('en') or TODO('ONE-LINE POSITIONING'),
              'taglineZh': (P.get('tagline') or {}).get('zh') or TODO('口号'), 'taglineEn': (P.get('tagline') or {}).get('en') or TODO('TAGLINE'),
              'motto': motto,
              'contacts': brief.get('contacts', []), 'chips': P.get('platforms', []) + ([P['status']] if P.get('status') else [])},
    'scenes': scenes,
}
json.dump(film, open(proj / 'film.json', 'w'), ensure_ascii=False, indent=1)
if not brief_path:   # a brief for THIS product from its docs (never another product's example)
    json.dump({'_how': 'Drafted by autofilm.py from the docs. Fill what is missing from the user\'s docs; every claim must be checkable. Field guide: templates/brief.example.json',
               'product': {'name': name, 'positioning': {'zh': '', 'en': ''}, 'tagline': {'zh': '', 'en': ''}},
               'genre': gid, 'facts': FACTS, 'features': [], 'contacts': []}, open(proj / 'brief.json', 'w'), ensure_ascii=False, indent=1)

# 4 · treatment scaffold for the crew --------------------------------------------------------------------
tpl = (SKILL / 'templates' / 'treatment.template.md').read_text()
beats = '\n'.join(f"| {i + 1} | `{s['type']}` | {s['bars'] if s['bars'] != 'rest' else MF.rest_bars(bpm)} | {next((b['role'] for b in G.GENRES['arcs'][genre['arc']] if b['type'] == s['type']), '')} | |" for i, s in enumerate(scenes))
fills = {'{{PRODUCT}}': name, '{{GENRE}}': f"{gid} — {genre['en']} / {genre['zh']}", '{{STYLE}}': style, '{{MOTION}}': motion, '{{ARC}}': genre['arc'],
         '{{MUSIC}}': music.get('file') or f"composed: {genre['music']['mood']} ~{bpm} BPM (original, royalty-free)", '{{TONE}}': genre['tone'],
         '{{MATERIALS}}': ', '.join(f'{k} {v}' for k, v in sorted(mats.items()) if v), '{{BEATS}}': beats, '{{SECONDS}}': f'{target:.0f}',
         '{{GOLDEN}}': f"templates/golden/{genre['arc']}.json", '{{FACTS}}': ' · '.join(FACTS) or '(no docs — ask the user for a README or brief)'}
for k, v in fills.items(): tpl = tpl.replace(k, str(v))
(proj / 'treatment.md').write_text(tpl)

todo = sum(1 for _ in MF._strings(film) if 'TODO' in _[1])
print(f"\n== draft ready → {proj}")
print(f"genre   {gid} ({genre['en']})" + (f"   ⚠ close call with {ranked[1]['genre']} — confirm with the user" if close else ''))
print(f"look    {style} · motion {motion} · arc {genre['arc']} · music {music.get('file') or 'composed ' + genre['music']['mood']}")
print(f"scenes  {len(scenes)} ({', '.join(s['type'] for s in scenes)}) ≈ {sum(s['bars'] for s in scenes if s['bars'] != 'rest') * bar_s + MF.rest_bars(bpm) * bar_s:.0f} s")
print(f"copy    {todo} TODO fields — the crew writes them (references/crew.md), starting with treatment.md")
print(f"voice   {voice['engine']}" + (f" {voice.get('voice')}" if voice['engine'] == 'kokoro' else '') + (f"  ({voice['_note']})" if voice.get('_note') else ''))
print(f"study   {SKILL / 'templates' / 'golden' / (genre['arc'] + '.json')} and references/copy-bank.md before writing a word")
print("next    1) run the crew: fill treatment.md (anchor lines first)   2) replace every TODO in film.json   3) python3 scripts/make_film.py film.json --stage check")
