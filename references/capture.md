# Capturing the real UI · 采集真实界面

English first, 中文在后。Use this when the user points at a product instead of giving screenshots ("make a film for the app on my computer", a URL, a dev server), or gives fewer than ~10 screens of a software product.

## English

### Which route
| The user gives | Route |
| --- | --- |
| an installed desktop app (`/Applications/X.app`, `C:\Program Files\X\X.exe`) | `capture_app.mjs --app <path>`. Works for Electron apps (most modern desktop apps); it says so if the app is not one |
| a web app or a running dev server | `capture_app.mjs --url <url>` |
| a native (non-Electron) app, or capture fails | ask the user for screenshots (one window per screen, 1920×1080 or larger). Do not improvise |
| the source code (with or without an installed build) | stills from the installed build or URL as above; for motion, ask once whether you may run its frontend in a sandbox, then `record_ui.mjs` (below). Do not build or run their repo unless they say yes |

### Do not
- **Never kill a process you did not start.** No `pkill`, `killall` or `kill` by app name: that stops the user's own running copy of the app and its backend. `capture_app.mjs` cleans up only what it started.
- Never run the product's source code, dev servers or backends without the user's yes; with it, only through `record_ui.mjs` (its own port, an empty profile, localhost only, demo data).
- Never open settings, licence, account, payment or delete screens unless the user asked, and never type the user's API keys or passwords.
- Never fake a screen. If a feature cannot be reached, leave it out of the film.

### Explore → shot list → shoot (about 15 minutes)
1. **Demo data first** (for data products): write a small script with a fixed seed that makes data with clear, plausible effects and a few % missing values (`examples/medstat-pilot/make_demo_data.py` is a model). Built-in samples often show no effect, and that makes the results dull.
2. **Explore** one screen at a time:
   `node scripts/capture_app.mjs explore --app "/Applications/X.app" --out explore`
   It saves `explore/explore.png` (look at it) and prints the headings, every clickable text and every input. To go deeper, pass the steps that reach the next screen:
   `--steps '[{"upload":"data/demo.csv"},{"click":"Import"},{"wait_for":"Variables","timeout":120000}]'`
   Repeat until you know the path through the core job: open → bring in data → do the work → see the result → take it away (export).
3. **Shot list:** if `examples/` has one for this product (`examples/medstat-pilot/shots.json`, verified on MedStat Pilot), start from it. Otherwise copy `templates/shots.example.json` to the project and fill it with the exact texts you saw. Plan 12–25 shots in film order:
   - the first screen, and the user's data arriving;
   - each step of the core job (one idea per shot);
   - every real output: result, plot (enlarged), table, report or export;
   - the AI feature if there is one (see below);
   - breadth: one scenario per feature family the product is known for (for an analysis tool: 3–5 different analyses, each run to its result and its enlarged plot).
4. **Shoot:** `node scripts/capture_app.mjs shoot shots.json`. Every shot is 3840×2160 (a 1920×1080 window at 2×). A failed step saves `_fail-<scenario>.png`, lists what can be clicked there, and prints a FIX; fix the step and rerun with `--only <scenario>`.
5. **Look** at every PNG. Re-shoot anything with a spinner, an error, an empty panel or a dialog over the subject. **Keep dense screens** (a full results page, a workspace with many panels): the film shows a screen whole for under a second, then zooms into readable regions, so density is not a reason to drop a shot. The run ends with a coverage line; under 12 shots or under 3 outputs, add scenarios before you go on.
6. The `out` folder is the materials folder. From an installed macOS app it also gets `app-info.md` (the product's name and version) and `logo.png` (the app icon). Put the user's docs or brief in it too (or text from their website or README), then run `autofilm.py` on it.

The app runs with a **copy** of the user's saved settings (`"profile": "copy"`), so first-run wizards are skipped and the real profile is never changed. Every scenario starts from a fresh launch; `"reuse": true` keeps one launch and reloads the window instead (faster for apps with a slow engine, but only if the app comes back clean after a reload). If the app hangs on a "starting service" screen, another copy of it (often the user's own, still open) holds its port. Ask the user to quit the app; do not kill it.

