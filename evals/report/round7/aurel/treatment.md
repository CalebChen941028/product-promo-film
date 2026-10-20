# Treatment · 创意方案 — Aurel Stoneware

> Written by the crew in `references/crew.md`, one section per role, in order.
> `python3 scripts/check_treatment.py treatment.md film.json` must pass before `make_film.py --stage build`.

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: Aurel Stoneware
- Genre · 类型: food-beverage — Food & beverage / 食品 / 饮品 / 餐饮
- Look · 风格: natural-fresh · Motion · 动效: gentle-story · Arc · 叙事结构: sensory
- Music · 音乐: composed: warm-acoustic ~98 BPM (original, royalty-free)
- Materials · 素材: cutout 3, logo 1, photo 3, text 1
- Target length · 目标时长: about 60 s (cover 3, photo 3, detail 2, statement 2, hero 4, lineup 3, finale 4 bars, then the end card)
- Tone for this genre · 本类型的语气: appetite and origin: taste, texture, hands, place
- Study first · 先读: `templates/golden/sensory.json` and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: Handmade stoneware mugs for slow coffee and tea at home. Each mug is thrown on the wheel, glazed by hand and fired twice, so no two glazes are the same. · Three glazes: sage, cream and clay · 350 ml, keeps coffee warm longer with a double-thick wall · Dishwasher safe, lead-free food-safe glaze · Made in a small studio, 40 mugs a week

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Home coffee and tea drinkers who buy handmade ware. Short social cut with sound on; the captions carry the story when sound is off.
- Rights · 授权: The photos and mug images in the folder are drawn placeholders supplied for this demo, not product photography. The logo is the placeholder brand mark. Music is composed for this film (original, no licence needed). No quotes are used.
- Gaps · 缺口: No real product photography, no real studio footage, no contacts or price. We do not fake a studio shot: the film stays on the three glazes and the facts from the brief, and the report says the imagery must be replaced before any real release.

## 2. Strategist · 策略
- Audience truth · 受众真相: "I want a mug that is mine, not one of a row of identical ones."
- Insight · 洞察: Mass-made ware is identical by design, and that sameness is what people now miss in the things they touch every morning.
- Single-minded proposition · 唯一主张: Each glaze is fired twice and never quite the same, so your mug is yours alone.
- Proof · 证据: (1) Thrown on the wheel, glazed by hand, fired twice, so no two glazes are the same. (2) Three glazes: sage, cream and clay. (3) Made in a small studio, 40 mugs a week.

## 3. Creative director · 创意总监
- Concept A: Fired twice — the kiln, not the maker, decides the last colour; one mug in steam, then the glaze that no one else has. Opening image: a single steaming mug on a warm table. Why it fits: it is the one fact in the brief that is both physical and surprising.
- Concept B: Forty a week — the small studio as the story; opening image: hands at a wheel. Why it fits: true, but it is about the maker, and the viewer is the one we need to speak to.
- Concept C: Warm for longer — the double-thick wall keeps coffee warm; opening image: steam rising from a cup. Why it fits: useful, but a feature, and it could be any mug.
- Chosen · 选定: A. It is the most surprising (a glaze that is never repeated) and the most true (fired twice, glazed by hand). It reaches the audience's own life: their morning mug.
- Hook (0–3 s) · 开场钩子: The cover photo fills the frame: one steaming mug on a warm table, with a soft pad under it. The voice says the hook line over the image. The logo does not appear.
- Hero moment · 高潮时刻: The sage mug lights up alone on the stage after the statement beat (about 55–65 % of the film): "Thrown on the wheel. Glazed by hand. Fired twice." This is the one moment the audience should remember.
- Hook line · 开场句: "Fired twice. No two glazes match."
- Hero line · 高潮句: "Aurel. Never the same glaze twice." (six words, with the name)
- Last line · 收尾句: "Fired twice. Yours alone." — a callback to the hook's "fired twice" and the same idea of one glaze, ending on the viewer.
- Title · 片名: Fired Twice

## 4. Copywriter · 文案
- Tagline · 口号: 每一次釉色，都只此一次 / Never the same glaze twice.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "Fired twice. No two glazes match." — the hook: a fact stated as a tension.
  - photo (shelf) → "Each one is made by hand, one at a time." — proof: the making, with the three glazes shown on screen.
  - detail (glaze) → "Glazed by hand. Never quite the same." — proof: texture, named as the hand's work.
  - statement → (no voice: the line is on screen and breathes on its own; a calm beat before the reveal) — "Made in a small studio. 40 mugs a week." on screen.
  - hero (sage mug) → "Thrown on the wheel. Glazed by hand. Fired twice." (zh: 两次烧制，每只釉色都独一无二) — the reveal, the process in three verbs, no adjectives.
  - lineup (clay, cream, sage) → (no voice: the range is shown, the three glazes are already named in the photo beat).
  - finale → "Aurel. Never the same glaze twice." — the hero line, with the name.
  - endcard → "Fired twice. Yours alone." — the last line, a callback to the hook.
