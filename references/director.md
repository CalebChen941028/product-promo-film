# Directing the film · 导演手册

English first, 中文在后。This is the "director's pass": how a top commercial director thinks about colour, camera, light, rhythm and sound. It also covers how this skill turns that into automatic defaults and a few `film.json` knobs.

## English

### 1. What a top promo-film director would use
| Stage | Industry tools | What they get from it |
| --- | --- | --- |
| Pre-production | Figma / FigJam boards, Frame.io animatics, a **colour script** (one swatch per scene) | the film decided before anything moves: one idea, an emotional arc, a hero moment |
| Product shots | Cinema 4D + Redshift/Octane, Blender Cycles, Rotato, Screen Studio | photoreal devices, real reflections and depth, screens that glow like light sources |
| Motion & compositing | After Effects (+ Element 3D, Trapcode Particular, Optical Flares, Deep Glow), Houdini, Unreal Engine; code-driven: Remotion, Motion Canvas, Rive | a virtual camera with a lens: depth of field, motion blur, parallax, flares, particles |
| Edit & colour | DaVinci Resolve (colour page, film emulation such as Dehancer / FilmConvert), Premiere | cuts on the music, a graded look (LUT), grain, halation, bloom, one consistent "print" |
| Sound | Pro Tools / Logic, libraries (Boom, Soundly, Splice), a voice actor, a music editor | whooshes that sell camera moves, impacts on reveals, risers into the drop, the track cut to picture |

The result is a film that feels **photographed, not animated**. Every move is motivated by a lens, light falls on the product, colour tells the story, and you *feel* the sound before you notice it.

**Restraint is the craft.** Top work (Apple, Stripe, Linear, Teenage Engineering) is mostly calm: a neutral grade, slow confident moves, few cuts with effects, and one big moment. Premium means *felt, not seen*. If a viewer can name an effect, it is too strong. This skill's defaults are tuned to sit just under that threshold.

### 2. The eight crafts and what this skill does with each
| Craft | Director's principle | What the skill does automatically | Your knob |
| --- | --- | --- | --- |
| **Story** | One idea; tension → release; a hero moment around 60–70 % of the film; end on the brand | fixed beats (cover → pain → reveal), the planner keeps the brief order, `finale` is the hero | scene order; `"hit": "hero"` to move the hero beat |
| **Colour script** | Colour follows emotion: cold, desaturated "before"; neutral, honest product; saturated peak; warm resolution | moods per scene type: pain = `cold`, numbers/finale = `peak`, endcard = `warm`, else `neutral`. Shifts are small and glide across cuts | `"mood": "cold|neutral|peak|warm|night"` per scene |
| **Grade** | One look for the whole film, chosen for the brand; 60-30-10 colour; one accent | a LUT per style (teal-night, clean-bright, bleach-print, pastel-glow, neon-night, warm-print), blended at 50 % so UI stays true and legible | `cinema.grade`, `cinema.grade_strength` |
| **Camera** | A virtual camera with weight: never static, motivated moves, parallax, speed ramps | the motion language sets entrances and focus moves; the shot plan (§6) gives each scene its own move (push, pull, pan, crane, arc, dolly zoom, handheld…). On top: a small kick on hits, a short focus pull as a scene lands, and 180° motion blur | `motion`; `"camera"` per scene; `cinema.motion_blur`; `cinema.lens` |
| **Cuts** | Cut on the beat; motivated transitions (whip pan, push through, match cut); not every cut needs an effect | the style's calm transition inside a chapter; the shot plan (§6) puts a designed cut where the story turns: chapter openings, out of the pain, into a breath, into the hero | `"cut"` per scene (§6) |
| **Light** | The product is the light source; glints on glass; rays and flares on reveals; bloom and halation | a soft glint crosses each window once, faint rays behind the cover logo and the hero tagline, one anamorphic flare on the hero moment only, gentle bloom in the finish. Light leaks and bokeh are off unless you ask (`lens.leak`, `lens.bokeh`) | `cinema.bloom`; `cinema.lens.flare/glint/leak/bokeh` |
| **Sound design** | About five layers: music, voice, transitions (whoosh), impacts, UI foley; restraint, with a sound only where the picture moves | synthesised cues (no samples, no licences), mixed low under the music: a sound only on camera cuts and hits, one impact + riser for the hero moment, a soft shimmer or chime on the logo, ticks on counters. About 10 cues a minute. The palette follows the motion language | `cinema.sfx`, `cinema.sfx_gain_db` |
| **Finish** | Real motion blur, fine grain, a print-like grade: nothing looks "computer clean" | motion blur (4 samples, 180° shutter), fine luma grain, LUT and bloom in one finishing pass, plus the same grade on the poster | `cinema.grain`, `--draft` for quick looks |

