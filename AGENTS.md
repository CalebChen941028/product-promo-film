# AGENTS.md — product-promo-film

**For any AI coding agent**: Codex, Claude Code, OpenCode, Antigravity, DeepSeek Harness, Kimi Code, ZCode, Cursor, Copilot, Gemini CLI, Qwen Code, Trae and others.
面向任何 AI 编程智能体。

## English
When the user asks for a promo, launch, ad, brand or explainer film for **any product**, read `SKILL.md` in this folder and follow its 10 steps in order. Short version:

1. `python3 scripts/doctor.py` → fix every MISS.
2. No screenshots, only the product (an installed app or a URL)? Capture the real UI first: `node scripts/capture_app.mjs explore --app "/Applications/X.app"`, then a shot list and `shoot` (`references/capture.md`). Never `pkill`/`killall`; never run the product's source code.
   Then `python3 scripts/autofilm.py <materials folder> --out <project> --mood "<the user's words for the feel>"` → the genre, look, motion, arc and music (the user's track, or composed) are chosen, and drafts are written: `film.json` with TODO copy, plus `treatment.md`. 8+ software screens become a chaptered tour (2–4 min).
3. Confirm with the user: the genre on a CLOSE CALL, music, voice, contacts. If you cannot ask, keep autofilm's choices, download nothing, and list your assumptions in the report.
4. Study `templates/golden/<arc>.json` and `references/copy-bank.md`, then play the crew in `references/crew.md` to fill `treatment.md` (three anchor lines first). Then `python3 scripts/check_treatment.py treatment.md` must pass.
5. Write the copy into `film.json` (replace every TODO) and re-check with `check_treatment.py treatment.md film.json`.
6. Do the director's pass (`references/director.md` §5).
7. `python3 scripts/make_film.py film.json --stage check`, then `build` → `vo` → `qa` (0 errors) → `render` → `finish`. Use `--draft` for a quick look. The build and render gates are enforced; never edit `film_out/`.
8. Report the files, the concept, what is placeholder or composed, and what the user must still supply.

Rules:
- Real material only; honest claims; real quotes.
- The user's music or a composed track; never one from the web.
- Kokoro or the user's voice; ask before any download.
- Never type the user's API keys.
- Restraint: one hero moment (a default; break it on purpose with a reason in the treatment).
- Everything else is a default you may replace when the film is better for it: your own scenes, motion, camera moves, cuts and look in code (`references/custom-scenes.md`); a taste check you break on purpose goes in the treatment as `- Deliberate · 刻意: <check> — <why>`. Honesty, rights and legible frames never bend.

## 中文
用户要为**任何产品**做宣传片、发布片、广告片、品牌片或讲解片时，读取本目录的 `SKILL.md`，按 10 个步骤依次执行。简版：

1. `python3 scripts/doctor.py`，修好所有 MISS。
2. 没有截图、只有产品本身（已安装的应用或网址）时，先采集真实界面：`node scripts/capture_app.mjs explore --app "/Applications/X.app"`，再写镜头清单并 `shoot`（见 `references/capture.md`）。不要 `pkill`/`killall`，不要运行产品源码。
   然后 `python3 scripts/autofilm.py <素材文件夹> --out <项目目录> --mood "<用户描述的风格感觉>"`：自动选定类型、风格、动效、叙事结构与音乐（用户的曲子或原创），并写出草稿：文案为 TODO 的 `film.json`，以及 `treatment.md`。软件截图 8 张以上会排成分章节的产品巡礼（2–4 分钟）。
3. 与用户确认：CLOSE CALL 时确认类型，以及音乐、配音、联系方式。无法询问时沿用 autofilm 的选择、不下载任何东西，并在汇报里列出假设。
4. 先读 `templates/golden/<结构>.json` 与 `references/copy-bank.md`，再按 `references/crew.md` 扮演团队填写 `treatment.md`（先写三句锚点），`check_treatment.py treatment.md` 必须通过。
5. 把文案写进 `film.json`（替换所有 TODO），再用 `check_treatment.py treatment.md film.json` 检查。
6. 做导演检查（`references/director.md` 第 5 节）。
7. 运行 `make_film.py film.json --stage check`，再依次 `build` → `vo` → `qa`（0 错误）→ `render` → `finish`；`--draft` 可快速预览。构建与渲染关卡是强制的；不要手改 `film_out/`。
8. 汇报文件、创意概念、哪些是占位或原创配乐、用户还需补充什么。

规则：
- 只用真实素材；说法可核实；引言真实。
- 音乐用用户的或原创配乐，不从网上找。
- 配音用 Kokoro 或用户录音；任何下载前先征得同意。
- 不替用户填写 API Key。
- 保持克制，全片只有一个高潮（这是默认值；有理由时可在方案中写明后打破）。
- 其余都是默认值，片子需要时可以换成你自己的：用代码写场景、动效、运镜、转场和视觉（`references/custom-scenes.md`）；有意打破的审美检查写进方案：`- Deliberate · 刻意: <检查项> — <理由>`。诚实、版权和画面清晰永不变通。
