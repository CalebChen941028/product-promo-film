# Treatment · 创意方案 — Quartile

> Written by the crew in `references/crew.md`, one section per role, in order.
> `python3 scripts/check_treatment.py treatment.md film.json` must pass before `make_film.py --stage build`.

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: Quartile
- Genre · 类型: science-data — Science, research, data analysis / 科研 / 数据分析 / 统计
- Look · 风格: paper-academic · Motion · 动效: precision-data · Arc · 叙事结构: problem-solution
- Music · 音乐: composed: minimal-electronic ~104 BPM (original, royalty-free)
- Materials · 素材: desktop 4, logo 1, phone 1, text 1, ui 5, video 1
- Target length · 目标时长: ~100 s
- Tone for this genre · 本类型的语气: exact, modest, evidence first; numbers must be checkable
- Study first · 先读: `templates/golden/problem-solution.json` and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: Desktop statistics for clinical researchers. Load a spreadsheet, pick an analysis, get a table and a figure you can put in a paper. · Survival analysis: Kaplan–Meier curves with log-rank test and numbers at risk · Diagnostic accuracy: ROC curves with AUC and 95% confidence interval · Meta-analysis: forest plots with fixed and random effects and I² heterogeneity · Every result exports as a reproducible R script, so a reviewer can rerun it · Figures export at 300 or 600 DPI · Runs on your own Mac or Windows PC; your data never leaves the computer · A phone companion lists your saved analyses

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Clinical and academic researchers, shown as a short product film on a web page or a conference slide; mostly watched with sound on, captions on for the rest. Evaluation film, not a live launch.
- Rights · 授权: The materials are the project's own wireframe placeholders (the README says so). The music is composed by `make_music.py`; the voice is Kokoro, already downloaded. No quotes, no people, no third-party logos.
- Gaps · 缺口: No real screenshots, so the screens are placeholder wireframes; the highlight boxes point at placeholder regions. The film makes claims only from the docs. No contacts, no testimonials, no price in the docs, so the end card carries none.

## 2. Strategist · 策略
- Audience truth · 受众真相: "A reviewer asks me to rerun the analysis, and I have to find out how I got the number."
- Insight · 洞察: The figure in the paper is the answer, but the reviewer wants the procedure. A click-driven tool leaves no trail, so every rerun is a rebuild.
- Single-minded proposition · 唯一主张: Quartile gives the same figure and the same answer every time you run it.
- Proof · 证据: Every result exports as a reproducible R script. Figures export at 300 or 600 DPI. Survival, ROC and forest plots each come with their statistics (log-rank, AUC with 95% CI, I²).

## 3. Creative director · 创意总监
- Concept A: Run it again — the paper has one line that needs a rerun; opening on a reviewer's note; why it fits: it is the real pain of clinical statistics.
- Concept B: The two-week figure — the time spent rebuilding a figure from memory; opening on a dull repeated click; why it fits: a vivid time cost, but it is about speed, which every tool claims.
- Concept C: Data that stays home — the privacy promise as the story; opening on a closed laptop; why it fits: true, but a claim about safety, not about the paper.
- Chosen · 选定: A (Run it again). It is the most surprising because the hero is a rerun, not a feature, and the most true because the R script export is in the docs. B is a speed claim every tool makes; C is true but reads as a disclaimer.
- Hook (0–3 s) · 开场钩子: The analysis workspace fills the frame in silence for the first beat, then the workspace under it. The voice says the hook line over the screen, blurred.
- Hero moment · 高潮时刻: The finale wall of real results, tilted, held for one bar, with the name and the tagline landing after a half-beat of silence, at about 60% of the film.
- Hook line · 开场句: "The reviewer asks you to run it again."
- Hero line · 高潮句: "Quartile. Same data. Same answer."
- Last line · 收尾句: "They run it again. It matches." (a callback to "run it again" from the hook; the change is that it matches)
- Title · 片名: Run It Again

