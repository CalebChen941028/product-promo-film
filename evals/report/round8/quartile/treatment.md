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
- Material status · 素材状态: the materials README says the screens are wireframe placeholders, not real captures. The film labels them as demo screens (chip) and makes no claim about the real interface.

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: clinical and academic researchers who write papers; plays on a laptop or a conference slide, sound often off, so captions are on.
- Rights · 授权: the product, the screens and the logo are placeholders supplied for this evaluation (no real product rights involved). The music is composed by make_music.py (original, royalty-free). The voice is Kokoro am_michael, already downloaded. No quotes, no photos of people.
- Gaps · 缺口: no real screen captures, no real photos, no testimonials, no contact details. We do not fake them: the screens are labelled as demo, and the end card carries platforms only.

## 2. Strategist · 策略
- Audience truth · 受众真相: "A reviewer will ask how I got this, and I have to be able to show them."
- Insight · 洞察: the figure is finished, but the reviewer's question arrives after the figure, and the tension is that the answer usually lives in a lost spreadsheet and a memory.
- Single-minded proposition · 唯一主张: Every figure you publish, a reviewer can rerun.
- Proof · 证据: (1) every result exports as a reproducible R script; (2) figures export at 300 or 600 DPI; (3) it runs on your own Mac or Windows PC and your data never leaves the computer.

## 3. Creative director · 创意总监
- Concept A: "The Reviewer" — the film's antagonist is the reviewer's question, and the product is the answer to it. Opening image: a survival curve, full frame, calm. Why it fits: it is about the researcher's real moment of exposure.
- Concept B: "Three Analyses, One Table" — a tour of survival, diagnostic and meta-analysis outputs in one workspace. Opening image: the workspace grid. Why it fits: accurate, but it is a feature list, and it could be any analysis tool.
- Concept C: "Forest, Clear" — macro on a forest plot and its confidence intervals, the eye finds the pooled estimate. Opening image: a single interval bar. Why it fits: precise, but it speaks to one analysis only.
- Chosen · 选定: A. It is the most surprising (the reviewer is the protagonist, not the product) and the most true (the R-script export is a real fact, and reviewers really do ask how a number was produced).
- Hook (0–3 s) · 开场钩子: the survival curve fills the frame, still. The voice says the hook line. Then the screen pushes gently into the curve. No logo.
- Hero moment · 高潮时刻: after half a beat of silence at about 65 % (the finale), the survival curve from the cold open returns, blurred behind the workspace, and resolves out of it as a finished, labelled figure. It holds alone for about 3 s, then the name.
- Hook line · 开场句: "A reviewer asks how you got that curve."
- Hero line · 高潮句: "Quartile. Every figure, rerunnable."
- Last line · 收尾句: "The reviewer asks how. The script answers." (a callback to the hook: the same reviewer, now answered)
- Title · 片名: "Rerunnable"

## 4. Copywriter · 文案
- Tagline · 口号: 每张图，都能重跑 / Every figure, rerunnable.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "A reviewer asks how you got that curve." (hook)
  - feature (workspace) → "It runs on your own Mac or Windows PC, and your data never leaves it."
  - detail (ROC) → "The AUC comes with its 95% confidence interval, on the figure you would publish."
  - statement → (no voice: a breath, the feeling only)
  - feature (forest) → "Forest plots with fixed and random effects, and I² for heterogeneity."
  - clip → "Every result exports as an R script a reviewer can run."
  - phone → "A phone companion lists your saved analyses."
  - finale → "Quartile. Every figure, rerunnable." (hero)
  - endcard → "The reviewer asks how. The script answers." (last)
- On-screen words · 画面文字: feature titles ≤ 42 chars; points ≤ 12 字; detail labels "AUC", "95% CI"; statement line; phone title; clip title; endcard chips.
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés (to be re-run at check stage).

