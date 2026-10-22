"""Check the crew's treatment before building: complete, specific, consistent with film.json, and above the taste bar.

Usage: python check_treatment.py treatment.md [film.json]
Prints ERROR/FIX lines like make_film.py; exit 1 if anything must be fixed. make_film.py runs it before every build.
Checks
  form      every section 0–9, no "<write:" or "{{" left; three concepts, a chosen one with a reason; hook; hero; tagline
            (zh ≤ 12 字, en ≤ 8 words); the three concepts really differ
  taste     eight scores 1–5, average ≥ 4.0, none below 3
  film.json (if given)
    copy        no TODO; tagline matches; lint_copy clean (no clichés, ≤ 2 vague words in the whole film)
    script      the treatment's voice-over is a real script (one line per beat), and every spoken line in film.json is in it
    specificity ≥ 2/3 of the spoken lines, and every feature/hero line, carry a concrete fact from the docs (a number or a
                noun from the README/brief) — "Like the first cup of the morning" may be the mood, not the whole film
    qualifiers  a claim the docs limit (Pro/paid edition, beta, one platform, region, planned) carries that limit in its scene
                (line, caption or chip); a limit that does not apply is named in §8 Qualifiers with 'not affected' and a reason
    idea        the chosen concept is on screen: its key words reach the film's copy, the tagline echoes the proposition
    cross-check each taste score is capped by what the film shows (e.g. "specific copy" cannot be 4 when half the lines
                are generic). A score above its cap is an ERROR: fix the film, never the score.
The docs are found from film.json "materials" (autofilm writes it) or the folder of brand.logo.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_copy  # noqa: E402

errs, warns_ = [], []
def err(m, fix): errs.append(f'ERROR {m}\n  FIX: {fix}')
def warn(m, fix): warns_.append(f'WARN  {m}\n  FIX: {fix}')
zhlen = lint_copy.zhlen

STOP = set('''a an the and or but of to in on at for with by from as is are was were be been being it its this that these those your you we our
they their them he she his her i me my not no so if then than there here into over under up down out off about after before again all any
both each few more most other some such only own same too very can will just should would could may might must do does did done has have had
having make makes made get gets got one ones every what when where which who why how also like way ways thing things day days time
less much many lot well back still even ever never always new old first last next own whole part keep keeps kept let lets go goes going come
comes take takes see seen look looks feel feels need needs want wants'''.split())
NUMWORDS = set('''one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty sixty hundred thousand million
once twice half dozen single double triple first second third'''.split())
GENERIC = set('''product products brand people life world moment moments story stories quality experience solution solutions everything
something nothing anything someone everyone today tomorrow future better best great good real true simple easy fast slow made make'''.split())


def stem(w):
    w = re.sub(r"['’]s$", '', w.lower()).strip("'’")
    for suf in ('ies', 'es', 's', 'ing', 'ed'):
        if len(w) > 4 and w.endswith(suf): return w[: -len(suf)] + ('y' if suf == 'ies' else '')
    return w


def words(s): return re.findall(r"[A-Za-z][A-Za-z'’\-]*", s or '')


def concrete_vocab(text, brand):
    """Stems of nouns/numbers a line can take from the docs: content words ≥ 3 letters, not stop/generic words, not the brand name."""
    bn = {stem(w) for w in words(brand)}
    return {stem(w) for w in words(text) if len(w) >= 3 and w.lower() not in STOP and w.lower() not in GENERIC} - bn


def is_concrete(line, vocab):
    if re.search(r'\d', line): return True
    ws = [w.lower() for w in words(line)]
    return any(w in NUMWORDS for w in ws) or any(stem(w) in vocab for w in ws if w not in STOP and w not in GENERIC)


QUALIFIERS = [r'pro(?:fessional)? (?:edition|version|plan|tier)', r'\bpro\b', r'premium', r'paid', r'enterprise', r'business plan', r'subscription', r'\bplus\b',
              r'beta', r'preview', r'early access', r'waitlist', r'coming soon', r'planned', r'roadmap', r'experimental', r'not yet',
              r'(?:mac ?os|windows|ios|android|linux|web|desktop|mobile)[- ]only', r'only (?:on|in|for) \w+', r'select(?:ed)? (?:regions|markets|countries)',
              r'limited edition', r'add-on', r'sold separately', r'requires? (?:a |an )?\w+ (?:plan|licen[cs]e|subscription|account)',
              '专业版', '高级版', '旗舰版', '付费', '会员', '订阅', '企业版', '测试版', '内测', '预览版', '即将', '计划中', '规划中', '实验性', '仅限', '仅支持', '选配', '另售', '部分地区', '限量']
QRE = re.compile('|'.join(f'(?:{q})' for q in QUALIFIERS), re.I)


def cjk_grams(s):
    c = re.sub(r'[^\u4e00-\u9fff]', '', s or '')
    return {c[k:k + 2] for k in range(len(c) - 1)}


def qkey(q):
    """The word that must reappear: "Pro edition" → Pro, "only on macOS" → macOS, "coming soon" → soon, 专业版 → 专业版."""
    w = q.split()
    if len(w) == 1: return w[0]
    return w[-1] if w[0].lower() in ('only', 'requires', 'require', 'not', 'select', 'selected', 'coming', 'sold', 'limited', 'early', 'business') else w[0]


def omitted_qualifiers(spec, docs):
    """(scene index, claim, doc sentence, qualifier) for claims the docs qualify but the scene does not."""
    flat = re.sub(r'"\s*[,:]\s*"|"\s*[\]\[{}]|[\]\[{}]\s*"|\\n', '\n', docs)       # JSON lists/fields from brief.json → one item per line
    flat = re.sub(r'[\w./-]+\.(?:png|jpe?g|webp|gif|webm|mp4|mov|docx?|pdf)\b', '', flat, flags=re.I)   # a file name ("02-data-preview.png") is not a qualifier
    sents = [x.strip(' -•*"') for x in re.split(r'(?<=[.!?。！？；;])\s+|\n+', flat) if QRE.search(x or '')]
    out, seen = [], set()
    for i, sc in enumerate(spec.get('scenes', [])):
        texts = [v for _, v in lint_copy.walk(sc) if isinstance(v, str) and len(v) > 3]
        scene_txt = ' '.join(texts)
        for t in texts:
            tw = {stem(w) for w in words(t) if w.lower() not in STOP and w.lower() not in GENERIC and len(w) > 2}
            for sent in sents:
                q = QRE.search(sent).group(0)
                sw = {stem(w) for w in words(sent) if w.lower() not in STOP and w.lower() not in GENERIC and len(w) > 2}
                cg = len(cjk_grams(t) & cjk_grams(sent))
                shared = len(tw & sw) + (2 if cg >= 3 else 1 if cg >= 2 else 0)
                need = 1 if len(sw) <= 3 else 2          # a short qualifier sentence ("Linux is planned.") names one thing
                if shared >= need and not re.search(re.escape(qkey(q)), scene_txt, re.I):
                    key = (i, sent)
                    if key not in seen: seen.add(key); out.append((i, t, sent, q))
    return out


PLACES = {'indoors': [r'\broom\b', r'\brooms\b', r'\bindoors?\b', r'\binside\b', r'living room', r'bedroom', r'kitchen', r'\boffice\b', r'\bdesk\b', r'\bstudy\b', r'\bsofa\b', r'\bcouch\b', r'\bat home\b',
                         '房间', '屋里', '室内', '家里', '客厅', '卧室', '书房', '办公室', '书桌', '沙发'],
          'outdoors': [r'\boutdoors?\b', r'\boutside\b', r'open air', r'\bcamp', r'\btent\b', r'\bgarden\b', r'\briver', r'\bforest\b', r'\bbeach\b', r'\bmountain', r'\bpark\b', r'\btrail\b',
                       '户外', '室外', '露营', '帐篷', '野外', '河边', '森林', '山间', '花园', '海边']}
WORD2DIGIT = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10', 'twelve': '12',
              'fifteen': '15', 'twenty': '20', 'thirty': '30', 'forty': '40', 'fifty': '50', 'sixty': '60', 'hundred': '100'}
NUMWORD_UNIT = r'\b(?:one|two|three|four|five|six|seven|eight|nine|ten|twelve|fifteen|twenty|thirty|forty|fifty|sixty|hundred)[- ](?:hours?|minutes?|days?|weeks?|months?|years?|millilit\w*|lit(?:re|er)s?|decibels?|watts?|percent|square)\b'
ZH_NUM_UNIT = r'[一二三四五六七八九十百千两]+(?:个)?(?:小时|分钟|毫升|升|分贝|瓦|平方|个月|年保修)'
SPEC_TERMS = [[r'battery', '电池'], [r'run ?time', '续航'], [r'\bml\b', r'millilit', '毫升'], [r'\blit(?:re|er)s?\b', r'\b\d+(?:\.\d+)? ?l\b', r'[\d一二三四五六七八九十两]\s*升'],
              [r'\bdb\b', r'decibel', '分贝'], [r'whisper', r'\bsilent', r'noiseless', '静音'], [r'coverage', '覆盖面积'], [r'square (?:feet|met)', r'm²', r'sq\.? ?ft', '平方'],
              [r'ultrasonic', '超声波'], [r'\bbpa\b'], [r'auto[- ]?(?:shut|off)', '自动断电'], [r'\btimer\b', '定时'], [r'rechargeable', '可充电'], [r'\busb'],
              [r'bluetooth', '蓝牙'], [r'waterproof', '防水'], [r'\bip[x\d]\d'], [r'certified', '认证'], [r'\bfda\b'], [r'clinically'], [r'antibacterial', '抗菌'],
              [r'\bhepa\b'], [r'warranty', '保修']]


def zh_num(s):
    """四十分钟 → '40', 十二 → '12', 三百 → '300' (simple Chinese numerals, for matching docs that use digits)."""
    d = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    m = re.match(r'[一二三四五六七八九十百千两零]+', s)
    if not m: return s
    total, cur = 0, 0
    for ch in m.group(0):
        if ch in d: cur = d[ch]
        elif ch == '十': total += (cur or 1) * 10; cur = 0
        elif ch == '百': total += (cur or 1) * 100; cur = 0
        elif ch == '千': total += (cur or 1) * 1000; cur = 0
    return str(total + cur)


def section(md, n):
    m = re.search(rf'^##\s+{n}\..*?(?=^##\s+\d+\.|\Z)', md, re.M | re.S)
    return m.group(0) if m else ''


def field(md, label):
    m = re.search(rf'{label}[^:\n]*:\s*(.+)', md)
    return m.group(1).strip() if m else ''


MINSTOP = set('a an the and or but of to in on at for with by from as is are be it its this that your you we our i my'.split())


def overlap(a, b, stop=STOP):
    A = {stem(w) for w in words(a) if w.lower() not in stop}
    B = {stem(w) for w in words(b) if w.lower() not in stop}
    return len(A & B) / max(1, min(len(A), len(B)))


if len(sys.argv) < 2: sys.exit(__doc__)
tpath = Path(sys.argv[1])
md = tpath.read_text()
for n in range(10):
    if not re.search(rf'^##\s+{n}\.', md, re.M): err(f'section {n} missing', 'keep every heading of templates/treatment.template.md')
left = re.findall(r'<write:[^>]*>', md)
if left: err(f'{len(left)} unfinished field(s), e.g. {left[0]}', 'each role writes its section (references/crew.md); replace every <write: …>')
if '{{' in md: err('template placeholders {{…}} left', 'regenerate with autofilm.py or fill them by hand')
concepts = {}
for c in 'ABC':
    m = re.search(rf'Concept {c}:\s*(\S.*)', md)
    if not m: err(f'Concept {c} missing', 'the creative director writes three genuinely different concepts')
    else: concepts[c] = m.group(1)
for x, y in (('A', 'B'), ('A', 'C'), ('B', 'C')):
    if x in concepts and y in concepts and overlap(concepts[x], concepts[y]) > 0.6:
        err(f'Concept {x} and {y} are one idea in two wordings', 'three DIFFERENT ideas: change the opening image and the angle, not the words (crew.md §3)')
ch = re.search(r'Chosen[^:]*:\s*([ABC])\b(.{12,})', md)
if not ch: err('no chosen concept with a reason', 'write "Chosen · 选定: B — because …"')
if not re.search(r'Hook \(0–3 s\)[^:]*:\s*\S.{10,}', md): err('hook for the first 3 seconds missing', 'say what we see and hear in seconds 0–3')
if not re.search(r'Hero moment[^:]*:\s*\S.{10,}', md): err('hero moment missing', 'name the one image the audience remembers')
tag = re.search(r'Tagline[^:]*:\s*(.+)', md)
tag_zh = tag_en = None
if tag:
    line = tag.group(1)
    zh = re.findall(r'[一-鿿][一-鿿，、·\s]*', line)
    tag_zh = max(zh, key=len).strip() if zh else None
    en = re.sub(r'[　-鿿＀-￯/|·—-]+', ' ', line).strip()
    tag_en = en or None
    if tag_zh and zhlen(tag_zh) > 12: err(f'Chinese tagline {zhlen(tag_zh)} 字', '≤ 12 汉字')
    if tag_en and len(re.findall(r"[A-Za-z']+", tag_en)) > 8: err(f'English tagline {len(tag_en.split())} words', '≤ 8 words')
else:
    err('tagline missing', 'the copywriter writes one tagline in zh and en')
CRIT = ['One idea', 'Hook', 'Specific', 'Image', 'Restraint', 'Rhythm', 'Hero', 'ending']
rows = re.findall(r'^\|\s*([^|]+?)\s*\|\s*([1-5])\s*\|', md, re.M)
scores = {}
for label, sc in rows:
    key = next((c for c in CRIT if c.lower() in label.lower()), None)
    if key: scores[key] = int(sc)
vals = list(scores.values())
if len(vals) < 8: err(f'taste review has {len(vals)} of 8 scores', 'score all eight criteria 1–5 honestly')
elif sum(vals) / len(vals) < 4 or min(vals) < 3:
    err(f'taste review average {sum(vals) / len(vals):.1f}, lowest {min(vals)}', 'redo the weakest part you can change (hook, a calm beat, a callback ending, the hero image) and re-score — up to three rounds; '
        'never inflate, never stop here. Image quality scores the choice and staging, not the source: placeholder limits go in §1 Gaps and the report')

if len(sys.argv) > 2:
    fpath = Path(sys.argv[2])
    spec = json.load(open(fpath))
    try:   # "rect": "@panel name" → the exact box (scripts/director.py); unresolved names are make_film's errors to report
        import director as _DIR
        _DIR.resolve_rects(spec, fpath.resolve().parent)
        for sc in spec.get('scenes', []):
            for p_ in sc.get('points', []) or []:
                if not isinstance(p_.get('rect'), (list, type(None))): p_.pop('rect', None)
    except Exception:
        pass
    todo = [p for p, v in lint_copy.walk(spec) if 'TODO' in v]
    if todo: err(f'film.json still has {len(todo)} TODO(s), e.g. {todo[0]}', 'write them from the treatment (copywriter)')
    b = spec.get('brand', {})
    if tag_en and b.get('taglineEn') and tag_en.lower().split()[:3] != b['taglineEn'].lower().split()[:3]:
        err('tagline in film.json differs from the treatment', 'use the treatment tagline in brand.taglineEn / taglineZh')
    for p, prob, fix in lint_copy.lint(spec):
        (err if prob.startswith(('cliché', '空话')) else warn)(f'copy {p}: {prob}', fix)
    vg = lint_copy.vague(spec)
    if len(vg) > 2:
        err(f'{len(vg)} vague words in the copy ({", ".join(sorted({w for _, w in vg})[:6])})', 'each one could sell any product — replace it with the noun or number it stands for')

    # the docs: what is true about this product
    base = fpath.parent
    mats = spec.get('materials') or (str(Path(b['logo']).parent) if b.get('logo') else None)
    docs = ''
    if mats and (base / mats).is_dir():
        import genres
        docs = genres.read_docs(base / mats)
    for bp in (base / 'brief.json', (base / mats / 'brief.json') if mats else None):
        if bp and bp.exists():
            docs += ' ' + json.dumps({k: v for k, v in json.load(open(bp)).items() if not k.startswith('_')}, ensure_ascii=False)
    vocab = concrete_vocab(docs, b.get('name', ''))
    # with no user docs, what the images visibly show (§5 "Each image shows", written by the art director) is the source
    # for specificity — never for numbers or specs, which still need the user's docs (below)
    visible = ' '.join(m.group(1) for m in re.finditer(r'`[^`]+\.(?:jpe?g|png|webp|webm|mp4|mov)`\s*(?:→|->|=|:)\s*([^\n]+)', section(md, 5), re.I))
    visible += ' ' + field(section(md, 2), 'Proof')   # the strategist's proof; with no docs it lists what the materials visibly show
    vocab |= concrete_vocab(visible, b.get('name', ''))

    # truth: numbers and spec terms need a source the USER supplied (text in the materials folder) — not file names, not an
    # agent-written brief. With no such text, the film may only claim what the materials show (a handle, mist, a glow, a place).
    truth = ''
    if mats and (base / mats).is_dir():
        for tp in sorted((base / mats).rglob('*')):
            if tp.is_file() and tp.suffix.lower() in ('.md', '.txt', '.json', '.csv', '.html') and tp.stat().st_size < 400000:
                truth += ' ' + tp.read_text(errors='ignore')
    tlow = truth.lower()
    copy_items = [(p_, v) for p_, v in lint_copy.walk(spec)] + [(f'brand.chips[{k}]', c) for k, c in enumerate(b.get('chips') or []) if isinstance(c, str)]
    copy_items += [(f'scenes[{i}].stats[{k}]', f"{st.get('value', '')}{st.get('suffix', '')} {st.get('en', '')} {st.get('zh', '')}") for i, sc in enumerate(spec.get('scenes', [])) for k, st in enumerate(sc.get('stats', []))]
    copy_items += [(f'scenes[{i}].data[{k}]', f"{x.get('value', '')}{sc.get('unit', '')} {x.get('label', '')}") for i, sc in enumerate(spec.get('scenes', [])) if sc.get('type') == 'chart' for k, x in enumerate(sc.get('data', [])) if isinstance(x, dict)]
    name_nums = set(re.findall(r'\d+', f"{b.get('name', '')} {b.get('nameAccent', '')}"))
    unsourced = []
    sec8 = section(md, 8)
    mat_stems = [tp.stem for tp in (base / mats).iterdir()] if mats and (base / mats).is_dir() else []
    def screen_sourced(n):   # §8 names the material file the figure is read from ("95% CI → km.png")
        return any(n in ln and any(st and st in ln for st in mat_stems) for ln in sec8.splitlines())
    for path_, v in copy_items:
        if '.chapter' in path_: continue   # chapter numbers are labels, not claims
        nums = [n for n in re.findall(r'(?<![\w.])\d+(?:[.,]\d+)?', v) if n not in name_nums]
        nums += [m.group(0) for m in re.finditer(NUMWORD_UNIT, v, re.I)] + re.findall(ZH_NUM_UNIT, v)
        for n in nums:
            key = n if n[0].isdigit() else (zh_num(n) if re.match(r'[一二三四五六七八九十百千两]', n) else re.split(r'[- ]', n.lower())[0])
            if key not in tlow and not (key in WORD2DIGIT and WORD2DIGIT[key] in tlow) and not screen_sourced(n) and not screen_sourced(key):
                unsourced.append((path_, n, 'number'))
        for group in SPEC_TERMS:
            m = next((m for t in group if (m := re.search(t, v, re.I))), None)
            if m and not any(re.search(t, truth, re.I) for t in group) and not screen_sourced(m.group(0)):
                unsourced.append((path_, m.group(0), 'spec'))
    for path_, n, kind in unsourced[:8]:
        err(f'{path_}: the {kind} "{n}" has no source in the user\'s docs' + ('' if truth.strip() else ' (there are no docs)'),
            'say only what the docs or the materials show; ask the user for the spec sheet, and list it in §1 Gaps. An invented spec is a false claim')
    if not truth.strip():
        warn('no user docs (README, brief, spec sheet) in the materials', 'claim only what the images and clips show, and list in §1 Gaps what the user must supply (name, specs, contacts)')

    scenes = spec.get('scenes', [])
    spoken = [(i, sc['type'], s) for i, sc in enumerate(scenes) for s in sc.get('say', []) if s.get('en')]
    body = [(i, t, s) for i, t, s in spoken if s.get('id') not in ('tagline', 'motto')]
    caps = {}

    # script: the voice-over lives in the treatment first, then in film.json
    vo = section(md, 4)
    m = re.search(r'Voice-over[^:\n]*:(.*?)(?=^- On-screen|^- Banned|\Z)', vo, re.M | re.S)
    vo_txt = m.group(1) if m else ''
    vo_lines = [l for l in re.split(r'(?<=[.?。？])\s+|→|\n', vo_txt) if len(words(l)) >= 2]
    if spoken and len(vo_lines) < max(2, len(spoken) // 2):
        err('§4 Voice-over is not a script', 'the copywriter writes every spoken line there, in film order: beat → "line" (the film.json say lines come from it)')
    missing = [s['en'] for _, _, s in spoken if max((overlap(s['en'], l) for l in vo_lines), default=0) < 0.5]
    if vo_lines and missing:
        err(f'{len(missing)} spoken line(s) in film.json are not in the treatment, e.g. "{missing[0][:60]}"', 'the treatment is the script: put the line in §4 (or take it out of film.json)')
    if not spoken:
        caps['Hook'] = 3; caps['ending'] = 3
        warn('no spoken lines at all', 'a film without a voice leans on captions — fine for sound-off, but say why in §1')

    # anchors: the three lines that carry the concept must be the film's cover, finale and end-card lines
    for label, idx in (('Hook line', 0), ('Hero line', 'finale'), ('Last line', -1)):
        want = field(section(md, 3), label)
        if not want or not scenes: continue
        sc = scenes[idx] if isinstance(idx, int) else next((x for x in scenes if x['type'] == 'finale'), None)
        got = ' '.join(x['en'] for x in (sc or {}).get('say', []))
        if sc is None or overlap(want, got, MINSTOP) < 0.5:
            err(f'{label} "{want[:50]}" is not what the {(sc or {}).get("type", idx)} scene says ("{got[:50]}")', 'the anchor lines are written first and used as written: put them in the cover / finale / endcard "say" (or change the treatment)')

    # specificity
    # deliberate choices: a crew may break a taste default on purpose ("- Deliberate · 刻意: Rhythm — three close-ups in a
    # row: the open is a macro sequence"). The named taste check then advises instead of blocking. Honesty never bends:
    # numbers, specs, qualifiers, places, TODOs and the form stay hard.
    TASTE = {'one idea': 'One idea', 'idea': 'One idea', 'hook': 'Hook', 'specific': 'Specific', 'copy': 'Specific', 'image': 'Image',
             'restraint': 'Restraint', 'rhythm': 'Rhythm', 'hero': 'Hero', 'ending': 'ending', 'memorable ending': 'ending'}
    deliberate = {}
    for ln in re.findall(r'Deliberate[^:\n]*:\s*([^\n]+)', md):
        for part in re.split(r'[;；]', ln):
            m_ = re.match(r'\s*([A-Za-z ]+?)\s*[—–:-]\s*(.+)', part)
            if not m_: continue
            key = TASTE.get(m_.group(1).strip().lower())
            reason = m_.group(2).strip()
            if key and (len(reason.split()) >= 6 or len(re.findall(r'[\u4e00-\u9fff]', reason)) >= 10): deliberate[key] = reason
    soft = lambda key: (lambda m, fix: warn(f'{m} — kept on purpose ({key}: "{deliberate[key][:60]}")', fix)) if key in deliberate else err
    if docs and body:
        vague_lines = [(t, s['en']) for _, t, s in body if not is_concrete(s['en'], vocab)]
        ratio = 1 - len(vague_lines) / len(body)
        proof = [(t, l) for t, l in vague_lines if t in ('feature', 'hero', 'numbers', 'compare', 'phone', 'clip', 'carousel')]
        for t, l in proof:
            soft('Specific')(f'{t} line has no fact from the docs: "{l[:70]}"', 'a proof beat names something real — a number, a part, a material, a place, a feature by name (from the README/brief)')
        if ratio < 2 / 3:
            soft('Specific')(f'only {ratio:.0%} of the spoken lines carry a concrete fact (need ≥ 67%)', 'replace mood lines with what is true: e.g. "Each glaze finds its own way through the kiln", not "Discover a new way to enjoy your morning"')
        caps['Specific'] = 5 if ratio >= 0.85 else (4 if ratio >= 0.75 else 3)
        if vague_lines and not proof: warn(f'{len(vague_lines)} line(s) without a fact, e.g. "{vague_lines[0][1][:60]}"', 'fine for one mood line; more reads as filler')
    elif not docs:
        warn('no docs found to check facts against', 'set "materials": "<folder with the README/brief>" in film.json (autofilm writes it)')

    # qualifiers: a claim the docs limit (edition, plan, beta, platform, region, "planned") must carry that limit in its scene
    if docs:
        reviewed = section(md, 8)
        for i, phrase, sent, q in omitted_qualifiers(spec, docs):
            if re.search(re.escape(qkey(q)), reviewed, re.I) and re.search(r'not affected|does not apply|不受影响|不适用', reviewed, re.I):
                warn(f'scene {i}: qualifier "{q}" reviewed in §8 as not applying to "{phrase[:50]}"', 'keep the reason in §8 Qualifiers')
                continue
            err(f'scene {i} says "{phrase[:60]}" without the docs\' qualifier "{q}" ("{sent[:90]}")',
                f'brand guardian: say the limit in that scene (put "{q}" in the line, the caption or a chip), or drop the claim. '
                'An omitted qualifier is a false claim even when every word is true')

    # idea: the chosen concept must reach the film
    copy_all = ' '.join(v for p, v in lint_copy.walk(spec))
    if ch and ch.group(1) in concepts:
        cname = re.split(r'\s[—–:-]\s|:', concepts[ch.group(1)])[0]
        key = [stem(w) for w in words(cname) if w.lower() not in STOP and len(w) > 2]
        if key and not any(k in {stem(w) for w in words(copy_all)} for k in key):
            soft('One idea')(f'the chosen concept "{cname.strip()}" never reaches the film', 'the idea must be on screen: put its key image or words in the hook, the hero line or the tagline — otherwise it is a feature list')
            caps['One idea'] = 3
    prop = field(section(md, 2), 'Single-minded proposition')
    if prop and tag_en and overlap(prop, tag_en + ' ' + (b.get('motto') or [''])[-1]) == 0 and overlap(prop, ' '.join(s['en'] for _, _, s in spoken[-2:])) == 0:
        warn('the ending does not echo the proposition', 'the tagline or the last line should say the single-minded proposition in other words')

    # cross-checks that cap self-scores
    types = [sc['type'] for sc in scenes]
    run_ = max((len(list(g)) for _, g in __import__('itertools').groupby(types)), default=0)
    feats = [sc for sc in scenes if sc['type'] == 'feature']
    if run_ >= 3 and len({sc.get('bars') for sc in feats}) <= 1:
        caps['Rhythm'] = 3
        warn(f'{run_} scenes of the same type in a row at the same length', 'breathe: put a calm beat (photo, detail, statement, a scene without voice) between them, or vary the bars')
    if body and all(sc.get('say') for sc in scenes if sc['type'] not in ('cover', 'endcard', 'finale')):
        caps['Rhythm'] = min(caps.get('Rhythm', 5), 4)
    c0 = scenes[0] if scenes else {}
    if c0.get('type') == 'cover' and c0.get('frame') == 'photo' and c0.get('media') and not c0.get('focus'):
        caps['Hook'] = min(caps.get('Hook', 5), 3)
        warn('the cold open is one still frame', 'give the cover a "focus" (the subject: scripts/subject_grid.py) — the open starts on that detail and pulls back to reveal the place')
    # place: the copy over an image names the same kind of place the image shows (no "room" over a tent)
    shows = {m.group(1): m.group(2) for m in re.finditer(r'`([^`]+\.(?:jpe?g|png|webp|webm|mp4|mov))`\s*(?:→|->|=|:)\s*([^\n]+)', section(md, 5), re.I)}
    def places(t):
        t = t.lower()
        return {k for k, ws in PLACES.items() if any(re.search(w, t) for w in ws)}
    for i, sc in enumerate(scenes):
        m = sc.get('media') if isinstance(sc.get('media'), str) else sc.get('image')
        if not isinstance(m, str) or Path(m).name not in shows: continue
        seen = places(shows[Path(m).name])
        copy_here = ' '.join([x.get('en', '') + ' ' + x.get('zh', '') for x in sc.get('say', [])] + [(sc.get('title') or {}).get('en', ''), (sc.get('title') or {}).get('zh', '')])
        said = places(copy_here)
        if seen and said and not (said & seen):
            err(f'scenes[{i}] says {"/".join(sorted(said))} over {Path(m).name}, which shows {"/".join(sorted(seen))} ("{shows[Path(m).name][:50]}")',
                'name what is in the frame: change the line, or put it over an image of that place')
    if c0.get('type') == 'cover' and (not c0.get('media') or (c0.get('open') is False and c0.get('name') is not False)):
        caps['Hook'] = min(caps.get('Hook', 5), 3)
        warn('the film opens on the logo', 'the first seconds are the product truth: give the cover an image (a cold open) and let the hook line land before the name')
    same = [i for i in range(1, len(scenes)) if scenes[i]['type'] in ('feature', 'photo', 'detail') and scenes[i]['type'] == scenes[i - 1]['type']]
    if same:
        caps['Rhythm'] = min(caps.get('Rhythm', 5), 4)
        warn(f'scenes[{same[0]}]: two {scenes[same[0]]["type"]} beats in a row share one shape', 'vary the proof (zoomed detail, one number, a clip, before → after) or put a breath between them')
    detours = [sc['type'] for sc in scenes if sc['type'] in ('clip', 'phone') and not sc.get('say')]
    if detours:
        caps['One idea'] = min(caps.get('One idea', 5), 4)
        warn(f'a silent {detours[0]} scene', 'give it one line that serves the idea — or cut it')
    specs = [s['en'] for _, _, s in spoken if lint_copy.spec_list(s['en'])]
    if specs:
        caps['Specific'] = min(caps.get('Specific', 5), 3 if len(specs) >= 2 else 4)
        warn(f'{len(specs)} spoken line(s) read as a spec sheet, e.g. "{specs[0][:60]}"', 'rewrite each as one benefit (what it means for the viewer); keep specs for points or the end card')
    silent_tex = [i for i, sc in enumerate(scenes) if sc['type'] == 'detail' and not sc.get('say') and not any(c.get('zh') or c.get('en') for c in sc.get('crops', []))]
    if silent_tex:
        caps['Rhythm'] = min(caps.get('Rhythm', 5), 3)
        warn(f'scenes[{silent_tex[0]}] is a silent texture with no purpose', 'give the detail a line or a labelled crop (what are we looking at, and why it matters) — or cut it')
    # hero ≥ 4 needs a staged treatment AND a callback to the hook (the same image transformed, or the hook's words answered)
    fin = next((sc for sc in scenes if sc['type'] == 'finale'), None)
    if fin:
        hook_media = c0.get('media') if c0.get('type') == 'cover' else None
        img_cb = bool(hook_media) and hook_media in (fin.get('image'), fin.get('backdrop'))
        hero_say = ' '.join(x['en'] for sc in scenes if sc['type'] in ('finale', 'hero') for x in sc.get('say', []))
        hook_line = next((x['en'] for sc in scenes[:1] for x in sc.get('say', [])), '')
        word_cb = bool(hook_line) and overlap(hook_line, hero_say + ' ' + (tag_en or ''), MINSTOP) > 0
        staged = fin.get('hero') in ('result', 'rise', 'stack') or fin.get('image') or any(sc['type'] == 'hero' for sc in scenes)
        if not (staged and (img_cb or word_cb)):
            caps['Hero'] = min(caps.get('Hero', 5), 3)
            warn('the hero does not pay off the hook', 'stage the finale (a hero treatment or a bookend image) and call back to the hook: the same image transformed, or the hook line answered in the hero line')
    if fin and not (fin.get('hero') in ('result', 'rise', 'stack') or fin.get('image')) and not any(sc['type'] == 'hero' for sc in scenes):
        caps['Hero'] = min(caps.get('Hero', 5), 3)
        warn('the hero moment is the default image wall', 'give the finale a hero treatment: "hero": "result" | "rise" | "stack" for screens, or "image" (a bookend photo)')
    holds = [sc['type'] for sc in scenes if not sc.get('say') and isinstance(sc.get('bars'), (int, float)) and
             ((sc['type'] == 'detail' and sc['bars'] > 2) or (sc['type'] in ('hero', 'photo', 'feature') and sc['bars'] > 3))]
    holds += [sc['type'] for sc in scenes if sc['type'] == 'hero' and isinstance(sc.get('bars'), (int, float)) and sc['bars'] > 3 and not isinstance(sc.get('media'), list)]
    if holds:
        caps['Rhythm'] = min(caps.get('Rhythm', 5), 3)
        warn(f'a long hold on one image ({holds[0]})', 'silent or single-image beats over ~6 s read as empty: 2–3 bars, or give the beat a line')
    if c0.get('type') == 'cover' and isinstance(c0.get('media'), str) and re.search(r'home|welcome|start[-_ ]?screen|splash|login|sign.?in|settings?|empty|blank|首页|欢迎|设置', Path(c0['media']).stem, re.I):
        caps['Hook'] = min(caps.get('Hook', 5), 3)
        warn('the cold open is a home / start screen', 'a home screen shows nothing happening: open on the best real output (a result, a plot, the answer), as autofilm chose, and let the hook line name the tension')
    if scenes and scenes[0]['type'] == 'cover' and isinstance(scenes[0].get('media'), str) and re.search(r'detail|texture|macro|grain|close', scenes[0]['media'], re.I):
        caps['Hook'] = min(caps.get('Hook', 5), 3)
        warn('the cold open is a texture', 'open on an image with a subject; textures belong in the detail beat')
    media = [m for sc in scenes if sc['type'] not in ('finale', 'cover') for m in ([sc['media']] if isinstance(sc.get('media'), str) else sc.get('media') or [])]
    dup = {m for m in media if media.count(m) > 1}
    if dup:
        caps['Image'] = 3
        warn(f'the same image carries two beats: {sorted(dup)[0]}', 'one image, one beat — use another material, or drop the weaker beat')
    for i, sc in enumerate(scenes):
        if sc['type'] == 'feature' and sc.get('frame') != 'photo' and sc.get('points') and not any(p.get('rect') for p in sc['points']) and \
                not (isinstance(sc.get('media'), str) and (base / sc['media']).exists() and __import__('suggest_rects').is_chart(base / sc['media'], sc.get('base'))):
            caps['Image'] = min(caps.get('Image', 5), 3)
            warn(f'scenes[{i}] feature on a screen has no highlight rects', f'python3 scripts/suggest_rects.py {sc.get("media")} --preview . → copy the rect of the region each point talks about')
            break
    big = [i for i, sc in enumerate(scenes) for p in sc.get('points', []) if p.get('rect') and
           p['rect'][2] * p['rect'][3] > 0.3 * (sc.get('base') or [1920, 1080])[0] * (sc.get('base') or [1920, 1080])[1]]
    if big:
        caps['Image'] = min(caps.get('Image', 5), 3)
        warn(f'scenes[{big[0]}]: a highlight box covers most of the screen', 'box only the region the point names (suggest_rects.py --preview); a box around everything highlights nothing')
    hero_hits = [sc for sc in scenes if sc.get('hit') == 'hero']
    if len(hero_hits) > 1: caps['Restraint'] = 3; soft('Restraint')(f'{len(hero_hits)} scenes marked "hit": "hero"', 'exactly one hero moment (references/director.md §5)')
    cover_line = next((s['en'] for sc in scenes[:1] for s in sc.get('say', [])), '')
    end_line = ' '.join(s['en'] for sc in scenes[-1:] for s in sc.get('say', [])) + ' ' + ' '.join((b.get('motto') or [])[-1:])
    if cover_line and end_line.strip() and overlap(cover_line, end_line, MINSTOP) == 0 and overlap(tag_en or '', end_line, MINSTOP) == 0:
        caps['ending'] = min(caps.get('ending', 5), 3)
        warn('the ending does not call back to the opening or the tagline', 'a callback: let the last line echo a word or image of the first (crew.md §3)')
    if end_line.strip() and is_concrete(end_line, set()) and re.search(r'\d|open|book|available|from', end_line, re.I) and not overlap(tag_en or '', end_line):
        caps['ending'] = min(caps.get('ending', 5), 3)
        warn('the last line is logistics (dates, prices, booking)', 'logistics go in the contacts; the last line is the one the audience keeps')
    for k, cap in caps.items():
        if k in scores and scores[k] > cap:
            soft(k)(f'taste score "{k}" = {scores[k]}, but the film shows at most {cap}', 'fix the film (copy, images, rhythm) until it earns the score — or lower the score and improve another part. Never inflate.')

print('\n'.join(warns_))
print('\n'.join(errs) if errs else 'treatment OK — the crew signed off; build the film')
sys.exit(1 if errs else 0)
