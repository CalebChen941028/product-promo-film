# Treatment · 创意方案 — Humidifier

> Written by the crew in `references/crew.md`, one section per role, in order. Replace every `write` field.
> `python3 scripts/check_treatment.py treatment.md film.json` must pass before `make_film.py --stage build`.
> 由 `references/crew.md` 中的各角色依次填写；替换所有 `write` 字段，检查通过后再构建。

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: Humidifier
- Genre · 类型: food-beverage — Food & beverage / 食品 / 饮品 / 餐饮 (autofilm close call with travel-hospitality-living; kept as drafted, see §1)
- Look · 风格: natural-fresh · Motion · 动效: gentle-story · Arc · 叙事结构: sensory
- Music · 音乐: composed: warm-acoustic ~98 BPM (original, royalty-free)
- Materials · 素材: photo 4, video 1 (the video is not used: it shows generated browser and app windows, not the product)
- Target length · 目标时长: ~45 s — 4 stills carry the film; the finale reuses them as a callback, so nothing repeats in a row
- Tone for this genre · 本类型的语气: appetite and origin — NOT applied. A humidifier is not food; the copy speaks about air, light and the room
- Study first · 先读: `templates/golden/sensory.json` and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: `brief.json` in this folder, hand-filled from what the images show (mist from the dome, blue glow, frosted dome, rose-gold ring, leather handle). No spec sheet was supplied

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: People who live with the air in their home or who like calm outdoor and desk setups. Short vertical and landscape social cuts, sound on or off (captions carry the voice).
- Rights · 授权: The four stills and the clip were supplied by the user. The file names show they are AI-generated images (Gemini), not photographs of a shipped product, so they are not evidence of real product performance. Ownership and use rights for the images are to be confirmed by the user. Music is original, composed by `make_music.py`. Voice is Kokoro am_michael (Apache-2.0), already downloaded.
- Gaps · 缺口: No brief, no brand name, no logo, no contacts, no spec sheet. Name is the generic word "Humidifier" and the logo is a labelled text placeholder (`brand/logo-PLACEHOLDER.png`). Genre: autofilm's close call (food-beverage vs travel-hospitality-living) kept as drafted, since the user could not be asked; switching to travel-hospitality-living only changes the music default. The clip is left out because it shows generated browser windows. Nothing is claimed beyond what the images show.

## 2. Strategist · 策略
- Audience truth · 受众真相: "The air in my room is just air. I never think about it."
- Insight · 洞察: We stop noticing the things that quietly shape how a room feels, so a good object only gets credit when it makes the air visible.
- Single-minded proposition · 唯一主张: Soft mist and warm light, in the room you live in.
- Proof · 证据: (1) a plume of mist rises from the dome in the studio, office and living-room shots; (2) a blue glow shows through the frosted dome; (3) the same object sits in three settings: an outdoor camp table, a home office, a living room.

## 3. Creative director · 创意总监
- Concept A: Noticing — the film makes the unnoticed air visible, one mist plume at a time — opens on the camp table with the plume rising against the trees — the viewer sees the air before they hear the claim.
- Concept B: Four rooms, one light — the same glow in a camp, an office, a living room and a white studio, cut between them — opens on the glow — the object is a constant, the places change.
- Concept C: Room air with a texture — the air in a room becomes something you can see and feel: frost, glow, mist — opens on the plume against the trees — the film turns a commodity into a sensation, which is true to what the frames show.
- Chosen · 选定: C — the most surprising, because it asks the viewer to see air as a material; the most true, because the mist and the frosted glass are in every frame.
- Hook (0–3 s) · 开场钩子: Camp table, soft morning light. A plume of mist rises from the humidifier against the trees. The voice speaks the hook line over the image.
- Hero moment · 高潮时刻: The white studio shot. Mist curls up from the dome and the blue glow lights the frosted glass. It lands in the finale, at about 70 % of the film, and the finale returns to the opening camp frame so the film answers its own hook.
- Hook line · 开场句: A room's air has a texture. Nobody notices.
- Hero line · 高潮句: Humidifier. Soft mist. Warm light.
- Last line · 收尾句: Now you can feel the air.
- Title · 片名: The Air, Softened (working)

## 4. Copywriter · 文案
- Tagline · 口号: 柔雾，暖光。 / Soft mist. Warm light.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "A room's air has a texture. Nobody notices."
  - photo → "Mist drifts past a quiet desk by the window."
  - detail → "The frosted shell glows warm from within."
  - hero → "A rose-gold ring frames the glowing dome."
  - finale → "Humidifier. Soft mist. Warm light."
  - endcard → "Now you can feel the air."
