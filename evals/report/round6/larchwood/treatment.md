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
- Target length · 目标时长: ~65 s — 5 images/clips carry about 65 s; the sensory arc would run 75 s with more material. Do not pad: no repeats, no long holds
- Tone for this genre · 本类型的语气: atmosphere and light; invite, do not sell
- Study first · 先读: `templates/golden/sensory.json` (a top film in this arc, every scene with a `_why`) and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: Three small cabins on a lake, for people who want a few days without a screen. · Three cabins on the shore of Lake Øyvatn, Telemark, Norway; each sleeps two · A 40-minute walk from the nearest road; your bags go over on a hand cart · No Wi-Fi; there is phone signal only on the jetty · A wood-fired sauna on the shore, and the lake to cool off in · Solar power, a wood stove and a kettle; drinking water from the spring · Open 15 May to 30 September; stays of three nights or more · Book at larchwood.example

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Adults planning a few days away from screens, reached on social video and the booking site. Sound is often off on social, so every beat must read with captions on.
- Rights · 授权: The five images and the logo are drawn placeholders supplied with the evaluation folder (README: "The images are drawn placeholders, not photographs"). No photographs of the real cabins exist in the materials. The film is for evaluation only until real photography replaces them.
- Gaps · 缺口: No real photographs of the cabins, the jetty, the sauna or guests; no people; no real signal-on-the-jetty shot. Instead: each beat is carried by one image chosen for its fact (dusk cabin for arrival, sauna wood for the sauna, dawn lake for the lake, the window for the stay). The gaps are named in the report, not hidden by extra scenes.

## 2. Strategist · 策略
- Audience truth · 受众真相: "I want a few days away, but I will not walk far with bags to get there."
- Insight · 洞察: The walk is the barrier and also the promise. The 40-minute walk with bags on a hand cart is what keeps the cabins quiet, so the distance is the product, not the flaw.
- Single-minded proposition · 唯一主张: The last forty minutes of the trip are on foot, and they are the point. (Concept: the walk in.)
- Proof · 证据: (1) A 40-minute walk from the nearest road, bags on a hand cart. (2) No Wi-Fi; phone signal only on the jetty. (3) Open 15 May to 30 September; stays of three nights or more.

## 3. Creative director · 创意总监
- Concept A: The walk in — the distance from the road is the first thing we give you; opening image is the cabin at dusk at the end of the path — why it fits: it turns the one fact guests would complain about into the reason to come.
- Concept B: Signal on the jetty — the phone works only at the water's edge; opening image is a phone face-down on a wooden plank — why it fits: sharp and on-theme, but it sells absence, not the place, and it is close to every digital-detox ad.
- Concept C: Three cabins, one lake — the place and the sauna; opening image is the lake at dawn — why it fits: true and warm, but it is a list of what is there, and it could be any lakeside stay.
- Chosen · 选定: A (The walk in). It is the most surprising (a hotel whose experience starts forty minutes before the door) and the most true (the 40-minute walk and the hand cart are in the docs, and only this place has them). B is a theme; C is a catalogue.
- Hook (0–3 s) · 开场钩子: The cabin at dusk, one lit window, full frame, slow push-in. The voice opens on the walk. The image gives a subject (a place) before any claim.
- Hero moment · 高潮时刻: The finale: the cabin at dusk returns full-bleed with the name and the distance, after the stay has been shown. It is the one moment the viewer remembers: the lit window again, now known to be forty minutes away.
- Hook line · 开场句: "The last forty minutes are on foot."
- Hero line · 高潮句: "Larchwood. Forty minutes from the road."
- Last line · 收尾句: "Forty minutes on foot. Then only the lake."
- Title · 片名: The walk in

## 4. Copywriter · 文案
- Tagline · 口号: 四十分钟，靠双脚走到 / Forty minutes on foot.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "The last forty minutes are on foot." (zh: 最后那四十分钟，要靠双脚。)
  - detail → "Wood-fired, then the lake to cool off in." (zh: 柴火烧热，然后下湖。)
  - hero → "Three cabins on Lake Øyvatn. Each sleeps two." (zh: 挪威湖畔的三座小屋，每座住两人。)
  - photo (lake) → "No Wi-Fi. Your phone finds signal only on the jetty." (zh: 没有无线网，手机只在码头有信号。)
  - photo (window) → "A wood stove, a kettle, and spring water to drink." (zh: 木柴炉、一把水壶，喝的水来自泉眼。)
  - finale → "Larchwood. Forty minutes from the road." (zh: Larchwood：离公路四十分钟。)
  - endcard → "Forty minutes on foot. Then only the lake." (zh: 四十分钟步行，然后只剩湖。)
