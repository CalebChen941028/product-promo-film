# Visual styles · 视觉风格

English first, 中文在后。A style = `styles/<id>.css` (colours, fonts, frames, captions, chapter label) + `styles/<id>.js` (background, scene transition, window chrome, beat pulse, default motion). Style and motion are independent: any style works with any motion language (`references/motion.md`). Images: `docs/gallery/` in the repo.

## English

| id | Look | Transition · pulse | Default motion | Best for |
| --- | --- | --- | --- | --- |
| `midnight-tech` | deep navy stage, fine grid, accent glow, dark glass chrome | cross-fade · glow on every beat in choruses | cinematic-3d | dev tools, data/science software, B2B platforms (the MedStat Pilot film) |
| `clean-light` | bright off-white, soft colour haze, huge black type, long soft shadows | zoom-blur · soft glow | gentle-story | consumer & productivity apps, clinicians, investor demos |
| `editorial-mono` | near-black, off-white type, one hot accent, thin rules, giant chapter numerals, lower-third captions | hard wipe · accent edge bar | editorial-type | manifestos, opinionated research tools, launch teasers |
| `aurora-glass` | moving colour mesh, frosted-glass cards, white type, caption pill | zoom · glow | playful-pop | consumer/creator/AI apps, social-first launches |
| `neon-cyber` | black + neon grid floor, scanlines, magenta/cyan glow, monospace labels | glitch RGB-split + flash · flash | kinetic-launch | dev/security/infra, gaming-adjacent, EDM/trap music |
| `paper-academic` | warm paper with grain, serif display, ink-blue accent, hand-drawn ellipse highlights, footnote captions | page turn · none | precision-data | research, statistics, education, publishing |
| `luxe-noir` | velvet black, one warm spotlight, champagne accent, high-contrast serif, frameless photography | slow dissolve · none | gentle-story | fashion, beauty, fragrance, jewellery, watches, premium hardware, wine |
| `natural-fresh` | warm linen, soft sun glow, sage + terracotta, humanist type, photos with natural shadows | soft zoom · none | gentle-story | food & drink, wellness, travel, home & living, family, sustainable brands |

### Finish per style (applied after rendering; `cinema` in film.json overrides)
| id | Grade (LUT) | Bloom | Grain |
| --- | --- | --- | --- |
| `midnight-tech` | teal-night: teal shadows, clean neutral-warm highlights | 0.14 | 0.18 |
| `clean-light` | clean-bright: neutral, slightly warm whites | 0.05 | 0.08 |
| `editorial-mono` | bleach-print: lower saturation, print contrast | 0.04 | 0.30 |
| `aurora-glass` | pastel-glow: lifted blacks, violet shadows | 0.18 | 0.15 |
| `neon-cyber` | neon-night: deep blacks, magenta/cyan split | 0.24 | 0.20 |
| `paper-academic` | warm-print: warm paper, soft contrast | 0.03 | 0.28 |
| `luxe-noir` | noir-gold: deep blacks, warm golden highlights | 0.10 | 0.22 |
| `natural-fresh` | sunlit: warm daylight, soft lifted shadows | 0.06 | 0.14 |

All looks blend at 50 % by default, so the product's real UI colours stay true. Preview one on a still: `python3 scripts/grade.py teal-night look.cube --preview in.png out.png`.

### Changing the accent colour
Each CSS file starts with `:root { --accent: … }`. Use the product logo's main colour; keep contrast ≥ 4.5:1 against the background for text. `--accent-2` is a secondary highlight.

### Making a new style
Copy the closest pair of files, rename the id in both, change `:root` tokens and the backgrounds; keep every class name (`.win .bar .pic .hl .tag .chip .card .h-display .h-zh .kicker .big-num .muted .accent .warn .code #chapter #capband #capzh #capen #vignette #pulse #flash`). Then render a QA sheet of the demo with it (`examples/demo/film.json`, set `style`).

## 中文

| id | 视觉 | 转场 · 节拍脉冲 | 默认动效 | 适合 |
| --- | --- | --- | --- | --- |
| `midnight-tech` | 深海军蓝舞台、细网格、主色辉光、深色玻璃窗框 | 交叉淡化 · 副歌每拍辉光 | cinematic-3d | 开发工具、数据 / 科研软件、B2B 平台（MedStat Pilot 成片） |
| `clean-light` | 亮白舞台、柔和彩色光晕、超大黑字、长柔阴影 | 缩放虚化 · 柔光 | gentle-story | 消费级与效率应用、面向医生、融资演示 |
| `editorial-mono` | 近黑底、米白字、单一热色、细分隔线、巨型章节数字、左下字幕 | 硬划像 · 主色边条 | editorial-type | 品牌宣言、有观点的科研工具、发布预告 |
| `aurora-glass` | 流动彩色渐变、毛玻璃卡片、白字、胶囊字幕 | 缩放 · 辉光 | playful-pop | 消费 / 创作者 / AI 应用、社交平台首发 |
| `neon-cyber` | 黑底霓虹网格地面、扫描线、品红青色辉光、等宽字体 | 故障 RGB 分离 + 闪白 · 闪光 | kinetic-launch | 开发 / 安全 / 基础设施、游戏相关、电子乐 |
| `paper-academic` | 暖色纸张颗粒、衬线标题、墨蓝主色、手绘椭圆高亮、脚注式字幕 | 翻页 · 无 | precision-data | 科研、统计、教育、出版 |
| `luxe-noir` | 丝绒黑、一束暖光、香槟金主色、高反差衬线字体、无边框摄影 | 慢溶解 · 无 | gentle-story | 时尚、美妆、香氛、珠宝、腕表、高端硬件、酒类 |
| `natural-fresh` | 暖色亚麻底、柔和阳光、鼠尾草绿与陶土色、人文无衬线字体、自然阴影的照片 | 柔和缩放 · 无 | gentle-story | 食品饮品、身心健康、旅行、家居、亲子、可持续品牌 |

### 各风格的成片质感（渲染后施加，film.json 的 `cinema` 可覆盖）
| id | 调色（LUT） | 辉光 | 颗粒 |
| --- | --- | --- | --- |
| `midnight-tech` | teal-night：青色暗部、干净偏暖的高光 | 0.14 | 0.18 |
| `clean-light` | clean-bright：中性、略暖的白 | 0.05 | 0.08 |
| `editorial-mono` | bleach-print：低饱和、印刷感对比 | 0.04 | 0.30 |
| `aurora-glass` | pastel-glow：抬升的黑、紫色暗部 | 0.18 | 0.15 |
| `neon-cyber` | neon-night：深黑、品红 / 青色分离 | 0.24 | 0.20 |
| `paper-academic` | warm-print：暖纸色、柔和对比 | 0.03 | 0.28 |
| `luxe-noir` | noir-gold：深黑、温暖的金色高光 | 0.10 | 0.22 |
| `natural-fresh` | sunlit：温暖日光、柔和抬升的暗部 | 0.06 | 0.14 |

默认按 50% 强度混合，保证产品真实界面颜色不失真。单帧预览：`python3 scripts/grade.py teal-night look.cube --preview in.png out.png`。

### 改主色
每个 CSS 开头是 `:root { --accent: … }`，取产品 Logo 的主色；文字与背景对比度不低于 4.5:1。`--accent-2` 为辅助高亮色。

### 新建风格
复制最接近的一对文件，两处都改 id，修改 `:root` 变量与背景；所有类名保持不变（同上英文列表）。再用 `examples/demo/film.json` 把 `style` 换成新风格，渲染 QA 联系表检查。
