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
- Audience & where it plays · 受众与投放渠道: Adults planning a short break who want to switch off. Plays on web and social, mostly with sound off, so captions carry the voice-over. Landscape 1080p only; no vertical cut in this pass.
- Rights · 授权: All images are drawn placeholders supplied for this evaluation (not photographs); the logo is a placeholder mark; the name, positioning and larchwood.example are placeholders. Music is composed original (make_music.py). Voice is Kokoro am_michael, already downloaded. Nothing is licensed from outside. No quotes are used.
- Gaps · 缺口: No real photographs, no people, no real sauna or cabin interior, no testimonial. We stage the drawn placeholders as the brand's stand-ins and state this in the report; we do not invent guest quotes or real photo credits.

## 2. Strategist · 策略
- Audience truth · 受众真相: "I need a few days off the phone, but I want to know I can still get out if I have to."
- Insight · 洞察: The walk is what makes the place feel far away, and that distance is exactly what a tired person wants. The same walk is the one thing that makes them hesitate.
- Single-minded proposition · 唯一主张: Forty minutes on foot is how you leave the screens behind.
- Proof · 证据: A 40-minute walk from the nearest road, bags carried on a hand cart · No Wi-Fi, phone signal only on the jetty · Open 15 May to 30 September, stays of three nights or more.

## 3. Creative director · 创意总监
- Concept A: The walk in — the 40-minute path is the film; we follow the trail from road to door, so the screen-free promise is earned step by step. Opening image: a forest trail between the trees. Why it fits: it is the one fact no competitor can fake, and it makes the product a journey.
- Concept B: Signal at the jetty — the only phone bars are at the water's edge; we follow a phone that never finds a signal until the jetty. Opening image: a phone held up in the dark. Why it fits: funny and true, but it frames the product as a gadget problem, not a holiday.
- Concept C: The lit window — one cabin window glows at dusk seen from the lake; the whole film is the view from outside. Opening image: the cabin at night. Why it fits: beautiful, but it shows the place without the reason to go.
- Chosen · 选定: A, the walk in. It is the most true, because the walk is the real barrier and the real gift, and the most surprising, because a film about a 40-minute walk is not a holiday ad. The cabin image is kept as the bookend, so the lit window arrives as the reward at the end of the walk.
- Hook (0–3 s) · 开场钩子: The forest trail fills the frame, mist between tall trunks, and a calm male voice says the nearest road is forty minutes off. The picture and the number land together.
- Hero moment · 高潮时刻: The finale: the lit cabin window at dusk, full-bleed, with the name and tagline. It lands at about 70 % of the run, after the walk, the lake and the sauna.
- Hook line · 开场句: The walk in is forty minutes from the nearest road. Bags come by hand cart.
- Hero line · 高潮句: Larchwood. Three cabins, no signal.
- Last line · 收尾句: Forty minutes in. Stay a few days.
- Title · 片名: The Walk In · 步入

