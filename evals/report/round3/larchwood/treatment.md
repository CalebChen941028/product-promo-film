# Treatment · 创意方案 — Larchwood

> Written by the crew in `references/crew.md`, one section per role, in order. Replace every `write` field.
> `python3 scripts/check_treatment.py treatment.md film.json` must pass before `make_film.py --stage build`.
> 由 `references/crew.md` 中的各角色依次填写；替换所有 `write` 字段，检查通过后再构建。

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: Larchwood
- Genre · 类型: travel-hospitality-living — Travel, hospitality, home, real estate / 旅行 / 酒店 / 家居 / 地产
- Look · 风格: natural-fresh · Motion · 动效: gentle-story · Arc · 叙事结构: sensory
- Music · 音乐: composed: ambient-air ~88 BPM (original, royalty-free)
- Materials · 素材: logo 1, photo 5, text 1
- Target length · 目标时长: ~75 s
- Tone for this genre · 本类型的语气: atmosphere and light; invite, do not sell
- Study first · 先读: `templates/golden/sensory.json` (a top film in this arc, every scene with a `_why`) and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: Three small cabins on a lake, for people who want a few days without a screen. · Three cabins on the shore of Lake Øyvatn, Telemark, Norway; each sleeps two · A 40-minute walk from the nearest road; your bags go over on a hand cart · No Wi-Fi; there is phone signal only on the jetty · A wood-fired sauna on the shore, and the lake to cool off in · Solar power, a wood stove and a kettle; drinking water from the spring · Open 15 May to 30 September; stays of three nights or more · Book at larchwood.example

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Adults planning a few days away from work and screens, who search for a cabin on a phone. Web and social, most of it with sound off, so captions carry every spoken line. A vertical cut can follow later.
- Rights · 授权: The five images and the logo in the materials folder are drawn placeholders, not photographs; the README says so. The music is an original underscore from make_music.py. The voice is Kokoro am_michael, already downloaded. No quotes are used. Owner confirmation of the brand and the placeholders is still needed from the user.
- Gaps · 缺口: No real photographs of the cabins, the sauna, the jetty or the lake, and no real booking screen. Five images for seven beats, so the film stays inside the placeholders and reuses them only in the finale wall. Real photos should replace them before any publication. Length lands near 68 s, under the 75 s target, because the materials give five images and no second feature.

## 2. Strategist · 策略
- Audience truth · 受众真相: "I need a few days where nobody can reach me, and I don't want to drive to find it."
- Insight · 洞察: The place that is hardest to reach is the one that gives the quiet. The distance is what people are buying, and it reads as a cost on a booking page.
- Single-minded proposition · 唯一主张: The forty-minute walk in is what keeps the stay quiet.
- Proof · 证据: A 40-minute walk from the nearest road, with the bags carried on a hand cart. No Wi-Fi, and phone signal only on the jetty. Open 15 May to 30 September, for stays of three nights or more.

## 3. Creative director · 创意总监
- Concept A: The walk in — the forty-minute walk on foot is the threshold; opening image: a lit cabin window at dusk at the end of a path — why it fits: the walk is the one true, checkable fact that makes the place feel far away.
- Concept B: One bar of signal — phone signal only on the jetty; opening image: the lake at dawn, with the jetty as the only place a phone works — why it fits: it turns the missing Wi-Fi into a scene, but it is a feature, and it needs the jetty to explain itself.
- Concept C: Bags on a hand cart — the bags go over on a hand cart; opening image: a wood detail of the sauna — why it fits: it is charming and true, but it is a logistics detail, and a viewer will not remember it.
- Chosen · 选定: A, The walk in. It is the most true, because the walk is in the docs, and the most surprising, because a holiday place is sold by how far it is to reach. B and C each stay a feature; A is what the whole film is about.
- Hook (0–3 s) · 开场钩子: Cabin-dusk fills the frame, the one lit window in the dark, with a slow push-in. The voice says: "Forty minutes on foot from the nearest road." Music enters soft on the first beat.
- Hero moment · 高潮时刻: The lake at dawn, the reveal of Larchwood. The still water mirrors the far mountains and the film holds on it, the one image the audience keeps. It lands at bar 10 of 22 (about 45 %), and the finale wall that follows carries the tagline.
- Hook line · 开场句: Forty minutes on foot from the nearest road.
- Hero line · 高潮句: Larchwood. Days without a screen.
- Last line · 收尾句: Forty minutes in. Then, the quiet lake. (It calls back to the hook: the same walk, now the reward.)
- Title · 片名: Forty Minutes In

## 4. Copywriter · 文案
- Tagline · 口号: 三间小屋，一湖静水 / Three cabins. One lake.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "Forty minutes on foot from the nearest road."
  - photo → "Your bags follow on a hand cart."
  - detail → (no voice: the wood and the lake carry this beat, so the film breathes after the hook)
  - hero → "Three cabins on the shore of Lake Øyvatn, Telemark, Norway."
  - feature → "Each cabin sleeps two, with a wood stove and spring water."
  - finale → "Larchwood. Days without a screen."
  - endcard → "Forty minutes in. Then, the quiet lake."
