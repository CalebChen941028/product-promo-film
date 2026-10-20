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
- Target length · 目标时长: ~72 s (28 bars + end card)
- Tone for this genre · 本类型的语气: exact, modest, evidence first; numbers must be checkable
- Study first · 先读: `templates/golden/problem-solution.json` (a top film in this arc, every scene with a `_why`) and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: A desktop research-statistics workbench for clinical medicine and public health. Data upload and cleaning, statistical analysis, figures, Word reports and reproducible R scripts are done in one workspace. · Survival analysis: Kaplan–Meier curves with numbers at risk · ROC curves, meta-analysis forest plots, Cox and logistic regression · Results export as reproducible R scripts and Word reports (Pro edition) · Optional AI interpretation of the results; with a local model (Ollama, LM Studio) nothing leaves the computer · Runs on macOS (Apple silicon) and Windows 10/11 x64, with R installed locally · Current release: internal beta (Preview)

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Clinical researchers and graduate students in medicine and public health. Plays as a 16:9 landscape film for the internal beta group, mostly with sound off, so captions are on.
- Rights · 授权: All screens are MedStat Pilot's own interface captured with synthetic demo data (demo_trial.csv, demo_meta.csv). The logo is the product logo. Music is composed by make_music.py (original). Voice is Kokoro am_michael. No quotes, testimonials or third-party photos. Confirmed with the user? No: the run was unattended, so these are assumptions listed in the report.
- Gaps · 缺口: No testimonial, no contacts, no price and no Windows screenshot in the materials, so the Windows claim appears only as a chip. Nothing invented to fill these gaps; the film is labelled beta.

## 2. Strategist · 策略
- Audience truth · 受众真相: When a reviewer asks how I got this number, I have to go back and find the clicks.
- Insight · 洞察: Point-and-click analysis is fast, but its method lives in clicks nobody can replay, so the result is only as credible as the path a reviewer can rerun.
- Single-minded proposition · 唯一主张: The analysis, written down as code you can rerun.
- Proof · 证据: (1) Results export as reproducible R scripts and Word reports (README). (2) Kaplan–Meier curves with numbers at risk, and an APA three-line table, on one analysis screen (README and the KM screen). (3) Runs on macOS (Apple silicon) and Windows 10/11 x64 with R installed locally (README).

## 3. Creative director · 创意总监
- Concept A: The reviewer's question — the film opens on the question every reviewer asks, then answers it with the product. Opening image: the KM analysis screen, held calm. Why it fits: the audience has been asked this exact question.
- Concept B: Clicks become code — each analysis step is written out as an R line. Opening image: a survival curve, then the code panel. Why it fits: true to the R export, but the line-by-line mechanism is not on screen in the materials, so it would promise more than we can show.
- Concept C: Numbers with their address — every number points back to its table and its method. Opening image: the APA table. Why it fits: true, but abstract; it reads like a spec sheet.
- Chosen · 选定: A. It is the most surprising because the film starts with a reviewer, not the product, and the most true because the product's job is to answer that question, which the R export and the KM table can show.
- Hook (0–3 s) · 开场钩子: The full KM analysis screen holds calm for a second, then pushes into the results panel with the survival curve. Voice: "The reviewer asked how. Nobody remembered the clicks."
- Hero moment · 高潮时刻: The KM survival curve with its numbers at risk rises out of the blurred analysis screen from the hook, on the downbeat after a half-beat of silence. It holds alone for about 3 seconds, then the name and tagline appear. It lands at bar 25 of about 31 (about 80 % of the runtime, later than the 60–70 % rule of thumb) because the proof must land first; the golden problem-solution film is built the same way.
- Hook line · 开场句: The reviewer asked how. Nobody remembered the clicks.
- Hero line · 高潮句: MedStat Pilot. The analysis, written as code.
- Last line · 收尾句: The reviewer asks how. Run the script.
- Title · 片名: How did you get this number? · 这个数字怎么来的？

## 4. Copywriter · 文案
- Tagline · 口号: 分析过程，写成代码 / The analysis, written as code.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "The reviewer asked how. Nobody remembered the clicks." (zh: 审稿人问，这个数字怎么来的。没人记得点过哪些按钮。)
  - feature 1 → "Upload the data and clean it in the same workspace." (zh: 数据上传与清洗，在同一个工作台完成。)
  - detail → "The table is ready for the paper. Export the report or the R code from the same screen." (zh: 三线表可直接放进论文；同一屏导出报告或 R 代码。)
  - statement → (no voice: the text is the breath; the room is quiet for two bars)
  - feature 2 → "Survival curves come with their numbers at risk, so the reader sees who is left." (zh: 生存曲线下方附风险人数表，读者能看到每个时点还剩多少人。)
  - carousel → "The same workbench draws survival curves, ROC curves and forest plots." (zh: 同一个工作台里，也能画 ROC 曲线与森林图。)
  - finale → "MedStat Pilot. The analysis, written as code." (zh: MedStat Pilot：分析过程，写成代码。)
  - endcard → "The reviewer asks how. Run the script." (zh: 审稿人问怎么算的，运行这段脚本即可。)
- On-screen words · 画面文字:
  - cover chapter: 演示数据 / DEMO DATA
  - feature 1 title: 拖入数据，先核对变量 / Drop the data. Check the variables.
  - feature 1 points: 读取 .sav .csv .xlsx .dta / Reads .sav, .csv, .xlsx, .dta; 分析前核对变量 / Check variables before analysis
  - detail crops: 三线表 / APA three-line table; 导出与 R 代码 / Export and R code
  - statement: 结果会被读，方法会被查。 / Results get read. Methods get checked.
  - feature 2 title: 生存曲线与风险人数表 / Survival curves with numbers at risk
  - feature 2 points: 风险人数表 / Numbers at risk; 两组曲线同图对照 / Both groups on one figure
  - carousel panels: 生存曲线 / Survival; Meta 森林图 / Forest plot; ROC 曲线 / ROC curve
  - finale tagline: MedStat Pilot — 分析过程，写成代码 / The analysis, written as code.
  - endcard motto: 审稿人问怎么算的， / 运行这段脚本即可。 / The reviewer asks how. Run the script.
