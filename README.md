# Reelwright · 片匠

**Commercial-grade promo films for any product, from a folder of materials: an agent skill.**
**任何产品，一个素材文件夹，做出商业级宣传片：给 AI 智能体用的 skill。**

> *Reelwright*: a *reel* (film) and a *wright* (a maker, as in shipwright). The craftsperson who builds your film from your real material.
> *片匠*：以匠人之心，用你的真实素材一帧一帧打造片子。(Formerly `product-promo-film`.)

[English](#english) · [中文](#中文)

![cover](docs/gallery/cover.jpg)

<a id="english"></a>
## English

**Reelwright** is an agent skill that turns a folder into a promo film. Point an AI coding agent at a folder: screenshots, product photos or cut-outs, clips, a logo and a README. No screenshots? Point it at the installed app or a URL instead: `scripts/capture_app.mjs` drives the real app from a shot list and captures every screen at 3840×2160. Music is optional. It produces a 1080p film of 45 s to 4 min (the length follows the materials) with:
- a cover poster;
- real material animated with restraint, cut on the beat;
- an original underscore when you have no track;
- a natural English voice-over (local, open-source TTS);
- bilingual captions and SRT;
- an end card with your motto and contacts.

It works for software, apps, hardware, fashion, food, services, places and brands.

![any product](docs/gallery/any-product.jpg)

### How it gets to a top-tier result
- **It understands the product.**
  - `genres.py` classifies it into one of 15 genres (SaaS, developer and AI tools, science, fintech, consumer apps, electronics, fashion and luxury, food and drink, health, education, mobility, travel and living, games and events, kids, brand and mission). That sets the look, the motion, the story arc and the music.
  - `intake.py` tells screens, photos, cut-outs, figures and logos apart.
- **One folder, one command to a draft.** `autofilm.py <folder>` casts every material into the beat that suits it (reveal, detail, range, proof, hero…). It writes `film.json` and a `treatment.md` for the crew.
- **A built-in crew** (`references/crew.md`): producer, strategist, creative director, copywriter, a high-taste art director, motion designer and editor, composer, brand guardian and design critic. They write a treatment with three concepts, one chosen idea, a hook in 3 s, one hero moment, a tagline and a script.
  - `check_treatment.py` blocks the build until it is complete, consistent and scores ≥ 4/5 on taste. It also checks quality, not just form: proof lines must carry facts from the docs, the chosen concept must reach the film, film.json must say what the treatment says, and each self-score is capped by what the film can be measured to show.
  - `lint_copy.py` removes clichés and flags vague words.
  - **Golden films** (`templates/golden/`, one per story arc, every scene with a `_why`) and a **copy bank** (`references/copy-bank.md`) give mid-sized models something top-level to imitate.
- **No music? It composes one.** `make_music.py` writes an original, royalty-free underscore bar for bar from the scene plan. Sections change on the cuts, half a beat of silence falls before the hero, and the end rings out. There are 7 moods, from cinematic pulse to warm acoustic and luxe lounge.
- **The film is data, not code.**
  - `film.json` picks from 24 scene types: cover · pain · feature · carousel · numbers · gallery · clip · phone · compare · statement · finale · endcard; photo · hero · detail · lineup · quote · footage for physical products, places and people; flow · hub · type · chart · mg drawn in code; and `custom` for scenes you write yourself.
  - `make_film.py` runs check → build → voice → QA → render → finish, and every error prints a `FIX:` line.
- **Products with source code, in motion:** with the user's yes, `record_ui.mjs` runs the product's own frontend in a sandbox (its own port, an empty profile, localhost only, demo responses for the backend) and records scripted interactions at 30 fps with a gliding cursor; flows that cannot run there can be redrawn in code from the source, always labelled 界面示意 · Illustrative UI on screen.
- **Effects and transitions designed for the product:** keyframe cuts and moves anchored on an element (`"at"`): a zoom-through into the button or detail the story continues from, the product's own gesture as the effect (`references/director.md` §10).
- **A briefing before any work** (`scripts/briefing.py`): what the skill will do and will not do, what the user is responsible for, how long it takes, and the questions that shape the film; nothing starts until the user confirms.
- **The director proposes, the user decides** (`scripts/proposals.py`): 2–3 directions that look and move differently, each with a preview rendered from the real materials; the agent waits for the user's choice or changes, and the build refuses an unapproved draft.
- **A look chosen from the materials, not by product type** (`scripts/look.py`): it scores all 8 styles on what the pictures actually are and writes its reasons into the treatment; the user's own words for the feel (`--mood`) count triple.
- **A director that designs before it makes** (`scripts/director.py`): it reads every picture (screen or photo, dense or calm, the quiet side, where the subject sits) and gives each scene its own layout, camera move and cut, with the reason, in a storyboard you can read and overrule. 7 feature layouts, photo/gallery/carousel/detail variants, 15 camera moves (push, pan, crane, arc, dolly zoom, handheld…) and 12 cuts (rack focus, iris, doors, light leak, dip…), within the motion language's palette.
- **Free to design the motion:** the director's shot plan is a proposal. Agents write their own camera moves and cuts as keyframes in film.json, design motion-graphics scenes (`"type": "mg"`: text, shapes, lines, numbers and real images on beat keyframes, strokes that draw themselves), or drop to code; only honesty, rights and legible frames are fixed.
- **Story drawn in code, any product:** journey maps, many-into-one hubs, kinetic type and real-number charts glue the materials together; real footage plays from its best moment and can open the film.
- **A restrained director's cinema layer:** a colour script, a LUT grade, adaptive 180° motion blur, a subtle lens and light, and quiet synthesised sound design. Effects are felt, not seen.
- **Automatic layout QA** measures overlaps, off-frame content and caption collisions, so mid-sized models ship clean frames.
- **Highlight boxes that land on the element, for any product** (`scripts/snap.py`): every box snaps onto the real element under it (the page's own element boxes, else blocks found in the pixels), and the point's words move a box written on the wrong element (page texts, or the system's text recognition on any screenshot). Measured on random interfaces from no particular product (`evals/rects/`): a box written by eye frames its element 11 % of the time, after snapping 87–95 %.
- **Enforced gates:** no build before the treatment passes, no render before QA passes, no hand edits in `film_out/`, no downloads without the user's OK.
- **Measured on smaller models:** given one line, Claude Haiku's films matched the film Claude Opus made on the same materials (within critic noise) and beat it on others, in blind panels of three independent critics, with every honesty gate passing. `evals/` holds the test folders, the method and the full report ([evals/REPORT.md](evals/REPORT.md)).

### 8 visual styles × 6 motion languages
The look and the movement are chosen separately, and neither is a default: the director reads the materials (`scripts/look.py`: screens or photos, light or dark UI, saturation, density, charts, warm or cool hues) and scores all eight styles with written reasons.

| Style | Preview | Default motion | Suits |
| --- | --- | --- | --- |
| `midnight-tech` | ![](docs/gallery/midnight-tech.jpg) | `cinematic-3d` | platforms, B2B, serious tech |
| `keynote-light` | ![](docs/gallery/keynote-light.jpg) | `gentle-story` | consumer & productivity, care, hardware |
| `editorial-mono` | ![](docs/gallery/editorial-mono.jpg) | `editorial-type` | manifesto, brand, opinion |
| `aurora-glass` | ![](docs/gallery/aurora-glass.jpg) | `playful-pop` | consumer, creators, kids |
| `neon-cyber` | ![](docs/gallery/neon-cyber.jpg) | `kinetic-launch` | dev tools, AI agents, games, events |
| `paper-academic` | ![](docs/gallery/paper-academic.jpg) | `precision-data` | science, data, research, finance |
| `luxe-noir` | ![](docs/gallery/luxe-noir.jpg) | `gentle-story` | fashion, beauty, jewellery, premium hardware |
| `natural-fresh` | ![](docs/gallery/natural-fresh.jpg) | `gentle-story` | food & drink, wellness, travel, home, family |

The feature walkthrough has a different layout in each motion language:

![feature layouts](docs/gallery/motions.jpg)

### Director's cinema layer: restrained, professional, premium
How a top commercial director works is turned into automatic defaults. The guide is [references/director.md](references/director.md).
- **Colour:** a colour script (cold "before", honest product, a slightly richer peak, a warm close), and a LUT per style blended at 50 % so real UI and product colours stay true.
- **Camera:** barely-there handheld, edge depth of field and a focus pull. Camera cuts happen only where the story turns.
- **Light:** soft glints, faint rays, and one anamorphic flare on the hero moment.
- **Sound:** about 10 quiet cues a minute, under the music.
- **Control:** `"cinema": "auto"` is the default; `"off"` turns it off; an object tunes it. `--draft` gives quick looks.

![cinema off vs auto](docs/gallery/cinema.jpg)

### Install
```bash
git clone https://github.com/CalebChen941028/reelwright.git
cd reelwright
./install.sh                 # ~/.agents/skills + Claude Code + Codex   (Windows: .\install.ps1)
./install.sh all             # + OpenCode, Antigravity, DeepSeek Harness, Kimi Code, Cursor, Copilot, Gemini CLI, Qwen Code, Trae
npm install && npx playwright install chromium   # Playwright lives in this folder; the installed copies read it from here (any order works)
python3 scripts/doctor.py
```
Keep the cloned folder where it is: if you move it, run `./install.sh` again.
Where each agent looks for skills: [references/agents.md](references/agents.md). Agents without skill support: point them at [AGENTS.md](AGENTS.md).

### Quick start
Ask your agent: *"Make a promo film for my product from ~/materials with the Reelwright skill."* It follows [SKILL.md](SKILL.md):
```bash
python3 scripts/briefing.py --project ~/my-film --materials ~/materials   # show the briefing, wait, then --ack "<the user's reply>"
python3 scripts/autofilm.py ~/materials --out ~/my-film --mood "<the user's words>"   # draft: genre, look, arc, music, film.json, treatment.md
python3 scripts/proposals.py ~/my-film/film.json              # 2–3 directions with previews; wait, then --apply <A|B|C>
# the crew fills treatment.md and every TODO (references/crew.md), then:
python3 scripts/check_treatment.py ~/my-film/treatment.md ~/my-film/film.json
python3 scripts/make_film.py ~/my-film/film.json              # check → build → voice → QA → render → finish
```
Examples:
- [examples/product-demo](examples/product-demo): a physical product, no music supplied, with the full crew treatment.
- [examples/demo](examples/demo): software, the user's track.
- [examples/medstat-pilot](examples/medstat-pilot): a verified shot list for an installed desktop app, with its demo data and scripted AI replies.

### Requirements
- Python 3.9+ with numpy and Pillow.
- Node 18+ with Playwright (Chromium).
- ffmpeg (`pip install imageio-ffmpeg` works).
- Optional, for the voice-over: Kokoro (Apache-2.0) in a Python 3.12 venv; see [references/audio.md](references/audio.md).

### Docs
- [SKILL.md](SKILL.md): the procedure.
- [crew](references/crew.md): the roles and the taste rubric.
- [copy bank](references/copy-bank.md) and [golden films](templates/golden): what top-level copy and structure look like, per arc and genre.
- [genres](references/genres.md): product type → story arc, music, voice (the look is chosen from the materials).
- [director](references/director.md): colour, camera, light, sound, restraint.
- [film-spec](references/film-spec.md): every `film.json` field.
- [materials](references/materials.md): what to put in the folder.
- [styles](references/styles.md), [motion](references/motion.md), [audio](references/audio.md).
- [custom scenes](references/custom-scenes.md): your own scenes, motion graphics, keyframe moves and cuts, redrawn UI.
- [storyboard](references/storyboard.md), [capture](references/capture.md) (incl. `record_ui.mjs`), [qa](references/qa.md), [troubleshooting](references/troubleshooting.md), [agents](references/agents.md).
- [evals](evals/README.md): blind tests on smaller models and the product-agnostic box benchmarks.

### Credits & licences
- **Reelwright:** MIT. © 2026 Liangliang Chen (陈亮亮), [github.com/CalebChen941028](https://github.com/CalebChen941028), WeChat official account 科研牛马研习社. Built with Codex & Claude.
- **Not bundled, installed by you:** Playwright (Apache-2.0), Kokoro-82M (Apache-2.0), ffmpeg (LGPL/GPL builds).
- **Demo music** (`examples/demo/demo-music.m4a`): original, CC0. Music composed by `make_music.py` is yours to use.
- **Placeholders:** the product-demo images are drawn placeholders for a fictional brand.
- Use only material, music and voices you have the rights to.

<a id="中文"></a>
## 中文

**Reelwright · 片匠**：把一个文件夹交给 AI 编程智能体：截图、产品照片或透明底产品图、录屏、Logo、README，音乐可有可无。没有截图时，也可以直接指向已安装的应用或网址：`scripts/capture_app.mjs` 按镜头清单操作真实应用，以 3840×2160 采集每一屏。它会做出一部 45 秒到 4 分钟的 1080p 宣传片（片长取决于素材多少）：
- 封面海报；
- 克制而有节奏的真实素材动效，切点卡在节拍上；
- 没有音乐时自动原创配乐；
- 自然的英文配音（本地开源 TTS）；
- 中英双语字幕与 SRT；
- 带理念和联系方式的结尾页。

适用于软件、App、硬件、时尚、食品、服务、空间与品牌。

### 怎样做到顶级效果
- **先理解产品**：
  - `genres.py` 把产品归入 15 类之一（SaaS、开发者与 AI 工具、科研、金融、消费级 App、消费电子、时尚奢品、食品饮品、健康、教育、出行工业、旅行家居、游戏活动、儿童、品牌公益），据此决定风格、动效、叙事结构与音乐。
  - `intake.py` 自动区分界面截图、照片、透明底产品图、图表与 Logo。
- **一个文件夹，一条命令出草稿**：`autofilm.py <文件夹>` 把每份素材分配到最合适的拍点（揭晓、细节、系列、证明、高潮……），写出 `film.json` 和供团队填写的 `treatment.md`。
- **内置制作团队**（`references/crew.md`）：制片、策略、创意总监、文案、高品味美术指导、动效与剪辑、作曲、品牌把关、设计评审。他们产出包含三个概念、选定创意、3 秒钩子、唯一高潮、口号与脚本的创意方案。
  - `check_treatment.py` 在方案完整、一致且品味评分 ≥ 4/5 之前阻止构建；它也检查质量而不只是格式：证据句要带文档里的事实，选定的创意要进入片子，film.json 要与方案一致，自评分会被片子可测量的表现封顶。
  - `lint_copy.py` 清除空话套话，并标出含糊的词。
  - **范例片**（`templates/golden/`，每种叙事结构一部，每个场景都有 `_why`）与**文案范例库**（`references/copy-bank.md`），让中等规模的模型有顶级水准可以模仿。
- **没有音乐就作曲**：`make_music.py` 按场景逐小节原创无版权配乐，段落在切点变化，高潮前留半拍静默，结尾自然收束；有七种情绪可选。
- **片子是数据而不是代码**：
  - `film.json` 从 24 种场景中选择：基础场景；photo · hero · detail · lineup · quote · footage 用于实物产品、空间与人物；flow · hub · type · chart · mg 用代码绘制；`custom` 用于自己编写的场景。
  - `make_film.py` 一条命令完成检查到交付，出错时给出 `FIX:`。
- **有源码的产品也能流畅演示**：用户同意后，`record_ui.mjs` 在沙盒里运行产品自己的前端（独立端口、空白配置、只访问本机、后端用演示数据），按脚本操作并以 30 帧录制，带平滑光标；沙盒里跑不起来的流程可按源码用代码重绘，画面上始终标注“界面示意 · Illustrative UI”。
- **按产品设计特效与转场**：关键帧转场和运镜可锚定在画面元素上（`"at"`）：穿越推进到故事接下来的按钮或细节，用产品本身的动作做特效（`references/director.md` 第 10 节）。
- **开工前先说明**（`scripts/briefing.py`）：会做什么、不会做什么、用户需负责什么、大概多久，以及决定成片效果的问题；用户确认后才开始。
- **导演提方案，用户来拍板**（`scripts/proposals.py`）：2–3 套在视觉和动效上都不同的方向，每套附真实素材渲染的预览；智能体等待用户选择或修改，没有确认方向的草稿无法构建。
- **视觉风格由素材决定，不按产品类型套用**（`scripts/look.py`）：按图片的真实情况给 8 种风格打分并把理由写进方案；用户描述风格的用词（`--mood`）权重三倍。
- **动效可以自由设计**：导演的镜头表只是建议。智能体可以在 film.json 里用关键帧写自己的运镜和转场，设计 MG 动画场景（`"type": "mg"`：文字、形状、线条、数字和真实图片按节拍关键帧运动，描边可自动画出），也可以写代码；固定不变的只有诚实、版权和画面清晰。
- **先设计、后制作的导演**（`scripts/director.py`）：读懂每张画面（截图还是照片、密还是疏、哪一侧安静、主体在哪），为每个场景选好版式、运镜和转场并写明理由，生成可读、可改的分镜表。功能场景 7 种版式，照片、画廊、轮播、细节各有变体，15 种运镜（推拉、横移、升降、环绕、希区柯克变焦、手持……）、12 种转场（焦点转移、圆形展开、对开、漏光、黑场……），都在本片动效语言的调色板之内。
- **用代码讲故事，适用于任何产品**：旅程图、多合一汇聚、动态文字、真实数字图表把素材串起来；实拍视频从最好的片段播放，也可以做开场。
- **克制的导演电影层**：色彩脚本、LUT 调色、自适应 180° 运动模糊、含蓄的镜头与光效、轻声的合成声音设计；效果感受得到，看不出来。
- **自动版式 QA**：用数值检测重叠、出画、字幕冲突，中等规模的模型也能交出干净的画面。
- **高亮框落在元素上，适用于任何产品**（`scripts/snap.py`）：每个框吸附到它下面的真实元素（页面自己的元素位置，否则用像素识别的块），要点的文字会把写在错误元素上的框移到正确的卡片（页面文字，或在任何截图上用系统文字识别）。在与具体产品无关的随机界面上实测（`evals/rects/`）：目测写的框准确率 11%，吸附后 87–95%。
- **强制关卡**：方案未通过不构建，QA 未通过不渲染，不许手改 `film_out/`，未经用户同意不下载。
- **在较小模型上实测**：只给一句提示，Claude Haiku 做出的片子在三位独立评审的盲评中，同一素材上与 Claude Opus 制作的片子持平（在评审波动范围内），其他素材上超过它，且所有诚实性关卡都通过。`evals/` 里有测试素材、方法和完整报告（[evals/REPORT.md](evals/REPORT.md)）。

### 8 种视觉风格 × 6 种动效语言
风格与动效分开选择，都由导演读素材后决定（没有默认值，见 `scripts/look.py`）；对照表与预览见上方英文部分。新增 `luxe-noir`（安静的奢华感：时尚、美妆、珠宝、高端硬件）与 `natural-fresh`（日光与材质：食品、身心健康、旅行、家居、亲子）。

### 安装与快速开始
安装命令见上方英文部分：克隆后运行 `./install.sh`，并在克隆的文件夹里运行 `npm install && npx playwright install chromium`（先后顺序不限；安装副本通过 `.source` 文件读取这里的 Playwright，所以请保留这个文件夹，移动后重新运行 `./install.sh`）。使用流程见上方英文部分（开工说明 → 起草 → 方案选择 → 团队创作 → 构建）。对智能体说：“用 Reelwright（片匠）skill，根据 ~/materials 里的素材给我的产品做一部宣传片”，它会按 [SKILL.md](SKILL.md) 执行。示例：
- [examples/product-demo](examples/product-demo)：实物产品，无音乐，含完整团队方案。
- [examples/demo](examples/demo)：软件，使用用户音乐。
- [examples/medstat-pilot](examples/medstat-pilot)：已安装桌面应用的已验证镜头清单，含演示数据与脚本化 AI 回复。

### 署名与许可
- **Reelwright · 片匠**：MIT 许可。© 2026 陈亮亮，[github.com/CalebChen941028](https://github.com/CalebChen941028)，微信公众号：科研牛马研习社。由 Codex 与 Claude 协作开发。
- **不随仓库分发、需自行安装**：Playwright、Kokoro-82M、ffmpeg。
- **示例音乐**：原创，CC0；`make_music.py` 生成的配乐可自由使用。
- **占位图**：产品示例中的图片是虚构品牌的绘制占位图。
- 请只使用你有权使用的素材、音乐和声音。
