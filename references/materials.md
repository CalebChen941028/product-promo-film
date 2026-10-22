# Materials & brief · 素材与需求

English first, 中文在后。One folder in, a drafted film out: `python3 scripts/autofilm.py <folder> --out <project>`.

## English

### What to put in the folder (any product)
| Material | Software / apps | Physical products | Services / brands / places |
| --- | --- | --- | --- |
| **Hero visuals** | 6–20 real screenshots, ideally 2× (3840×2160); phone captures | product cut-outs (transparent PNG, one per colour/model/angle) | photographs of the place, the people (with consent), the work |
| **Texture / detail** | crops come from screenshots | macro photos (material, finish, stitching, glaze…) | close-ups of hands, tools, ingredients |
| **Context** | screen recordings (any format → WebM) | lifestyle photos (in use, in a room, on a table); **real footage** (the product working, being used, poured, worn), any format | wide establishing shots; footage of the place and the work |
| **Logo** | transparent PNG ≥ 512 px (name it `logo.png`) | same | same |
| **Music** (optional) | the user's licensed track | same | same; without one an original underscore is composed |
| **Voice** (optional) | `vo_*.wav` recordings, or Kokoro TTS | same | same |
| **Words** | README, brief.json, feature list, specs, real testimonials | same | same |

What `intake.py` (run by autofilm) recognises:
- **desktop** / **phone**: screens, from flat pixel areas and sharp text edges.
- **photo**: natural images (JPEG photos are always photos, even drawn ones).
- **packshot**: a product on a bright, flat background. autofilm keeps it for the hero, framed; it is not masked automatically, so ask for a transparent PNG if a cut-out or lineup is wanted.
- **cutout**: an object on transparency.
- **figure**: charts and plots.
- **footage** vs **screen** recordings: one frame from the middle of each clip decides. Footage can open the film, stand in for a photo beat, or get its own beat; it plays from its best moment (`scripts/footage.py`: sharp, exposed, moving but not shaking). Screen recordings go to `clip` scenes. Name a clip `*screen*` / `*record*` to force a screen, `*footage*` / `*shot*` for footage.
- **logo**, music, voice and docs.

File names help: `*detail*`, `*texture*` and `*macro*` go to detail beats, `*lifestyle*` and `*scene*` to photo beats, and `*screen*` or `*ui*` mark screens. The folder's name counts as a hint for the genre (a folder called `humidifier` reads as home living). Role guesses are heuristics, so check the summary it prints.

### Images only, no words
The film can still be made, but it may claim only what the images visibly show: the crew writes one line per image in treatment §5 (place and subject), and that is the source for concrete copy. Every number and spec term (battery, ml, dB, coverage, waterproof, certified…) needs text the user supplied in the folder; with none, `check_treatment` blocks it. Indoor words over an outdoor image (and the reverse) are blocked too. The report lists what the user must still supply: name, logo, a README or spec sheet, contacts. AI-generated renders and clips with garbled UI are flagged, not presented as real.

### The brief (optional, makes everything better)
`templates/brief.example.json` → `brief.json` in the folder. The fields autofilm uses:
- `product.name`, `nameAccent`, `positioning{zh,en}`, `tagline{zh,en}`, `platforms`, `status`;
- `insight{zh,en}`: the human truth (opens sensory and human-story films);
- `pain{zh,en}`;
- `features[{zh,en,materials:[globs]}]`, where `materials` decides which image proves each feature;
- `numbers[{value,suffix,zh,en}]`;
- `differentiators`;
- `testimonials[{zh,en,who,role}]`: real and approved only;
- `motto{zh:[line1,line2],en}`;
- `contacts`;
- `genre` (to override the classifier).

### Good material
- **Screens:** the same window size throughout; real effects on demo data; no personal data; one state per shot.
- **Products:** cut-outs at ≥ 1500 px with clean edges. Shoot the same angle for each colour (a lineup). One hero angle gets its own file.
- **Photos:** ≥ 1920 px wide, natural light, one subject, room for text on one side. No stock clichés.
- **Rights:** only material the user owns or may use. People in photos must have consented.

