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
- Audience & where it plays · 受众与投放渠道: Travellers planning a few quiet days, mostly on phones with sound off. Landscape 1080p; captions carry the story with sound off.
- Rights · 授权: All images are drawn placeholders supplied in the materials folder for this evaluation (not photographs); the brand is a placeholder. The logo and text are the user's. No third-party music or quotes. Music is composed (make_music.py).
- Gaps · 缺口: No photographs of the real cabins, the jetty or the sauna; the images supplied are drawn placeholders. The jetty is never shown as a place of signal; the film says it in words. Missing shots are replaced by a different beat, not faked.

## 2. Strategist · 策略
- Audience truth · 受众真相: "I want a few days where nothing needs me to answer."
- Insight · 洞察: The place is the reward, but the only way to reach it is to leave the phone behind.
- Single-minded proposition · 唯一主张: Three cabins, a lake, and no signal except on the jetty.
- Proof · 证据: (1) Only phone signal is on the jetty. (2) Three cabins, each sleeping two, on Lake Øyvatn. (3) 40-minute walk from the road; bags on a hand cart.

## 3. Creative director · 创意总监
- Concept A: Quiet hours — the film is a list of slow mornings and dusks with nothing to check; opening on dawn mist; the place is the calm.
- Concept B: The walk in — the film follows the path from the road to the cabins, with the bags on a hand cart; opening on the forest trail.
- Concept C: The Jetty — the only signal is at the end of the jetty, so the whole film walks toward a place where you put the phone down; opens on the lake at dawn with a single line about the jetty.
- Chosen · 选定: C. It is the most surprising (a holiday place defined by where the signal stops) and the most true (the facts say it: phone signal only on the jetty). It gives a physical object to end on: the phone, left on the jetty.
- Hook (0–3 s) · 开场钩子: Lake Øyvatn at dawn, mist lifting off the water, a slow push-in across the still surface. The voice says the signal line over the lake.
- Hero moment · 高潮时刻: The three cabins' lit window at dusk, then the full finale wall of all five images, the name and tagline. It lands at about 65 % of the film.
- Hook line · 开场句: "Phone signal here waits at the end of the jetty."
- Hero line · 高潮句: "Larchwood. Three cabins. One lake."
- Last line · 收尾句: "Leave the phone on the jetty." (callback to the hook's jetty)
- Title · 片名: The Jetty · 码头

## 4. Copywriter · 文案
- Tagline · 口号: 三座小屋，一片湖 / Three cabins. One lake.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s): 
  - cover → "Phone signal here waits at the end of the jetty." (hook; fact: phone signal only on the jetty)
  - photo → "Three cabins on the shore of Lake Øyvatn, each sleeping two." (fact: three cabins, sleeps two)
  - detail → (no voice: the texture of the wood carries the beat after the first fact)
  - hero → "Forty minutes' walk in. Your bags follow on a hand cart." (fact: 40-minute walk, hand cart)
  - feature → "Power comes from the sun, and the water from the spring." (fact: solar power, spring water)
  - statement → (no voice: on-screen line only)
  - finale → "Larchwood. Three cabins. One lake." (hero line; the name plus the tagline)
  - endcard → "Leave the phone on the jetty." (last line; callback)
