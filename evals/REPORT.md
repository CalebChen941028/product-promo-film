# Blind test report: a smaller model with this skill · 小模型盲测报告

English first, 中文在后。Dates: 2026-10-20 to 2026-10-21. Model under test: **Claude Haiku** (as a sub-agent), given one line and nothing else:
`Make a promo film for the product in <folder> using the skill at ~/Desktop/product-promo-film (read SKILL.md and follow it). Output to <dir>.`
Evidence: [`report/`](report): each run's `treatment.md` and `film.json`, contact sheets for the placeholder folders, and every critic's table and blind mapping. How to rerun: [README.md](README.md).

## English

### Verdict (2026-10-21): accepted
**Criterion (agreed with the user after round 9):** films that Haiku makes from one line reach the level of the film Claude Opus made (the reference), judged blind in the same panel, with every honesty gate passing.

**Result: met.** In the acceptance panel (three fresh blind critics, 16–18), both retest films made on the final skill scored above the Opus reference:

| Film | Who made it | Materials | Mean of critics 16–18 |
| --- | --- | --- | --- |
| Reference (Aurel) | Opus | drawn placeholders | 2.96 |
| Humidifier 10a | Haiku, final skill | the user's AI renders, no docs | 3.21 |
| Humidifier 10c | Haiku, final skill | the user's AI renders, no docs | **3.71** |
| Humidifier 9a | Haiku, round-8 skill | the same | 3.67 |
| Larchwood r8 | Haiku | drawn placeholders | **3.71** (critic 16: 4.00, none < 3) |

- 10c beat the reference with all three critics, and 10a with two of three (critic 18: 3.13 vs 3.25).
- Both runs passed every gate, QA had 0 errors, both used the cached voice, both invented no numbers or specs, and both left out the garbled AI clip.
- **Caveat on materials:** the humidifier films use photoreal renders and the reference uses drawn placeholders, so part of their lead is the images (image quality 4.0 vs 2.0). Two comparisons isolate the skill:
  - On the **same folder** as the reference (Aurel, drawn mugs), Haiku's films matched it within critic noise in every panel: 3.25 vs 3.00, 3.33 vs 3.46, and 3.29 / 3.17 vs 3.29.
  - On **other drawn-placeholder folders**, Haiku's Larchwood beat the reference in every panel since round 6.

**Not met:** the original stretch target, "average ≥ 4 from independent critics". No film averages 4. The best are 3.71 (10c and Larchwood), and one critic gave Larchwood a 4.00. The skill author's own scores reached 4.1 in round 3, but that critic is not independent.

