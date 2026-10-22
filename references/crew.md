# The crew · 制作团队

English first, 中文在后。A top film is made by a team, so play each role in turn. Each role writes its own section of `treatment.md` (from `templates/treatment.template.md`; `autofilm.py` pre-fills the facts). The **design critic** then scores the result. Build only when `python3 scripts/check_treatment.py treatment.md film.json` passes.

## English

### Latitude
Every rule below is the craft's default, written for the average film. A role may break one when the film is better for it: say what and why in the treatment (§9 `- Deliberate · 刻意: <check> — <why>`), and the matching check advises instead of blocking. The brand guardian's rules are the exception: truth, sources, qualifiers, rights and legibility never bend. Roles may also go beyond the library — their own scenes, motion, moves, cuts and look (`references/custom-scenes.md`).

### How to run the crew
1. Read the facts (§0 of the treatment), the materials (look at the images if you can) and the brief. Then study the golden film for your arc (`templates/golden/<arc>.json`, named in §0) and `references/copy-bank.md`: they show what each role's output looks like at the top level.
2. Play the roles **in order**, one at a time. Write only that role's section, and stay inside its job.
3. Then play the **design critic**. Score honestly. If the average is < 4 or any score is < 3, go back to the weakest role **you can change** and redo that part (a sharper hook, a calm beat, a callback ending, a better image for the hero), then re-score. Up to three rounds. Never inflate a score, and never stop at the gate: a limit of the materials (placeholders, few photos) goes in §1 Gaps and in the report, not in a score.
   - **Image quality & choice** scores what the crew controls: which image carries each beat, the crop, the order, the hero image saved for the hero. Drawn placeholders chosen and staged well can score 4; a weak image chosen when a better one was in the folder cannot.
4. The copywriter copies the final words into `film.json` and replaces every `TODO`. Run `lint_copy.py`.
5. The editor checks bars and beats in `film.json` against the rhythm map. Then `make_film.py --stage check`.

### 1. Producer: is this possible and allowed?
- **Job:** audience, channel (sound on? vertical cut later?), length, materials, rights.
- **Rules:**
  - Only real product images.
  - Music is the user's track or composed by `make_music.py`.
  - Quotes must be real and approved.
  - Missing material is solved by a different beat, not by faking it.
- **Shot wishlist:** autofilm writes `shot_wishlist.md`: the shots that would lift this film most (size, content, light, camera specs) for the user or a real crew to shoot, and draft prompts for AI-generated mood shots. AI imagery is only ever atmosphere, labelled as such; it never stands in for the product, its screens or its results.

### 2. Strategist: what is true, and what matters?
- **Job:** the audience truth, the insight (the tension), the *single-minded proposition* (one sentence), and the proof.
- **Good:** "Researchers lose a week per paper to formatting tables." **Bad:** "Researchers want efficiency."
- The proposition must be **specific, true, and about the audience's life**, not about the product's features.
- **Audience:** who exactly (role, situation), what they use today instead (the real competitor is often a habit: a spreadsheet, five tools, doing nothing), and the one doubt that stops them. The film answers that doubt once, with proof.
- **USP → proof beat:** at most three selling points; for each, what makes it different from the alternative, and the scene and image that prove it. A selling point no image can prove is cut, or said only in the voice with a source.
- **AIDA, honestly:** Attention = the hook in 3 s; Interest = the problem or the reveal; Desire = the proof and the hero (the viewer sees themselves with it); Action = one true next step on the end card. Persuade with true social proof (real quotes, real numbers) and clarity, never with fake scarcity, fake urgency or invented testimonials.

### 3. Creative director: the idea people remember
- **Job:** three *different* concepts (not three wordings of one). Choose the one that is the most surprising **and** the most true. Write the hook (0–3 s) and the hero moment. Then write the **three anchor lines** — hook line (cover), hero line (finale), last line (end card) — each saying the chosen concept in a different way, the last one a callback to the first. A concept that does not reach these three lines is not chosen; it is decoration.
- **Hook patterns that work:**
  - **macro detail:** texture before the whole;
  - **contrast cut:** old vs new in one cut;
  - **a bold true number;**
  - **silence + one word;**
  - **a human moment:** hands, a face, a place;
  - **a question the audience has asked themselves.**
