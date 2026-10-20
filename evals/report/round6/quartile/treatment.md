# Treatment · 创意方案 — Quartile

> Written by the crew in `references/crew.md`, one section per role, in order.

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: Quartile
- Genre · 类型: science-data — Science, research, data analysis / 科研 / 数据分析 / 统计
- Look · 风格: paper-academic · Motion · 动效: precision-data · Arc · 叙事结构: problem-solution
- Music · 音乐: composed: minimal-electronic ~104 BPM (original, royalty-free)
- Materials · 素材: desktop 4, logo 1, phone 1, text 1, ui 5, video 1
- Target length · 目标时长: ~74 s
- Tone for this genre · 本类型的语气: exact, modest, evidence first; numbers must be checkable
- Study first · 先读: `templates/golden/problem-solution.json` and `references/copy-bank.md`
- Facts to use · 可用事实: Desktop statistics for clinical researchers. Load a spreadsheet, pick an analysis, get a table and a figure you can put in a paper. · Survival analysis: Kaplan–Meier curves with log-rank test and numbers at risk · Diagnostic accuracy: ROC curves with AUC and 95% confidence interval · Meta-analysis: forest plots with fixed and random effects and I² heterogeneity · Every result exports as a reproducible R script, so a reviewer can rerun it · Figures export at 300 or 600 DPI · Runs on your own Mac or Windows PC; your data never leaves the computer · A phone companion lists your saved analyses

Materials note: the screens and charts in the folder are wireframe placeholders (README). Every claim below is taken from the README list above.

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Clinical researchers and graduate students who write papers. Plays on a laptop or a landing page, sound on, captions on for silent autoplay.
- Rights · 授权: Logo, screens and charts are the project's own placeholder artwork for this evaluation. Music is composed original (make_music). No quotes, no photos of people. Demo film, labelled as such in the chips.
- Gaps · 缺口: No real product captures, no testimonial and no contact details in the docs. We use the placeholder screens as they are, show only what they show, and leave the end-card contacts empty.

## 2. Strategist · 策略
- Audience truth · 受众真相: "A reviewer asks how I got that number, and I have to rebuild the analysis from memory."
- Insight · 洞察: Researchers want to be trusted without a long explanation; a reviewer wants to check, not to take the number on faith.
- Single-minded proposition · 唯一主张: Every result you publish, a reviewer can rerun.
- Proof · 证据: (1) Every result exports as a reproducible R script. (2) Survival, ROC and forest plots, with log-rank, AUC with 95% CI, and I². (3) Figures at 300 or 600 DPI, and your data never leaves your computer.

## 3. Creative director · 创意总监
- Concept A: Methods first — open on the methods paragraph, the words a reviewer reads, then show the analysis that backs each word. Opening image: a desktop workspace with a results table. Why it fits: it speaks to the paper, which is where the audience works.
- Concept B: Rerun it — a reviewer asks one question and the answer is a script they run themselves. Opening image: the desktop workspace, then the question as text. Why it fits: it is the export feature, and it turns the product into a promise about trust.
- Concept C: Figure ready — the figure goes from screen to journal page at 600 DPI with no redraw. Opening image: a forest plot, sharp. Why it fits: visual, but it is about the output, not the reason the audience cares.
- Chosen · 选定: B. Rerun it. It is the most surprising (a film about a reviewer, not about the app) and the most true (the README promises the script). It also gives a callback: the reviewer who asks in the first line answers in the last line.
- Hook (0–3 s) · 开场钩子: The desktop workspace fills the frame, calm and cold. The hook line is spoken over it: a reviewer asked how the number was made.
- Hero moment · 高潮时刻: The forest plot rises out of the blurred workspace at about 65 %, a publication figure with its method labelled beside it. The one image the audience remembers: a figure that is ready for the paper.
- Hook line · 开场句: A reviewer asked how you got that number.
- Hero line · 高潮句: Quartile. Every result, rerunnable.
- Last line · 收尾句: The reviewer asks. The script answers.
- Title · 片名: Rerun It

## 4. Copywriter · 文案
- Tagline · 口号: 结果，可以重跑 / Every result, rerunnable.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "A reviewer asked how you got that number."
  - feature (meta-analysis) → "Pool your studies. Fixed or random effects, with I² for heterogeneity."
  - feature (diagnostic) → "Diagnostic accuracy, with the ROC curve and the AUC's 95% interval."
  - statement → "A result should survive a rerun." (no new fact; the breath before the proofs)
  - feature (survival) → "Survival curves with a log-rank test, and the numbers still at risk."
  - clip → (no voice: the results screen scrolls, and the image says it)
  - phone → "Your saved analyses, on the phone."
  - finale → "Quartile. Every result, rerunnable."
  - endcard → "The reviewer asks. The script answers."
