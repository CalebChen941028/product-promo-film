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
- Target length · 目标时长: ~74 s — 6 images/clips carry about 74 s; the sensory arc would run 75 s with more material. Do not pad: no repeats, no long holds
- Tone for this genre · 本类型的语气: appetite and origin: taste, texture, hands, place
- Study first · 先读: `templates/golden/sensory.json` (a top film in this arc, every scene with a `_why`) and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: Handmade stoneware mugs for slow coffee and tea at home. Each mug is thrown on the wheel, glazed by hand and fired twice, so no two glazes are the same. · Three glazes: sage, cream and clay · 350 ml, keeps coffee warm longer with a double-thick wall · Dishwasher safe, lead-free food-safe glaze · Made in a small studio, 40 mugs a week

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: Home coffee and tea drinkers who buy handmade ceramics. Online, landscape 1080p, often watched with sound off, so captions carry every line.
- Rights · 授权: All images are drawn placeholders from the demo folder (its README says so), and the logo is a demo placeholder. Aurel is a placeholder brand, not a real product. Music is original, composed by `make_music.py`. No quotes, no testimonials.
- Gaps · 缺口: No real product photos, so the mugs are drawn; the film is labelled a demo and must be re-cut with studio photography before any real use. Only three photos and three cut-outs exist, so every beat uses a different image (morning-table returns only as the deliberate bookend). No contact details and no URL were supplied, so the end card carries the last line alone.

## 2. Strategist · 策略
- Audience truth · 受众真相: "I want my morning cup to feel like it is mine, not from a shelf of identical ones."
- Insight · 洞察: Most mugs are identical because they are made to be identical. The people who care about their cup want the opposite, and a handmade object is the only way to get it.
- Single-minded proposition · 唯一主张: Every Aurel mug is glazed by hand, so no two are alike.
- Proof · 证据:
  1. Each mug is thrown on the wheel, glazed by hand and fired twice, so no two glazes are the same (README).
  2. 350 ml, with a double-thick wall that keeps coffee warm longer (README).
  3. Three glazes: sage, cream and clay (README).

