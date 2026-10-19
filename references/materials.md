# Materials & brief · 素材与需求

English first, 中文在后。One folder in, a drafted film out: `python3 scripts/autofilm.py <folder> --out <project>`.

## English

### What to put in the folder (any product)
| Material | Software / apps | Physical products | Services / brands / places |
| --- | --- | --- | --- |
| **Hero visuals** | 6–20 real screenshots, ideally 2× (3840×2160); phone captures | product cut-outs (transparent PNG, one per colour/model/angle) | photographs of the place, the people (with consent), the work |
| **Texture / detail** | crops come from screenshots | macro photos (material, finish, stitching, glaze…) | close-ups of hands, tools, ingredients |
| **Context** | screen recordings (any format → WebM) | lifestyle photos (in use, in a room, on a table) | wide establishing shots |
| **Logo** | transparent PNG ≥ 512 px (name it `logo.png`) | same | same |
| **Music** (optional) | the user's licensed track | same | same; without one an original underscore is composed |
| **Voice** (optional) | `vo_*.wav` recordings, or Kokoro TTS | same | same |
| **Words** | README, brief.json, feature list, specs, real testimonials | same | same |

What `intake.py` (run by autofilm) recognises:
- **desktop** / **phone**: screens, from flat pixel areas and sharp text edges.
- **photo**: natural images.
- **cutout**: an object on transparency.
- **figure**: charts and plots.
- **logo**, clips, music, voice and docs.

File names help: `*detail*`, `*texture*` and `*macro*` go to detail beats, `*lifestyle*` and `*scene*` to photo beats, and `*screen*` or `*ui*` mark screens. Role guesses are heuristics, so check the summary it prints.

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
| **情境** | 录屏（任意格式，自动转 WebM） | 使用场景照片（在用、在房间、在桌上） | 全景照片 |
| **Logo** | 透明 PNG，≥ 512 px（命名为 `logo.png`） | 同左 | 同左 |
| **音乐**（可选） | 用户授权的曲子 | 同左 | 同左；没有时自动原创配乐 |
| **配音**（可选） | `vo_*.wav` 录音，或 Kokoro 合成 | 同左 | 同左 |
| **文字** | README、brief.json、功能列表、规格、真实评价 | 同左 | 同左 |

`intake.py`（autofilm 会调用）能识别：
- **desktop** / **phone**：界面截图，依据平坦像素区域和清晰的文字边缘判断。
- **photo**：自然照片。
- **cutout**：透明底物体。
- **figure**：图表。
- **logo**，以及录屏、音乐、配音、文档。

文件名也有帮助：`*detail*`、`*texture*`、`*macro*` 会进入细节拍点，`*lifestyle*`、`*scene*` 进入照片拍点，`*screen*`、`*ui*` 标记为界面。分类是启发式的，请核对打印出的汇总。

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
