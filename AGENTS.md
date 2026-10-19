# AGENTS.md — product-promo-film

**For any AI coding agent** (Codex, Claude Code, OpenCode, Antigravity, DeepSeek Harness, Kimi Code, ZCode, Cursor, Copilot, Gemini CLI, Qwen Code, Trae …).
面向任何 AI 编程智能体。

## English
When the user asks for a product promo / launch / explainer video, **read `SKILL.md` in this folder and follow its 11 steps in order.** Short version:

1. `python3 scripts/doctor.py` → fix every MISS.
2. Put the user's materials in `materials/`; run `scripts/intake.py`.
3. Fill `brief.json` (from `templates/brief.example.json`) with the user.
4. `scripts/recommend_style.py` → let the user pick look + motion.
5. Copy `templates/film.example.json` → `film.json`; fill scenes from the library (`references/film-spec.md`).
6. Director's pass (`references/director.md` §5): one hero moment, mood arc, camera cuts only where the story turns. Defaults do most of it.
7. `python3 scripts/make_film.py film.json --stage check` until no ERROR, then `build` → `vo` → `qa` (0 errors) → `render` → `finish` (`--draft` for a quick look).
8. Report files, what is demo/simulated, and what the user must still supply.

Rules: real UI only · honest claims · user-provided/licensed music · Kokoro or user voice (no OS voices) · never type the user's API keys · ask before downloading models · never render before QA passes.

## 中文
用户要做产品宣传片、发布视频或讲解视频时，**读取本目录的 `SKILL.md`，按其中 11 个步骤依次执行。** 简版：

1. `python3 scripts/doctor.py`，修好所有 MISS。
2. 用户素材放进 `materials/`，运行 `scripts/intake.py`。
3. 与用户一起填写 `brief.json`（模板：`templates/brief.example.json`）。
4. 运行 `scripts/recommend_style.py`，让用户选定视觉风格与动效语言。
5. 复制 `templates/film.example.json` 为 `film.json`，从场景库填写场景（`references/film-spec.md`）。
6. 导演检查（`references/director.md` 第 5 节）：一个高潮、情绪弧线、只在故事转折处用镜头转场；默认值已完成大部分。
7. `python3 scripts/make_film.py film.json --stage check` 直到没有 ERROR，再依次 `build` → `vo` → `qa`（0 错误）→ `render` → `finish`（`--draft` 可快速预览）。
8. 汇报文件位置、哪些是演示 / 模拟内容、用户还需补充什么。

规则：只用真实界面 · 说法可核实 · 音乐由用户提供或已授权 · 配音用 Kokoro 或用户录音（不用系统语音）· 不替用户填写 API Key · 下载模型前先征得同意 · QA 不通过不渲染。
