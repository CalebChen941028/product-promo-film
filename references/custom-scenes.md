# The director's cut: your own scenes, motion, moves, cuts and look · 导演剪辑版：自定义场景、动效、运镜、转场与视觉

English first, 中文在后。Everything the skill picks is a default. When the film needs something the library does not have, write it. The engine, the QA, the captions, the grade, the sound and the honesty gates keep working on whatever you write.

## English

### What is fixed and what is free
| Layer | Default | Yours to replace |
| --- | --- | --- |
| Story | autofilm's arc and beats | any scene list, any order, any length |
| Scenes | 23 library types | `{"type": "mg", "layers": […]}` motion graphics in JSON, or `{"type": "custom", "fn": "name"}` + your script |
| Motion language | 6 languages | `"motions"`: your own, built on one (`"like"`) |
| Layout, camera, cut | the director's proposal | per scene `"layout"` / `"camera"` / `"cut"`; keyframe `"cameras"` / `"cuts"` in film.json; or `CAMERA.x` / `CUT.x` in code |
| Look | 8 styles | `"css"`: your stylesheet over the style (variables, fonts, any rule) |
| Colour, grade | the colour director, the style's LUT | `"palette"`, `"cinema": {"grade", "grade_strength", …}` |
| Music, sound, voice | composed underscore, synthesised cues, Kokoro | the user's track, mood/BPM/seed, `cinema.sfx`, recordings |
| Taste checks | caps on the self-scores | `- Deliberate · 刻意: <check> — <why>` in the treatment turns that check into advice |
| **Never** | | real material only, true claims with sources, labelled demo data and AI imagery, rights, privacy, legible and unbroken frames (QA) |

### Motion graphics without code: the `mg` scene
Design an MG beat in film.json: layers, each with keyframes in **beats** from the scene's start, so every move lands on the music.
```json
{"type": "mg", "bars": 4, "say": [{"en": "…", "zh": "…"}], "layers": [
  {"kind": "circle", "r": 230, "stroke": "accent", "width": 4, "draw": [0, 3]},
  {"kind": "line", "points": [[-520, 180], [0, 0], [520, -180]], "stroke": "faint", "draw": [1, 4]},
  {"kind": "rect", "w": 360, "h": 6, "radius": 3, "fill": "accent", "keys": [[2, {"sx": 0, "y": 120}], [3, {"sx": 1, "y": 120}]]},
  {"kind": "text", "zh": "一口，*醒*过来", "en": "One sip, awake", "size": 72,
   "keys": [[0.5, {"o": 0, "y": 40, "blur": 12}], [1.5, {"o": 1, "y": 0, "blur": 0}]]},
  {"kind": "number", "value": 102, "suffix": "", "zh": "种方法", "en": "methods", "at": 2, "keys": [[0, {"x": -400}]]},
  {"kind": "image", "media": "materials/cup.jpg", "w": 300, "radius": 150, "keys": [[3, {"o": 0, "x": 520, "s": 0.8}], [4.5, {"o": 1, "x": 520, "s": 1}, "eback"]]}
]}
```
- Kinds: `text` (`zh`, `en?`, `size?`, `align?`; `*word*` in the accent) · `rect` (`w`, `h`, `radius?`, `fill?`, `stroke?`) · `circle` (`r`) · `line` (`points`, px from the centre) · `path` (`d`, SVG in stage px 1920 × 1080) · `number` (`value`, `suffix?`, `zh?`, `en?`, `at`) · `image` (`media`: a real material, `w`, `radius?`).
- Keys: `[[beat, {x, y, s, sx, sy, rz, o, blur}, "ease"?], …]`; x/y px from the centre; eases `eio` `eo` `ex` `esoft` `eback` `linear` (per key or `"ease"` per layer). `draw: [b0, b1]` traces a stroke between two beats.
- Colours: `accent`, `accent2`, `ink`, `muted`, `faint`, `bg`, or any CSS colour (the style's tokens keep it in the film's palette).
- Honesty still holds: a `number` shows only its true value (it never counts through others) and is checked against the docs like any other number; `image` takes only real materials.

