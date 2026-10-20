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
- Audience & where it plays · 受众与投放渠道: Clinical researchers and their co-authors, on a laptop or a conference screen, most with sound off; 16:9 master only for this round.
- Rights · 授权: All images are the project's own placeholder wireframes and logo from the materials folder (README: "placeholder product for the product-promo-film evaluation"). No photos, quotes or third-party music. Music is composed for this film. No quotes are used.
- Gaps · 缺口: The screens are wireframe placeholders, not real captures, and carry no readable labels. We do not invent UI text or numbers. The forest, ROC and survival images are generic plots with no axis values. Contacts and a real testimonial are missing; the end card carries no contact line.

## 2. Strategist · 策略
- Audience truth · 受众真相: "When a reviewer asks us to run it again, we open last year's file and hope it still matches."
- Insight · 洞察: Researchers are judged on whether a result can be reproduced, but rerunning an analysis by hand is slow and easy to get wrong.
- Single-minded proposition · 唯一主张: Results a reviewer can rerun, and get the same answer.
- Proof · 证据: Every result exports as a reproducible R script; figures export at 300 or 600 DPI; the data never leaves the computer.

## 3. Creative director · 创意总监
- Concept A: The Rerun — a reviewer asks you to run the analysis again, and the film answers by running it again — opening image: a forest plot on a blank page, then the question on screen — why it fits: reproducibility is exactly what a reviewer asks for.
- Concept B: Open Figure — the figure leaves the manuscript and is checked line by line by strangers — opening image: a single ROC curve drawn slowly from the corner — why it fits: figures are the thing reviewers actually look at.
- Concept C: Stays Home — the file never leaves the desk, so the privacy promise is shown rather than said — opening image: a spreadsheet alone on an empty desk — why it fits: the data-protection point is real, but it is a feature, not the reason to buy.
- Chosen · 选定: A — because it is the most true (the reproducible R script is the product) and the most surprising (the film is about a reviewer's request, not the software).
- Hook (0–3 s) · 开场钩子: The forest plot fills the frame, cold and full-bleed, with one soft pulse on its first estimate. A question, spoken over it: "Can you run that again?" Silence after it.
- Hero moment · 高潮时刻: The wall of real screens tilts into place as the name lands. One held beat of silence, then "Same analysis. Same answer." It lands at about 65 % of the film.
- Hook line · 开场句: "Can you run that again?"
- Hero line · 高潮句: "Same analysis. Same answer." — the tagline, with the name on screen.
- Last line · 收尾句: "Run it again. Same script, same answer." — a callback to the hook's words, ending on the viewer's own check.
- Title · 片名: Run It Again

## 4. Copywriter · 文案
- Tagline · 口号: 同样的分析，同样的结果 / Same analysis. Same answer.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "Can you run that again?"
  - feature (meta-analysis) → "Pooled estimates from fixed and random effects, and how much the studies disagree."
  - feature (ROC) → "The ROC curve gives the AUC, with its 95% confidence interval, so the claim has a range."
  - statement → (no voice: a breath, the feeling only)
  - feature (survival) → "Kaplan–Meier curves, with the log-rank test and numbers at risk."
  - clip → (no voice: the screen recording does the work)
  - phone → (no voice: the saved list on the phone)
  - finale → "Same analysis. Same answer."
  - endcard → "Run it again. Same script, same answer."
- On-screen words · 画面文字: Fixed and random effects · I² heterogeneity · AUC · 95% confidence interval · Log-rank test · Numbers at risk · Demo screens (chip) · macOS · Windows
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés

## 5. Art director · 美术指导
- Look · 视觉: paper-academic: a white page, dark ink, one accent colour taken from the logo (the mint-teal of the logo tile). Two type faces at most. Plots and screens stay neutral so the accent points at the figure being discussed.
- Images · 画面选择: The forest plot carries the hook (it reads as "a result"), and the same plot is reused for the first feature. The ROC and survival plots each carry their own feature. The phone screen carries the mobile line. The best image, the full wall of screens, is saved for the finale.
- Composition rules · 构图: Margins ≥ 96 px; one focal point per frame; labels short and away from the image edges; captions never cover the plot axes.
- We will NOT show · 不出现: globes, handshakes, lightbulbs, stock smiles, floating icons, invented dashboards with fake numbers, any claim of a clinical result.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: precision-data: measured reveals, lines drawn left to right, no bounce. Matches a figure being checked.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | the question on the forest plot |
| 2 | `feature` | 5 | reveal + proof | meta-analysis: fixed/random effects, I² |
| 3 | `feature` | 5 | reveal + proof | ROC: AUC and its interval |
| 4 | `statement` | 2 | breath | no picture, no new fact |
| 5 | `feature` | 5 | reveal + proof | survival: log-rank and numbers at risk |
| 6 | `clip` | 2 | it really runs | the screen recording, no voice |
| 7 | `phone` | 3 | everywhere | saved analyses on the phone |
| 8 | `finale` | 4 | hero | the tagline, the name |
| 9 | `endcard` | 3 | close | the callback |

- Cuts · 转场: Hard cuts only at the bar lines of the question (cover to feature 1) and at the turn into the finale. Everything else dissolves on the bar.
- Breathing room · 留白: After the two dense feature beats, the statement and the silent clip give the film a rest. Then the half-beat of silence before "Same analysis." makes the hero land.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: Composed minimal-electronic, ~104 BPM: a sparse pulse under the hook, a steady build through the three features, a drop to the pulse alone for the statement, a lift on the finale bar.
- Silence · 静默: One half-beat of silence after "Can you run that again?" and one more before "Same analysis." No other held breath.
- Sound palette · 音效: Very low: a soft tick on each drawn line in the features; nothing on the clip and phone beats. The tick is kept under the music.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "Desktop statistics for clinical researchers" → README line 1.
  - "Survival: Kaplan–Meier, log-rank, numbers at risk" → README bullets.
  - "Diagnostic: ROC, AUC, 95% CI" → README bullets.
  - "Meta-analysis: forest plots, fixed and random effects, I²" → README bullets.
  - "Reproducible R script" and "300 or 600 DPI" → README bullets.
  - "Runs on your own Mac or Windows PC; data never leaves the computer" → README bullet.
  - "Phone companion lists your saved analyses" → README bullet.
  - No accuracy, speed or clinical-outcome claim is made.
- Legibility & access · 可读与无障碍: Captions on. Contrast checked on the paper background. The screens carry no readable text, so nothing important sits under captions.
- Sign-off · 签字: approved as a demo, with changes needed before any public release: real captures replace the wireframes, and the chip "Demo screens" stays until they do.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | Reproduction runs through the hook, the proof and the last line. |
| Hook in 3 s · 三秒抓人 | 4 | A full-bleed plot and a direct question in the first second. |
| Specific, true copy · 具体真实 | 4 | Every proof line names a method and carries a fact from the README. |
| Image quality & choice · 画面 | 3 | Each beat has its own image and the best wall is saved for the hero, but the screens are wireframe placeholders with no readable labels. Limit in §1 Gaps. |
| Restraint · 克制 | 5 | One hero, one accent colour, a quiet statement and a silent clip. |
| Rhythm · 节奏 | 4 | Dense beats alternate with a breath and a silent clip; no run of identical beats. |
| Hero moment · 高潮 | 4 | The wall of screens and the held beat before the tagline. |
| Memorable ending · 结尾记忆点 | 4 | The callback to "run that again" closes the film. |