### Method
- **Folders:** Aurel (a physical product, drawn mugs; the reference film exists for it), Quartile (desktop software, wireframes), Larchwood (lakeside cabins, drawn photos), MedStat Pilot (eight real screenshots with synthetic data; kept local), and the humidifier (the user's own four AI renders plus a 10 s clip, no docs; kept local).
- **Runs:** a Haiku sub-agent got only the line above, with no other help. Deviations were logged: stalls, nudges, hand edits and downloads.
- **Critics:** fresh Claude Sonnet sub-agents in panels of three. Each saw anonymised, shuffled films with no treatment and no self-scores:
  - a 20-frame sheet from 1.0 s (`evals/sheet.py`);
  - a moments sheet with dense strips of the hook, the hero and the end;
  - the spoken script;
  - the rubric (`references/crew.md` §9).

  They scored eight criteria from 1 to 5. They never saw motion or heard audio.
- **Compare only within one panel.** Each panel rescored the reference next to the new films, and panels differ by up to 0.2 on the same film.

### Scores by panel (mean of three critics)
| Panel | Reference | Aurel | Quartile | Larchwood | MedStat (real screens) | Humidifier |
| --- | --- | --- | --- | --- | --- | --- |
| 1–3 (rounds 1→3–5) | 3.25 | 2.84 → 3.13 | 2.67 → 3.42 | 3.13 → 3.83 | — | — |
| 4–6 (rounds 5 / 6) | 3.00 | 3.25 / 3.08 | 2.96 / 2.96 | 3.17 / 3.50 | — / 2.96 | — |
| 7–9 (rounds 6 / 7) | 3.46 | 3.17 / 3.33 | 2.67 / 3.25 | 3.38 / 3.50 | 2.96 / 3.33 | — |
| 10–12 (rounds 7 / 8) | 3.29 | 3.29 / 3.17 | 2.84 / 2.88 | 3.38 / 3.54 | 3.17 / 3.25 | — |
| 13–15 (round 9) | 2.92 | — | — | 3.50 (r8) | — | 9a 3.58 · 9b 3.17 · 9c 3.42 |
| 16–18 (round 10, acceptance) | 2.96 | — | — | 3.71 (r8) | — | 9a 3.67 · **10a 3.21 · 10c 3.71** |

In panel 1–3, "→" runs from round 1 to the best of rounds 3–5, as means across the critics who saw each film.

### How the runs behave now (round 1 → rounds 3–10)
| | Round 1 | Rounds 3–10 |
| --- | --- | --- |
| Voice-over | 2 of 3 captions only | every run used Kokoro with a voice already downloaded, with 0 downloads |
| Treatment §4 is a real script; the concept reaches the film | 2 of 3 | every run (enforced) |
| Last line | logistics on 1 (dates) | a callback to the hook on every run |
| Self-scores above what the film shows | 2 of 3 | caught by the gate; two runs re-scored one criterion after a block (noted below) |
| Invented numbers or specs | 0 docs to check against | 0 (gated; no number or spec passes without a source the user supplied) |
| SRT delivered | 1 of 3 | every run |
| Stalls | — | round 2: three, all fixed in the skill; round 10: one, from a gate bug (fixed) |

### What changed in the skill (rounds 1–10)
1. **The crew cannot be skipped.**
   - `make_film.py` will not build until `check_treatment.py` passes.
   - The gate checks quality as well as form:
     - proof lines must carry facts;
     - film.json must match the script;
     - the three concepts must differ;
     - the hook, hero and last line must reach the film.
   - Each self-score is capped by what can be measured: long holds, texture or logo cold opens, oversized boxes, same-shape proof beats, detours, a hero with no callback, and spec lists.
2. **Honesty gates.**
   - **Numbers and specs:** every number and spec term needs a source the user supplied (text in the folder, or a screen the brand guardian names). With no docs, the copy may say only what the images visibly show, from the art director's per-image lines in §5.
   - **Limits:** a claim the docs limit (Pro edition, beta, one platform) must state its limit in the same scene.
   - **Place:** indoor words over an outdoor image are blocked, and so is the reverse.
   - **Counters** never pass through false numbers.
3. **Copy to imitate:** five golden films, one per arc, each with a `_why`, plus `references/copy-bank.md` (anchor lines, weak-to-strong rewrites).
4. **Inputs:**
   - autofilm writes the brief from the product's own docs.
   - JPEG photos are classed as photos, and packshots are flagged and kept for the hero.
   - The folder's name counts as a genre hint (added after round 10).
   - Hospitality and home-living words are in the genre keywords.
5. **Screens:**
   - `suggest_rects.py` pre-fills highlight boxes (dialogs, panels, at most a quarter of the screen) and draws none on charts.
   - Zooms are clamped so text reads at ≥ 18 px.
   - A dense screen is shown whole for under 1 s.
6. **Structure and motion:**
   - **Hook first:** a photo cover opens on its subject (`focus`, picked with `subject_grid.py`) and reveals the place by about 3.4 s. A screen cover pushes into a readable region.
   - **Hero:** a staged hero that calls back to the hook. Screens resolve the output on the downbeat. Photo films use a transforming bookend, with the name in the lower third.
   - **Rhythm:** proof shapes vary, there is a breath after two proof beats, and the length follows the materials (about 9 s per image).
7. **Pipeline:**
   - QA must pass on the latest build.
   - Generated files are fingerprinted.
   - The voice runs offline.
   - SRT is always delivered.
8. **Measurement:** `evals/sheet.py` replaced fade-from-black sheets, which had no effect on the hook verdict (3.00 before vs 2.93 after on the same films), and added moments sheets.

### Round log
- **Rounds 1–5** (placeholder folders, critics 1–3): the crew went from decorative to enforced. Voice, SRT, a concept that reaches the film, and honest scores all reached every run. Larchwood rose from 3.13 to 3.83, and Aurel and Quartile improved.
- **Round 6** (critics 4–6): three screen-hero treatments and the real-screens folder. Scores were flat. Full-app screenshots were too dense to read at film scale.
- **Round 7** (critics 7–9): hook first, readable screens and varied proof. Every folder improved (mean 3.05 → 3.35), and Larchwood and Quartile beat the reference with some critics.
- **Round 8** (critics 10–12): measurement fixed, and the hero staged on the hit. Scores were flat, and "hero" stayed at 3. Gates added afterwards: counters, and claims with omitted limits.
- **Round 9** (critics 13–15): the user's own AI renders with no docs. There were no invented specs, the garbled clip was excluded, and the image scores rose to 3.3–3.7. 9a scored 3.58. Fixes: a gate for numbers and specs with no docs, the packshot, casting, then the two-beat cold open and the place check.
- **Round 10** (critics 16–18, acceptance): a retest on the same folder with the final skill.
  - 10c scored 3.71 (hook 3.67, image 4.0), and 10a scored 3.21; critics called 10a's copy slogan-like and noted a reused image.
  - Run 10b was stopped by a gate bug. With no docs, the gate counted nothing as concrete, so it blocked every line. The bug was fixed (the §5 per-image lines and §2 proof now count), and 10c ran on the fixed skill.
  - Both runs had to override autofilm's genre guess (food-beverage) by hand. This was fixed after the round, and autofilm now reads the folder name: `humidifier` gives home living. It has not been re-measured.

### Still open
1. **The hero moment.** No critic yet calls one memorable the next day ("competent, not unforgettable"). It may need real motion material, such as a clip of the product working.
2. **End cards carry no image.** Critics say the line lands but the picture does not.
3. **Run-to-run variance is as large as most skill changes:** 3.21 vs 3.71 on the same folder and skill. A weak concept (a mood such as "the soft hour", rather than one sentence) still passes the gate.
4. **Short films when materials are thin:** 46–52 s on four images. This is honest, but critics notice it.
5. **Placeholder materials cap the image score at about 3.** Real photographs have not been tested; the humidifier materials are AI renders.

### Honesty findings across runs
- **The gates caught:**
  - an omitted Pro-edition limit (round 8, MedStat);
  - an unsourced "95 %" read off a screen (round 7, MedStat);
  - "room" over a tent (round 9b);
  - a test line inventing an 8-hour, 300 ml tank, which raised 8 errors.
- **Not caught by any gate:**
  - 9b calls a lilac glow "warm";
  - 10a says the name twice in a row (hero, then finale).
- **Self-score changes after a block:** two runs re-scored a criterion after the gate blocked them. Round 6 raised an image score, citing the rule to judge staging, not placeholders. Run 10c re-scored copy as a materials gap. Both are within the rules, but they are worth watching.
- **The humidifier materials are AI renders, not photographs of a real product.** Every run said the films are concept pieces, and every run listed what the user must supply: name, logo, spec sheet, and the rights to the renders.

### Notes on this test
- The skill author changed the skill and also scored rounds 1–3. The independent critics exist to check that bias, and they are stricter.
- Round 2 Aurel and Quartile were each nudged once ("your render finished; continue") after they waited on a background monitor. That failure mode was then fixed.
- At the start of round 2, the round-1 evidence sat in the skill folder for about a minute before it was moved out. No run's copy matches it.
- In round 7 the reference film was re-rendered with the same film.json and treatment, because I had deleted the original render by mistake.
- The user's materials (MedStat screens and the humidifier renders) and any sheets made from them were never committed.

## 中文

### 结论（2026-10-21）：验收通过
**验收标准**（第 9 轮后与用户商定）：Haiku 只凭一句话做出的片子，要达到 Claude Opus 制作的参考片的水平：在同一组评审中盲评，且所有诚实性关卡都要通过。

**结果：达到。** 在验收这组评审（三位全新的盲评评审，编号 16–18）中，用最终版技能做出的两部复测片，得分都高于 Opus 参考片：

| 片子 | 谁做的 | 素材 | 评审 16–18 平均 |
| --- | --- | --- | --- |
| 参考片（Aurel） | Opus | 手绘占位图 | 2.96 |
| 加湿器 10a | Haiku，最终版技能 | 用户的 AI 渲染图，无文档 | 3.21 |
| 加湿器 10c | Haiku，最终版技能 | 同上 | **3.71** |
| 加湿器 9a | Haiku，第 8 轮技能 | 同上 | 3.67 |
| Larchwood 第 8 轮 | Haiku | 手绘占位图 | **3.71**（评审 16 给 4.00，无单项 < 3） |

- 三位评审都给 10c 比参考片高的分；10a 有两位高于参考片，评审 18 给 3.13，参考片 3.25。
- 两次运行都通过了所有关卡，QA 0 错误，都用了本地已有的音色，都没有编造数字或规格，也都没用那段乱码 AI 视频。
- **素材差异的说明**：加湿器片用的是照片级渲染图，参考片用的是手绘占位图，所以领先有一部分来自图片（画面分 4.0 对 2.0）。另有两组对比能单独看出技能本身的作用：
  - **同一素材文件夹**（Aurel，手绘杯子）：Haiku 的片子在每一组评审里都与参考片持平，差距在评审波动范围内（3.25 对 3.00；3.33 对 3.46；3.29 / 3.17 对 3.29）。
  - **其他手绘占位素材**：从第 6 轮起，Haiku 做的 Larchwood 在每一组评审里都高于参考片。

**没有达到的**：最初的拔高目标“独立评审平均 ≥ 4”。没有任何一部片子平均达到 4；最高是 3.71（10c 和 Larchwood），有一位评审给 Larchwood 打了 4.00。技能作者自己在第 3 轮打出过 4.1，但作者不是独立评审。

### 方法
- **素材文件夹**：
  - Aurel：实物产品，手绘杯子，有参考片可比；
  - Quartile：桌面软件，线框图；
  - Larchwood：湖畔小木屋，手绘照片；
  - MedStat Pilot：8 张真实截图，演示数据，只保存在本地；
  - 加湿器：用户自己的 4 张 AI 渲染图和一段 10 秒视频，没有文档，只保存在本地。
- **运行**：Haiku 子智能体只拿到上面那一句提示，没有任何其他帮助。偏差都记录在案：卡住、被提醒、手改文件、下载。
- **评审**：每组三位全新的 Claude Sonnet 子智能体。每位只看到匿名、打乱顺序的片子，看不到方案和自评分。每部片子给他们看：
  - 从 1.0 秒起的 20 帧联系表（`evals/sheet.py`）；
  - 开场、高潮、结尾的密集关键帧条；
  - 旁白脚本；
  - 评分表（`references/crew.md` 第 9 节）。

  八项标准各打 1–5 分。评审看不到运动画面，也听不到声音。
- **只在同一组评审内比较**：每组都把参考片和新片放在一起重新打分；同一部片在不同组之间最多差 0.2。

### 各组评审分数（三位评审平均）
| 评审组 | 参考片 | Aurel | Quartile | Larchwood | MedStat（真实截图） | 加湿器 |
| --- | --- | --- | --- | --- | --- | --- |
| 1–3（第 1 轮 → 第 3–5 轮） | 3.25 | 2.84 → 3.13 | 2.67 → 3.42 | 3.13 → 3.83 | — | — |
| 4–6（第 5 / 6 轮） | 3.00 | 3.25 / 3.08 | 2.96 / 2.96 | 3.17 / 3.50 | — / 2.96 | — |
| 7–9（第 6 / 7 轮） | 3.46 | 3.17 / 3.33 | 2.67 / 3.25 | 3.38 / 3.50 | 2.96 / 3.33 | — |
| 10–12（第 7 / 8 轮） | 3.29 | 3.29 / 3.17 | 2.84 / 2.88 | 3.38 / 3.54 | 3.17 / 3.25 | — |
| 13–15（第 9 轮） | 2.92 | — | — | 3.50（第 8 轮） | — | 9a 3.58 · 9b 3.17 · 9c 3.42 |
| 16–18（第 10 轮，验收） | 2.96 | — | — | 3.71（第 8 轮） | — | 9a 3.67 · **10a 3.21 · 10c 3.71** |

1–3 组的“→”指第 1 轮到第 3–5 轮中最好的一轮，取看过该片的各位评审的平均。

### 现在的运行表现（第 1 轮 → 第 3–10 轮）
- **配音**：第 1 轮三部里有两部只有字幕；之后每次都用本地已下载的 Kokoro 音色，没有下载。
- **方案与创意**：方案第 4 节是真正的脚本，创意也落到了片子里：第 1 轮三部中两部做到；之后每次都做到（强制）。
- **结尾句**：之后每次都呼应开场。
- **虚高自评**：被关卡拦下；有两次在被拦后改了一项自评，见下文。
- **编造数字或规格**：0 次。没有用户提供的来源，任何数字和规格都过不了关卡。
- **SRT**：之后每次都交付。
- **卡住**：
  - 第 2 轮三次，都已在技能里修复；
  - 第 10 轮一次，原因是关卡的 bug，已修复。

### 技能的改动（第 1–10 轮）
1. **团队流程不能跳过。**
   - `check_treatment.py` 不通过，`make_film.py` 就不构建。
   - 关卡同时检查质量与格式：
     - 证据句要带事实；
     - film.json 要与脚本一致；
     - 三个概念要不同；
     - 开场、高潮、结尾三句要进入片子。
   - 自评分会被可测量的问题封顶：长时间停顿、纹理或 Logo 冷开场、过大的高亮框、同形状的证据拍点、离题镜头、不呼应开场的高潮、规格清单。
2. **诚实性关卡。**
   - **数字与规格**：每个数字和规格词都要有用户提供的来源（文件夹里的文字，或品牌把关人点名的截图）。没有文档时，文案只能说图片里看得见的东西，依据是美术指导在第 5 节为每张图写的那一行。
   - **适用范围**：文档里有限制的说法（专业版、测试版、单一平台），必须在同一场景里说明限制。
   - **地点**：户外画面配室内用词会被拦下，反之亦然。
   - **计数动画**：不会滚过错误的数字。
3. **可模仿的文案**：五部范例片，每种叙事结构一部，每个场景都写了 `_why`；以及 `references/copy-bank.md`（锚点句、由弱到强的改写）。
4. **输入**：
   - autofilm 从产品自己的文档写 brief。
   - JPEG 一律按照片处理；产品白底图会被识别出来，留给高潮。
   - 文件夹名作为类型线索（第 10 轮后加入）。
   - 类型关键词补全了住宿和家居。
5. **界面**：
   - `suggest_rects.py` 预填高亮框：对话框和面板，最大不超过屏幕的四分之一；图表上不画框。
   - 推近时保证文字 ≥ 18 px。
   - 密集界面完整显示不超过 1 秒。
6. **结构与运动**：
   - **先出钩子**：照片封面先停在主体上（`focus`，用 `subject_grid.py` 选），约 3.4 秒内拉开到全景；界面封面推近到可读区域。
   - **高潮**：高潮有编排并呼应开场。界面片在重拍上让产出清晰浮现；照片片用会变化的首尾呼应，名称放在画面下三分之一处。
   - **节奏**：证据拍点换形状，两个证据拍点后留一口气，片长跟着素材走（每张图约 9 秒）。
7. **流程**：
   - 最新构建的 QA 通过才能渲染。
   - 生成文件带指纹。
   - 配音离线运行。
   - 始终交付 SRT。
8. **测量**：`evals/sheet.py` 取代了从黑场开始取帧的联系表，并新增关键帧条。修正前后同一批片子的“开场”分是 3.00 对 2.93，说明黑场并不是开场分低的原因。

### 各轮概要
- **第 1–5 轮**（占位素材，评审 1–3）：团队流程从摆设变成强制执行。配音、SRT、落到片子里的创意和诚实的自评，每次运行都做到了。Larchwood 从 3.13 升到 3.83，Aurel 和 Quartile 也有提升。
- **第 6 轮**（评审 4–6）：新增三种界面高潮处理和真实截图文件夹。分数持平；完整应用截图在成片尺寸下太密，看不清。
- **第 7 轮**（评审 7–9）：先出钩子、界面可读、证据换形状。所有文件夹都有提升（平均 3.05 → 3.35），Larchwood 和 Quartile 在部分评审那里超过参考片。
- **第 8 轮**（评审 10–12）：修正了测量，高潮落在击点上。分数持平，“高潮”仍是 3 分。之后新增两个关卡：计数动画，以及漏写适用范围的说法。
- **第 9 轮**（评审 13–15）：用户自己的 AI 渲染图，没有文档。没有编造规格，乱码视频被排除，画面分升到 3.3–3.7，9a 得 3.58。随后的修复：无文档时的数字与规格关卡、产品白底图、选图，然后是两拍冷开场和地点检查。
- **第 10 轮**（评审 16–18，验收）：同一文件夹、最终版技能复测。
  - 10c 得 3.71（开场 3.67，画面 4.0），10a 得 3.21。评审认为 10a 的文案像口号，并且有一张图重复使用。
  - 10b 被关卡的 bug 拦住：没有文档时，关卡把所有说法都判为不具体，于是拦下每一句。已修复（第 5 节每图一行和第 2 节证据现在都算依据），10c 在修复后的技能上运行。
  - 两次运行都手动改掉了 autofilm 猜的类型（食品饮料）。本轮之后已修复，autofilm 现在会读文件夹名，`humidifier` 会判为家居生活类；尚未复测。

### 仍未解决的问题
1. **高潮**：还没有评审说哪个高潮“第二天还记得”，评价是“称职，但不难忘”。可能需要真实的运动素材，比如产品工作时的视频。
2. **结尾页没有画面**：评审说结尾那句话立得住，但画面留不下来。
3. **同一文件夹、同一版技能，两次运行的差距和多数技能改动一样大**（3.21 对 3.71）。概念偏弱时（比如“柔和时刻”这种氛围，而不是一句话），仍能通过关卡。
4. **素材少时片子偏短**：4 张图做出 46–52 秒。这是诚实的长度，但评审会注意到。
5. **占位素材把画面分卡在 3 分左右**：还没有用真实照片测过；加湿器素材是 AI 渲染图。

### 各轮的诚实性发现
- **关卡拦下的**：
  - 漏写“专业版”的限制（第 8 轮 MedStat）；
  - 从截图读出、没有来源的“95%”（第 7 轮 MedStat）；
  - 帐篷画面配“房间”（第 9 轮 9b）；
  - 一句编造“8 小时、300 毫升水箱”的测试文案，触发 8 个错误。
- **没有被任何关卡拦下的**：
  - 9b 把淡紫色的光说成“暖光”；
  - 10a 连着两场都念品牌名（高潮之后紧接 finale）。
- **被拦后改了自评**：有两次运行在被关卡拦下后改了一项自评。第 6 轮依据“按选择与呈现评画面”提高了画面分；10c 把文案扣分记为素材缺口。两次都在规则允许范围内，但值得留意。
- **加湿器素材是 AI 渲染图，不是真实产品的照片。** 每次运行都说明了片子是概念片，并列出用户需要提供的东西：名称、Logo、规格表，以及渲染图的使用授权。

### 关于本次测试的说明
- 技能作者既修改了技能，也给第 1–3 轮打了分；独立评审正是为了检验这种偏差，而且他们更严格。
- 第 2 轮 Aurel 和 Quartile 在等待后台监视时，各被中性地提醒过一次（“渲染已完成，请继续”）；这种情况随后已在技能里修复。
- 第 2 轮开始时，第 1 轮的证据在技能文件夹里放了约一分钟才移走；没有任何一次运行的文案与它相同。
- 第 7 轮的参考片是用同样的 film.json 和方案重新渲染的，因为我误删了原渲染文件。
- 用户的素材（MedStat 截图和加湿器渲染图），以及用它们做出的联系表，从未提交。
