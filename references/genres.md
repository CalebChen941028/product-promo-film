# Product genres · 产品类型

English first, 中文在后。`scripts/genres.py` scores each genre on keyword hits in the brief, docs and file names, plus what the materials folder contains. The top genre sets the defaults below for the story arc, music and voice. The **look** (style and motion) is not a default: the director chooses it from the materials (`scripts/look.py`, `references/director.md` §9), so the style column below is only the genre's usual character, one input among several. Override with `"genre"` in the brief or `film.json`, or with `autofilm.py --genre`. Edit or add genres in `templates/genres.json`.

## English
| Genre | Product | Look | Motion | Composed music | Arc |
| --- | --- | --- | --- | --- | --- |
| `software-saas` | Software, SaaS, productivity · 软件 / SaaS / 效率工具 | `midnight-tech` (or `clean-light`, `editorial-mono`) | `cinematic-3d` | `cinematic-pulse` 104 | `problem-solution` |
| `developer-ai` | Developer tools, AI agents, infrastructure · 开发者工具 / AI 智能体 / 安全基础设施 | `neon-cyber` (or `midnight-tech`, `editorial-mono`) | `kinetic-launch` | `minimal-electronic` 120 | `hype` |
| `science-data` | Science, research, data analysis · 科研 / 数据分析 / 统计 | `midnight-tech` (or `paper-academic`, `clean-light`) | `precision-data` | `minimal-electronic` 104 | `problem-solution` |
| `finance-fintech` | Finance, fintech, payments · 金融 / 支付 / 理财 | `midnight-tech` (or `clean-light`, `paper-academic`) | `precision-data` | `minimal-electronic` 108 | `problem-solution` |
| `mobile-consumer-app` | Consumer app, social, creator tools · 消费级 App / 社交 / 创作 | `aurora-glass` (or `clean-light`, `natural-fresh`) | `playful-pop` | `bright-pop` 118 | `hype` |
| `consumer-electronics` | Consumer electronics, smart hardware · 消费电子 / 智能硬件 / 设备 | `clean-light` (or `midnight-tech`, `luxe-noir`) | `cinematic-3d` | `cinematic-pulse` 100 | `reveal` |
| `fashion-beauty-luxury` | Fashion, beauty, luxury · 时尚 / 美妆 / 奢品 / 珠宝 | `luxe-noir` (or `editorial-mono`, `natural-fresh`) | `gentle-story` | `luxe-lounge` 90 | `sensory` |
| `food-beverage` | Food & beverage · 食品 / 饮品 / 餐饮 | `natural-fresh` (or `luxe-noir`, `clean-light`) | `gentle-story` | `warm-acoustic` 98 | `sensory` |
| `health-wellness` | Health, care, wellness · 健康 / 医疗服务 / 身心 | `clean-light` (or `natural-fresh`, `paper-academic`) | `gentle-story` | `warm-piano` 84 | `human-story` |
| `education-learning` | Education, learning · 教育 / 学习 / 知识 | `clean-light` (or `paper-academic`, `aurora-glass`) | `gentle-story` | `warm-piano` 96 | `human-story` |
| `mobility-industrial` | Automotive, mobility, industrial · 汽车 / 出行 / 工业 / 制造 | `midnight-tech` (or `editorial-mono`, `luxe-noir`) | `cinematic-3d` | `cinematic-pulse` 100 | `reveal` |
| `travel-hospitality-living` | Travel, hospitality, home, real estate · 旅行 / 酒店 / 家居 / 地产 | `natural-fresh` (or `luxe-noir`, `clean-light`) | `gentle-story` | `ambient-air` 88 | `sensory` |
| `game-entertainment-event` | Games, entertainment, events · 游戏 / 娱乐 / 活动发布 | `neon-cyber` (or `editorial-mono`, `aurora-glass`) | `kinetic-launch` | `minimal-electronic` 124 | `hype` |
| `kids-family` | Kids, family, toys · 儿童 / 亲子 / 玩具 | `aurora-glass` (or `natural-fresh`, `clean-light`) | `playful-pop` | `bright-pop` 116 | `human-story` |
| `brand-mission` | Brand, mission, non-profit · 品牌 / 公益 / 机构宣言 | `editorial-mono` (or `clean-light`, `luxe-noir`) | `editorial-type` | `warm-piano` 88 | `human-story` |

### Story arcs
- **problem-solution**: tension → reveal → proof → why it is new → hero
- **reveal**: details first → the reveal → craft → range → specs → in life → hero
- **sensory**: mood → texture → the feeling named → reveal → origin → range → a real voice → hero
- **human-story**: human truth → a person → tension → how it helps → a real voice → impact → hero
- **hype**: the promise → show it running → proof → breadth → outputs → numbers → hero

Beats whose material is missing are skipped; optional beats are dropped first when the film runs long (`autofilm.py --seconds`).

## 中文
各类型对应的风格、动效、原创配乐与叙事结构见上表。`genres.py` 依据 brief、文档、文件名中的关键词，以及素材文件夹里有什么（界面、照片、透明底产品图、录屏）来打分。可在 brief 或 `film.json` 中用 `"genre"` 覆盖，或运行 `autofilm.py --genre`。在 `templates/genres.json` 中可修改或新增类型。

### 叙事结构
- **problem-solution**：矛盾 → 揭晓 → 证明 → 新在哪里 → 高潮
- **reveal**：先细节 → 揭晓 → 工艺 → 系列 → 规格 → 生活场景 → 高潮
- **sensory**：氛围 → 质感 → 点出感受 → 揭晓 → 来源 → 系列 → 真实声音 → 高潮
- **human-story**：人性真相 → 一个人 → 矛盾 → 如何帮助 → 真实声音 → 影响 → 高潮
- **hype**：承诺 → 实际运行 → 证明 → 广度 → 产出 → 数字 → 高潮

缺少素材的拍点会被跳过；片子过长时（`autofilm.py --seconds`）先删可选拍点。
