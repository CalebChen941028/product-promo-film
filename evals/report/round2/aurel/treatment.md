# Treatment · 创意方案 — Aurel Stoneware

> Written by the crew in `references/crew.md`, one section per role, in order.
> `python3 scripts/check_treatment.py treatment.md film.json` must pass before `make_film.py --stage build`.
> 由 `references/crew.md` 中的各角色依次填写；检查通过后再构建。

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: Aurel Stoneware
- Genre · 类型: food-beverage — Food & beverage / 食品 / 饮品 / 餐饮
- Look · 风格: natural-fresh · Motion · 动效: gentle-story · Arc · 叙事结构: sensory
- Music · 音乐: composed: warm-acoustic ~98 BPM (original, royalty-free)
- Materials · 素材: cutout 3, logo 1, photo 3, text 1
- Target length · 目标时长: ~75 s
- Tone for this genre · 本类型的语气: appetite and origin: taste, texture, hands, place
- Study first · 先读: `templates/golden/sensory.json` and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: Handmade stoneware mugs for slow coffee and tea at home. Each mug is thrown on the wheel, glazed by hand and fired twice, so no two glazes are the same. · Three glazes: sage, cream and clay · 350 ml, keeps coffee warm longer with a double-thick wall · Dishwasher safe, lead-free food-safe glaze · Made in a small studio, 40 mugs a week

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Home coffee and tea drinkers who buy handmade ceramics; short social cut with sound on or off. Captions are on for the silent viewer.
- Rights · 授权: Logo and images are drawn placeholders from the product-promo-film demo set (README says so). Music is composed by make_music.py (original, royalty-free). Voice is Kokoro am_michael, already downloaded locally. No quotes are used.
- Gaps · 缺口: No real product photos, no contact details, no price, no testimonials. The film uses only the facts above. Contacts are left empty rather than invented.

## 2. Strategist · 策略
- Audience truth · 受众真相: My morning mug is the one thing I actually pick out myself.
- Insight · 洞察: We want a mug that feels like ours, but mass-made mugs look identical.
- Single-minded proposition · 唯一主张: Every Aurel glaze is hand-applied, so no two are the same.
- Proof · 证据: Thrown on the wheel, glazed by hand, fired twice (README). Three glazes: sage, cream, clay. Double-thick wall keeps coffee warm longer, 350 ml. Made in a small studio, 40 mugs a week.

