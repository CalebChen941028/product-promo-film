# Treatment · 创意方案 — MedStat Pilot

> Written by the crew in `references/crew.md`, one section per role, in order.

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: MedStat Pilot
- Genre · 类型: science-data — Science, research, data analysis / 科研 / 数据分析 / 统计
- Look · 风格: paper-academic · Motion · 动效: precision-data · Arc · 叙事结构: problem-solution
- Music · 音乐: composed: minimal-electronic ~104 BPM (original, royalty-free)
- Materials · 素材: desktop 8, logo 1, text 1, ui 8
- Target length · 目标时长: ~92 s
- Tone for this genre · 本类型的语气: exact, modest, evidence first; numbers must be checkable
- Study first · 先读: `templates/golden/problem-solution.json` and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: desktop research-statistics workbench for clinical medicine and public health · data upload, cleaning, analysis, figures, Word reports and reproducible R scripts in one workspace · Kaplan–Meier curves with numbers at risk · ROC curves, meta-analysis forest plots, Cox and logistic regression · results export as reproducible R scripts and Word reports (Pro edition) · optional AI interpretation; with a local model (Ollama, LM Studio) nothing leaves the computer · macOS (Apple silicon) and Windows 10/11 x64, R installed locally · internal beta (Preview)

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: clinical and public-health researchers who run survival, ROC and meta-analyses. Played as a product film, sound on or off; the voice-over is captioned in both languages, so it works muted.
- Rights · 授权: logo and screenshots are the product's own (from the materials README: captured with synthetic demo data). Music is original, composed by make_music.py. Voice is Kokoro, already installed. No quotes, no third-party photos, no stock. The owner confirms the screenshots may be used publicly.
- Gaps · 缺口: no real product photography (no cut-outs); the only written source is the materials README, so every claim is limited to it; no Windows screenshot; no contacts or website supplied, so the end card carries none. The film says "internal beta" on screen, because the README does.

## 2. Strategist · 策略
- Audience truth · 受众真相: "My results have to hold up when a reviewer asks me to rerun them."
- Insight · 洞察: a number on a slide is only worth as much as the steps behind it; most tools hide those steps, so the result cannot be checked.
- Single-minded proposition · 唯一主张: Every result ships with the figure and the code that made it. (12 words)
- Proof · 证据: (1) Results export as reproducible R scripts (README). (2) Kaplan–Meier curves are drawn with numbers at risk under them (README, screenshot). (3) Data upload to a finished figure happens in one workspace (README).

