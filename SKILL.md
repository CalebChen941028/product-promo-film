---
name: product-promo-film
description: Make a commercial-grade promo film (45 s – 4 min as the materials allow, 1080p, landscape) for ANY product — software, apps, hardware, fashion, food, services, brands — from the user's materials folder (screenshots, photos, product cut-outs, clips, logo, docs), with or without the user's music. Classifies the product into 15 genres to pick the look (8 styles), motion (6 theme-driven languages), story arc and an original composed underscore when no track is given. A built-in crew (strategist, creative director, copywriter, art director, editor, composer, brand guardian, design critic) writes a checked treatment. A restrained director's cinema layer adds colour script, LUT grade, motion blur and subtle sound design. Kokoro voice-over, bilingual captions, poster and SRT. One command from folder to draft (autofilm.py), one command to film (make_film.py), automatic QA. Use for promo / launch / ad / brand / explainer videos, 宣传片, 产品视频, 广告片.
---

# Product Promo Film · 产品宣传片

> **English first, 中文在后。** The hard rules below never bend. Everything else is a default: the steps are the safe path that makes a good film with any model, and every choice in them (story, scenes, layout, motion, camera, cuts, look, colour, music) can be replaced with your own when the film needs it — see "Two routes". Scripts print `FIX:` lines when something is wrong: do what they say, then rerun. Edit `film.json`, never the generated `film_out/`.
>
> 下面的硬性规则永不变通；其余都是默认值：步骤是任何模型都能做出好片子的稳妥路线，其中每个选择（叙事、场景、版式、动效、运镜、转场、视觉、配色、音乐）在片子需要时都可以换成你自己的，见“两条路线”。脚本出错时打印 `FIX:`，照做后重跑。只改 `film.json`，不要手改生成的 `film_out/`。

## English

### What you deliver
| File | Spec |
| --- | --- |
| `final/<name>-1080p.mp4` | H.264 1920×1080 30 fps, AAC 48 kHz, −14 LUFS; graded, motion-blurred, with sound design |
| `final/<name>-cover-4k.png`, `-cover-1280.jpg` | poster = the cover frame |
| `final/<name>.bilingual/zh/en.srt` | captions aligned to the voice-over |
| `treatment.md` | the crew's creative treatment (concept, script, rhythm, sound, sign-off) |
| `film.json` | the editable source of the whole film |

### Hard rules
1. **Real material only.** Use real screenshots, captures (`scripts/capture_kit.mjs`) and real product photos. Never draw a fake UI or a fake product to pass as real. Placeholders are allowed only in demos, and must be labelled.
2. **Be honest.** Every claim (numbers, specs, health, finance, privacy) must be checkable in the user's docs. Quotes are real and approved. Demo or mock content is labelled.
3. **Licences:**
   - Music: the user's track, or the original underscore composed by `make_music.py`. Never take a track from the web.
   - Voice: Kokoro (Apache-2.0) or the user's recordings; never OS voices.
   - Ask before downloading any model or voice. Say the name, source and size.
4. **Secrets.** Never type a user's API key into an app or config.
5. **Gates (enforced).** `make_film.py` refuses to build until `check_treatment.py` passes, and refuses to render until QA has 0 errors on the latest build. Generated files are fingerprinted: a hand edit in `film_out/` stops the pipeline.
6. **Restraint.** Calm, professional, premium: effects are felt, not seen, and the film has one hero moment (`references/director.md`).

### Two routes (and you are free to design)
The motion, the camera, the cuts and the motion graphics are yours to design. The director's shot plan, the 6 motion languages, the 12 cuts and the built-in camera moves are a proposal and a vocabulary, not a cage: change any scene's `layout` / `camera` / `cut` / `motion`, write your own moves and cuts as keyframes in film.json, design MG scenes (`"type": "mg"`), or write code. No permission and no `Deliberate` note is needed for a creative choice; say your intent in treatment §6. Only the hard rules and the QA bind.
- **Autopilot (any model):** follow the steps. autofilm drafts the film, the director proposes every shot, the colour director the palette, the crew writes the words, the checks keep it clean. This is the floor, and it is a good film.
- **Director's cut (when you can see further):** keep the hard rules and the tools, and replace any default with something better — your own motion language, camera moves and cuts as keyframes in film.json (`"cameras"`, `"cuts"`), motion graphics as `mg` scenes (layers of text, shapes, lines, numbers and real images on beat keyframes), or your own scenes, moves and look in code (`references/custom-scenes.md`); any scene order, any length. When a taste check stands in the way of a better film, break it on purpose and say why in the treatment (`- Deliberate · 刻意: Rhythm — …`): the check then advises instead of blocking. The QA, the captions, the grade, the sound and the honesty gates still run on everything you write.

