# Treatment · 创意方案 — Quartile

> Written by the crew in `references/crew.md`, one section per role, in order. Replace every `write` field.
> `python3 scripts/check_treatment.py treatment.md film.json` must pass before `make_film.py --stage build`.
> 由 `references/crew.md` 中的各角色依次填写；替换所有 `write` 字段，检查通过后再构建。

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: Quartile
- Genre · 类型: science-data — Science, research, data analysis / 科研 / 数据分析 / 统计
- Look · 风格: paper-academic · Motion · 动效: precision-data · Arc · 叙事结构: problem-solution
- Music · 音乐: composed: minimal-electronic ~104 BPM (original, royalty-free)
- Materials · 素材: desktop 4, logo 1, phone 1, text 1, ui 5, video 1
- Target length · 目标时长: ~100 s
- Tone for this genre · 本类型的语气: exact, modest, evidence first; numbers must be checkable
- Study first · 先读: `templates/golden/problem-solution.json` (a top film in this arc, every scene with a `_why`) and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: Desktop statistics for clinical researchers. Load a spreadsheet, pick an analysis, get a table and a figure you can put in a paper. · Survival analysis: Kaplan–Meier curves with log-rank test and numbers at risk · Diagnostic accuracy: ROC curves with AUC and 95% confidence interval · Meta-analysis: forest plots with fixed and random effects and I² heterogeneity · Every result exports as a reproducible R script, so a reviewer can rerun it · Figures export at 300 or 600 DPI · Runs on your own Mac or Windows PC; your data never leaves the computer · A phone companion lists your saved analyses

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Clinical researchers and the reviewers they answer to. Played on a laptop or a conference screen, sound often off, so captions are on and the voice-over repeats nothing the screen already says. Landscape 1080p only; no vertical cut in this round.
- Rights · 授权: The README states the product and every screen are wireframe placeholders made for the product-promo-film evaluation, not real captures. The film is therefore a labelled DEMO: the end card carries a "Demo · 演示" chip. The logo is the placeholder logo supplied in the folder. No quotes, no testimonials, no photos of people. Music is composed by `make_music.py` (original). Voice is Kokoro `am_michael`, already downloaded, so no download is needed.
- Gaps · 缺口: No real product captures, no user quote, no contacts, no price. We do not invent any of them. Contacts stay empty; the film says only what the README says. The clip uses the supplied recording as it is, labelled as a demo.

## 2. Strategist · 策略
- Audience truth · 受众真相: "When a reviewer asks how I got this figure, I want to answer in one breath."
- Insight · 洞察: The analysis lives in a menu and in the researcher's head. A figure is only as defensible as the steps behind it, and the steps are the part a reviewer will check.
- Single-minded proposition · 唯一主张: Clinical figures a reviewer can rerun. (6 words)
- Proof · 证据: (1) every result exports as a reproducible R script, so a reviewer can rerun it; (2) figures export at 300 or 600 DPI; (3) survival with log-rank and numbers at risk, diagnostic accuracy with AUC and 95% CI, and meta-analysis forest plots with fixed or random effects and I² heterogeneity. All from the README.

## 3. Creative director · 创意总监
- Concept A: The reviewer's question — one-line idea: the film opens on the question a reviewer asks, and each scene is one answer. Opening image: a figure on screen, a cursor resting on the export control. Why it fits: it is the audience's own fear, and the R script is the answer.
- Concept B: Same figure, twice — one-line idea: a figure is drawn, then drawn again from its script, identically. Opening image: two identical plots overlapping and aligning. Why it fits: it proves reproducibility, but it shows a mechanism, not a feeling.
- Concept C: Paper-ready — one-line idea: a spreadsheet becomes a manuscript figure in stages. Opening image: a blank table. Why it fits: accurate, but it could sell any statistics tool.
- Chosen · 选定: A. It is the most true (reviewers do ask this) and the most surprising, because the film speaks to the reviewer the researcher will face, not to the researcher. The R script is then the answer, in the last line.
- Hook (0–3 s) · 开场钩子: Black screen. A forest-plot line draws in, then a second, then a silence. The hook line arrives over the last line drawn.
- Hero moment · 高潮时刻: The five real-looking screens tilt into one wall behind the name, after a half-beat of silence. It lands at the finale, about 65 % of the way through.
- Hook line · 开场句: "Your reviewer will ask how you got this figure."
- Hero line · 高潮句: "Quartile. Figures a reviewer can rerun."
- Last line · 收尾句: "They ask how. You send the script."
- Title · 片名: Ask How (working title)

## 4. Copywriter · 文案
- Tagline · 口号: 审稿人能重跑的图。 / Figures a reviewer can rerun.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "Your reviewer will ask how you got this figure." (fact-free hook: the concept as a question)
  - feature (forest plot) → "Pool the studies, fixed or random. I² sits in the same figure."
  - feature (ROC) → "Diagnostic accuracy, as an AUC with its 95% confidence interval. Stated, not implied."
  - statement → "The analysis is the quick part. The review is not."
  - feature (survival) → "Survival curves with the log-rank test, and the numbers still at risk beneath them."
  - clip → (no voice: the real screen recording runs under its own UI, so the sound stays quiet)
  - phone → (no voice: the title carries the one fact, that saved analyses are listed on the phone)
  - finale → "Quartile. Figures a reviewer can rerun."
  - endcard → "They ask how. You send the script."
