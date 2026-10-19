"""Check the crew's treatment before building: complete, specific, consistent with film.json, and above the taste bar.

Usage: python check_treatment.py treatment.md [film.json]
Prints ERROR/FIX lines like make_film.py; exit 1 if anything must be fixed.
Checks
  - every section 0–9 present, no "<write:" or "{{" left
  - three concepts (A, B, C) and a "Chosen" line naming one of them, with a reason
  - a hook for the first 3 seconds and a hero moment
  - tagline: Chinese ≤ 12 characters, English ≤ 8 words
  - taste scores: all 1–5, average ≥ 4.0, none below 3
  - film.json (if given): no TODO left, its tagline matches the treatment's, its copy passes lint_copy
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_copy  # noqa: E402

errs = []
def err(m, fix): errs.append(f'ERROR {m}\n  FIX: {fix}')
zhlen = lint_copy.zhlen

if len(sys.argv) < 2: sys.exit(__doc__)
md = Path(sys.argv[1]).read_text()
for n in range(10):
    if not re.search(rf'^##\s+{n}\.', md, re.M): err(f'section {n} missing', 'keep every heading of templates/treatment.template.md')
left = re.findall(r'<write:[^>]*>', md)
if left: err(f'{len(left)} unfinished field(s), e.g. {left[0]}', 'each role writes its section (references/crew.md); replace every <write: …>')
if '{{' in md: err('template placeholders {{…}} left', 'regenerate with autofilm.py or fill them by hand')
for c in 'ABC':
    if not re.search(rf'Concept {c}:\s*\S', md): err(f'Concept {c} missing', 'the creative director writes three genuinely different concepts')
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
scores = [int(x) for x in re.findall(r'^\|[^|]+\|\s*([1-5])\s*\|', md, re.M)]
if len(scores) < 8: err(f'taste review has {len(scores)} of 8 scores', 'score all eight criteria 1–5 honestly')
elif sum(scores) / len(scores) < 4 or min(scores) < 3:
    err(f'taste review average {sum(scores) / len(scores):.1f}, lowest {min(scores)}', 'improve the weakest criteria (change the concept, the copy or the images) and re-score — do not inflate scores')
if len(sys.argv) > 2:
    spec = json.load(open(sys.argv[2]))
    todo = [p for p, v in lint_copy.walk(spec) if 'TODO' in v]
    if todo: err(f'film.json still has {len(todo)} TODO(s), e.g. {todo[0]}', 'write them from the treatment (copywriter)')
    b = spec.get('brand', {})
    if tag_en and b.get('taglineEn') and tag_en.lower().split()[:3] != b['taglineEn'].lower().split()[:3]:
        err('tagline in film.json differs from the treatment', 'use the treatment tagline in brand.taglineEn / taglineZh')
    warnsl = []
    for p, prob, fix in lint_copy.lint(spec):
        (err if prob.startswith(('cliché', '空话')) else lambda m, f: warnsl.append(f'WARN  {m}\n  FIX: {f}'))(f'copy {p}: {prob}', fix)
    if warnsl: print('\n'.join(warnsl))
print('\n'.join(errs) if errs else 'treatment OK — the crew signed off; build the film')
sys.exit(1 if errs else 0)