- **Resonance devices:**
  - one specific truth instead of five claims;
  - a callback (the end echoes the opening image);
  - the rule of three;
  - a held pause before the hero;
  - ending on the audience ("for the questions that matter"), not on the product.
- **Reject:** "fast, easy, powerful" concepts; anything that could be any brand's ad.

### 4. Copywriter: fewer, truer words
- **Job:** the tagline (zh ≤ 12 字, en ≤ 8 words; format `中文 / English`), the full script — one bullet per scene in film order (`- cover → "line"`; a silent scene says why) — and every on-screen word. film.json's lines are copied from this script, never written somewhere else.
- **Rules:**
  - Verbs and nouns, not adjectives.
  - Every proof line (feature, hero, numbers…) carries one fact from the docs: a number, a material, a place, a feature by name. Say what it means for the viewer; never read a spec list aloud (`lint_copy` flags attribute lists, runs of units and 3+ short items; the copy score is capped).
  - Numbers only if checkable.
  - Never repeat on screen what the voice says.
  - Spoken English runs at about 2.5 words per second.
  - Chinese captions are natural Chinese, not a translation of the English.
- **Banned:** see `scripts/lint_copy.py` (revolutionary, seamless, next-gen, 颠覆, 赋能, 极致, 一站式 …), exclamation marks and unprovable superlatives.
- **Call to action:** one true next step the docs support (join the beta, download, book a table), zh ≤ 8 字 / en ≤ 4 words, in `brand.cta` — the end card shows it last, as a button. No CTA the product cannot honour; "none" is a fine answer. The last spoken line stays the callback, not the CTA.

### 5. Art director & colorist: the high-taste designer
- **Job:** confirm the look (style) and the palette the colour director chose (`film.json` "palette", treatment §5; `references/director.md` §8), choose the best image for every beat, and keep the best one for the hero.
- **As colorist:** the grade's temperature follows the palette (warm products warm, clinical and tech cool), at a strength that keeps real UI and product colours true; one look for the whole film; the colour script moves only slightly (cold before, honest product, a richer peak, a warm close).
- **Taste rules:**
  - **One focal point per frame.** If two things compete, cut one.
  - **One accent colour.** Everything else is neutral. The brightest thing on screen is what the voice is talking about.
  - **Two typefaces at most** (the style sets them). Never add a third.
  - **Whitespace is a feature.** Margins ≥ 96 px. Text never touches an image edge.
  - **Real over decorative.** A real product photo beats any illustration. A real UI beats any mock-up.
  - **No clichés:** globes, handshakes, light bulbs, stock smiles, floating icons, fake dashboards.
- **Style choice by product:** `references/styles.md` and `genres.py`. Photos go in `photo` / `detail` / `hero` scenes. Cut-outs (transparent PNG) go in `hero` / `lineup`. Screens go in `feature` / `carousel` / `phone`.
- **Full bleed beats a card.** A photograph carries its beat full-frame (`photo`, a one-photo `hero`) with one line; a card with a list of specs reads as a slide. Keep ≤ 2 points on any card, and only points that serve the idea.
- **The cold open needs a subject:** the cover image plays full-frame for the first seconds, so give it a place, a person or the product in use, never a texture.
- **Two beats in the cold open.** A photo cover gets a `focus` on its subject (`python3 scripts/subject_grid.py <photo> --preview .`, then `--cells`): the film opens on that detail and pulls back to the place. One still frame for 6 s reads as a slide; `check_treatment` caps the hook at 3 without it.
- **Name what is in the frame.** In §5 write one line per image (place and subject). The copy over an image names the same kind of place: no "room" over a tent. `check_treatment` blocks indoor words over an outdoor image and the reverse.
- **The hook before the name.** The first ~5 s are the product truth (the image and the hook line); the logo comes after, or only at the hero and end card (`"name": false`).
- **Readable screens.** At film scale, UI text must land at ≥ 18 px: a whole dense screen is shown for under a second, then the beat zooms to the region the line is about (a rect per point; carousel panels get a `crop`; a screen cover gets a `focus`). `check` warns when text would be smaller.
- **The hero pays off the hook.** It is the hook's image transformed (the same screen, now with the answer resolved out of it; the same photo, now whole and lit) or the hook's words answered. One move on the downbeat after the half-beat of silence, ~3 s alone, then the name. `check_treatment` caps "hero" at 3 without a callback.
- **The hero is a real output.** Screen-led films end on the work, done: one result screen (`"hero": "result"`), the one figure or report that matters rising out of the UI (`"rise"`), or a calm stack of outputs (`"stack"`). Photo-led films return to the cover photo (`"image"`). The tilted wall is a fallback, not a hero.
- **A texture has a purpose:** a silent detail beat needs a line or labelled crops; otherwise cut it.

