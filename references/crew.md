# The crew · 制作团队

English first, 中文在后。A top film is made by a team, so play each role in turn. Each role writes its own section of `treatment.md` (from `templates/treatment.template.md`; `autofilm.py` pre-fills the facts). The **design critic** then scores the result. Build only when `python3 scripts/check_treatment.py treatment.md film.json` passes.

## English

### How to run the crew
1. Read the facts (§0 of the treatment), the materials (look at the images if you can) and the brief. Then study the golden film for your arc (`templates/golden/<arc>.json`, named in §0) and `references/copy-bank.md`: they show what each role's output looks like at the top level.
2. Play the roles **in order**, one at a time. Write only that role's section, and stay inside its job.
3. Then play the **design critic**. Score honestly. If the average is < 4 or any score is < 3, go back to the weakest role and redo that part. Never inflate a score.
4. The copywriter copies the final words into `film.json` and replaces every `TODO`. Run `lint_copy.py`.
5. The editor checks bars and beats in `film.json` against the rhythm map. Then `make_film.py --stage check`.

### 1. Producer: is this possible and allowed?
- **Job:** audience, channel (sound on? vertical cut later?), length, materials, rights.
- **Rules:**
  - Only real product images.
  - Music is the user's track or composed by `make_music.py`.
  - Quotes must be real and approved.
  - Missing material is solved by a different beat, not by faking it.

### 2. Strategist: what is true, and what matters?
- **Job:** the audience truth, the insight (the tension), the *single-minded proposition* (one sentence), and the proof.
- **Good:** "Researchers lose a week per paper to formatting tables." **Bad:** "Researchers want efficiency."
- The proposition must be **specific, true, and about the audience's life**, not about the product's features.

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
  - Every proof line (feature, hero, numbers…) carries one fact from the docs: a number, a material, a place, a feature by name. Say what it means for the viewer; never read a spec list aloud.
  - Numbers only if checkable.
  - Never repeat on screen what the voice says.
  - Spoken English runs at about 2.5 words per second.
  - Chinese captions are natural Chinese, not a translation of the English.
- **Banned:** see `scripts/lint_copy.py` (revolutionary, seamless, next-gen, 颠覆, 赋能, 极致, 一站式 …), exclamation marks and unprovable superlatives.

### 5. Art director: the high-taste designer
- **Job:** confirm the look (style) and the one accent colour (from the logo), choose the best image for every beat, and keep the best one for the hero.
- **Taste rules:**
  - **One focal point per frame.** If two things compete, cut one.
  - **One accent colour.** Everything else is neutral. The brightest thing on screen is what the voice is talking about.
  - **Two typefaces at most** (the style sets them). Never add a third.
  - **Whitespace is a feature.** Margins ≥ 96 px. Text never touches an image edge.
  - **Real over decorative.** A real product photo beats any illustration. A real UI beats any mock-up.
  - **No clichés:** globes, handshakes, light bulbs, stock smiles, floating icons, fake dashboards.
- **Style choice by product:** `references/styles.md` and `genres.py`. Photos go in `photo` / `detail` / `hero` scenes. Cut-outs (transparent PNG) go in `hero` / `lineup`. Screens go in `feature` / `carousel` / `phone`.

### 6. Motion designer & editor: rhythm
- **Job:** the motion language (by theme) and the rhythm map (one row per scene).
- Camera cuts only where the story turns. There is exactly one hero moment, around 60–70 % of the film.
- **Breathing:** after two dense beats, one calm beat. The first 3 s and the last 5 s are the most watched; make them perfect.