### 3. The palettes by theme (chosen with the motion language)
| Motion language | Lens | Cuts | Sound palette |
| --- | --- | --- | --- |
| `cinematic-3d` | slight handheld, edge DOF, short focus pull, glints, hero flare | push into reveal + hero | whoosh · impact · riser · shimmer · tick |
| `precision-data` | locked-off camera, no DOF, faint glints, no flare | style (clean) | paper swish · soft thud · chime · tick |
| `kinetic-launch` | quicker handheld, firmer kick, hero flare | whip on chapters + hero | whip · impact · riser · shimmer · tick |
| `gentle-story` | slow floating camera, soft focus pull, faint hero flare | style (dissolve) | airy swell · chime |
| `playful-pop` | light sway, hero flare | whip into hero | whip · thud · shimmer · pop |
| `editorial-type` | locked-off, no light effects | style (hard) | paper · thud · chime · type |

### 4. What still needs a human studio (be honest with the user)
- Photoreal 3D device renders, particles and fluids need Blender, C4D or Houdini. If the user has such renders, put them in as `clip` scenes (WebM).
- Live-action footage, an original score, and a professional voice actor's performance.
- Fine colour work on real camera footage.

The skill reaches "premium motion-design commercial" quality from screenshots alone. It does not pretend to be a live-action shoot.

### 5. The director's pass (do this before `--stage render`)
1. **One idea.** Write the film's single sentence. Every scene must serve it; cut the rest.
2. **Arc.** Check the moods read cold → neutral → peak → warm. Add `"mood"` only to break the default deliberately.
3. **Hero moment.** Exactly one biggest beat (usually `finale`; move it with `"hit": "hero"`) at about 60–70 % of the runtime. Other hits: at most one per 20 s.
4. **Shots and cuts.** Read the shot plan that `--stage check` prints (§6). Designed cuts sit where the story turns; the rest stay calm. No layout, move or designed cut twice in a row. Override a scene only on purpose.
5. **Less.** If an effect is noticeable on its own, lower it (`cinema.lens`, `bloom`, `grain`, `sfx_gain_db`). When in doubt, leave it out.
6. **Light.** One accent colour on screen at a time. The brightest thing in the frame is what the narration talks about.
7. **Rhythm.** After a dense feature scene, give the eye a rest: a statement, a numbers beat or a calm clip.
8. **Sound.** No more than one effect per 2 s outside the hero moment. The mix ducks effects under speech automatically; still, don't add a `hit` right where a narration line starts.
9. **Draft first.** `make_film.py film.json --draft`, then look at stills around every cut and hit (`render.mjs stills … t-0.2 t t+0.3`).
10. **Final.** Run without `--draft` (motion blur and grain on). Check the grade on the poster; legibility wins over mood.
11. **Report.** Say which effects are synthetic (sound design, light) and that you could not listen to the mix.

### 6. Shot grammar: a frame, a move and a cut for every scene
Short-film and title-design craft, built in (each implemented from scratch in `templates/engine.js`, `patterns.js` and `library.js`):

