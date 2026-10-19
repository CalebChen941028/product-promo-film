# Materials & brief · 素材与需求

English first, 中文在后。

## English

### Ask the user for (checklist)
| Item | Why | If missing |
| --- | --- | --- |
| Product name (+ accent word), one-line positioning (zh/en) | cover, end card | ask; never invent |
| Logo, transparent PNG ≥ 512 px | cover, end card, finale | app icon from the repo (`build/icon.png` …) |
| Music they own or licensed (2–4 min) | rhythm of every cut | ask; do not download music yourself |
| 6–20 screenshots of the real product, ideally 2× (3840×2160) | every feature scene | capture them (`references/capture.md`) |
| Screen recordings (any format) | `clip` scenes | optional; intake converts to WebM |
| Feature list with the screen that proves each | `feature`/`carousel` scenes | derive from README, confirm with the user |
| 2–6 differentiators vs the old way | `compare` scene | ask; keep claims checkable |
| Motto / belief (zh + en) | end card | offer a polished version, get approval |
| Contacts: developer, email, social account, GitHub/site | end card | ask which ones may be public |
| Platforms + status (Beta…) | chips | from README |
| Voice: language, male/female, or their own recording | narration | default: English, `am_michael` |

### Intake
```bash
python3 scripts/intake.py materials --out build --ffmpeg "$FFMPEG"
```
Prints counts, guesses (logo / desktop / phone / figure), the suggested `base` for each image, converts videos to `build/clips/*.webm` and audio to `build/audio/*.wav`, and lists what is missing. Role guesses are heuristics — confirm.

### Brief
`templates/brief.example.json` → `brief.json`. Feature `energy` (low/mid/high) tells the planner where a feature fits the music (privacy/explanations = low; numbers/galleries = high). Feed it to `recommend_style.py` and `plan_storyboard.py`.

### Good screenshots
- Same window size for all (1920×1080 CSS px at 2× is ideal); hide personal data; use demo data with real effects.
- One state per shot (before/after a click = two shots → `layers` in custom scenes, or two scenes).
- Crop-worthy regions: tables, charts, dialogs. Avoid empty states unless that is the point.

## 中文

### 向用户要（清单）
| 项目 | 用途 | 没有时 |
| --- | --- | --- |
| 产品名（+ 强调词）、一句话定位（中英） | 封面、结尾页 | 询问，不要编造 |
| Logo，透明 PNG，至少 512 px | 封面、结尾页、高潮段 | 用仓库里的应用图标（如 `build/icon.png`） |
| 用户拥有或已授权的音乐（2–4 分钟） | 所有切点的节奏 | 询问，不要自行下载音乐 |
| 6–20 张真实产品截图，最好 2 倍（3840×2160） | 所有功能场景 | 自己采集（`references/capture.md`） |
| 录屏（任意格式） | `clip` 场景 | 可选；intake 会转成 WebM |
| 功能清单，以及能证明每个功能的画面 | `feature` / `carousel` 场景 | 从 README 整理，再与用户确认 |
| 2–6 条与传统方式的差异 | `compare` 场景 | 询问；只写可核实的说法 |
| 理念 / 信条（中英） | 结尾页 | 可帮忙润色，需用户确认 |
| 联系方式：开发者、邮箱、公众号 / 社交账号、GitHub / 网站 | 结尾页 | 问清哪些可以公开 |
| 平台 + 版本状态（Beta 等） | 平台标签 | 来自 README |
| 配音：语言、男声 / 女声、或用户自己的录音 | 旁白 | 默认英文 `am_michael` |

### 素材整理
运行上面的 `intake.py` 命令：它会统计数量、猜测角色（Logo / 桌面截图 / 手机截图 / 图表）、给出每张图建议的 `base`，把视频转成 `build/clips/*.webm`、音频转成 `build/audio/*.wav`，并列出缺少的素材。角色是推测出来的，请确认。

### Brief
复制 `templates/brief.example.json` 为 `brief.json`。功能的 `energy`（low / mid / high）告诉规划器这个功能适合放在音乐的哪一段（隐私、说明类为 low；数字、图集为 high）。brief 会被 `recommend_style.py` 和 `plan_storyboard.py` 使用。

### 好截图的标准
- 所有截图窗口大小一致（1920×1080 CSS px、2 倍最理想）；隐藏个人数据；用带真实效应的演示数据。
- 一张图一个状态（点击前后是两张图）。
- 值得放大的区域：表格、图表、对话框；除非要表达“空状态”，否则避免空白页面。
