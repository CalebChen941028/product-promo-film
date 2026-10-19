# Quality assurance · 质量检查

English first, 中文在后。

## English

### Automatic (always)
`python3 scripts/make_film.py film.json --stage qa` renders every scene at 40/75/95 % of its length and measures the DOM:

| Code | Meaning | Typical fix in film.json |
| --- | --- | --- |
| `offstage` | text, or > 20 % of a frame, leaves the 1920×1080 stage | shorter text; fewer points/items; another scene type |
| `text-overlap` | two text blocks overlap | shorter labels; fewer stats/rows; more bars |
| `chapter-hit` | the top-left chapter label touches content | remove `chapter` from that scene, or use a scene with smaller media |
| `caption-hit` | the bottom caption covers on-screen text | move the line (`at`) or shorten the scene's text |
| `caption-media` (warn) | caption sits on a screenshot's lower part | usually fine; avoid it when key numbers are at the bottom |
| `small-text` (warn) | text < 14 px | fewer words per label |
| `missing-media` | a file failed to load | fix the path (relative to film.json) |
Rule: **0 errors before rendering.** Warnings are judgement calls.

### Visual (if you can read images)
Open `film_out/qa/sheet*.png` (3×3 frames each). Check: the cover is complete; highlights sit on the right UI region (else fix the `rect`); nothing important under captions; transitions are not black; the end card is centred and correct (names, email, accounts).

### Final file
`ffprobe`/`ffmpeg -i final/*.mp4`: duration = music length, 1920×1080 30 fps, AAC 48 kHz. Pull a frame at each render-worker boundary to check for glitches. SRT lines match the voice-over.

## 中文

### 自动检查（每次必做）
`python3 scripts/make_film.py film.json --stage qa` 会在每个场景 40%、75%、95% 处取帧并测量页面元素：

| 代码 | 含义 | film.json 中常见改法 |
| --- | --- | --- |
| `offstage` | 文字或画框 20% 以上超出 1920×1080 画面 | 缩短文字、减少要点、换场景类型 |
| `text-overlap` | 两个文字块重叠 | 缩短标签、减少数字 / 行数、加小节 |
| `chapter-hit` | 左上章节标签压到内容 | 去掉该场景的 `chapter`，或换素材更小的场景 |
| `caption-hit` | 底部字幕盖住画面文字 | 调整该句的 `at`，或精简场景文字 |
| `caption-media`（警告） | 字幕压在截图下部 | 通常没问题；关键数字在底部时要避开 |
| `small-text`（警告） | 文字小于 14 px | 每个标签少写几个字 |
| `missing-media` | 素材加载失败 | 修正路径（相对 film.json） |
规则：**渲染前必须 0 个错误**，警告视情况处理。

### 目视检查（能看图时）
打开 `film_out/qa/sheet*.png`（每张 3×3 帧），检查：封面完整；高亮框对准正确的界面区域（否则改 `rect`）；字幕下没有重要内容；转场没有黑帧；结尾页居中，姓名、邮箱、账号正确。

### 成片
确认时长等于音乐长度、1920×1080 30fps、AAC 48kHz；在各渲染分段的交界处抽帧检查；SRT 与配音一致。
