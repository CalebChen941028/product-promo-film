---
name: product-promo-film
description: Make a commercial-grade product promo film (1–4 min, 1080p, landscape) from a product's REAL UI and the user's materials — screenshots, screen recordings, logo, music — with 6 visual styles × 6 theme-driven motion languages, a director's cinema layer (colour script, LUT grade, motion blur, lens + light effects, synthesised sound design), beat-synced cuts, natural English voice-over (local Kokoro TTS), bilingual captions, cover poster and SRT. Declarative film.json + one command (make_film.py) with automatic layout QA, so any capable agent gets a polished result. Use for promo / launch / ad / explainer videos, 宣传片, 产品视频, product films.
---

# Product Promo Film · 软件产品宣传片

> **English first, 中文在后。** Follow the steps literally. Every script prints `FIX:` lines when something is wrong — do what they say, then rerun. Never hand-edit generated files (`film_out/`); edit `film.json`.
>
> 严格按步骤执行。脚本出错时会打印 `FIX:`，照做后重跑即可。不要手改 `film_out/` 里的生成文件，只改 `film.json`。

## English

### What you deliver
| File | Spec |
| --- | --- |
| `final/<name>-1080p.mp4` | H.264 1920×1080 30 fps, AAC 48 kHz, −14 LUFS; graded, motion-blurred, with sound design |
| `final/<name>-cover-4k.png`, `-cover-1280.jpg` | poster = the cover frame |
| `final/<name>.bilingual/zh/en.srt` | captions aligned to the voice-over |
| `film.json` | the editable source of the whole film |

### Hard rules
1. **Real UI only.** Product screens come from the user's files or from capturing the running product (`scripts/capture_kit.mjs`). Never draw a fake UI to pass as the product.
2. **Be honest.** Mark demo data as demo. If AI output was produced by a mock, say so. Every on-screen claim (numbers, platforms, privacy) must be checkable in the user's docs or code.
3. **Licences.** Music: only what the user provides (or licensed). Voice: Kokoro (Apache-2.0) or the user's recordings — never OS system voices (non-commercial licences). Ask before downloading models; say name, source, size.
4. **Secrets.** Never type a user's API key into an app or config. Ask the user to do it.
5. **Do not render before QA passes** (`--stage qa` → 0 errors).

### Steps (do them in order)
1. **Environment** — `python3 scripts/doctor.py`. Fix every `MISS` line. (One-time: `npm i playwright && npx playwright install chromium` in this folder.)
2. **Collect materials** into one folder (`materials/`): screenshots (2× preferred), screen recordings, logo (transparent PNG), music file, any docs. Then
   `python3 scripts/intake.py materials --out build --ffmpeg <ffmpeg>` → `build/manifest.json` (roles, sizes, `base` for each image, WebM clips) and a list of what is missing. Ask the user for missing items.
3. **Write the brief** — copy `templates/brief.example.json` to `brief.json` and fill it with the user (product name, one-liner, audience, 3–6 features with their materials, 2–6 differentiators, motto, contacts, platforms, status). Facts only.
4. **Pick look + motion by theme** — `python3 scripts/recommend_style.py brief.json --grid build/grid.json` (run `scripts/beat_grid.py <music> --out build/grid.json` first). Show the top 3 to the user; use their choice. Tables: `references/styles.md`, `references/motion.md`.
5. **Plan bars** — `python3 scripts/plan_storyboard.py build/grid.json brief.json --out storyboard.md` gives music sections and a scene draft. Total scene bars must fit the music; if not, extend the music (`"music": {"extend": {...}}`, see `references/audio.md`) or cut scenes.
6. **Write film.json** — copy `templates/film.example.json` (or `examples/demo/film.json`). One entry per scene from the library: `cover · pain · feature · carousel · numbers · gallery · clip · phone · compare · statement · finale · endcard`. Each needs `bars` and its fields (`references/film-spec.md`). Narration goes in each scene's `say` list (`en` spoken, `zh` caption, optional `cap` for on-screen digits). Rects for `feature.points`: measure with `python3 scripts/grid_overlay.py grids/ <image>` (base coordinates).
7. **Direct** — read `references/director.md` §5 and do the director's pass in film.json. Defaults already give a colour script, hits, camera cuts, light and sound design (`"cinema": "auto"`). Defaults are deliberately restrained: calm, professional, premium. Only add `"hit"`, `"mood"` or `"cut"` on a scene to change a beat on purpose. Keep exactly one hero moment, and never turn effects up just to be noticed.
8. **Check** — `python3 scripts/make_film.py film.json --stage check`. Repeat until no ERROR.
9. **Build + voice + QA** — `python3 scripts/make_film.py film.json --stage build`, then `--stage vo`, then `--stage qa`. QA must report 0 errors. If you can view images, read `film_out/qa/sheet*.png` and fix anything ugly via film.json. Optional quick look: `python3 scripts/make_film.py film.json --stage render --draft` then `--stage finish --draft`.
10. **Render + finish** — `python3 scripts/make_film.py film.json --stage render`, then `--stage finish`. Final quality renders 4 motion-blur samples per frame, about 4× the draft time: roughly 20–40 min for 3 minutes.
11. **Report** to the user: file paths; what is demo/simulated; what you could not verify (you cannot hear the mix); what they must supply (download link, QR code).

