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
- Audience & where it plays · 受众与投放渠道: Travellers planning a few quiet days, Norway-curious readers, people who want a break from screens. Shown on a booking page or a social feed, most often with the sound off, so captions carry the story.
- Rights · 授权: All six images are drawn placeholder illustrations supplied with the evaluation folder (not photographs). The logo and brand "Larchwood" are an evaluation placeholder. No music is taken from the web; the underscore is composed. No quotes are used.
- Gaps · 缺口: No real photographs, no people, no interiors, no guest quote. We do not fake any of them. The film works on atmosphere and facts, and the report lists what a real shoot would add.

## 2. Strategist · 策略
- Audience truth · 受众真相: "I need a few days where nobody can reach me, and I want to feel I earned it."
- Insight · 洞察: Getting far enough away is the hard part, and the distance is also what makes the stay worth it. The walk is the cost; the cabin is the reward.
- Single-minded proposition · 唯一主张: A few days on a lake, with nothing to check. (10 words)
- Proof · 证据:
  - A 40-minute walk from the nearest road; bags go over on a hand cart (README).
  - No Wi-Fi; phone signal only on the jetty (README).
  - Three cabins on the shore of Lake Øyvatn, Telemark, Norway; each sleeps two (README).
  - A wood-fired sauna on the shore, and the lake to cool off in (README).
  - Open 15 May to 30 September; stays of three nights or more (README).

## 3. Creative director · 创意总监
- Concept A: The walk in — the distance is the price, and the cabin is what you arrive at. Opening image: the cabin at dusk, one lit window, after a long path. Why it fits: it turns the one hard fact (40 minutes from the road) into the emotional payoff.
- Concept B: Signal on the jetty — the only phone signal is at the end of the dock, so the film is about the one place you can still check something, and choosing not to. Opening image: the jetty at the water's edge. Why it fits: true and surprising, but it reads as a joke about the product rather than about the stay.
- Concept C: The window view — the film is one view, framed by a window, slowly seen over days. Opening image: the window with the lake. Why it fits: pretty, but any lake cabin could use it.
- Chosen · 选定: A. It is the most surprising (a cabin is marketed by how far away it is) and the most true (every fact in the README is about getting there or being there). B is a good detail and becomes the no-signal beat; C is decoration.
- Hook (0–3 s) · 开场钩子: The cabin-dusk image fills the frame, one warm window lit in a blue dusk, no logo. The voice says the hook line over the lit window.
- Hero moment · 高潮时刻: The cabin-dusk image returns full-bleed at the finale, lit, with the name and the tagline. It lands at about bar 16 of 24, roughly 65 % of the film.
- Hook line · 开场句: The nearest road is a forty-minute walk away.
- Hero line · 高潮句: Larchwood. Nothing to check.
- Last line · 收尾句: The road can wait. You have arrived.
- Title · 片名: Larchwood — the walk in

## 4. Copywriter · 文案
- Tagline · 口号: 放下手机，住几天 / Nothing to check.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "The nearest road is a forty-minute walk away." (zh: 最近的公路，走路要四十分钟。)
  - detail → "A wood-fired sauna, and the lake to cool off in." (zh: 柴火桑拿，之后跳进湖里降温。)
  - hero → "Larchwood. Three cabins on the shore of Lake Øyvatn, Telemark." (zh: 三座湖畔小屋，位于挪威泰勒马克。)
  - photo → "Each cabin sleeps two. Three cabins, one shore." (zh: 每座小屋住两人，三座，同一片湖岸。)
  - detail → "No Wi-Fi. Phone signal is on the jetty." (zh: 没有 Wi-Fi，手机信号只在码头。)
  - finale → "Larchwood. Nothing to check." (zh: Larchwood：放下手机，住几天。)
  - endcard → "The road can wait. You have arrived." (zh: 公路可以等，你已经到了。)
