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
- Audience & where it plays · 受众与投放渠道: Clinical and epidemiology researchers who write papers; watched on a laptop or in a lab-meeting screen share, sound often off, so every beat must read with captions. Landscape 1080p. A vertical cut is not planned.
- Rights · 授权: Music is an original underscore composed by `make_music.py` (no third-party track). Logo, screens and the forest/ROC/survival images are the placeholder materials supplied for this evaluation, which are wireframe placeholders, not real captures. No quotes, no testimonials, no people. Voice is Kokoro am_michael (Apache-2.0), already downloaded.
- Gaps · 缺口: The screens are wireframe placeholders, so no real UI is shown; the film is labelled as a demo on the end card (contacts row). The results figures are generic plots, not a real analysis. No numbers beyond the README are used. Nothing in the film promises a feature the README does not list. The clip is the supplied screen recording, used without voice.

## 2. Strategist · 策略
- Audience truth · 受众真相: "My reviewer will ask me to rerun the analysis, and I need to be able to do it."
- Insight · 洞察: Running a statistical test is easy; proving the number again, to someone else, months later, is the hard part, and it is the part that gets a paper accepted.
- Single-minded proposition · 唯一主张: A result is only evidence if someone can run it again.
- Proof · 证据: (1) Every result exports as a reproducible R script. (2) Survival, ROC and meta-analysis in one desktop tool. (3) Figures at 300 or 600 DPI. (4) Your data never leaves your Mac or Windows PC.

