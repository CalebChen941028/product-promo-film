# Capturing the real UI · 采集真实界面

English first, 中文在后。Use this when the user has no (or too few) screenshots and the product can run (web app, dev server, desktop app with a web build).

## English

### Setup
- Playwright Chromium, viewport 1920×1080, `deviceScaleFactor: 2` → 3840×2160 PNGs; all rects in films use CSS px (base `[1920, 1080]`).
- Start the app's web/dev mode (README: `npm run dev`, backend + frontend). The analysis/results must be computed for real.
- `scripts/capture_kit.mjs`: `boot()` (seed localStorage, e.g. language or AI settings), `click(text)`, `shot(name)`, `seq(name, ms)` (timestamped frames), `tall(text, name)` (whole scroll container), `download(text, file)` (real exports), `clickables()` (list buttons on an unknown screen).
- **One fresh browser context per scenario** — some dialogs ignore Escape and block later clicks.

### Explore → script → shoot
1. `node capture_kit.mjs explore` → screenshot + list of clickable texts.
2. Locate by visible text (`getByText(text, {exact:true})`); buttons with emoji: `locator("button:has-text('核心词')")`; inputs by placeholder.
3. Write one scenario per film scene: upload demo data → parse → open each tool → run an analysis → open results/plots → export.

### What to capture
| Kind | How | Used by |
| --- | --- | --- |
| full screens | `shot` | `feature`, `cover`, `finale` |
| states of one flow | several `shot`s | custom scenes with `layers` |
| dialogs / panels | full screen, then `modal_bbox.py` | `carousel` crops |
| enlarged results | click "expand/preview" then `shot` | `gallery` |
| long content | `tall` | sidebars, AI answers |
| streaming / animation | `seq` (clip the panel for speed) | custom scenes |
| exported files | `download`; render Word/PDF page 1 with `qlmanage -t -s 1600` (macOS) | `gallery`, custom |

### Filming AI features honestly
- No model available → `scripts/mock_llm.mjs` (OpenAI-compatible, on the Ollama port). Point the app at it as a local provider.
- Write replies **from the real results** of the same demo data; tell the user the AI text was scripted.
- Never type the user's real API key into the app — they do it themselves.

### Demo data
Generate it (fixed seed) with clear, plausible effects and a few % missing values. Built-in test data often has no effects → dull results. Leave out methods that fail or render badly.

## 中文

### 准备
- Playwright Chromium，视口 1920×1080，`deviceScaleFactor: 2`，输出 3840×2160；片子里的坐标一律用 CSS px（base `[1920, 1080]`）。
- 启动产品的 Web / 开发模式（看 README），分析结果必须是真实计算出来的。
- `scripts/capture_kit.mjs` 提供：`boot()`（预写 localStorage，如语言、AI 设置）、`click(文字)`、`shot(名称)`、`seq(名称, 毫秒)`（带时间戳的序列帧）、`tall(文字, 名称)`（整个滚动容器）、`download(文字, 文件)`（真实导出文件）、`clickables()`（列出陌生页面上可点击的按钮）。
- **每个场景用一个新的浏览器上下文**：有的弹窗按 Escape 关不掉，会挡住后续点击。

### 探索 → 写脚本 → 拍摄
1. `node capture_kit.mjs explore`：截图，并列出可点击的文字。
2. 按可见文字定位；按钮带 emoji 时用 `locator("button:has-text('核心词')")`；输入框按 placeholder 定位。
3. 每个场景写一个 scenario：上传演示数据 → 解析 → 打开各工具 → 运行分析 → 打开结果和图 → 导出。

### 采什么
见上方英文表格：全屏截图、同一流程的多个状态、弹窗、放大的结果图、长内容、流式过程、导出文件（macOS 用 `qlmanage -t -s 1600` 渲染 Word / PDF 第一页）。

### 诚实地拍 AI 功能
- 没有可用模型时，用 `scripts/mock_llm.mjs`（OpenAI 兼容接口，监听 Ollama 端口），把应用配置成本地模型。
- 回复内容必须依据同一份演示数据的真实结果撰写，并告诉用户 AI 文本是预先写好的。
- 不要替用户把真实 API Key 填进应用。

### 演示数据
用固定随机种子生成，带明确、可信的效应，并有少量缺失值。内置测试数据往往没有效应，结果平淡。跑不出来或图形难看的方法直接不放。
