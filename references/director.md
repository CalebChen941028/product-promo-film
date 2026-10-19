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
| **Camera** | A virtual camera with weight: never static, motivated moves, parallax, speed ramps | the motion language sets entrances and focus moves. On top: a barely-there handheld drift, a small kick on hits, a short focus pull as a scene lands, and 180° motion blur | `motion`; `cinema.motion_blur`; `cinema.lens` |
| **Cuts** | Cut on the beat; motivated transitions (whip pan, push through, match cut); not every cut needs an effect | the style's calm transition almost everywhere. Camera cuts only where the story turns: cinematic = push into the reveal and the hero, kinetic = whip on chapter changes and the hero, playful = whip into the hero | `"cut": "style|whip|push"` per scene |
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
4. **Cuts.** Camera cuts (`whip`/`push`) only where the story turns; the rest stay calm. Never two camera cuts in a row.
5. **Less.** If an effect is noticeable on its own, lower it (`cinema.lens`, `bloom`, `grain`, `sfx_gain_db`). When in doubt, leave it out.
6. **Light.** One accent colour on screen at a time. The brightest thing in the frame is what the narration talks about.
7. **Rhythm.** After a dense feature scene, give the eye a rest: a statement, a numbers beat or a calm clip.
8. **Sound.** No more than one effect per 2 s outside the hero moment. The mix ducks effects under speech automatically; still, don't add a `hit` right where a narration line starts.
9. **Draft first.** `make_film.py film.json --draft`, then look at stills around every cut and hit (`render.mjs stills … t-0.2 t t+0.3`).
10. **Final.** Run without `--draft` (motion blur and grain on). Check the grade on the poster; legibility wins over mood.
11. **Report.** Say which effects are synthetic (sound design, light) and that you could not listen to the mix.

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
| **转场** | 切在拍点上；转场要有动机（甩镜、推进穿越、匹配剪辑）；不是每个切点都要特效 | 绝大多数切点用风格自带的平静转场；只在故事转折处用镜头转场：cinematic 在揭晓和高潮推进穿越，kinetic 在章节切换和高潮甩镜，playful 只在进入高潮时甩镜 | 每个场景的 `"cut"` |
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
4. **转场**：镜头转场（`whip`/`push`）只用在故事转折处，其余保持平静；不要连续两次镜头转场。
5. **做减法**：任何效果如果单独就能被注意到，就调低它（`cinema.lens`、`bloom`、`grain`、`sfx_gain_db`）；拿不准时就不加。
6. **光**：画面上同一时间只有一种强调色；最亮的东西就是旁白正在讲的东西。
7. **节奏**：密集的功能场景之后，给眼睛休息：一句宣言、一个数字场景或一段平静的录屏。
8. **声音**：高潮以外，每 2 秒最多一个音效；混音会自动在人声下压低音效，但仍不要把 `hit` 放在旁白开口的位置。
9. **先草稿**：`make_film.py film.json --draft`，再看每个切点和击点前后的静帧（`render.mjs stills … t-0.2 t t+0.3`）。
10. **终版**：去掉 `--draft` 渲染（开启运动模糊和颗粒），检查封面调色，可读性优先于氛围。
11. **汇报**：说明哪些效果是合成的（音效、光效），并说明你无法试听混音。
