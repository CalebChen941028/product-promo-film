# Treatment · 创意方案 — Humidifier

> Written by the crew in `references/crew.md`, one section per role, in order. Replace every `write` field.
> `python3 scripts/check_treatment.py treatment.md film.json` must pass before `make_film.py --stage build`.
> 由 `references/crew.md` 中的各角色依次填写；替换所有 `write` 字段，检查通过后再构建。

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: Humidifier
- Genre · 类型: travel-hospitality-living — Travel, hospitality, home, real estate / 旅行 / 酒店 / 家居 / 地产
- Look · 风格: natural-fresh · Motion · 动效: gentle-story · Arc · 叙事结构: sensory
- Music · 音乐: composed: ambient-air ~88 BPM (original, royalty-free)
- Materials · 素材: photo 4, video 1
- Target length · 目标时长: ~65 s — 5 images/clips carry about 65 s; the sensory arc would run 75 s with more material. Do not pad: no repeats, no long holds
- Tone for this genre · 本类型的语气: atmosphere and light; invite, do not sell
- Study first · 先读: `templates/golden/sensory.json` (a top film in this arc, every scene with a `_why`) and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: none from the user. No README, brief, spec sheet or name. brief.json lists only what the four renders visibly show (a clear dome, a blue light, mist, a desk by a window); the film claims only that.

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Adults who think about the air in their own home (living room, home office). Short-form social and a product page. Sound on or off: the film must work muted, so every spoken line has a caption.
- Rights · 授权: The four stills and the mp4 are AI-generated (Gemini renders), not photographs of a shipped product. Rights to the renders and to the product design are unconfirmed. Music is composed by make_music.py (original). No logo, font or quote is used. Before any public release the user must confirm the renders depict a product they will sell.
- Gaps · 缺口: No product name, logo, specs, docs, contacts or real product photos. The name "Humidifier" is a generic placeholder. The film makes no specs, numbers or health claims, because the docs do not exist. The mp4 shows an invented shop site ("Camplox") in a mock browser, so it is not used. The campsite still implies outdoor or portable use that no doc supports, so it is not used either.

## 2. Strategist · 策略
- Audience truth · 受众真相: "I only notice the air in my home when it feels wrong."
- Insight · 洞察: We spend most of the day indoors, yet we rarely notice how a room feels until it stops feeling right. The product is about that quiet change, not about a feature list.
- Single-minded proposition · 唯一主张: A room can feel softer, hour by hour.
- Proof · 证据: Only what the renders show: mist rising from a clear dome in a lived-in room, a blue light inside the dome, a desk by a window in the afternoon. No numbers and no performance or health claims.

## 3. Creative director · 创意总监
- Concept A: "Golden hour, indoors" — the whole film is one afternoon in one room; the window light is the hero, the product only keeps the time.
- Concept B: "The window's breath" — the mist is the room breathing; a sequence of breaths that ends on one exhale.
- Concept C: "The soft hour" — every room has an hour when it feels calmer; the product marks that hour; the film opens on the mist and the room, and ends on the same room, a little softer.
- Chosen · 选定: C, "The soft hour". It is the most true (a room does change through the day, and people notice it only sometimes) and the least like a humidifier ad, because it sells a time of day, not a feature.
- Hook (0–3 s) · 开场钩子: A living room, warm and dim. Mist rises from the dome in the middle of the frame. The camera opens on the dome and the mist, then pulls back to the whole room, and the question arrives.
- Hero moment · 高潮时刻: The finale. The cover room returns, starts tight and dim, pulls to the whole frame on the downbeat at about 70 % of the film and lights up, then holds alone for about 2.5 s before the name and the tagline.
- Hook line · 开场句: "Does your room feel right this hour?" / 这个时刻，你的房间舒服吗？ (a question the viewer has asked themselves)
- Hero line · 高潮句: "Humidifier. The soft hour, every day." / 加湿器：每天一个柔和时刻。
- Last line · 收尾句: "Every room, a little softer." / 每个房间，都慢慢变柔和。 (a callback to the room and the hour of the hook)
- Title · 片名: The Soft Hour · 柔和时刻

## 4. Copywriter · 文案
- Tagline · 口号: 每天，一个柔和的时刻 / The soft hour, every day.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "Does your room feel right this hour?"
  - photo → "A desk by the window, mid-afternoon."
  - hero → "Humidifier. A clear dome, a soft blue light."
  - finale → "Humidifier. The soft hour, every day."
  - endcard → "Every room, a little softer."