- On-screen words · 画面文字: photo title 雾气，慢慢升起 / Mist, rising slowly (≤ 42 chars). Hero title 加湿器 / Humidifier. Nothing else on screen: the images carry the rest.
- Banned words checked · 已排除空话: yes — ran lint_copy.py through make_film.py --stage check; no clichés in the spoken lines.

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh. The one accent colour is the rose-gold of the product's own ring (no brand colour was supplied). Warm neutrals, soft blue glow, the white studio shot as the cleanest frame.
- Images · 画面选择: cover = the camp table (the wide, soft frame, mist against trees); photo = the home office (desk, window, mist); detail = the living room, cropped to the frosted dome and the warm light; hero = the white studio shot (the best image, kept for the reveal); finale = the four stills cycle and the camp frame returns to close the loop.
- Composition rules · 构图: Margins ≥ 96 px. One focal point per frame: the humidifier. Text sits on the lower third with a soft scrim. Only one accent colour.
- We will NOT show · 不出现: screen recordings or browser windows (the clip is not used), fake UI, people's faces in close-up, stock smiles, handshakes, globes, medical or skincare imagery, essential oil bottles, any number on screen, any claim of health or room humidity levels.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story — slow push-ins and soft dissolves suit a calm, sensory product; no whips, no hard glitches.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 4 | hook | camp table, mist against trees; cold open, no name |
| 2 | `photo` | 4 | life | office desk and window, mist |
| 3 | `detail` | 2 | texture | living room crop: frosted dome and warm light |
| 4 | `hero` | 3 | reveal | white studio shot; the name lands here |
| 5 | `finale` | 4 | hero | the camp frame returns (callback to the hook) and the four stills resolve |
| 6 | `endcard` | rest | close | logo, name, positioning, last line |

- Cuts · 转场: Cuts fall on bar lines. Soft swells between cover, photo and detail. A slightly longer dissolve into the hero, where the story turns from the air to the object.
- Breathing room · 留白: A half-beat of near silence before the hero line in the finale, so the name lands on a held frame.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: original composed underscore, warm-acoustic, ~98 BPM. Builds gently through the photo and detail, lifts at the hero, holds under the finale, rings out under the endcard.
- Silence · 静默: The half-beat before the hero line in the finale.
- Sound palette · 音效: one soft chime on the logo, a quiet swell on the hero cut. No hiss or whoosh on the mist itself; the image carries it. No UI sounds.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "a room's air has a texture" → an opinion about the air, not a product claim; no fact to check;
  - "a plume of mist rises from the dome" → visible in the studio, office and living-room stills;
  - "a blue glow through the frosted dome" → visible in the studio, office and living-room stills;
  - "frosted glass, a warm glow, soft edges" → visible in the living-room still and the studio shot;
  - "a rose-gold ring and a leather handle" → visible in the studio shot;
  - "soft mist, warm light" → the film's proposition; the same visible facts.
  No spec, number, health, performance or humidity claim is made.
- Qualifiers · 限定条件: none in the docs. No edition, region, plan or beta is claimed. The stills are AI-generated renders and the film says nothing about real-world performance.
- Legibility & access · 可读与无障碍: captions on for every spoken line; contrast on the scrim checked; nothing important sits under captions.
- Sign-off · 签字: draft approved for the film, with changes needed before publication: real brand name, real logo (the current one is a labelled placeholder), contacts and rights confirmation for the images.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | One idea: the room's air as something seen. Every beat serves it. |
| Hook in 3 s · 三秒抓人 | 4 | The camp frame with mist against trees, and a line that names what nobody notices. |
| Specific, true copy · 具体真实 | 3 | Lines only name what the stills show; there is no spec sheet, so the copy cannot be more specific without inventing facts. |
| Image quality & choice · 画面 | 4 | Four clean, consistent stills; the studio shot is the strongest; the office and living-room frames are warm and calm. |
| Restraint · 克制 | 5 | Six scenes, one hero, no effects that are seen rather than felt. |
| Rhythm · 节奏 | 4 | Cuts on bar lines; the finale callback closes the loop. |
| Hero moment · 高潮 | 4 | The studio mist and glow, resolved in the finale. |
| Memorable ending · 结尾记忆点 | 4 | "Now you can feel the air" calls back to "nobody notices". |
