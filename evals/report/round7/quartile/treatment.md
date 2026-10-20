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
- Target length · 目标时长: ~74 s — 6 images/clips carry about 74 s; the problem-solution arc would run 100 s with more material. Do not pad: no repeats, no long holds
- Tone for this genre · 本类型的语气: exact, modest, evidence first; numbers must be checkable
- Study first · 先读: `templates/golden/problem-solution.json` (a top film in this arc, every scene with a `_why`) and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: Desktop statistics for clinical researchers. Load a spreadsheet, pick an analysis, get a table and a figure you can put in a paper. · Survival analysis: Kaplan–Meier curves with log-rank test and numbers at risk · Diagnostic accuracy: ROC curves with AUC and 95% confidence interval · Meta-analysis: forest plots with fixed and random effects and I² heterogeneity · Every result exports as a reproducible R script, so a reviewer can rerun it · Figures export at 300 or 600 DPI · Runs on your own Mac or Windows PC; your data never leaves the computer · A phone companion lists your saved analyses

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Clinical and academic researchers who write papers and face reviewers. Watched on a laptop or a conference screen, most likely with sound on; the film must also read with sound off (captions on).
- Rights · 授权: All screens, charts and the logo are placeholders made for this evaluation (the README says so). No real customer, testimonial or third-party music. Music is composed (original). Voice is Kokoro am_michael (downloaded, Apache-2.0).
- Gaps · 缺口: The screens are wireframes and the charts are unlabelled sketches (no axis text, no numbers, no risk table, no AUC value on screen). So nothing on screen can prove a number; the proof lines name what the product does (from the README), and the image only shows the shape. The survival curve and the phone companion are left out of this cut: the film stays on one proposition, and their facts remain in the README. The film is labelled as a demo on the end card. Real captures would replace these files without changing the film's structure.

## 2. Strategist · 策略
- Audience truth · 受众真相: "Reviewers ask how I got this number, and I have to explain it again."
- Insight · 洞察: A figure in a paper is only as trusted as the path behind it. The reviewer's question is the real test, and the work is rarely written down in a way someone else can run.
- Single-minded proposition · 唯一主张: A reviewer can rerun every result you publish.
- Proof · 证据:
  - Every result exports as a reproducible R script, so a reviewer can rerun it.
  - Figures export at 300 or 600 DPI.
  - ROC curves with the AUC and its 95% confidence interval; forest plots with fixed and random effects and I².

## 3. Creative director · 创意总监
- Concept A: The reviewer's question — the film opens on the question a reviewer asks, and the product is the answer; open on a forest plot, end on the script. Why it fits: it is the audience's own moment of doubt.
- Concept B: From sheet to figure — a spreadsheet becomes a figure, step by step, the way a tool demo would show. Why it fits: true, but it is the generic version of every analysis tool.
- Concept C: Numbers at risk — the survival curve's risk table as a metaphor for who is still in the study. Why it fits: beautiful, but the screens do not show a risk table, so the image would lie.
- Chosen · 选定: A. It is the most surprising (a film about a reviewer, not about the software) and the most true (the R script is the answer to the question, and it is in the README).
- Hook (0–3 s) · 开场钩子: The forest plot fills the frame, almost still. One voice line, no logo: a reviewer asks how you got that number. The question lands on the image before the name appears.
- Hero moment · 高潮时刻: The forest plot, the figure you can put in the paper, rises out of the workspace and settles in the frame, with the name and "Quartile. Show the work." It lands at about 73 %, after the proof has been seen.
- Hook line · 开场句: A reviewer asks how you got that number.
- Hero line · 高潮句: Quartile. Show the work.
- Last line · 收尾句: The reviewer asks again. The answer is a script.
- Title · 片名: Show the work

## 4. Copywriter · 文案
- Tagline · 口号: 把每一步写清楚 / Show the work.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "A reviewer asks how you got that number."
  - feature (forest plot) → "Pool the studies with a fixed or a random model, and see the heterogeneity I² beside them."
  - detail (ROC) → "The AUC, with its 95% confidence interval, on the curve you will publish."
  - statement → (no voice: a breath after two proofs)
  - numbers → (no voice: the screen says 600 and 95 %)
  - clip → "Load a sheet, pick a test, and the figure is ready."
  - finale → "Quartile. Show the work."
  - endcard → "The reviewer asks again. The answer is a script."
- On-screen words · 画面文字:
  - feature: title "Pool the studies, two ways" / 两种方式合并研究; points "Fixed and random effects" / 固定与随机效应, "I² heterogeneity" / I² 异质性
  - detail: crop "ROC curve" / ROC 曲线; crop "AUC with 95% CI" / AUC 与 95% 置信区间
  - statement: "Every number has a path back." / 每个数字，都有来路。
  - numbers: "600 DPI, for the paper" / 600 DPI，用于论文; "95% confidence interval" / 95% 置信区间
  - clip: "Load a sheet, get the figure." / 载入表格，得到图表
  - endcard demo label: "Demo · placeholder screens" / 演示 · 占位界面
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés. No praise adjectives, no "seamless", "powerful", "AI".

