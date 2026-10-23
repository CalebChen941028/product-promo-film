# Blind tests on smaller models · 小模型盲测

English first, 中文在后。How reliably does a mid-sized model make a top-quality film with this skill? These folders measure it. Results and the acceptance verdict: [REPORT.md](REPORT.md).

## English

### The folders
| Folder | Product | What it tests |
| --- | --- | --- |
| `examples/product-demo/materials` | Aurel Stoneware, a physical product (cut-outs, photos, no music) | the sensory arc; the reference film (made by Claude Opus) exists to compare against |
| `evals/software/materials` | Quartile, desktop statistics (wireframe screens, a phone screen, a clip) | screens, highlight boxes, the problem-solution arc |
| `evals/service/materials` | Larchwood, three lakeside cabins (drawn photos, no music, no cut-outs) | a service with no product shot; the genre and the voice without help |

All three are placeholder brands with drawn or wireframe images. The report also used two folders that are never committed: real screenshots of the user's app, and the user's own product renders with no docs. For a test like that, use materials the user provides, and keep both the materials and any sheets made from them local.

### Run a blind test
1. `PLAYWRIGHT_NODE_MODULES=<…/node_modules> ./evals/make_materials.sh` builds the images.
2. Copy each materials folder to a neutral path. For Aurel this matters, because the reference treatment sits next to its folder.
3. Give a smaller model (e.g. Claude Haiku as a sub-agent) only this prompt, nothing else:
   `Make a promo film for the product in <folder> using the skill at <skill path> (read SKILL.md and follow it). Output to <dir>.`
   Log any deviations: stalls, nudges, hand-edited files, downloads, and gates that were skipped.
4. Make the critic's view of each film, including the reference:
   `python3 evals/sheet.py <film.mp4> <out_prefix> --film <film.json>`
   This writes a 20-frame sheet from 1.0 s and a moments sheet (hook, hero, end). Add a short script with the scene order, the spoken lines and the titles.
5. Score with **three fresh critics** (e.g. Claude Sonnet sub-agents). Each critic gets its own shuffled folder of `F01…` files plus `references/crew.md` §9 as `rubric.md`, and no treatments or self-scores. Keep each critic's mapping.
6. Put the reference in every panel, and compare films only within one panel.
7. The acceptance bar used in the report is the mean of three critics ≥ the reference's mean, with every gate passing. The stretch bar is an average ≥ 4.

### Highlight boxes and crops, product-agnostic (`evals/rects/`)
Random interfaces of many kinds (light, dark, low-contrast, borderless cards, tables, charts, forms, phone width, CJK and Latin), with the true box of every element. Nothing comes from any one product.
```
node evals/rects/gen_ui.mjs evals/runs/rects 40 7
python3 evals/rects/bench.py evals/runs/rects          # boxes written by eye vs snapped (scripts/snap.py)
python3 evals/rects/bench_cuts.py evals/runs/rects     # crops that cut through content vs clean crops
python3 evals/rects/bench_text.py evals/runs/rects     # a point's words correcting a box written on the wrong element
```
Tuned on seed 7, checked on a held-out set (seed 99): a box written by eye (off by 10–40 %) frames its element (IoU ≥ 0.7) 11 % of the time; snapped to the page's element boxes 95 %, to pixel blocks only 87 %. Cut crops caught 65 %, clean crops flagged 0 %. Words (half the boxes written on a wrong element): with the page's element texts, wrong boxes corrected 54–60 % and right boxes untouched (95–98 %); with OCR on a plain screenshot (macOS Vision, else Tesseract), wrong boxes corrected 18–23 %, right boxes within 1 point of pixels-only snapping.


## 中文

### 素材文件夹
- `examples/product-demo/materials`：实物产品 Aurel 炻器（透明底产品图、照片、无音乐），测感官叙事结构；有 Claude Opus 制作的参考片可比。
- `evals/software/materials`：桌面统计软件 Quartile（线框界面、手机截图、录屏），测界面、高亮框与问题-解决结构。
- `evals/service/materials`：湖畔小木屋 Larchwood（手绘照片，无音乐、无产品图），测没有产品图的服务类，以及无人帮助时的类型与配音选择。

三者都是占位品牌，图片均为手绘或线框占位图。报告还用了两个从不提交的文件夹：用户自己应用的真实截图，以及用户自己、没有文档的产品渲染图。做这类测试时，请使用用户提供的素材，素材和用它做出的联系表都只留在本地。

### 运行盲测
1. 运行 `./evals/make_materials.sh` 生成图片（需设置 `PLAYWRIGHT_NODE_MODULES`）。
2. 把每个素材文件夹复制到中性路径。Aurel 尤其要这样做，因为参考方案就在它旁边。
3. 只给较小的模型（如作为子智能体的 Claude Haiku）上面那一句提示，不给任何其他帮助。记录偏差：卡住、被提醒、手改文件、下载、跳过关卡。
4. 为每部片子（包括参考片）准备评审看的材料：
   `python3 evals/sheet.py <film.mp4> <输出前缀> --film <film.json>`
   这会生成从 1.0 秒起的 20 帧联系表，以及开场、高潮、结尾的关键帧条。另附一份简短脚本，写明场景顺序、旁白和标题。
5. 用**三位全新的评审**打分（如 Claude Sonnet 子智能体）。每位评审拿到自己的、顺序打乱的 `F01…` 文件夹，以及作为 `rubric.md` 的 `references/crew.md` 第 9 节；不给方案，也不给自评分。保存每位评审的对应表。
6. 每组评审都放入参考片，只在同一组评审内比较。
7. 报告采用的验收线：三位评审的平均分 ≥ 参考片的平均分，且所有关卡通过。拔高目标：平均 ≥ 4。

### 高亮框与裁剪的通用测试（`evals/rects/`）
随机生成多种界面（浅色、深色、低对比、无边框卡片、表格、图表、表单、手机宽度、中英文），并记录每个元素的真实位置，与任何具体产品无关。命令见上方英文。以种子 7 调参、以独立的种子 99 复核：凭目测写的框（偏差 10–40%）准确框住元素（重合度 ≥ 0.7）的比例为 11%；吸附到页面元素位置后为 95%，只用像素识别为 87%。切断内容的裁剪检出 65%，干净裁剪误报 0%。文字纠错（一半的框故意写在错误元素上）：有页面元素文字时，错框纠正 54–60%，对的框不受影响（95–98%）；普通截图用 OCR（macOS Vision，否则 Tesseract）时，错框纠正 18–23%，对的框与纯像素吸附相差不到 1 个百分点。
