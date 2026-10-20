# Treatment · 创意方案 — Humidifier

> Written by the crew in `references/crew.md`, one section per role, in order.
> 由 `references/crew.md` 中的各角色依次填写。

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: Humidifier (working title, no brand name supplied / 工作名，用户未提供品牌名)
- Genre · 类型: travel-hospitality-living — Travel, hospitality, home, real estate / 旅行 / 酒店 / 家居 / 地产
- Look · 风格: natural-fresh · Motion · 动效: gentle-story · Arc · 叙事结构: sensory
- Music · 音乐: composed: ambient-air ~88 BPM (original, royalty-free)
- Materials · 素材: 4 AI-generated images (3 lifestyle, 1 studio on white) + brief.json
- Target length · 目标时长: ~56 s
- Tone for this genre · 本类型的语气: atmosphere and light; invite, do not sell
- Study first · 先读: `templates/golden/sensory.json` and `references/copy-bank.md`
- Facts to use · 可用事实: only what the images show (brief.json, `features`): a thin mist rising from the top; a soft blue-violet glow inside the dome; a rose-gold ring with three icon controls (power, mist, light); a leather carry handle; a white stone-look base; use in a camp, at a desk, in a living room. No specs, numbers, prices or testimonials were supplied.

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: people choosing a home humidifier, watching on a phone, often with sound off (captions on; the voice-over carries the same words).
- Rights · 授权: all four images are AI-generated renders (Gemini), not photographs of a real product. No real brand, logo or person appears. Music is composed by the pipeline. Voice is Kokoro am_michael (already installed). The film is a concept piece until real product photos and specs replace these images.
- Gaps · 缺口: no product name, logo, specs, price, contacts, testimonials or real photos. The film makes no numeric, health or performance claim; the name stays a working title; the end card carries no contact details.

## 2. Strategist · 策略
- Audience truth · 受众真相: "The room feels stuffy and dry, and I never know what to do about it."
- Insight · 洞察: the air in the room is invisible, but the mist makes it visible and calm.
- Single-minded proposition · 唯一主张: One soft mist, wherever you sit.
- Proof · 证据: (1) a thin mist rises from the top of the unit; (2) the dome carries a soft blue-violet glow; (3) a leather handle makes it easy to move from room to room; (4) it is shown on a camp table, a desk and a living room sofa.

## 3. Creative director · 创意总监
- Concept A: Quiet room — the film stays in one living room at dusk; the mist and glow fill the frame. Opening image: the glow in a dim room. Why it fits: calm and warm, but it shows one place only.
- Concept B: One mist, three places — the same unit moves from a campsite to a desk to a living room; the mist is the thread that connects them. Opening image: a thin mist rising on an open-air camp table. Why it fits: it shows range (the handle, the places) and it is the most surprising opening for a humidifier.
- Concept C: The ring of controls — a close look at the rose-gold ring and its three icons, then the unit working in the room. Opening image: the ring, in close detail. Why it fits: it is precise, but the film would then be about buttons, not air.
- Chosen · 选定: B. It is the most surprising because the cover is a campsite, not a room, and it is the most true because the four images really show three places and one mist. Concept B keeps the proposition (one soft mist, wherever you sit) and gives the audience a reason to keep watching.
- Hook (0–3 s) · 开场钩子: a thin thread of mist rises on an open-air camp table, the glow visible under the dome. The cover holds still for three bars; no name, no logo.
- Hero moment · 高潮时刻: the studio shot of the unit alone on white, mist rising, the glow lit; it lands at about 65 % of the film (the hero scene). After it, the camp image returns, now lit, to echo the cover.
- Hook line · 开场句: "A thin thread of mist, rising in the open air."
- Hero line · 高潮句: "Humidifier. Let the air soften, slowly."
- Last line · 收尾句: "Wherever you sit, the mist rises slowly."
- Title · 片名: Mist, Wherever You Sit (working title)