### Camera moves and cuts without code: keyframes
```json
"cameras": {"float-up": {"from": {"s": 1.0, "y": 30, "rz": -0.6}, "to": {"s": 1.07, "y": -20, "rz": 0.4}, "ease": "esoft", "pulse": 0.006}},
"cuts":    {"lift": {"from": {"o": 0, "y": 120, "s": 0.96, "blur": 10}, "to": {"o": 0, "y": -80, "blur": 6}, "reveal": "up", "ease": "eo", "len": 1.4}}
```
- A camera moves the whole scene from `from` to `to` over its length (`x y z` px, `s` scale, `rx ry rz` degrees); `pulse` adds a scale kick on every beat.
- A cut brings the incoming scene from `from` (`o` opacity, `blur`, `bright` too) and sends the outgoing one towards `to` (default: it stays); `reveal` opens the incoming scene as `left` `right` `up` `down` `circle` or `center`; `len` × the style's crossfade (0.4–2).
- `"at": [x, y]` (stage px) makes either one scale and turn around that point, and a `circle` reveal open from it: a **zoom-through** dives into a button or a detail and the next scene grows out of it: `"cuts": {"dive": {"at": [1000, 560], "from": {"o": 0, "s": 0.6}, "to": {"s": 3.2, "o": 0, "blur": 10}, "reveal": "circle", "len": 1.8}}`. Which cut fits which product and scene: `references/director.md` §10.
- Use them by name (`"camera": "float-up"`, `"cut": "lift"`), or write the object straight on a scene: `"cut": {"from": {"o": 0, "x": -200}, "reveal": "circle"}`.

