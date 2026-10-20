# Treatment · 创意方案 — Aurel Stoneware

> Written by the crew in `references/crew.md`, one section per role, in order. Replace every `write` field.
> `python3 scripts/check_treatment.py treatment.md film.json` must pass before `make_film.py --stage build`.
> 由 `references/crew.md` 中的各角色依次填写；替换所有 `write` 字段，检查通过后再构建。

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: Aurel Stoneware
- Genre · 类型: food-beverage — Food & beverage / 食品 / 饮品 / 餐饮
- Look · 风格: natural-fresh · Motion · 动效: gentle-story · Arc · 叙事结构: sensory
- Music · 音乐: composed: warm-acoustic ~98 BPM (original, royalty-free)
- Materials · 素材: cutout 3, logo 1, photo 3, text 1
- Target length · 目标时长: ~75 s
- Tone for this genre · 本类型的语气: appetite and origin: taste, texture, hands, place
- Study first · 先读: `templates/golden/sensory.json` (a top film in this arc, every scene with a `_why`) and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: Handmade stoneware mugs for slow coffee and tea at home. Each mug is thrown on the wheel, glazed by hand and fired twice, so no two glazes are the same. · Three glazes: sage, cream and clay · 350 ml, keeps coffee warm longer with a double-thick wall · Dishwasher safe, lead-free food-safe glaze · Made in a small studio, 40 mugs a week

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: People who make slow coffee or tea at home and buy a mug for it. Social feed, sound often off, so the captions carry the film; a 16:9 cut for the web.
- Rights · 授权: Materials are the project's own drawn placeholders (README: "Images are drawn placeholders, not product photos"). Music is composed by make_music.py (original). Voice is Kokoro am_michael, already downloaded. No quotes are used.
- Gaps · 缺口: No real product photography, so the film shows the placeholder images as-is and says nothing a photo would have to prove. Real photos of the glaze and the studio would replace the cover, the shelf and the detail beat. No contact details in the docs, so the end card has no contacts.

## 2. Strategist · 策略
- Audience truth · 受众真相: "I want a mug that feels like mine, not like one from a shop shelf."
- Insight · 洞察: A mug is bought as a set of identical things, but the person who uses it wants one that is theirs. Handmade work is the only way to get that, and it shows only in the glaze.
- Single-minded proposition · 唯一主张: Every mug is glazed by hand, so no two are the same.
- Proof · 证据: (1) thrown on the wheel, glazed by hand, fired twice, so no two glazes are the same; (2) three glazes: sage, cream and clay; (3) 350 ml with a double-thick wall that keeps coffee warm longer; (4) made in a small studio, 40 mugs a week.

## 3. Creative director · 创意总监
- Concept A: "Made once" — the mug is one of forty made that week; the opening image is a single mug on a table, the studio count as the frame.
- Concept B: "Warm longer" — the double-thick wall keeps coffee warm; the opening image is steam over the cup, the film is about a slower morning.
- Concept C: "No two alike" — the glaze is the unrepeatable part; the opening image is a close glaze texture that could be any colour until the camera pulls back to the mug.
- Chosen · 选定: C. It is the most surprising (a glaze texture first, not the object) and the most true (fired twice, so no two glazes are the same). A stays as a beat (photo), B stays as a fact (350 ml).
- Hook (0–3 s) · 开场钩子: The morning-table image, a single mug with steam rising, played full frame. The voice says the hook line over the first 1 s, with a quiet hold on the mug.
- Hero moment · 高潮时刻: The single sage mug lit on the stage, the name, and the three words "Thrown on the wheel. Glazed by hand. Fired twice." It lands at roughly 60–70 % through the film, in the finale and reveal.
- Hook line · 开场句: "No two glazes are the same."
- Hero line · 高潮句: "Aurel. No two alike."
- Last line · 收尾句: "The same morning. A different mug." (callback: the cover image of a morning with a mug)
- Title · 片名: No two alike

## 4. Copywriter · 文案
- Tagline · 口号: 没有两只一样 / No two alike
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "No two glazes are the same." (hook)
  - photo → "Made in a small studio, forty mugs a week." (no proof beyond the fact in the docs)
  - detail → (no voice: the glaze texture is the beat; the music carries it)
  - hero → "Aurel. Thrown on the wheel. Glazed by hand. Fired twice." (name + the craft)
  - lineup → (no voice: the three colours and the 350 ml fact are on screen)
  - finale → "Aurel. No two alike." (hero line)
  - endcard → "The same morning. A different mug." (last line, callback to the cover)
