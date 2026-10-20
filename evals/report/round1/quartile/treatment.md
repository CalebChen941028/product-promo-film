# Treatment · 创意方案 — Quartile

> Written by the crew in `references/crew.md`, one section per role, in order.
> `python3 scripts/check_treatment.py treatment.md film.json` must pass before `make_film.py --stage build`.

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: Quartile
- Genre · 类型: science-data — Science, research, data analysis / 科研 / 数据分析 / 统计
- Look · 风格: paper-academic · Motion · 动效: precision-data · Arc · 叙事结构: problem-solution
- Music · 音乐: composed: minimal-electronic ~104 BPM (original, royalty-free)
- Materials · 素材: desktop 4, logo 1, phone 1, text 1, ui 5, video 1
- Target length · 目标时长: ~77 s (29 bars + end card)
- Tone for this genre · 本类型的语气: exact, modest, evidence first; numbers must be checkable

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Clinical researchers and graduate students; sound-off social and product page first, sound-on for lab meetings. Landscape 1080p only for now.
- Rights · 授权: All screens and figures are the project's own wireframe placeholders (per the materials README). Music is composed for this film (no third-party track). No quotes, no photos of people. Logo supplied by the product team.
- Gaps · 缺口: No real product captures yet. The film is labelled as a demo with placeholder screens, and it will be re-cut with real captures before any public launch. No voice-over yet (Kokoro not installed); captions carry the narration.

## 2. Strategist · 策略
- Audience truth · 受众真相: "Every figure in my paper has to survive a reviewer, and I still rebuild the same tables by hand."
- Insight · 洞察: The analysis is quick; the trust is slow. Reviewers want to rerun what you ran, and the figure has to be publishable at 300 DPI.
- Single-minded proposition · 唯一主张: Publication-ready statistics, and the data never leaves your computer.
- Proof · 证据: (1) Kaplan–Meier curves with log-rank test and numbers at risk; (2) ROC curves with AUC and 95% CI; (3) forest plots with fixed and random effects and I²; every result exports as a reproducible R script; figures at 300 or 600 DPI; runs on your own Mac or Windows PC.

## 3. Creative director · 创意总监
- Concept A: Reviewer's eye — the film opens on a figure and asks whether a reviewer could rerun it; every scene answers with a checkable step. Opening image: a forest plot filling the frame.
- Concept B: Quiet desk — the whole film happens on one desk; each analysis is a drawer that opens. Opening image: an empty workspace.
- Concept C: Ledger — numbers written into a paper ledger, one line each. Opening image: a table line being typed.
- Chosen · 选定: A. It is the most true (it names the reviewer, a real pressure) and the most specific (a figure that can be rerun). B is pleasant but generic; C is clever but hides the product.
- Hook (0–3 s) · 开场钩子: Macro crop on one forest-plot marker and its confidence line (texture before the whole), then a slow pull back to the full plot. One spoken line: "Every figure should survive a reviewer." Captions in zh and en.
- Hero moment · 高潮时刻: The finale, five analyses laid out side by side in one frame, held for one bar before the tagline. It lands at about 60–70 % of the film.
- Title · 片名: Quartile — Reviewer-ready

## 4. Copywriter · 文案
- Tagline · 口号: 投稿级统计，数据留在本机 / Statistics ready for publication. Your data stays here.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s): (cover) Every figure should survive a reviewer. (feature 1) Kaplan–Meier curves, log-rank test and numbers at risk, in one run. (feature 2) The ROC curve, the AUC and its 95% confidence interval. (feature 3) Forest plots with fixed and random effects, and I² heterogeneity. (clip) One analysis, one table, one figure. (phone) Your saved analyses, on the phone. (finale) Statistics ready for publication. Your data stays here. (end card) Every result, reproducible.
- On-screen words · 画面文字: 生存分析 / Survival analysis; Kaplan–Meier 曲线与风险人数; Log-rank 检验; 诊断准确性 / Diagnostic accuracy; ROC 曲线与 AUC; AUC 的 95% 置信区间; Meta 分析 / Meta-analysis; 固定与随机效应模型; I² 异质性; 一次分析，一张表，一张图; 手机上查看已保存的分析; DEMO · 演示画面（占位线框）
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés

