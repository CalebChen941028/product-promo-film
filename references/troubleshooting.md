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
| Highlight box misses the target | rect measured in the wrong space | rects are in `base` units; measure on `grid_overlay.py` output |
| Dialog won't close during capture | app ignores Escape | new browser context per scenario, or click its close button |
| User pasted a real API key | — | do not enter it anywhere; suggest revoking it; use the local/mock route |

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
| 高亮框没对准 | 坐标量错了空间 | rect 用 `base` 单位，在 `grid_overlay.py` 的网格图上量 |
| 采集时弹窗关不掉 | 应用不响应 Escape | 每个场景开新的浏览器上下文，或点关闭按钮 |
| 用户在对话里发了真实 API Key | — | 不要填写到任何地方，建议对方吊销，改走本地 / mock 路线 |