- On-screen words · 画面文字: Photo: "Bags on a hand cart. You walk the path." Hero: "Larchwood". Feature title: "Three quiet cabins". Points: "Sleeps two per cabin", "Wood stove and kettle", "Drinking water from the spring". Contact: "Book at larchwood.example". No word repeats what the voice says.
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh, because the genre is hospitality and the look should feel like outdoors and wood, not a product screen. The accent is the cream outline of the logo, used on the endcard and the taglines only; the pine-green disc is the base colour.
- Images · 画面选择: cover = cabin-dusk (the lit window, the hook); photo = forest-trail (the path, text on a soft scrim); detail = sauna-wood-detail (texture, no voice); hero = lake-dawn (the reveal, the best image, saved for the one hero); feature = window-view (two windows onto the lake, frame photo, so no highlight rects); finale = all five images as a tilted wall; endcard = logo on a plain ground.
- Composition rules · 构图: Margins at least 96 px. Text sits in the lower third over a soft scrim, never over the lit window. One focal point per frame. Two typefaces at most, as the style sets them.
- We will NOT show · 不出现: phone screens, Wi-Fi or signal icons, booking-widget UI, people posing or smiling at the camera, stock sunsets with slogans, globes, handshakes, or any fake product view.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story. Slow push-ins and soft dissolves suit a quiet place; no whip, no hard flash.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | cabin-dusk, push-in, voice from 0.6 bar |
| 2 | `photo` | 4 | walk in | forest-trail, text on a scrim |
| 3 | `detail` | 3 | texture | sauna wood, no voice, the calm beat |
| 4 | `hero` | 4 | reveal | lake-dawn, the one hero image |
| 5 | `feature` | 4 | the rooms | window-view, four points |
| 6 | `finale` | 4 | hero line | five-image wall, tagline |
| 7 | `endcard` | rest | close | callback to the walk |

- Cuts · 转场: Cuts fall on bar lines. A cut only at the turns: cover to photo (the walk begins), detail to hero (the lake opens up). Between the other scenes, a soft dissolve.
- Breathing room · 留白: After the cover's voice, bar 3 is a rest with the photo's path; the detail beat (bars 7–10) has no voice, so the wood and water carry the film for three bars before the reveal.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: Composed, mood ambient-air at ~88 BPM. It starts under the cover, builds gently through the walk, and opens up at the reveal. It falls back under the feature and rests for the endcard.
- Silence · 静默: One half-bar of silence before the reveal line, so the lake arrives in silence. A second held breath in the detail beat (no voice).
- Sound palette · 音效: Kept low. Wind in pines under the walk; a light water lap at the lake reveal; nothing at the feature and the endcard. No whoosh on the cabin window.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "Forty minutes on foot from the nearest road" → README: "A 40-minute walk from the nearest road"
  - "Your bags follow on a hand cart" → README: "your bags go over on a hand cart"
  - "Three cabins on the shore of Lake Øyvatn, Telemark, Norway" → README: "Three cabins on the shore of Lake Øyvatn, Telemark, Norway"
  - "Each cabin sleeps two" → README: "each sleeps two"
  - "A wood stove and spring water" → README: "a wood stove and a kettle; drinking water from the spring"
  - "Days without a screen" → README: "a few days without a screen"
  - "Forty minutes in. Then, the quiet lake." → restates the 40-minute walk and the lake, both in README
  - Book at larchwood.example; open 15 May to 30 September → README; stays of three nights or more → README
  - Not claimed: "no signal anywhere" (the README says phone signal on the jetty, so the film does not say there is none)
- Legibility & access · 可读与无障碍: Captions on, English and Chinese. Text contrast checked on the scrim. Nothing important sits under the captions.
- Sign-off · 签字: approved for the placeholder evaluation film; changes needed before publication: replace the five placeholders with real photos, and the user confirms the brand and the claims.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | The walk in runs from the hook to the last line; the concept's key word "forty minutes" is on screen twice. |
| Hook in 3 s · 三秒抓人 | 4 | A lit window at dusk with a concrete number in the first line. |
| Specific, true copy · 具体真实 | 4 | Most lines carry a fact from the README (40 minutes, Lake Øyvatn, sleeps two, spring water). Two mood lines remain. |
| Image quality & choice · 画面 | 3 | The images are drawn placeholders, chosen to fit each beat, but they are flat illustrations, not photographs, so the ceiling is 3. |
| Restraint · 克制 | 5 | One hero, a silent detail beat, one accent colour, nothing extra. |
| Rhythm · 节奏 | 4 | Calm detail after the hook; the feature is denser, so the rhythm shows a breath before the hero. |
| Hero moment · 高潮 | 4 | The lake reveal is the one image worth remembering, though the drawn style limits its impact. |
| Memorable ending · 结尾记忆点 | 4 | The last line returns to the walk and the lake. |

Average 4.0; lowest 3 (image, a placeholder limit that real photos would lift).
