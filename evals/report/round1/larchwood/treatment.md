# Treatment · 创意方案 — Larchwood

> Written by the crew in `references/crew.md`, one section per role, in order. Replace every `write` field.
> `python3 scripts/check_treatment.py treatment.md film.json` must pass before `make_film.py --stage build`.
> 由 `references/crew.md` 中的各角色依次填写；替换所有 `write` 字段，检查通过后再构建。

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: Larchwood
- Genre · 类型: travel-hospitality-living — Travel, hospitality, home, real estate / 旅行 / 酒店 / 家居 / 地产
- Look · 风格: natural-fresh · Motion · 动效: gentle-story · Arc · 叙事结构: sensory
- Music · 音乐: composed: ambient-air ~88 BPM (original, royalty-free)
- Materials · 素材: desktop 3, logo 1, photo 2, text 1, ui 3
- Target length · 目标时长: ~75 s
- Tone for this genre · 本类型的语气: atmosphere and light; invite, do not sell

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: People planning a few days away from screens: couples and friends who would rather be outside. Plays on phones and social, often with sound off, so captions carry the meaning.
- Rights · 授权: Logo and images are drawn placeholders from the materials folder, not photographs; the brand is a placeholder for evaluation. No people, no testimonials, no outside music. Music is original and composed. Confirm with the user before any real use.
- Gaps · 缺口: No real photographs, no real interior shots, no testimonials, no recorded voice-over. We use the five supplied images at full frame, the chip says Demo, and captions carry the narration.

## 2. Strategist · 策略
- Audience truth · 受众真相: I know I should switch off, but I never quite do.
- Insight · 洞察: The phone is always within reach, so stopping takes effort. A place that takes the signal away makes stopping the default.
- Single-minded proposition · 唯一主张: Three cabins, a forty-minute walk, and no signal.
- Proof · 证据: No Wi-Fi, and phone signal only on the jetty. A 40-minute walk from the nearest road, with bags on a hand cart. Open 15 May to 30 September; stays of three nights or more.

## 3. Creative director · 创意总监
- Concept A: The Walk In: the forty-minute walk is the threshold, and phones are left behind on the way. Opening image: a trail between tall trees in the mist. Why it fits: the walk is a real, checkable part of arriving.
- Concept B: Signal Bars: the phone's bars fall away as the cabin comes into view. Opening image: the forest path, then a cabin window at dusk. Why it fits: it turns the one hard fact (signal only on the jetty) into a feeling.
- Concept C: Cold Lake, Warm Wood: the lake at dawn set against the wood of the sauna. Opening image: wood grain close up. Why it fits: the amenities are shown through senses, not a list.
- Chosen · 选定: A, because the walk is the most surprising thing to a screen-bound viewer (the phone stays at the road), and it is the most true: it is a fact in the README.
- Hook (0–3 s) · 开场钩子: 0–3 s: the cabin window glows at dusk over a dark lake, with a low ambient pad. Captions read: Three cabins on a Norwegian lake. No Wi-Fi.
- Hero moment · 高潮时刻: About 70 %: the finale. The five images tilt into a wall and the tagline lands in a quiet bar, with the lake image in the centre.
- Title · 片名: Forty Minutes In

## 4. Copywriter · 文案
- Tagline · 口号: 几天，不需要屏幕 / A few days without a screen
- Voice-over · 旁白 (one line per beat, ~2.5 words/s): Narration is captions only (no voice-over recorded): hook, three feature lines, tagline, closing line. Each line is one sentence and under 2.5 words per second.
- On-screen words · 画面文字: Cover: Larchwood, the positioning line and chips. Feature titles as in film.json (zh 12 字 or less, en 42 characters or less). Nothing that the picture already says.
- Banned words checked · 已排除空话: yes, lint_copy.py run on film.json: 0 clichés.

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh: calm greens and greys, with one accent colour from the logo, the cream of the triangle against the forest-green disc.
- Images · 画面选择: cabin-dusk = cover (the lit window); sauna-wood-detail = detail (texture before the whole); forest-trail = walk; lake-dawn = lake and sauna; window-view = no Wi-Fi; the five together = finale wall.
- Composition rules · 构图: Margins 96 px or more; one focal point per frame; labels top-left, captions bottom; no text over the cabin window or the lake horizon.
- We will NOT show · 不出现: Phones on screen, Wi-Fi or signal-bar graphics, people, stock smiles, globes, handshakes, fake UI.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story: slow push-ins and soft cuts; no whips.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | |
| 2 | `detail` | 3 | texture | |
| 3 | `statement` | 2 | the feeling, named | |
| 4 | `feature` | 4 | craft + origin | |
| 5 | `feature` | 4 | craft + origin | |
| 6 | `feature` | 4 | craft + origin | |
| 7 | `finale` | 4 | hero | |
| 8 | `endcard` | 5 | close | |

- Cuts · 转场: Cut on bar lines into each scene; the finale is the only soft dissolve; no cut inside the hero.
- Breathing room · 留白: One bar of hold after the statement, before the finale, so the tagline lands in quiet.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: Composed ambient-air, about 88 BPM, original and royalty-free: pads and bells with almost no drums, building into the finale.
- Silence · 静默: Half a beat of silence before the finale's tagline.
- Sound palette · 音效: Very low: a soft shimmer on the logo and one soft hit at the finale. No sound effects on the walk.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实: Three cabins, each sleeps two: README line 1. 40-minute walk, hand cart: line 2. No Wi-Fi, signal on the jetty: line 3. Sauna, lake: line 4. Solar, stove, spring water: line 5. Dates and three-night minimum: line 6. Images and brand are placeholders (demo).
- Legibility & access · 可读与无障碍: Captions on, bilingual zh and en; contrast checked on dark frames; nothing important under captions.
- Sign-off · 签字: approved for demo use only; real photographs and the real brand are needed before any release.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 5 | One idea: the walk in, one place, one feeling. |
| Hook in 3 s · 三秒抓人 | 4 | The cabin window at dusk is clear in under three seconds. |
| Specific, true copy · 具体真实 | 4 | Copy comes straight from the README facts. |
| Image quality & choice · 画面 | 4 | Consistent palette across the five images; still flat placeholder art. |
| Restraint · 克制 | 4 | Music and motion stay quiet; no effects beyond the finale. |
| Rhythm · 节奏 | 4 | Cuts sit on bar lines; the statement gets one bar of hold. |
| Hero moment · 高潮 | 4 | The finale wall holds the tagline in quiet. |
| Memorable ending · 结尾记忆点 | 4 | The closing line gives the dates and the minimum stay. |
