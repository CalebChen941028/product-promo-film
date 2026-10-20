# film.json reference · film.json 字段说明

English first, 中文在后。Paths are relative to `film.json`. 1 bar = 4 beats (120 BPM → 2 s).

## English

### Top level
| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `name` | string | yes | output file prefix |
| `out` | string | no | working folder (default `film_out`) |
| `materials` | path | no | the materials folder (autofilm writes it); `check_treatment.py` reads the docs there to check that proof lines carry facts |
| `treatment` | path / `"skip"` | no | the crew's treatment (default `treatment.md`); the build refuses to start until it passes `check_treatment.py`. `"skip"` only for a throwaway test cut |
| `genre` | string | no | product type from `templates/genres.json` (`python3 scripts/genres.py --list`); sets the defaults for style, motion and composed music |
| `style` | string | yes | look: `midnight-tech` `keynote-light` `editorial-mono` `aurora-glass` `neon-cyber` `paper-academic` `luxe-noir` `natural-fresh`, or `auto` (from the genre) |
| `motion` | string | no | motion language: `cinematic-3d` `precision-data` `kinetic-launch` `gentle-story` `playful-pop` `editorial-type`; empty = the style's default |
| `music.file` | path | no | the user's track (mp3/wav/m4a…). Without it, an original underscore is composed bar-for-bar from the scenes |
| `music.generate` | object | no | `{"mood": "auto"\|"cinematic-pulse"\|"minimal-electronic"\|"warm-piano"\|"bright-pop"\|"luxe-lounge"\|"ambient-air"\|"warm-acoustic", "bpm": 98, "seed": 3}`. The end card (`"rest"`) is then about 8 s (3–4 bars) plus a ring-out bar |
| `music.extend` | object | no | `{"from_bar": A, "to_bar": B, "times": 1}` repeats bars A–B once (a chorus) to lengthen the film |
| `voice.engine` | `kokoro` / `files` / `none` | no | TTS, the user's recordings (`"files": {"<say id>": "rec.wav"}`), or captions only |
| `voice.voice` / `lang` / `python` / `espeak_data` | — | for kokoro | e.g. `am_michael`, `a`, path to a Python with kokoro (default `$KOKORO_PYTHON` or `~/.venvs/kokoro`), short copy of espeak-ng-data |
| `voice.allow_download` | bool | no | default false: the vo stage runs offline and stops if the model or voice is not downloaded. Set true only after the user agreed to the download |
| `brand` | object | yes | see below |
| `scenes` | list | yes | in playing order; first `cover`, last `endcard` with `"bars": "rest"` |
| `tools.ffmpeg` / `tools.node_modules` / `tools.workers` | — | no | override tool discovery / render workers |
| `cover_t` | number | no | second used for the cover poster (default 4.2) |
| `cinema` | `"auto"` / `"off"` / object | no | the director's cinema layer (default `"auto"` = on, all defaults from the style + motion). See below |

### cinema (director's layer, `references/director.md`)
| Key | Default | Meaning |
| --- | --- | --- |
| `grade` | style's look | LUT: `teal-night` `clean-bright` `bleach-print` `pastel-glow` `neon-night` `warm-print` `teal-orange` `none` |
| `grade_strength` | 0.5 | 0–1 blend of the look; keep ≤ 0.7 so UI colours stay true |
| `bloom` | style's value | 0–0.6 glow around bright areas |
| `grain` | style's value | 0–1 film grain (luma, moving) |
| `motion_blur` | 4 | samples per frame over a 180° shutter (1 = off). `--draft` forces 1 |
| `sfx` | `auto` | synthesised sound design from the scenes; `off` = music + voice only |
| `sfx_gain_db` | −2 | level of the sound design bus (−6 = quieter, 0 = louder) |
| `lens` | by motion (restrained) | override `{shake, hz, dof, pull, glint, flare, kick, leak, bokeh}`; 0 = off. `leak` and `bokeh` are 0 by default — add them only for soft or playful briefs |

### brand
`name`, `nameAccent` (second word in the accent colour), `logo` (transparent PNG), `positioningZh`, `positioningEn`, `taglineZh`, `taglineEn`, `motto` = [zh line 1, zh line 2 (accent), English line], `contacts` = list of [LABEL_EN, 中文标签, value, sub-line] (≤ 3 reads best), `chips` = platforms/status (last chip highlighted if it says Beta/Preview/内测).