- On-screen words · 画面文字:
  - hero title: Larchwood
  - photo title: Lake Øyvatn, Telemark (zh: 泰勒马克，Øyvatn湖)
  - endcard contacts: BOOK / 预订 · larchwood.example · open 15 May – 30 September, 3 nights min
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés (no "getaway", "paradise", "escape", "unwind").

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh. Muted greens, slate blue and warm lamp-light; the one accent is the warm cream/amber of the cabin window, which matches the cream triangle in the logo. Single focal point per frame.
- Images · 画面选择:
  - cabin-dusk → cover (hook, full-bleed, subject first) and finale (bookend, the hero).
  - sauna-wood-detail → detail beat 2 (texture: wood, then the sauna fact).
  - forest-trail → hero reveal (the walk in, the place).
  - lake-dawn → photo beat (the lake, the cabins' shore).
  - window-view → detail beat 5 (the window and the no-signal line).
  - logo → endcard (and the brand card at the reveal).
- Composition rules · 构图: margins ≥ 96 px; text sits on the lower third or a soft scrim; no text over the lit window.
- We will NOT show · 不出现: phones, screens, Wi-Fi symbols, people posing, hot tubs, pine-cone clichés, globes, aerial drone sweeps, fake interiors.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story — slow push-ins and settling moves, matching a walk and a quiet place. No whips, no flashy transitions.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | cabin-dusk, no logo |
| 2 | `detail` | 2 | texture | sauna wood, one line |
| 3 | `hero` | 3 | reveal | the walk in, name appears |
| 4 | `photo` | 4 | mood | the lake, the shore, three cabins |
| 5 | `detail` | 4 | texture | window and no-signal line |
| 6 | `finale` | 4 | hero | cabin-dusk bookend, name + tagline |
| 7 | `endcard` | rest | close | callback line, contacts |

- Cuts · 转场: cut only where the story turns: cover → detail (from dusk to the wood), and hero → photo (from the walk to the lake). The finale returns to the cover image as a bookend.
- Breathing room · 留白: After the photo beat, the detail on the window is held quiet for four bars, with only a line, so the viewer rests before the finale.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed, ambient-air, ~88 BPM, original. Sits low, builds gently into the finale, then rings out on the endcard.
- Silence · 静默: half a beat of silence before the finale's hero line; no other held breath.
- Sound palette · 音效: keep it low. A soft crackle or stove sound under the sauna detail is welcome; no whooshes and no impact hits. The hero moment gets the default flare only.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "The nearest road is a forty-minute walk away" → README: 40-minute walk from the nearest road.
  - "A wood-fired sauna, and the lake to cool off in" → README: wood-fired sauna on the shore, and the lake.
  - "Three cabins on the shore of Lake Øyvatn, Telemark" → README: three cabins, Lake Øyvatn, Telemark, Norway.
  - "Each cabin sleeps two" → README: each sleeps two.
  - "No Wi-Fi. The only signal is on the jetty" → README: no Wi-Fi; phone signal only on the jetty.
  - "Open 15 May – 30 September, 3 nights min" → README: open 15 May to 30 September; stays of three nights or more.
  - "The road can wait. You have arrived." is an invitation, not a claim.
  - "Nothing to check" is the no-Wi-Fi fact restated as an invitation, not a new claim.
- Legibility & access · 可读与无障碍: captions on, contrast checked against the dark cabin image; the only on-screen text is the name and the endcard contacts, kept clear of the lit window.
- Sign-off · 签字: approved for an evaluation cut. Changes needed before any public use: replace the drawn placeholders with real photographs and confirm the brand name.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | The walk in is the one idea; the copy keeps returning to distance and the cabin. |
| Hook in 3 s · 三秒抓人 | 4 | A lit cabin in dusk and a line about the road: a tension in the first seconds. |
| Specific, true copy · 具体真实 | 4 | Every proof line carries a README fact (distance, signal, sauna, opening dates). |
| Image quality & choice · 画面 | 3 | The images are drawn placeholders; chosen and staged with care, but not photographs, so it cannot score higher. |
| Restraint · 克制 | 5 | Gentle motion, one hero, no logo before the hero, quiet holds. |
| Rhythm · 节奏 | 4 | Two detail beats are separated by the photo and hero, so the proof shapes change. |
| Hero moment · 高潮 | 4 | The lit cabin returning full-bleed at the finale is a moment to remember. |
| Memorable ending · 结尾记忆点 | 4 | "The road can wait forty minutes" calls back to the hook and lands on the viewer. |

Average 4.0; no score below 3. Limits in §1 Gaps and in the report, not in the scores.
