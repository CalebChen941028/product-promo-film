# The director's cut: your own scenes, motion, moves, cuts and look · 导演剪辑版：自定义场景、动效、运镜、转场与视觉

English first, 中文在后。Everything the skill picks is a default. When the film needs something the library does not have, write it. The engine, the QA, the captions, the grade, the sound and the honesty gates keep working on whatever you write.

## English

### What is fixed and what is free
| Layer | Default | Yours to replace |
| --- | --- | --- |
| Story | autofilm's arc and beats | any scene list, any order, any length |
| Scenes | 22 library types | `{"type": "custom", "fn": "name"}` + your script |
| Motion language | 6 languages | `"motions"`: your own, built on one (`"like"`) |
| Layout, camera, cut | the director's proposal | per scene `"layout"` / `"camera"` / `"cut"`; your own `CAMERA.x` / `CUT.x` |
| Look | 8 styles | `"css"`: your stylesheet over the style (variables, fonts, any rule) |
| Colour, grade | the colour director, the style's LUT | `"palette"`, `"cinema": {"grade", "grade_strength", …}` |
| Music, sound, voice | composed underscore, synthesised cues, Kokoro | the user's track, mood/BPM/seed, `cinema.sfx`, recordings |
| Taste checks | caps on the self-scores | `- Deliberate · 刻意: <check> — <why>` in the treatment turns that check into advice |
| **Never** | | real material only, true claims with sources, labelled demo data and AI imagery, rights, privacy, legible and unbroken frames (QA) |

### Custom scenes
List your files in film.json `"scripts": ["scenes/mine.js"]` (paths relative to film.json); they load after the library. Register a scene and use it:
```js
CUSTOM.beforeAfter = (start, end, o) => {
  scene(start, end, (R, S) => { /* build once: win(), textEl(), img(), div() */ },
                    (S, lt, d) => { /* every frame: place(), setCrop(), M.text(), M.pop() — pure functions of lt */ });
};
```
```json
{"type": "custom", "fn": "beforeAfter", "bars": 4, "assets": {"before": "materials/raw.png", "after": "materials/table.png"},
 "say": [{"en": "…", "zh": "…"}], "size": "MS"}
```
- `assets` are copied with the film; read them as `o.assets.before`. Any other field reaches the scene as `o.*`.
- The API is the library's: `scene`, `win(R, {srcs, base, crop, w, chrome})`, `setCrop`, `place(el, {x, y, z, rx, ry, rz, s, o})`, `textEl`, `img`, `div`, `hl` / `posHL`, `M.win` / `M.enter` / `M.text` / `M.pop` / `M.focus` (the scene's motion language), `prog`, `fade`, `lerp`, `clamp`, `eo`, `eio`, `ex`, `esoft`, `eback`, `bar(n)`. The header of `templates/engine.js` lists all of it; `templates/library.js` is the best set of examples.
- Rules: deterministic (no timers, no CSS animations, no `Math.random`); colours and type from the style (`var(--accent)`, `.h-zh`, `.kicker`, `.chip`…); 96 px margins; real pictures only. A `.webm` path in `srcs` plays as footage.
- Working example: `templates/custom.example.js` (a before → after wipe).

### Your own motion language
```json
"motions": {"quiet-lab": {"like": "precision-data", "enter": "rise", "text": "blur", "camera": "dolly", "tilt": 0.1,
                          "focus": {"dur": 1.1, "ease": "esoft"},
                          "palette": {"feature": ["split", "full"], "camera": ["dolly", "pan-l", "pan-r"], "cuts": ["blur", "wipe"]}}},
"motion": "quiet-lab"
```
Primitives: `enter` fly · snap · punch · rise · bloom · slide; `text` rise · mask · maskup · slide · blur · bounce; `hl` grow · draw · flash · soft · bounce; `pop` back · snap · punch · soft · elastic; `camera` any built-in or your own; `focus.ease` eio · eo · ex · esoft · eback · linear. `"palette"` tells the director which layouts, moves and cuts this language may use. A scene can also borrow one: `"motion": "quiet-lab"`.

### Your own camera moves and cuts
In a script:
```js
CAMERA.spiral = ({ t, lt, dur, p, beat, bar }) => `rotate(${(p * 2 - 1) * 0.8}deg) scale(${1 + 0.04 * p})`;   // p: eased 0→1 over the scene
CUT['film-burn'] = ({ p, inc }) => ({ opacity: inc ? p : 1 - p, filter: `brightness(${1 + Math.sin(Math.PI * p) * 1.8}) sepia(${Math.sin(Math.PI * p)})` });
CUT['film-burn'].len = 1.6;   // × the style's crossfade (≤ 2)
```
Then `"camera": "spiral"`, `"cut": "film-burn"` on any scene. `--stage check` accepts the names your scripts register.

