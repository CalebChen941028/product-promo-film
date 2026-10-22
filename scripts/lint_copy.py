"""Copy lint: the copywriter's red pen. Flags clichés, hype, unverifiable superlatives and over-long lines.

Usage: python lint_copy.py film.json [--strict]
Exit 1 with --strict when anything is flagged. make_film.py --stage check runs the same rules as warnings.

Why: premium films say one specific, true thing per beat. Generic hype ("revolutionary", "颠覆", "赋能") reads as
cheap, and nobody can check it. Replace each flagged word with what the product actually does, a number, or nothing.
"""
import argparse
import json
import re
import sys

CLICHES_EN = ['revolutionary', 'revolutionize', 'game-changing', 'game changer', 'cutting-edge', 'cutting edge', 'next-gen', 'next generation',
              'seamless', 'seamlessly', 'world-class', 'best-in-class', 'unleash', 'empower', 'synergy', 'disrupt', 'leverage', 'innovative',
              'state-of-the-art', 'ultimate', 'unparalleled', 'robust', 'paradigm', 'groundbreaking', 'one-stop', 'all-in-one solution', 'like never before',
              'redefine', 'elevate your', 'supercharge', 'magic', 'effortless', 'blazing fast']
CLICHES_ZH = ['颠覆', '赋能', '极致', '一站式', '革命性', '全方位', '打造', '黑科技', '重新定义', '无与伦比', '震撼', '史诗级', '遥遥领先', '引领', '领先的',
              '前所未有', '划时代', '最强', '顶级', '完美', '闭环', '抓手', '降本增效', '全链路', '智慧化']
# vague words: not banned, but each one is a line that could sell any product. Three or more in a film fail check_treatment.
VAGUE_EN = ['experience', 'discover', 'journey', 'unlock', 'elevate', 'transform', 'embrace', 'beautiful', 'amazing', 'perfect', 'powerful',
            'easy', 'easily', 'simple', 'simply', 'intuitive', 'solution', 'premium', 'quality', 'crafted for', 'designed for you', 'next level',
            'more than just', 'whether you', 'imagine', 'say goodbye', "in today's", 'the art of', 'your way', 'everything you need', 'built for',
            'peace of mind', 'made for you', 'reimagine', 'boost', 'enhance', 'streamline', 'stunning', 'incredible', 'unique experience']
VAGUE_ZH = ['体验', '品质', '轻松', '简单', '高效', '强大', '尽享', '开启', '专属', '匠心', '美好', '畅享', '全新', '升级', '智能', '便捷', '品味生活', '理想']
# spec-sheet phrasing: a voice-over that reads like a datasheet. One benefit per line beats four attributes.
ATTR_EN = ['dishwasher safe', 'dishwasher-safe', 'lead-free', 'bpa-free', 'food-safe', 'food safe', 'waterproof', 'water-resistant', 'microwave safe',
           'oven safe', 'eco-friendly', 'non-toxic', 'gluten-free', 'sugar-free', 'rechargeable', 'lightweight', 'portable', 'durable', 'compact']
ATTR_ZH = ['可洗碗机', '洗碗机可', '无铅', '食品级', '防水', '耐热', '便携', '轻量', '环保', '无毒', '可充电']
UNITS = re.compile(r'\d[\d.,]*\s?(ml|mm|cm|kg|g|w|kw|v|mah|wh|gb|tb|mb|hz|dpi|ppi|fps|%|°c?|nits|lm|db|毫升|毫米|厘米|克|千克|瓦)(?![a-z])', re.I)
SUPERLATIVE = re.compile(r"(\bthe (best|fastest|only|most \w+)\b|#1|\bnumber one\b|\bworld'?s (best|first|fastest|only)\b|\bunbeatable\b)", re.I)
zhlen = lambda s: sum(1 for ch in s or '' if '　' <= ch <= '鿿' or '＀' <= ch <= '￯')


MEDIA_PATH = re.compile(r'^\S+\.(?:png|jpe?g|webp|gif|webm|mp4|mov|svg)$', re.I)