- On-screen words · 画面文字: Titles: 森林图：合并效应 / Forest plots, fixed or random effects · ROC 曲线与置信区间 / ROC curves with 95% CI · 生存曲线与对数秩检验 / Kaplan–Meier with log-rank · 每项分析，都是一份结果 / Each analysis, a result · 手机上查看已保存的分析 / Saved analyses on the phone. Points: 固定或随机效应 · I² 异质性 · AUC 与 95% CI · 对数秩检验, each highlighted on the chart it names. Nothing the image already says.
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés.

## 5. Art director · 美术指导
- Look · 视觉: paper-academic. The one accent colour is the logo's teal, and the figures keep a neutral paper ground so the data is the brightest thing in frame. Two typefaces only, from the style.
- Images · 画面选择: the forest plot carries the cover (blurred behind the hook) and the first feature; the ROC curve carries the second feature, where it is the whole frame; the survival curves carry the third; the phone list carries the mobile beat; the desktop workspace and the four analysis figures make the finale wall. The best image, the ROC curve, is held for the feature where the proof is strongest.
- Composition rules · 构图: margins at least 96 px, text never touches an image edge, one focal point per frame, and the highlight rectangles sit only on the region the point names.
- We will NOT show · 不出现: globes, handshakes, stock smiles, lightbulbs, floating icons, and any dashboard that pretends to be real. The wireframes stay labelled as demo.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: precision-data. Lines draw on, numbers settle, nothing bounces. A statistics film should look measured, and this motion language is built for that.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | the question, over the forest plot |
| 2 | `feature` | 5 | reveal + proof | pooled estimates, fixed or random |
| 3 | `feature` | 5 | reveal + proof | diagnostic accuracy, AUC with CI |
| 4 | `statement` | 2 | breath | the calm beat before the next proof |
| 5 | `feature` | 5 | reveal + proof | survival, log-rank, numbers at risk |
| 6 | `clip` | 2 | it really runs | real screen recording, no voice |
| 7 | `phone` | 3 | everywhere | saved analyses on the phone |
| 8 | `finale` | 4 | hero | the name and the tagline |
| 9 | `endcard` | 3 | close | the callback to "how" |

- Cuts · 转场: a cut only where the story turns: cover to the first feature (the question becomes an answer), statement to survival (the breath ends), and into the finale (the hero). Everything else is a plain dissolve from the style.
- Breathing room · 留白: after the ROC feature, the one-line statement rests the audience before the survival curves. The endcard is held for its full length, since the last five seconds must be perfect.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed minimal-electronic, about 104 BPM, original. It builds under the three features, drops to near silence under the statement, and builds again into the finale.
- Silence · 静默: the half-beat before the hero line, and the silence after the hook question so the question lands.
- Sound palette · 音效: very low. A soft tick as each figure line draws. No whoosh on the phone scene. Deliberately no sound under the clip, which keeps the real recording honest.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "every result exports as a reproducible R script" → README, feature list;
  - "figures at 300 or 600 DPI" → README;
  - "log-rank and numbers at risk" → README, survival analysis;
  - "AUC with 95% confidence interval" → README, diagnostic accuracy;
  - "fixed or random effects, I² heterogeneity" → README, meta-analysis;
  - "saved analyses on the phone" → README, phone companion;
  - "Demo" label → README states the product and screens are placeholders.
- Legibility & access · 可读与无障碍: captions on for every voiced line, Chinese and English; contrast checked on the paper ground; no important content sits under a caption.
- Sign-off · 签字: approved, with the condition that the film is labelled as a demo of a placeholder product (chip "Demo · 演示" on the end card, and this note in the report). No copy change required.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 5 | One question, one answer, asked again in the last line. Every proof line is an answer to it. |
| Hook in 3 s · 三秒抓人 | 4 | The forest-plot lines draw in, then the question. Strong, but the cover image is a placeholder wireframe. |
| Specific, true copy · 具体真实 | 4 | Each proof line names a method and a fact from the README (AUC with 95% CI, log-rank, numbers at risk, I²). |
| Image quality & choice · 画面 | 3 | The images are labelled wireframe placeholders from the README. Choice is good, quality is honest and modest. |
| Restraint · 克制 | 5 | One hero, a breath before it, no extra effects beyond the style's restrained cinema layer. |
| Rhythm · 节奏 | 4 | Nine beats with a statement in the middle. Two proof scenes sit close together, which the breath resolves. |
| Hero moment · 高潮 | 4 | The finale wall of screens and the name, after the silence. |
| Memorable ending · 结尾记忆点 | 4 | The callback "They ask how. You send the script." returns the hook's word. |
