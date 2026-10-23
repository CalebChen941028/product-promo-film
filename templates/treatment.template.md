# Treatment · 创意方案 — {{PRODUCT}}

> Written by the crew in `references/crew.md`, one section per role, in order. Replace every `write` field.
> `python3 scripts/check_treatment.py treatment.md film.json` must pass before `make_film.py --stage build`.
> 由 `references/crew.md` 中的各角色依次填写；替换所有 `write` 字段，检查通过后再构建。

## 0. Facts · 事实（autofilm 自动填写）
- Product · 产品: {{PRODUCT}}
- Genre · 类型: {{GENRE}}
- Look · 风格: {{STYLE}} · Motion · 动效: {{MOTION}} · Arc · 叙事结构: {{ARC}}
- Music · 音乐: {{MUSIC}}
- Materials · 素材: {{MATERIALS}}
- Target length · 目标时长: {{SECONDS}}
- Tone for this genre · 本类型的语气: {{TONE}}
- Study first · 先读: `{{GOLDEN}}` (a top film in this arc, every scene with a `_why`) and `references/copy-bank.md` — learn the moves, never copy the lines
- Facts to use · 可用事实: {{FACTS}}

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: <write: who watches, on which platform, sound on or off>
- Rights · 授权: <write: music / photos / logos / quotes — who owns them, confirmed with the user?>
- Gaps · 缺口: <write: what material is missing and what we do instead>
- Shot wishlist · 补拍清单: <write: the shots that would lift the film most (see shot_wishlist.md: size, content, light, specs), or "none needed">

## 2. Strategist · 策略
- Audience · 目标受众: <write: who exactly (role, situation), what they use today instead, and the one doubt that stops them>
- Audience truth · 受众真相: <write: one sentence the audience would say about their own life>
- Insight · 洞察: <write: the tension between that truth and what they want>
- Single-minded proposition · 唯一主张: <write: the ONE thing this film says, ≤ 12 words>
- Proof · 证据: <write: 2–3 checkable facts that make the proposition true>
- USP → proof beat · 卖点 → 证明画面: <write: each selling point (≤ 3), what makes it different from the alternative, and the scene + image that proves it>
- AIDA · 说服路径: <write: Attention = the hook (scene 0) · Interest = the problem/reveal (scenes) · Desire = the proof and the hero (scenes) · Action = the call to action>

## 3. Creative director · 创意总监
- Concept A: <write: name — one-line idea — opening image — why it fits>
- Concept B: <write: name — one-line idea — opening image — why it fits>
- Concept C: <write: name — one-line idea — opening image — why it fits>
- Chosen · 选定: <write: A, B or C — and why it is the most surprising AND the most true>
- Hook (0–3 s) · 开场钩子: <write: what we see and hear in the first three seconds>
- Hero moment · 高潮时刻: <write: the one image the audience remembers, and where it lands (≈ 60–70 %)>
- Hook line · 开场句: <write: the spoken line of the cover — the concept as a tension, a question or a physical detail>
- Hero line · 高潮句: <write: the finale line — the proposition in ≤ 6 words, with the name>
- Last line · 收尾句: <write: the end-card line — a callback that echoes a word or image of the hook>
- Title · 片名: <write: working title>

## 4. Copywriter · 文案
- Tagline · 口号: <write: zh ≤ 12 字 / en ≤ 8 words — say both>
- Voice-over · 旁白 (one line per beat, ~2.5 words/s): <write: one bullet per scene in film order, e.g.  - cover → "the hook line" — every proof line carries one fact from the docs; a scene with no voice says (no voice: why)>
- On-screen words · 画面文字: <write: every title/label, ≤ 12 字 / ≤ 42 chars; nothing that the image already says>
- Call to action · 行动号召: <write: one true next step from the docs, zh ≤ 8 字 / en ≤ 4 words ("申请内测 / Join the beta") → brand.cta in film.json; or "none" if the docs give none>
- Banned words checked · 已排除空话: <write: yes — ran lint_copy.py, 0 clichés>

## 5. Art director & colorist · 美术指导与调色
- Palette · 配色（the colour director chose it: keep it, or change film.json "palette" and say why）: {{PALETTE}}
- Look · 视觉（the director chose **{{STYLE}}** from the materials, with these reasons — read them, then confirm or change film.json "style" / "motion"; the look is a decision for THIS product）:
  - {{LOOKS}}
  <write: style id, why it fits THIS product's taste and audience, and why not the alternatives; how the palette serves the feeling>
- Grade · 调色: <write: the grade (LUT) and why its temperature matches the palette — warm products warm, clinical and tech cool; keep real UI and product colours true>
- Each image shows · 每张图的内容 (place and subject, one line per file; the copy over an image must name the same kind of place):
{{IMAGE_LIST}}
- Images · 画面选择: <write: which material carries each beat; best image saved for the hero>
- Composition rules · 构图: <write: margins, where text lives, one focal point per frame>
- We will NOT show · 不出现: <write: clichés to avoid (globes, handshakes, stock smiles, fake UI…)>

## 6. Director & DP, motion designer & editor · 导演与摄影指导、动效与剪辑
- Motion language · 动效语言: <write: id and why it matches the theme>
- Storyboard · 分镜（the director designed it from the materials: frame = layout · camera move · cut into the scene; `why` is its reason. Keep it, or change a scene's `layout` / `camera` / `cut` in film.json on purpose and say why here）:

| # | scene | bars | job of this beat | frame | why |
| --- | --- | --- | --- | --- | --- |
{{BEATS}}

- Shot sizes · 景别: <write: read the size column of the storyboard: the open moves close → wide or wide → close on purpose, a chapter goes wide → medium → close, never three alike in a row>
- Cuts · 转场: <write: every designed cut and effect with what motivates it in THIS product and story (a shared element to zoom through, the product's own gesture, a story turn); the plain cuts that stay plain. Design your own keyframe cuts and moves where the library has nothing that fits (references/director.md §10)>
- Breathing room · 留白: <write: where the film rests for a moment, and why>

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: <write: the user's track, or composed mood + BPM; where it builds, where it drops>
- Silence · 静默: <write: the half-beat before the hero, any other held breath>
- Sound palette · 音效: <write: kept low; which moments get a sound and which deliberately do not>

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实: <write: claim → source>
- Qualifiers · 限定条件: <write: every limit the docs put on a claim (edition/plan, beta, platform, region, planned) → how the film says it in that scene; or 'none in the docs'. A limit that truly does not apply: name it and write 'not affected' with the reason>
- Legibility & access · 可读与无障碍: <write: captions on, contrast OK, nothing important under captions>
- Sign-off · 签字: <write: approved / changes needed>

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
- Deliberate · 刻意: none   (or, per default you break on purpose: "<taste check> — <why, ≥ 6 words>", e.g. "Rhythm — three close-ups in a row: the open is a macro sequence"; separate several with ;)
| Criterion · 标准 | Score | Why |
| --- | --- | --- |
| One idea · 一个核心概念 | <write: 1-5> | <write: why> |
| Hook in 3 s · 三秒抓人 | <write: 1-5> | <write: why> |
| Specific, true copy · 具体真实 | <write: 1-5> | <write: why> |
| Image quality & choice · 画面 | <write: 1-5> | <write: why> |
| Restraint · 克制 | <write: 1-5> | <write: why> |
| Rhythm · 节奏 | <write: 1-5> | <write: why> |
| Hero moment · 高潮 | <write: 1-5> | <write: why> |
| Memorable ending · 结尾记忆点 | <write: 1-5> | <write: why> |
