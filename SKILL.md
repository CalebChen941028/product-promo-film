---
name: product-promo-film
description: Make a commercial-grade promo film (1–4 min, 1080p, landscape) for ANY product — software, apps, hardware, fashion, food, services, brands — from the user's materials folder (screenshots, photos, product cut-outs, clips, logo, docs), with or without the user's music. Classifies the product into 15 genres to pick the look (8 styles), motion (6 theme-driven languages), story arc and an original composed underscore when no track is given. A built-in crew (strategist, creative director, copywriter, art director, editor, composer, brand guardian, design critic) writes a checked treatment. A restrained director's cinema layer adds colour script, LUT grade, motion blur and subtle sound design. Kokoro voice-over, bilingual captions, poster and SRT. One command from folder to draft (autofilm.py), one command to film (make_film.py), automatic QA. Use for promo / launch / ad / brand / explainer videos, 宣传片, 产品视频, 广告片.
---

# Product Promo Film · 产品宣传片

> **English first, 中文在后。** Follow the steps literally. Every script prints `FIX:` lines when something is wrong: do what they say, then rerun. Never hand-edit generated files (`film_out/`); edit `film.json`.
>
> 严格按步骤执行。脚本出错时会打印 `FIX:`，照做后重跑即可。不要手改 `film_out/` 里的生成文件，只改 `film.json`。

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
5. **Gates.** Do not build before `check_treatment.py` passes, and do not render before QA has 0 errors.
6. **Restraint.** Calm, professional, premium: effects are felt, not seen, and the film has one hero moment (`references/director.md`).