- On-screen words · 画面文字: photo "Three glazes. One shelf." / 三种釉色，一排架子 · lineup title "350 ml, double-thick wall" / 350 毫升，双层厚壁 · colour labels Clay / 陶土, Cream / 奶白, Sage / 鼠尾草 · hero title "Aurel Stoneware" / Aurel 陶瓷
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh. The accent colour is the logo's sage green, taken from the logo circle. Everything else is warm neutral from the photos.
- Images · 画面选择: cover = morning-table (a mug in use, a place: the table and steam); photo = shelf (three glazes together, the studio beat); detail = glaze-detail (the glaze texture, the concept); hero = single mug-sage cutout (the reveal, one colour, one object); lineup = the three cutouts (clay, cream, sage); finale = morning-table again as a bookend, the same frame as the cover, so the last image is the first. The best image, the one with a subject in use, carries the cover and the bookend.
- Composition rules · 构图: one focal point per frame; text sits in the lower third on a soft scrim; margins ≥ 96 px; no text on the mug.
- We will NOT show · 不出现: globes, handshakes, light bulbs, stock smiles, floating icons, fake dashboards; no fake product photography; no lifestyle people who are not in the materials.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story — slow push-ins and soft dissolves that suit a slow morning and a quiet product.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | the mug in use, full frame |
| 2 | `photo` | 3 | place | the studio count, the shelf |
| 3 | `detail` | 2 | texture | silent: the glaze is the beat |
| 4 | `hero` | 4 | reveal | one sage mug, the name |
| 5 | `lineup` | 3 | range | three glazes, 350 ml fact |
| 6 | `finale` | 4 | hero | bookend, the tagline |
| 7 | `endcard` | 3 | close | the callback |

- Cuts · 转场: Cuts only where the story turns: cover to photo (from the mug in use to the place), and hero to lineup (from one mug to the range). Everything else dissolves gently.
- Breathing room · 留白: After the photo beat, the detail beat is silent for two bars so the glaze texture can be seen. The hero reveal holds on the single mug for half a bar before the name appears.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed warm-acoustic at ~98 BPM, an original underscore. It rises gently into the hero reveal and lowers again for the lineup.
- Silence · 静默: A half-beat of silence before the hero line in the finale, and two silent bars on the detail beat.
- Sound palette · 音效: kept low. A soft ceramic-like tick on the hero reveal, nothing on the cover or the lineup, so the film stays felt, not heard.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "No two glazes are the same" → README: "glazed by hand and fired twice, so no two glazes are the same"
  - "Thrown on the wheel. Glazed by hand. Fired twice." → README: same sentence
  - "Made in a small studio, forty mugs a week" → README: "Made in a small studio, 40 mugs a week"
  - "350 ml, double-thick wall" → README: "350 ml, keeps coffee warm longer with a double-thick wall"
  - three glazes sage, cream, clay → README: "Three glazes: sage, cream and clay"
  - no claim about dishwasher safety or lead-free glaze is used on screen (not needed for this film)
- Legibility & access · 可读与无障碍: captions on for every voice line; contrast checked on the scrim; nothing important under captions.
- Sign-off · 签字: approved, with the placeholder caveat: the film is a demo cut from drawn placeholder images, not a shipping product film.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 5 | One sentence: no two alike. Every beat is about the glaze or the hand that makes it. |
| Hook in 3 s · 三秒抓人 | 4 | The mug in use with steam, then the line "No two glazes are the same." |
| Specific, true copy · 具体真实 | 4 | Each proof line carries a fact from the README (wheel, hand glaze, fired twice, 350 ml, 40 a week). |
| Image quality & choice · 画面 | 4 | Each beat has its image; the cover and the bookend share the best frame. The images are placeholders, so the ceiling is capped (see Gaps). |
| Restraint · 克制 | 4 | Two silent beats, one hero, no effects beyond the cinema defaults. |
| Rhythm · 节奏 | 4 | Dense, then calm (detail), then the hero, then the range. |
| Hero moment · 高潮 | 4 | The single sage mug is the one moment to remember. |
| Memorable ending · 结尾记忆点 | 4 | The callback to the cover: the same morning, a different mug. |
