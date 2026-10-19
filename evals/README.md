# Blind tests on smaller models · 小模型盲测

English first, 中文在后。How reliably does a mid-sized model make a top-quality film with this skill? These folders measure it. Results: [REPORT.md](REPORT.md).

## English

### The three folders
| Folder | Product | What it tests |
| --- | --- | --- |
| `examples/product-demo/materials` | Aurel Stoneware, a physical product (cut-outs, photos, no music) | the sensory arc; the reference film exists to compare against |
| `evals/software/materials` | Quartile, desktop statistics (wireframe screens, a phone screen, a clip) | screens, highlight boxes, the problem-solution arc |
| `evals/service/materials` | Larchwood, three lakeside cabins (drawn photos, no music, no cut-outs) | a service with no product shot; the genre and the voice without help |

All three are placeholder brands; the images are drawn or wireframe placeholders.

### Run a blind test
1. `PLAYWRIGHT_NODE_MODULES=<…/node_modules> ./evals/make_materials.sh` builds the images.
2. Copy each materials folder to a neutral path (for Aurel this matters: the reference treatment sits next to its folder).
3. Give a smaller model (e.g. Claude Haiku as a sub-agent) only this prompt, nothing else:
   `Make a promo film for the product in <folder> using the skill at <skill path> (read SKILL.md and follow it). Output to <dir>.`
4. Score each film with the taste rubric (`references/crew.md` §9) from the contact sheet, the script and the treatment, as an outside critic. Score the reference film the same way. Note deviations: skipped crew or gates, hand-edited files, downloads, missing rects, stalls.

## 中文
### 三个文件夹
- `examples/product-demo/materials`：实物产品 Aurel 炻器（透明底产品图、照片、无音乐），测感官叙事结构，有参考成片可比。
- `evals/software/materials`：桌面统计软件 Quartile（线框界面、手机截图、录屏），测界面、高亮框与问题-解决结构。
- `evals/service/materials`：湖畔小木屋 Larchwood（手绘照片，无音乐、无产品图），测没有产品图的服务类，以及无人帮助时的类型与配音选择。

三者都是占位品牌，图片均为手绘或线框占位图。

### 运行盲测
1. 运行 `./evals/make_materials.sh` 生成图片（需设置 `PLAYWRIGHT_NODE_MODULES`）。
2. 把每个素材文件夹复制到中性路径（Aurel 尤其要这样做：参考方案就在它旁边）。
3. 只给较小的模型（如作为子智能体的 Claude Haiku）上面那一句提示，不给任何其他提示。
4. 以外部评审身份，按 `references/crew.md` 第 9 节的品味标准，依据联系表、脚本和方案给每部片打分；参考片也用同样方式打分。记录偏差：跳过团队或关卡、手改生成文件、下载、缺少高亮框、卡住不动。