### Steps (do them in order)
1. **Environment.** Run `python3 scripts/doctor.py` and fix every `MISS`. First time only: in this folder run `npm i playwright && npx playwright install chromium`.
2. **Materials → draft.** The user gives a folder or uploads files: screenshots, photos, product cut-outs (transparent PNG), clips, logo, music (optional), README or brief (optional).
   - **No folder, only the product** (an installed app, a URL), or under ~10 screens of software? Capture the real UI first with `scripts/capture_app.mjs` (explore → shot list → shoot; `references/capture.md`). If `examples/` has a shot list for this product (`examples/medstat-pilot/shots.json` for MedStat Pilot), start from it. Shoot 12–25 screens: autofilm refuses fewer than 8 from an app. Its output folder is the materials folder. Never `pkill`/`killall` anything and never run the product's source code: the user's own copy of the app may be open.
   - Then run `python3 scripts/autofilm.py <folder> --out <project> --mood "<the user's own words for the feel>"` (e.g. `"大气 商业 科技感"`, `"warm, human, quiet"`; leave it out only if the user said nothing about the feel). It:
     - classifies every file;
     - reads the docs and picks the **genre** (`scripts/genres.py --list`: 15 types, from SaaS to fashion, food and hardware);
     - picks the **look** (style + its motion): there is no default look. `scripts/look.py` reads every picture (screen or photo, light or dark UI, saturation, density, charts, the warmth of the dominant hue), weighs it with the product's character and the docs' tone, and scores all 8 styles with written reasons (the user's `--mood` words, if any, count triple). The treatment shows the reasons and the runners-up; the crew confirms or changes the look for THIS product (step 4), so two films of one category look alike only when their materials and mood do. Switch with `"style"` / `"motion"` in film.json;
     - picks the story arc and music (the user's track, or composed);
     - casts each material into a beat, best screens first (plots and results lead; home screens, prompts and settings come last); real footage plays from its best moment and can open the film;
     - **directs before anything is made**: reads every picture (screen or photo, dense or calm, the quiet side, where the subject sits) and writes each scene's layout, camera move and cut, with the reason, into `film.json` and the storyboard in `treatment.md` §6;
     - picks the **palette** like a colour director: the brand colour first, else colour psychology for the product type, in harmony with the materials' hues and legible on the style (`references/director.md` §8);
     - adds code-drawn story glue where the arc needs it (a journey map, many-into-one, kinetic type; `references/director.md` §7);
     - with 8 or more software screens (home screens and prompts do not count), plans a **chaptered tour** (2–4 min, like `examples/medstat-pilot`): one chapter per stage of the job, from the shot names `NN-chapter-what`;
     - writes `film.json` (with `TODO` copy), `treatment.md`, and `shot_wishlist.md` (the shots that would lift the film, with specs, for the user or a real crew; AI prompts only for atmosphere, never the product).
3. **Confirm with the user.** Ask only what matters:
   - the feel in their own words (big and cinematic? warm and human? clean and calm? rigorous and academic?): it steers the look;
   - the genre and look, if autofilm printed **CLOSE CALL**;
   - their own music, or the composed underscore;
   - voice-over language and voice (autofilm picks a voice that is already downloaded; any other voice is a download: ask first);
   - contacts for the end card.

   **Cannot ask** (a batch run, a sub-agent, the user is away)? Do not stop and do not download. Keep autofilm's genre, look, composed music and voice, take contacts from the docs (or leave them empty), and list every assumption in the report.
4. **Crew.** First study the golden film autofilm prints (`templates/golden/<arc>.json`, or `tour.json` for a chaptered tour; every scene has a `_why`) and `references/copy-bank.md`. Learn the moves; never copy their lines. Then read `references/crew.md` and play each role in order, filling `treatment.md`: producer → strategist (audience, USP → proof, AIDA) → creative director (3 concepts, choose 1, then the **three anchor lines**: hook, hero, last) → copywriter (a full script, one bullet per scene, a true call to action) → art director & colorist (palette, grade) → director & DP, motion designer & editor (the storyboard: shot sizes, moves, cuts) → composer → brand guardian → design critic. Then run `python3 scripts/check_treatment.py treatment.md` until it passes. A low taste score means redo the weakest part you can change, not re-score; never stop at the gate. What the materials cannot give (placeholders, few photos) goes in the report, not in a score.
5. **Write the film.**
   - Copy the treatment's words into `film.json` and replace every `TODO`.
   - Use the anchor lines exactly as written: hook → cover, hero → finale, last → endcard.
   - A photo cover needs a `focus` on its subject (`python3 scripts/subject_grid.py <photo> --preview .`, then `--cells B2,C3`): the open starts on that detail and reveals the place.
   - Screen points come with suggested `rect`s. Check them: `python3 scripts/suggest_rects.py <screenshot> --preview .` draws numbered boxes; give each point the box it talks about. Real photos (`"frame": "photo"`) need none. Never put `"frame": "photo"` on a screenshot to silence a warning.
   - Scene types and fields are in `references/film-spec.md`.
   - Then run `python3 scripts/check_treatment.py treatment.md film.json`. It checks that the film says what the treatment says, that proof lines carry facts from the docs, and it caps any taste score the film does not earn.
6. **Direct.** Do the director's pass (`references/director.md` §5). Defaults already set the colour script, hits, light and sound, and a **shot plan** gives every scene its own layout, camera move and cut (`--stage check` prints it; §6). For a calmer or richer film set `"direction": {"variety": "calm" | "rich"}`; the plan is a proposal: replace any scene's `layout` / `camera` / `cut` / `motion`, or design your own (keyframe `"cameras"` / `"cuts"`, `mg` scenes; `references/custom-scenes.md`) wherever the film is better for it.
7. **Check.** Run `python3 scripts/make_film.py film.json --stage check` until there is no ERROR. Fix copy warnings from the lint too.
8. **Build + voice + QA.** Run `--stage build`, then `--stage vo`, then `--stage qa`. QA must have 0 errors. If you can view images, read `film_out/qa/sheet*.png` and fix anything ugly in `film.json`.
9. **Render.** Optional quick look: `--stage render --draft`, then `--stage finish --draft`. Final, as ONE command so nothing waits on you in between: `python3 scripts/make_film.py film.json --stage render && python3 scripts/make_film.py film.json --stage finish`. It takes 5–20 minutes; if you run it in the background, wait for that command to exit, then check `final/`. Motion blur is applied only to frames that move.
10. **Report** to the user:
    - the file paths and the chosen concept;
    - every assumption you made without asking;
    - what is demo, placeholder or composed;
    - what you could not verify (you cannot hear the mix);
    - what they must still supply (the ✗ rows of `shot_wishlist.md`, a true call to action if the docs give none).

### Quality bar (why the defaults look good: keep them)
- One idea, one hero moment. The hook lands in the first 3 s, and the last 5 s are perfect.
- Cuts fall on bar lines, with one idea per bar.
- On-screen labels ≤ 12 汉字 / 42 chars; captions ≤ 30 汉字.
- No clichés (`scripts/lint_copy.py`).
- Speech sits ~10 dB over the music; sound design sits under it.
- One focal point and one accent colour per frame; margins ≥ 96 px. QA keeps the chapter label and captions clear.
- Max 4 points per feature, 6 comparison rows, 6 lineup items. Two calm scenes beat one crowded scene.
- Sharp material: capture screens at 2× (3840 wide); `--stage check` warns when a picture is enlarged over 1.5× (soft) or a dense screen is shown too small to read. Fix the material or the frame, never ignore it.

### Going further (optional)
- Manual route (no autofilm): `templates/film.example.json` + `scripts/recommend_style.py` + `scripts/plan_storyboard.py`.
- Composed music on its own: `python3 scripts/make_music.py --list`.
- Tune the cinema layer: `"cinema": {...}` (`references/film-spec.md`).
- The director's cut — your own scenes, motion languages, camera moves, cuts and look: `references/custom-scenes.md` (example: `templates/custom.example.js`).
- Golden films, one per story arc plus `tour.json` (copy and structure to learn from, not buildable): `templates/golden/`.
- Worked examples:
  - `examples/demo/`: software, the user's track;
  - `examples/product-demo/`: a physical product, composed music, full crew treatment;
  - `examples/medstat-pilot/`: a 3:26 production film.
- Install for other agents: `references/agents.md`.

## 中文

### 交付物
| 文件 | 规格 |
| --- | --- |
| `final/<名称>-1080p.mp4` | H.264 1920×1080 30fps，AAC 48kHz，−14 LUFS；已调色、运动模糊、含声音设计 |
| `final/<名称>-cover-4k.png`、`-cover-1280.jpg` | 封面海报（片头封面定帧） |
| `final/<名称>.bilingual/zh/en.srt` | 与配音对齐的字幕 |
| `treatment.md` | 团队的创意方案（概念、脚本、节奏、声音、签字） |
| `film.json` | 整部片子的可编辑源文件 |

### 硬性规则
1. **只用真实素材**：真实截图、录屏（`scripts/capture_kit.mjs`）、真实产品照片；不得画假界面或假产品冒充真实。只有演示才可用占位图，且必须标注。
2. **诚实**：数字、规格、健康、金融、隐私等说法都要能在用户资料里核实；引言必须真实且经授权；演示 / mock 内容要标注。
3. **授权**：
   - 音乐只用用户提供的，或 `make_music.py` 原创的配乐，不从网上找。
   - 配音用 Kokoro（Apache-2.0）或用户录音，不用系统语音。
   - 下载任何模型或音色前先说明名称、来源、大小并征得同意。
4. **密钥**：不替用户把 API Key 填进应用或配置。
5. **关卡（强制）**：`check_treatment.py` 不通过，`make_film.py` 拒绝构建；最近一次构建的 QA 不是 0 错误，拒绝渲染。生成文件带指纹，手改 `film_out/` 会让流程停下。
6. **克制**：平静、专业、高级；效果“感受得到，看不出来”，全片只有一个高潮（`references/director.md`）。

### 两条路线（动效可以自由设计）
动效、运镜、转场和 MG 动画由你来设计。导演的镜头表、6 种动效语言、12 种转场和内置运镜都是建议和词汇表，不是限制：任何场景的 `layout` / `camera` / `cut` / `motion` 都可以改；可以在 film.json 里用关键帧写你自己的运镜和转场，设计 MG 场景（`"type": "mg"`），或者写代码。创意选择不需要许可，也不需要写 `Deliberate`；在方案第 6 节写明意图即可。只有硬性规则和 QA 是约束。
- **自动驾驶（任何模型）**：按步骤走。autofilm 起草，导演为每个镜头给出建议，色彩导演定配色，团队写文案，检查保证干净。这是底线，也是一部好片子。
- **导演剪辑版（当你看得更远时）**：守住硬性规则、用好工具，把任何默认值换成更好的：在 film.json 里用关键帧写你自己的动效语言、运镜和转场（`"cameras"`、`"cuts"`），用 `mg` 场景做 MG 动画（文字、形状、线条、数字和真实图片按节拍关键帧运动），或用代码写你自己的场景、运镜和视觉（`references/custom-scenes.md`）；任意场景顺序、任意长度。某条审美检查挡住了更好的片子时，有意打破它，并在方案里写明理由（`- Deliberate · 刻意: Rhythm — …`），该检查就从阻止改为提醒。QA、字幕、调色、声音和诚实关卡对你写的一切照常生效。

### 步骤（按顺序）
1. **环境**：运行 `python3 scripts/doctor.py`，修好所有 `MISS`。首次需在本目录运行 `npm i playwright && npx playwright install chromium`。
2. **素材 → 草稿**：用户给一个文件夹或上传文件（截图、照片、透明底产品图、录屏、Logo、音乐可选、README 或 brief 可选）。
   - **没有素材文件夹、只有产品本身**（已安装的应用、网址），或软件截图少于约 10 张：先用 `scripts/capture_app.mjs` 采集真实界面（探索 → 镜头清单 → 拍摄，见 `references/capture.md`）。若 `examples/` 里已有这个产品的镜头清单（MedStat Pilot 用 `examples/medstat-pilot/shots.json`），就从它开始。拍 12–25 屏：从应用采集少于 8 屏时 autofilm 会拒绝。它的输出文件夹就是素材文件夹。不要 `pkill`/`killall` 任何进程，也不要运行产品源码：用户自己可能正开着这个应用。
   - 然后运行 `python3 scripts/autofilm.py <文件夹> --out <项目目录> --mood "<用户自己描述的风格感觉>"`（如 `"大气 商业 科技感"`、`"温暖 人文 安静"`；用户没说才省略），它会：
     - 给每个文件分类；
     - 读文档判断**产品类型**（`scripts/genres.py --list`：15 类，从 SaaS 到时尚、食品、硬件）；
     - 选定**视觉风格**（风格及其动效）：没有默认风格：`scripts/look.py` 读懂每张图（截图还是照片、浅色还是深色界面、饱和度、信息密度、是否图表、主色冷暖），结合产品特点与文档语气，给 8 种风格逐一打分并写明理由（用户给的 `--mood` 用词若有，权重三倍）。方案里会列出理由和备选；团队在第 4 步针对这款产品确认或修改，所以只有素材与气质真的相近时，同类产品的片子才会长得像。可在 film.json 的 `"style"` / `"motion"` 里改；
     - 选定叙事结构、音乐（用户的曲子或原创）；
     - 把素材分配到各个拍点，好画面优先（图表、结果在前；首页、弹窗提示、设置页在后）；真实视频从最好的片段开始播放，也可以做开场；
     - **先设计、后制作**：导演读懂每张画面（截图还是照片、密还是疏、哪一侧安静、主体在哪），把每个场景的版式、运镜、转场连同理由写进 `film.json`，并在 `treatment.md` 第 6 节生成分镜表；
     - 像色彩导演一样选**配色**：品牌色优先，否则按产品类型的色彩心理选色，并与素材色调和谐、在风格背景上清晰可读（`references/director.md` 第 8 节）；
     - 在叙事需要处加入代码动画（旅程图、多合一、动态文字，见 `references/director.md` 第 7 节）；
     - 软件截图有 8 张或更多（首页和提示框不算）时，排成**分章节的产品巡礼**（2–4 分钟，类似 `examples/medstat-pilot`）：按镜头名 `NN-章节-内容` 每个工作阶段一章；
     - 写出 `film.json`（文案为 `TODO`）、`treatment.md`，以及 `shot_wishlist.md`（最能提升片子的补拍镜头及拍摄参数，供用户或真人团队拍摄；AI 提示词只用于氛围镜头，绝不生成产品本身）。
3. **与用户确认**（只问关键的）：
   - 他们想要的气质（大气商业？温暖人文？简洁克制？严谨学术？），用他们自己的话：它决定视觉风格；
   - 输出 **CLOSE CALL** 时确认类型与风格；
   - 用他们自己的音乐还是原创配乐；
   - 旁白语言与音色（autofilm 会选已下载的音色；换其他音色需要下载，先征得同意）；
   - 结尾页联系方式。

   **无法询问**（批处理、子智能体、用户不在）时：不要停下，也不要下载。沿用 autofilm 选定的类型、风格、原创配乐和音色，联系方式取自文档（没有就留空），并在汇报里列出每一个假设。
4. **团队创作**：先读 autofilm 打印的范例片（`templates/golden/<结构>.json`，分章节巡礼用 `tour.json`；每个场景都有 `_why`）和 `references/copy-bank.md`，学手法，不抄句子。再读 `references/crew.md`，按顺序扮演各角色填写 `treatment.md`：制片 → 策略（目标受众、卖点 → 证明画面、AIDA）→ 创意总监（三个概念、选一个，再写**三句锚点**：开场句、高潮句、收尾句）→ 文案（完整脚本，每个场景一条；一个真实的行动号召）→ 美术指导与调色（配色、调色）→ 导演与摄影指导、动效与剪辑（分镜表：景别、运镜、转场）→ 作曲 → 品牌把关 → 设计评审。然后运行 `python3 scripts/check_treatment.py treatment.md` 直到通过。品味分低就重做你能改变的最弱环节，不要改分数，也不要停在关卡前；素材本身给不了的（占位图、照片太少）写进汇报，不计入分数。
5. **写入影片**：
   - 把方案中的文字写进 `film.json`，替换所有 `TODO`。
   - 三句锚点原样使用：开场句 → cover，高潮句 → finale，收尾句 → endcard。
   - 照片封面要给主体设 `focus`（`python3 scripts/subject_grid.py <照片> --preview .`，再用 `--cells B2,C3`）：开场先停在这个细节上，再拉开到全景。
   - 界面截图的要点已预填建议的 `rect`。用 `python3 scripts/suggest_rects.py <截图> --preview .` 画出编号框核对，每个要点对应它所说的那个框；真实照片（`"frame": "photo"`）不需要。不要给截图加 `"frame": "photo"` 来消除警告。
   - 场景类型与字段见 `references/film-spec.md`。
   - 然后运行 `check_treatment.py treatment.md film.json`：它检查片子说的是否就是方案里写的、证据句是否带有文档里的事实，并会给片子撑不起的品味分封顶。
6. **导演检查**：按 `references/director.md` 第 5 节检查。默认值已设好色彩脚本、击点、光效和声音；**镜头表**为每个场景自动选好版式、运镜和转场（`--stage check` 会打印，见第 6 节）。想更克制或更丰富，设 `"direction": {"variety": "calm" 或 "rich"}`；镜头表只是建议：任何场景的 `layout` / `camera` / `cut` / `motion` 都可以换，也可以自己设计（关键帧 `"cameras"` / `"cuts"`、`mg` 场景，见 `references/custom-scenes.md`），只要片子因此更好。
7. **检查**：`python3 scripts/make_film.py film.json --stage check` 直到没有 ERROR，文案检查的提示也要处理。
8. **构建 + 配音 + QA**：依次运行 `--stage build`、`--stage vo`、`--stage qa`，QA 必须 0 错误；能看图就看 `film_out/qa/sheet*.png`，不满意就改 `film.json`。
9. **渲染**：可选快速预览 `--stage render --draft`，再 `--stage finish --draft`。终版用**一条命令**连跑，中间不用等你：`python3 scripts/make_film.py film.json --stage render && python3 scripts/make_film.py film.json --stage finish`，需 5–20 分钟；若放在后台运行，等这条命令结束后再检查 `final/`（运动模糊只用于运动的帧）。
10. **汇报**：
    - 文件路径与选定的创意；
    - 未经询问而做的每一个假设；
    - 哪些是演示、占位或原创配乐；
    - 哪些没法验证（你听不到混音）；
    - 用户还需补充什么（`shot_wishlist.md` 中标 ✗ 的镜头；文档没有时，一个真实的行动号召）。

### 质量底线（默认值就是这样调出来的，别改坏）
- 一个核心概念、一个高潮；前 3 秒要抓人，最后 5 秒要完美。
- 切点在小节线上，一小节一个意思。
- 画面标签 ≤ 12 汉字 / 42 字符，字幕 ≤ 30 汉字。
- 不用空话（`scripts/lint_copy.py`）。
- 人声比音乐高约 10 dB，音效压在音乐之下。
- 每帧一个视觉焦点、一种强调色，边距 ≥ 96 px；QA 保证章节标签与字幕区不被遮挡。
- 每个功能最多 4 个要点，对比最多 6 行，产品阵列最多 6 个；宁可两个平静的场景，也不要一个拥挤的场景。
- 素材要清晰：界面按 2 倍（3840 宽）采集；`--stage check` 会在画面被放大超过 1.5 倍（发虚）或密集界面显示过小（看不清）时警告。修素材或换画面，不要忽略。

### 进阶（可选）
- 手动路线（不用 autofilm）：`templates/film.example.json` + `scripts/recommend_style.py` + `scripts/plan_storyboard.py`。
- 单独生成原创配乐：`python3 scripts/make_music.py --list`。
- 调整电影层：`"cinema": {...}`（见 `references/film-spec.md`）。
- 导演剪辑版——自定义场景、动效语言、运镜、转场与视觉：`references/custom-scenes.md`（示例：`templates/custom.example.js`）。
- 范例片（每种叙事结构一部，另有 `tour.json`；学文案和结构，不可直接构建）：`templates/golden/`。
- 实战案例：
  - `examples/demo/`：软件，使用用户音乐；
  - `examples/product-demo/`：实物产品，原创配乐，含完整团队方案；
  - `examples/medstat-pilot/`：3:26 正式成片。
- 安装到其他智能体：`references/agents.md`。