## 3. Creative director · 创意总监
- Concept A: **Fired twice** — the making: the film walks through throwing, glazing and the two firings. Opening image: a wheel-thrown mug on a table. Why it fits: honest, but it is a process list and any studio could say it.
- Concept B: **No two alike** — the glaze is a fingerprint: every cup is a different surface. Opening image: the morning table with one mug and its steam, then the glaze texture. Why it fits: the fact is physical, true for every mug, and the reverse of what a shelf of identical mugs promises.
- Concept C: **Slow coffee** — warmth and time, the double-thick wall. Opening image: steam over the morning table. Why it fits: pleasant, but any mug brand could say it.
- Chosen · 选定: B. It is the most surprising (a promise of difference, from a product that is usually sold as the same) and the most true (each glaze is brushed on by hand and fired twice, so no two come out identical).
- Hook (0–3 s) · 开场钩子: The mug on the morning table, steam rising, in warm light. The voice says the tension in one line: the cup is made by hand, and no two are ever the same.
- Hero moment · 高潮时刻: The finale: the morning table returns full-frame as a bookend and the name lands with the promise, "No two glazes alike." It lands at about 67 % of the film, after the three-glaze lineup.
- Hook line · 开场句: "Made by hand. No two are ever the same."
- Hero line · 高潮句: "Aurel. No two glazes alike."
- Last line · 收尾句: "Same coffee. A cup no one else has." (It echoes the hook's "no two are ever the same" with the cup the viewer holds.)
- Title · 片名: No Two Alike

## 4. Copywriter · 文案
- Tagline · 口号: 没有两只一样 / No two glazes alike
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "Made by hand. No two are ever the same." (纯手工制作，没有两只一样。) — the hook, a tension
  - detail → "Glazed by hand, then fired twice." (手工上釉，然后烧制两次。) — the texture named, with a fact
  - hero → "Thrown on the wheel. Made for slow coffee and tea." (拉坯成形，为慢慢品的咖啡与茶而做。) — the reveal, with a fact
  - photo → "350 ml, with a double-thick wall that keeps coffee warm longer." (350 毫升，双倍厚度的杯壁，咖啡更久保温。) — proof, said as what it means
  - lineup → (no voice: the three glazes speak through their labels, a calm beat before the hero)
  - finale → "Aurel. No two glazes alike." (Aurel：没有两只一样。) — the hero line
  - endcard → "Same coffee. A cup no one else has." (同样的咖啡，一只别人没有的杯子。) — the last line, a callback
- On-screen words · 画面文字:
  - hero title: "Aurel Stoneware" / "Aurel 陶器"
  - photo title: "Three glazes" / "三款釉色"
  - lineup labels: "Sage 鼠尾草绿", "Cream 奶油白", "Clay 陶土棕"
- Banned words checked · 已排除空话: yes — ran lint_copy.py, 0 clichés

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh. Warm neutrals with the sage green of the mug as the one accent colour. Two typefaces at most, as the style sets them.
- Images · 画面选择:
  - cover: morning-table (the mug on the table, steam: a place and a subject for the cold open)
  - detail: glaze-detail (texture before the whole; the glaze is what the hook promised)
  - hero: the three cut-outs, sage leading (the product lights up)
  - photo: shelf (three glazes side by side in one real setting)
  - lineup: the three cut-outs in sage, cream, clay order (the range)
  - finale: morning-table returns full-frame (the bookend, the best image saved for the hero)
- Composition rules · 构图: margins ≥ 96 px; text sits in the lower third over a soft scrim; one focal point per frame, the mug; the sage accent is the only saturated colour.
- We will NOT show · 不出现: globes, handshakes, stock smiles, hands doing a pose, floating icons, a fake kiln or fake studio, any invented number.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story. Slow push-ins and soft fades, because the film is about a calm morning and a handmade object, not speed.
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | the tension line over the morning table |
| 2 | `detail` | 2 | texture | the glaze, with one fact; a short beat |
| 3 | `hero` | 4 | reveal | the three mugs light up, the name lands |
| 4 | `photo` | 4 | mood | three glazes on a shelf, with the wall fact |
| 5 | `lineup` | 3 | range | silent calm, the labels do the talking |
| 6 | `finale` | 4 | hero | the bookend and the promise |
| 7 | `endcard` | rest | close | the callback to the hook |

- Cuts · 转场: Camera cuts only where the story turns: the cover into the glaze (texture before the whole), and the lineup into the finale (the bookend). Everything else uses the style's calm transition.
- Breathing room · 留白: The lineup is the calm beat before the finale, with no voice, so the hero has room. The detail beat is short so it does not sit as dead air.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: original composed warm-acoustic, ~98 BPM (`make_music.py`), starts soft under the cover, builds through the hero and photo, drops to a quiet bed for the lineup and rises again for the finale.
- Silence · 静默: half a beat of silence before the finale, after the lineup.
- Sound palette · 音效: kept very low. A soft ceramic tap on the hero reveal and a gentle hit on the finale only. No sound on the detail or the lineup, so the glaze reads as quiet and real.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "Made by hand" and "no two are ever the same" → README: thrown on the wheel, glazed by hand, fired twice, so no two glazes are the same.
  - "Glazed by hand, then fired twice" → README.
  - "Thrown on the wheel. Made for slow coffee and tea." → README: handmade for slow coffee and tea at home; thrown on the wheel.
  - "350 ml, with a double-thick wall that keeps coffee warm longer." → README.
  - "Three glazes" and the names sage, cream, clay → README.
  - "Same coffee. A cup no one else has." → a metaphor for "no two glazes are the same"; it is not a serial-number claim. Flagged for the real brand to confirm.
- Legibility & access · 可读与无障碍: Captions on for every line. The sage accent on cream reaches the contrast needed for captions. Nothing important sits under a caption.
- Sign-off · 签字: approved for the demo, with changes needed before any real use: real photography to replace the drawn mugs, and the brand to confirm the last line.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 5 | "No two alike" reaches the hook, the hero line and the last line |
| Hook in 3 s · 三秒抓人 | 4 | A mug and steam on a table, plus a tension line you can quote |
| Specific, true copy · 具体真实 | 4 | Every proof line carries a README fact: wheel, hand glaze, two firings, 350 ml, double-thick wall |
| Image quality & choice · 画面 | 4 | Each beat has its own image, the glaze texture is the detail, and the bookend is saved for the finale; the drawn art is a placeholder, which is stated in the gaps |
| Restraint · 克制 | 5 | Calm transitions, one hero, sound kept low, nothing extra |
| Rhythm · 节奏 | 4 | Quiet lineup before the finale, no three identical beats in a row |
| Hero moment · 高潮 | 3 | The bookend and the promise are clear, but the drawn mugs make the hero a quiet one, not a big moment |
| Memorable ending · 结尾记忆点 | 4 | The last line calls back to the hook |

Average 4.1: passes. The hero score is held at 3 because the drawn placeholders limit the moment; real photography would be the fix.