## 中文

### 文件夹里放什么（任何产品）
| 素材 | 软件 / App | 实物产品 | 服务 / 品牌 / 空间 |
| --- | --- | --- | --- |
| **主视觉** | 6–20 张真实截图，最好 2 倍分辨率；手机截图 | 透明底产品图（每个颜色 / 型号 / 角度一张） | 场所、人物（需同意）、工作过程的照片 |
| **质感 / 细节** | 从截图中裁取 | 微距照片（材质、工艺、缝线、釉面……） | 手、工具、原料的特写 |
| **情境** | 录屏（任意格式，自动转 WebM） | 使用场景照片（在用、在房间、在桌上）；**实拍视频**（产品运转、被使用、倒入、穿戴），任意格式 | 全景照片；场所与工作过程的实拍视频 |
| **Logo** | 透明 PNG，≥ 512 px（命名为 `logo.png`） | 同左 | 同左 |
| **音乐**（可选） | 用户授权的曲子 | 同左 | 同左；没有时自动原创配乐 |
| **配音**（可选） | `vo_*.wav` 录音，或 Kokoro 合成 | 同左 | 同左 |
| **文字** | README、brief.json、功能列表、规格、真实评价 | 同左 | 同左 |

`intake.py`（autofilm 会调用）能识别：
- **desktop** / **phone**：界面截图，依据平坦像素区域和清晰的文字边缘判断。
- **photo**：自然照片（JPEG 一律按照片处理，手绘的也一样）。
- **packshot**：浅色纯背景上的产品图。autofilm 把它留给高潮，带框使用；不会自动抠图，需要透明底或阵列展示时请向用户要透明 PNG。
- **cutout**：透明底物体。
- **figure**：图表。
- **实拍视频**与**录屏**：取每段视频中间的一帧来判断。实拍视频可以做开场、替代照片拍点，或单独成为一拍，并从最好的片段开始播放（`scripts/footage.py`：清晰、曝光正常、有动作但不抖）。录屏用于 `clip` 场景。文件名含 `screen` / `record` 强制当录屏，含 `footage` / `shot` 当实拍。
- **logo**，以及音乐、配音、文档。

文件名也有帮助：`*detail*`、`*texture*`、`*macro*` 会进入细节拍点，`*lifestyle*`、`*scene*` 进入照片拍点，`*screen*`、`*ui*` 标记为界面。文件夹名也是类型的线索（叫 `humidifier` 的文件夹会被判为家居生活类）。分类是启发式的，请核对打印出的汇总。

### 只有图片、没有文字
照样可以做，但只能说图片里看得见的东西：团队在方案第 5 节为每张图写一行（地点与主体），这就是具体文案的依据。任何数字和规格词（续航、毫升、分贝、覆盖面积、防水、认证……）都需要用户放进文件夹的文字作来源，没有就会被 `check_treatment` 拦下；室内用词配户外画面（或反之）也会被拦下。报告会列出用户还需提供的东西：名称、Logo、README 或规格表、联系方式。AI 生成的渲染图、带乱码界面的视频会被标明，不当作真实素材呈现。

### Brief（可选，但会让一切更好）
把 `templates/brief.example.json` 复制为素材文件夹里的 `brief.json`。autofilm 会用到：
- 名称、定位、口号、平台、状态；
- `insight`：受众真相，用于情感类开场；
- `pain`；
- `features`：其中 `materials` 决定每个卖点用哪张图证明；
- `numbers`、`differentiators`；
- `testimonials`：仅限真实且经授权的评价；
- `motto`、`contacts`；
- `genre`：用来覆盖自动分类。

### 好素材的标准
- **界面**：全部同一窗口尺寸；演示数据但效果真实；不含个人信息；一张图一个状态。
- **产品**：透明底图 ≥ 1500 px，边缘干净；每个颜色用同一角度拍（用于阵列展示），主角度单独一张。
- **照片**：宽 ≥ 1920 px，自然光，单一主体，一侧留出放文字的空间；不用图库俗套画面。
- **授权**：只用用户拥有或有权使用的素材；照片中的人物须本人同意。