| Device | What it does on screen | Where the director uses it |
| --- | --- | --- |
| **Layouts** (`layout`) | feature: `center` (3D window), `split` / `split-r` (window + numbered list, leader lines), `full` (full-bleed + headline cards), `soft` (one line at a time), `stickers`, `editorial` (giant index) · photo: `left` `right` `bottom` `center` (full-bleed + scrim) or `split` (framed photo + clean text side) · gallery: `coverflow` `grid` `strip` · carousel: `menu` `stack` (a deck) · detail: `macro` or `split` (the whole image with a box + the region magnified) | a dense screen with 3+ points → a list layout; a chart or a photo → a full frame; never the same layout twice in a row |
| **Camera moves** (`camera`) | `push` / `pull` (5 % in or out), `pan-l` / `pan-r` (lateral 70 px), `crane` (rise), `tilt`, `arc` (a slow orbit step), `vertigo` (dolly zoom: the frame pushes while depth flattens), `handheld` (a slow breathing float), `reveal` (starts close and high, settles onto the whole), plus the languages' `orbit` `punch` `dolly` `sway` | lateral moves alternate direction; photos breathe handheld in the softer languages; statements push in |
| **Cuts** (`cut`) | `whip` (pan + motion blur), `push` (through the frame), `slide-up`, `wipe` (a hard edge), `iris` (a circle opens), `zoom` (settles from 125 %), `blur` (defocus dissolve), `rack` (focus pulls from one scene to the next), `doors` (split open from the centre), `light` (a light leak carries the change), `dip` (a breath through the background) | chapter openings take a designed cut; the way out of the pain takes a push; a breath (statement) takes a dip, blur or light; the hero takes the language's signature cut; inside a chapter the style's calm transition |
| **Motion language per scene** (`motion`) | one scene borrows another language's entrances, text reveals and focus speed | rarely, on purpose: a `gentle-story` breath inside a `precision-data` film |

**How the director chooses** (`make_film.py` → `plan_shots`, printed as a shot plan by `--stage check` and `build`):
1. The film's motion language owns a **palette**: its signature layout, move and cut first, then variations that keep its grammar (precision-data never orbits; gentle-story never whips).
2. **Content fit**: what the scene holds picks the frame (points with highlight boxes, charts, photos, labelled crops).
3. **Rhythm**: the least-used option wins ties, the last one is never repeated, and only a share of cuts are designed (restraint).
4. **Your word wins**: `"layout"`, `"camera"`, `"cut"` or `"motion"` on a scene overrides the plan; `"direction": {"variety": "calm" | "balanced" | "rich"}` sets how far the plan strays from the signature (default balanced).

### 7. Code-drawn animation: story glue between the materials
Some beats are better drawn than shown. The scene library draws them in code, in the film's style and motion language — never a fake product UI, only diagrams, type and real numbers:
| Scene | Story job | Where autofilm puts it |
| --- | --- | --- |
| `flow` | the journey at a glance: what the user brings → what they leave with | a chaptered software tour: right after the opening, built from the chapter names (`"steps": "chapters"`); a human-story film: the person's day or journey in three moments |
| `hub` | the turn: many scattered chores become one place | a problem-solution film with a pain beat: right after the pain, naming the same chores |
| `type` | a truth said as words that rise on the beat | a sensory, reveal or human-story film: the one-line breath becomes two lines of kinetic type, the second turning on one `*word*` |
| `chart` | a real trend or comparison, drawn | never automatic: add it when the user's docs hold a series of real numbers (values are gated like every number) |

Real footage is material, not glue: `footage` scenes (and a `.webm` cover, photo or hero) play the clip from its best moment, which `scripts/footage.py` finds (sharp, exposed, moving but not shaking; a glitchy stretch scores low).