- On-screen words · 画面文字: photo title "Three glazes" / 三种釉色; statement "Made in a small studio. 40 mugs a week." / 小工作室，每周 40 只; hero title "Aurel Stoneware" / 手作陶瓷马克杯; lineup labels Clay / 陶土, Cream / 奶油, Sage / 鼠尾草; finale tagline captions hidden (already on screen); endcard chips "350 ml", "Dishwasher safe", "Lead-free glaze".
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés. No adjectives in the proof lines; no "premium", "handcrafted with love", "perfect".

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh. The one accent colour is the logo's sage green (the "A" disc), and everything else stays warm neutral, matching the cream and clay of the mugs. Two typefaces at most, set by the style.
- Images · 画面选择: The cover uses the morning-table image (one mug, steam, full-bleed), the best single image, and it bookends the finale. The shelf photo carries the three glazes in one frame. The glaze detail carries the texture beat. The sage cut-out carries the hero reveal alone, so the hero image is not diluted by the lineup. The lineup then shows all three.
- Composition rules · 构图: Margins of 96 px or more; text sits in the lower third over a soft scrim, never on the mug; one focal point per frame (the mug or the glaze), never two things competing.
- We will NOT show · 不出现: stock smiles, hands holding mugs in a stock kitchen, globes, leaves, bean icons, fake UI, fake studio sets, a logo before the hero.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story — slow push-ins, soft cuts; the hero lights up and breathes, matching a handmade, unhurried product.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | photo full-bleed, voice carries the hook |
| 2 | `photo` | 3 | proof: three glazes | shelf photo, one fact spoken |
| 3 | `detail` | 2 | texture | short; glaze close-up with one line |
| 4 | `statement` | 2 | calm | one line on screen, the breath before the reveal |
| 5 | `hero` | 4 | reveal | the sage mug alone; the one hero moment (~50–65 %) |
| 6 | `lineup` | 3 | range | clay, cream, sage side by side; silent by design |
| 7 | `finale` | 4 | hero line | morning-table bookend returns, tagline |
| 8 | `endcard` | rest | close | the callback line on the end card |

- Cuts · 转场: Soft cuts throughout. A cut only where the story turns: cover to shelf (from the mug to the range), and statement to hero (the breath before the reveal).
- Breathing room · 留白: The statement and the lineup are the rest beats. After two dense beats (photo, detail), the statement gives the audience a moment before the hero.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed warm-acoustic, ~98 BPM, original and royalty-free. Builds gently through the photo and detail, drops to a pad under the statement, rises into the hero, and resolves on the finale.
- Silence · 静默: half a beat of silence before "Thrown on the wheel." and before "Fired twice. Yours alone."
- Sound palette · 音效: low and warm. A soft ceramic tick at the hero reveal only; no whooshes, no risers beyond the hero.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "Fired twice" / "Thrown on the wheel. Glazed by hand. Fired twice." → README: "thrown on the wheel, glazed by hand and fired twice."
  - "No two glazes match" / "Never the same glaze twice" → README: "so no two glazes are the same."
  - "Three glazes: sage, cream and clay." → README: "Three glazes: sage, cream and clay."
  - "Made in a small studio. 40 mugs a week." → README: "Made in a small studio, 40 mugs a week."
  - "Dishwasher safe", "Lead-free glaze" (chips) → README: "Dishwasher safe, lead-free food-safe glaze."
  - "350 ml" (chip) → README: "350 ml."
  - No claim about warmth beyond the README; the double-thick wall is not used on screen in this cut.
- Legibility & access · 可读与无障碍: captions on for every line; contrast is checked on the cream and sage backgrounds; nothing important sits under the captions.
- Sign-off · 签字: approved for this demo, with one condition: the imagery is drawn placeholder art and must be replaced with real product photography before any real release.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 5 | "Fired twice, so no two glazes match" reaches the hook, the hero line and the last line. |
| Hook in 3 s · 三秒抓人 | 4 | The steaming mug and the line "No two glazes match" land at once; the placeholder image limits it. |
| Specific, true copy · 具体真实 | 4 | Every proof line carries a fact from the README; no adjectives. |
| Image quality & choice · 画面 | 3 | Drawn placeholder images, chosen and staged well (the sage cut-out gets the hero alone), but they are not real photography, so the score stays at 3. |
| Restraint · 克制 | 5 | One hero, two calm beats, no extra effects. |
| Rhythm · 节奏 | 4 | Dense, calm, hero, range, close; the statement breathes before the reveal. |
| Hero moment · 高潮 | 4 | The sage mug alone at about 55–65 %, with three verbs. |
| Memorable ending · 结尾记忆点 | 4 | The callback "Fired twice. Yours alone." closes on the viewer. |
