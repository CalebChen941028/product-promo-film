# Worked example: MedStat Pilot · 实战案例

![cover](cover.jpg)

## English
MedStat Pilot is the desktop statistics app this skill was first built and tested on (its 3:26 launch film is the reference the Haiku tests are compared with). This folder keeps what still helps a new film of an installed app:

| File | What it is |
| --- | --- |
| `shots.json` | **start here** to film the installed app: a verified shot list for `scripts/capture_app.mjs` (14 shots at 4K: data, tools, t-test, KM and ROC plots, the Word report, the AI assistant on the scripted mock) |
| `make_demo_data.py` | the synthetic trial the shots use (240 patients, ~10 mmHg SBP effect, survival, biomarker, a few % missing) |
| `replies.json` | the local mock model's replies, written from the real R output of that demo data (the film says the AI text was scripted) |

Captures, music and rendered films are not in the repo: the screenshots are product material and the music belongs to its owner. The hand-written compositor the first film was made with lives in the git history; new films use `film.json` + `make_film.py`.

## 中文
MedStat Pilot 是本 skill 最初构建和测试所用的桌面统计软件（它的 3:26 发布片是 Haiku 测试的对照参考）。本文件夹保留对拍摄已安装应用仍有用的部分：`shots.json`（`scripts/capture_app.mjs` 的已验证镜头清单，**从这里开始**）、`make_demo_data.py`（镜头所用的模拟试验数据）、`replies.json`（根据这份演示数据真实 R 结果写的本地模拟模型回复；片中会说明 AI 文本为脚本）。

截图、音乐和成片不放入仓库：截图属于产品素材，音乐归原作者所有。第一部片子使用的手写合成器保存在 git 历史中；新片子请用 `film.json` + `make_film.py`。
