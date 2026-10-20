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
- Audience & where it plays · 受众与投放渠道: Adults planning a few quiet days away. Social video and the booking page hero; often sound off, so captions carry the film. Landscape 1080p.
- Rights · 授权: Images are drawn placeholders supplied with the materials (no photographs of the real cabins). The logo is the placeholder brand mark. No quotes. Music is the composed underscore (original, royalty-free). Voice is Kokoro am_michael, already downloaded. Brand is an evaluation placeholder for a demo build.
- Gaps · 缺口: No photos of the real cabins, lake, sauna or stove. The film uses drawn placeholders and says so in the report; real photography must replace them before any public use. No phone number supplied, so the contact line is the booking URL only.

## 2. Strategist · 策略
- Audience truth · 受众真相: "I want a few days where nobody can reach me, and I want to know I could."
- Insight · 洞察: They want to be unreachable, yet the phone comes out the moment they arrive. Here the only signal is a walk to the jetty, so the rule of the place does the work for them.
- Single-minded proposition · 唯一主张: Three cabins where the phone only works on the jetty.
- Proof · 证据: (1) Phone signal only on the jetty. (2) Three cabins on Lake Øyvatn, each sleeps two. (3) A 40-minute walk from the nearest road; bags go over on a hand cart.

## 3. Creative director · 创意总监
- Concept A: Long way in: the 40-minute walk and the hand cart. Opening image: a cart on the forest trail. Why it fits: it makes the distance the luxury, but it is a logistics story and does not reach the phone.
- Concept B: Signal on the jetty: the only signal is a short walk to the water. Opening image: the cabin at dusk, one lit window. Why it fits: it turns a real rule of the place into the whole idea, and it lands on the viewer's own habit.
- Concept C: One lit window: the cabin lamp at dusk as the film's only light. Opening image: the window. Why it fits: pure atmosphere, but no proposition; it is decoration.
- Chosen · 选定: B. It is the most surprising (the reason to come is a place with no signal, and even that has a shore) and the most true (phone signal only on the jetty is in the docs).
- Hook (0–3 s) · 开场钩子: The cabin at dusk, window lit, the lake still under it. The voice says the hook line over one quiet breath. No logo, no product name.
- Hero moment · 高潮时刻: The cabin at dusk returns full-frame and lit, held alone for about 2.5 s, then the name. It lands at about 70 % of the film.
- Hook line · 开场句: "Here, signal lives on the jetty."
- Hero line · 高潮句: "Larchwood. Three cabins, no screen."
- Last line · 收尾句: "Leave your signal on the jetty."
- Title · 片名: Signal on the jetty

## 4. Copywriter · 文案
- Tagline · 口号: 三间小屋，无需屏幕 / Three cabins. No screen.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "Here, signal lives on the jetty." (zh: 这里的信号，只在码头。)
  - detail (sauna) → "A wood-fired sauna on the shore, then the lake." (zh: 岸边是柴火桑拿，然后是湖。)
  - hero (trail) → "Larchwood. A forty-minute walk from the road, bags on a hand cart." (zh: Larchwood：离最近的路四十分钟步行，行李由手推车运送。)
  - photo (lake) → "Three cabins on Lake Øyvatn. Each sleeps two." (zh: 三间小屋临湖而立，每间住两人。)
  - detail (window) → "Solar power, a wood stove, and drinking water from the spring." (zh: 太阳能供电，木柴炉取暖，饮用水取自泉水。)
  - finale → "Larchwood. Three cabins, no screen." (zh: Larchwood：三间小屋，无需屏幕。)
  - endcard → "Leave your signal on the jetty." (zh: 把信号留在码头。)
- On-screen words · 画面文字: photo label "Lake Øyvatn, Telemark" (zh: 挪威 Telemark 湖畔); hero label "Larchwood" (zh: Larchwood). Nothing else; the voice carries the rest.
- Banned words checked · 已排除空话: yes, to be run with lint_copy.py.

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh. The accent is the cream of the logo mark, used only for the one lit window and the name; everything else is neutral forest and lake grey.
- Images · 画面选择: cover = cabin-dusk (a subject, the cabin, in the cold open). detail = sauna-wood-detail (texture, two bars, short). hero = forest-trail (the walk in; the name arrives here). photo = lake-dawn (mood, the lake and three-cabin fact). detail = window-view (a view from inside; amenities). finale = cabin-dusk again, the bookend. The best image is kept for the hero.
- Composition rules · 构图: margins at least 96 px; text in the lower third; one focal point per frame; the cabin window is the only warm light.
- We will NOT show · 不出现: people posing, phones or Wi-Fi icons, fake interfaces, globes, handshakes, floating icons, a booking screen.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story. Slow push-ins and small pans; the camera moves for the walk and holds for the cabin.
- Rhythm map · 节奏表: as drafted (cover 3, detail 2, hero 3, photo 4, detail 4, finale 4, endcard 3 bars).

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | the subject first; no name |
| 2 | `detail` | 2 | texture | calm beat after the hook |
| 3 | `hero` | 3 | reveal | first name, with the walk in |
| 4 | `photo` | 4 | mood | the lake, three cabins |
| 5 | `detail` | 4 | texture | window view; the amenities |
| 6 | `finale` | 4 | hero | bookend, ~70 % |
| 7 | `endcard` | 3 | close | callback to the jetty |

- Cuts · 转场: cut from the cabin to the sauna wood (the cabin is entered); cut from the trail to the lake (the walk ends at the water); cut back to the cabin at dusk for the hero (the callback).
- Breathing room · 留白: after the lake photo the window detail rests; before the finale name the frame holds about 2.5 s with no voice.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed ambient-air, about 88 BPM, original. It enters soft under the cabin, builds gently under the lake, and thins out to a bed for the finale.
- Silence · 静默: one bar of silence after the hook line, then the sauna; a half-beat before the finale name.
- Sound palette · 音效: kept low. A soft wood crackle under the sauna detail and a faint lake lap under the lake photo. No sound on the walk and none at the cabin window: the film is quiet on purpose.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实: three cabins on Lake Øyvatn, Telemark, Norway; each sleeps two; 40-minute walk from the nearest road; bags on a hand cart; phone signal only on the jetty; no Wi-Fi; wood-fired sauna on the shore and the lake to cool off in; solar power, wood stove, kettle; drinking water from the spring; 15 May to 30 September; stays of three nights or more. All from the materials README. "Without a screen" follows from "No Wi-Fi" plus "phone signal only on the jetty".
- Legibility & access · 可读与无障碍: captions on for every voice line; contrast checked for the cream accent on dark images; nothing important under captions.
- Sign-off · 签字: approved for the evaluation build only. Drawn placeholder images and the placeholder brand must be replaced before any public use.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | Signal on the jetty drives the hook, the proof and the last line. |
| Hook in 3 s · 三秒抓人 | 4 | A subject (cabin at dusk) and a line about a real rule of the place. |
| Specific, true copy · 具体真实 | 4 | Every proof line carries a fact from the README. |
| Image quality & choice · 画面 | 4 | Placeholders, but each is chosen for its beat and the best one is kept for the hero. Limit stated in Gaps. |
| Restraint · 克制 | 4 | One warm light, one hero, quiet sound. |
| Rhythm · 节奏 | 4 | Calm beats between proof beats; no shape repeats in a row. |
| Hero moment · 高潮 | 4 | The bookend to the hook, held alone. |
| Memorable ending · 结尾记忆点 | 4 | The callback to the jetty ends on the viewer. |
