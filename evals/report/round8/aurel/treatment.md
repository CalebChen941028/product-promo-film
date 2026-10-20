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
- Target length · 目标时长: ~60 s (7 scenes). No padding: no repeats, no long holds
- Tone for this genre · 本类型的语气: appetite and origin: taste, texture, hands, place
- Study first · 先读: `templates/golden/sensory.json` and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: Handmade stoneware mugs for slow coffee and tea at home. Each mug is thrown on the wheel, glazed by hand and fired twice, so no two glazes are the same. · Three glazes: sage, cream and clay · 350 ml, keeps coffee warm longer with a double-thick wall · Dishwasher safe, lead-free food-safe glaze · Made in a small studio, 40 mugs a week

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Home coffee and tea drinkers who want a mug that feels chosen, not catalogue-bought. Online and social; sound may be off, so every spoken line is captioned in Chinese and English.
- Rights · 授权: The imagery is drawn placeholders supplied with the demo (the README says so). No product photos. Music is the original underscore composed by `make_music.py`; voice is Kokoro (am_michael, already installed). No quotes, no third-party assets.
- Gaps · 缺口: No real product photos, no hands on the wheel, no glaze close-ups from the studio, no contact details. The making is told in voice-over and in one texture beat rather than shown in footage. Contacts are left empty for the end card.

## 2. Strategist · 策略
- Audience truth · 受众真相: "Everyone's morning mug looks the same. I want one that is mine."
- Insight · 洞察: Mass-made mugs are identical; people want the small ritual of a cup that is unlike any other.
- Single-minded proposition · 唯一主张: Each Aurel mug is hand-glazed and fired twice, so no two are alike.
- Proof · 证据: (1) glazed by hand and fired twice, so no two glazes are the same; (2) the double-thick wall keeps coffee warm longer; (3) made in a small studio, 40 mugs a week.

## 3. Creative director · 创意总监
- Concept A: Glaze as fingerprint — every mug carries a glaze no other mug shares. Opening image: a macro texture of glaze. Why it fits: it is the true, specific fact of the product (fired twice, glazed by hand).
- Concept B: Warm for longer — the double-thick wall holds the heat of the first cup. Opening image: steam over a mug on a table. Why it fits: a real benefit, but any mug company can say it.
- Concept C: Forty a week — the small studio as the story. Opening image: a shelf of finished mugs. Why it fits: true and quiet, but it sells the maker, not the cup in the hand.
- Chosen · 选定: A. It is the most surprising (a mass-market promise inverted: the sameness is the thing to avoid) and the most true (glazed by hand, fired twice).
- Hook (0–3 s) · 开场钩子: A warm morning table, a mug with steam, the voice says the hook line. The product is in use before its name appears.
- Hero moment · 高潮时刻: The morning table returns at about 70 %, starting tight and dim, then pulling back and lighting up as the name and tagline arrive.
- Hook line · 开场句: "No two glazes are the same." (the concept as a true, checkable fact)
- Hero line · 高潮句: "Aurel. One glaze. One mug."
- Last line · 收尾句: "Your glaze. Nobody else's." (a callback to the hook: the same idea, now addressed to the viewer)
- Title · 片名: One glaze

## 4. Copywriter · 文案
- Tagline · 口号: 一釉一杯，各不相同 / One glaze. One mug.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "No two glazes are the same."
  - detail → "Glazed by hand, then fired twice."
  - hero → "Double-thick walls keep your coffee warm longer."
  - photo → "Forty mugs a week, from one small studio."
  - lineup → (no voice: the three glazes are named on screen; a calm beat after two facts)
  - finale → "Aurel. One glaze. One mug."
  - endcard → "Your glaze. Nobody else's."
- On-screen words · 画面文字: hero title "Aurel Stoneware"; photo title "Three glazes" / 三款釉色; lineup labels Clay / 陶土, Cream / 奶白, Sage / 鼠尾草绿; finale tagline; endcard motto.
- Banned words checked · 已排除空话: yes — `lint_copy.py` reports "copy OK" on film.json.

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh, chosen because the product is handmade and tactile. One accent colour: #3f7d58, the deep sage green from the logo. Everything else is warm neutral.
- Images · 画面选择: morning-table (cover, a mug in use, the hook); glaze-detail (the texture beat, the making); mug-clay (the hero, one mug, clean); shelf (the range, with the studio fact); clay, cream and sage cutouts (the lineup); morning-table returns for the finale, transformed. The best image (morning-table) is saved for the hook and the hero.
- Composition rules · 构图: margins at least 96 px; text in the lower third; one focal point per frame; captions never over the mug.
- We will NOT show · 不出现: globes, handshakes, stock smiles, floating icons, fake UI, a mug on a white void, any product photo that is not in the materials.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story. Slow push-ins and soft crossfades that suit a sensory, handmade product.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | the true fact, product in use |
| 2 | `detail` | 2 | texture | the making, one line of fact, kept short |
| 3 | `hero` | 4 | reveal | the name and the one fact about the mug |
| 4 | `photo` | 4 | mood | the studio, a fact with no adjectives |
| 5 | `lineup` | 3 | range | silent beat after two facts |
| 6 | `finale` | 4 | hero | the morning table returns and lights up |
| 7 | `endcard` | rest | close | the callback to the hook |

- Cuts · 转场: Crossfades only where the story turns: from the table to the texture (human to material) and from the studio to the range. The finale is the only transform (dim and tight to whole and lit).
- Breathing room · 留白: The lineup is silent for three bars after two facts, so the three glazes can be seen before the finale.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: Composed, warm-acoustic, about 98 BPM, original (make_music.py). It stays low under the voice, builds gently through the hero and opens fully at the finale.
- Silence · 静默: A half-beat of silence before the finale name, so the lit frame lands on its own.
- Sound palette · 音效: Kept low. No effects on the glaze close-up or the lineup; the room tone is the only sound there, by design.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "No two glazes are the same" → README: "thrown on the wheel, glazed by hand and fired twice, so no two glazes are the same".
  - "Glazed by hand, then fired twice" → README.
  - "Double-thick walls keep your coffee warm longer" → README: "keeps coffee warm longer with a double-thick wall".
  - "Forty mugs a week, from one small studio" → README: "Made in a small studio, 40 mugs a week".
  - "Three glazes" (sage, cream, clay) → README.
  - Chips "350 ml" and "Dishwasher safe" → README.
- Legibility & access · 可读与无障碍: Captions on in both languages; contrast checked by QA; nothing important sits under the captions.
- Sign-off · 签字: Approved for the demo, with one condition: the imagery is drawn placeholders (the README says so), so this film must not be used as product marketing until real product photos replace them.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | "No two glazes are the same" is the concept, and it reaches the hook, the hero and the last line. |
| Hook in 3 s · 三秒抓人 | 4 | The product is in use on a morning table with a true, checkable claim in the first second. |
| Specific, true copy · 具体真实 | 4 | Each proof line carries one fact from the README, said as what it means to the drinker. |
| Image quality & choice · 画面 | 4 | Placeholder imagery is staged well: one image per beat, the best one saved for the finale. |
| Restraint · 克制 | 4 | One hero moment, one accent colour, a silent lineup beat, no extra effects. |
| Rhythm · 节奏 | 4 | Short texture beat, then reveal, studio fact, silent range, then the finale. No three identical beats in a row. |
| Hero moment · 高潮 | 4 | The morning table returns lit, the hook echoes, the name lands in the frame. |
| Memorable ending · 结尾记忆点 | 4 | The callback "Your glaze. Nobody else's." ends on the viewer, not the logistics. |