### Every scene
| Field | Meaning |
| --- | --- |
| `type` | one of the types below |
| `bars` | length in bars (number ≥ the type's minimum) or `"rest"` (only the last scene) |
| `chapter` | optional `["01", "数据", "DATA"]` → top-left chapter label while the scene plays |
| `say` | optional narration lines `[{en, zh, cap?, at?, id?}]`. `en` is spoken, `zh` is the Chinese caption, `cap` replaces the English caption (digits: "300 DPI"), `at` = start in bars from the scene start (default spread evenly from 0.3), `id` = `tagline`/`motto` to hide the caption because the text is already on screen |
| `mood` | optional colour-script mood: `cold` `neutral` `peak` `warm` `night` (default by type: pain cold, numbers/finale peak, endcard warm) |
| `cut` | optional cut INTO this scene: `style` (the style's transition), `whip` (pan + motion blur), `push` (camera flies through). Default by motion language |
| `energy` | optional 0–3: the music section under this scene when the music is composed (default by type) |
| `hit` | optional `true`/`false`/`"hero"`. A hit is a small camera kick plus a soft sound on the scene's first beat (default: the scene after `pain`, `numbers`). The one `"hero"` beat (default `finale`) also gets the flare, the impact and a riser |

### Scene types
| type | min bars | fields | notes |
| --- | --- | --- | --- |
| `cover` | 3 | `media?` (blurred UI behind), `base?` | logo, name, positioning, chips; also the poster |
| `pain` | 3 | `items?` = 4 × [zh, en] | "the old way": grey tool windows tangle and collapse |
| `feature` | 3 (≥ 1 + points) | `media`, `base?`, `title{zh,en}`, `points[{zh,en,rect?,focus?}]` ≤ 4, `frame?: "photo"` | the workhorse; layout depends on the motion language. `rect` highlights a screen region; photos (`"frame": "photo"`) need none |
| `carousel` | 2 | `title?`, `panels[{zh,en,media,base?,crop?}]` ≤ 6 | dialogs/tools flip in one per slice beside a menu |
| `numbers` | 2 | `stats[{value,suffix?,zh,en}]` ≤ 3, `chips?` ≤ 12 | counters on the beat |
| `gallery` | 2 | `items[{media,zh?,en?}]` ≤ 8 | coverflow of result images; say one name per item (`at`) |
| `clip` | 2 | `media` (.webm), `base?`, `title?`, `offset?`, `rate?` | screen recording, seeked frame-exactly |
| `phone` | 2 | `media`, `base` (points, e.g. [393,852]), `title{zh,en}` | mobile screenshot in a device frame |
| `compare` | 3 | `rows[[oldZh,oldEn,newZh,newEn]]` ≤ 6, `header?` | traditional vs this product |
| `statement` | 1 | `zh`, `en?` | one big line (manifesto beat) |
| `finale` | 4 | `media` = list of images | tilted wall of real screens + name + tagline |
| `endcard` | 4 | — | logo, name, positioning, motto, contacts, chips |
| `photo` | 2 | `media`, `base?`, `title?{zh,en}`, `focus?` (end crop), `side?: "left"\|"bottom"` | full-bleed photograph with a slow push-in; text on a soft scrim |
| `hero` | 3 | `media` (one image or several angles), `base?`, `title{zh,en}`, `cutout?` | the reveal: the product lights up and breathes. Transparent PNGs stand on the stage with a contact shadow and reflection (auto-detected); a single photograph fills the frame and lights up as the camera eases in |
| `detail` | 2 | `media`, `base?`, `crops?[{rect,zh?,en?}]` ≤ 4 | macro close-ups (texture before the whole); default crops are chosen for you |
| `lineup` | 2 | `items[{media,zh?,en?}]` ≤ 6, `title?`, `cutout?` | the range (colours, models, sizes) standing together |
| `quote` | 2 | `zh`, `en?`, `who`, `role?` | a **real**, approved testimonial; large and quiet |

### Coordinates
`base` is the coordinate space of an image: for a 2× capture of a 1920×1080 window use `[1920, 1080]` (default); `intake.py` prints a suggested `base` for every image. `rect`/`crop`/`focus` = `[x, y, w, h]` in base units. `scripts/suggest_rects.py <image> --preview .` suggests numbered rects (cards, panels, charts, tables) in base units for any image size; autofilm pre-fills feature points with them. Measure by hand with `scripts/grid_overlay.py` (grid labels are base units for 1920×1080 captures) or `scripts/modal_bbox.py` for dialogs.

## 中文

### 顶层字段
| 字段 | 类型 | 必填 | 含义 |
| --- | --- | --- | --- |
| `name` | 字符串 | 是 | 输出文件名前缀 |
| `out` | 字符串 | 否 | 工作目录（默认 `film_out`） |
| `materials` | 路径 | 否 | 素材文件夹（autofilm 自动写入）；`check_treatment.py` 读取其中文档，核对证据句是否带有事实 |
| `treatment` | 路径 / `"skip"` | 否 | 团队创意方案（默认 `treatment.md`）；未通过 `check_treatment.py` 时拒绝构建。`"skip"` 仅用于一次性测试片 |
| `genre` | 字符串 | 否 | 产品类型（`templates/genres.json`，`python3 scripts/genres.py --list`），决定风格、动效、原创配乐的默认值 |
| `style` | 字符串 | 是 | 视觉风格：`midnight-tech` `keynote-light` `editorial-mono` `aurora-glass` `neon-cyber` `paper-academic` `luxe-noir` `natural-fresh`，或 `auto`（按类型） |
| `motion` | 字符串 | 否 | 动效语言：`cinematic-3d` `precision-data` `kinetic-launch` `gentle-story` `playful-pop` `editorial-type`；留空则用风格默认值 |
| `music.file` | 路径 | 否 | 用户提供的音乐；不提供时按场景逐小节原创一段配乐 |
| `music.generate` | 对象 | 否 | `{"mood": "auto" 或 情绪名, "bpm": 98, "seed": 3}`；此时结尾页（`"rest"`）约 8 秒（3–4 小节），另加一小节余音 |
| `music.extend` | 对象 | 否 | `{"from_bar": A, "to_bar": B, "times": 1}`：把第 A–B 小节（通常是副歌）重复一遍来加长 |
| `voice.engine` | `kokoro` / `files` / `none` | 否 | 合成配音、用户录音（`"files": {"<say id>": "rec.wav"}`）、或只要字幕 |
| `voice.voice` / `lang` / `python` / `espeak_data` | — | 用 kokoro 时 | 如 `am_michael`、`a`、装了 kokoro 的 Python 路径（默认 `$KOKORO_PYTHON` 或 `~/.venvs/kokoro`）、espeak-ng 数据的短路径副本 |
| `voice.allow_download` | 布尔 | 否 | 默认 false：配音阶段离线运行，模型或音色未下载时停止。只有用户同意下载后才设为 true |
| `brand` | 对象 | 是 | 见下 |
| `scenes` | 列表 | 是 | 按播放顺序；第一个是 `cover`，最后一个是 `"bars": "rest"` 的 `endcard` |
| `tools.*` | — | 否 | 手动指定 ffmpeg、node_modules、渲染进程数 |
| `cover_t` | 数字 | 否 | 封面海报取第几秒（默认 4.2） |
| `cinema` | `"auto"` / `"off"` / 对象 | 否 | 导演电影层（默认 `"auto"` 开启，参数取自风格与动效语言），见下 |

### cinema（导演电影层，见 `references/director.md`）
| 键 | 默认 | 含义 |
| --- | --- | --- |
| `grade` | 风格自带 | 调色 LUT：`teal-night` `clean-bright` `bleach-print` `pastel-glow` `neon-night` `warm-print` `teal-orange` `none` |
| `grade_strength` | 0.5 | 调色强度 0–1；不超过 0.7 以保证界面色彩真实 |
| `bloom` | 风格自带 | 0–0.6，亮部辉光 |
| `grain` | 风格自带 | 0–1，胶片颗粒（亮度、动态） |
| `motion_blur` | 4 | 每帧采样次数（180° 快门），1 为关闭；`--draft` 强制为 1 |
| `sfx` | `auto` | 按场景自动合成声音设计；`off` 只保留音乐和人声 |
| `sfx_gain_db` | −2 | 音效总线电平（−6 更轻，0 更响） |
| `lens` | 随动效语言（克制） | 覆盖 `{shake, hz, dof, pull, glint, flare, kick, leak, bokeh}`，0 为关闭；`leak`、`bokeh` 默认 0，只在柔和或活泼的项目中再打开 |

### brand（品牌）
`name`、`nameAccent`（强调色显示的第二个词）、`logo`（透明 PNG）、`positioningZh` / `positioningEn`（定位）、`taglineZh` / `taglineEn`（口号）、`motto` = [中文第一行, 中文第二行（强调色）, 英文一句]、`contacts` = [英文标签, 中文标签, 值, 副行] 的列表（3 组最好看）、`chips` = 平台 / 版本状态（最后一个若是 Beta / 内测 会高亮）。

### 每个场景都有
| 字段 | 含义 |
| --- | --- |
| `type` | 场景类型（见下表） |
| `bars` | 小节数（不少于该类型最小值），或 `"rest"`（只能用在最后一个场景） |
| `chapter` | 可选，`["01", "数据", "DATA"]`，场景播放时左上角显示章节 |
| `say` | 可选旁白 `[{en, zh, cap?, at?, id?}]`：`en` 是念出来的英文，`zh` 是中文字幕，`cap` 替换英文字幕（用于显示数字），`at` 为相对场景起点的小节数（默认从 0.3 起均匀分布），`id` 写 `tagline` / `motto` 时隐藏字幕（画面上已有同一句） |
| `mood` | 可选，色彩脚本情绪：`cold` `neutral` `peak` `warm` `night`（默认：痛点 cold，数字和高潮 peak，结尾 warm） |
| `cut` | 可选，进入本场景的转场：`style`（风格自带）、`whip`（甩镜 + 运动模糊）、`push`（镜头推进穿越）；默认随动效语言 |
| `energy` | 可选 0–3：原创配乐时本场景下的音乐强度（默认按类型） |
| `hit` | 可选 `true`/`false`/`"hero"`：击点是场景第一拍的轻微镜头冲击加轻声音效（默认：痛点之后的场景、`numbers`）；唯一的 `"hero"` 高潮（默认 `finale`）另有镜头光晕、重击和上升音 |

### 场景类型
| 类型 | 最少小节 | 字段 | 说明 |
| --- | --- | --- | --- |
| `cover` | 3 | `media?`（背景虚化界面）、`base?` | Logo、名称、定位、平台标签；同时是封面海报 |
| `pain` | 3 | `items?` = 4 组 [中文, 英文] | “传统方式”：灰色工具窗口互相牵扯后塌缩 |
| `feature` | 3（≥ 1 + 要点数） | `media`、`base?`、`title{zh,en}`、`points[{zh,en,rect?,focus?}]` ≤ 4、`frame?: "photo"` | 主力场景；版式随动效语言变化；`rect` 用于高亮界面区域，照片（`"frame": "photo"`）不需要 |
| `carousel` | 2 | `title?`、`panels[{zh,en,media,base?,crop?}]` ≤ 6 | 工具 / 对话框逐个翻入，左侧菜单同步高亮 |
| `numbers` | 2 | `stats[{value,suffix?,zh,en}]` ≤ 3、`chips?` ≤ 12 | 按拍计数的大数字 |
| `gallery` | 2 | `items[{media,zh?,en?}]` ≤ 8 | 结果图 coverflow，旁白逐张点名（用 `at`） |
| `clip` | 2 | `media`（.webm）、`base?`、`title?`、`offset?`、`rate?` | 录屏，逐帧精确定位 |
| `phone` | 2 | `media`、`base`（点尺寸，如 [393,852]）、`title{zh,en}` | 手机截图套设备外框 |
| `compare` | 3 | `rows[[旧中文,旧英文,新中文,新英文]]` ≤ 6、`header?` | 传统方式 vs 本产品 |
| `statement` | 1 | `zh`、`en?` | 一句大字（宣言） |
| `finale` | 4 | `media` = 图片列表 | 真实界面倾斜成墙 + 名称 + 口号 |
| `endcard` | 4 | — | Logo、名称、定位、理念、联系方式、平台标签 |
| `photo` | 2 | `media`、`base?`、`title?{zh,en}`、`focus?`（终止裁切）、`side?` | 满幅照片缓慢推近，文字放在柔和的渐变遮罩上 |
| `hero` | 3 | `media`（一张或多个角度）、`base?`、`title{zh,en}`、`cutout?` | 揭晓：产品亮起并轻微呼吸；透明底 PNG 会自动带接触阴影与倒影立在舞台上；单张照片则满幅铺开，随镜头缓推逐渐亮起 |
| `detail` | 2 | `media`、`base?`、`crops?[{rect,zh?,en?}]` ≤ 4 | 微距特写（先质感，后全貌），默认自动选取裁切 |
| `lineup` | 2 | `items[{media,zh?,en?}]` ≤ 6、`title?`、`cutout?` | 产品系列（颜色、型号、尺寸）并排展示 |
| `quote` | 2 | `zh`、`en?`、`who`、`role?` | **真实**且经授权的用户评价，大字、安静 |

### 坐标
`base` 是图片的坐标空间：1920×1080 窗口的 2 倍截图用 `[1920, 1080]`（默认）；`intake.py` 会为每张图给出建议的 `base`。`rect` / `crop` / `focus` 都是 base 单位下的 `[x, y, 宽, 高]`。`scripts/suggest_rects.py <图片> --preview .` 会自动给出编号的建议框（卡片、面板、图表、表格），适用于任意尺寸，单位为 base；autofilm 会用它预填功能要点。也可用 `scripts/grid_overlay.py` 手动量取（网格刻度即 1920×1080 截图的 base 单位），弹窗可用 `scripts/modal_bbox.py` 自动求框。