## 4. Copywriter · 文案
- Tagline · 口号: 同样的数据，同样的结果 / Same data. Same answer.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "The reviewer asks you to run it again." (hook; the reviewer's request, no product yet)
  - feature survival → "The log-rank test and the numbers at risk, already on the curve." (fact: log-rank and numbers at risk)
  - feature ROC → "The AUC comes with its 95% confidence interval, so a reader sees how sure you are." (fact: AUC, 95% CI)
  - clip → (no voice: the results scroll; the screen says "every result exports as an R script")
  - statement → "A number should survive a second run." (breath; no new fact)
  - feature forest → "Fixed or random effects, and I² for heterogeneity, on one figure." (fact: fixed/random, I²)
  - finale → "Quartile. Same data. Same answer." (hero)
  - endcard → "They run it again. It matches." (last; callback to the hook)
- On-screen words · 画面文字: survival title "Survival curves, ready for the paper"; ROC "ROC curve, with its AUC"; clip title "Every result exports as an R script."; forest title "Forest plot, fixed or random"; point labels: "Log-rank test", "Numbers at risk", "AUC with 95% CI", "Reference diagonal", "Fixed and random effects", "I² heterogeneity".
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés.

## 5. Art director · 美术指导
- Look · 视觉: paper-academic: quiet paper ground, dark ink, one accent colour taken from the logo (teal, #2EE6C8 family). The logo is a dark rounded square with teal bars, so teal is the only accent.
- Images · 画面选择: cover = workspace.png (the analysis window, the paper's home); survival and ROC and forest each carry their own beat; the clip carries the R-script proof; finale uses the five real images; the best image (the forest plot with its reference line) is kept for the hero context.
- Composition rules · 构图: margins 96 px; one focal point per frame; text sits on the paper ground, never over a curve; the highlight boxes mark the region each point names.
- We will NOT show · 不出现: a generic statistics icon, a globe, a handshake, a stock scientist, a fake p-value, a fake journal logo, a fake reviewer quote.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: precision-data — the figures draw and the boxes lock on the points, no bounce. It matches a method that must be exact.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | the reviewer's request |
| 2 | `feature` | 4 | reveal + proof | survival: log-rank, numbers at risk |
| 3 | `feature` | 4 | reveal + proof | ROC: AUC with 95% CI |
| 4 | `clip` | 2 | it really runs | every result exports as an R script |
| 5 | `statement` | 2 | breath | the feeling, no new fact |
| 6 | `feature` | 4 | reveal + proof | forest: fixed/random, I² |
| 7 | `finale` | 4 | hero | the name and the tagline |
| 8 | `endcard` | rest | close | the callback |

- Cuts · 转场: Camera cuts only where the story turns: into the statement (a true pause after three proofs) and into the finale (the one hero moment). Other cuts are plain style transitions.
- Breathing room · 留白: After the ROC proof, the clip and the statement give the viewer room before the forest figure; the statement holds two bars with no picture change beyond a slow push.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed minimal-electronic, ~104 BPM, original. Low pulse through the proofs, opening out at the finale, ringing out on the end card.
- Silence · 静默: A half-beat of silence before the hero line; the statement is held as a second silence.
- Sound palette · 音效: Kept low. Soft ticks on the figure draws and one soft hit on the hero beat. No sound on the statement, so the sentence lands alone.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "Log-rank test", "numbers at risk" → docs: Survival analysis line.
  - "AUC with 95% CI" → docs: Diagnostic accuracy line.
  - "Fixed and random effects", "I² heterogeneity" → docs: Meta-analysis line.
  - "Every result exports as an R script" → docs: reproducible R script line.
  - "Same data. Same answer." → a reading of the R-script export; the film makes no speed or accuracy claim beyond that.
  - "Runs on your computer; data never leaves" is in the docs but not used on screen.
- Legibility & access · 可读与无障碍: captions on for every spoken line; contrast checked on the paper ground; nothing important sits under captions.
- Sign-off · 签字: approved for the evaluation film, with the placeholder-screen caveat stated in the report (not a product claim).

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | One proposition, "run it again, it matches"; every line serves it. |
| Hook in 3 s · 三秒抓人 | 4 | The reviewer's request is a true, specific tension, spoken over the analysis window. |
| Specific, true copy · 具体真实 | 4 | Each proof line names a method and its statistic from the docs (log-rank, AUC 95% CI, I²). |
| Image quality & choice · 画面 | 4 | Placeholder wireframes chosen and staged well; the highlight boxes match the points. The real screenshots were not provided, so this stays at 4, not 5. |
| Restraint · 克制 | 4 | One hero, calm statement, no extra effects. |
| Rhythm · 节奏 | 4 | Two dense features, a clip, a breath, a feature, then the hero. |
| Hero moment · 高潮 | 4 | The name and the tagline land after silence, on the real-results wall. |
| Memorable ending · 结尾记忆点 | 4 | The callback "It matches" closes the loop the hook opened. |
