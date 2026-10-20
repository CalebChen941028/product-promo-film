# Treatment · 创意方案 — Humidifier

> Written by the crew in `references/crew.md`, one section per role, in order. Replace every `write` field.
> `python3 scripts/check_treatment.py treatment.md film.json` must pass before `make_film.py --stage build`.
> 由 `references/crew.md` 中的各角色依次填写；替换所有 `write` 字段，检查通过后再构建。

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: Humidifier
- Genre · 类型: travel-hospitality-living — Travel, hospitality, home, real estate / 旅行 / 酒店 / 家居 / 地产 (overrode autofilm's food-beverage close call: a home appliance, not food)
- Look · 风格: natural-fresh · Motion · 动效: gentle-story · Arc · 叙事结构: sensory
- Music · 音乐: composed: ambient-air ~88 BPM (original, royalty-free)
- Materials · 素材: photo 4 (AI-generated renders), video 1 (1280×720, 10 s, not used)
- Target length · 目标时长: ~49 s, six scenes. No padding: no repeats, no long holds
- Tone for this genre · 本类型的语气: atmosphere and light; invite, do not sell
- Study first · 先读: `templates/golden/sensory.json` and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: none. No README or brief was supplied. The only facts are what the renders show: a white dome with a frosted top and a fine mesh crown, a rose-gold ring with three control icons, a leather carry handle, a soft blue-violet light inside, and a mist plume

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: people who want a calm, lived-in room (home, study, travel). Sound on or off; 16:9 for web. Draft only: not for publishing as an ad for a real product
- Rights · 授权: the four images and the video are AI-generated renders (Gemini), not photographs of a manufactured product. Confirm with the user who made them and that they may be used. Music is composed by `make_music.py` (original). Voice is Kokoro am_michael (Apache-2.0). No logo, no quotes, no real people
- Gaps · 缺口: no README, brief, spec sheet, brand name, logo, price, contacts or real product photo. The film therefore makes no product claims. The brand name "Humidifier" is a generic placeholder. The video is not used. Packshot is a render on white, so the detail beat uses crops of it, not a cut-out. The logo is a PLACEHOLDER wordmark (`placeholder-logo.png`, text "Humidifier" in the rose-gold accent), made because none was supplied; replace it with the real logo before any use

## 2. Strategist · 策略
- Audience truth · 受众真相: "I want the place I sit to feel softer than it did this morning."
- Insight · 洞察: the air in a place is the one thing nobody sees, yet it sets how long we stay in it
- Single-minded proposition · 唯一主张: Wherever you sit down, the air can be soft.
- Proof · 证据: the materials show the same device in three places: a campsite table, a study desk, a living room. That is the only proof available; no product facts are claimed

## 3. Creative director · 创意总监
- Concept A: Morning first — the mist rises before the day starts. Opening image: a campsite table at dawn. Fits the calm, but is a time-of-day idea and gives no link between places.
- Concept B: The breath of a room — the mist as the room breathing out. Opening image: the mist plume above the dome. Fits the material, but is abstract and hard to tie to a place.
- Concept C: Wherever you sit down — the same device, in three ordinary places, the air is already moving. Opening image: the campsite table, mist rising before anyone speaks. Fits all the materials.
- Chosen · 选定: C. It is the most true to the materials (the device really appears in three places) and the most surprising (a campsite and a study share one ordinary object without any explanation).
- Hook (0–3 s) · 开场钩子: the campsite table, full frame, the mist plume already rising from the dome; the camera starts on the dome and pulls back to the whole table and tent
- Hero moment · 高潮时刻: the campsite image returns as a bookend (tight and dim, then whole and lit) at about 65 %, with the name and tagline on the downbeat
- Hook line · 开场句: "Before anyone speaks, the mist is already rising."
- Hero line · 高潮句: "Humidifier. Soft air, wherever you sit."
- Last line · 收尾句: "Sit down. The mist is already rising."
- Title · 片名: 哪里坐下 · Wherever You Sit (working title)

## 4. Copywriter · 文案
- Tagline · 口号: 哪里坐下，哪里就有柔雾。 / Soft air, wherever you sit.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "Before anyone speaks, the mist is already rising." (zh: 还没人开口，雾已经升起。)
  - photo → "Pages turn slowly beside the window. The mist rises with them." (zh: 书页在窗边慢慢翻，雾跟着升起。)
  - detail → "A fine mesh crown. Three quiet controls, in rose gold." (zh: 细密的网罩，三个安静的按键，玫瑰金色。)
  - hero → "The same soft mist, now on a sideboard by the sofa." (zh: 同一缕柔雾，此刻落在沙发旁的矮柜上。)
  - finale → "Humidifier. Soft air, wherever you sit." (zh: 加湿器：哪里坐下，哪里就有柔雾。)
  - endcard → "Sit down. The mist is already rising." (zh: 坐下吧，雾已经升起。)
- On-screen words · 画面文字: 窗边书桌 / By the window, a desk (photo title); 加湿器 / Humidifier (hero title). Nothing else on screen
- Banned words checked · 已排除空话: yes — ran `lint_copy.py`; no product claims, no superlatives, no travel clichés ("getaway", "escape", "paradise")

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh. The accent is the rose-gold of the device ring, the only warm colour; everything else stays neutral. No logo exists, so no accent is taken from one
- Each image shows · 每张图的内容:
  - `Gemini_Generated_Image_7qz0iq7qz0iq7qz0.jpeg` → outdoors: a campsite folding table beside a tent, a river and mountains behind; the humidifier is on the table with mugs, a notebook and a phone
  - `Gemini_Generated_Image_eus5wheus5wheus5.jpeg` → indoors: a study by a window, a desk with a laptop and books, a plant, and the humidifier on the desk with mist rising
  - `Gemini_Generated_Image_rhr16lrhr16lrhr1.jpeg` → product: the humidifier alone on a white background, lit from inside, mist above (a render). Used as two macro crops: the mesh crown and the control ring
  - `Gemini_Generated_Image_vhvjcbvhvjcbvhvj.jpeg` → indoors: a living room with a sofa and a knitted throw, the humidifier on a wooden sideboard, a plant, a cup and a small bottle
  - `gemini_generated_video_83248141.mp4` → not used. Its content was not reviewed; adding it would require a .webm conversion and a clip beat it does not need
- Images · 画面选择: the campsite render carries the cover and the finale bookend (it is the hook image). The desk render carries the photo beat. The white packshot, cropped to the mesh crown and the control ring, carries the texture beat (texture before the whole). The warm living-room render carries the hero, because it is the most lit and lived-in frame and the reveal lands in it
- Composition rules · 构图: one focal point per frame (the humidifier). Titles sit on the soft scrim, away from the product. Margins ≥ 96 px. No text over the device
- We will NOT show · 不出现: fake UI, a logo that does not exist, people looking at the camera, stock smiles, globes, handshakes, any real brand or product name beyond the generic placeholder

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story. Slow push-ins and pulls; the mist and the light do the moving. Nothing flashes
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | campsite, starts on the dome, pulls back to the table |
| 2 | `photo` | 3 | mood | the study desk, a calm beat after the hook |
| 3 | `detail` | 2 | texture | two macro crops of the packshot: mesh crown, then control ring |
| 4 | `hero` | 3 | reveal | the living room lights up, name on the scrim |
| 5 | `finale` | 4 | hero | the campsite image returns, tagline on the downbeat |
| 6 | `endcard` | 3 | close | the last line echoes the hook |

- Cuts · 转场: cut into the detail (macro) and into the finale (bookend) only. The other beats use the style's default soft dissolve
- Breathing room · 留白: the photo is the calm beat between the hook and the macro detail. The hero is held about 3 s before the name, so the product is seen before it is named

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed ambient-air, ~88 BPM, original. It rises gently under the photo, dips into the macro detail and lifts into the hero and finale
- Silence · 静默: a half-beat of silence before the hero. No other held silence
- Sound palette · 音效: kept low. A soft air sound under the mist beats; no sound on the detail beyond the music. No sound on the endcard but the music ring-out

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实: the film makes no product claims. Every line describes what the renders show (a mesh crown, three controls, a rose-gold ring, a window, a desk, a sideboard, a sofa). "Soft air" and "the air can be soft" are the proposition, not a measurable claim (no humidity level, no room size, no health effect)
- Qualifiers · 限定条件: none in the docs (there are no docs). The film claims no hours, no room sizes, no health benefit, no availability. Not affected
- Legibility & access · 可读与无障碍: captions on in Chinese and English; the scrim keeps titles readable; nothing important sits under the captions
- Sign-off · 签字: changes needed. The film is a draft. It must not go out as an advertisement for a real product until the user confirms the renders are approved for use, and supplies the real name, logo, product facts and a real product photograph

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | "Wherever you sit down" is carried by the copy (sit down, the mist) and by the images (three places) |
| Hook in 3 s · 三秒抓人 | 4 | the mist already rising in a campsite is a physical detail, and the camera starts on it |
| Specific, true copy · 具体真实 | 4 | each line names something concrete on screen (a window, a desk, a mesh crown, a sideboard) and is true to that image, and the hook and last line are quotable. The missing product facts are a material limit, recorded in Gaps, not a writing shortfall |
| Image quality & choice · 画面 | 4 | each beat has a clear image; the macro crops give a real texture beat; the warm living-room frame carries the hero. The renders are AI-generated, a limit noted in Rights and Gaps |
| Restraint · 克制 | 4 | one hero, no effects beyond the style's |
| Rhythm · 节奏 | 4 | 3/3/2/3/4/3 bars with one calm beat between dense ones |
| Hero moment · 高潮 | 4 | the bookend returns the hook image, so the hero answers the hook |
| Memorable ending · 结尾记忆点 | 4 | "Sit down. The mist is already rising." echoes the hook |
