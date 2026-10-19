# Visual styles · 视觉风格

English first, 中文在后。A style = `styles/<id>.css` (colours, fonts, frames, captions, chapter label) + `styles/<id>.js` (background, scene transition, window chrome, beat pulse, default motion). Style and motion are independent: any style works with any motion language (`references/motion.md`). Images: `docs/gallery/` in the repo.

## English

| id | Look | Transition · pulse | Default motion | Best for |
| --- | --- | --- | --- | --- |
| `midnight-tech` | deep navy stage, fine grid, accent glow, dark glass chrome | cross-fade · glow on every beat in choruses | cinematic-3d | dev tools, data/science software, B2B platforms (the MedStat Pilot film) |
| `keynote-light` | bright off-white, soft colour haze, huge black type, long soft shadows | zoom-blur · soft glow | gentle-story | consumer & productivity apps, clinicians, investor demos |
| `editorial-mono` | near-black, off-white type, one hot accent, thin rules, giant chapter numerals, lower-third captions | hard wipe · accent edge bar | editorial-type | manifestos, opinionated research tools, launch teasers |
| `aurora-glass` | moving colour mesh, frosted-glass cards, white type, caption pill | zoom · glow | playful-pop | consumer/creator/AI apps, social-first launches |
| `neon-cyber` | black + neon grid floor, scanlines, magenta/cyan glow, monospace labels | glitch RGB-split + flash · flash | kinetic-launch | dev/security/infra, gaming-adjacent, EDM/trap music |
| `paper-academic` | warm paper with grain, serif display, ink-blue accent, hand-drawn ellipse highlights, footnote captions | page turn · none | precision-data | research, statistics, education, publishing |

### Changing the accent colour
Each CSS file starts with `:root { --accent: … }`. Use the product logo's main colour; keep contrast ≥ 4.5:1 against the background for text. `--accent-2` is a secondary highlight.

### Making a new style
Copy the closest pair of files, rename the id in both, change `:root` tokens and the backgrounds; keep every class name (`.win .bar .pic .hl .tag .chip .card .h-display .h-zh .kicker .big-num .muted .accent .warn .code #chapter #capband #capzh #capen #vignette #pulse #flash`). Then render a QA sheet of the demo with it (`examples/demo/film.json`, set `style`).

## 中文

| id | 视觉 | 转场 · 节拍脉冲 | 默认动效 | 适合 |
| --- | --- | --- | --- | --- |
| `midnight-tech` | 深海军蓝舞台、细网格、主色辉光、深色玻璃窗框 | 交叉淡化 · 副歌每拍辉光 | cinematic-3d | 开发工具、数据 / 科研软件、B2B 平台（MedStat Pilot 成片） |
| `keynote-light` | 亮白舞台、柔和彩色光晕、超大黑字、长柔阴影 | 缩放虚化 · 柔光 | gentle-story | 消费级与效率应用、面向医生、融资演示 |
| `editorial-mono` | 近黑底、米白字、单一热色、细分隔线、巨型章节数字、左下字幕 | 硬划像 · 主色边条 | editorial-type | 品牌宣言、有观点的科研工具、发布预告 |
| `aurora-glass` | 流动彩色渐变、毛玻璃卡片、白字、胶囊字幕 | 缩放 · 辉光 | playful-pop | 消费 / 创作者 / AI 应用、社交平台首发 |
| `neon-cyber` | 黑底霓虹网格地面、扫描线、品红青色辉光、等宽字体 | 故障 RGB 分离 + 闪白 · 闪光 | kinetic-launch | 开发 / 安全 / 基础设施、游戏相关、电子乐 |
| `paper-academic` | 暖色纸张颗粒、衬线标题、墨蓝主色、手绘椭圆高亮、脚注式字幕 | 翻页 · 无 | precision-data | 科研、统计、教育、出版 |

### 改主色
每个 CSS 开头是 `:root { --accent: … }`，取产品 Logo 的主色；文字与背景对比度不低于 4.5:1。`--accent-2` 为辅助高亮色。

### 新建风格
复制最接近的一对文件，两处都改 id，修改 `:root` 变量与背景；所有类名保持不变（同上英文列表）。再用 `examples/demo/film.json` 把 `style` 换成新风格，渲染 QA 联系表检查。