### Steps (do them in order)
1. **Environment.** Run `python3 scripts/doctor.py` and fix every `MISS`. First time only: in this folder run `npm i playwright && npx playwright install chromium`.
2. **Materials → draft.** The user gives a folder or uploads files: screenshots, photos, product cut-outs (transparent PNG), clips, logo, music (optional), README or brief (optional). Run `python3 scripts/autofilm.py <folder> --out <project>`. It:
   - classifies every file;
   - reads the docs and picks the **genre** (`scripts/genres.py --list`: 15 types, from SaaS to fashion, food and hardware);
   - picks the style, motion, story arc and music (the user's track, or composed);
   - casts each material into a beat;
   - writes `film.json` (with `TODO` copy) and `treatment.md`.
3. **Confirm with the user.** Ask only what matters:
   - the genre and look, if autofilm printed **CLOSE CALL**;
   - their own music, or the composed underscore;
   - voice-over language and voice (`kokoro` voices download once: ask first);
   - contacts for the end card.
4. **Crew.** Read `references/crew.md` and play each role in order, filling `treatment.md`: producer → strategist → creative director (3 concepts, choose 1, hook, hero) → copywriter → art director → motion/editor → composer → brand guardian → design critic. Then run `python3 scripts/check_treatment.py treatment.md` until it passes. A low taste score means redo, not re-score.
5. **Write the film.**
   - Copy the treatment's words into `film.json` and replace every `TODO`.
   - For screen points, measure `rect`s with `python3 scripts/grid_overlay.py` (base coordinates). Photos need none.
   - Scene types and fields are in `references/film-spec.md`.
   - Then run `python3 scripts/check_treatment.py treatment.md film.json`.
6. **Direct.** Do the director's pass (`references/director.md` §5). Defaults already set the colour script, hits, cuts, light and sound. Change a beat only on purpose.
7. **Check.** Run `python3 scripts/make_film.py film.json --stage check` until there is no ERROR. Fix copy warnings from the lint too.
8. **Build + voice + QA.** Run `--stage build`, then `--stage vo`, then `--stage qa`. QA must have 0 errors. If you can view images, read `film_out/qa/sheet*.png` and fix anything ugly in `film.json`.
9. **Render.** Optional quick look: `--stage render --draft`, then `--stage finish --draft`. Final: `--stage render`, then `--stage finish`. Motion blur is applied only to frames that move.
10. **Report** to the user:
    - the file paths and the chosen concept;
    - what is demo, placeholder or composed;
    - what you could not verify (you cannot hear the mix);
    - what they must still supply.

### Quality bar (why the defaults look good: keep them)
- One idea, one hero moment. The hook lands in the first 3 s, and the last 5 s are perfect.
- Cuts fall on bar lines, with one idea per bar.
- On-screen labels ≤ 12 汉字 / 42 chars; captions ≤ 30 汉字.
- No clichés (`scripts/lint_copy.py`).
- Speech sits ~10 dB over the music; sound design sits under it.
- One focal point and one accent colour per frame; margins ≥ 96 px. QA keeps the chapter label and captions clear.
- Max 4 points per feature, 6 comparison rows, 6 lineup items. Two calm scenes beat one crowded scene.

### Going further (optional)
- Manual route (no autofilm): `templates/film.example.json` + `scripts/recommend_style.py` + `scripts/plan_storyboard.py`.
- Composed music on its own: `python3 scripts/make_music.py --list`.
- Tune the cinema layer: `"cinema": {...}` (`references/film-spec.md`).
- Custom JS scenes: `templates/library.js`, `patterns.js`, `engine.js`.
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
5. **关卡**：`check_treatment.py` 不通过不构建，QA 不是 0 错误不渲染。
6. **克制**：平静、专业、高级；效果“感受得到，看不出来”，全片只有一个高潮（`references/director.md`）。

### 步骤（按顺序）
1. **环境**：运行 `python3 scripts/doctor.py`，修好所有 `MISS`。首次需在本目录运行 `npm i playwright && npx playwright install chromium`。
2. **素材 → 草稿**：用户给一个文件夹或上传文件（截图、照片、透明底产品图、录屏、Logo、音乐可选、README 或 brief 可选）。运行 `python3 scripts/autofilm.py <文件夹> --out <项目目录>`，它会：
   - 给每个文件分类；
   - 读文档判断**产品类型**（`scripts/genres.py --list`：15 类，从 SaaS 到时尚、食品、硬件）；
   - 选定风格、动效、叙事结构、音乐（用户的曲子或原创）；
   - 把素材分配到各个拍点；
   - 写出 `film.json`（文案为 `TODO`）和 `treatment.md`。
3. **与用户确认**（只问关键的）：
   - 输出 **CLOSE CALL** 时确认类型与风格；
   - 用他们自己的音乐还是原创配乐；
   - 旁白语言与音色（kokoro 音色需下载一次，先征得同意）；
   - 结尾页联系方式。
4. **团队创作**：读 `references/crew.md`，按顺序扮演各角色填写 `treatment.md`：制片 → 策略 → 创意总监（三个概念、选一个、开场钩子、高潮）→ 文案 → 美术指导 → 动效与剪辑 → 作曲 → 品牌把关 → 设计评审。然后运行 `python3 scripts/check_treatment.py treatment.md` 直到通过。品味分低就重做，不要改分数。
5. **写入影片**：
   - 把方案中的文字写进 `film.json`，替换所有 `TODO`。
   - 界面截图的要点用 `scripts/grid_overlay.py` 量 `rect`（base 坐标），照片不需要。
   - 场景类型与字段见 `references/film-spec.md`。
   - 然后运行 `check_treatment.py treatment.md film.json`。
6. **导演检查**：按 `references/director.md` 第 5 节检查；默认值已设好色彩脚本、击点、转场、光效和声音，只有刻意为之才改。
7. **检查**：`python3 scripts/make_film.py film.json --stage check` 直到没有 ERROR，文案检查的提示也要处理。
8. **构建 + 配音 + QA**：依次运行 `--stage build`、`--stage vo`、`--stage qa`，QA 必须 0 错误；能看图就看 `film_out/qa/sheet*.png`，不满意就改 `film.json`。
9. **渲染**：可选快速预览 `--stage render --draft`，再 `--stage finish --draft`；终版运行 `--stage render`，再 `--stage finish`（运动模糊只用于运动的帧）。
10. **汇报**：
    - 文件路径与选定的创意；
    - 哪些是演示、占位或原创配乐；
    - 哪些没法验证（你听不到混音）；
    - 用户还需补充什么。

### 质量底线（默认值就是这样调出来的，别改坏）
- 一个核心概念、一个高潮；前 3 秒要抓人，最后 5 秒要完美。
- 切点在小节线上，一小节一个意思。
- 画面标签 ≤ 12 汉字 / 42 字符，字幕 ≤ 30 汉字。
- 不用空话（`scripts/lint_copy.py`）。
- 人声比音乐高约 10 dB，音效压在音乐之下。
- 每帧一个视觉焦点、一种强调色，边距 ≥ 96 px；QA 保证章节标签与字幕区不被遮挡。
- 每个功能最多 4 个要点，对比最多 6 行，产品阵列最多 6 个；宁可两个平静的场景，也不要一个拥挤的场景。

### 进阶（可选）
- 手动路线（不用 autofilm）：`templates/film.example.json` + `scripts/recommend_style.py` + `scripts/plan_storyboard.py`。
- 单独生成原创配乐：`python3 scripts/make_music.py --list`。
- 调整电影层：`"cinema": {...}`（见 `references/film-spec.md`）。
- 自写 JS 场景：`templates/library.js`、`patterns.js`、`engine.js`。
- 实战案例：
  - `examples/demo/`：软件，使用用户音乐；
  - `examples/product-demo/`：实物产品，原创配乐，含完整团队方案；
  - `examples/medstat-pilot/`：3:26 正式成片。
- 安装到其他智能体：`references/agents.md`。