## 5. Art director · 美术指导
- Look · 视觉: paper-academic style — white and cool-grey paper, black axes, the product's teal (#2EE6C5-range, from the logo) as the single accent colour; a second data colour (blue) only inside figures.
- Images · 画面选择: cover = forest plot, blurred behind the logo; detail = macro crops of two forest-plot rows (the marker and its CI line); feature 1 = survival curves; feature 2 = ROC curve; feature 3 = forest plot with I² point; clip = scrolling results walkthrough; phone = phone-results; finale = all five panels; hero = the finale frame. The workspace wireframe is not used, because it shows no real output.
- Composition rules · 构图: margins ≥ 96 px; text never over a figure's data region; one focal point per frame; captions in the lower safe area.
- We will NOT show · 不出现: globes, handshakes, stock researchers smiling at laptops, glowing brains, fake dashboards with invented numbers, any real-looking patient data, any claim that the screens are real captures.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: precision-data — figures draw in along their true axes, no bounce, no spin; each draw is a single ease-out.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | forest plot blurred behind the logo |
| 2 | `detail` | 2 | macro hook | crops on one marker and its CI line |
| 3 | `feature` | 5 | reveal + proof | survival curves |
| 4 | `feature` | 5 | reveal + proof | ROC curve |
| 5 | `feature` | 5 | reveal + proof | forest plot and I² |
| 6 | `clip` | 2 | it really runs | scrolling results |
| 7 | `phone` | 3 | everywhere | saved analyses |
| 8 | `finale` | 4 | hero | five panels, tagline |
| 9 | `endcard` | rest | close | motto and demo label |

- Cuts · 转场: Hard cuts only at bar lines. Cut from the forest plot (cover) to survival (feature 1) when the voice says "survival"; no cross-dissolves inside the feature run.
- Breathing room · 留白: One rest between feature 3 and the clip (the bar before the clip is empty grey paper for half a bar), and the held frame before the hero.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed minimal-electronic, ~104 BPM, original (make_music.py). Builds gently through the features, drops to a single pulse for the clip, returns for the finale.
- Silence · 静默: Half a beat of silence before the finale; the hero is held in that silence.
- Sound palette · 音效: Very low. A soft tick on each figure draw. No whooshes, no risers, no sound on the logo.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - KM curves, log-rank, numbers at risk → README "Survival analysis"
  - ROC, AUC and 95% CI → README "Diagnostic accuracy"
  - Forest plot, fixed and random effects, I² → README "Meta-analysis"
  - Reproducible R script export → README bullet 4
  - 300 or 600 DPI figures → README bullet 5
  - Runs on own Mac or Windows PC; data never leaves the computer → README bullet 6
  - Phone companion lists saved analyses → README bullet 7
  - Tagline and proposition are derived from the above; no performance numbers used.
- Legibility & access · 可读与无障碍: captions on for every beat; text contrast ≥ 4.5:1 against paper; nothing important sits under captions.
- Sign-off · 签字: approved for a demo cut, with the DEMO label visible on the end card and the on-screen placeholder note; changes needed before any public launch: replace placeholder screens with real captures.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | One claim: reviewer-ready statistics on your own computer. |
| Hook in 3 s · 三秒抓人 | 4 | A forest plot drawn from the centre line, with one line of voice. |
| Specific, true copy · 具体真实 | 4 | Every line maps to a README feature; no superlatives. |
| Image quality & choice · 画面 | 4 | The opening is a macro crop of real figure output, not decoration. The data is placeholder, so it cannot be a 5 yet. |
| Restraint · 克制 | 4 | Only one tick sound per figure; no decorative effects. |
| Rhythm · 节奏 | 4 | Three features at equal length, one calm clip, then the finale. |
| Hero moment · 高潮 | 4 | Five panels in one frame, held in silence. |
| Memorable ending · 结尾记忆点 | 4 | "Every result, reproducible." after the tagline. |
