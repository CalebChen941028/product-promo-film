# Treatment · 创意方案 — Larchwood

> Written by the crew in `references/crew.md`, one section per role, in order.
> `python3 scripts/check_treatment.py treatment.md film.json` must pass before `make_film.py --stage build`.
> 由 `references/crew.md` 中的各角色依次填写；检查通过后再构建。

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: Larchwood
- Genre · 类型: travel-hospitality-living — Travel, hospitality, home, real estate / 旅行 / 酒店 / 家居 / 地产
- Look · 风格: natural-fresh · Motion · 动效: gentle-story · Arc · 叙事结构: sensory
- Music · 音乐: composed: ambient-air ~88 BPM (original, royalty-free)
- Materials · 素材: logo 1, photo 5, text 1
- Target length · 目标时长: ~75 s
- Tone for this genre · 本类型的语气: atmosphere and light; invite, do not sell
- Study first · 先读: `templates/golden/sensory.json` and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: Three small cabins on a lake, for people who want a few days without a screen. · Three cabins on the shore of Lake Øyvatn, Telemark, Norway; each sleeps two · A 40-minute walk from the nearest road; your bags go over on a hand cart · No Wi-Fi; there is phone signal only on the jetty · A wood-fired sauna on the shore, and the lake to cool off in · Solar power, a wood stove and a kettle; drinking water from the spring · Open 15 May to 30 September; stays of three nights or more · Book at larchwood.example

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Adults planning a few days away from work and screens, Europe and North America, mostly on social video with sound off. Captions are on by default, so every line must read on its own. Landscape 1080p only for now; a vertical cut is a later task.
- Rights · 授权: Music is composed by `make_music.py` (original, no licence needed). Photos and logo are drawn placeholders supplied for this evaluation, not photographs of Larchwood. The brand and facts are a placeholder brand. Nothing is quoted; no testimonials.
- Gaps · 缺口: No real photographs of the cabins, the lake, the sauna or the jetty. The five images are drawn placeholders and are labelled as such in the report. Contacts and a real booking link are not confirmed; the end card uses the single address given in the docs.

## 2. Strategist · 策略
- Audience truth · 受众真相: "I want a few days where nothing needs me to check my phone."
- Insight · 洞察: The place that feels most restful is also the one that makes you walk for it, so the rest has to be earned.
- Single-minded proposition · 唯一主张: Three cabins by a lake, with no Wi-Fi and a walk in. (10 words)
- Proof · 证据: (1) Phone signal only on the jetty. (2) A 40-minute walk from the nearest road; bags on a hand cart. (3) Each cabin sleeps two; a wood-fired sauna on the shore.

## 3. Creative director · 创意总监
- Concept A: Signal on the jetty — the only bar of signal is at the end of the boardwalk, so the phone is left there. Opening image: the cabin at dusk, the jetty running into the water. Why it fits: it is true, physical and it sets up a callback.
- Concept B: The walk in — the 40-minute walk and the hand cart. Opening image: the forest trail. Why it fits: honest and specific, but it is about effort, not about rest.
- Concept C: Light at the window — the lit window of a cabin at dusk as the only light for miles. Opening image: the window glow. Why it fits: atmosphere, but it does not give the viewer a reason to act.
- Chosen · 选定: A. It is the most surprising (a phone is left on the jetty, which is the one place it works) and it is true to the docs. Its callback (leave the phone on the jetty) is the ending, so the idea is in the hook, the hero and the last line.
- Hook (0–3 s) · 开场钩子: Cabin at dusk, full frame, warm window, the jetty reaching into dark water. The voice opens with the signal line. No logo yet.
- Hero moment · 高潮时刻: The lake at dawn, full frame, the cabins' name and the three-cabins fact, then the finale montage of all five images. The hero sits at about two-thirds of the film.
- Hook line · 开场句: "The nearest signal is at the end of the jetty."
- Hero line · 高潮句: "Larchwood. Three cabins, one lake."
- Last line · 收尾句: "Leave the phone on the jetty."
- Title · 片名: Larchwood — the jetty

## 4. Copywriter · 文案
- Tagline · 口号: 湖畔三间小屋，无需网络 / Three cabins, one lake, no Wi-Fi.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "The nearest signal is at the end of the jetty." (proof: phone signal only on the jetty)
  - photo (forest-trail) → "Forty minutes on foot from the nearest road." (proof: 40-minute walk from the road)
  - detail (sauna wood) → (no voice: a texture beat after two lines of facts)
  - hero (lake-dawn) → "Larchwood. Three cabins on Lake Øyvatn, each sleeping two." (proof: three cabins, sleeps two)
  - photo (window-view) → "Drinking water comes from the spring." (proof: spring water; solar, stove and kettle are on screen)
  - photo (cabin-dusk) → "Stay long enough to let the lake set the pace." (proof: minimum stay of three nights, on screen)
  - finale → hero line (tagline, shown on screen, caption hidden)
  - endcard → "Leave the phone on the jetty." (motto, caption hidden)
