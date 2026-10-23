#!/usr/bin/env python3
"""The director's proposals: 2–3 directions for the film, each with a real preview, for the USER to choose or edit.
Nothing is written past the draft until the user has picked one (make_film.py refuses to build an autofilm draft whose
"approved" is empty).

  python3 proposals.py <project>/film.json [--n 3] [--no-previews]
      reads the materials like the director (scripts/look.py), writes <project>/proposals.md with 2–3 directions
      (look, motion, pace, palette, grade, the director's reasons) and renders a 3-frame preview of each one from the
      real materials (proposals/<A|B|C>.jpg). The agent adds a concept, a hook and a hero line to every option, shows
      the file and the previews to the user, and WAITS.

  python3 proposals.py <project>/film.json --apply B [--style … --motion … --variety … --mood "…"] [--note "…"] [--by user|assumed]
      after the user answers: redrafts the film in the chosen direction (autofilm again, same materials and settings,
      with any change the user asked for), records the decision in film.json "approved" and in proposals.md.
      --by assumed only when the user cannot be asked (a batch run); say so in the report.
"""
import argparse, copy, json, re, shutil, subprocess, sys, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import look as LOOK          # noqa: E402
import palette as PAL        # noqa: E402

# every option should look AND move differently: the motions a look can carry, best first
LOOK_MOTIONS = {'midnight-tech': ['cinematic-3d', 'precision-data', 'kinetic-launch'], 'neon-cyber': ['kinetic-launch', 'cinematic-3d', 'playful-pop'],
                'clean-light': ['gentle-story', 'precision-data', 'cinematic-3d'], 'paper-academic': ['precision-data', 'editorial-type', 'gentle-story'],
                'editorial-mono': ['editorial-type', 'kinetic-launch', 'precision-data'], 'luxe-noir': ['gentle-story', 'editorial-type', 'cinematic-3d'],
                'natural-fresh': ['gentle-story', 'playful-pop', 'editorial-type'], 'aurora-glass': ['playful-pop', 'kinetic-launch', 'gentle-story']}
PACE = {'gentle-story': 'calm', 'precision-data': 'balanced', 'cinematic-3d': 'balanced', 'editorial-type': 'balanced',
        'kinetic-launch': 'rich', 'playful-pop': 'rich'}
STYLE_GRADE = {}


def style_grade(style):
    if style not in STYLE_GRADE:
        try:
            import make_film as MF
            STYLE_GRADE[style] = MF.style_profile(style).get('grade')
        except Exception:
            STYLE_GRADE[style] = None
    return STYLE_GRADE[style]


def load(film_path):
    film_path = Path(film_path).resolve()
    proj = film_path.parent
    f = json.load(open(film_path))
    man = proj / 'build' / 'manifest.json'
    if not man.exists(): sys.exit('ERROR no build/manifest.json next to film.json.\n  FIX: run autofilm.py first: proposals are made from its draft')
    m = json.load(open(man))
    return film_path, proj, f, m


def options(f, m, n, mood=''):
    src = Path(m['materials'])
    gid = f.get('genre') or ''
    docs = ''
    try:
        import genres as G
        docs = G.read_docs(src)
    except Exception:
        pass
    lk = LOOK.choose(m['items'], src, gid, docs, mood or (f.get('_autofilm') or {}).get('mood', ''))
    styles = [s for s, _ in lk['ranked']][:n]
    logo = next((src / i['file'] for i in m['items'] if i.get('role') == 'logo'), None)
    pics = [src / i['file'] for i in m['items'] if i.get('kind') == 'image' and i.get('role') in ('desktop', 'photo', 'cutout', 'figure', 'phone')]
    brief = {}
    bp = (f.get('_autofilm') or {}).get('brief')
    if bp and Path(bp).exists(): brief = json.load(open(bp))
    out, used_m, used_v = [], set(), set()
    for k, st in enumerate(styles):
        cands = ([lk['motion']] if k == 0 else []) + LOOK_MOTIONS.get(st, [LOOK.STYLE_MOTION.get(st, lk['motion'])])
        motion = next((c for c in cands if c not in used_m), cands[0]); used_m.add(motion)
        pace = PACE.get(motion, 'balanced')
        if pace in used_v: pace = next((v for v in ('balanced', 'calm', 'rich') if v not in used_v), pace)
        used_v.add(pace)
        pal = PAL.choose(gid, st, logo, pics, brand_hex=brief.get('brand_color'))
        temp = pal.pop('temperature', 'neutral'); pal.pop('style_accent', None)
        grade = PAL.grade_for(temp, style_grade(st), st) or style_grade(st)
        score = dict(lk['ranked'])[st]
        reasons = next((l.split(': ', 1)[1] for l in lk['why'] if l.strip().startswith(('look ' + st, 'also ' + st))), '')
        out.append({'id': 'ABC'[k], 'style': st, 'motion': motion, 'variety': pace, 'palette': pal, 'grade': grade,
                    'score': round(score, 1), 'what': LOOK.STYLES[st], 'why': reasons, 'recommended': k == 0})
    return out, lk