### Redrawn UI (illustrative): a product's logic in code
When a flow cannot be recorded (a native engine, licensed data, hardware) and the user agreed, redraw it from the source and mark the scene `"illustrative": true`: the film then shows 界面示意 · Illustrative UI on screen for that scene (`"illustrative_label"` changes the words, never empty), and `check_treatment.py` requires §8 to name it. Start from `templates/ui-sim.example.js` (`CUSTOM.uiSim`: a window drawn from the product's tokens, a cursor that types and clicks, a progress bar, table rows and bars that grow, the true value shown only when a bar lands).
- Take everything from the source: the tokens from its CSS or theme, the labels from its components or i18n files, the flow from its handlers (what is typed, what is clicked, what appears, in what order). Demo values only.
- Simplify, never embellish: leave out what is not needed, but add nothing the product does not do and no result it cannot produce.
- Prefer a real recording (`record_ui.mjs`) or a real capture wherever one is possible; a redrawn scene explains, a real one proves.

### Custom scenes (code)
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
| 场景 | 23 种内置类型 | `{"type": "mg", "layers": […]}` 用 JSON 做 MG 动画，或 `{"type": "custom", "fn": "名字"}` + 你的脚本 |
| 动效语言 | 6 种 | `"motions"`：基于某一种（`"like"`）定义你自己的 |
| 版式、运镜、转场 | 导演的建议 | 每个场景的 `"layout"` / `"camera"` / `"cut"`；film.json 里的关键帧 `"cameras"` / `"cuts"`；或代码里的 `CAMERA.x` / `CUT.x` |
| 视觉 | 8 种风格 | `"css"`：叠加在风格之上的样式表（变量、字体、任意规则） |
| 配色、调色 | 色彩导演、风格 LUT | `"palette"`、`"cinema": {"grade", "grade_strength", …}` |
| 音乐、声音、配音 | 原创配乐、合成音效、Kokoro | 用户的曲子、情绪/BPM/种子、`cinema.sfx`、录音 |
| 审美检查 | 自评分封顶 | 在方案里写 `- Deliberate · 刻意: <检查项> — <理由>`，该项改为提醒 |
| **永远不变** | | 只用真实素材；说法真实有出处；演示数据与 AI 画面要标注；版权；隐私；画面清晰不出错（QA） |

### 不写代码的 MG 动画：`mg` 场景
在 film.json 里设计一段 MG：由图层组成，每个图层的关键帧以**拍**计（从场景开始算），所以每个动作都落在音乐上（示例见上方英文）。
- 图层类型：`text`（`zh`、`en?`、`size?`、`align?`；`*词*` 用强调色）· `rect`（`w`、`h`、`radius?`、`fill?`、`stroke?`）· `circle`（`r`）· `line`（`points`，相对画面中心的像素）· `path`（`d`，1920 × 1080 画面坐标的 SVG 路径）· `number`（`value`、`suffix?`、`zh?`、`en?`、`at`）· `image`（`media`：真实素材，`w`、`radius?`）。
- 关键帧：`[[拍, {x, y, s, sx, sy, rz, o, blur}, "缓动"?], …]`；x/y 是相对中心的像素；缓动 `eio` `eo` `ex` `esoft` `eback` `linear`（可逐帧写，或整层写 `"ease"`）。`draw: [b0, b1]` 让描边在两拍之间自己画出来。
- 颜色：`accent`、`accent2`、`ink`、`muted`、`faint`、`bg`，或任意 CSS 颜色（用风格变量能保持与全片配色一致）。
- 诚实规则不变：`number` 只显示真实数值（不会滚动经过其他数字），并像其他数字一样对照文档检查；`image` 只能用真实素材。

### 不写代码的运镜与转场：关键帧
在 film.json 写 `"cameras"` 与 `"cuts"`（示例见上方英文）：
- 运镜让整个场景在场景时长内从 `from` 运动到 `to`（`x y z` 像素、`s` 缩放、`rx ry rz` 角度）；`pulse` 让每拍有一次轻微的缩放冲击。
- 转场让进入的场景从 `from` 进来（也可用 `o` 不透明度、`blur`、`bright`），离开的场景朝 `to` 离开（默认不动）；`reveal` 以 `left` `right` `up` `down` `circle` `center` 的形状揭开新场景；`len` 是风格交叉淡化时长的倍数（0.4–2）。
- `"at": [x, y]`（画面像素）让运镜或转场围绕该点缩放、旋转，`circle` 揭开也从该点展开：**穿越推进**——推进一个按钮或一处细节，下一幕从那里长出来（示例见上方英文）。哪种转场适合哪种产品和场景：`references/director.md` 第 10 节。
- 按名字使用（`"camera": "float-up"`、`"cut": "lift"`），或直接把对象写在场景上：`"cut": {"from": {"o": 0, "x": -200}, "reveal": "circle"}`。

### 重绘界面（界面示意）：用代码展示产品逻辑
某个流程无法录制（原生引擎、授权数据、硬件）且用户同意时，可以按源码重绘，并给该场景写 `"illustrative": true`：片子会在这个场景的画面上显示“界面示意 · Illustrative UI”（可用 `"illustrative_label"` 改文字，但不能为空），`check_treatment.py` 也会要求方案第 8 节写明。从 `templates/ui-sim.example.js` 开始（`CUSTOM.uiSim`：用产品的设计变量绘制窗口，光标输入和点击，进度条，表格逐行出现，柱子生长，柱子落定后才显示真实数值）。
- 一切取自源码：设计变量取自它的 CSS 或主题，文字取自组件或多语言文件，流程取自事件处理代码（输入什么、点什么、出现什么、什么顺序）。只用演示数据。
- 只简化、不美化：可以省略不需要的部分，但不添加产品做不到的功能，也不展示它产生不了的结果。
- 能录制（`record_ui.mjs`）或截图的地方，优先用真实素材；重绘的场景用来讲解，真实的场景用来证明。

### 自定义场景（代码）
在 film.json 写 `"scripts": ["scenes/mine.js"]`（相对 film.json 的路径），脚本在场景库之后加载。注册场景（`CUSTOM.名字 = (start, end, o) => { scene(...) }`），然后用 `{"type": "custom", "fn": "名字", "bars": 4, "assets": {...}}` 调用。`assets` 里的图片会随片子复制，在脚本里用 `o.assets.xxx` 读取；其他字段都以 `o.*` 传入。可用的 API 与场景库相同（见上方英文与 `templates/engine.js` 开头）。规则：结果只取决于时间（不用定时器、CSS 动画、随机数）；颜色和字体取自风格变量；边距 96 px；只用真实画面。`.webm` 会作为视频播放。完整示例：`templates/custom.example.js`。

### 自定义动效语言
在 `"motions"` 里基于一种内置语言（`"like"`）组合原语并调参数（入场、文字显现、高亮、弹出、镜头、推近时长与缓动），可附带 `"palette"` 告诉导演这种语言能用哪些版式、运镜和转场。设为全片 `"motion"`，或只给某个场景使用。

### 自定义运镜与转场
在脚本里注册 `CAMERA.名字 = ({t, lt, dur, p, beat, bar}) => 'CSS transform'` 和 `CUT['名字'] = ({p, inc}) => ({opacity, transform, filter, clipPath})`（可设 `.len`，≤ 2），然后在场景里写 `"camera"` / `"cut"`。`--stage check` 会识别脚本里注册的名字。

### 自定义视觉
`"css": ["look.css"]` 在风格之后加载，优先级最高：可改变量、字体、字幕带、标签形状等。强调色由 `"palette"` 最后设定；想让 CSS 决定强调色，就删掉 `"palette"`。字体用系统已安装字体，或绝对路径的 `file://`。

### 有意打破审美默认值
审美检查保护的是平均水平。你的片子需要打破某一条时，在方案第 9 节写明：`- Deliberate · 刻意: Rhythm — 连续三个特写：开场是一组微距; Specific — 中段是一段安静的情绪段落`。对应检查就从阻止改为提醒。可写的检查项：One idea、Hook、Specific、Image、Restraint、Rhythm、Hero、ending。诚实类检查不能写进来。