## 4. Copywriter · 文案
- Tagline · 口号: 让空气，慢慢变柔和 / Let the air soften, slowly
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "A thin thread of mist, rising in the open air." (cover, 0.6 s)
  - photo (living room) → "A soft blue-violet glow, low in the room." (photo, title only on screen)
  - detail (office) → "A rose-gold ring, and three quiet controls." (detail, 0.0 s)
  - statement → "Dry air makes a room hard to settle in." (statement, on screen only)
  - hero (studio) → "Mist, a glow, and a leather handle to carry it." (hero, 1.0 s)
  - finale → "Humidifier. Let the air soften, slowly." (finale, 1.2 s, the hero anchor)
  - endcard → "Wherever you sit, the mist rises slowly." (endcard, 0.6 s, the last anchor)
- On-screen words · 画面文字: photo "Evening, in the living room" / "晚上的客厅"; statement is the insight line; hero title "Humidifier" / "加湿器"; nothing else.
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés (no "premium", "stunning", "effortless").

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh, warm neutrals with the one accent colour taken from the rose-gold ring (no logo colour exists yet). Light is soft and late-afternoon in every image.
- Images · 画面选择: cover = lifestyle_camp.jpeg (the mist plume, the open-air table); photo = lifestyle_living.jpeg (glow, sofa, plant); detail = lifestyle_office.jpeg (the unit on the desk, the ring); hero = product_studio.jpeg (the unit alone, the most complete view of the ring and handle); finale = all four, the camp image leading.
- Composition rules · 构图: 16:9 landscape, margins ≥ 96 px; text sits in the lower third or in the clear sky/wall area, never over the mist or the glow; one focal point per frame (the unit).
- We will NOT show · 不出现: a fake app or screen; a Google-like browser or storefront (one generated clip was excluded for this reason); stock smiles; a person holding the product; health or medical imagery; any invented brand mark.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story — slow push-ins and slow drifts, no hard wipes. Movement follows the mist.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | the mist, no name |
| 2 | `photo` | 3 | mood | the living room, the glow |
| 3 | `detail` | 2 | texture | the ring and the three controls |
| 4 | `statement` | 2 | the feeling, named | the insight, on screen |
| 5 | `hero` | 3 | reveal | the unit alone, the name |
| 6 | `finale` | 4 | hero | the four images, the tagline |
| 7 | `endcard` | rest | close | the last line, a callback to the mist |

- Cuts · 转场: cut on bar lines only. The cuts happen where the place changes (camp → living room → office → studio).
- Breathing room · 留白: one half-bar of silence after the statement, before the hero reveal, so the unit arrives in quiet.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed ambient-air, ~88 BPM, soft pads and a low pulse. It builds gently through the living room and office, drops to near-silence before the hero, and swells on the finale.
- Silence · 静默: the half-bar before the hero reveal; the endcard lets the music settle out.
- Sound palette · 音效: no sound effects on the cover. A soft breath-like texture only at the hero (the mist), kept under the music. The office detail gets nothing.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实: "a thin mist rises" → cover and hero images show it; "a soft blue-violet glow" → living room and studio images show it; "a rose-gold ring with three quiet controls" → studio image shows the ring and three icons; "a leather handle" → studio image; "in the open air / in a room" → the four images. No claim about humidity levels, capacity, runtime, health, noise or price.
- Qualifiers · 限定条件: none in the docs (no docs were supplied). The concept status is marked in film.json chips as "Concept".
- Legibility & access · 可读与无障碍: captions on (zh + en); all on-screen text is over the clear areas; the voice-over is also in captions.
- Sign-off · 签字: approved as a concept piece only. Before any public use, the images must be replaced with real photos of the product, and a real name, logo and specs must be supplied by the user.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | one mist, three places; every beat serves it |
| Hook in 3 s · 三秒抓人 | 4 | a campsite mist plume is an unexpected opening |
| Specific, true copy · 具体真实 | 4 | every proof line names a thing visible in the images |
| Image quality & choice · 画面 | 4 | choice and staging: each image carries its own beat; the cover puts the mist plume in the upper third; the studio shot is the only clean view of the ring and handle. (Source limits, AI-generated renders, are in §1 Gaps and the report, not in this score.) |
| Restraint · 克制 | 4 | no fake UI, no numbers, no hard cuts |
| Rhythm · 节奏 | 4 | bar-line cuts; a quiet beat before the hero |
| Hero moment · 高潮 | 4 | the studio reveal after the silence |
| Memorable ending · 结尾记忆点 | 4 | the last line calls back to the mist of the cover |