### 8. Colour: psychology, brand and harmony (`scripts/palette.py`)
The style sets the ground (background, ink, type); the colour director sets the voice (the accent, about 10 % of every frame).
1. **Brand first.** A brand colour (`brand_color` in brief.json, or the most vivid colour of the logo) is the accent, tuned only in lightness for legibility.
2. **Colour psychology by product type.** Medicine and science: teal and blue (trust, calm precision), never a red accent (alarm). Finance: deep green (growth), navy (trust), gold (value); not red (loss). Food: amber, tomato, olive (appetite, warmth, freshness); never blue or purple (they suppress appetite). Luxury and beauty: muted gold, blush, oxblood; not clinical greens and cyans. Health and wellness: sage, soft teal, peach (calm, care). Kids: tangerine, sky, leaf, soft and never neon. Industry and mobility: safety orange, steel blue. Hospitality and living: terracotta, sand, lake blue, forest. Developer and AI: violet, cyan, a spark of lime. Games and events: magenta, electric blue, acid green.
3. **Harmony with the pictures**, which fill most of every frame: an accent that echoes their dominant hue (analogous) for calm products, one that stands against it (near-complementary) for lively ones; never the clashing band 60–120° away. Neutral pictures (UI greys) leave the accent as the only colour voice.
4. **Taste and legibility.** Clear and bright on dark grounds; on light grounds the lightest tone that still reaches 3:1 (vivid, not muddy); muted for luxury, editorial and paper styles. The second accent comes from the same genre palette, analogous for calm products and split-complementary for lively ones.
5. **60-30-10 and one accent per frame**: ground 60, ink 30, accent 10. `--stage check` warns when an accent falls under 3:1 contrast.

### 9. The look: chosen from the materials, never a default (`scripts/look.py`)
Nothing picks a style by product type alone. `look.py` reads every picture (screen or photo, light or dark UI, saturation, information density, charts, the warmth of the dominant hue), weighs it with the product's character and the docs' tone words, and scores all 8 styles, writing the reasons into `treatment.md` §5. The user's own words for the feel (`autofilm.py --mood "大气 商业 科技感"`) count triple. A tie is settled by evidence (a dense white UI pops on a dark ground, a sparse one blends with a bright ground). The motion follows the look; a dense data UI gets `precision-data` instead of 3D drift. The crew confirms or changes `"style"` / `"motion"` in film.json and says why, so two films of one category look alike only when their materials and mood do. The thresholds are judgement calls: when a pick feels wrong for a product, change the film and say so in §5.

## 中文

### 1. 顶级宣传片导演会用什么
| 阶段 | 行业工具 | 得到什么 |
| --- | --- | --- |
| 前期 | Figma / FigJam 分镜、Frame.io 动态分镜、**色彩脚本**（每场一个色块） | 动手前就定好：一个核心概念、情绪弧线、高潮时刻 |
| 产品镜头 | Cinema 4D + Redshift/Octane、Blender Cycles、Rotato、Screen Studio | 照片级设备、真实反射与景深、像光源一样发光的屏幕 |
| 动效与合成 | After Effects（Element 3D、Trapcode Particular、Optical Flares、Deep Glow）、Houdini、Unreal；代码驱动：Remotion、Motion Canvas、Rive | 带镜头特性的虚拟摄影机：景深、运动模糊、视差、光晕、粒子 |
| 剪辑与调色 | DaVinci Resolve（调色页、Dehancer / FilmConvert 胶片模拟）、Premiere | 按音乐剪辑、统一调色（LUT）、颗粒、光晕溢出、辉光 |
| 声音 | Pro Tools / Logic、音效库（Boom、Soundly、Splice）、配音演员、音乐剪辑师 | 呼啸声托起运镜、重击声托起揭晓、上升音推向高潮、音乐贴着画面剪 |

结果是一部**像“拍”出来而不是“做”出来**的片子：每个运动都有镜头逻辑，光落在产品上，色彩讲故事，声音先于意识被感受到。

**克制本身就是功力。** 顶级作品（Apple、Stripe、Linear、Teenage Engineering）大多是安静的：中性的调色、缓慢而笃定的运镜、很少的特效转场、只有一个高潮。高级感是“感受得到，看不出来”；观众能叫出名字的效果就是太重了。本 skill 的默认值就调在这条线之下。