## 4. Copywriter · 文案
- Tagline · 口号: 湖边三间小屋，没有信号 / Three cabins on a lake. No signal.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "The walk in is forty minutes from the nearest road. Bags come by hand cart." (the hook; proof: 40 min, hand cart)
  - photo 2 → "There is no Wi-Fi. Phone signal only on the jetty." (proof: no Wi-Fi, jetty signal)
  - detail 3 → (no voice: texture before the reveal, a calm beat after a dense line)
  - hero 4 → "Three cabins on the shore. Each one sleeps two." (proof: three cabins, two guests each)
  - finale → "Larchwood. Three cabins, no signal." (hero line, on screen as the tagline)
  - endcard → "Forty minutes in. Stay a few days." (last line: callback to the hook's forty minutes)
- On-screen words · 画面文字:
  - hero 4: "Larchwood" / Larchwood
  - photo 2: "Lake Øyvatn, Telemark, Norway" / 挪威特勒马克 · Øyvatn 湖
  - endcard contacts: BOOK · larchwood.example · stays of three nights or more
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés.

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh. Muted greens and warm wood, one warm accent from the cabin window (the logo's cream on deep green). Only two typefaces, from the style.
- Images · 画面选择: one distinct image per beat, so no drawn placeholder repeats: cover = forest trail (the walk, a subject for the cold open); photo = lake at dawn (the place); detail = sauna wood (texture, no voice); hero = window view (the reveal); finale = cabin at dusk, the bookend and the only image held back for the hero moment.
- Composition rules · 构图: Margins 96 px; text sits on a soft scrim at the lower third; one focal point per frame; the lit window is the only warm element in the finale.
- We will NOT show · 不出现: stock smiles, handshakes, floating icons, a fake booking UI, Wi-Fi symbols, phones held up, globes, fjord clichés with no stated place.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story — slow push-ins and fades. It matches a film about walking, not about speed.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | forest trail, the number lands |
| 2 | `photo` | 3 | place | lake at dawn, no Wi-Fi, jetty signal |
| 3 | `detail` | 2 | texture | sauna wood, no voice |
| 4 | `hero` | 3 | reveal | window view, name, three cabins |
| 5 | `finale` | 4 | hero | cabin at dusk, tagline (~65 % of the run) |
| 6 | `endcard` | rest | close | callback to forty minutes |

- Cuts · 转场: Cuts only where the story turns: cover to photo (we reach the lake), hero to finale (the walk ends at the cabin).
- Breathing room · 留白: The detail beat (sauna wood, no voice) rests the viewer after the place and before the reveal.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed ambient-air, ~88 BPM, original. It builds gently into the reveal and sits low under the voice-over.
- Silence · 静默: Half a beat of silence before the finale, the lit window arriving on silence.
- Sound palette · 音效: Keep it low. Soft wind and water under the lake beat; the sauna detail gets no sound, so the picture carries it.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "Forty minutes from the nearest road" → README: "A 40-minute walk from the nearest road"
  - "Bags come by hand cart" → README: "your bags go over on a hand cart"
  - "Each one sleeps two" → README: "each sleeps two"
  - "Three cabins on the shore" → README: "Three cabins on the shore of Lake Øyvatn"
  - "No Wi-Fi. Phone signal only on the jetty" → README: "No Wi-Fi; there is phone signal only on the jetty"
  - "Solar power, a wood stove, a kettle, spring water" → README: "Solar power, a wood stove and a kettle; drinking water from the spring"
  - "Stay a few days", "stays of three nights or more" → README: "stays of three nights or more"
  - "15 May to 30 September" → README: "Open 15 May to 30 September"
  - "larchwood.example" → README: "Book at larchwood.example"
- Legibility & access · 可读与无障碍: Captions on; the zh and en captions sit above the scrim; contrast checked on the cream text over the dark scrim; nothing important sits under the captions.
- Sign-off · 签字: approved, with the caveat that the images are placeholders and the brand name is a placeholder. Report must say so.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | One walk, one proposition; the concept reaches the hook, the hero line and the last line. |
| Hook in 3 s · 三秒抓人 | 4 | Path into the trees with a concrete number in the first line. |
| Specific, true copy · 具体真实 | 4 | Almost every spoken line carries a fact from the README (40 min, no Wi-Fi, jetty, three cabins, spring). |
| Image quality & choice · 画面 | 4 | Drawn placeholders, each beat has its own image, the best one held for the finale; placeholders limit it, not the staging. |
| Restraint · 克制 | 4 | One hero moment; two silent beats; no extra effects. |
| Rhythm · 节奏 | 4 | Breathes after the dense facts; no three identical beats in a row. |
| Hero moment · 高潮 | 4 | The cabin window at dusk, reached on foot. |
| Memorable ending · 结尾记忆点 | 4 | "Forty minutes in" calls back to the hook and ends on the viewer. |
