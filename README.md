# product-promo-film

**Commercial-grade product promo films from your real UI — an agent skill.**
**用软件的真实界面，做出商业级宣传片 —— 一个给 AI 智能体用的 skill。**

[English](#english) · [中文](#中文)

![cover](docs/gallery/cover.jpg)

<a id="english"></a>
## English

Give an AI coding agent your product's screenshots, screen recordings, logo and a music track. It produces a 1–4 minute 1080p film:
- cover poster
- real UI animated in 3D, with cuts on the beat
- natural English voice-over (local, open-source TTS)
- bilingual captions + SRT
- a balanced end card with your motto and contacts

It was built while making the MedStat Pilot launch film and generalised so that **mid-sized models can reach the same quality**.

### Why it works with many agents and models
- **The film is data, not code.** A `film.json` lists scenes from a library (`cover · pain · feature · carousel · numbers · gallery · clip · phone · compare · statement · finale · endcard`), each with bars, text and screenshot regions.
- **One command:** `make_film.py` runs check → build → voice → QA → render → mix → deliver. Every error prints a `FIX:` line.
- **Automatic layout QA:** text overlaps, off-frame elements, chapter-label and caption collisions are measured, so no visual judgement is needed.
- **Tuned defaults** from a finished commercial film: sizes, timings, mix levels (speech +10 dB over music, −14 LUFS).
- **A director's cinema layer, restrained by default:** a colour script across scenes, a LUT grade, 180° motion blur, a subtle lens and light, and synthesised sound design. One hero moment.

### 6 visual styles × 6 motion languages
The **look** (style) and the **movement** (motion language) are chosen separately. Motion follows the theme of your materials; `recommend_style.py` suggests pairs from your brief and music. Each row below is a style with its default motion; any style can take any motion (`"motion"` in film.json).

| Style | Preview (feature scene) | Default motion language | Theme it suits |
| --- | --- | --- | --- |
| `midnight-tech` | ![](docs/gallery/midnight-tech.jpg) | `cinematic-3d` | platforms, B2B, serious tech |
| `keynote-light` | ![](docs/gallery/keynote-light.jpg) | `gentle-story` | care, education, mission |
| `editorial-mono` | ![](docs/gallery/editorial-mono.jpg) | `editorial-type` | manifesto, brand, opinion |
| `aurora-glass` | ![](docs/gallery/aurora-glass.jpg) | `playful-pop` | consumer, creators, social |
| `neon-cyber` | ![](docs/gallery/neon-cyber.jpg) | `kinetic-launch` | dev tools, security, AI agents |
| `paper-academic` | ![](docs/gallery/paper-academic.jpg) | `precision-data` | science, data, research, finance |

Each motion language also has its own layout for a feature walkthrough:
- **cinematic-3d:** a 3D window with tags.
- **precision-data:** a spec sheet with drawn leader lines.
- **kinetic-launch:** zoom bursts with slammed headlines.
- **gentle-story:** slow Ken Burns, one line at a time.
- **playful-pop:** sticker bubbles.
- **editorial-type:** a magazine split screen.

![feature layouts](docs/gallery/motions.jpg)

### Director's cinema layer: restrained, professional, premium
How a top commercial director works (colour script, grade, lens, light, cuts, sound, finish) is turned into automatic defaults. The guide is [references/director.md](references/director.md). Restraint is the rule: effects are felt, not seen, and the film has exactly one hero moment.
- **Colour script:** a cold "before", a neutral and honest product, a slightly richer peak, a warm close. The shifts are small and glide across cuts.
- **Grade + finish:** a LUT per style, blended at 50 % so the real UI colours stay true. Fine grain and gentle bloom, plus 4-sample 180° motion blur.
- **Lens:**
  - A barely-there handheld drift, edge depth of field and a short focus pull as each scene lands.
  - Camera cuts (whip or push) only where the story turns.
- **Light:**
  - A soft glint crosses each window once.
  - Faint rays sit behind the cover logo and the hero tagline.
  - One anamorphic flare appears, on the hero moment only.
- **Sound design (synthesised, royalty-free):** about 10 quiet cues a minute. Sounds come only on camera cuts and hits, with one impact plus riser for the hero. The palette follows the motion language.
- **Control:**
  - `"cinema": "auto"` is the default; `"off"` turns it off; a `{...}` object tunes it.
  - Per scene: `mood`, `cut`, `hit`.
  - `--draft` gives fast previews.

![cinema off vs auto](docs/gallery/cinema.jpg)

### Install
```bash
git clone https://github.com/CalebChen941028/product-promo-film.git
cd product-promo-film
./install.sh                 # ~/.agents/skills + Claude Code + Codex   (Windows: .\install.ps1)
./install.sh all             # + OpenCode, Antigravity, DeepSeek Harness, Kimi Code, Cursor, Copilot, Gemini CLI, Qwen Code, Trae
npm i playwright && npx playwright install chromium
python3 scripts/doctor.py
```
Where each agent looks for skills: [references/agents.md](references/agents.md). Agents without skill support: point them at [AGENTS.md](AGENTS.md).

### Quick start
```bash
cd examples/demo
python3 ../../scripts/make_film.py film.json --stage check
python3 ../../scripts/make_film.py film.json          # build → voice → QA → render → finish
```
The demo uses placeholder UI and an original public-domain track. For your product, ask your agent: *"Make a promo film for my product with the product-promo-film skill"*. It will follow [SKILL.md](SKILL.md).

### Requirements
- Python 3.9+ with numpy and Pillow
- Node 18+ with Playwright (Chromium)
- ffmpeg (`pip install imageio-ffmpeg` works)
- Optional, for the voice-over: a Python 3.12 venv with [Kokoro](https://github.com/hexgrad/kokoro) (Apache-2.0); setup in [references/audio.md](references/audio.md)

### Docs
- [SKILL.md](SKILL.md): the procedure
- [director](references/director.md): colour, camera, light, rhythm, sound, and restraint
- [film-spec](references/film-spec.md)
- [styles](references/styles.md)
- [motion](references/motion.md)
- [materials](references/materials.md)
- [capture](references/capture.md)
- [audio](references/audio.md)
- [storyboard](references/storyboard.md)
- [qa](references/qa.md)
- [troubleshooting](references/troubleshooting.md)
- [agents](references/agents.md)

### Credits & licences
- **This skill:** MIT. © 2026 Liangliang Chen (陈亮亮), [github.com/CalebChen941028](https://github.com/CalebChen941028), WeChat official account 科研牛马研习社. Built with Codex & Claude.
- **Not bundled, installed by you:** Playwright (Apache-2.0), Kokoro-82M (Apache-2.0), ffmpeg (LGPL/GPL builds).
- **Demo music** (`examples/demo/demo-music.m4a`): original, CC0.
- Use only music and voices you have the rights to.

<a id="中文"></a>
## 中文

把产品的截图、录屏、Logo 和一段音乐交给 AI 编程智能体，它就能做出一部 1–4 分钟的 1080p 宣传片：
- 封面海报
- 真实界面的 3D 动效演示，切点卡在节拍上
- 自然的英文配音（本地开源 TTS）
- 中英双语字幕与 SRT
- 居中协调、带理念与联系方式的结尾页

这个 skill 来自 MedStat Pilot 宣传片的实战，并做了通用化，**让中等规模的模型也能做出同样水准的作品**。

### 为什么很多智能体和模型都能用好
- **片子是数据而不是代码**：`film.json` 从场景库里选场景（封面、痛点、功能演示、工具轮播、大数字、结果图集、录屏、手机、对比、宣言、高潮、结尾页），每个场景只需填写小节数、文字和截图区域。
- **一条命令**：`make_film.py` 依次完成检查 → 构建 → 配音 → QA → 渲染 → 混音 → 交付，出错时给出 `FIX:` 修复指令。
- **自动版式 QA**：用数值检测文字重叠、出画、章节标签与字幕冲突，不依赖视觉判断。
- **调好的默认值**：尺寸、节奏、混音电平（人声比音乐高约 10 dB，成片 −14 LUFS）都来自完成的商业成片。
- **导演电影层（默认克制）**：跨场景的色彩脚本、LUT 调色、180° 运动模糊、含蓄的镜头与光效、合成声音设计；全片只有一个高潮。

### 6 种视觉风格 × 6 种动效语言
**画面风格**与**动效语言**分开选择；动效依据素材传递的主题来选，`recommend_style.py` 会根据 brief 和音乐推荐搭配（对照表见上方英文部分）。每种动效语言对“功能演示”也有不同版式：
- **cinematic-3d**：3D 窗口加标签。
- **precision-data**：规格表加绘制引线。
- **kinetic-launch**：放大爆发加大标题。
- **gentle-story**：慢速推拉，一次一句。
- **playful-pop**：贴纸气泡。
- **editorial-type**：杂志分屏。

### 导演电影层：克制、专业、高级
把顶级广告导演的做法（色彩脚本、调色、镜头、光、转场、声音、成片质感）变成自动默认值，手册见 [references/director.md](references/director.md)。原则是克制：效果“感受得到，看不出来”，全片只有一个高潮。
- **色彩脚本**：冷色的“过去”，中性真实的产品，略微饱满的高潮，温暖的结尾；变化幅度小，跨切点平滑过渡。
- **调色与质感**：每种风格一个 LUT，按 50% 混合，保证真实界面颜色不失真；细腻颗粒、轻微辉光；每帧 4 次采样的 180° 运动模糊。
- **镜头**：
  - 几乎察觉不到的手持漂移、边缘景深、场景落定时的短暂对焦。
  - 只在故事转折处用镜头转场（甩镜或推进穿越）。
- **光**：
  - 每个窗口扫过一次柔和高光。
  - 封面 Logo 和高潮口号后有淡淡光芒。
  - 只在高潮出现一次宽银幕光晕。
- **声音设计（程序合成，无版权问题）**：约每分钟 10 个轻声音效，只在镜头转场和击点出现，高潮有一次重击加上升音；音色随动效语言变化。
- **控制**：
  - 默认 `"cinema": "auto"`，用 `"off"` 关闭，或用 `{...}` 对象微调。
  - 每个场景可设 `mood`、`cut`、`hit`。
  - `--draft` 快速预览。

### 安装
命令同上方英文部分。`./install.sh all` 会同时安装到 OpenCode、Antigravity、DeepSeek Harness、Kimi Code、Cursor、Copilot、Gemini CLI、Qwen Code、Trae 等的目录。各智能体的目录见 [references/agents.md](references/agents.md)；不支持 skill 的智能体请让它读取 [AGENTS.md](AGENTS.md)。

### 快速开始
运行 `examples/demo` 里的示例（占位界面 + 原创公有领域音乐）。做自己产品的片子时，对智能体说：“用 product-promo-film skill 给我的产品做一部宣传片”，它会按 [SKILL.md](SKILL.md) 执行。

### 环境要求
- Python 3.9+（numpy、Pillow）
- Node 18+ 与 Playwright（Chromium）
- ffmpeg（可用 `pip install imageio-ffmpeg`）
- 可选：配音需要 Python 3.12 虚拟环境与 Kokoro（Apache-2.0），安装方法见 [references/audio.md](references/audio.md)

### 署名与许可
- **本 skill**：MIT 许可。© 2026 陈亮亮，[github.com/CalebChen941028](https://github.com/CalebChen941028)，微信公众号：科研牛马研习社。由 Codex 与 Claude 协作开发。
- **不随仓库分发、需自行安装**：Playwright（Apache-2.0）、Kokoro-82M（Apache-2.0）、ffmpeg。
- **示例音乐**：原创，CC0。
- 请只使用你有权使用的音乐和声音。