### Quality bar (why the defaults look good — keep them)
- Cuts land on bar lines; one idea per bar; text ≤ 14 Chinese characters per on-screen label, captions ≤ 30.
- Speech sits ~10 dB above the music (mix_audio.py). Natural voice speed 1.0 (max 1.12).
- Windows ≤ 1400 px wide and centred; the chapter label (top-left) and captions (bottom 250 px) stay clear — QA enforces this.
- Max 4 points per feature scene, max 6 comparison rows; prefer two scenes over one crowded scene.
- One hero moment, one accent colour at a time, a camera cut only where the story turns, and sound only where the picture moves (`references/director.md`).

### Going further (optional)
- Tune the cinema layer: `"cinema": {"grade": "teal-orange", "grade_strength": 0.5, "motion_blur": 4, "bloom": 0.2, "grain": 0.3, "sfx_gain_db": -3, "lens": {"shake": 0}}`, or `"cinema": "off"` (`references/film-spec.md`).
- Custom scenes in JS: `templates/scenes.example.js`, `templates/library.js`, `templates/patterns.js`, engine API at the top of `templates/engine.js`.
- Capturing a running web app with Playwright, mock local AI for filming: `references/capture.md`.
- Worked production example (3:26 film, hand-written scenes): `examples/medstat-pilot/`.
- Install for other agents: `references/agents.md`.

## 中文

### 交付物
| 文件 | 规格 |
| --- | --- |
| `final/<名称>-1080p.mp4` | H.264 1920×1080 30fps，AAC 48kHz，响度 −14 LUFS |
| `final/<名称>-cover-4k.png`、`-cover-1280.jpg` | 封面海报（片头封面定帧） |
| `final/<名称>.bilingual/zh/en.srt` | 与配音对齐的字幕 |
| `film.json` | 整部片子的可编辑源文件 |

### 硬性规则
1. **只用真实界面**：产品画面来自用户提供的素材，或用 `scripts/capture_kit.mjs` 从运行中的产品采集；不得画假界面冒充产品。
2. **诚实**：演示数据要标注；AI 内容若来自 mock，要明确告知；画面上的数字、平台、隐私说法都要能在用户的文档或代码里核实。
3. **授权**：音乐只用用户提供或已授权的；配音用 Kokoro（Apache-2.0）或用户录音，不用系统自带语音（非商用许可）；下载模型前先说明名称、来源、大小并征得同意。
4. **密钥**：不要替用户把 API Key 填进应用或配置文件，请用户自己操作。
5. **QA 不过不渲染**（`--stage qa` 必须 0 个 ERROR）。