## 3. Creative director · 创意总监
- Concept A: Results you can rerun — a result is only as good as the steps you can rerun; open on the one sentence every reviewer asks. Opening image: a real analysis screen, the question on top.
- Concept B: Quiet pipeline — one continuous camera that follows a file from import to figure without a cut; opening image: an empty drop zone.
- Concept C: The reviewer's question — the film is a single question asked at each step ("can you rerun that?"); opening image: a p-value line in a table.
- Chosen · 选定: A, Results you can rerun. It is the most true (the README's central claim is reproducibility) and the most specific to researchers; its key word, rerun, is in the hook, the hero and the last line. B is pleasant but says nothing a rival could not say; C turns into a list of features.
- Hook (0–3 s) · 开场钩子: a real AI-interpretation panel fills the frame, the paper-ready paragraph sits in focus; the voice says the first line over the real text, nothing else on screen.
- Hero moment · 高潮时刻: the Kaplan–Meier figure rises out of the blurred analysis window as the one output that matters, landing at about 65 %.
- Hook line · 开场句: "A result you cannot rerun is only an opinion."
- Hero line · 高潮句: "MedStat Pilot. Results you can rerun." (5 words plus name)
- Last line · 收尾句: "Now anyone can rerun the result." — a callback to "rerun" in the hook.
- Title · 片名: Results You Can Rerun

## 4. Copywriter · 文案
- Tagline · 口号: 每个结果，都能重跑 / Results you can rerun.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "A result you cannot rerun is only an opinion." (zh: 无法重跑的结果，只是一个观点。)
  - feature (home) → "Upload your data and clean it, in the same workspace as the analysis." (zh: 上传数据、清洗变量，与分析在同一工作区完成。)
  - detail (tool_compute) → "One line derives a new variable, with row sums and z-scores built in." (zh: 一行公式即可派生新变量，行求和与 Z 分数已内置。)
  - statement → (no voice: a breath before the proof turns to the survival figure; the line is on screen only)
  - feature (km) → "Kaplan–Meier curves, with the numbers at risk printed beneath, so follow-up stays visible." (zh: Kaplan–Meier 曲线下附风险人数表，随访人数一目了然。)
  - carousel → (no voice: four plots carry the beat)
  - finale → "MedStat Pilot. Results you can rerun." (zh: 每个结果，都能重跑)
  - endcard → "Now anyone can rerun the result." (zh: 现在，任何人都能重跑这个结果。)
- On-screen words · 画面文字: home: 从已有的数据文件开始 / Start from the file you already have; tool_compute: 快速公式 / Quick formulas; statement: 数据之后，才轮到判断。 / After the data, the judgement.; km: 生存曲线与风险人数表 / Survival curves with numbers at risk; carousel: 生存曲线 / Survival, 森林图 / Forest plot, ROC 曲线 / ROC curves.
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés.

## 5. Art director · 美术指导
- Look · 视觉: paper-academic, one accent colour taken from the logo (the teal of the logo badge). Light paper ground, dark ink text; the teal is used only on the point being talked about.
- Images · 画面选择: cover = ai_final (the AI paragraph is the claim the hook is about); feature = home (the drop zone and the project card are the two things the points name); detail = tool_compute cropped to the quick-formula row and the function list; feature km = km (the chart with the table); carousel = km_plot, meta_plot, roc_plot; finale = km_plot rising out of ai_final as backdrop. The best screen (km_plot) is saved for the hero.
- Composition rules · 构图: margins ≥ 96 px; one focal point per frame; text sits in the empty paper area, never over a figure.
- We will NOT show · 不出现: globes, handshakes, stock researchers, fake dashboards, invented charts, made-up numbers. The R-code screenshot is left out: it carries a download-failure banner, which is not the message this film wants.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: precision-data — slow pushes into the named region, straight cuts on the bar line; no spinning, no bounce.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 4 | hook | the opinion line over the real AI paragraph |
| 2 | `feature` | 5 | reveal + proof | start from the file; two points |
| 3 | `detail` | 5 | proof, new shape | zoomed crops of quick formulas and functions |
| 4 | `statement` | 2 | breath | the judgement line, no new fact |
| 5 | `feature` | 5 | reveal + proof | survival figure with numbers at risk |
| 6 | `carousel` | 3 | breadth | three plots, no voice |
| 7 | `finale` | 4 | hero | km figure rises; tagline |
| 8 | `endcard` | 3 | close | callback to "rerun" |

- Cuts · 转场: only at the bar line before the feature (2→3) and before the hero; the rest are dissolves inside a scene.
- Breathing room · 留白: the statement beat is the one rest before the survival proof; the carousel is a quiet scan, not a second feature.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed minimal-electronic, ~104 BPM (original). It builds from the statement and drops out for the last half bar before the hero line.
- Silence · 静默: the half-beat before "Results you can rerun." and a held breath after the carousel.
- Sound palette · 音效: a soft tick on each point appears; no sound on the hero figure beyond the riser.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "Reads .sav, .csv, .xlsx and more" → README and home screen (supported formats list).
  - "Quick formulas", "row sums and z-scores" → tool_compute screenshot (row_sum, Z-score visible).
  - "Survival curves with numbers at risk" → README; km screenshot shows the Number at risk table.
  - "Results export as reproducible R scripts" → README (used in the proposition, not in a shot).
  - "Forest plot", "ROC curves" → README names both; panels shown are the product's own output screenshots.
  - "Nothing leaves the computer" with a local model → README. Not used in the film because it needs a local model; it is in the copy bank only if cut back in.
  - "internal beta" → README, shown as a chip.
- Legibility & access · 可读与无障碍: both languages captioned; chart text is read before the push; no important content under captions; contrast of the teal on paper checked against the logo.
- Sign-off · 签字: approved for internal-beta promo use; changes needed if the owner wants Windows shots or a public release statement.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | One proposition, reached in the hook, the hero and the last line. |
| Hook in 3 s · 三秒抓人 | 4 | A real analysis claim over a real screen, a sentence people argue with. |
| Specific, true copy · 具体真实 | 4 | Every proof line names a feature or number that exists in the README or the screenshots. |
| Image quality & choice · 画面 | 4 | Real product output, each beat on its best image; the carousel now crops each plot to its chart area, so no dense screen is shown whole. Placeholder limits (no photos, demo data) are in §1 Gaps. |
| Restraint · 克制 | 4 | One hero, two quiet beats, no decorative effects. |
| Rhythm · 节奏 | 4 | Two dense proofs are split by a breath and a crop, not two identical beats in a row. |
| Hero moment · 高潮 | 4 | The survival figure rising from the window is the one moment to remember. |
| Memorable ending · 结尾记忆点 | 4 | The callback "rerun" lands the hook back on the viewer. |
