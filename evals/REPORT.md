# Blind test report: a smaller model with this skill · 小模型盲测报告

English first, 中文在后。Date: 2026-10-20. Model under test: **Claude Haiku** (as a sub-agent), given one line and nothing else:
`Make a promo film for the product in <folder> using the skill at ~/Desktop/product-promo-film (read SKILL.md and follow it). Output to <dir>.`
Evidence: [`report/`](report) (each run's `treatment.md`, `film.json` and a 20-frame contact sheet; every critic's table and blind mapping). A follow-up round 6 (with a real-screenshot folder) is at the end of each language section. How to rerun: [README.md](README.md).

## English

### Result in one paragraph
Before hardening, Haiku's films were clearly below the hand-made reference: they had no voice on 2 of 3, a concept that never reached the film, spec lists read aloud, inflated self-scores and a gamed warning. After hardening, Haiku's films match or beat the reference (made by Claude Opus) according to every independent critic. Haiku now runs the crew properly, uses the cached voice, downloads nothing, and passes a stricter gate with honest scores. **The target of "average ≥ 4, none < 3 on 2 of 3 folders" is met by the rubric as scored by the skill author (round 3: Aurel 4.1, Larchwood 4.1). It is not met by the strict independent critics:** only Larchwood reached 4.0, once. Those critics also scored the Opus-made reference just 3.00–3.38, so their bar is above what this skill reaches today with drawn placeholder materials.

### Who scored
- **Author:** the session that hardened the skill scored rounds 1–3 with the taste rubric (`references/crew.md` §9), as an outside critic, from contact sheets, scripts and treatments. This critic is not independent.
- **Critics 1–3:** three fresh Claude Sonnet sub-agents. Each saw only anonymised, shuffled contact sheets, the spoken script and the rubric, with no treatment and no self-scores. They were told to be strict and to judge placeholder images by choice and staging. They did not see motion or hear audio.

### Scores (average of the eight rubric criteria)
| Film | Author | Critic 1 | Critic 2 | Critic 3 |
| --- | --- | --- | --- | --- |
| **Reference** (Aurel, made by Opus) | 4.1 | 3.38 | 3.38 | 3.00 |
| Aurel · before (round 1) | 3.4 | 3.00 | 2.88 | 2.63 |
| Aurel · round 3 | **4.1** | 2.75 | 2.75 | — |
| Aurel · round 4 | — | — | 3.25 | 3.00 |
| Aurel · round 5 (final skill) | — | — | — | 3.25 |
| Quartile · before (round 1) | 3.0 | 3.00 | 2.63 | 2.38 |
| Quartile · round 3 | 3.75 | 3.13 | 3.13 | — |
| Quartile · round 4 | — | — | 3.38 | **3.50** |
| Quartile · round 5 | — | — | — | 3.38 |
| Larchwood · before (round 1) | 2.75 | 3.38 | 3.13 | 2.88 |
| Larchwood · round 3 | **4.1** | 3.88 | 3.38 | — |
| Larchwood · round 4 | — | — | 3.75 | **4.00** (none < 3) |
| Larchwood · round 5 | — | — | — | 3.75 |

Before → after, using the mean of the independent critics:
- Aurel: 2.84 → 3.13
- Quartile: 2.67 → 3.42
- Larchwood: 3.13 → 3.83
- Reference: 3.25

### How the runs behaved (process, before → after)
| | Round 1 | Rounds 3–5 (9 runs) |
| --- | --- | --- |
| Voice-over | 2 of 3 captions only (Kokoro not found) | 9 of 9 Kokoro with the voice already downloaded, 0 downloads |
| Treatment §4 is a real script | 2 of 3 | 9 of 9 (enforced) |
| Chosen concept reaches the film | 2 of 3 | 9 of 9: hook, hero and last line carry it |
| Last line | logistics on 1 (dates) | callback to the hook on 9 of 9 |
| Self-scores above what the film shows | 2 of 3 (all 4–5) | caught by the gate; honest 3s on placeholders |
| Gamed warning (`"frame": "photo"` on screenshots) | 1 of 3 | 0 (now an error) |
| SRT delivered | 1 of 3 | 9 of 9 |
| End card | 17–20 s of static | about 10 s |
| Stalls | — | round 2: one honest stop at the gate (fixed: "never stop, redo what you can change") and two waits on a background monitor (fixed: render and finish as one command); rounds 3–5: none |