### Recording the real UI in motion from the source (`record_ui.mjs`)
Stills cut together are stiff; a real interaction recorded from the product's own frontend is smooth and true. With the user's yes for this product:
1. Read the repo: how the frontend starts (`package.json` scripts, `vite.config`, the dev port), which calls go to a backend, which demo data exists.
2. Write a recipe (`templates/record.example.json`): `"serve"` (the dev command on a free port), `"url"` (a server the user runs for this) or `"static"` (a built `dist`); `"mock"` demo responses for every backend call the takes need; `"takes"` with the steps of each interaction, in the order the user would do them, with `"hold"` where the eye needs to read.
3. Run `node scripts/record_ui.mjs recipe.json --approved-by-user`. Each take starts from an empty browser profile, the network is limited to localhost (`"network": "open"` only if the user said the product may reach its real services), a soft cursor glides to every target and ripples on each click, and the screen is recorded at 30 fps (`"scale": 2` = 4K, sharp when a scene zooms in). It stops only the server it started.
4. Put the `.webm` takes in the materials folder: intake files them as screen recordings; use them in `clip` scenes or as footage; the poster `.png` of each take also works as a still.
The data on screen is demo data: say so in the film as for any demo. Where a flow cannot run in a sandbox (a native engine, licensed data, hardware), and the user agreed, redraw it in code instead (`references/custom-scenes.md`, "Redrawn UI"): it is labelled 界面示意 · Illustrative UI on screen.