- On-screen words · 画面文字: forest plot: 固定与随机效应 / Fixed and random effects; I² 异质性 / I² heterogeneity; ROC: ROC 曲线与 AUC / ROC curve and AUC; 95% 置信区间 / 95% CI on the AUC; survival: Kaplan–Meier 与 log-rank / Kaplan–Meier with log-rank; 风险人数 / Numbers at risk; clip: 结果逐屏查看 / The results, screen by screen; phone: 手机上查看已保存的分析 / Saved analyses on your phone.
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés.

## 5. Art director · 美术指导
- Look · 视觉: paper-academic. The accent colour comes from the logo's teal; everything else is neutral paper and graphite. Two typefaces, the style's own.
- Images · 画面选择: cover = the desktop workspace (the subject is the work, not a texture). Feature 1 = forest plot. Feature 2 = ROC curve. Feature 3 = survival curve. Clip = the results scroll. Phone = saved analyses. Finale hero = forest plot, rising out of the workspace. The workspace is used once as the cover and once as the blurred backdrop of the hero, which is the same subject, not a repeat.
- Composition rules · 构图: margins 96 px; captions sit clear of the chart; one focal point per frame; the highlight boxes mark the regions the points talk about.
- We will NOT show · 不出现: globes, handshakes, stock scientists, fake 3D charts, invented p-values or AUC values, any fake testimonial.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: precision-data. Charts draw on the beat and the highlight boxes snap to the regions named in the copy. It suits a reviewer's patience: measured, never bouncy.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | the workspace, the question |
| 2 | `feature` | 5 | reveal + proof | meta-analysis |
| 3 | `feature` | 5 | reveal + proof | diagnostic accuracy |
| 4 | `statement` | 2 | breath | the feeling, no new fact |
| 5 | `feature` | 5 | reveal + proof | survival |
| 6 | `clip` | 2 | it really runs | results scroll |
| 7 | `phone` | 3 | everywhere | saved analyses |
| 8 | `finale` | 4 | hero | the figure rises |
| 9 | `endcard` | 3 | close | the callback |

- Cuts · 转场: camera cuts only at the three story turns: cover to meta-analysis (the question becomes the answer), survival to the clip (the answer runs), and the clip to the hero (the work leads to the figure).
- Breathing room · 留白: the statement beat after the first two proof scenes. Two dense beats, then one calm beat.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed minimal-electronic, ~104 BPM, original and royalty-free. It stays quiet under the voice, builds slightly into the survival beat, and drops to a single pulse for the hero.
- Silence · 静默: the half-beat before the hero line, and the statement beat is held with no music swell.
- Sound palette · 音效: a soft tick on each chart draw and a soft click on the highlight boxes. No whoosh on the question, no bell on the hero.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "Every result exports as a reproducible R script" → README, facts line 4.
  - "Fixed and random effects, I² heterogeneity" → README, meta-analysis line.
  - "Log-rank, numbers at risk, AUC with 95% CI" → README, survival and diagnostic lines.
  - "300 or 600 DPI" → README, figure line (not shown on screen; only in captions if used).
  - "Your data never leaves the computer" → README, runs on your own Mac or Windows line. Not in the film copy beyond the phone and finale lines to keep the claim narrow.
  - "Your saved analyses, on the phone" → README, phone companion line.
- Legibility & access · 可读与无障碍: captions on by default; English and Chinese captions; the highlight boxes use the accent colour with a 3 px outline; nothing important sits under the captions.
- Sign-off · 签字: approved with the placeholder note. Changes needed: none beyond keeping the demo chip on the end card.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | One idea, reviewers can rerun the work. Every feature line points back to it. |
| Hook in 3 s · 三秒抓人 | 4 | The workspace and the question land in the first seconds. |
| Specific, true copy · 具体真实 | 4 | Each proof line names a method and a README fact; no invented numbers. |
| Image quality & choice · 画面 | 4 | Each beat has the image its copy names; the best figure (forest plot) is kept for the hero. The wireframe limit is recorded in §1 Gaps, not here. |
| Restraint · 克制 | 4 | One hero, two calm beats, no extra effects. |
| Rhythm · 节奏 | 4 | Dense proofs, one breath, one clip, one phone, one hero. |
| Hero moment · 高潮 | 4 | The forest plot rises out of the workspace as the figure for the paper. |
| Memorable ending · 结尾记忆点 | 4 | The callback turns the reviewer's question into the answer. |
