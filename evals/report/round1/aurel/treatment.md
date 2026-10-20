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
- Target length · 目标时长: ~70 s
- Tone for this genre · 本类型的语气: appetite and origin: taste, texture, hands, place

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: People who make slow coffee and tea at home, first seen on a phone with sound off, so captions carry the film. Sound-on version for the same audience.
- Rights · 授权: All imagery is drawn placeholder art supplied with the demo (the materials README says so). The logo is a placeholder mark. Music is an original composition from `make_music.py`. No quotes. The film is therefore a labelled demo, not a publishable ad.
- Gaps · 缺口: No real product photography and no contact details. We do not fake either. The film is labelled "Demo · placeholder imagery" on the cover and endcard. End card has no contact line until the user supplies one.

## 2. Strategist · 策略
- Audience truth · 受众真相: "My morning coffee should taste like it was made for me, not poured from a row of identical cups."
- Insight · 洞察: Mass-made mugs are all the same, but the one we use every day should feel like ours.
- Single-minded proposition · 唯一主张: Handmade stoneware, and no two glazes are the same.
- Proof · 证据: (1) Thrown on the wheel, glazed by hand, fired twice. (2) Three glazes: sage, cream and clay. (3) 350 ml with a double-thick wall that keeps coffee warm longer. (4) Dishwasher safe, lead-free food-safe glaze. (5) Made in a small studio, 40 mugs a week.

## 3. Creative director · 创意总监
- Concept A: "Warm wall" — the double-thick wall holds heat; open on steam rising from a mug in morning light. Fits the warmth proof, but it is a product-benefit story that any mug brand could tell.
- Concept B: "Second fire" — follow the clay through two firings; open on the kiln door. Fits the craft proof, but the kiln is not in our material and the story is about process, not the person drinking.
- Concept C: "No two alike" — three real glazes, each one unrepeatable; open on a close glaze texture. Fits the single-minded proposition directly and no other brand can claim it.
- Chosen · 选定: C. It is the most surprising (the variation is the product, not a flaw) and the most true (the README says no two glazes are the same). Concept A is kept only as the warmth line inside the hero scene.
- Hook (0–3 s) · 开场钩子: The cover opens on the morning table, blurred behind the logo. Steam is visible, and the first line is spoken at 0.6 bars: "Thrown on the wheel. Glazed by hand."
- Hero moment · 高潮时刻: The finale: six real images tilt into a wall and the tagline lands: "No two glazes are the same." Placed at about 63 % of the runtime (bar 17 of 27), after one half-beat of silence.
- Title · 片名: No Two Alike · 各不相同

## 4. Copywriter · 文案
- Tagline · 口号: 没有两只一样的杯子 / No two glazes are the same
- Voice-over · 旁白 (one line per beat, ~2.5 words/s):
  - cover → "Thrown on the wheel. Glazed by hand." / 在拉坯机上拉出，手工上釉。
  - detail → "Look closer. Each glaze runs differently." / 仔细看，每层釉都有自己的走向。
  - hero → "Three hundred fifty milliliters. A double-thick wall keeps coffee warm longer." / 350 毫升，双层厚壁，咖啡保温更久。
  - feature → "Forty mugs a week, from one small studio." / 一间小工作室，每周做出四十只杯子。
  - finale → "No two glazes are the same." (caption hidden: the text is on screen) / 没有两只一样的杯子。
  - endcard → "Aurel stoneware. Made by hand, one mug at a time." / 手作而成，一只一只。
- On-screen words · 画面文字:
  - cover: logo, "Aurel Stoneware", positioning (zh/en), chips "Demo · placeholder imagery".
  - detail: no title.
  - hero: "为慢慢喝而做 / Made for slow coffee".
  - feature: "手拉、手上釉、两次烧成 / Thrown, glazed, fired twice"; points "手工拉坯与上釉 / Thrown on the wheel, glazed by hand", "两次烧制 / Fired twice", "无铅食品级釉，可洗碗机 / Lead-free, food-safe, dishwasher safe".
  - lineup: "三种釉色 / Three glazes"; labels 陶土 Clay, 奶白 Cream, 鼠尾草绿 Sage.
  - finale: the tagline (shown on screen).
  - endcard: motto 为慢咖啡与慢茶而做 / 一只一只，手作而成 / Made by hand, one mug at a time.