### 2. 八项手艺，以及本 skill 怎么做
| 手艺 | 导演原则 | 本 skill 自动完成 | 可调参数 |
| --- | --- | --- | --- |
| **叙事** | 一个核心概念；紧张 → 释放；高潮在全片 60–70% 处；以品牌收尾 | 固定开场（封面 → 痛点 → 揭晓），规划器保持 brief 顺序，`finale` 即高潮 | 场景顺序；用 `"hit": "hero"` 指定高潮场景 |
| **色彩脚本** | 色彩跟随情绪：冷而灰的“过去”，中性真实的产品，饱和的高潮，温暖的收尾 | 按场景类型自动设定情绪：痛点 `cold`，数字和高潮 `peak`，结尾 `warm`，其余 `neutral`；变化幅度小，跨切点平滑过渡 | 每个场景的 `"mood"` |
| **调色** | 全片一个统一的“胶片”，贴合品牌；60-30-10 配色；一个强调色 | 每种风格一个 LUT（teal-night、clean-bright、bleach-print、pastel-glow、neon-night、warm-print），按 50% 强度混合，保证界面色彩真实可读 | `cinema.grade`、`cinema.grade_strength` |
| **运镜** | 有重量的虚拟摄影机：不静止、有动机、有视差、有变速 | 动效语言决定入场与聚焦；再叠加几乎察觉不到的手持漂移、击点时的轻微冲击、场景落定时的短暂对焦、180° 运动模糊 | `motion`、`cinema.motion_blur`、`cinema.lens` |
| **转场** | 切在拍点上；转场要有动机（甩镜、推进穿越、匹配剪辑）；不是每个切点都要特效 | 章节内用风格自带的平静转场；镜头表（第 6 节）在故事转折处放设计过的转场：章节开头、走出痛点、喘口气、进入高潮：cinematic 在揭晓和高潮推进穿越，kinetic 在章节切换和高潮甩镜，playful 只在进入高潮时甩镜 | 每个场景的 `"cut"` |
| **光** | 产品就是光源；玻璃上的高光；揭晓时的光芒与镜头光晕；辉光与光晕溢出 | 每个窗口扫过一次柔和高光、封面 Logo 与高潮口号后有淡淡光芒、只在高潮出现一次宽银幕光晕、成片加轻微辉光；漏光和光斑默认关闭（需要时用 `lens.leak`、`lens.bokeh` 打开） | `cinema.bloom`、`cinema.lens` |
| **声音设计** | 约五层：音乐、人声、转场呼啸、重击、界面音效；克制，画面动才有声 | 用合成音效（无采样、无版权问题），压在音乐之下：只在镜头转场和击点有声音，高潮有一次重击加上升音，Logo 处有轻柔的闪光音或钟声，数字有轻点声；约每分钟 10 个音效；音色随动效语言变化 | `cinema.sfx`、`cinema.sfx_gain_db` |
| **成片质感** | 真实运动模糊、细颗粒、胶片般的调色，不要“电脑味” | 运动模糊（每帧 4 次采样，180° 快门）、细腻的亮度颗粒、LUT 与辉光一次完成，封面同样调色 | `cinema.grain`；`--draft` 快速预览 |

### 3. 按主题的组合
各动效语言对应的镜头、转场和音色，见上方英文第 3 节的表格。简要说：cinematic 稳重电影感；precision 冷静精确、几乎无特效；kinetic 利落有力；gentle 柔和温暖；playful 轻快；editorial 干净硬朗。所有组合都以克制为前提。

### 4. 仍然需要专业团队的部分（要对用户说清楚）
- 照片级 3D 设备渲染、粒子和流体需要 Blender、C4D 或 Houdini；若用户已有渲染，可作为 `clip` 场景（WebM）放入。
- 实拍、原创配乐、专业配音演员的表演。
- 针对实拍素材的精细调色。

本 skill 用截图即可做到“高端动效广告片”水准，但不冒充实拍大片。