### 6. Director & DP, motion designer & editor: frame, movement, rhythm
- **Job:** read the storyboard the director designed (`treatment.md` §6: size, layout, camera, cut and the reason per scene) and keep or change it on purpose; the motion language (by theme); the rhythm.
- **As director & DP (shot sizes, 景别):** the open moves close → wide (a detail, then the place) or wide → close on purpose; a chapter goes wide → medium → close (the whole tool, the panel, the number); never three shots of the same size in a row; the hero is the closest, cleanest frame of the film. Camera moves are motivated (a push toward what the voice names, a lateral drift with the slides), small, and never fight a zoom already inside the frame.
- **Montage:** cut on the bar; a match cut when two scenes share a shape or an image (the hero returning to the hook's screen is the strongest one); a breath after two dense beats.
- **As motion designer:** code-drawn glue (journey map, many-into-one, kinetic type, real-number charts; `references/director.md` §7) only where the story needs a picture the materials do not have.
- Camera cuts only where the story turns. There is exactly one hero moment, around 60–70 % of the film.
- **Breathing:** after two dense beats, one calm beat. The first 3 s and the last 5 s are the most watched; make them perfect.
- **Vary the proof.** Two proof beats in a row never share a shape: follow a feature with a zoomed detail, one number, a clip, a before → after, or a breath. A phone or clip scene earns its place with a line that serves the idea, or it is cut.
- **No dead holds:** a calm beat is short. A silent texture lasts 2 bars, a one-image reveal 3; anything held longer on one still image reads as empty (`check` warns).

### 7. Composer & sound designer: what we feel
- **Job:** the music (the user's track, or a composed mood + BPM that matches the genre), where it builds, the half-beat silence before the hero, and the sound palette. Keep the sound low: felt, not heard.
- Composed moods: `python3 scripts/make_music.py --list`.

### 8. Brand guardian: nothing false, nothing unreadable
- **Job:** check every claim against a source.
- **Qualifiers:** when the docs limit a claim (Pro or paid edition, beta or preview, one platform, some regions, "planned" or "coming soon"), the scene that makes the claim must say the limit: in the line, the caption or a chip. An omitted qualifier is a false claim even when every word is true. `check_treatment.py` blocks the build on one; list them in §8 Qualifiers.
- **Numbers:** a number on screen is the true value from the docs. Never show a count-up frame that reads as another number (the `numbers` scene reveals the real value by default).
- Check rights for music, photos, logos and quotes.
- Captions must always be readable, and nothing important may sit under them.
- **Sign-off** is required before the build.

### 9. Design critic: the taste review
Score each criterion 1–5. `check_treatment.py` cross-checks the scores against the film and caps what it can measure: specific copy (share of lines with a fact), one idea (the concept reaches the copy), image choice (one image per beat, highlight boxes on screens), rhythm (no three identical beats in a row), restraint (one hero) and the ending (a callback, not logistics). A score above its cap fails the build. Fix the film; never the score.

| Criterion | 1 | 3 | 5 |
| --- | --- | --- | --- |
| One idea | a list of features | a theme | one sentence everyone repeats |
| Hook in 3 s | a logo fade-in | a nice shot | you cannot look away |
| Specific, true copy | slogans | clear | a line you'd quote |
| Image quality & choice | random screens | relevant | every frame could be a poster |
| Restraint | effects everywhere | mostly calm | nothing extra, nothing missing |
| Rhythm | monotone | follows the music | breathes with it |
| Hero moment | none | a big moment | a moment you remember the next day |
| Memorable ending | contact sheet | clean end card | the line and the image stay with you |

## 中文

### 自由度
下面每条规则都是行业默认做法，是为一般水平的片子写的。某个角色认为打破某条能让片子更好时，可以打破：在方案里写明打破了什么、为什么（第 9 节 `- Deliberate · 刻意: <检查项> — <理由>`），对应检查就从阻止改为提醒。品牌把关的规则例外：真实、出处、限定条件、版权和可读性永不变通。各角色也可以超出场景库：写自己的场景、动效、运镜、转场和视觉（`references/custom-scenes.md`）。

### 怎么运行团队
1. 读事实（treatment 第 0 节）、素材（能看图就看）和 brief；再读本叙事结构的范例片（`templates/golden/<结构>.json`，第 0 节写明）和 `references/copy-bank.md`，看清每个角色在顶级水准下交出什么。
2. **按顺序**逐个扮演角色，每次只写该角色的那一节，不越界。
3. 再扮演**设计评审**，诚实打分：平均分低于 4 或任一项低于 3，就回到**你能改变的**最弱环节重做（更锐利的开场、一个平静拍点、首尾呼应的结尾、为高潮换一张更好的图），再重新打分，最多三轮。绝不虚高打分，也不要停在关卡前：素材本身的局限（占位图、照片太少）写进第 1 节“缺口”和汇报里，不计入分数。
   - **画面质量与选择**只评团队能控制的部分：每个拍点用哪张图、怎么裁、什么顺序、最好的图是否留给高潮。选得好、用得好的手绘占位图可以得 4 分；文件夹里有更好的图却选了差的，就不行。
4. 文案把最终文字写进 `film.json`，替换所有 `TODO`，运行 `lint_copy.py`。
5. 剪辑对照节奏表核对 `film.json` 的小节和拍点，然后运行 `make_film.py --stage check`。

### 1. 制片：能不能做、可不可以用
- **职责**：受众、渠道（是否有声播放、之后是否要竖版）、时长、素材、授权。
- **规则**：
  - 只用真实产品画面。
  - 音乐用用户的曲子或 `make_music.py` 原创。
  - 引言必须真实且经授权。
  - 缺素材就换一个拍点，不造假。
- **补拍清单**：autofilm 会写出 `shot_wishlist.md`，列出最能提升这部片子的镜头（景别、内容、光线、拍摄参数），供用户或真人团队拍摄，并附上 AI 氛围镜头的提示词草稿。AI 画面只能作氛围用并明确标注，绝不能替代产品本身、产品界面或产品结果。

### 2. 策略：什么是真的、什么重要
- **职责**：受众真相、洞察（其中的矛盾）、**唯一主张**（一句话）、证据。
- **好的例子**：“研究者每写一篇论文要在排版表格上花掉一周。”**差的例子**：“研究者想要效率。”
- 主张必须**具体、真实、关于受众的生活**，而不是罗列产品功能。
- **目标受众**：具体是谁（角色、处境）、他们现在用什么替代（真正的竞争对手常常是习惯：一张表格、五个软件、什么都不做）、阻止他们的那个顾虑。片子用证据回答一次这个顾虑。
- **卖点 → 证明画面**：最多三个卖点；每个写清与替代方案的不同，以及哪个场景、哪张画面证明它。没有画面能证明的卖点就删掉，或只在旁白里带着来源说出。
- **诚实的 AIDA**：吸引 = 3 秒钩子；兴趣 = 问题或揭晓；欲望 = 证据与高潮（观众看到自己用上它）；行动 = 结尾页上一个真实的下一步。用真实的社会证明（真实引言、真实数字）和清晰来说服，绝不用虚假的稀缺、虚假的紧迫感或编造的评价。

### 3. 创意总监：让人记住的创意
- **职责**：三个**真正不同**的创意（不是一个创意的三种说法），选出最出人意料**且**最真实的那个；写出开场钩子（0–3 秒）和高潮时刻；再写**三句锚点**——开场句（封面）、高潮句（finale）、收尾句（结尾页），各用不同方式说出选定的创意，收尾句呼应开场句。没有落到这三句里的创意，只是装饰。
- **有效的开场方式**：
  - **微距细节**：先质感，后全貌；
  - **对比切**：新旧一刀切开；
  - **一个大胆而真实的数字；**
  - **静默加一个词；**
  - **人的瞬间**：手、脸、地点；
  - **一个观众问过自己的问题。**
- **引起共鸣的手法**：
  - 一个具体的真相胜过五个卖点；
  - 首尾呼应（结尾回到开场画面）；
  - 三段式；
  - 高潮前的停顿；
  - 结尾落在观众身上，而不是产品身上。
- **否决**：“快、简单、强大”式创意；任何换个品牌也能用的广告。

### 4. 文案：更少、更真的字
- **职责**：口号（中文 ≤ 12 字、英文 ≤ 8 词，格式 `中文 / English`）、完整脚本（按片序每个场景一条：`- cover → "台词"`；无旁白的场景写明原因）、所有画面文字。film.json 的台词从这份脚本照抄，不在别处另写。
- **规则**：
  - 多用动词和名词，少用形容词。
  - 每句证据（feature、hero、numbers 等）都带一个文档里的事实：数字、材料、地点、功能名；讲它对观众意味着什么，不要念规格清单（`lint_copy` 会标出属性罗列、连串单位和 3 个以上的短项，文案分会被封顶）。
  - 只写可核实的数字。
  - 画面文字不重复旁白。
  - 英文语速约每秒 2.5 个词。
  - 中文字幕要写成自然的中文，而不是英文的翻译。
- **禁用**：见 `scripts/lint_copy.py`（颠覆、赋能、极致、一站式、revolutionary、seamless 等）、感叹号、无法证明的最高级。
- **行动号召**：文档支持的一个真实下一步（申请内测、下载、预订），中文 ≤ 8 字 / 英文 ≤ 4 词，写进 `brand.cta`，结尾页最后以按钮形式出现。产品做不到的不写；写“无”也完全可以。最后一句旁白仍是呼应开场的那句，不是行动号召。

### 5. 美术指导与调色：高品味设计师
- **职责**：确认视觉风格和色彩导演选定的配色（`film.json` 的 "palette"，方案第 5 节；见 `references/director.md` 第 8 节），为每个拍点挑最好的画面，把最好的一张留给高潮。
- **作为调色师**：调色的冷暖跟随配色（暖调产品偏暖，医疗与科技偏冷），强度以保持真实界面和产品颜色为准；全片一个影调；色彩脚本只轻微变化（之前偏冷、产品真实、高潮略浓、收尾偏暖）。
- **品味规则**：
  - **每帧一个视觉焦点**，两个元素抢戏就删一个。
  - **一种强调色**，其余都是中性色；画面最亮的东西就是旁白正在讲的东西。
  - **最多两种字体**（由风格决定），不再加第三种。
  - **留白是设计的一部分**：边距 ≥ 96 px，文字不贴图片边。
  - **真实胜过装饰**：真实产品照胜过任何插画，真实界面胜过任何样机。
  - **不用俗套**：地球、握手、灯泡、摆拍笑脸、漂浮图标、假仪表盘。
- **按产品选风格**：见 `references/styles.md` 与 `genres.py`。照片放 `photo` / `detail` / `hero`；透明底产品图放 `hero` / `lineup`；界面截图放 `feature` / `carousel` / `phone`。
- **满幅胜过卡片**：照片满幅承载一个拍点（`photo`、单张照片的 `hero`），配一句话；带规格清单的卡片像幻灯片。任何卡片最多 2 个要点，而且只放服务于核心概念的要点。
- **高潮回应开场**：高潮是开场画面的变化（同一张界面，答案从中浮现；同一张照片，变成完整而明亮的全景），或者回答开场句。在半拍静默后的强拍上只做一个动作，单独停留约 3 秒，再出名称。没有呼应时 `check_treatment` 会把高潮分封顶为 3。
- **高潮是真实的产出**：以界面为主的片子落在“做成的结果”上——一张结果界面（`"hero": "result"`）、从界面中升起的那张关键图表或报告（`"rise"`），或一组安静叠入的产出（`"stack"`）；以照片为主的片子回到封面照片（`"image"`）。倾斜图片墙只是兜底，不是高潮。
- **纹理要有用意**：无旁白的细节拍点需要一句话或带标注的裁切，否则就删掉。
- **冷开场要有主体**：封面图会在开头几秒满幅播放，要用地点、人物或使用中的产品，不要用纹理。
- **冷开场要有两拍**：照片封面要给主体设 `focus`（`python3 scripts/subject_grid.py <照片> --preview .`，再用 `--cells` 选格子）：片子先停在这个细节上，再拉开到全景。一张静图停 6 秒就像幻灯片；没有 `focus` 时 `check_treatment` 会把开场分封顶为 3。
- **说画面里有的东西**：在第 5 节为每张图写一行（地点与主体）。图上的文案要说同一类地点：帐篷画面上不能说“房间”。室内词配户外画面（或反过来）会被 `check_treatment` 拦下。
- **先出钩子，再出名字**：开头约 5 秒是产品的真相（画面与开场句），Logo 在之后出现，或只在高潮与结尾页出现（`"name": false`）。
- **界面要看得清**：在成片尺寸下，界面文字至少 18 px；整屏密集截图停留不超过一秒，随即推近到旁白所说的区域（每个要点给 rect，轮播面板给 `crop`，界面封面给 `focus`）。文字过小时 `check` 会提示。

### 6. 导演与摄影指导、动效设计与剪辑：画面、运动、节奏
- **职责**：审阅导演设计的分镜表（`treatment.md` 第 6 节：每个场景的景别、版式、运镜、转场及理由），保留或有意识地修改；动效语言（按主题选）；节奏。
- **作为导演与摄影指导（景别）**：开场刻意地由近到远（先细节、后环境）或由远到近；一章内由全景到中景到特写（整个工具、那块面板、那个数字）；不连续三个相同景别；高潮是全片最近、最干净的画面。运镜要有动机（推向旁白所说的东西、随轮播横移），幅度小，不与画面内已有的推近打架。
- **蒙太奇**：切在小节线上；两个场景形状或画面相同时用匹配剪辑（高潮回到开场那张界面就是最强的一次）；两个密集拍点后喘一口气。
- **作为动效设计师**：代码动画（旅程图、多合一、动态文字、真实数字图表，见 `references/director.md` 第 7 节）只用在故事需要、而素材里没有的画面上。
- 只在故事转折处用镜头转场；全片只有一个高潮，位于 60–70% 处。
- **呼吸感**：连续两个密集拍点之后给一个平静拍点。开头 3 秒和结尾 5 秒最常被看到，要做到完美。
- **证据要换形状**：相邻两个证据拍点不用同一种形状：功能之后接放大的细节、一个数字、一段录屏、前后对比，或一口气。手机或录屏场景要有一句服务于核心概念的旁白，否则就删掉。
- **不要空停**：平静拍点要短。无旁白的纹理 2 小节，单张图的揭晓 3 小节；一张静图停得更久就会显得空（`check` 会提示）。

### 7. 作曲与声音设计：让人感受到的部分
- **职责**：音乐（用户的曲子，或按类型选的原创情绪与 BPM）、在哪里推进、高潮前的半拍静默、音效组合。声音要压低：感受得到，不喧宾夺主。
- 可选的原创情绪：`python3 scripts/make_music.py --list`。

### 8. 品牌把关：没有虚假，没有看不清
- **职责**：每条说法都对照来源核实。
- **限定条件**：文档对某个说法有限定（专业版或付费版、测试版或预览版、仅某平台、部分地区、“计划中”“即将推出”），作出该说法的场景就必须说明这个限定，写在旁白、字幕或标签里。遗漏限定条件就是虚假说法，即使每个字都属实。`check_treatment.py` 发现后会阻止构建；请在第 8 节“限定条件”中逐条列出。
- **数字**：画面上的数字必须是文档中的真实值，不能出现计数途中被读成别的数字的帧（`numbers` 场景默认直接呈现真实值）。
- 核实音乐、照片、Logo、引言的授权。
- 字幕必须始终可读，重要内容不能被字幕遮挡。
- 构建前必须**签字**。

### 9. 设计评审：品味评分
`check_treatment.py` 会用片子本身交叉核对并给可测的分数封顶：文案具体度（带事实的句子比例）、核心概念（创意是否进入文案）、画面选择（一图一拍点、截图有高亮框）、节奏（不连续三个相同拍点）、克制（只有一个高潮）、结尾（首尾呼应而不是营业信息）。分数超过上限就不能构建：改片子，不改分数。每项 1–5 分（评分标准见上方英文表格）：一个核心概念、三秒抓人、具体真实的文案、画面质量与选择、克制、节奏、高潮、结尾记忆点。平均 ≥ 4 且每项 ≥ 3 才能构建。