- On-screen words · 画面文字: Scene titles: "Lake Øyvatn, Telemark" (hero), "Signal on the jetty" (lake photo), "Solar light, wood heat" (window). Every title is ≤ 42 characters and repeats a fact, not the voice.
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh, because the product sells a place and its texture. The accent colour is the cream mark of the logo on pine green (#2E3B36-ish); everything else is neutral. Two typefaces at most, set by the style.
- Images · 画面选择:
  - cabin-dusk → cover (hook: a place and a light, full frame) and the finale bookend (the hero moment).
  - sauna-wood-detail → detail (texture; the one line names the wood-fired sauna and the lake).
  - forest-trail → hero reveal (the path through the trees is the walk in; the name sits on the path).
  - lake-dawn → lake photo (no-signal fact).
  - window-view → window photo (the stay: solar, wood stove, spring water).
  - logo → endcard mark, and the accent colour source.
  - The best image, cabin-dusk, is saved for the cover and the hero bookend; it is not used twice in the middle.
- Composition rules · 构图: Margins ≥ 96 px; text sits in the lower third over calm areas; one focal point per frame; captions never cover the cabin window.
- We will NOT show · 不出现: globes, handshakes, smiling stock guests, fake Wi-Fi icons, fake phone UI, any map or price graphic not from the docs.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story — slow push-ins and drifts, no zooms that call attention to themselves. It matches a place that is quiet by design.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | the walk, the dusk cabin |
| 2 | `detail` | 2 | texture | sauna wood, the lake is next |
| 3 | `hero` | 3 | reveal | the name on the path; the three cabins |
| 4 | `photo` | 4 | mood | no signal — the first fact about absence |
| 5 | `photo` | 4 | mood | the stay: warmth, light, water |
| 6 | `finale` | 4 | hero | the cabin returns, the distance named |
| 7 | `endcard` | 3 | close | the callback to the hook |

- Cuts · 转场: Cuts on bar lines. The camera changes only at the turn in the story: from the walk (cover, hero) to the stay (photos) and back to the cabin (finale).
- Breathing room · 留白: After the two fact beats (3 and 4), the window photo gives a calm hold, then the finale. The first 3 s and the last 5 s are kept clean.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed ambient-air (~88 BPM, original): a single warm pad and a soft pulse that builds under the window beat and opens on the finale. No borrowed track.
- Silence · 静默: A half-beat of silence before the hero line; the room tone of a cabin (wind, a fire crackling) under the detail beat, kept very low.
- Sound palette · 音效: Very low: a kettle, a faint fire, lake water. Deliberately no phone, notification or Wi-Fi sound: the film is about their absence.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "The last forty minutes are on foot." → docs: "A 40-minute walk from the nearest road; your bags go over on a hand cart."
  - "Three cabins on Lake Øyvatn. Each sleeps two." → docs: "Three cabins on the shore of Lake Øyvatn, Telemark, Norway; each sleeps two."
  - "Wood-fired, then the lake to cool off in." → docs: "A wood-fired sauna on the shore, and the lake to cool off in."
  - "No Wi-Fi. Your phone finds signal only on the jetty." → docs: "No Wi-Fi; there is phone signal only on the jetty."
  - "A wood stove, a kettle, and spring water to drink." → docs: "Solar power, a wood stove and a kettle; drinking water from the spring."
  - "Forty minutes from the road." → same fact as the walk line.
  - Season and stay length on the end card → docs: "Open 15 May to 30 September; stays of three nights or more."
- Legibility & access · 可读与无障碍: Captions on for every line; the 30-char caption limit holds; the accent colour on pine green passes contrast; nothing important sits under captions.
- Sign-off · 签字: approved for evaluation, with changes needed before any public release: replace the drawn placeholders with real photographs of the cabins, the jetty and the sauna, and confirm the booking terms with the owner.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 5 | The walk in carries every beat: the hook, the hero and the last line all say the same forty minutes. |
| Hook in 3 s · 三秒抓人 | 4 | A subject and a light in the first frame, plus a line that makes the viewer ask why. It is calm rather than gripping. |
| Specific, true copy · 具体真实 | 4 | Every proof line carries a checkable fact from the docs; one line still leans on atmosphere. |
| Image quality & choice · 画面 | 3 | The images are drawn placeholders. They are chosen so each carries one fact and the best one is saved for the finale, but they read as illustration, not photography. |
| Restraint · 克制 | 4 | One hero, no effects beyond a slow push and a soft light; the sound is deliberately sparse. |
| Rhythm · 节奏 | 4 | Two fact beats in a row are followed by a calm window beat; no three identical beats together. |
| Hero moment · 高潮 | 4 | The bookend of the cabin with the distance named is a real moment, but it depends on the placeholder image. |
| Memorable ending · 结尾记忆点 | 4 | The last line echoes the first; it ends on the audience, not on the booking page. |