- Banned words checked · 已排除空话: yes — lint_copy.py to be run on film.json; no superlatives, no "revolutionary", no "seamless".

## 5. Art director · 美术指导
- Look · 视觉: paper-academic: a light paper ground, dark ink text, one accent colour, the teal from the logo. Two typefaces at most, set by the style.
- Images · 画面选择:
  - cover: km.png (the analysis screen), focus on the KM result panel. This is the hook's image, and it returns as the hero's backdrop.
  - feature 1: home.png (the drop zone and the format list), with rects on the format line and the variable-check hint.
  - detail: km.png, two crops, the APA three-line table and the export buttons, each zoomed so it reads at film size.
  - feature 2: km_plot.png, the KM figure with the risk table, rects on the risk table and on the two curves.
  - carousel: km_plot, meta_plot (forest plot), roc_plot (ROC), each cropped to the figure.
  - finale: km_plot.png rises out of km.png; the cover screen is the hero's backdrop, a callback.
  - endcard: logo, name, positioning.
  - The T-test screen (ai_final.png) and the R-script warning screen (r_code.png) are not used: one shows an interface warning, and the other has too much small text for film scale.
- Composition rules · 构图: margins at least 96 px; text on the left third, the screen or figure on the right; one focal point per frame; captions at the bottom third, clear of the figure.
- We will NOT show · 不出现: the R-script download warning dialog; any real patient data; the Pro gate badges; fake UI or fake result numbers; globes, handshakes, stock lab coats, floating icons.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: precision-data — crisp measured pushes, numbers resolve in place, the hero rises out of a blurred backdrop. No flourishes, no bounce.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 4 | hook | full screen calm, then push into the KM panel |
| 2 | `feature` | 5 | reveal + proof | drop zone and the supported formats |
| 3 | `detail` | 5 | proof, new shape | two zoomed crops: the APA table, the export buttons |
| 4 | `statement` | 2 | breath | text only, no picture, no new fact |
| 5 | `feature` | 5 | reveal + proof | KM figure with numbers at risk |
| 6 | `carousel` | 3 | breadth | survival, forest plot, ROC: one workbench |
| 7 | `finale` | 4 | hero | the KM curve rises out of the hook's screen |
| 8 | `endcard` | rest | close | callback to the reviewer's question |

- Cuts · 转场: cut into feature 1 (the story turns from the question to the product), cut into the finale (the hero), cut into the end card. Everything else is a plain dissolve inside the scene.
- Breathing room · 留白: after the two dense proof beats (feature 1, detail), a two-bar statement with no picture. It names the feeling before the figure arrives.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: original composed minimal-electronic at about 104 BPM via make_music.py. The pulse builds through the carousel, drops to near silence on the statement, and rises again into the finale.
- Silence · 静默: the half-beat before the hero downbeat; the two bars of the statement.
- Sound palette · 音效: kept low. A soft tick on the hook line, and the default soft hit on the hero. The rest stays quiet, because the film should be felt, not heard.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "desktop research-statistics workbench for clinical medicine and public health" → README
  - "Kaplan–Meier curves with numbers at risk" → README; the KM screen shows the number-at-risk table
  - "reads .sav, .csv, .xlsx, .dta" → the home screen's format list (.sav / .csv / .xlsx / .dta among others)
  - "check the variables before analysis" → the home screen's hint: read the data, check the variable recognition, then analyse
  - "APA three-line table" → the KM result screen shows the "APA 三线表" heading
  - "export the report or the R code" → README (reproducible R scripts and Word reports); the export buttons are visible on the screen
  - "survival, ROC and forest plots" → README; the screens show each figure
  - "macOS (Apple silicon) and Windows 10/11 x64" → README; shown as chips only, not in the voice-over
  - "beta" → README; the Beta chip on the end card
  - Demo data → every screen is captured with synthetic demo data; the cover carries a DEMO DATA chapter label
- Legibility & access · 可读与无障碍: captions on for every line; contrast is high on the paper ground; nothing important sits under a caption; screen text is zoomed to at least 18 px.
- Sign-off · 签字: approved with the changes above built in (the demo label, the beta chip, no unverified claims in the voice-over).

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | One question, one answer. The proposition ("written as code you can rerun") is in the hook, the hero and the last line. |
| Hook in 3 s · 三秒抓人 | 4 | A reviewer's question over a real analysis screen. It creates tension in the first three seconds. |
| Specific, true copy · 具体真实 | 4 | Each proof line names a file type, a table, a figure or a feature visible in the materials. Nothing is inflated. |
| Image quality & choice · 画面 | 4 | Real screens, zoomed to the readable parts. The hero reuses the hook's own screen. Limited by screenshots only, with no real photography, so not a 5. |
| Restraint · 克制 | 4 | Calm measured motion, one hero, a breath before it. The chips carry the platform facts so the voice does not list them. |
| Rhythm · 节奏 | 4 | Two proof beats are followed by a breath, then a figure and a carousel; no three identical beats in a row. |
| Hero moment · 高潮 | 4 | The KM plot rises out of the hook's screen, a real callback. Lands later than the rule of thumb because the proof must land first. |
| Memorable ending · 结尾记忆点 | 4 | "The reviewer asks how. Run the script." echoes the hook word for word and lands on the viewer. |
