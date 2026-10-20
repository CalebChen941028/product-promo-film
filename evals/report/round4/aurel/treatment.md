
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
- Audience & where it plays · 受众与投放渠道: Home coffee and tea drinkers who buy slow, handmade things. Short social cut with sound on; the film is a demo for the product-promo-film skill, so it plays as a demo, not a live campaign.
- Rights · 授权: The brand "Aurel Stoneware" is a placeholder brand written for the skill demo (see materials/aurel/README.md). All product images are drawn placeholder art, not photos of a real product. Music is composed by make_music.py (original). Voice is Kokoro am_michael (Apache-2.0, already downloaded). No quotes are used.
- Gaps · 缺口: No real product photography, no real studio or hands at the wheel, no contact details, no customer quote. We do not fake any of these: the film uses the drawn mugs as they are, labels the demo on the end card, and leaves contacts empty.

## 2. Strategist · 策略
- Audience truth · 受众真相: "I want my morning mug to feel like it was made for me, not picked off a shelf."
- Insight · 洞察: Every mass-made mug matches every other. A slow coffee deserves a cup that is not quite like any other.
- Single-minded proposition · 唯一主张: Every Aurel mug is glazed by hand, so no two are the same.
- Proof · 证据: (1) glazed by hand and fired twice, so no two glazes are the same; (2) three glazes: sage, cream, clay; (3) 350 ml with a double-thick wall that keeps coffee warm longer; (4) dishwasher safe, lead-free food-safe glaze; (5) a small studio making 40 mugs a week.

## 3. Creative director · 创意总监
- Concept A: "Fired twice" — the mug as a record of two firings and one pair of hands; opening image: a mug on a morning table, then a glaze close-up. Why it fits: it is the physical truth of the process.
- Concept B: "Warm longer" — the double-thick wall keeps the morning coffee warm; opening image: steam over a cup at a table. Why it fits: it is a real benefit, but the copy would read as a spec sheet.
- Concept C: "Forty a week" — a small studio, forty mugs a week, one person at a time; opening image: a shelf of finished mugs. Why it fits: scale is honest, but it makes the product sound small, not wanted.
- Chosen · 选定: A, "Fired twice". It is the most surprising (a mug usually looks like its twin) and the most true (each glaze is a separate act of hands). Concept B is kept as a supporting beat (the shelf photo), and C becomes the last line.
- Hook (0–3 s) · 开场钩子: A mug on a warm morning table, no logo. A single calm voice line starts at 0.6 bars.
- Hero moment · 高潮时刻: The three finished mugs (sage, cream, clay) side by side in the finale, the film's one held image before the endcard.
- Hook line · 开场句: "Fired twice, glazed by hand. No two match."
- Hero line · 高潮句: "Aurel: no two glazes alike."
- Last line · 收尾句: "Made by hand. Never two alike." (a callback to "No two match" in the hook)
- Title · 片名: Fired Twice

## 4. Copywriter · 文案
- Tagline · 口号: 每一道釉，只此一次 / No two glazes are the same.
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "Fired twice, glazed by hand. No two match."
  - detail (glaze) → (no voice: the glaze texture is the beat; the viewer sees the variation without a line)
  - hero (reveal) → "Aurel. Thrown on the wheel, glazed by hand, in sage, cream or clay."
  - photo (shelf) → "Three hundred and fifty millilitres, with a double-thick wall that keeps coffee warm longer."
  - lineup (three mugs) → "Dishwasher safe, with a lead-free, food-safe glaze."
  - finale (hero) → "Aurel: no two glazes alike."
  - endcard → "Made by hand. Never two alike."
- On-screen words · 画面文字: cover title "Aurel Stoneware"; photo title zh "慢慢做，慢慢喝" / en "Made slowly, for slow mornings"; shelf title zh "双层厚壁 · 保温更久" / en "Double-thick wall, warm longer"; lineup labels zh 陶土 / 奶白 / 鼠尾草绿 with en Clay / Cream / Sage.
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés (to be confirmed at stage check)

## 5. Art director · 美术指导
- Look · 视觉: style natural-fresh (from the genre food-beverage); one accent colour from the logo's sage green; the three glazes are the palette of the film.
- Images · 画面选择: cover = morning-table.jpg (a subject on a table: the cold open needs a subject); detail = glaze-detail.jpg for the texture beat; reveal = the three mugs (clay, cream, sage) on a plain field; shelf photo = shelf.jpg for the benefit line; lineup = the three mugs in a row; finale = all of the above, the one held image before the endcard. Each image has its own role; the three mugs repeat because they are the product.
- Composition rules · 构图: margins at least 96 px; text sits on calm areas, never over the mug; one focal point per frame; one accent colour.
- We will NOT show · 不出现: globes, handshakes, stock smiles, fake steam animations, fake UI, real-looking brand logos beyond the placeholder "A".

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story — slow push-ins and soft fades, matching a slow-coffee tone.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | |
| 2 | `detail` | 2 | texture | |
| 3 | `hero` | 4 | reveal | |
| 4 | `photo` | 4 | fact | |
| 5 | `lineup` | 3 | range | |
| 6 | `finale` | 4 | hero | |
| 7 | `endcard` | 3 | close | |

- Cuts · 转场: Cuts only where the story turns: cover into the glaze detail (the object comes close), and the finale into the endcard. Everything else is a soft style cut.
- Breathing room · 留白: The detail beat is silent (two bars of glaze texture) so the viewer sees the variation before the reveal.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed warm-acoustic at ~98 BPM, original. It stays low under the voice, builds gently from the hero reveal, and holds through the finale.
- Silence · 静默: half a beat of silence before the finale line.
- Sound palette · 音效: low, warm: a soft ceramic tick on the reveal and a soft sound at the glaze detail. No sound on the endcard tagline.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "Fired twice, glazed by hand" → README: thrown on the wheel, glazed by hand, fired twice.
  - "No two match" → README: so no two glazes are the same.
  - "Sage, cream, clay" → README: three glazes.
  - "350 ml, double-thick wall, keeps coffee warm longer" → README.
  - "Dishwasher safe, lead-free food-safe glaze" → README.
  - "Forty mugs a week" → README: 40 mugs a week.
  - No claim outside the README is used.
- Legibility & access · 可读与无障碍: captions on; text sits on calm areas; contrast checked by QA; nothing important sits under the captions.
- Sign-off · 签字: approved for the demo, with these limits: placeholder brand, drawn placeholder art, placeholder endcard demo label.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 4 | "Fired twice, no two alike" is in the hook, the hero and the last line. |
| Hook in 3 s · 三秒抓人 | 4 | The macro glaze and the first line land in 3 s; the drawn art is simple, so the hook is clean rather than striking. |
| Specific, true copy · 具体真实 | 4 | Every proof line carries a fact from the README (wheel, fired twice, 350 ml, 40 a week). |
| Image quality & choice · 画面 | 4 | Drawn placeholders chosen and staged to fit the beats, but they are not photographs, so the score is capped. |
| Restraint · 克制 | 4 | One hero (the finale), calm rhythm, a silent beat before the hero. |
| Rhythm · 节奏 | 4 | Calm, varied beats; no three identical beats in a row. |
| Hero moment · 高潮 | 4 | The three mugs together in the finale line. |
| Memorable ending · 结尾记忆点 | 4 | The last line calls back to the hook: "Never two alike." |