### 5. 导演检查（`--stage render` 之前执行）
1. **一个概念**：写出全片的一句话，每个场景都要为它服务，多余的删掉。
2. **弧线**：确认情绪是冷 → 中性 → 高潮 → 温暖；只有在刻意打破默认时才加 `"mood"`。
3. **高潮**：只有一个最大的拍点（通常是 `finale`，可用 `"hit": "hero"` 改到别的场景），位于全片 60–70% 处；其他击点每 20 秒最多一个。
4. **镜头与转场**：看 `--stage check` 打印的镜头表（第 6 节）。设计过的转场放在故事转折处，其余保持平静；版式、运镜、设计转场都不连续重复。只有刻意为之才逐场景覆盖。
5. **做减法**：任何效果如果单独就能被注意到，就调低它（`cinema.lens`、`bloom`、`grain`、`sfx_gain_db`）；拿不准时就不加。
6. **光**：画面上同一时间只有一种强调色；最亮的东西就是旁白正在讲的东西。
7. **节奏**：密集的功能场景之后，给眼睛休息：一句宣言、一个数字场景或一段平静的录屏。
8. **声音**：高潮以外，每 2 秒最多一个音效；混音会自动在人声下压低音效，但仍不要把 `hit` 放在旁白开口的位置。
9. **先草稿**：`make_film.py film.json --draft`，再看每个切点和击点前后的静帧（`render.mjs stills … t-0.2 t t+0.3`）。
10. **终版**：去掉 `--draft` 渲染（开启运动模糊和颗粒），检查封面调色，可读性优先于氛围。
11. **汇报**：说明哪些效果是合成的（音效、光效），并说明你无法试听混音。

### 6. 镜头语法：每个场景各有自己的版式、运镜与转场
吸收了短片与片头设计中常用的手法（全部在 `templates/engine.js`、`patterns.js`、`library.js` 中自行实现，未搬运第三方代码）：

| 手法 | 画面效果 | 导演怎么用 |
| --- | --- | --- |
| **版式**（`layout`） | 功能：`center`（3D 窗口居中）、`split` / `split-r`（窗口 + 编号列表 + 引线，左右镜像）、`full`（满幅 + 标题卡）、`soft`（一次一句）、`stickers`（贴纸气泡）、`editorial`（巨型编号）· 照片：`left` `right` `bottom` `center`（满幅 + 渐变遮罩）或 `split`（照片卡片 + 留白文字）· 画廊：`coverflow` `grid` `strip` · 轮播：`menu` `stack`（叠卡）· 细节：`macro` 或 `split`（左边全图带框、右边局部放大） | 要点多、截图密 → 列表版式；图表、照片 → 满幅；同一版式不连续出现 |
| **运镜**（`camera`） | `push` / `pull`（推近 / 拉远 5%）、`pan-l` / `pan-r`（横移 70 px）、`crane`（升）、`tilt`（俯仰）、`arc`（缓慢环绕一步）、`vertigo`（希区柯克变焦：推近同时纵深变平）、`handheld`（缓慢的手持呼吸感）、`reveal`（从近处高处落到全景），以及各动效语言自带的 `orbit` `punch` `dolly` `sway` | 横移左右交替；柔和的语言里照片带手持呼吸；宣言句缓推 |
| **转场**（`cut`） | `whip`（甩镜 + 运动模糊）、`push`（穿过画面）、`slide-up`（上滑）、`wipe`（硬边擦除）、`iris`（圆形展开）、`zoom`（从 125% 落定）、`blur`（虚焦叠化）、`rack`（焦点从上一场转到下一场）、`doors`（从中缝向两侧打开）、`light`（漏光带过）、`dip`（经背景过渡，一口气） | 章节开头用设计过的转场；走出痛点用 push；宣言句用 dip / blur / light；高潮用该语言的招牌转场；章节内用风格自带的平静转场 |
| **场景级动效语言**（`motion`） | 单个场景借用另一种语言的入场、文字和推近节奏 | 少用、刻意用：比如在 precision-data 片子里插一拍 gentle-story 的“喘口气” |

**导演如何选择**（`make_film.py` 的 `plan_shots`；`--stage check` 和 `build` 都会打印镜头表）：
1. 全片动效语言有一套**调色板**：招牌版式、运镜、转场排第一，其后是不破坏语法的变化（precision-data 不环绕，gentle-story 不甩镜）。
2. **按内容匹配**：场景里有什么（带高亮框的要点、图表、照片、带标签的裁切）决定画面。
3. **按节奏**：用得最少的优先，上一个绝不重复，只有一部分转场是设计过的（克制）。
4. **人工优先**：场景上写了 `"layout"`、`"camera"`、`"cut"`、`"motion"` 就以它为准；`"direction": {"variety": "calm" | "balanced" | "rich"}` 决定偏离招牌风格的程度（默认 balanced）。

