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
- Audience & where it plays · 受众与投放渠道: gift and home-coffee shoppers, in social feeds; mostly watched sound-off, so captions stay on. 16:9 cut first; a vertical cut later if needed.
- Rights · 授权: the brand "Aurel Stoneware", the logo and every image are demo placeholders supplied in the materials (drawn, not photographs). Music is original, composed by make_music.py. No quotes and no testimonials are used.
- Gaps · 缺口: no real product photos, so every image is a labelled drawn placeholder; no contact details in the docs, so the contacts are left empty; no real customer quote. Voice is am_michael (already downloaded). The genre's suggested af_heart would be a download that has not been approved, so it is not used.

## 2. Strategist · 策略
- Audience truth · 受众真相: "Every morning I reach for the same mug, and it could be anyone's."
- Insight · 洞察: people want one small daily object to feel like theirs, but a mug that matches its twin perfectly feels like it came off a shelf.
- Single-minded proposition · 唯一主张: Each Aurel mug is glazed by hand, so no two are alike.
- Proof · 证据: each glaze is applied by hand and the mug is fired twice; three glazes (sage, cream, clay); 350 ml with a double-thick wall that keeps coffee warm longer.

## 3. Creative director · 创意总监
- Concept A: No two alike — every glaze runs its own way, so every mug is its own — opening: a slow macro of green glaze with one streak of colour — why it fits: it is the one fact a matching set can never claim.
- Concept B: The first cup — the quiet ritual of slow coffee and tea at home — opening: a steaming mug on a sunlit table — why it fits: the moment the viewer already owns, though it could sell any ceramic.
- Concept C: Shelf of three — the range shown at once, the mugs as a family — opening: three mugs in a row on a wooden shelf — why it fits: a clear catalogue image, safe, but with no reason to care.
- Chosen · 选定: A — because it is the most surprising idea for a mug (a mug is meant to match) and the most true (the docs say every glaze is different).
- Hook (0–3 s) · 开场钩子: a slow macro of green glaze drifting in soft light, no product name on screen; the voice says "No two glazes are the same."
- Hero moment · 高潮时刻: the three glazes standing in a row (clay, cream, sage) in the lineup, the one image people remember; it lands about two-thirds of the way through.
- Hook line · 开场句: No two glazes are the same.
- Hero line · 高潮句: Aurel. Three glazes, no two alike.
- Last line · 收尾句: Your glaze. No one else has the same.
- Title · 片名: No Two Alike

## 4. Copywriter · 文案
- Tagline · 口号: 三种釉色，没有两件相同 / Three glazes. No two alike.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "No two glazes are the same."
  - photo → "Made for slow coffee and tea at home."
  - hero → "Thrown on the wheel, glazed by hand, fired twice."
  - feature → "The double-thick wall keeps coffee warm for longer."
  - lineup → "Sage, cream or clay."
  - finale → "Aurel. Three glazes, no two alike."
  - endcard → "Your glaze. No one else has the same."
- On-screen words · 画面文字: photo "在家，慢慢喝 / Slow coffee, at home"; hero "手工陶瓷马克杯 / Aurel Stoneware"; feature "350 ml，双层厚壁 / Double-thick wall, 350 ml"; lineup labels "陶土色 / Clay", "奶白色 / Cream", "鼠尾草绿 / Sage". Nothing repeats the voice-over.
- Banned words checked · 已排除空话: pending lint_copy.py (see the report).

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh. The one accent colour is the sage green of the logo; no other accent is used. Two typefaces at most, as the style sets them.
- Images · 画面选择: cover = glaze-detail (texture before the whole, the concept as an image); photo = morning-table (mood, a drawn placeholder, labelled as such); hero = mug-sage (the reveal, one glaze carries the name); feature = shelf (the range in context, text on a scrim); lineup = mug-clay, mug-cream, mug-sage (the three glazes, the hero moment); finale = the six images as a wall; endcard = logo.
- Composition rules · 构图: one focal point per frame, margins ≥ 96 px, text never on a bright edge, captions clear of the product.
- We will NOT show · 不出现: globes, handshakes, stock smiles, floating icons, fake UI, steam-and-sunlight clichés beyond the placeholder art, invented customer quotes.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story. Calm, slow push-ins; it suits a craft object and a sensory brief.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | texture first, the concept as a line |
| 2 | `photo` | 3 | mood | the place and the ritual |
| 3 | `hero` | 4 | reveal | one mug lights up and breathes |
| 4 | `feature` | 5 | craft + facts | photo frame, four short points |
| 5 | `lineup` | 3 | hero | three glazes side by side |
| 6 | `finale` | 4 | tagline | the wall of images |
| 7 | `endcard` | rest | close | callback to the hook |

- Cuts · 转场: only where the story turns: into the hero (from mood to product) and into the lineup (the hero moment).
- Breathing room · 留白: the photo beat after the hook is slow and quiet; the feature sits after the reveal so the viewer can read four points calmly.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed warm-acoustic, about 98 BPM (original). It builds into the reveal and lifts at the finale; no track is taken from the web.
- Silence · 静默: a half-beat of silence before the lineup, so the three glazes arrive on an open beat.
- Sound palette · 音效: kept low under the voice. A soft tick on the hero and the lineup only; nothing on the cover or the photo.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实: handmade / thrown on the wheel / glazed by hand / fired twice → README; three glazes, sage, cream, clay → README; 350 ml, double-thick wall, keeps coffee warm longer → README; lead-free food-safe glaze, dishwasher safe → README. Not used: "40 mugs a week" (not needed for this film).
- Legibility & access · 可读与无障碍: captions on in Chinese and English; text sits on scrims with contrast checked; nothing important sits under captions.
- Sign-off · 签字: approved for demo use only. The brand, logo and images are placeholders and the film says so in the report; it is not a real product launch.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 5 | "no two alike" reaches the hook, the hero line and the last line |
| Hook in 3 s · 三秒抓人 | 4 | a glaze texture and a claim that makes the viewer look twice |
| Specific, true copy · 具体真实 | 4 | most spoken lines carry a documented fact (glazes, wall, 350 ml, twice-fired); the ending is a callback |
| Image quality & choice · 画面 | 4 | each beat has its own image, the glaze opens, the mug reveal is staged well; the art is placeholder, so not a 5 |
| Restraint · 克制 | 4 | one hero moment, calm photo and feature beats |
| Rhythm · 节奏 | 4 | slow beats between the reveal and the lineup; the rhythm is even, not inventive |
| Hero moment · 高潮 | 4 | three glazes in a row, placed around two-thirds in |
| Memorable ending · 结尾记忆点 | 4 | the last line calls back to "no two glazes" |