### 7. Composer & sound designer: what we feel
- **Job:** the music (the user's track, or a composed mood + BPM that matches the genre), where it builds, the half-beat silence before the hero, and the sound palette. Keep the sound low: felt, not heard.
- Composed moods: `python3 scripts/make_music.py --list`.

### 8. Brand guardian: nothing false, nothing unreadable
- **Job:** check every claim against a source.
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

### 怎么运行团队
1. 读事实（treatment 第 0 节）、素材（能看图就看）和 brief；再读本叙事结构的范例片（`templates/golden/<结构>.json`，第 0 节写明）和 `references/copy-bank.md`，看清每个角色在顶级水准下交出什么。
2. **按顺序**逐个扮演角色，每次只写该角色的那一节，不越界。
3. 再扮演**设计评审**，诚实打分：平均分低于 4 或任一项低于 3，就回到最弱的环节重做；绝不虚高打分。
4. 文案把最终文字写进 `film.json`，替换所有 `TODO`，运行 `lint_copy.py`。
5. 剪辑对照节奏表核对 `film.json` 的小节和拍点，然后运行 `make_film.py --stage check`。

### 1. 制片：能不能做、可不可以用
- **职责**：受众、渠道（是否有声播放、之后是否要竖版）、时长、素材、授权。
- **规则**：
  - 只用真实产品画面。
  - 音乐用用户的曲子或 `make_music.py` 原创。
  - 引言必须真实且经授权。
  - 缺素材就换一个拍点，不造假。

### 2. 策略：什么是真的、什么重要
- **职责**：受众真相、洞察（其中的矛盾）、**唯一主张**（一句话）、证据。
- **好的例子**：“研究者每写一篇论文要在排版表格上花掉一周。”**差的例子**：“研究者想要效率。”
- 主张必须**具体、真实、关于受众的生活**，而不是罗列产品功能。

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
  - 每句证据（feature、hero、numbers 等）都带一个文档里的事实：数字、材料、地点、功能名；讲它对观众意味着什么，不要念规格清单。
  - 只写可核实的数字。
  - 画面文字不重复旁白。
  - 英文语速约每秒 2.5 个词。
  - 中文字幕要写成自然的中文，而不是英文的翻译。
- **禁用**：见 `scripts/lint_copy.py`（颠覆、赋能、极致、一站式、revolutionary、seamless 等）、感叹号、无法证明的最高级。

### 5. 美术指导：高品味设计师
- **职责**：确认视觉风格和唯一的强调色（取自 Logo），为每个拍点挑最好的画面，把最好的一张留给高潮。
- **品味规则**：
  - **每帧一个视觉焦点**，两个元素抢戏就删一个。
  - **一种强调色**，其余都是中性色；画面最亮的东西就是旁白正在讲的东西。
  - **最多两种字体**（由风格决定），不再加第三种。
  - **留白是设计的一部分**：边距 ≥ 96 px，文字不贴图片边。
  - **真实胜过装饰**：真实产品照胜过任何插画，真实界面胜过任何样机。
  - **不用俗套**：地球、握手、灯泡、摆拍笑脸、漂浮图标、假仪表盘。
- **按产品选风格**：见 `references/styles.md` 与 `genres.py`。照片放 `photo` / `detail` / `hero`；透明底产品图放 `hero` / `lineup`；界面截图放 `feature` / `carousel` / `phone`。

### 6. 动效设计与剪辑：节奏
- **职责**：动效语言（按主题选）和节奏表（每个场景一行）。
- 只在故事转折处用镜头转场；全片只有一个高潮，位于 60–70% 处。
- **呼吸感**：连续两个密集拍点之后给一个平静拍点。开头 3 秒和结尾 5 秒最常被看到，要做到完美。

### 7. 作曲与声音设计：让人感受到的部分
- **职责**：音乐（用户的曲子，或按类型选的原创情绪与 BPM）、在哪里推进、高潮前的半拍静默、音效组合。声音要压低：感受得到，不喧宾夺主。
- 可选的原创情绪：`python3 scripts/make_music.py --list`。

### 8. 品牌把关：没有虚假，没有看不清
- **职责**：每条说法都对照来源核实。
- 核实音乐、照片、Logo、引言的授权。
- 字幕必须始终可读，重要内容不能被字幕遮挡。
- 构建前必须**签字**。

### 9. 设计评审：品味评分
`check_treatment.py` 会用片子本身交叉核对并给可测的分数封顶：文案具体度（带事实的句子比例）、核心概念（创意是否进入文案）、画面选择（一图一拍点、截图有高亮框）、节奏（不连续三个相同拍点）、克制（只有一个高潮）、结尾（首尾呼应而不是营业信息）。分数超过上限就不能构建：改片子，不改分数。每项 1–5 分（评分标准见上方英文表格）：一个核心概念、三秒抓人、具体真实的文案、画面质量与选择、克制、节奏、高潮、结尾记忆点。平均 ≥ 4 且每项 ≥ 3 才能构建。
