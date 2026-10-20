# Treatment · 创意方案 — MedStat Pilot

> Written by the crew in `references/crew.md`, one section per role, in order. Replace every `write` field.
> `python3 scripts/check_treatment.py treatment.md film.json` must pass before `make_film.py --stage build`.
> 由 `references/crew.md` 中的各角色依次填写；替换所有 `write` 字段，检查通过后再构建。

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: MedStat Pilot
- Genre · 类型: science-data — Science, research, data analysis / 科研 / 数据分析 / 统计
- Look · 风格: paper-academic · Motion · 动效: precision-data · Arc · 叙事结构: problem-solution
- Music · 音乐: composed: minimal-electronic ~104 BPM (original, royalty-free)
- Materials · 素材: desktop 8, logo 1, text 1, ui 8
- Target length · 目标时长: ~92 s — 8 images/clips carry about 92 s; the problem-solution arc would run 100 s with more material. Do not pad: no repeats, no long holds
- Tone for this genre · 本类型的语气: exact, modest, evidence first; numbers must be checkable
- Study first · 先读: `templates/golden/problem-solution.json` (a top film in this arc, every scene with a `_why`) and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: A desktop research-statistics workbench for clinical medicine and public health. Data upload and cleaning, statistical analysis, figures, Word reports and reproducible R scripts are done in one workspace. · Survival analysis: Kaplan–Meier curves with numbers at risk · ROC curves, meta-analysis forest plots, Cox and logistic regression · Results export as reproducible R scripts and Word reports (Pro edition) · Optional AI interpretation of the results; with a local model (Ollama, LM Studio) nothing leaves the computer · Runs on macOS (Apple silicon) and Windows 10/11 x64, with R installed locally · Current release: internal beta (Preview)

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Researchers, graduate students and clinical or public-health analysts who run survival, ROC and meta-analyses. Plays as a product intro on the web and to beta testers; sound on (composed underscore), bilingual captions on.
- Rights · 授权: All screens and the logo are the product's own captures, made with synthetic demo data (per the materials README). Music: original underscore composed by make_music.py (no web track). Voice: Kokoro am_michael (Apache-2.0, already downloaded, no new download). No people, no patient data, no quotes.
- Gaps · 缺口: No real photos, no user quote, no web address or contact in the docs, and no Windows screen (Windows appears only as a platform chip). None of these is faked: the film stays on real UI and real outputs, and the end card carries no contact line.

## 2. Strategist · 策略
- Audience truth · 受众真相: "When a reviewer asks how I got this number, I have to rebuild the analysis from memory."
- Insight · 洞察: Running the analysis is fast. Defending it is slow. Researchers want to show their work, not only their result.
- Single-minded proposition · 唯一主张: Every result comes with the R script that produced it.
- Proof · 证据:
  1. Results export as reproducible R scripts (docs: "Results export as reproducible R scripts and Word reports").
  2. Upload, cleaning, analysis, figures and reports are done in one workspace (docs: "Data upload and cleaning … in one workspace").
  3. Kaplan–Meier curves with numbers at risk, ROC curves, meta-analysis forest plots, Cox and logistic regression (docs).
  4. Optional AI reading: with a local model, nothing leaves the computer (docs). Not narrated in this film.

## 3. Creative director · 创意总监
- Concept A: The reviewer's question. One line: the film opens on a real result with its R-code button and asks the question every reviewer asks; the answer is the script, one click away. Opening image: the result screen (APA table, R 代码 button, AI reading).
- Concept B: One workspace. One line: a tour of the product from an empty upload window to finished outputs. Opening image: the home screen with its empty drop zone.
- Concept C: Nothing leaves the computer. One line: privacy as the point, shown through the optional AI reading on a local model. Opening image: the AI interpretation panel.
- Chosen · 选定: A. It is the most true (the R-script export is a real feature visible on the result screen) and the most specific to this audience. B is a feature tour the audience has seen before. C depends on a local model being used, so it is a conditional claim, not a headline.
- Hook (0–3 s) · 开场钩子: Full-bleed result screen (the APA table and the R 代码 button), slow push toward the table; the voice asks the question. The first image is a real analysis, not a logo.
- Hero moment · 高潮时刻: The same result screen returns at about 70 % of the film and pushes in until the tagline settles above it. It is the callback to the cover: the answer, shown whole, with its script.
- Hook line · 开场句: A reviewer asks how you got that number.
- Hero line · 高潮句: MedStat Pilot. Every result, with its script.
- Last line · 收尾句: The reviewer asks. The script answers.
- Title · 片名: Every Result, With Its Script

## 4. Copywriter · 文案
- Tagline · 口号: 每个结果，都有脚本可查 / Every result, with its script.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "A reviewer asks how you got that number." (zh: 审稿人问：这个数字怎么来的？)
  - feature (home) → "Drop in your data file. Upload, cleaning and analysis stay in one workspace." (zh: 拖入数据文件，就在同一个工作区里开始分析。)
  - feature (tool) → "Calculate and recode variables in one panel, then run the analysis on the cleaned data." (zh: 在一个面板里计算、重编码变量，再用整理好的数据做分析。)
  - statement → no voice: a breath after two dense beats; the feeling only, no new fact.
  - carousel → "ROC curves and meta-analysis forest plots, from the same data." (zh: ROC 曲线与 Meta 森林图，来自同一份数据。)
  - feature (km) → "Kaplan–Meier curves, with numbers at risk. Every result exports as a reproducible R script." (zh: Kaplan–Meier 曲线与风险人数。每个结果可导出可复现的 R 脚本。)
  - finale → tagline on screen, caption hidden: "MedStat Pilot. Every result, with its script."
  - endcard → "The reviewer asks. The script answers." (zh: 审稿人问，脚本来答。)