- On-screen words · 画面文字: photo title "By the window, the afternoon slows" / 窗边，午后慢下来; hero title "Humidifier" / 加湿器. Nothing else.
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés; no superlatives, no exclamation marks, no numbers.

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh (warm neutrals, soft light, one accent). The one accent colour is the rose-gold band of the product, so the frame stays neutral and the product is the warmest thing in it. The blue light inside the dome is the only cool colour and it stays small.
- Each image shows · 每张图的内容:
  - `Gemini_Generated_Image_vhvjcbvhvjcbvhvj.jpeg` → indoors, a living room: a sofa with a knit throw, sheer curtains, a window, a wooden sideboard; the product with mist and a blue light, a mug, a fern.
  - `Gemini_Generated_Image_eus5wheus5wheus5.jpeg` → indoors, a home office: a wooden desk by a window, a laptop, a notebook, the product on the desk; a person reading at the edge of the frame.
  - `Gemini_Generated_Image_rhr16lrhr16lrhr1.jpeg` → product packshot on a plain white background, the dome lit blue inside; no room.
  - `Gemini_Generated_Image_7qz0iq7qz0iq7qz0.jpeg` → NOT USED: outdoors, a campsite table by a tent. It implies outdoor or portable use that no doc supports.
  - `gemini_generated_video_83248141.mp4` → NOT USED: a mock browser window with an invented shop site ("Camplox") and an outdoor scene. It is a fake UI and must not pass as real product footage.
- Images · 画面选择: The cover opens on the living room, focused on the dome and the mist (cells C2–C3 → [960,268,480,536]). The photo beat is the desk by the window. The hero is the full packshot on white, the cleanest frame of the product, saved for the reveal. The finale returns to the living room, the image that answers the cover. Each image carries one beat.
- Composition rules · 构图: one focal point per frame; margins ≥ 96 px; text sits in the calm area away from the product; captions never cover the product.
- We will NOT show · 不出现: fake browser or app UI, invented shop sites, outdoor or camping scenes, globes, handshakes, stock smiles, floating icons, close-ups that imply a feature the renders do not show.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story — slow drift and long holds, no whip cuts. It matches a film about a room that changes slowly.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | the dome and the mist first, then the room and the question |
| 2 | `photo` | 3 | mood | the desk by the window, one line |
| 3 | `hero` | 3 | reveal | the full packshot on white, the name |
| 4 | `finale` | 4 | hero | the living room returns, lights up on the downbeat |
| 5 | `endcard` | rest | close | the callback line |

- Cuts · 转场: only where the story turns: cover → photo (a slow swell), photo → hero (a soft cut from the window to the product), hero → finale (the room returns on the downbeat).
- Breathing room · 留白: the half-beat after the question, so the viewer can answer it before the photo arrives.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed ambient-air, ~88 BPM, original (make_music.py). It starts with a soft pad, opens a little on the photo beat and builds gently into the finale downbeat. No drop, no percussion.
- Silence · 静默: half a beat of silence before the finale downbeat, then the room lights up.
- Sound palette · 音效: low. A soft swell on the cover and finale cuts; a small chime only on the endcard. No sound effect for the mist, because the film must not imply a sound it cannot prove.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "Does your room feel right this hour?" → a question, not a claim.
  - "A desk by the window, mid-afternoon." → visible in the office render.
  - "Humidifier. A clear dome, a soft blue light." → visible in the packshot (clear dome, blue light inside). The name is a generic placeholder.
  - "The soft hour, every day." and "Every room, a little softer." → mood lines, not measured effects.
  - No numbers, no spec terms, no health claims, no comparisons, no "clean", "pure", "healthy" or "better sleep".
- Qualifiers · 限定条件: none in the docs (there are no docs). Nothing is claimed as available in a region, on a platform or in a plan, so no limit applies: not affected.
- Legibility & access · 可读与无障碍: captions on for every spoken line (zh and en); captions sit below the product, not over it; title text is white on the calm area with contrast ≥ 4.5:1; nothing important sits under captions.
- Sign-off · 签字: changes needed. Approved as a draft only. Before any public release the user must confirm the product name and logo, confirm that the AI renders depict a product they will sell, and confirm the rights to the images.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | "The soft hour" runs through the question, the hero line and the last line, said three different ways. |
| Hook in 3 s · 三秒抓人 | 4 | Mist rising from a dome, then a question the viewer has asked themselves. Calm, but the question holds attention. |
| Specific, true copy · 具体真实 | 4 | Every spoken line names something visible in the renders (a desk, a window, a clear dome, a blue light). No product facts, because none were supplied. |
| Image quality & choice · 画面 | 4 | Three distinct real-looking frames each carry one beat (room, desk, product), and the finale returns to the cover room. Two frames were rejected for fake UI or unsupported outdoor use. Renders, not photographs: a limit of the source, recorded in §1. |
| Restraint · 克制 | 4 | One hero moment (the finale), a slow drift, and only three cuts. |
| Rhythm · 节奏 | 4 | Question, a calm office beat, a reveal, a return; no two beats share a shape. |
| Hero moment · 高潮 | 4 | The room returns and lights up on the downbeat, answering the cover image. |
| Memorable ending · 结尾记忆点 | 4 | The last line calls back the room and the softness of the hook, and ends on the viewer's room, not the product. |