### 步骤（按顺序）
1. **环境**：`python3 scripts/doctor.py`，修好所有 `MISS`（首次需在本目录 `npm i playwright && npx playwright install chromium`）。
2. **收集素材**到 `materials/`：截图（最好 2 倍分辨率）、录屏、Logo（透明 PNG）、音乐、文档；运行 `python3 scripts/intake.py materials --out build --ffmpeg <ffmpeg>`，得到 `build/manifest.json`（角色、尺寸、每张图的 `base`、转好的 WebM），并列出缺什么，缺的向用户要。
3. **写 brief**：复制 `templates/brief.example.json` 为 `brief.json`，与用户一起填写（产品名、一句话定位、受众、3–6 个功能及对应素材、2–6 条差异点、理念、联系方式、平台、版本状态），只写事实。
4. **按主题选风格与动效**：先 `scripts/beat_grid.py <音乐> --out build/grid.json`，再 `python3 scripts/recommend_style.py brief.json --grid build/grid.json`，把前三名给用户选。对照表见 `references/styles.md`、`references/motion.md`。
5. **排小节**：`python3 scripts/plan_storyboard.py build/grid.json brief.json --out storyboard.md`，得到音乐段落与场景草稿；场景小节总数要放得进音乐，放不下就延长音乐或删场景。
6. **写 film.json**：复制 `templates/film.example.json`（或 `examples/demo/film.json`）。每个场景从场景库里选类型：`cover · pain · feature · carousel · numbers · gallery · clip · phone · compare · statement · finale · endcard`，填 `bars` 和字段（`references/film-spec.md`）。旁白写在场景的 `say` 里（`en` 念出来，`zh` 字幕，`cap` 可选，用来在画面上显示数字）。`feature.points` 的坐标用 `scripts/grid_overlay.py` 量（base 坐标）。
7. **导演检查**：读 `references/director.md` 第 5 节，在 film.json 里完成导演检查。默认（`"cinema": "auto"`）已有色彩脚本、击点、镜头转场、光效和声音设计；默认值刻意克制：平静、专业、高级。只有要刻意改变某个拍点时，才在场景上加 `"hit"`、`"mood"` 或 `"cut"`；全片只保留一个高潮，不要为了“显眼”而加强效果。
8. **检查**：`python3 scripts/make_film.py film.json --stage check`，直到没有 ERROR。
9. **构建 + 配音 + QA**：依次 `--stage build`、`--stage vo`、`--stage qa`，QA 必须 0 个错误；能看图就看 `film_out/qa/sheet*.png`，不满意就改 film.json。可选快速预览：`--stage render --draft`，再 `--stage finish --draft`。
10. **渲染 + 收尾**：`--stage render`，再 `--stage finish`。终版每帧 4 次运动模糊采样，耗时约为草稿的 4 倍：3 分钟成片约 20–40 分钟。
11. **汇报**：文件路径；哪些是演示 / 模拟内容；哪些没法验证（你听不到声音）；用户还需要补什么（下载链接、二维码等）。

### 质量底线（默认值就是这样调出来的，别改坏）
- 切点在小节线上，一个小节一个意思；画面标签不超过 14 个汉字，字幕不超过 30 个汉字。
- 人声比音乐高约 10 dB；语速 1.0（最多 1.12）。
- 窗口宽度不超过 1400 px 并居中；左上章节标签与底部 250 px 字幕区不被遮挡（QA 会检查）。
- 每个功能场景最多 4 个要点，对比表最多 6 行；宁可拆成两个场景，也不要挤在一起。
- 只有一个高潮；同一时间只有一种强调色；只在故事转折处用镜头转场；画面动才有声音（`references/director.md`）。

### 进阶（可选）
- 调整电影层：`"cinema": {"grade": "teal-orange", "grade_strength": 0.5, "motion_blur": 4, "bloom": 0.2, "grain": 0.3, "sfx_gain_db": -3, "lens": {"shake": 0}}`，或 `"cinema": "off"`（见 `references/film-spec.md`）。
- 自写 JS 场景：`templates/scenes.example.js`、`library.js`、`patterns.js`，引擎 API 见 `engine.js` 开头。
- 用 Playwright 采集运行中的 Web 应用、用本地 mock 模型拍 AI 功能：`references/capture.md`。
- 完整实战（3:26 成片，手写场景）：`examples/medstat-pilot/`。
- 安装到其他智能体：`references/agents.md`。