- On-screen words · 画面文字: feature titles and points as in film.json, each ≤ 42 chars (en) / ≤ 12 字 (zh).
- Banned words checked · 已排除空话: yes, lint_copy.py reports copy OK.

## 5. Art director · 美术指导
- Look · 视觉: paper-academic. Light, calm, one accent colour: the teal of the logo. Nothing else is coloured.
- Images · 画面选择:
  - cover: ai_final.png (the result screen: the question sits over the real number and its script);
  - feature 1: home.png (the empty drop zone: where every analysis starts);
  - feature 2: tool_compute.png (the calculation and recoding panel: data cleaning);
  - statement: no image;
  - carousel: meta_plot.png and roc_plot.png (two more real outputs, demo data);
  - feature 3: km.png (the Kaplan–Meier screen with its numbers-at-risk table);
  - finale: ai_final.png again, the best real result, saved for the hero and returned to as a callback.
  - Not used: r_code.png, because its screen shows an error banner (a failed R-script download), and an error state must not serve as proof of a feature.
- Composition rules · 构图: margins ≥ 96 px; one focal point per frame; point labels sit beside the highlighted region, not on it. Highlight boxes only where a point names a region.
- We will NOT show · 不出现: globes, handshakes, stock people, invented charts, hand-drawn UI, dashboards with fake numbers, any screen that shows an error state.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: precision-data. Measured push-ins, rectangles that highlight a region, no decorative motion. It fits a film about checkable results.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | the question over the real result |
| 2 | `feature` | 5 | reveal + proof | the start: upload |
| 3 | `feature` | 5 | reveal + proof | the cleaning step |
| 4 | `statement` | 2 | breath | calm after two dense beats |
| 5 | `carousel` | 3 | breadth | two more outputs |
| 6 | `feature` | 5 | reveal + proof | Kaplan–Meier with numbers at risk; the R script |
| 7 | `finale` | 4 | hero | the result returns, pushes in, the tagline lands |
| 8 | `endcard` | rest | close | callback to the hook |

- Cuts · 转场: Hard cut into the cover; default cut into the carousel; push into the finale, the only camera move that is not a plain cut. No whip, no flash.
- Breathing room · 留白: The statement after the two cleaning beats. It is the one beat with no picture, so it reads as a pause, not a gap.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed, minimal-electronic, ~104 BPM (original, royalty-free, from make_music.py). It starts under the cover, lifts a little into feature 2, sits low through the carousel, and opens fully on the finale.
- Silence · 静默: Half a beat of silence before the hero line, so the tagline arrives into quiet.
- Sound palette · 音效: Soft tick on each highlight box only. No sound on the statement. Design sound stays well under the voice.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "one workspace: upload, cleaning, analysis, figures, reports, R scripts" → docs README;
  - "Kaplan–Meier with numbers at risk" → docs README and km.png (risk table visible);
  - "ROC curves and meta-analysis forest plots" → docs README and roc_plot.png and meta_plot.png;
  - "each result exports as a reproducible R script" → docs README ("Results export as reproducible R scripts") and the R 代码 button on ai_final.png;
  - "Every result, with its script" → the same export claim applied to each result view. It is a claim about the export, not a guarantee that every script runs in every environment.
  - Cox, logistic regression and the local AI reading are in the docs but not narrated, so nothing is claimed that the screens do not show.
- Legibility & access · 可读与无障碍: Bilingual captions on; on-screen labels within 42 characters (en) / 12 字 (zh); nothing important under captions.
- Demo labelling · 演示标注: Screens use synthetic demo data (materials README). The end card carries a "Demo data · 演示数据" chip so no one reads a demo table as a real study.
- Status · 状态: The end card says "Internal beta · 内测版". The film does not claim general availability.
- Sign-off · 签字: approved for internal review. Before any public release: real photos, a real user quote with consent, and Windows screens if Windows is to be shown.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | One proposition (every result, with its script) is said in the hook, the hero and the last line. |
| Hook in 3 s · 三秒抓人 | 4 | A question every researcher knows, over a real result with its R-code button. |
| Specific, true copy · 具体真实 | 4 | Each proof line carries a documented fact: R script export, numbers at risk, ROC, forest plots, workspace. |
| Image quality & choice · 画面 | 4 | Each beat has the best real screen in the folder; the result screen is saved for the hero; the error-banner screen is excluded. Source limits (no photos) are in Gaps, not in this score. |
| Restraint · 克制 | 4 | One hero, one accent colour, calm statement beat, no effects beyond the push. |
| Rhythm · 节奏 | 4 | Hook, dense beat, dense beat, breath, breadth, proof, hero, close. No three identical beats in a row. |
| Hero moment · 高潮 | 4 | The result returns as a callback and pushes in; it is the one screen that holds the whole claim. |
| Memorable ending · 结尾记忆点 | 4 | The callback to the question: "The reviewer asks. The script answers." |