def preview(film_path, proj, f, opt):
    """Build the cover + the first two story beats + the end card in this direction (copy blanked) and grab 3 frames."""
    pf = copy.deepcopy(f)
    pf.update({'style': opt['style'], 'motion': opt['motion'], 'palette': opt['palette'], 'treatment': 'skip', '_preview': True,
               'voice': {'engine': 'none'}, 'out': f'proposals/_build_{opt["id"]}', 'name': f'proposal-{opt["id"]}',
               'direction': {'variety': opt['variety']}})
    pf['cinema'] = {'grade': opt['grade']} if opt['grade'] else 'auto'
    for k in ('camera', 'cut', 'layout'):
        for sc in pf['scenes']: sc.pop(k, None)   # let this direction's own director plan the frames
    sc = pf['scenes']
    rank = {'feature': 0, 'lineup': 0, 'carousel': 1, 'gallery': 1, 'compare': 2, 'hero': 3, 'photo': 4, 'footage': 4, 'detail': 5}   # beats that show the look's type, cards and frames
    mid = sorted([s for s in sc[1:-1] if s.get('type') in rank], key=lambda s: rank[s['type']])[:1]
    pf['scenes'] = [sc[0]] + mid + [sc[-1]]

    def blank(o, key=''):   # placeholder words, so the look's type, cards and frames show in the preview (never used in the film)
        if isinstance(o, dict): return {k: blank(v, k) for k, v in o.items()}
        if isinstance(o, list): return [blank(v, key) for v in o]
        if isinstance(o, str) and o.startswith('TODO'):
            return '示例标题' if 'zh' in key.lower() or key in ('motto',) else 'Sample line' if 'en' in key.lower() else '示例 Sample'
        return o
    pf = blank(pf)
    for s in pf['scenes']: s.pop('say', None)
    mu = pf.get('music') or {}
    if isinstance(mu, dict) and mu.get('extend'): mu.pop('extend')
    tmp = proj / f'film.proposal-{opt["id"]}.json'
    json.dump(pf, open(tmp, 'w'), ensure_ascii=False, indent=1)
    mf = HERE / 'make_film.py'
    r = subprocess.run([sys.executable, mf, tmp, '--stage', 'build', '--draft'], capture_output=True, text=True)
    out_dir = proj / pf['out']
    jpg = proj / 'proposals' / f'{opt["id"]}.jpg'
    try:
        if r.returncode != 0 or not (out_dir / 'film' / 'film.html').exists():
            tail = [l for l in (r.stdout + r.stderr).splitlines() if 'ERROR' in l][:3]
            return None, 'preview not built: ' + ('; '.join(tail) or 'see make_film output')
        (out_dir / 'tools').mkdir(exist_ok=True)
        js = out_dir / 'tools' / 'proposal_frames.mjs'
        js.write_text('''import { chromium } from 'playwright';
import { pathToFileURL } from 'url';
import path from 'path';
const [html, out] = process.argv.slice(2);
const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto(pathToFileURL(path.resolve(html)).href);
await p.evaluate(() => window.ready);
const S = await p.evaluate(() => SCENES.map((s) => [s.s, s.e]));
const ts = [S[0][0] + (S[0][1] - S[0][0]) * 0.93, S[1][0] + Math.min(2.4, (S[1][1] - S[1][0]) * 0.3), S[2][0] + Math.min(4, (S[2][1] - S[2][0]) * 0.6)];   // the name, a story beat, the end card
let k = 0;
for (const t of ts) { await p.evaluate((tt) => window.renderFrame(tt), t); await p.waitForTimeout(200); await p.screenshot({ path: `${out}_${k++}.png` }); }
await b.close();
''')
        stem = proj / 'proposals' / f'_{opt["id"]}'
        rr = subprocess.run(['node', js, out_dir / 'film' / 'film.html', stem], capture_output=True, text=True, cwd=out_dir)
        shots = sorted((proj / 'proposals').glob(f'_{opt["id"]}_*.png'))
        if rr.returncode != 0 or not shots: return None, 'preview frames failed: ' + (rr.stderr.strip().splitlines() or ['?'])[-1][:160]
        from PIL import Image, ImageDraw
        tiles = [Image.open(s).convert('RGB').resize((640, 360)) for s in shots]
        sheet = Image.new('RGB', (640 * len(tiles) + 8 * (len(tiles) - 1), 360), (12, 12, 14))
        for i, t in enumerate(tiles): sheet.paste(t, (i * 648, 0))
        sheet.save(jpg, quality=88)
        for s in shots: s.unlink()
        return jpg, None
    finally:
        tmp.unlink(missing_ok=True)
        shutil.rmtree(out_dir, ignore_errors=True)


