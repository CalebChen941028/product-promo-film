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

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: people who make coffee or tea at home and care how a morning feels; Instagram / Xiaohongshu / WeChat Channels, often sound off — captions carry the film
- Rights · 授权: placeholder brand for the skill's demo: drawn placeholder images, music composed by make_music.py, no quotes used
- Gaps · 缺口: no real product photos and no people — the film leans on texture (glaze), light (morning table) and the objects themselves

## 2. Strategist · 策略
- Audience truth · 受众真相: "The first cup of the day is the one quiet moment that is mine."
- Insight · 洞察: mass-made mugs are all identical, but nobody wants their quiet moment to feel mass-made
- Single-minded proposition · 唯一主张: every Aurel mug is one of one, made by hand
- Proof · 证据: thrown on the wheel and glazed by hand; fired twice so glazes vary; a small studio making 40 a week (README)

## 3. Creative director · 创意总监
- Concept A: One of one — every glaze runs its own way, so every mug is unique — opens on morning light on a quiet table — the product truth IS the emotion
- Concept B: The first sip — a morning ritual told in light and steam — opens on an empty table at dawn — warm, but could be any coffee brand
- Concept C: Forty a week — scarcity and craft, the studio counting — opens on the number 40 — honest but reads like a sales pitch
- Chosen · 选定: A — the most surprising (a mug film that lingers on glaze like a painting) and the most true (the uniqueness is real, not claimed)
- Hook (0–3 s) · 开场钩子: a still breakfast table in morning light, the brand appears; the voice: "Some things shouldn't be made the same way twice."
- Hero moment · 高潮时刻: the three mugs lighting up one after another in the reveal, then "One of one" on the finale at about 65 % of the film
- Title · 片名: One of One

## 4. Copywriter · 文案
- Tagline · 口号: 每一只，都只有一只 / One of one
- Voice-over · 旁白 (one line per beat, ~2.5 words/s): cover "Some things shouldn't be made the same way twice." → photo "Like the first cup of the morning." → detail "Each glaze finds its own way through the kiln." → hero "Aurel stoneware. Thrown on the wheel, glazed by hand, fired twice." → feature "Sage, cream and clay. 350 ml, in a double-thick wall that holds the heat." → lineup (no voice: let them look) → finale "Aurel. One of one." → endcard "Made slowly. Best enjoyed the same way."
- On-screen words · 画面文字: 清晨第一杯 / The first cup of the day · 每一只，都只有一只 / ONE OF ONE · 三种釉色 / Three glazes · 鼠尾草绿 奶油白 陶土红; nothing repeats the voice word for word
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh (warm linen, daylight): the product is about mornings and craft; accent = sage green from the logo
- Images · 画面选择: morning-table for the mood, glaze-detail for texture, the three cut-outs for the reveal, shelf for the range; the cut-outs are saved for the hero
- Composition rules · 构图: 96 px margins; text in the left third over a soft scrim on photos; one mug or one texture in focus per frame
- We will NOT show · 不出现: latte-art clichés, stock hands, 'perfect morning' smiles, fake reviews

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story: slow push-ins, soft focus, one line at a time — matches a slow, tactile product
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | |
| 2 | `photo` | 3 | mood | |
| 3 | `detail` | 3 | texture | |
| 4 | `hero` | 4 | reveal | |
| 5 | `feature` | 4 | craft + origin | |
| 6 | `lineup` | 3 | range | |
| 7 | `finale` | 4 | hero | |
| 8 | `endcard` | 5 | close | |

- Cuts · 转场: none — gentle-story keeps the style's dissolves everywhere; the reveal is carried by light, not by a camera move
- Breathing room · 留白: the lineup has no voice: a few seconds just to look at the three glazes

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: composed warm-acoustic ~98 BPM: plucked strums and a shaker; lifts at the reveal, peaks at the finale, rings out on the end card
- Silence · 静默: the half beat before the finale downbeat; the end card rings out on a held chord
- Sound palette · 音效: a soft chime on the logo; a quiet swell on the reveal and the finale; nothing on the photo and detail beats

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实: handmade, wheel-thrown, glazed by hand, fired twice, 350 ml, double-thick wall, 40 a week → materials/README.md (placeholder brand)
- Qualifiers · 限定条件: none in the docs (no edition, platform, region or planned limits on any claim)
- Legibility & access · 可读与无障碍: captions always on; dark-on-linen captions with a band; no text under captions
- Sign-off · 签字: approved for the demo — images are labelled as placeholders in the README

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 5 | one sentence: every mug is one of one |
| Hook in 3 s · 三秒抓人 | 4 | a still, warm frame and a line that makes you wait for the next |
| Specific, true copy · 具体真实 | 4 | every line is a fact from the README, said plainly |
| Image quality & choice · 画面 | 3 | drawn placeholders — real product photography would make this a 5 |
| Restraint · 克制 | 5 | no camera cuts, no flare, one quiet sound per beat |
| Rhythm · 节奏 | 4 | two image beats, a reveal, a rest, then the hero |
| Hero moment · 高潮 | 4 | three mugs lighting up, then the tagline |
| Memorable ending · 结尾记忆点 | 4 | the motto echoes the opening: made slowly, enjoyed slowly |
