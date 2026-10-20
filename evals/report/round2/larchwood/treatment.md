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
- Audience & where it plays · 受众与投放渠道: Adults who want a few days off screens; short-form and web video, often with sound off, so captions carry the story.
- Rights · 授权: All five photos and the logo are drawn placeholders from the evaluation folder (the README says so), not photographs of the real cabins. Music is composed for this film. No quotes or testimonials are used. Before any public use, the owner must replace the images with real photography of Larchwood and confirm the brand.
- Gaps · 缺口: No real photographs of the cabins, the sauna, the jetty or the people. We stage the placeholders with calm framing and captions, and say so in the report. No claim depends on the picture alone.

## 2. Strategist · 策略
- Audience truth · 受众真相: "I need to switch off, but I would not know what to do with an empty weekend somewhere remote."
- Insight · 洞察: The wish to disconnect is real, but it comes with unease about being out of reach; the walk in is what makes the disconnection feel earned.
- Single-minded proposition · 唯一主张: Forty minutes on foot, and nothing left to check.
- Proof · 证据: (1) a 40-minute walk from the nearest road, bags carried by hand cart; (2) no Wi-Fi, phone signal only on the jetty; (3) wood-fired sauna on the shore and the lake to cool off in.

## 3. Creative director · 创意总监
- Concept A: The walk in — the film follows the 40-minute path, and the phone goes quiet before the cabin appears. Opening image: a path into the trees. Why it fits: the walk is the real filter, and it is the one fact that is both a cost and a gift.
- Concept B: The jetty bar — the only signal is a single bar on the jetty; the film is about where the signal stops. Opening image: a phone at the water's edge. Why it fits: true, but it leans on a device, and the film should lean on the place.
- Concept C: The lit window — a cabin at dusk as a warm invitation. Opening image: one lit window in the dark. Why it fits: atmospheric, but it could be any cabin brand's ad.
- Chosen · 选定: A. It is the most surprising (the inconvenience of the walk is the selling point) and the most true (the 40 minutes is a fact in the docs and it does the work the marketing cannot).
- Hook (0–3 s) · 开场钩子: The cover is the lit cabin at dusk, held still, with the voice saying the hook line over it. The first three seconds are the cabin and a single sentence about distance.
- Hero moment · 高潮时刻: The lake at dawn, with the name "Larchwood" and the tagline. It lands at about 65 % of the film, after the walk and the sauna.
- Hook line · 开场句: The road ends forty minutes before this door.
- Hero line · 高潮句: Larchwood. Nothing left to check.
- Last line · 收尾句: Forty minutes in. The lake does the rest.
- Title · 片名: Forty Minutes In

## 4. Copywriter · 文案
- Tagline · 口号: 四十分钟之后，无需查看 / Forty minutes in. Nothing to check.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "The road ends forty minutes before this door." (zh: 离这扇门，最近的路还要走四十分钟。)
  - photo → "Your bags go over on a hand cart." (zh: 行李由手推车送过去。)
  - detail → (no voice: the sauna wood is the texture beat, after two lines of facts)
  - hero → "Three cabins on Lake Øyvatn, Telemark. Each sleeps two." (zh: 三间小屋，立于特勒马克的厄维特恩湖畔，每间住两人。)
  - feature 1 → "No Wi-Fi. The phone stays in the bag, except on the jetty." (zh: 没有 Wi-Fi，手机留在包里，码头除外。)
  - feature 2 → "Solar power, a wood stove and a kettle. Drinking water from the spring." (zh: 太阳能供电，柴火炉烧水，饮用水取自泉眼。)
  - finale → "Larchwood. Nothing left to check." (zh: Larchwood：什么都不必再查看。)
  - endcard → "Forty minutes in. The lake does the rest." (zh: 步行四十分钟，其余交给湖。)