def write_md(proj, f, opts, lk, notes):
    name = (f.get('brand') or {}).get('name', '')
    L = [f'# Director\'s proposals · 导演方案 — {name}', '',
         'The director read the materials and proposes these directions. **Show them to the user (with the previews) and wait for their choice or changes before any copy, voice or render.**',
         '导演读完素材后提出以下方向。**把方案和预览图给用户看，等用户选择或修改后，再写文案、配音、渲染。**', '',
         f'What the materials are · 素材情况: {lk["facts"]}', '',
         'Before showing: write the three lines of every option (concept, hook, hero) from the docs and the materials. 展示前：为每个方案写好三行（概念、开场、高潮）。', '']
    for o in opts:
        star = ' — recommended · 推荐' if o['recommended'] else ''
        L += [f'## Option {o["id"]} · 方案 {o["id"]}{star}',
              f'- Look · 视觉: **{o["style"]}** — {o["what"]}',
              f'- Motion & pace · 动效与节奏: {o["motion"]} · variety {o["variety"]}',
              f'- Colour · 配色: accent {o["palette"]["accent"]} · second {o["palette"]["accent2"]} · grade {o["grade"] or "style default"}',
              f'- Why the director sees it · 导演的依据 (score {o["score"]}): {o["why"] or "—"}',
              f'- Preview · 预览: ' + (f'![{o["id"]}](proposals/{o["id"]}.jpg)' if o.get('preview') else (notes.get(o['id']) or 'not rendered')),
              '- Concept · 创意概念: <write: one idea for this direction, in a sentence>',
              '- Hook · 开场: <write: what the first 3 seconds show and say>',
              '- Hero · 高潮: <write: the one moment the film builds to>', '']
    L += ['## Decision · 决定', '- Pending: waiting for the user. 待定：等待用户选择。',
          '- Then: `python3 scripts/proposals.py film.json --apply <A|B|C> [--style … --motion … --variety … --mood "…"] --note "<the user\'s changes>"`', '']
    (proj / 'proposals.md').write_text('\n'.join(L))