## 5. Art director · 美术指导
- Look · 视觉: paper-academic: a light, paper-like ground with one accent colour from the logo (the teal on the dark tile). Neutral greys everywhere else; the accent is the brightest thing on screen, which is the figure the voice names.
- Images · 画面选择:
  - cover: forest-plot.png, full frame (the figure is the calm subject of the hook).
  - feature: forest-plot.png at the proof position, points carry labels (no boxes, the chart is sparse).
  - detail: roc-curve.png, two crops: the curve, and the top-right of the curve for the AUC claim.
  - numbers: the stat tiles over the paper-like ground, no image.
  - clip: scroll-results.webm (the real recording available).
  - finale: forest-plot.png rising out of workspace.png (the one output that matters, the figure for the paper, over the workspace it came from). Saved for the hero: the forest plot is not shown full-frame before the finale except as the cover; the cover shows it once, the hero rises it out of the UI.
  - endcard: the logo.
- Composition rules · 构图: margins ≥ 96 px; text sits in the empty areas of the paper-like ground, never over a curve. One focal point per frame.
- We will NOT show · 不出现: globes, handshakes, bulbs, stock smiles, floating icons, a fake risk table or fake AUC numbers on any image, real-looking clinical data, a patient.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: precision-data — measured, grid-aligned moves; cuts land on the bar line; no drifting.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 4 | hook | the question over the forest plot, no logo |
| 2 | `feature` | 5 | reveal + proof | meta-analysis, fixed and random |
| 3 | `detail` | 4 | proof, shape changed | zoomed ROC crops, AUC with its CI |
| 4 | `statement` | 2 | breath | "Every number has a path back." |
| 5 | `numbers` | 2 | proof, shape changed | 600 DPI and 95%, the screen speaks |
| 6 | `clip` | 2 | it really runs | the real recording, the workflow |
| 7 | `finale` | 4 | hero | the figure rises out of the workspace, the name, the tagline |
| 8 | `endcard` | 3 | close | the callback line, the demo label |

- Cuts · 转场: cuts only at the turns: hook → proof (cover to feature), proof → breath (detail to statement), breath → proof (statement to numbers), proof → hero (clip to finale). No whip on the clip.
- Breathing room · 留白: the statement after two proof beats (detail, then one breath before the numbers). The end card holds the last line, then rests.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed minimal-electronic, ~104 BPM (original, from make_music.py). Low under the voice (about 10 dB below); it builds into the finale and drops for the last line.
- Silence · 静默: half a beat before "Quartile." in the finale, and the statement beat is a true pause.
- Sound palette · 音效: a soft click on the forest plot's first point and on the finale's name; no sound on the statement and no effects on the clip. Kept low: felt, not heard.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "Every result exports as a reproducible R script" → README line 4.
  - "Figures export at 300 or 600 DPI" → README line 5.
  - "AUC with its 95% confidence interval" → README (diagnostic accuracy).
  - "Fixed and random effects; I²" → README (meta-analysis).
  - "Load a spreadsheet, pick an analysis, get a table and a figure" → README line 1.
  - "Runs on Mac or Windows" → README line 7 (chips on the end card).
  - No claim about speed, accuracy or customers; no number that is not in the README.
- Legibility & access · 可读与无障碍: captions on for all voice; the on-screen words are at least 18 px at film scale; contrast checked on the paper-like ground; no important text under a caption.
- Sign-off · 签字: approved for a demo cut only: copy is true to the README; the visuals are placeholders and are labelled as such on the end card. Not approved as a marketing film for the real product until real captures replace the placeholders.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | The reviewer's question runs through hook, hero and last line; the film is about one proposition. |
| Hook in 3 s · 三秒抓人 | 4 | A question the audience has asked themselves, spoken over a calm, full-frame figure. |
| Specific, true copy · 具体真实 | 4 | Every voice line carries a README fact and says what it means for a reviewer; no praise words. |
| Image quality & choice · 画面 | 4 | Each beat has one relevant image, the figure carries the hook and the hero, and the best figure is saved for the hero. The placeholder limit is recorded in §1 Gaps, not scored here. |
| Restraint · 克制 | 4 | One hero, two calm beats, no effects beyond the precision-data motion. |
| Rhythm · 节奏 | 4 | No two proof beats in a row share a shape (feature, zoomed detail, breath, numbers, clip). |
| Hero moment · 高潮 | 4 | The hero is the output the proposition is about, rising out of the workspace it came from. |
| Memorable ending · 结尾记忆点 | 4 | The callback repeats "the answer" from the question, and the end card carries the demo label honestly. |