- Banned words checked · 已排除空话: yes, lint_copy.py run in the check stage; no superlatives, no exclamation marks.

## 5. Art director · 美术指导
- Look · 视觉: natural-fresh. Warm neutral ground with one accent: the sage green of the logo disc (about #3E7D58). Two typefaces at most, set by the style.
- Images · 画面选择: cover uses the morning table as a blurred background (steam and warm light, no product). Detail uses the glaze close-up (texture before the whole). Hero uses the sage mug on the stage (the accent matches the logo). Feature uses the shelf photo with the three mugs. Lineup uses the three mug cutouts side by side. Finale uses all six images as the wall. Endcard is type over the logo. The morning photo appears only as the cover background and inside the finale wall.
- Composition rules · 构图: one focal point per frame; margins ≥ 96 px; text never touches an image edge; captions sit clear of the product.
- We will NOT show · 不出现: stock smiles, hands that are not ours, globes, handshakes, light bulbs, fake testimonials, fake studio or fake kiln footage, fake UI.

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: gentle-story. Slow floating camera, soft focus pull, faint light on the hero. Matches a calm product for slow mornings.
- Rhythm map · 节奏表 (matches film.json):

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
| 1 | `cover` | 3 | hook | steam and first line |
| 2 | `detail` | 3 | texture | the glaze before the whole |
| 3 | `hero` | 4 | reveal | the sage mug; the warmth proof |
| 4 | `feature` | 4 | craft + origin | three checkable points |
| 5 | `lineup` | 3 | range | three glazes, breathing |
| 6 | `finale` | 4 | hero | the wall and the tagline |
| 7 | `endcard` | 5 | close | motto and name |

- Cuts · 转场: calm style dissolves throughout. No camera cuts in this gentle-story film; the hero is carried by the light and the tagline.
- Breathing room · 留白: the lineup beat after the dense feature beat, and the half-beat before the finale.

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: original, composed warm-acoustic, ~98 BPM. Builds gently through the feature beat and lifts into the finale.
- Silence · 静默: a half-beat of silence before the finale's tagline.
- Sound palette · 音效: airy swell and soft chimes, with two soft hits on scene starts. No impacts. Kept low: felt, not heard.

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实:
  - "Thrown on the wheel, glazed by hand, fired twice" → materials README (first paragraph).
  - "Three glazes: sage, cream and clay" → materials README.
  - "350 ml, double-thick wall, keeps coffee warm longer" → materials README.
  - "Dishwasher safe, lead-free food-safe glaze" → materials README.
  - "Forty mugs a week, from one small studio" → materials README ("40 mugs a week").
  - "No two glazes are the same" → materials README.
  - "For slow coffee and tea at home" → materials README.
- Legibility & access · 可读与无障碍: captions on; contrast checked by QA; nothing important sits under captions.
- Sign-off · 签字: approved as a labelled demo (placeholder imagery and logo). Not approved for public release until real product photography, a real logo and a contact line are supplied.

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | 5 | "No two glazes are the same" is one sentence, and the whole film points at it. |
| Hook in 3 s · 三秒抓人 | 3 | Steam and a clear first line, but the opening frame is a blurred placeholder photo, so it is not yet striking. |
| Specific, true copy · 具体真实 | 5 | Every line traces to the README; the tagline is a line people would quote. |
| Image quality & choice · 画面 | 3 | Drawn placeholder art, not product photography. Choice is right for the beats; quality is capped by the materials. Scored honestly, not raised. |
| Restraint · 克制 | 4 | Few effects; one camera cut; sound kept low. |
| Rhythm · 节奏 | 4 | The lineup breathes after the feature; the finale comes after a half-beat of silence. |
| Hero moment · 高潮 | 4 | The wall and the tagline at about 63 %. |
| Memorable ending · 结尾记忆点 | 4 | The motto and the tagline stay together; the end card has no contact line yet. |

Average 4.0; no score below 3. Passes the gate, with the image score (3) as the known limit: the film needs real product photography before any public use.