### Your own look
`"css": ["look.css"]` loads after the style, so it wins: `:root { --bg-edge: #0d0f12; --ink: #f4f1ea; --zh: "Source Han Serif SC", serif; }`, a different caption band, a new chip shape. Accent colours come from `"palette"` (it is applied last); remove `"palette"` to let your CSS set them. Fonts: installed system fonts, or absolute `file://` URLs.

### Breaking a taste default on purpose
The taste checks protect the average film. When your film needs to break one, say so in the treatment (§9):
`- Deliberate · 刻意: Rhythm — three close-ups in a row: the open is a macro sequence; Specific — the middle is a quiet mood passage`
That check then advises instead of blocking. Checks you can name: One idea, Hook, Specific, Image, Restraint, Rhythm, Hero, ending. Honesty checks cannot be named.

## 中文

### 什么是固定的，什么是自由的
| 层面 | 默认 | 可以替换为你自己的 |
| --- | --- | --- |
| 叙事 | autofilm 的结构与拍点 | 任意场景列表、顺序、长度 |
| 场景 | 22 种内置类型 | `{"type": "custom", "fn": "名字"}` + 你的脚本 |
| 动效语言 | 6 种 | `"motions"`：基于某一种（`"like"`）定义你自己的 |
| 版式、运镜、转场 | 导演的建议 | 每个场景的 `"layout"` / `"camera"` / `"cut"`；你自己的 `CAMERA.x` / `CUT.x` |
| 视觉 | 8 种风格 | `"css"`：叠加在风格之上的样式表（变量、字体、任意规则） |
| 配色、调色 | 色彩导演、风格 LUT | `"palette"`、`"cinema": {"grade", "grade_strength", …}` |
| 音乐、声音、配音 | 原创配乐、合成音效、Kokoro | 用户的曲子、情绪/BPM/种子、`cinema.sfx`、录音 |
| 审美检查 | 自评分封顶 | 在方案里写 `- Deliberate · 刻意: <检查项> — <理由>`，该项改为提醒 |
| **永远不变** | | 只用真实素材；说法真实有出处；演示数据与 AI 画面要标注；版权；隐私；画面清晰不出错（QA） |

### 自定义场景
在 film.json 写 `"scripts": ["scenes/mine.js"]`（相对 film.json 的路径），脚本在场景库之后加载。注册场景（`CUSTOM.名字 = (start, end, o) => { scene(...) }`），然后用 `{"type": "custom", "fn": "名字", "bars": 4, "assets": {...}}` 调用。`assets` 里的图片会随片子复制，在脚本里用 `o.assets.xxx` 读取；其他字段都以 `o.*` 传入。可用的 API 与场景库相同（见上方英文与 `templates/engine.js` 开头）。规则：结果只取决于时间（不用定时器、CSS 动画、随机数）；颜色和字体取自风格变量；边距 96 px；只用真实画面。`.webm` 会作为视频播放。完整示例：`templates/custom.example.js`。

### 自定义动效语言
在 `"motions"` 里基于一种内置语言（`"like"`）组合原语并调参数（入场、文字显现、高亮、弹出、镜头、推近时长与缓动），可附带 `"palette"` 告诉导演这种语言能用哪些版式、运镜和转场。设为全片 `"motion"`，或只给某个场景使用。

### 自定义运镜与转场
在脚本里注册 `CAMERA.名字 = ({t, lt, dur, p, beat, bar}) => 'CSS transform'` 和 `CUT['名字'] = ({p, inc}) => ({opacity, transform, filter, clipPath})`（可设 `.len`，≤ 2），然后在场景里写 `"camera"` / `"cut"`。`--stage check` 会识别脚本里注册的名字。

### 自定义视觉
`"css": ["look.css"]` 在风格之后加载，优先级最高：可改变量、字体、字幕带、标签形状等。强调色由 `"palette"` 最后设定；想让 CSS 决定强调色，就删掉 `"palette"`。字体用系统已安装字体，或绝对路径的 `file://`。

### 有意打破审美默认值
审美检查保护的是平均水平。你的片子需要打破某一条时，在方案第 9 节写明：`- Deliberate · 刻意: Rhythm — 连续三个特写：开场是一组微距; Specific — 中段是一段安静的情绪段落`。对应检查就从阻止改为提醒。可写的检查项：One idea、Hook、Specific、Image、Restraint、Rhythm、Hero、ending。诚实类检查不能写进来。