- On-screen words · 画面文字:
  - photo: "A 40-minute walk in" / "步行四十分钟"
  - hero: "Larchwood"
  - feature 1: "No Wi-Fi. Signal on the jetty." / "没有 Wi-Fi，信号在码头"; points: "No Wi-Fi in the cabins" / "Phone signal on the jetty only"
  - feature 2: "Solar light, wood stove" / "太阳能照明，柴火炉"; points: "Solar power" / "Drinking water from the spring"
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés. No "getaway", "paradise", "escape", "unwind" or "perfect".

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh (muted, sparse, daylight and dusk); one accent colour taken from the logo's cream on dark green. Warm amber from the lit cabin window is the only warm light.
- Images · 画面选择:
  - cover: cabin-dusk (the lit cabin is the first thing seen)
  - photo: forest-trail (the path, the walk in)
  - detail: sauna-wood-detail (texture, no voice)
  - hero: lake-dawn (best image, saved for the reveal)
  - feature 1: window-view (the cabin window with the lake outside)
  - feature 2: cabin-dusk (the cover image comes back here; with five placeholder images this is a limit, noted in the report)
  - finale: all five, as a montage
- Composition rules · 构图: margins ≥ 96 px; title text sits in the lower third away from the focal point; one focal point per frame; text never touches an image edge.
- We will NOT show · 不出现: stock smiles, handshakes, globes, phones held up to scenery, fake UI, a hot tub, people's faces (none are in the materials, and none are invented).

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story — slow push-ins and soft fades, matching a walk at the pace of a walker.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | lit cabin, hook line |
| 2 | `photo` | 3 | mood | the path, the walk in |
| 3 | `detail` | 3 | texture | sauna wood, silence |
| 4 | `hero` | 4 | reveal | lake at dawn, the name |
| 5 | `feature` | 4 | craft + origin | no Wi-Fi, jetty signal |
| 6 | `feature` | 4 | craft + origin | solar, stove, spring |
| 7 | `finale` | 4 | hero | the tagline |
| 8 | `endcard` | 3 | close | callback to the hook |

- Cuts · 转场: cuts only at the three turns: cover to path (the walk begins), path to lake (the reveal), finale to endcard. Everything else dissolves.
- Breathing room · 留白: after the two feature beats, the finale holds for a full bar before the hero line; the sauna detail is silent.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed ambient-air, ~88 BPM, no drums. It builds softly under the walk and opens at the reveal.
- Silence · 静默: half a beat of air before the hero line; the sauna detail is silent.
- Sound palette · 音效: wind and water at a low level; a soft wooden knock on the cabin door once, on the hook line. No other effects.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - 40-minute walk from the nearest road → materials README, bullet 2
  - bags by hand cart → README, bullet 2
  - no Wi-Fi; phone signal only on the jetty → README, bullet 3
  - wood-fired sauna, lake to cool off in → README, bullet 4
  - solar power, wood stove, kettle, spring water → README, bullet 5
  - three cabins, Lake Øyvatn, Telemark, each sleeps two → README, bullet 1
  - open 15 May–30 September; stays of three nights or more → README, bullet 6 (contacts only)
  - the images are placeholders, not photographs of Larchwood → README footnote; disclosed in the report
- Legibility & access · 可读与无障碍: captions on; cream text on the dark photo passes contrast; nothing important sits under the captions.
- Sign-off · 签字: approved for the evaluation build. Changes needed before public use: real photographs and brand confirmation from the owner.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | One idea: the 40-minute walk is the filter. The copy returns to it at the hook and the last line. |
| Hook in 3 s · 三秒抓人 | 4 | The hook line names a fact (the road ends forty minutes away) over a lit cabin. |
| Specific, true copy · 具体真实 | 4 | Every proof line carries a fact from the README: distance, Wi-Fi, jetty signal, sauna, solar, spring. |
| Image quality & choice · 画面 | 4 | Drawn placeholders, but each beat has its own image where possible, and the best one (the lake) is saved for the reveal. The cover image repeats in feature 2, a limit of five images. |
| Restraint · 克制 | 4 | Quiet beats, one hero, one silence, no effects beyond a soft fade. |
| Rhythm · 节奏 | 4 | Dense feature beats are followed by a calm montage; the sauna is silent. |
| Hero moment · 高潮 | 4 | The lake at dawn, the name, and the tagline after the walk. |
| Memorable ending · 结尾记忆点 | 4 | The last line calls back to the forty minutes of the hook. |
