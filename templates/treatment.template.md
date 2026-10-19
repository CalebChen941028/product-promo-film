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
- Target length · 目标时长: ~{{SECONDS}} s
- Tone for this genre · 本类型的语气: {{TONE}}

## 1. Producer · 制片
- Audience & where it plays · 受众与投放渠道: <write: who watches, on which platform, sound on or off>
- Rights · 授权: <write: music / photos / logos / quotes — who owns them, confirmed with the user?>
- Gaps · 缺口: <write: what material is missing and what we do instead>

## 2. Strategist · 策略
- Audience truth · 受众真相: <write: one sentence the audience would say about their own life>
- Insight · 洞察: <write: the tension between that truth and what they want>
- Single-minded proposition · 唯一主张: <write: the ONE thing this film says, ≤ 12 words>
- Proof · 证据: <write: 2–3 checkable facts that make the proposition true>

## 3. Creative director · 创意总监
- Concept A: <write: name — one-line idea — opening image — why it fits>
- Concept B: <write: name — one-line idea — opening image — why it fits>
- Concept C: <write: name — one-line idea — opening image — why it fits>
- Chosen · 选定: <write: A, B or C — and why it is the most surprising AND the most true>
- Hook (0–3 s) · 开场钩子: <write: what we see and hear in the first three seconds>
- Hero moment · 高潮时刻: <write: the one image the audience remembers, and where it lands (≈ 60–70 %)>
- Title · 片名: <write: working title>

## 4. Copywriter · 文案
- Tagline · 口号: <write: zh ≤ 12 字 / en ≤ 8 words — say both>
- Voice-over · 旁白 (one line per beat, ~2.5 words/s): <write: beat → line, in film order>
- On-screen words · 画面文字: <write: every title/label, ≤ 12 字 / ≤ 42 chars; nothing that the image already says>
- Banned words checked · 已排除空话: <write: yes — ran lint_copy.py, 0 clichés>

## 5. Art director · 美术指导
- Look · 视觉: <write: style id and why; the one accent colour (from the logo)>
- Images · 画面选择: <write: which material carries each beat; best image saved for the hero>
- Composition rules · 构图: <write: margins, where text lives, one focal point per frame>
- We will NOT show · 不出现: <write: clichés to avoid (globes, handshakes, stock smiles, fake UI…)>

## 6. Motion designer & editor · 动效与剪辑
- Motion language · 动效语言: <write: id and why it matches the theme>
- Rhythm map · 节奏表:

| # | scene | bars | job of this beat | note |
| --- | --- | --- | --- | --- |
{{BEATS}}

- Cuts · 转场: <write: where the camera cuts are (only where the story turns)>
- Breathing room · 留白: <write: where the film rests for a moment, and why>

## 7. Composer & sound designer · 作曲与声音
- Music · 音乐: <write: the user's track, or composed mood + BPM; where it builds, where it drops>
- Silence · 静默: <write: the half-beat before the hero, any other held breath>
- Sound palette · 音效: <write: kept low; which moments get a sound and which deliberately do not>

## 8. Brand guardian · 品牌把关
- Every claim checked · 每条说法已核实: <write: claim → source>
- Legibility & access · 可读与无障碍: <write: captions on, contrast OK, nothing important under captions>
- Sign-off · 签字: <write: approved / changes needed>

## 9. Taste review · 品味评审 (1–5; average ≥ 4, none below 3)
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