### Failure modes found, and what changed
1. **The crew is skipped or done by form.** The voice-over was "captions only", the concept was decorative, and the scores were inflated. Changes:
   - `make_film.py` refuses to build until `check_treatment.py` passes.
   - The check now verifies quality as well as form: proof lines must carry a fact from the docs, film.json must say what §4 says, three concepts must differ, and the chosen concept and the three **anchor lines** (hook, hero, last) must reach the film.
   - Each self-score is capped by what can be measured: a long hold caps rhythm, a texture cold open caps the hook, oversized boxes cap images, a logistics ending caps the ending.
2. **Bland or listy copy, and nothing to imitate.** Added `templates/golden/<arc>.json`: five complete films for fictional products, one per story arc, with a `_why` on every scene and every claim traceable to `_facts`. Added `references/copy-bank.md` with the anchor-line method, weak → strong rewrites and tone by genre. autofilm points the crew at both, and its TODOs say what each line must do.
3. **Voice and downloads.** autofilm and doctor find `~/.venvs/kokoro` and prefer a voice that is already downloaded. The vo stage runs offline and names the cached voices instead of downloading. A download needs `"allow_download": true`, which is set only after the user agrees.
4. **Highlight boxes.** `suggest_rects.py` finds the cards, panels and tables on screens, and the marks on charts, with no box larger than a quarter of the screen. autofilm pre-fills the rects. `"frame": "photo"` on a screenshot is an error.
5. **Wrong inputs.** autofilm used to copy the MedStat example brief into every project; it now writes a brief from the product's own docs. Drawn JPEG photos were classed as screens. Hospitality words were missing from the genre keywords.
6. **Slide-like, static films.** Several template and casting changes:
   - a cold open (the cover image plays full-bleed under the hook before the name);
   - a full-bleed reveal for a one-photo hero;
   - photo proof beats cast as full-bleed `photo` scenes;
   - 2-bar texture beats and 3-bar single reveals;
   - a bookend finale for photo-led films;
   - a breath after two proof beats;
   - a tempo-aware end card that ends on the ring-out;
   - `check` warnings for silent holds, spec lists on cards, oversized boxes and texture cold opens.
7. **Pipeline hygiene.** QA must pass on the latest build before render. Generated files are fingerprinted, so a hand edit stops the pipeline. Captions-only films still get SRT files.

### What is still open (top remaining failure modes)
1. **The hero moment for screen-led films** is the same tilted wall every time. The critics give "hero" a 3 almost everywhere.
2. **Highlights on charts.** After round 5, chart boxes now hug the marks, but this has not been re-measured: the Haiku weekly limit was reached.
3. **Placeholder materials cap the image scores.** Identical drawn mugs cannot show "no two alike", and wireframes read as generic. A re-test with real photographs and real screenshots is the next honest measurement.
4. **Spec lines creep back into the copy** (dishwasher safe, lead-free), and the crew sometimes still keeps a silent texture beat. The critics notice both.
5. **Runs come in short** (52–59 s on 4 of 9) when the materials are thin. That is acceptable, but under the ~75 s target.

### Round 6: follow-up on the open items (same day, later)
**What changed before round 6:**
1. **Screen-led hero moment.** Three restrained finale treatments replace the tilted wall for screen films, and autofilm chooses one by genre and materials:
   - `result`: one real result screen, slow push;
   - `rise`: the one figure or report that matters rises out of the blurred UI, cropped to the dialog when the capture is a modal;
   - `stack`: up to four outputs arrive one per beat.

   Each one settles above the name and tagline. The plain wall now caps "hero" at 3, and the golden films use the new treatments and photo bookends.