### Steps in a shot list
`click` (visible text; `"exact": false` for part of a text), `css`, `click_xy`, `upload`, `open_dialog` (the app's native Open dialog returns a file), `fill`, `type`, `select`, `key`, `hover`, `wait_for`, `sleep`, `scroll`, `wheel`, `shot` (optional `clip`), `tall` (a whole scrolling panel as one image), `download` (a real export; Word and PDF also get a page-1 preview PNG on macOS), `seq` (timestamped frames of a moving moment). The full list is at the top of `scripts/capture_app.mjs`. A `download` step saves a file the product exports on this computer; it is not a download from the internet, so "download nothing" (about models and voices) does not rule it out. Every `shot` is checked for visible error or empty-state messages: a flagged shot is reshot or dropped, never filmed.

### Filming AI features honestly
- The user says the app's AI is already configured: film it with **their** setup. Add `"profile_extra": ["secrets"]` to the shot list: it copies the app's own encrypted key store into the temporary profile, so the app reads its configuration itself; you never see, type or print the key, and the copy is deleted after the run. Do this only when the user asked for the AI features to be filmed. If the AI panel still fails, ask the user (do not guess at settings).
- No model is set up (the AI panel shows an error or asks for a provider): do not drop the AI chapter. Add `"mock_llm": {"port": 11434, "replies": "replies.json"}` and point the app at it as a local provider (Ollama base URL `http://localhost:11434/v1`) with `storage`: `explore` prints the app's localStorage keys and the shape of its AI settings (secrets masked), so copy that shape with the local URL and an empty key. `examples/medstat-pilot/replies.json` shows the replies format. The user can set it up instead.
- Write the replies **from the real results** of the same demo data, and tell the user that the AI text was scripted.
- Never type the user's API key into the app, even when they paste it in chat; they set it up themselves.

### Older route
`scripts/capture_kit.mjs` is the same idea as a Playwright script you edit by hand (web apps only). `examples/medstat-pilot/shoot.mjs` is the full capture behind the 3:26 reference film.

## 中文

### 选哪条路
| 用户给的是 | 做法 |
| --- | --- |
| 已安装的桌面应用（`/Applications/X.app`、`C:\Program Files\X\X.exe`） | `capture_app.mjs --app <路径>`，适用于 Electron 应用（多数现代桌面应用）；不是 Electron 时脚本会直接说明 |
| 网页应用或正在运行的开发服务器 | `capture_app.mjs --url <地址>` |
| 原生（非 Electron）应用，或采集失败 | 请用户提供截图（每屏一个窗口，1920×1080 或更大），不要自行变通 |
| 有源代码（不论是否有安装版） | 截图仍按上面的方法从安装版或网址采集；要做动态演示时，先问一次能否在沙盒里运行它的前端，再用 `record_ui.mjs`（见下文）。用户同意前不要构建或运行他们的仓库 |

### 不要做
- **不要结束不是你启动的进程**：不用 `pkill`、`killall`，也不按应用名 `kill`，否则会关掉用户自己正在用的应用和它的后台服务。`capture_app.mjs` 只清理它自己启动的进程。
- 未经用户同意，不要运行产品源码、开发服务器或后端；同意后也只通过 `record_ui.mjs` 运行（独立端口、空白配置、只访问本机、演示数据）。
- 除非用户要求，不进设置、授权、账户、支付、删除等界面；不替用户填写 API Key 或密码。
- 不伪造界面；到不了的功能就不放进片子。

### 探索 → 镜头清单 → 拍摄（约 15 分钟）
1. **先做演示数据**（数据类产品）：写一个固定随机种子的小脚本，生成效应明确、可信、带少量缺失值的数据（参考 `examples/medstat-pilot/make_demo_data.py`）。内置样例数据往往没有效应，结果很平淡。
2. **逐屏探索**：
   `node scripts/capture_app.mjs explore --app "/Applications/X.app" --out explore`
   它会保存 `explore/explore.png`（要看），并打印标题、所有可点击文字和输入框。要往深处走，就把到达下一屏的步骤传进去：
   `--steps '[{"upload":"data/demo.csv"},{"click":"导入"},{"wait_for":"变量","timeout":120000}]'`
   反复探索，直到摸清核心任务的路径：打开 → 导入数据 → 做事 → 看结果 → 带走（导出）。
3. **镜头清单**：若 `examples/` 里已有这个产品的清单（`examples/medstat-pilot/shots.json`，已在 MedStat Pilot 上验证），就从它开始；否则把 `templates/shots.example.json` 复制到项目里，用看到的原文填写，按影片顺序规划 12–25 个镜头：
   - 首屏，以及用户数据进来的那一刻；
   - 核心任务的每一步（一个镜头一个意思）；
   - 每个真实产出：结果、放大的图、表、报告或导出；
   - 若有 AI 功能，也要拍（见下）；
   - 广度：产品主打的每类功能各拍一个场景（分析软件就跑 3–5 种不同的分析，每种都拍到结果和放大的图）。
4. **拍摄**：`node scripts/capture_app.mjs shoot shots.json`，每张 3840×2160（1920×1080 窗口的 2 倍）。某步失败时会保存 `_fail-<场景>.png`、列出当时能点的文字并给出 FIX；改好后用 `--only <场景>` 重拍。
5. **逐张查看**：有加载圈、报错、空面板，或弹窗挡住主体的，都要重拍。**密集的界面要保留**（完整的结果页、多面板的工作区）：片子只让整屏停留不到一秒，随后推近到可读区域，所以“太密”不是删镜头的理由。拍摄结束时会打印覆盖情况；镜头少于 12 个或产出少于 3 个时，先补拍再继续。
6. `out` 文件夹就是素材文件夹。拍 macOS 已安装应用时，它还会自动写入 `app-info.md`（产品名称与版本）和 `logo.png`（应用图标）。把用户的文档或简介也放进去（或来自官网、README 的文字），再对它运行 `autofilm.py`。

应用会使用用户已保存设置的**副本**（`"profile": "copy"`），所以会跳过首次设置向导，也不会改动真实配置。每个场景都重新启动应用；`"reuse": true` 则只启动一次、场景之间刷新窗口（引擎启动慢的应用更快，但前提是刷新后界面能回到干净状态）。若应用卡在“启动服务中”，说明另一个实例（通常是用户自己开着的那个）占用了端口：请用户退出应用，不要强行结束它。

### 用源码录制真实界面的动态演示（`record_ui.mjs`）
截图拼接显得生硬；从产品自己的前端录下的真实操作既流畅又真实。用户同意后：
1. 读仓库：前端怎么启动（`package.json` 脚本、`vite.config`、开发端口），哪些请求发给后端，有哪些演示数据。
2. 写录制脚本（`templates/record.example.json`）：`"serve"`（在空闲端口运行开发命令）、`"url"`（用户为此开着的服务）或 `"static"`（构建好的 `dist`）；为录制需要的每个后端请求写 `"mock"` 演示响应；`"takes"` 按用户的操作顺序写每段步骤，需要让观众看清的地方加 `"hold"`。
3. 运行 `node scripts/record_ui.mjs recipe.json --approved-by-user`。每段录制都从空白浏览器配置开始，网络只允许本机（用户明确同意产品可访问真实服务时才用 `"network": "open"`），平滑光标移向每个目标、点击时有涟漪，按 30 帧录制（`"scale": 2` 为 4K，推近时依然清晰）。它只停止自己启动的服务。
4. 把 `.webm` 放进素材文件夹：intake 会识别为界面录屏，可用在 `clip` 场景或当作视频素材；每段的封面 `.png` 也可作截图使用。
画面里是演示数据，片中要像其他演示一样注明。沙盒里跑不起来的流程（原生引擎、授权数据、硬件），在用户同意后可改用代码重绘（见 `references/custom-scenes.md` 的“重绘界面”），画面上会标注“界面示意 · Illustrative UI”。

### 镜头清单里的步骤
`click`（可见文字；`"exact": false` 表示匹配部分文字）、`css`、`click_xy`、`upload`、`open_dialog`（让应用的原生“打开”对话框返回指定文件）、`fill`、`type`、`select`、`key`、`hover`、`wait_for`、`sleep`、`scroll`、`wheel`、`shot`（可加 `clip`）、`tall`（把整个滚动面板拍成一张长图）、`download`（真实导出；在 macOS 上 Word、PDF 还会生成第一页的预览 PNG）、`seq`（带时间戳的连续帧）。完整说明见 `scripts/capture_app.mjs` 文件开头。`download` 是把产品导出的文件存到本机，不是从网上下载，所以“不要下载任何东西”（指模型、音色）并不禁止它。每个 `shot` 都会检查画面里有没有报错或空状态提示：被标出的镜头要重拍或删掉，绝不放进片子。

### 诚实地拍 AI 功能
- 用户说应用的 AI 已经配置好：用**他们自己的**配置来拍。在镜头清单里加 `"profile_extra": ["secrets"]`：它把应用自己加密保存的密钥库复制到临时配置里，由应用自行读取；你看不到、不输入、不打印密钥，运行结束后副本会删除。只有用户要求拍 AI 功能时才这样做。若 AI 面板仍然报错，就问用户，不要猜测设置。
- 用户没配置模型（AI 面板报错或要求选择服务）时，不要删掉 AI 章节：加上 `"mock_llm": {"port": 11434, "replies": "replies.json"}`，并用 `storage` 把应用指向这个本地模型（Ollama 地址 `http://localhost:11434/v1`）。`explore` 会打印应用的 localStorage 键名和 AI 设置的结构（密钥已遮盖），照这个结构填入本地地址、密钥留空即可；回复格式见 `examples/medstat-pilot/replies.json`。也可以请用户自己配置。
- 回复内容必须依据同一份演示数据的**真实结果**撰写，并告诉用户 AI 文本是预先写好的。
- 即使用户在对话里贴出 API Key，也不要替他填进应用，由用户自己配置。

### 旧方法
`scripts/capture_kit.mjs` 思路相同，但需要手改 Playwright 脚本，只适用于网页应用。`examples/medstat-pilot/shoot.mjs` 是 3:26 参考片背后的完整采集脚本。
