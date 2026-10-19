# Storyboard on the beat · 卡在节拍上的分镜

English first, 中文在后。

## English

### Draft automatically
```bash
python3 scripts/beat_grid.py music.mp3 --ffmpeg "$FFMPEG" --out build/grid.json
python3 scripts/plan_storyboard.py build/grid.json brief.json --out storyboard.md
```
The draft keeps the brief's order, gives each scene a bar range, and flags a feature with ⚠ when its `energy` is two steps from its music (reorder the brief or move the beat).

### The proven structure (MedStat Pilot, 120 BPM, 3:26)
| Bars | Music | Scene type | Content |
| --- | --- | --- | --- |
| 0–3 | intro | cover | logo, name, positioning, platforms |
| 3–7 | intro | pain | scattered old tools collapse |
| 7–16 | build | feature ×2–3 | home → data recognised → preview |
| 16–24 | build+ | carousel | toolbox, one tool per bar |
| 24–28 | chorus 1 | numbers | 17 domains · 100+ methods |
| 28–40 | chorus 1 | feature | pick method → drag variables → run → results → AI insight |
| 40–47 | break | feature (quiet) | AI assistant + privacy |
| 47–56 | build 2 | gallery | one result type per bar, named in the voice-over |
| 56–72 | chorus 2 | feature / gallery | figures & DPI → Word report → reproducible R → AI studio |
| 72–88 | chorus 2 (extended) | compare + statement | old way vs new, one row per 2 bars; platforms |
| 88–96 | final chorus | finale | wall of real screens, keywords on beats, tagline |
| 96–end | outro | endcard | logo · name · motto · contacts · chips |

### Narration (`say`)
~2.5 English words per second. One sentence per line. Gallery: one short phrase per item, `at` = item index + 0.15. Lines already typeset on screen get `id: "tagline"` / `"motto"`.

## 中文

### 自动起草
运行上方两条命令。草稿保持 brief 的顺序，给每个场景分配小节；某个功能的 `energy` 与所在音乐段相差两级时标 ⚠（调整 brief 顺序或移动这一段）。

### 验证过的结构（MedStat Pilot，120 BPM，3:26）
| 小节 | 音乐 | 场景类型 | 内容 |
| --- | --- | --- | --- |
| 0–3 | 前奏 | cover | Logo、名称、定位、平台 |
| 3–7 | 前奏 | pain | 分散的旧工具塌缩 |
| 7–16 | 铺垫 | feature ×2–3 | 主界面 → 数据识别 → 预览 |
| 16–24 | 铺垫加强 | carousel | 工具箱，每小节一个工具 |
| 24–28 | 副歌 1 | numbers | 17 个领域 · 100+ 方法 |
| 28–40 | 副歌 1 | feature | 选方法 → 拖变量 → 运行 → 结果 → AI 解读 |
| 40–47 | 间奏 | feature（安静） | AI 助手 + 隐私 |
| 47–56 | 铺垫 2 | gallery | 每小节一种结果图，配音点名 |
| 56–72 | 副歌 2 | feature / gallery | 图表与 DPI → Word 报告 → 可复现 R → AI 工作台 |
| 72–88 | 副歌 2（延长） | compare + statement | 传统 vs 新方式，每 2 小节一行；平台 |
| 88–96 | 终段副歌 | finale | 真实界面墙、按拍闪关键词、口号 |
| 96–尾 | 尾声 | endcard | Logo · 名称 · 理念 · 联系方式 · 平台 |

### 旁白（`say`）
英文约每秒 2.5 个词，每行一句。图集场景每张图一个短语，`at` = 序号 + 0.15。画面上已经排版的句子用 `id: "tagline"` / `"motto"`。