- On-screen words · 画面文字:
  - photo title: zh "木柴炉，一把水壶" / en "A wood stove. A kettle." (fact: wood stove and kettle)
  - hero title: "Larchwood"
  - feature title: zh "太阳能供电，泉水饮用" / en "Sun for power. Spring for water."
  - feature points: "Solar power" / "太阳能供电"; "Drinking water from the spring" / "泉水饮用"
  - statement: zh "没有无线网络，只有湖。" / en "No Wi-Fi. Just the lake." (fact: no Wi-Fi)
  - endcard contacts: "BOOK" · "larchwood.example" · "stays of three nights or more" (fact: booking, minimum stay)
  - chips: "Telemark, Norway" · "15 May – 30 Sep" (fact: location, season)
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés. No "getaway", "paradise", "escape", "perfect".

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh, chosen for the sensory arc and the natural palette of the materials. The one accent colour is the logo's warm cream (#E8DFCC) on the logo's deep green (#2F3D38); everything else is neutral.
- Images · 画面选择: cover = lake-dawn (the hook is the lake, the phone is only a word); photo = cabin-dusk (the lit window carries "a wood stove, a kettle"); detail = sauna-wood-detail (texture before the whole); hero = forest-trail (the walk in); feature = window-view (the cabin window for the power and water facts); statement = no image (text beat); finale = all five; endcard = the logo mark on dark.
- Composition rules · 构图: margins ≥ 96 px; text sits on the lower third of the still image with a soft scrim; one focal point per frame; captions never cover the cabin window or the lake horizon.
- We will NOT show · 不出现: phones or screens (the film is about not using them), Wi-Fi symbols, signal bars, stock smiles, hands on laptops, globes, fake dashboards, a map pin, any shot of people.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story. Slow push-ins and light parallax suit a place film. No whip pans and no flashy transitions.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | the jetty line over the lake |
| 2 | `photo` | 3 | mood | the cabins, the stove, the kettle |
| 3 | `detail` | 3 | texture | sauna wood, no voice |
| 4 | `hero` | 4 | reveal | the walk in and the name |
| 5 | `feature` | 4 | craft + origin | sun and spring, the window |
| 6 | `statement` | 2 | breath | no Wi-Fi, just the lake |
| 7 | `finale` | 4 | hero | the name, the three cabins, one lake |
| 8 | `endcard` | rest | close | the callback to the jetty |

- Cuts · 转场: Only soft dissolves. A single camera cut into the hero (`hit: "hero"` on finale). No whip cuts anywhere.
- Breathing room · 留白: After the feature (sun and spring), the statement holds two bars with almost no motion, so the viewer rests before the finale.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed, ambient-air, ~88 BPM. Quiet pads and a soft pulse; it builds gently into the finale and rings out under the endcard.
- Silence · 静默: half a beat of silence before the finale's name, and the detail beat is held with no voice.
- Sound palette · 音效: low, natural only: a faint wind on the lake, the wood-stove crackle at the photo scene. Nothing sharp; no phone sounds, no notifications.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "Phone signal here waits at the end of the jetty." → README: phone signal only on the jetty.
  - "Three cabins on the shore of Lake Øyvatn, each sleeping two." → README: three cabins, each sleeps two.
  - "Forty minutes' walk in. Your bags follow on a hand cart." → README: 40-minute walk, bags over on a hand cart.
  - "Power comes from the sun, and the water from the spring." → README: solar power; drinking water from the spring.
  - "No Wi-Fi. Just the lake." → README: No Wi-Fi; the lake is on the doorstep.
  - Booking, season and minimum stay → README: 15 May–30 September; three nights or more; larchwood.example.
  - No claim about Wi-Fi beyond "no signal except the jetty"; no claim about weather or wildlife.
- Legibility & access · 可读与无障碍: captions on by default, and every spoken line is captioned in zh and en; contrast of the cream text on the scrim ≥ 4.5:1; nothing important sits under the captions.
- Sign-off · 签字: approved, with the placeholder caveat: the imagery and brand are placeholders for evaluation. Nothing here may be published as a real business's advertising.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | The jetty is the one idea: the hook and the last line both carry it. |
| Hook in 3 s · 三秒抓人 | 4 | A signal line over a lake at dawn is a tension before the product. |
| Specific, true copy · 具体真实 | 4 | Every proof line carries a fact from the README (distance, count, sleeps, power, water). |
| Image quality & choice · 画面 | 3 | The images are drawn placeholders, not photographs; choices are relevant but not photographic. |
| Restraint · 克制 | 4 | Soft dissolves, one hero, a quiet statement beat. |
| Rhythm · 节奏 | 4 | Sequence of 3-3-3-4-4-2-4 bars with calm beats between dense ones. |
| Hero moment · 高潮 | 4 | The finale wall of all five images lands at about 65 %. |
| Memorable ending · 结尾记忆点 | 4 | "Leave the phone on the jetty." calls back to the hook. |