def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            if k.startswith('_') or k in ('media', 'image', 'backdrop', 'materials', 'treatment', 'file', 'logo', 'type', 'style', 'motion', 'genre', 'contacts', 'chips', 'voice', 'music', 'tools', 'out', 'name', 'id', 'cinema', 'cut', 'mood', 'hero',
                                          'rect', 'focus', 'crop', 'layout', 'camera', 'palette', 'direction', 'poster', 'kind', 'unit', 'source', 'fn', 'assets', 'scripts', 'css', 'motions', 'code', 'hot', 'file', 'size', 'side', 'view'):
                continue
            if k == 'steps' and isinstance(v, str): continue   # "steps": "chapters" is an instruction, not copy
            yield from walk(v, f'{path}.{k}' if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f'{path}[{i}]')
    elif isinstance(o, str) and not MEDIA_PATH.search(o):   # a file path ("materials/01-data.png") is not copy
        yield path, o


def spec_list(s):
    """Why a line reads as a spec sheet (attribute list, a run of units, 3+ short items in a row), or None."""
    low = s.lower()
    attrs = [a for a in ATTR_EN if a in low] + [a for a in ATTR_ZH if a in s]
    if len(attrs) >= 2: return f'attribute list ({", ".join(attrs[:3])})'
    if len(UNITS.findall(s)) >= 2: return f'{len(UNITS.findall(s))} units in one line'
    segs = [x.strip(' .。') for x in re.split(r'[,，、;；/]| and | or |和|与|及', s) if x.strip(' .。')]
    if len(segs) >= 3 and sum(1 for x in segs if len(x.split()) <= 3 and zhlen(x) <= 6) >= 3: return f'{len(segs)} items in a row'
    return None


def vague(spec):
    """(path, word) for every vague word in the copy (see VAGUE_EN / VAGUE_ZH)."""
    out = []
    for path, s in walk(spec):
        low = s.lower()
        out += [(path, w) for w in VAGUE_EN if re.search(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', low)]
        out += [(path, w) for w in VAGUE_ZH if w in s]
    return out


def lint(spec):
    """Return a list of (path, problem, fix)."""
    out = []
    for path, s in walk(spec):
        low = s.lower()
        for w in CLICHES_EN:
            if re.search(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', low):
                out.append((path, f'cliché "{w}"', 'say what it actually does, or give a number'))
        for w in CLICHES_ZH:
            if w in s:
                out.append((path, f'空话 / cliché「{w}」', '换成产品具体做了什么，或一个可核实的数字'))
        m = SUPERLATIVE.search(s)
        if m and path.endswith('en'):
            out.append((path, f'superlative "{m.group(0)}"', 'only if it is provable — otherwise drop it'))
        last = path.split('.')[-1]
        if last == 'zh' and ('title' in path or 'points' in path or 'items' in path or 'panels' in path) and zhlen(s) > 12:
            out.append((path, f'on-screen label {zhlen(s)} 字', '≤ 12 汉字 for titles and labels'))
        if last == 'en' and ('title' in path or 'points' in path) and len(s) > 42:
            out.append((path, f'on-screen label {len(s)} chars', '≤ 42 characters'))
        if path.split('.')[0] != 'brand' or last in ('motto',):
            for w in [w for w in VAGUE_EN if re.search(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', low)] + [w for w in VAGUE_ZH if w in s]:
                out.append((path, f'vague "{w}"', 'name the thing itself: a noun or a number from the docs (what, how many, where)'))
        if ('say' in path or path.endswith(('title.en', 'title.zh'))) and spec_list(s):
            out.append((path, f'spec list: {spec_list(s)}', 'one benefit per line, said as what it means for the viewer; specs go to points or the end card'))
        if '!' in s or '！' in s:
            out.append((path, 'exclamation mark', 'premium copy rarely shouts — remove it'))
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('spec'); ap.add_argument('--strict', action='store_true')
    a = ap.parse_args()
    res = lint(json.load(open(a.spec)))
    for p, prob, fix in res:
        print(f'WARN  {p}: {prob}\n  FIX: {fix}')
    print(f'{len(res)} copy issue(s)' if res else 'copy OK')
    sys.exit(1 if res and a.strict else 0)