## 3. Creative director · 创意总监
- Concept A: Glazed by hand — a macro look at the glaze, texture before the whole mug. Opening image: close glaze texture on linen-light. Why it fits: it proves the single claim with the object itself.
- Concept B: Warm for longer — a slow morning, the coffee stays hot. Opening image: steam over a mug. Why it fits: true, but it is a product feature, not a reason to choose this mug.
- Concept C: Forty a week — a studio counts its output. Opening image: a shelf of mugs. Why it fits: honest and human, but it talks about the maker, not the buyer.
- Chosen · 选定: A. It is the most surprising (no two identical) and the most true (the README's own fact), and it gives the buyer a reason to care about the object.
- Hook (0–3 s) · 开场钩子: Soft morning table, then a slow push into the glaze texture. Voice: "Glazed by hand. No two glazes are the same." Caption shows the same line.
- Hero moment · 高潮时刻: The three mugs stand together, lit from the side, in a clean finale. It lands at about 60–70% of the runtime.
- Hook line · 开场句: Glazed by hand. No two glazes are the same.
- Hero line · 高潮句: Aurel. One glaze, one mug.
- Last line · 收尾句: Glazed by hand. Yours alone.
- Title · 片名: Aurel — One Glaze, One Mug

## 4. Copywriter · 文案
- Tagline · 口号: 每一抹釉，都只此一次 / No two glazes are the same.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "Glazed by hand. No two glazes are the same." (hook; the glaze is handmade, which is the claim)
  - detail → (no voice: texture before the whole, the viewer just looks)
  - hero → "Thrown on the wheel. Fired twice." (fact: thrown on the wheel, fired twice)
  - feature → "Double-thick walls keep your coffee warm for longer." (fact: double-thick wall)
  - lineup → (no voice: the three glazes stand together and speak for themselves)
  - finale → "Aurel. One glaze, one mug." (hero line with the name)
  - endcard → "Glazed by hand. Yours alone." (last line, callback to the hook)
- On-screen words · 画面文字: feature title "双层杯壁，温得更久 / Warm for longer"; points "350 ml，双层杯壁 / 350 ml, double-thick wall", "洗碗机可清洗 / Dishwasher safe"; hero title "手作陶杯 / Aurel Stoneware"; lineup "土褐釉 / Clay", "奶油釉 / Cream", "鼠尾草绿釉 / Sage".
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés.

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh. Accent colour is the logo's sage green (#3F7D5A area). Soft neutral backgrounds, warm light, one focal point per frame. Real over decorative: the mug images are the product, not illustration.
- Images · 画面选择: cover uses morning-table (warm, calm, the object in its setting); detail uses glaze-detail (texture before the whole); hero, lineup and finale use the three mug cut-outs; feature uses shelf. The best image, the sage mug in the hero, is saved for the reveal.
- Composition rules · 构图: margins ≥ 96 px; text sits on a soft scrim, never on the busiest part of the image; one focal point per frame.
- We will NOT show · 不出现: hands holding mugs (no hands in the materials), stock smiles, fake dashboards, steam clichés beyond the one provided, globes or handshakes.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story. Slow floating camera, soft focus pull, faint hero flare. It matches a sensory, slow-morning film.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | |
| 2 | `detail` | 3 | texture | |
| 3 | `hero` | 4 | reveal | |
| 4 | `feature` | 4 | craft + warmth | |
| 5 | `lineup` | 3 | range | |
| 6 | `finale` | 4 | hero | |
| 7 | `endcard` | rest | close | |

- Cuts · 转场: camera cuts only at the reveal (hero) and the finale. Everything else uses the style's calm dissolve.
- Breathing room · 留白: the lineup beat is silent, so the three glazes can be seen before the finale.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed warm-acoustic ~98 BPM, original. It builds into the hero and settles on the endcard.
- Silence · 静默: half a beat of silence before the hero line, and the silent lineup beat.
- Sound palette · 音效: kept low. Soft chime on the logo, one impact and riser on the hero moment, no sound on the detail and lineup.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "Glazed by hand. No two glazes are the same." → README: "glazed by hand ... so no two glazes are the same"
  - "Thrown on the wheel. Fired twice." → README
  - "Double-thick walls keep your coffee warm for longer." → README: "keeps coffee warm longer with a double-thick wall"
  - "350 ml", "Dishwasher safe", "lead-free food-safe glaze", "40 mugs a week" → README
  - No claim about price, delivery, or health.
- Legibility & access · 可读与无障碍: captions on for all voice lines; contrast checked against the soft backgrounds; no important text sits under captions.
- Sign-off · 签字: approved for a demo cut, with the note that the images are drawn placeholders and the film must be labelled as a demo if shown publicly.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | One claim (no two glazes are the same) runs through hook, hero and last line. |
| Hook in 3 s · 三秒抓人 | 4 | A close glaze texture and a plain, specific sentence. |
| Specific, true copy · 具体真实 | 4 | Every line carries a fact from the README. |
| Image quality & choice · 画面 | 3 | Images are drawn placeholders, so they are clean but not photographic. Honest score. |
| Restraint · 克制 | 5 | Two silent beats, one hero, one flare. |
| Rhythm · 节奏 | 4 | Calm cover and detail, dense feature, silent lineup, finale. |
| Hero moment · 高潮 | 4 | Three mugs lit together, the sage mug in front. |
| Memorable ending · 结尾记忆点 | 4 | The last line echoes the hook. |