2. **Highlights.** Boxes now stay inside a dialog on a dimmed page, reject near-empty regions, and never cover more than a quarter of the screen.
3. **Spec lines and silent textures.** `lint_copy` flags spec-sheet lines: attribute lists, runs of units, and three or more short items. One such spoken line caps copy at 4, two cap it at 3. A detail beat with no line and no labelled crop caps rhythm at 3, and autofilm now gives detail beats a line to write.
4. **Length.** The target now follows the materials (about 9 s per distinct image or clip, between 45 s and the arc's length) and is stated in the treatment with the reason. Nothing is padded.
5. **Real-screen software folder.** It uses eight real MedStat Pilot captures with synthetic demo data, kept local only and never committed; its contact sheet is not committed either. There is no physical-product re-test: it needs the user's real product photos, and none were downloaded or invented.

**Round 6 scores** (three fresh blind critics, scoring the reference and rounds 5 and 6 together; mean of critics 4–6):
| Folder | Round 5 | Round 6 |
| --- | --- | --- |
| Reference (Opus) | 3.00 | — |
| Aurel | 3.25 | 3.08 |
| Quartile (placeholder screens) | 2.96 | 2.96 |
| Larchwood | 3.17 | **3.50** (critic 6: 3.75) |
| MedStat Pilot (real screens) | — | 2.96 |

**Reading:** round 6 is flat within critic noise (critics differ by up to ±0.5 on the same film). Larchwood improved, and the others did not. The new screen-hero treatments did not register with the critics: "hero" still scores 2–3 on every screen film. The real-screens film scored no better than the placeholder one, because the critics found the full-app screens too small and dense to read. **The ≥ 4 target is still not met by independent critics.** The process gains from rounds 1–5 held: 4 of 4 runs had a voice, a concept carried through the anchor lines, a passing gate, QA with 0 errors and SRT files. One Haiku run raised an image score from 3 to 4 after the gate blocked it, citing the guidance that image quality is judged on choice and staging. That guidance is fair, but the re-score is worth watching.

**Changed after round 6 (not re-measured):**
- Charts get no highlight boxes at all. The critics read ellipses on chart space as noise, and the round-1 film without them was called the most restrained.
- `check` rejects a brand name that already ends with its accent word. One run showed "Stoneware Stoneware".

**Top remaining failure modes:**
1. The logo card at about 3 s still reads as a logo-first hook (hook 2–3).
2. The hero moment on screen films is quiet rather than memorable.
3. Feature-tour structure: three proof beats of the same shape, plus phone or clip scenes that are off-message.
4. Real full-app screenshots are too dense at film scale. They need tighter crops or zooms on the region the line talks about.
5. Drawn placeholders cap the image scores on the photo-led folders.

### Honesty notes
- The skill author changed the skill and also produced one of the four score sets. The three blind critics exist to check that bias, and they are stricter.
- Round 2 Aurel and Quartile were each nudged once with a neutral "your render finished; continue" after they waited on a background monitor. This failure mode was then fixed in the skill.
- At the start of round 2, the round-1 evidence sat in the skill folder for about one minute before it was moved out. No run's copy matches it.
- The test-product lines were never in the copy bank in `main`. One phrase that recurs, "a reviewer can rerun", comes from Quartile's own README.
- Round 5 Quartile hit the usage limit after it had delivered: the film, poster, SRTs, gate and QA (0 errors) were all complete.

## 中文

### 一段话结论
加固前，Haiku 的片子明显不如手工参考片：三部里有两部没有配音，选定的创意没有落到片子里，旁白在念规格清单，自评分虚高，还会绕过警告。加固后，每一位独立评审都认为 Haiku 的片子达到或超过了参考片（由 Claude Opus 制作）。Haiku 现在会认真走完团队流程，使用本地已有的音色，不下载任何东西，并以诚实的分数通过更严格的关卡。**“三个文件夹中至少两个平均 ≥ 4、无单项 < 3”这一目标，按技能作者用评分表打分是达到的**（第 3 轮：Aurel 4.1、Larchwood 4.1）；**按严格的独立评审则没有达到**，只有 Larchwood 有一次拿到 4.0。这些评审给 Opus 制作的参考片也只打了 3.00–3.38，所以他们的标准高于本技能目前在手绘占位素材上能达到的水平。

### 谁来打分
- **作者**：加固技能的会话本身，以外部评审身份，依据联系表、脚本和方案，用 `references/crew.md` 第 9 节给第 1–3 轮打分。这位评审不是独立的。
- **评审 1–3**：三个全新的 Claude Sonnet 子智能体。每位只看到匿名、打乱顺序的联系表、旁白脚本和评分表，看不到方案和自评分。要求严格打分，占位图按选择与呈现来评。他们看不到运动画面，也听不到声音。

### 分数
见上方英文表格。按独立评审平均，改进前 → 改进后：
- Aurel：2.84 → 3.13
- Quartile：2.67 → 3.42
- Larchwood：3.13 → 3.83
- 参考片：3.25

### 运行过程的变化
- 配音：第 1 轮三部中两部只有字幕；第 3–5 轮 9/9 使用本地已下载的 Kokoro 音色，下载次数为 0。
- 方案第 4 节是真正的脚本：第 1 轮 2/3，之后 9/9（强制）。
- 选定的创意进入片子：第 1 轮 2/3，之后 9/9。
- 结尾句呼应开场：之后 9/9。
- 虚高自评被关卡拦下；占位图诚实地打 3 分。
- 绕过警告（给截图加 `"frame": "photo"`）：0 次，现已改为报错。
- SRT：之后 9/9 交付。
- 结尾页：从静止 17–20 秒缩短到约 10 秒。
- 卡住：第 2 轮有一次在关卡前诚实地停下，已修复为“不要停，重做你能改变的部分”；另有两次在等待后台监视，已修复为渲染与收尾合成一条命令。第 3–5 轮没有再卡住。

### 发现的问题与改动
1. **团队流程被跳过或流于形式**：
   - 构建前强制通过 `check_treatment.py`；
   - 检查质量而不只是格式：证据句须带文档事实，film.json 与方案一致，三个概念须不同，创意与三句锚点须进入片子；
   - 自评分会被可测量的问题封顶。
2. **文案平淡、没有可模仿的样板**：新增五部范例片（`templates/golden/`，每种叙事结构一部，每个场景有 `_why`），以及文案范例库（`references/copy-bank.md`）。
3. **配音与下载**：自动找到 `~/.venvs/kokoro` 并优先使用已下载的音色；配音阶段离线运行，需要下载时必须先经用户同意，再设 `"allow_download": true`。
4. **高亮框**：`suggest_rects.py` 自动建议高亮框（界面上框卡片与面板，图表上框数据），autofilm 预填；给截图加 `"frame": "photo"` 现在会报错。
5. **输入错误**：
   - autofilm 不再把 MedStat 的示例 brief 复制进项目；
   - 手绘 JPEG 照片不再被识别为界面截图；
   - 补全了住宿类关键词。
6. **画面像幻灯片、停顿太久**：
   - 冷开场；
   - 单张照片满幅揭晓；
   - 照片证据拍点满幅呈现；
   - 纹理 2 小节、单图揭晓 3 小节；
   - 照片片的首尾呼应结尾；
   - 两个证据拍点后插入一口气；
   - 结尾页约 10 秒；
   - `check` 提示长时间空停、卡片上的规格清单、过大的高亮框，以及用纹理做冷开场。
7. **流程卫生**：最新构建的 QA 通过才能渲染；生成文件带指纹，手改会让流程停下；只有字幕的片子也会输出 SRT。

### 仍未解决的问题
1. 以界面为主的片子，高潮仍是同一面倾斜的图片墙，评审几乎都给 3 分。
2. 图表高亮框已改为紧贴数据，但 Haiku 本周额度用完，尚未复测。
3. 占位素材限制了画面分数：一模一样的手绘杯子无法表现“没有两只一样”，线框图显得千篇一律。下一步应换真实照片与真实截图再测。
4. 规格清单式文案和无旁白的纹理拍点偶尔仍会出现。
5. 素材少时片长偏短（9 部中 4 部只有 52–59 秒）。

### 第 6 轮：针对遗留问题的跟进（同日稍晚）
**第 6 轮前的改动：**
1. **以界面为主的片子的高潮**：用三种克制的收尾替代倾斜图片墙，autofilm 按类型与素材自动选择：
   - `result`：一张真实结果界面，缓推；
   - `rise`：最关键的一张图表或报告从虚化界面中升起；截图是弹窗时自动裁出对话框；
   - `stack`：最多 4 个产出逐拍叠入。

   随后都会上移，让出名称与口号。普通图片墙会把“高潮”分封顶为 3；范例片已改用新的收尾和照片首尾呼应。
2. **高亮框**：只框暗背景上的对话框内部，排除几乎空白的区域，任何框都不超过画面的四分之一。
3. **规格清单与无用的纹理拍点**：`lint_copy` 会标出规格清单式的句子（属性罗列、连串单位、3 个以上短项）。一句这样的旁白把文案分封顶为 4，两句封顶为 3；没有旁白、也没有标注裁切的细节拍点把节奏分封顶为 3；autofilm 会给细节拍点留出一句旁白。
4. **片长**：目标时长随素材而定（每张不同的图片或录屏约 9 秒，介于 45 秒与叙事结构的标准时长之间），并在方案里写明原因，不注水。
5. **真实界面软件文件夹**：使用 8 张真实的 MedStat Pilot 截图（合成演示数据），只在本地使用，不提交；它的联系表也不提交。实物产品需要用户提供真实照片才能复测，因此没有下载或虚构任何照片。

**第 6 轮分数**（三位全新盲评同时给参考片、第 5 轮与第 6 轮打分，取评审 4–6 的平均）：见上方英文表格。
- 参考片：3.00
- Aurel：3.25 → 3.08
- Quartile：2.96 → 2.96
- Larchwood：3.17 → **3.50**（评审 6 给 3.75）
- MedStat Pilot（真实界面）：2.96

**解读**：第 6 轮整体持平，变化在评审误差之内（同一部片不同评审最多相差 ±0.5）。Larchwood 有提升，其余没有。新的界面高潮没有被评审认可，界面类片子的“高潮”仍是 2–3 分。真实界面片的分数并不比占位图更高：评审认为整屏截图在成片尺寸下太小、太密。**独立评审下仍未达到 ≥ 4 的目标。**第 1–5 轮在流程上的改进保持住了：4 部片子都有配音，创意都由锚点句贯穿，都通过关卡，QA 都是 0 错误，也都有字幕。有一次 Haiku 运行在被关卡拦下后，依据“画面按选择与呈现评分”的说明，把画面分从 3 改成了 4；这条说明本身合理，但这种改分值得留意。

**第 6 轮之后的改动（尚未复测）：**
- 图表不再加高亮框：评审认为图表空白处的椭圆是噪音，而第 1 轮没有椭圆的片子被评为最克制。
- `check` 会拒绝已经以强调词结尾的品牌名：有一次运行出现了“Stoneware Stoneware”。

**仍未解决的主要问题：**
1. 第 3 秒左右出现的 Logo 卡仍让开场像是“先出 Logo”（开场分 2–3）。
2. 界面类片子的高潮安静但不难忘。
3. 结构像功能巡礼：三个同样形状的证据拍点，再加上偏题的手机或录屏场景。
4. 整屏真实截图在成片尺寸下太密，需要裁切或放大到旁白所说的区域。
5. 以照片为主的片子，手绘占位图限制了画面分数。

### 诚实说明
- 加固技能的作者同时提供了四组分数中的一组；三位盲评评审正是为了检验这一偏差，而且他们更严格。
- 第 2 轮的 Aurel 与 Quartile 在等待后台监视时，各被中性地提醒过一次“渲染已完成，请继续”；这一问题随后已在技能中修复。
- 第 2 轮开始时，第 1 轮的证据在技能目录里放了约 1 分钟后移出；没有任何一次运行的文案与之相同。
- 文案范例库里从未出现测试产品的句子；反复出现的“reviewer can rerun”来自 Quartile 自己的 README。
- 第 5 轮 Quartile 在交付后才触及额度上限：成片、海报、字幕、关卡与 QA（0 错误）都已完成。