- On-screen words · 画面文字:
  - cover: none beyond the hook line
  - photo 2: 行李走手推车 / Bags come on a hand cart
  - hero: Larchwood
  - photo 5: 太阳能、柴炉与水壶 / Solar, a wood stove, a kettle
  - photo 6: 至少住三晚 / Three nights or more
  - endcard: contacts and the booking address
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés.

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh. Muted, cool palette with one warm accent taken from the logo's cream and the cabin window light. Only the warm window and the wood carry warmth; everything else stays neutral.
- Images · 画面选择: The cover is the cabin at dusk because it has a subject and the jetty leads the eye to the lake. The forest trail carries the walk. The sauna wood is a texture beat. The lake at dawn is the best image and is kept for the reveal. The window view carries the amenities beat. The cabin at dusk returns for the stay line as a callback to the cover. The finale uses all five images.
- Composition rules · 构图: Margins at least 96 px. Text sits in the lower third over a soft scrim and never touches an image edge. One focal point per frame.
- We will NOT show · 不出现: phone screens, Wi-Fi icons, people with phones, stock smiles, floating icons, fake dashboards, a map pin, maps of Norway.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story. Slow push-ins and soft cross-dissolves suit the sensory arc and the quiet subject.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | |
| 2 | `photo` | 3 | mood | the walk |
| 3 | `detail` | 2 | texture | no voice |
| 4 | `hero` | 3 | reveal | the name |
| 5 | `photo` | 3 | mood | amenities |
| 6 | `photo` | 3 | mood | stay length, callback image |
| 7 | `finale` | 4 | hero | the tagline |
| 8 | `endcard` | 3 | close | the callback line |

- Cuts · 转场: Camera cuts only where the story turns: cover to walk (the path opens), the sauna texture to the reveal (from wood to the lake), and the finale into the end card.
- Breathing room · 留白: After the walk and the reveal there is a two-bar texture beat with no voice, so the viewer rests before the amenities. The end card is the last quiet moment.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: Original composed ambient-air, ~88 BPM, warm pads with a soft pulse, built from `make_music.py`. It opens quiet, lifts gently into the reveal and holds through the finale.
- Silence · 静默: A half-beat of silence before the tagline on the finale. Nothing else is held.
- Sound palette · 音效: Kept very low. A soft wood knock as the sauna texture starts, and the sound of water on the jetty as the cover turns. No sound on the photos.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "phone signal only on the jetty" → docs: "No Wi-Fi; there is phone signal only on the jetty"
  - "40-minute walk, bags on a hand cart" → docs: "A 40-minute walk from the nearest road; your bags go over on a hand cart"
  - "three cabins on Lake Øyvatn, each sleeping two" → docs: "Three cabins on the shore of Lake Øyvatn, Telemark, Norway; each sleeps two"
  - "solar power, wood stove, kettle, spring water" → docs: "Solar power, a wood stove and a kettle; drinking water from the spring"
  - "three nights or more" → docs: "stays of three nights or more"
  - "open 15 May to 30 September" → docs: "Open 15 May to 30 September"
  - "sauna and the lake to cool off in" → docs: "A wood-fired sauna on the shore, and the lake to cool off in"
  - Tagline "Three cabins. One lake. No Wi-Fi." → restates the docs; no extra claim.
- Legibility & access · 可读与无障碍: Captions on. Contrast checked against the scrim. Nothing important sits under the captions.
- Sign-off · 签字: approved, with the placeholder-imagery note carried into the report.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | The jetty signal runs from hook to callback. |
| Hook in 3 s · 三秒抓人 | 4 | A cabin at dusk and a line that makes you ask why. |
| Specific, true copy · 具体真实 | 4 | Every proof line carries a fact from the docs. |
| Image quality & choice · 画面 | 4 | Each beat has a fitting image; the best image (lake at dawn) is kept for the reveal. The images are drawn placeholders, so their source limit is in §1 Gaps and in the report, not in this score. |
| Restraint · 克制 | 4 | One hero moment, quiet texture beats, no effects beyond push-ins. |
| Rhythm · 节奏 | 4 | Quiet, then a lift at the reveal, then the finale. |
| Hero moment · 高潮 | 4 | The lake at dawn with the name and the three-cabins line. |
| Memorable ending · 结尾记忆点 | 4 | "Leave the phone on the jetty." |