def apply(film_path, proj, f, m, a):
    md = proj / 'proposals.md'
    if not md.exists(): sys.exit('ERROR no proposals.md.\n  FIX: run proposals.py film.json first and show the options to the user')
    text = md.read_text()
    blk = re.search(rf'## Option {a.apply}\b.*?(?=\n## |\Z)', text, re.S)
    if not blk: sys.exit(f'ERROR no option {a.apply} in proposals.md')
    pick = lambda label: (re.search(label + r'[^\n]*?\*\*([\w-]+)\*\*', blk.group(0)) or re.search(label + r'[^:]*:\s*([\w-]+)', blk.group(0)))
    style = a.style or pick('Look').group(1)
    mot = re.search(r'Motion & pace[^:]*:\s*([\w-]+)\s*·\s*variety\s*(\w+)', blk.group(0))
    motion, variety = a.motion or mot.group(1), a.variety or mot.group(2)
    if any('<write' in l for l in blk.group(0).splitlines()) and a.by == 'user':
        print('WARN option ' + a.apply + ' still has <write: …> lines; the crew writes them into treatment.md §3 anyway')
    A = f.get('_autofilm') or {}
    if not A.get('materials'): sys.exit('ERROR film.json has no "_autofilm" record.\n  FIX: redraft with the current autofilm.py, then run proposals.py again')
    cmd = [sys.executable, HERE / 'autofilm.py', A['materials'], '--out', proj, '--style', style, '--motion', motion, '--variety', variety]
    for k in ('brief', 'genre', 'music', 'voice'):
        if A.get(k): cmd += [f'--{k}', str(A[k])]
    if A.get('seconds'): cmd += ['--seconds', str(A['seconds'])]
    mood = a.mood if a.mood is not None else A.get('mood')
    if mood: cmd += ['--mood', mood]
    print('== redraft in option', a.apply, f'({style} · {motion} · {variety})')
    r = subprocess.run(cmd)
    if r.returncode != 0: sys.exit('ERROR autofilm failed; nothing was approved')
    nf = json.load(open(film_path))
    nf['approved'] = {'option': a.apply, 'by': a.by, 'style': style, 'motion': motion, 'variety': variety,
                      'note': a.note or '', 'at': datetime.date.today().isoformat()}
    json.dump(nf, open(film_path, 'w'), ensure_ascii=False, indent=2)
    who = 'the user chose' if a.by == 'user' else 'ASSUMED (the user could not be asked; say so in the report)'
    text = re.sub(r'## Decision · 决定\n.*', f'## Decision · 决定\n- Option {a.apply}: {who} — {style} · {motion} · {variety}' + (f' · changes: {a.note}' if a.note else '') + f' ({nf["approved"]["at"]})\n', text, flags=re.S)
    md.write_text(text)
    print(f'approved option {a.apply} ({who}). Next: the crew fills treatment.md (references/crew.md), using the chosen concept, hook and hero.')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('film'); ap.add_argument('--n', type=int, default=3); ap.add_argument('--no-previews', action='store_true')
    ap.add_argument('--apply'); ap.add_argument('--style'); ap.add_argument('--motion'); ap.add_argument('--variety', choices=['calm', 'balanced', 'rich'])
    ap.add_argument('--mood'); ap.add_argument('--note'); ap.add_argument('--by', choices=['user', 'assumed'], default='user')
    a = ap.parse_args()
    film_path, proj, f, m = load(a.film)
    if a.apply:
        a.apply = a.apply.upper()
        return apply(film_path, proj, f, m, a)
    n = max(2, min(3, a.n))
    opts, lk = options(f, m, n, a.mood or '')
    (proj / 'proposals').mkdir(exist_ok=True)
    notes = {}
    for o in opts:
        if a.no_previews: continue
        print(f'== preview {o["id"]}: {o["style"]} · {o["motion"]}')
        jpg, err = preview(film_path, proj, f, o)
        o['preview'] = bool(jpg)
        if err: notes[o['id']] = err; print('  ' + err)
    write_md(proj, f, opts, lk, notes)
    print(f'\n== {len(opts)} directions → {proj / "proposals.md"}' + ('' if a.no_previews else f' (previews in {proj / "proposals"})'))
    for o in opts: print(f'  {o["id"]}  {o["style"]:15s} {o["motion"]:15s} {o["variety"]:9s} accent {o["palette"]["accent"]}' + ('   ← recommended' if o['recommended'] else ''))
    print('NEXT: write each option\'s concept, hook and hero in proposals.md, show it and the previews to the user, and WAIT for their choice or changes.\n'
          '      Then: python3 scripts/proposals.py film.json --apply <A|B|C> [--style/--motion/--variety/--mood to apply their changes] --note "…"')


if __name__ == '__main__':
    main()
