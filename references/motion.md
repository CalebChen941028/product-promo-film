# Motion languages · 动效语言

English first, 中文在后。The motion language decides HOW things move — entrances, text reveals, highlights, focus moves inside a screenshot, camera on the beat, and the layout of `feature` scenes. The director picks it with the look from the materials (`scripts/look.py`) and the user confirms it among the proposals (`scripts/proposals.py`); set `"motion"` in film.json to change it, or define your own (`references/custom-scenes.md`). Empty = the one that goes with the style.

## English

| id | Feels like | Entrance | Text | Highlight | Focus move | Camera | `feature` layout | Theme |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `cinematic-3d` | a product trailer | fly from depth, 34° tilt | rise | glowing grow | 1.3 s smooth push | slow orbit | 3D window + tags | platforms, B2B, serious tech |
| `precision-data` | a measured lab demo | flat snap | mask wipe | traced outline | 0.45 s snap on the beat | none | spec sheet: numbered list, number badges on the highlights, a spotlight on the current point | science, data, research, finance, medicine |
| `kinetic-launch` | a launch-event drop | punch-in from 1.22× | fast slide | flash | 0.25 s whip | punch on every bar | full-bleed zoom bursts + slammed headline | dev tools, security, AI agents, gaming, fast music |
| `gentle-story` | a documentary | soft rise 1.6 s | blur-in | soft fade | 2 s slow Ken Burns | slow dolly | soft window + one line at a time | care, health, education, mission |
| `playful-pop` | a social-app ad | elastic bloom | bounce | bouncy | overshoot | gentle sway | tilted window + sticker bubbles | consumer, creators, kids, lifestyle |
| `editorial-type` | a magazine spread | hard slide from the edge | mask-up | traced bar | 0.4 s snap | none | split screen: giant index + list, window right | manifesto, brand, opinionated research |

### Pairing guide
- One motion language per film. Mixing languages reads as indecision.
- Fast music (≥ 128 BPM) → kinetic-launch or playful-pop; slow (≤ 95 BPM) → gentle-story or precision-data.
- A scientific product with an emotional mission (e.g. patient care) → gentle-story for the story beats is wrong; keep precision-data and put the emotion in the narration and music.
- The pairs in `references/styles.md` (default motion) are safe; cross pairs (e.g. clean-light + precision-data) are fine when the theme asks for it.

### Lens, cuts and sound
Each motion language also sets a restrained lens (handheld drift, depth of field, focus pull, glints), where camera cuts happen, and the sound palette. See `references/director.md` §3.

### Engine API (custom scenes)
`M.win(lt, dur, base)` big element entrance + drift · `M.enter` · `M.pop(lt, t0, base)` small items · `M.text(el, lt, t0, base)` any text block · `M.focus(lt, [[t, rect], …])` crop path · `M.camera` (applied by the engine) · `MO` (current language: `tilt`, `focus.dur`, `focus.ease` …) · `feature(start, end, opts)` the pattern above.

## 中文

| id | 观感 | 入场 | 文字 | 高亮 | 画面推近 | 镜头 | `feature` 版式 | 主题 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `cinematic-3d` | 产品预告片 | 从纵深飞入，34° 倾角 | 上浮 | 发光放大 | 1.3 秒平滑推近 | 缓慢环绕 | 3D 窗口 + 标签 | 平台、B2B、严肃科技 |
| `precision-data` | 精确的实验演示 | 平面快速到位 | 遮罩擦出 | 描边勾勒 | 0.45 秒按拍跳转 | 无 | 规格表：编号列表，高亮框带编号角标，聚光突出当前要点 | 科学、数据、科研、金融、医学 |
| `kinetic-launch` | 发布会高潮 | 从 1.22 倍冲入 | 快速滑入 | 闪光 | 0.25 秒甩切 | 每小节一次冲击 | 满屏放大爆发 + 大标题砸入 | 开发工具、安全、AI 智能体、游戏、快节奏音乐 |
| `gentle-story` | 纪录片 | 1.6 秒柔和上浮 | 由虚到实 | 柔和淡入 | 2 秒慢速推拉 | 缓慢推近 | 柔和窗口 + 一次一句 | 关怀、健康、教育、公益 |
| `playful-pop` | 社交 App 广告 | 弹性绽放 | 弹跳 | 弹跳 | 回弹 | 轻微摇摆 | 倾斜窗口 + 贴纸气泡 | 消费、创作者、儿童、生活方式 |
| `editorial-type` | 杂志跨页 | 从边缘硬滑入 | 自下遮罩擦出 | 描边条 | 0.4 秒跳转 | 无 | 分屏：巨型序号 + 列表，窗口在右 | 宣言、品牌、观点鲜明的科研 |

### 搭配原则
- 一部片子只用一种动效语言，混用会显得犹豫。
- 快歌（≥ 128 BPM）选 kinetic-launch 或 playful-pop；慢歌（≤ 95 BPM）选 gentle-story 或 precision-data。
- 有情感使命的科学产品（如患者关怀），仍用 precision-data，把情感放在旁白和音乐里。
- `references/styles.md` 中的默认搭配最稳；主题需要时也可以交叉搭配（如 clean-light + precision-data）。

### 镜头、转场与声音
每种动效语言还决定一套克制的镜头特性（手持漂移、景深、对焦、高光）、镜头转场的位置和音效音色，见 `references/director.md` 第 3 节。

### 引擎 API（自写场景时）
同上英文：`M.win`、`M.enter`、`M.pop`、`M.text`、`M.focus`、`M.camera`、`MO`、`feature(start, end, opts)`。
