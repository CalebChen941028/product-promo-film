"""Recommend a visual style + motion language from the material's THEME (brief text) and the MUSIC (tempo/energy).

Usage: python recommend_style.py brief.json [--grid grid.json] [--text "extra description of the product"]
Prints the top 3 pairs with reasons and the two lines to paste into film.json. Confirm the choice with the user.
Rules of thumb it encodes:
  science / data / research / finance / medical-research → precision-data (+ paper-academic or midnight-tech)
  developer / security / infra / AI-agent / gaming       → kinetic-launch (+ neon-cyber or midnight-tech)
  B2B platform / enterprise / analytics                  → cinematic-3d  (+ midnight-tech or keynote-light)
  consumer / creator / social / kids / lifestyle         → playful-pop   (+ aurora-glass or keynote-light)
  care / wellbeing / education / mission / non-profit    → gentle-story  (+ keynote-light or paper-academic)
  brand manifesto / opinion / launch teaser / editorial  → editorial-type (+ editorial-mono)
  music: ≥ 128 BPM or very punchy → favour kinetic/playful; ≤ 95 BPM or soft → favour gentle/precision.
"""
import argparse
import json
import re

ap = argparse.ArgumentParser()
ap.add_argument('brief'); ap.add_argument('--grid'); ap.add_argument('--text', default='')
a = ap.parse_args()
b = json.load(open(a.brief))
b = {k: v for k, v in b.items() if k not in ('contacts', 'voice', 'music', 'style', '_how')}  # theme words only
text = (json.dumps(b, ensure_ascii=False) + ' ' + a.text).lower()

THEMES = {
    'precision-data': ['统计', '数据', '科研', '研究', '分析', '医学', '临床', '论文', '金融', '量化', '实验', '生物', 'statistic', 'data', 'research', 'analysis', 'analytics', 'science', 'scientific', 'clinical', 'finance', 'lab', 'paper', 'journal'],
    'kinetic-launch': ['开发者工具', '代码', '安全', '运维', '云原生', '部署', '智能体', '游戏', '极速', 'developer tool', 'coding', 'devops', 'security', 'infra', 'cloud', 'api', 'agent', 'gaming', 'launch', 'fast', 'cli'],
    'cinematic-3d': ['平台', '企业', '工作台', '系统', '解决方案', 'saas', 'platform', 'enterprise', 'workbench', 'workspace', 'dashboard', 'b2b', 'suite', 'professional'],
    'playful-pop': ['社交', '创作', '学生', '儿童', '生活', '好玩', '可爱', '短视频', '社区', 'social', 'creator', 'kids', 'student', 'lifestyle', 'fun', 'community', 'consumer', 'emoji', 'friends'],
    'gentle-story': ['健康', '关怀', '教育', '公益', '心理', '陪伴', '患者', '温暖', '使命', 'health', 'care', 'wellbeing', 'education', 'learning', 'mission', 'nonprofit', 'patient', 'mindful', 'human'],
    'editorial-type': ['宣言', '理念', '品牌', '观点', '杂志', '态度', '信条', 'manifesto', 'brand', 'belief', 'opinion', 'editorial', 'magazine', 'statement', 'vision', 'motto'],
}
STYLE_FOR = {
    'precision-data': ['paper-academic', 'midnight-tech', 'keynote-light'], 'kinetic-launch': ['neon-cyber', 'midnight-tech', 'editorial-mono'],
    'cinematic-3d': ['midnight-tech', 'keynote-light', 'aurora-glass'], 'playful-pop': ['aurora-glass', 'keynote-light', 'neon-cyber'],
    'gentle-story': ['keynote-light', 'paper-academic', 'aurora-glass'], 'editorial-type': ['editorial-mono', 'paper-academic', 'keynote-light'],
}
score, why = {}, {}
for m, kws in THEMES.items():
    hits = [k for k in kws if re.search(re.escape(k), text)]
    score[m] = len(hits); why[m] = hits[:6]
if a.grid:
    g = json.load(open(a.grid)); bpm = g.get('bpm', 110)
    hi = [x['hi'] for x in g.get('bars', [])]; punch = (max(hi) - sorted(hi)[len(hi) // 2]) if hi else 0
    if bpm >= 128 or punch > 0.45:
        score['kinetic-launch'] += 2; score['playful-pop'] += 1; why['kinetic-launch'].append(f'music {bpm:.0f} BPM / punchy')
    elif bpm <= 95:
        score['gentle-story'] += 2; score['precision-data'] += 1; why['gentle-story'].append(f'music {bpm:.0f} BPM / calm')
    else:
        score['cinematic-3d'] += 1; why['cinematic-3d'].append(f'music {bpm:.0f} BPM / mid-tempo')
ranked = sorted(score, key=lambda m: -score[m])
print('Recommended (confirm with the user):')
for i, m in enumerate(ranked[:3]):
    st = STYLE_FOR[m][0] if i == 0 else STYLE_FOR[m][min(i, 1)]
    print(f"{i + 1}. motion {m:15s} + style {st:15s}  score {score[m]}  because: {', '.join(why[m]) or 'default'}")
best = ranked[0]
print('\nPaste into film.json:\n  "style": "%s",\n  "motion": "%s",' % (STYLE_FOR[best][0], best))
print('Alternatives for the same motion:', ', '.join(STYLE_FOR[best][1:]))
