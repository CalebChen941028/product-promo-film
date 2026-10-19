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
SUPERLATIVE = re.compile(r"(\bthe (best|fastest|only|most \w+)\b|#1|\bnumber one\b|\bworld'?s (best|first|fastest|only)\b|\bunbeatable\b)", re.I)
zhlen = lambda s: sum(1 for ch in s or '' if '　' <= ch <= '鿿' or '＀' <= ch <= '￯')


def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            if k.startswith('_') or k in ('media', 'file', 'logo', 'type', 'style', 'motion', 'genre', 'contacts', 'chips', 'voice', 'music', 'tools', 'out', 'name', 'id', 'cinema', 'cut', 'mood'):
                continue
            yield from walk(v, f'{path}.{k}' if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f'{path}[{i}]')
    elif isinstance(o, str):
        yield path, o


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
