# Troubleshooting · 常见问题

English first, 中文在后。

## English

| Symptom | Cause | Fix |
| --- | --- | --- |
| `ffmpeg not found` | not installed | `python3 -m pip install imageio-ffmpeg` (bundled static ffmpeg) or install ffmpeg |
| `playwright not found` / `Cannot find package 'playwright'` | not installed where scripts run | `npm i playwright && npx playwright install chromium` in the skill folder; or set `PLAYWRIGHT_NODE_MODULES=/path/to/node_modules` |
| Chinese shows as boxes (Linux) | no CJK font | `sudo apt install fonts-noto-cjk` |
| Video clip is black | H.264 source (Chromium build cannot decode it) | run `intake.py` → use the `.webm` it made |
| Kokoro: `Error processing file '…/phontab'` then exit | espeak-ng ignores data paths longer than its buffer; phonemizer resolves symlinks | copy `espeak-ng-data` to a short REAL folder (`~/.cache/kes`) and set `voice.espeak_data` |
| Kokoro: uv error about a project `.venv` | spaCy tried to auto-download its model into the wrong env | install `en_core_web_sm` into the Kokoro venv (audio.md) |
| Hugging Face `CAS Client Error` | Xet transfer blocked | `HF_HUB_DISABLE_XET=1` |
| `OfflineModeIsEnabled … voices/x.pt` | a new voice not downloaded yet | run once without `HF_HUB_OFFLINE` |
| Rendering takes seconds per frame | every worker holds all images in memory → swapping | fewer workers (`tools.workers`), downscale huge images, close other apps |
| `scenes need N bars but the music has M` | film longer than the music | shorten scenes or `music.extend` |
| Speech hard to hear | peak normalisation | keep mix_audio.py defaults (RMS −17 dBFS, duck 0.72) |
| Caption says "three hundred DPI" | spoken text used as caption | add `"cap": "300 DPI"` to that `say` line |
| Highlight box misses the target | rect measured in the wrong space | rects are in `base` units; start from `suggest_rects.py` (autofilm pre-fills them), check on `grid_overlay.py` output |
| Dialog won't close during capture | app ignores Escape | new browser context per scenario, or click its close button |
| Capture hangs on "starting service" / a backend never comes up | another copy of the app (often the user's own, still open) holds its port | ask the user to quit the app; never `pkill`/`killall` it |
| `capture_app.mjs`: "not an Electron app" | a native app cannot be driven | ask the user for screenshots, or film the web build with `--url` |
| A step fails in `capture_app.mjs` | the text differs (spelling, emoji, icon) or the screen was not ready | open `_fail-<scenario>.png`, copy a text from the printed list, add `"exact": false` or a `wait_for` before it, rerun with `--only <scenario>` |
| User pasted a real API key | — | do not enter it anywhere; suggest revoking it; use the local/mock route |
| Final render is slow | motion blur renders 4 samples per frame | use `--draft` while iterating; `"cinema": {"motion_blur": 2}` for a faster final |
| An effect looks flashy / cheap | an effect is noticeable on its own | lower it: `cinema.lens` (e.g. `{"flare": 0, "shake": 0}`), `bloom`, `grain`, `sfx_gain_db: -6`; or `"cinema": "off"` |
| UI colours look wrong after grading | the LUT is too strong for the product's brand colours | `"grade_strength": 0.3` or `"grade": "none"` |
| autofilm picked the wrong genre | the docs say little, or the product spans two genres | add a line about the product to the README/brief, or `autofilm.py --genre <id>` (`genres.py --list`) |
| A photo was treated as a screen (or the reverse) | role guess from pixel statistics | rename the file with a hint (`*_photo.jpg`, `*_screen.png`) and rerun autofilm |
| `copy not written: …TODO` | the crew has not filled that line | write it from treatment.md (references/crew.md) |
| `check_treatment` fails on the taste average | weak concept, copy or images | redo the weakest role's section; do not inflate scores |
| `… without the docs' qualifier "Pro edition"` | a scene makes a claim the docs limit (edition, beta, platform, region, planned) | say the limit in that scene (line, caption or chip) or drop the claim; if it truly does not apply, write it in treatment §8 Qualifiers with "not affected" and why |

## 中文

| 现象 | 原因 | 解决 |
| --- | --- | --- |
| 找不到 ffmpeg | 未安装 | `python3 -m pip install imageio-ffmpeg`（自带静态 ffmpeg），或安装 ffmpeg |
| 找不到 playwright | 脚本运行位置没有安装 | 在 skill 目录 `npm i playwright && npx playwright install chromium`，或设置 `PLAYWRIGHT_NODE_MODULES` |
| 中文显示成方块（Linux） | 没有中文字体 | `sudo apt install fonts-noto-cjk` |
| 录屏是黑的 | 源文件是 H.264，Chromium 无法解码 | 运行 `intake.py`，使用它生成的 `.webm` |
| Kokoro 报 `phontab` 后退出 | espeak-ng 忽略过长的数据路径，phonemizer 会解析软链接 | 把 `espeak-ng-data` 复制到短路径的真实目录（`~/.cache/kes`），并设置 `voice.espeak_data` |
| Kokoro 报项目 `.venv` 的 uv 错误 | spaCy 把模型自动下载到了错误的环境 | 把 `en_core_web_sm` 装进 Kokoro 的 venv（见 audio.md） |
| Hugging Face 报 `CAS Client Error` | Xet 传输被阻断 | `HF_HUB_DISABLE_XET=1` |
| 报 `OfflineModeIsEnabled … voices/x.pt` | 新音色尚未下载 | 去掉 `HF_HUB_OFFLINE` 运行一次 |
| 渲染每帧要好几秒 | 每个 worker 都加载全部图片，内存交换 | 减少 worker（`tools.workers`）、缩小超大图片、关闭其他程序 |
| 报“场景需要 N 小节，音乐只有 M 小节” | 片子比音乐长 | 缩短场景，或用 `music.extend` |
| 人声听不清 | 按峰值归一化 | 保持 mix_audio.py 默认值（RMS −17 dBFS，闪避 0.72） |
| 字幕出现 "three hundred DPI" | 字幕直接用了念出来的文字 | 给该句加 `"cap": "300 DPI"` |
| 高亮框没对准 | 坐标量错了空间 | rect 用 `base` 单位；先用 `suggest_rects.py`（autofilm 已预填），再在 `grid_overlay.py` 的网格图上核对 |
| 采集时弹窗关不掉 | 应用不响应 Escape | 每个场景开新的浏览器上下文，或点关闭按钮 |
| 采集卡在“启动服务中”，后台服务起不来 | 另一个应用实例（通常是用户自己开着的）占用了端口 | 请用户退出应用；不要 `pkill`/`killall` |
| `capture_app.mjs` 提示 “not an Electron app” | 原生应用无法自动操作 | 请用户提供截图，或用 `--url` 拍网页版 |
| `capture_app.mjs` 某一步失败 | 文字不一致（拼写、emoji、图标）或界面还没就绪 | 打开 `_fail-<场景>.png`，从打印的列表里复制文字，加 `"exact": false` 或在前面加 `wait_for`，再用 `--only <场景>` 重拍 |
| 用户在对话里发了真实 API Key | — | 不要填写到任何地方，建议对方吊销，改走本地 / mock 路线 |
| 终版渲染很慢 | 运动模糊每帧渲染 4 次 | 调试时用 `--draft`；或 `"cinema": {"motion_blur": 2}` 加快终版 |
| 某个效果显得花哨 / 廉价 | 效果单独就能被注意到 | 调低：`cinema.lens`（如 `{"flare": 0, "shake": 0}`）、`bloom`、`grain`、`sfx_gain_db: -6`；或 `"cinema": "off"` |
| 调色后界面颜色不对 | LUT 对品牌色太强 | `"grade_strength": 0.3` 或 `"grade": "none"` |
| autofilm 判断的产品类型不对 | 文档信息太少，或产品横跨两类 | 在 README / brief 中补一句产品描述，或用 `autofilm.py --genre <id>`（见 `genres.py --list`） |
| 照片被当成界面（或相反） | 按像素统计猜测角色 | 文件名加提示（`*_photo.jpg`、`*_screen.png`）后重跑 autofilm |
| 报 `copy not written: …TODO` | 团队还没写这一句 | 按 treatment.md 写上（见 references/crew.md） |
| `check_treatment` 品味平均分不够 | 概念、文案或画面偏弱 | 重做最弱角色的部分，不要虚高打分 |
| 报 `… without the docs' qualifier "Pro edition"` | 场景中的说法在文档里有限定（版本、测试版、平台、地区、计划中） | 在该场景的旁白、字幕或标签里说明限定，或删掉这句；确实不适用时，在 treatment 第 8 节“限定条件”中写明“not affected”与原因 |