## 3. Creative director · 创意总监
- Concept A: Run it again — the figure arrives with the script that made it, so the reviewer's question is answered before it is asked. Opening image: a forest plot, then a cursor that presses rerun. Why it fits: the README says exactly this (reproducible R script), and it is the one thing a reviewer cares about.
- Concept B: Quiet desk — the patient data never leaves the machine. Opening image: a closed drawer and a laptop with no cloud icon. Why it fits: true (data stays on the computer), but it is a reassurance, not a reason to choose the product for the paper.
- Concept C: Print-ready — 600 DPI, first time. Opening image: a ROC curve in extreme close-up on the edge of a page. Why it fits: true (300 or 600 DPI export), but it is a spec, and it could be any plotting tool's ad.
- Chosen · 选定: A — it is the most surprising (a reviewer's question, not a feature, opens the film) and the most true (the R script export is the documented feature that answers that question). B and C are kept as supporting proof lines, not as the idea.
- Hook (0–3 s) · 开场钩子: A forest plot fills the frame, slightly blurred. A calm voice asks the question a reviewer asks; the question is the first thing heard and the first caption on screen.
- Hero moment · 高潮时刻: The finale: five real-looking screens lift into a tilted wall while the tagline is spoken once after a half-beat of silence; the last one, the forest plot, resolves to a single clean rerun button. It lands at about 65 % of the film.
- Hook line · 开场句: A reviewer asks one question: can you run it again?
- Hero line · 高潮句: Quartile: every result, ready to rerun.
- Last line · 收尾句: Yes. Run it again, any time.
- Title · 片名: Run it again

## 4. Copywriter · 文案
- Tagline · 口号: 每个结果，都能重跑 / Every result, ready to rerun
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "A reviewer asks one question: can you run it again?"
  - feature (forest plot) → "Pool the studies with a fixed or random effect, and see how much they disagree: I squared."
  - feature (ROC) → "Diagnostic accuracy: the ROC curve, the AUC, and its 95% confidence interval, in one figure."
  - statement → (no voice: a breath between proofs, the caption carries it)
  - feature (survival) → "Survival curves arrive with their log-rank test and the numbers still at risk."
  - clip → (no voice: the screen speaks for itself, the title names the action)
  - phone → "Your saved analyses wait for you on the phone."
  - finale → "Quartile: every result, ready to rerun."
  - endcard → "Yes. Run it again, any time."
- On-screen words · 画面文字: Cover: 分析可以再跑 / the reviewer's question. Feature titles: 固定与随机效应，同一张图 / Fixed and random effects, one plot; ROC 曲线与 AUC 置信区间 / ROC and AUC with 95% CI; Kaplan–Meier 曲线与风险人数 / Kaplan–Meier curves and numbers at risk; 载入表格，选定分析 / Load a spreadsheet. Pick the analysis.; 手机上的已保存分析 / Saved analyses, on the phone. Statement: 一张桌面，三种证据 / One desk. Three ways to see the evidence. Endcard: a demo label, see contacts.
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés

## 5. Art director · 美术指导
- Look · 视觉: paper-academic: white paper, black ink, one accent colour taken from the logo: the teal of the logo mark (#2EE6C8 family), used only for the one thing the voice is talking about. Two typefaces at most (the style sets them).
- Images · 画面选择: The cover uses the forest plot, because it is the most specific image and reads as a question at a glance. Feature 1 uses the forest plot (meta-analysis, I²); feature 2 uses the ROC curve (AUC); feature 3 uses the survival curve (Kaplan–Meier). The screen recording is the clip, with no voice, so the film shows the product working once. The phone image is the phone beat. The finale wall uses the five images in the order forest, phone, ROC, survival, workspace; the forest plot is the last one, so the hero resolves on it. The best image, the forest plot, is saved for the cover and the finale; it is not used in the middle.
- Composition rules · 构图: Margins ≥ 96 px. One focal point per frame: one plot or one screen, with one highlighted rectangle per point. Text sits in the clear band below or beside the image, never on top of a curve. Captions stay clear of the chapter label.
- We will NOT show · 不出现: globes, handshakes, light bulbs, stock smiles, floating icons, fake dashboards, real patient or clinical photographs, any invented number on screen, any screen that claims a feature the README does not list.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: precision-data — slow, exact moves; holds on the figure; no spin, no bounce. It matches an evidence-first genre.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | |
| 2 | `feature` | 5 | reveal + proof | |
| 3 | `feature` | 5 | reveal + proof | |
| 4 | `statement` | 2 |  | |
| 5 | `feature` | 5 | reveal + proof | |
| 6 | `clip` | 2 | it really runs | |
| 7 | `phone` | 3 | everywhere | |
| 8 | `finale` | 4 | hero | |
| 9 | `endcard` | 3 | close | |

- Cuts · 转场: Hard cut into the cover; one soft push into feature 1; cut into the clip to show the product running; the only whip is into the finale, where the hero moment turns the film.
- Breathing room · 留白: After the two dense feature beats (forest, ROC, survival), the statement is the calm beat; it holds for two bars with no image, so the viewer can take in the proposition.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: Original minimal-electronic underscore at about 104 BPM, composed by `make_music.py`. It stays quiet and steady through the proof beats, rises gently into the clip, then drops to a single held pad before the hero.
- Silence · 静默: A half-beat of silence before the finale line ("Quartile: every result, ready to rerun.") and a held breath after the cover question.
- Sound palette · 音效: Low, dry clicks for the figure reveals (one per feature), no sound on the statement, one soft tone for the rerun button at the end. No whooshes and no risers beyond the one at the hero.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - Desktop statistics for clinical researchers → README line 1.
  - Kaplan–Meier, log-rank test, numbers at risk → README, survival bullet.
  - ROC with AUC and 95% CI → README, diagnostic accuracy bullet.
  - Forest plots, fixed and random effects, I² heterogeneity → README, meta-analysis bullet.
  - Every result exports as a reproducible R script → README bullet 4.
  - Figures at 300 or 600 DPI → README bullet 5.
  - Your data never leaves the computer, Mac or Windows → README bullet 6.
  - Phone companion lists your saved analyses → README bullet 7.
  - "I squared" explained as "how much they disagree" is a plain-language gloss of I² heterogeneity, not a new number.
- Legibility & access · 可读与无障碍: Captions on for every spoken line (zh and en); contrast of the accent on white is checked; nothing important sits under a caption.
- Sign-off · 签字: approved for a demo cut, with the end-card demo label; changes needed before any public release that uses real screens and real analyses.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | One proposition runs through cover, hero and last line: the result can be run again. Supporting features stay on it. |
| Hook in 3 s · 三秒抓人 | 4 | A question a researcher has actually been asked, over a figure, in the first three seconds. |
| Specific, true copy · 具体真实 | 4 | Most spoken lines carry a README fact (log-rank, AUC with 95% CI, I², R script, saved analyses). Two lines are deliberately mood (statement, last line). |
| Image quality & choice · 画面 | 4 | Each beat has one image, the best one is kept for the cover and the finale, and each highlight points at what the line names. The screens are placeholders, which limits the score and is stated in §1 Gaps. |
| Restraint · 克制 | 5 | One hero, one accent colour, a calm statement beat, no effects beyond the figure reveals. |
| Rhythm · 节奏 | 4 | Three feature beats are separated by a breath and a clip; no three identical beats in a row. |
| Hero moment · 高潮 | 4 | The wall of five screens lands on the forest plot and the tagline after a half-beat of silence. |
| Memorable ending · 结尾记忆点 | 4 | The last line calls back to the hook word for word, with one change: "Yes." |