## 5. Art director · 美术指导
- Look · 视觉: paper-academic, one accent colour from the logo (the teal #2EE6C8 family). Neutral paper ground, dark ink for text. Why: a reviewer-proof, quiet, scientific look.
- Images · 画面选择: cover and finale use the survival curve (the bookend). Staging: on the cover the curve plays full frame for the first second, then pushes into the curve's own region (the plot area, not the axes labels). The workspace carries the Mac/Windows line and is pushed into the chart panel, not the table. The ROC chart is a zoomed detail on the curve and its AUC label, not the whole figure. The forest plot is framed on the pooled diamond and the I² label. The clip is the scroll of results. The phone screenshot is shown whole in its frame. The best image (survival curve) is saved for the hero and only returns there.
- Composition rules · 构图: margins ≥ 96 px; text never touches the image edge; one focal point per frame; captions bottom, kept clear of the chart axes.
- We will NOT show · 不出现: a stock researcher, a globe, a glowing brain, a handshake, a fake dashboard with invented numbers. No invented p-values on screen beyond what the placeholder charts already show.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: precision-data — slow, measured pushes; cuts only on bar lines; no bounce.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 4 | hook | survival curve full frame, then the name |
| 2 | `feature` | 5 | reveal + proof | workspace: where your data stays |
| 3 | `detail` | 5 | proof, changed shape | zoomed ROC crop, AUC and 95% CI |
| 4 | `statement` | 2 | breath | the feeling, no new fact |
| 5 | `feature` | 5 | reveal + proof | forest plot: fixed, random, I² |
| 6 | `clip` | 2 | it really runs | the R-script line |
| 7 | `phone` | 3 | everywhere | saved analyses on the phone |
| 8 | `finale` | 4 | hero | the survival curve rises out of the UI, ~65 % |
| 9 | `endcard` | 3 | close | the callback |

- Cuts · 转场: camera cuts only at the hook-to-proof turn (cover to workspace), and at the hero (finale). Everything else is a push or a fade on bar lines.
- Breathing room · 留白: the statement beat after the detail, a calm breath before the proof turns to the rerun clip.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed minimal-electronic, ~104 BPM, original and royalty-free. It opens sparse under the hook, builds gently through the proof beats, and drops to a held note under the statement.
- Silence · 静默: the half-beat before the hero, and one held breath on the statement.
- Sound palette · 音效: a soft tick on each chart reveal and the finale resolve; nothing on the phone and the clip. Kept under the voice-over (about 10 dB below).

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "every result exports as a reproducible R script" → materials README, Quartile.
  - "figures export at 300 or 600 DPI" → materials README.
  - "runs on your own Mac or Windows PC; your data never leaves the computer" → materials README.
  - "AUC with 95% confidence interval", "Kaplan–Meier with log-rank and numbers at risk", "forest plots with fixed and random effects and I²" → materials README.
  - "a phone companion lists your saved analyses" → materials README.
  - No performance numbers, no comparisons with other software, no certification claims are made.
- Legibility & access · 可读与无障碍: captions on; the chart labels stay above 18 px at film scale; text on dark ink reaches at least 4.5:1 contrast; nothing important sits under captions.
- Sign-off · 签字: approved for the placeholder demo, with the material status noted in §0 and the demo chip on the end card. Any public release needs real captures and the real product claims checked again.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | The reviewer's question runs through hook, proof and last line. |
| Hook in 3 s · 三秒抓人 | 4 | A full-frame curve and a question every researcher has heard. |
| Specific, true copy · 具体真实 | 4 | Every proof line carries a fact from the README; no invented numbers. |
| Image quality & choice · 画面 | 4 | Each beat has a chosen image and a stated crop; the best image is held for the hero. The source is placeholder wireframes, which is recorded in §0 and §1, not in this score. |
| Restraint · 克制 | 4 | One hero, two calm beats, no extra effects. |
| Rhythm · 节奏 | 4 | Dense and calm beats alternate; no two proof beats share a shape. |
| Hero moment · 高潮 | 4 | The hook's curve returns and resolves into the finished figure. |
| Memorable ending · 结尾记忆点 | 4 | The callback closes the question the film opened. |
