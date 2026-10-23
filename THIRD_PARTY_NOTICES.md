# Third-party notices · 第三方声明

English first, 中文在后。Reelwright's own code is MIT-licensed ([LICENSE](LICENSE)). This page says what else it uses or mentions, and what is and is not covered by that licence. Licences are as the upstream projects publish them at the time of writing: check upstream before you redistribute or publish.

## English

### Software you install yourself (nothing here is bundled or redistributed by this repository)
| Component | Used for | Licence (upstream) |
| --- | --- | --- |
| [Playwright](https://playwright.dev) (`npm install`) | capture, render, QA | Apache-2.0; it downloads Chromium builds, each under its own licences |
| [Node.js](https://nodejs.org) | runs the capture / render scripts | MIT (with bundled third-party licences) |
| [NumPy](https://numpy.org), [Pillow](https://python-pillow.org) | image analysis, colour, snapping | BSD-3-Clause; HPND |
| [ffmpeg](https://ffmpeg.org) or `imageio-ffmpeg` | audio mix, encoding | LGPL-2.1+ or GPL-2+ depending on the build (the `imageio-ffmpeg` wrapper is BSD-2-Clause, its binaries are GPL builds) |
| [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) (`kokoro` on PyPI) | optional local English voice-over | model weights and package: Apache-2.0. Its dependencies are separate: PyTorch (BSD-style), spaCy (MIT), `misaki` (Apache-2.0), and `espeak-ng` (GPL-3.0-or-later, used by the phonemiser as a fallback) |
| Tesseract | optional text recognition fallback on non-macOS | Apache-2.0 |
| macOS Vision | text recognition on macOS (`scripts/ocr.swift`) | an operating-system framework: used, not redistributed |

The installers copy only this repository's own files. Voice-over, models and fonts are downloaded or provided by you, and only after you agree.

### What this repository contains besides code
| Files | What they are | Rights |
| --- | --- | --- |
| `docs/gallery/*`, `examples/product-demo/materials/*`, `templates/assets/*`, `evals/*/materials` | rendered or drawn by this project's own scripts; the brands in them (Demo Studio, Aurel Stoneware, Quartile, Larchwood, Relay) are fictional | MIT, like the code |
| `examples/demo/demo-music.m4a` | synthesised by `examples/demo/demo_music.py` | CC0 (public domain) |
| `examples/medstat-pilot/cover.jpg` and the shot list, demo-data script and scripted replies there | the maintainer's own product, MedStat Pilot: its name, logo and screens belong to the maintainer; the data is synthetic | shown as a worked example; the MIT licence covers the scripts, **not** the product's name or logo |
| `evals/report/*` | critics' tables and run notes from blind tests of this skill | MIT |

No fonts are bundled. The styles name fonts that are normally already on your machine (system fonts such as PingFang SC and SF Pro on macOS, Microsoft YaHei on Windows, Noto / Source Han / Inter where installed) and fall back to generic ones. A film embeds how those fonts look: for work you will publish commercially, check the licence of the fonts your machine used, or install open-licensed fonts (for example Inter, Noto Sans CJK, Source Han Sans: SIL OFL) and, if needed, point the film's `"css"` at them.

### Names and trademarks
Product, company and model names that appear here (for example Apple, macOS, Windows, Google, Antigravity, Codex, Claude, DeepSeek, Playwright, Kokoro, ffmpeg, After Effects, DaVinci Resolve) belong to their owners. They are used only to describe compatibility or industry practice. No affiliation or endorsement is implied, and no third-party logos are included.

### Your films
You are responsible for the rights to everything you put in a film (screenshots, photos, logos, music, quotes) and for the claims it makes. Reelwright labels demo data and illustrative UI on screen, and refuses unsourced figures, but it does not give legal advice. The voice-over is synthetic: disclose AI-generated voice where a platform or law asks for it. The software is provided "as is", without warranty (see [LICENSE](LICENSE)).

## 中文

Reelwright 自己的代码采用 MIT 许可（见 [LICENSE](LICENSE)）。本页说明它还使用、提到了哪些东西，以及哪些内容不在该许可范围内。许可信息以各上游项目目前公布的为准；再分发或发布前请自行到上游核对。

### 需要你自己安装的软件（本仓库不打包、不再分发）
| 组件 | 用途 | 许可（上游） |
| --- | --- | --- |
| [Playwright](https://playwright.dev)（`npm install`） | 采集、渲染、质检 | Apache-2.0；它会下载 Chromium，各部分另有许可 |
| [Node.js](https://nodejs.org) | 运行采集与渲染脚本 | MIT（含随附的第三方许可） |
| [NumPy](https://numpy.org)、[Pillow](https://python-pillow.org) | 图像分析、配色、吸附 | BSD-3-Clause；HPND |
| [ffmpeg](https://ffmpeg.org) 或 `imageio-ffmpeg` | 混音、编码 | 视构建而定，LGPL-2.1+ 或 GPL-2+（`imageio-ffmpeg` 包装库为 BSD-2-Clause，其二进制是 GPL 构建） |
| [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)（PyPI 的 `kokoro`） | 可选的本地英文配音 | 模型权重与软件包：Apache-2.0；其依赖另有许可：PyTorch（BSD 类）、spaCy（MIT）、`misaki`（Apache-2.0）、`espeak-ng`（GPL-3.0 及以上，音素转换的备用方案） |
| Tesseract | 非 macOS 上可选的文字识别备用方案 | Apache-2.0 |
| macOS Vision | macOS 上的文字识别（`scripts/ocr.swift`） | 操作系统自带框架：只使用，不再分发 |

安装脚本只复制本仓库自己的文件。配音、模型和字体由你自行下载或提供，且只在你同意之后进行。

### 仓库里除代码之外的内容
| 文件 | 是什么 | 权利 |
| --- | --- | --- |
| `docs/gallery/*`、`examples/product-demo/materials/*`、`templates/assets/*`、`evals/*/materials` | 由本项目自己的脚本渲染或绘制；其中的品牌（Demo Studio、Aurel Stoneware、Quartile、Larchwood、Relay）都是虚构的 | MIT，与代码相同 |
| `examples/demo/demo-music.m4a` | 由 `examples/demo/demo_music.py` 合成 | CC0（公有领域） |
| `examples/medstat-pilot/cover.jpg` 及其中的镜头清单、演示数据脚本和脚本化回复 | 维护者自己的产品 MedStat Pilot：名称、Logo、界面属于维护者；数据为合成数据 | 作为实战案例展示；MIT 许可只覆盖脚本，**不**包括该产品的名称和 Logo |
| `evals/report/*` | 评审表与盲测运行记录 | MIT |

仓库不打包任何字体。各风格指定的是你机器上通常已有的字体（macOS 上的苹方、SF Pro 等系统字体，Windows 上的微软雅黑，已安装时的 Noto / 思源 / Inter），找不到时回退到通用字体。成片会呈现这些字体的样子：用于商业发布的作品，请核对你机器上所用字体的许可，或安装开源许可字体（如 Inter、Noto Sans CJK、思源黑体：SIL OFL），必要时用片子的 `"css"` 指定它们。

### 名称与商标
这里出现的产品、公司和模型名称（如 Apple、macOS、Windows、Google、Antigravity、Codex、Claude、DeepSeek、Playwright、Kokoro、ffmpeg、After Effects、DaVinci Resolve）归各自所有者所有，仅用于描述兼容性或行业做法，不代表任何关联或背书，也不包含任何第三方 Logo。

### 你做的片子
你放进片子里的一切（截图、照片、Logo、音乐、引言）的权利，以及片子的说法，都由你负责。Reelwright 会在画面上标注演示数据和界面示意，并拒绝没有出处的数字，但它不提供法律意见。配音是合成声音：平台或法律要求披露 AI 生成声音时，请予以披露。本软件按"原样"提供，不附带任何担保（见 [LICENSE](LICENSE)）。