### 7. 代码动画：素材之间的叙事衔接
有些拍点画出来比拍出来更好。场景库用代码按本片的风格和动效语言绘制它们：只画示意图、文字和真实数字，绝不伪造产品界面。
| 场景 | 叙事作用 | autofilm 放在哪里 |
| --- | --- | --- |
| `flow` | 一眼看全旅程：用户带来什么 → 带走什么 | 分章节的软件巡礼：开场之后，用章节名自动生成（`"steps": "chapters"`）；人物故事：用三个时刻讲他的一天或一段旅程 |
| `hub` | 转折：散落的事务汇成一处 | 有痛点拍点的问题-解决叙事：紧接痛点之后，点名同样的那几件事 |
| `type` | 用随节拍升起的文字说出真相 | 感官、揭示、人物故事叙事：一句“喘口气”变成两行动态文字，第二行落在一个 `*词*` 上 |
| `chart` | 把真实的趋势或对比画出来 | 不会自动添加：用户文档里有一组真实数字时再加（数值和所有数字一样要过门禁） |

真实视频是素材，不是衔接：`footage` 场景（以及 `.webm` 作为封面、照片或揭晓）从片段中最好的时刻开始播放，由 `scripts/footage.py` 挑选（清晰、曝光正常、有动作但不抖；有故障闪烁的片段得分低）。

### 8. 色彩：心理、品牌与和谐（`scripts/palette.py`）
风格决定底色（背景、文字、字体），色彩导演决定“声音”：强调色，约占每帧的 10%。
1. **品牌优先**：品牌色（brief.json 的 `brand_color`，或 Logo 中最鲜明的颜色）就是强调色，只为可读性调整明度。
2. **按产品类型的色彩心理**：医疗与科研用青、蓝（信任、冷静、精确），强调色不用红（警报感）；金融用深绿（增长）、藏蓝（信任）、金（价值），不用红（亏损）；食品用琥珀、番茄红、橄榄（食欲、温暖、新鲜），不用蓝紫（抑制食欲）；奢侈与美妆用低饱和金、蜜粉、酒红，不用偏医疗感的青绿；健康与身心用鼠尾草绿、柔和青、蜜桃色（安抚、关怀）；儿童用橘、天蓝、嫩叶绿，柔和不刺眼；工业与出行用安全橙、钢蓝；酒店与居家用陶土红、沙色、湖蓝、森林绿；开发者与 AI 用紫、青，加一点亮绿；游戏与活动用洋红、电光蓝、荧光绿。
3. **与画面和谐**（画面占据每帧的大部分）：沉稳的产品让强调色呼应画面主色（邻近色），有活力的产品让它与主色对立（近互补色），避开相差 60–120° 的冲突区；画面以中性灰为主（界面）时，强调色就是唯一的色彩声音。
4. **品味与可读**：深色底上清亮；浅色底上取仍达到 3:1 的最浅色调（鲜明而不浑浊）；奢侈、编辑、纸质风格整体降饱和。第二强调色取自同一类型的色板：沉稳产品用邻近色，有活力的产品用分裂互补色。
5. **60-30-10，每帧一个强调色**：底色 60、文字 30、强调色 10。强调色对比度低于 3:1 时，`--stage check` 会警告。

### 9. 视觉风格：由素材决定，没有默认值（`scripts/look.py`）
没有任何环节只凭产品类型就选风格。`look.py` 读懂每张图（截图还是照片、浅色还是深色界面、饱和度、信息密度、是否图表、主色冷暖），结合产品特点与文档语气，给 8 种风格逐一打分，并把理由写进 `treatment.md` 第 5 节。用户自己描述风格的用词（`autofilm.py --mood "大气 商业 科技感"`）权重三倍。平局由证据决定（文字密的白色界面在深色底上最醒目，界面稀疏则与明亮底融合）。动效跟着风格走；信息密集的数据界面用 `precision-data`，不用 3D 漂移。团队在 film.json 的 `"style"` / `"motion"` 里确认或修改并写明理由，所以只有素材与气质真的相近时，同类产品的片子才会长得像。阈值是经验判断：某个选择不适合这款产品时，改片子并在第 5 节写明。
