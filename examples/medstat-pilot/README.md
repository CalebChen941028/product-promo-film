# Worked example: MedStat Pilot launch film v2 (3:26) · 实战案例

![cover](cover.jpg)

## English
The production film this skill was distilled from. It is the **hand-written** version, made before the scene library and `film.json` existed. Read it to see how a 13-scene film is built scene by scene; new films should use `film.json` + `make_film.py` instead.

| File | What it is |
| --- | --- |
| `film.html` + `script.js` + `data.js` + `film.js` | the compositor: helpers, 13 scenes, engine in one file (same API ideas as `templates/engine.js`) |
| `shots.json` | **start here** to film the installed app: a verified shot list for `scripts/capture_app.mjs` (14 shots at 4K: data, tools, t-test, KM and ROC plots, the Word report, the AI assistant on the scripted mock) |
| `shoot.mjs` | the original capture script (web dev build): upload, parse, toolbox, t-test run, 9 result plots, AI chat, Word/R downloads, tall captures |
| `replies.json` | the local mock model's replies, written from the real R output (the film says AI text was scripted) |
| `narration.json` | 35 English narration lines + Chinese captions, with `cap` for digits |
| `make_demo_data.py` | the synthetic trial (240 patients, ~10 mmHg SBP effect, survival, biomarker, a few % missing) |

Captures, music and the rendered film are not in the repo: the screenshots are product material, and the music belongs to its owner. The music was 120 BPM; its second chorus (bars 56–72) was repeated once to fit 3:26.

## 中文
这是本 skill 提炼自的正式成片，属于场景库和 `film.json` 出现之前的**手写版本**。可以参考它如何逐个场景搭出 13 个场景的完整片子；新片子请用 `film.json` + `make_film.py`。

各文件说明见上方英文表格。要拍已安装的应用，从 `shots.json` 开始（`scripts/capture_app.mjs` 的已验证镜头清单）。截图、音乐和成片未放入仓库：截图属于产品素材，音乐归原作者所有。原曲为 120 BPM，第二段副歌（第 56–72 小节）重复一次，使成片达到 3:26。
