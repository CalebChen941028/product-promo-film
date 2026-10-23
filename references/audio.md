# Music, voice-over, mix · 音乐、配音、混音

English first, 中文在后。

## English

### Music
- Only music the user owns or licensed. `make_film.py` converts it to 48 kHz WAV and runs `beat_grid.py` (BPM, first beat G, bar length, per-bar energy, section changes).
- **Too short?** Repeat a chorus: in film.json `"music": {"file": …, "extend": {"from_bar": 56, "to_bar": 72}}`. Pick a span whose last bar flows into its first (both downbeats with a strong hit) — look for two identical phrases in `film_out/audio/grid.json` (same energy pattern 16/32 bars apart). Verify the printed seam jump ≤ the song's p99.9.
- The film length = the (extended) music; the end card absorbs the remaining bars (`"bars": "rest"`).

### Voice-over (Kokoro: Apache-2.0 model and package; its dependencies have their own licences, see THIRD_PARTY_NOTICES.md)
Why not system voices: their licences often restrict commercial use (check yours), and they sound robotic without premium packs.

**Kokoro setup** (ask the user first; downloads ≈ 650 MB: PyPI `kokoro` + PyTorch, Hugging Face `hexgrad/Kokoro-82M`, spaCy `en_core_web_sm` from GitHub):
```bash
uv venv -p python3.12 ~/.venvs/kokoro          # or: python3.12 -m venv ~/.venvs/kokoro
uv pip install -p ~/.venvs/kokoro/bin/python kokoro soundfile
uv pip install -p ~/.venvs/kokoro/bin/python "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl"
mkdir -p ~/.cache && cp -R ~/.venvs/kokoro/lib/python3.12/site-packages/espeakng_loader/espeak-ng-data ~/.cache/kes
```
Then in film.json: `"voice": {"engine": "kokoro", "python": "~/.venvs/kokoro/bin/python", "voice": "am_michael"}`. The vo stage runs offline: if the model (≈ 330 MB) or the voice (≈ 0.5 MB each) is not downloaded yet, it stops and names the voices that are. After the user agrees, add `"allow_download": true` for one run (set `HF_HUB_DISABLE_XET=1` if Hugging Face transfers fail). autofilm and doctor find `~/.venvs/kokoro` on their own and prefer a voice that is already downloaded.
Voices: `am_michael` deep US male (trailer), `af_heart` warm US female, `bf_emma` British female, `bm_george` British male. `lang`: `a` US English, `b` British, `z` Mandarin, `j` Japanese.

Writing for the ear: ~2.5 words/s; one sentence per line; numbers as words in `en` ("three hundred"), digits in `cap` ("300"). Lines that do not fit are sped up to 1.12× max; if a line still says `OVER`, shorten it.

User recordings instead: `"voice": {"engine": "files", "files": {"<say id>": "rec/line1.wav"}}` (give each `say` an `id`). Captions only: `"engine": "none"`.

### Mix targets (mix_audio.py)
| Measure | Target |
| --- | --- |
| speech level | RMS-normalised ≈ −17 dBFS (never peak-normalise: speech ends up only +1 dB over music) |
| music under speech | ducked ≈ −11 dB (80 ms attack, 450 ms release) |
| speech over music | median ≈ +10 dB |
| final loudness | −14 LUFS, true peak −1 dB (applied at mux) |
You cannot hear the result: say so, and ask the user to listen.

### Sound design (sfx.py, synthesised, royalty-free)
`build` writes `film_out/audio/sfx_cues.json` from the scenes; `finish` synthesises it into a bus and mixes it under the music, ducked under speech.
- **Where:** camera cuts and hits only; the one hero moment gets an impact plus a riser; the logo gets a soft shimmer or chime; counters get ticks. About 10 cues a minute.
- **Level:** peaks −27 to −9 dBFS before the mix, plus `cinema.sfx_gain_db` (default −2). Raise it only if the user asks.
- **Palette:** follows the motion language (`references/director.md` §3). Listen to every sound: `python3 scripts/sfx.py --demo sfx_demo.wav`.
- **Off:** `"cinema": {"sfx": "off"}`.

### No music supplied? An original underscore (make_music.py)
Leave out `music.file` (or set `"music": {"generate": {"mood": "auto"}}`). At build time a bed is composed **bar for bar from the scene plan**:
- sections change exactly on the cuts: intro pads under the cover, rhythm on the features, drums on the proof, the full arrangement at the finale;
- half a beat of silence falls before the hero downbeat;
- the end card rings out on a held chord.

It is pure numpy: additive synthesis, FFT-filtered percussion and convolution reverb. It is seeded (`seed`), original and royalty-free.

| Mood | BPM | Feel | Genres |
| --- | --- | --- | --- |
| `cinematic-pulse` | 104 | minor, plucked ostinato, low toms | software, hardware, industrial |
| `minimal-electronic` | 120 | clean 16th plucks, four-on-the-floor | dev tools, data, fintech, events |
| `warm-piano` | 88 | piano + strings, soft kick and shaker | care, education, mission |
| `bright-pop` | 118 | offbeat plucks, claps, glockenspiel | consumer apps, kids |
| `luxe-lounge` | 90 | electric piano, deep bass, brushed groove | fashion, beauty, luxury |
| `ambient-air` | 86 | airy pads and bells, almost no drums | travel, living, wellness |
| `warm-acoustic` | 98 | strummed plucks, shaker, warm bass | food, lifestyle, handmade |

Listen to a mood on its own: `python3 scripts/make_music.py --mood warm-piano --bars 32 --out try.wav`. Be honest with the user: this is a tasteful underscore, not a hit song. For a flagship film, a licensed track they love is still better.


## 中文

### 音乐
- 只用用户拥有或已授权的音乐。`make_film.py` 会转成 48 kHz WAV 并运行 `beat_grid.py`（BPM、首拍 G、小节长度、逐小节能量、段落变化）。
- **太短**：重复一段副歌，在 film.json 写 `"music": {"file": …, "extend": {"from_bar": 56, "to_bar": 72}}`。选择“段尾能自然接回段首”的片段（两端都是带重音的强拍），可在 `film_out/audio/grid.json` 中找能量模式相同、相隔 16 / 32 小节的两段。确认打印的拼接跳变不超过全曲 p99.9。
- 片长等于（延长后的）音乐长度，剩余小节由结尾页（`"bars": "rest"`）吸收。

### 配音（Kokoro：模型与软件包为 Apache-2.0；其依赖另有许可，见 THIRD_PARTY_NOTICES.md）
为什么不用系统语音：它们的授权通常限制商用（请核对你自己的），且不装高级语音包时很机械。

**Kokoro 安装**（先征得用户同意；下载约 650 MB：PyPI 的 `kokoro` + PyTorch、Hugging Face 的 `hexgrad/Kokoro-82M`、GitHub 的 spaCy `en_core_web_sm`）：命令见上方英文代码块。之后在 film.json 写 `"voice": {"engine": "kokoro", "python": "~/.venvs/kokoro/bin/python", "voice": "am_michael"}`。首次运行会下载模型；Hugging Face 传输失败时设置 `HF_HUB_DISABLE_XET=1`。
配音阶段离线运行：模型（约 330 MB）或音色（每个约 0.5 MB）尚未下载时会停下，并列出已下载的音色；用户同意后，加 `"allow_download": true` 运行一次。autofilm 与 doctor 会自动找到 `~/.venvs/kokoro`，并优先选用已下载的音色。
音色：`am_michael` 低沉美式男声（预告片风格）、`af_heart` 温暖美式女声、`bf_emma` 英式女声、`bm_george` 英式男声。`lang`：`a` 美式英语、`b` 英式、`z` 普通话、`j` 日语。

写给耳朵听：约每秒 2.5 个词；每行一句；`en` 里数字写成单词，`cap` 里写阿拉伯数字。放不下的句子最多提速到 1.12 倍，仍显示 `OVER` 就删字。

用户自己录音：`"voice": {"engine": "files", "files": {"<say id>": "rec/line1.wav"}}`（给每条 `say` 加 `id`）。只要字幕：`"engine": "none"`。

### 混音目标
见上方英文表格：人声按 RMS 归一到约 −17 dBFS；有人声时音乐闪避约 −11 dB；人声比音乐高约 10 dB（中位数）；成片 −14 LUFS、真峰值 −1 dB。你听不到声音，要如实说明并请用户试听。

### 声音设计（sfx.py，程序合成，无版权问题）
`build` 根据场景写出 `film_out/audio/sfx_cues.json`，`finish` 将其合成为音效总线，压在音乐之下，并在人声处自动避让。
- **位置**：只在镜头转场和击点处；唯一的高潮有一次重击加上升音；Logo 有轻柔的闪光音或钟声；数字有轻点声。约每分钟 10 个。
- **电平**：混音前峰值 −27 到 −9 dBFS，再加 `cinema.sfx_gain_db`（默认 −2）。只有用户要求时才调高。
- **音色**：随动效语言变化（`references/director.md` 第 3 节）。试听全部音效：`python3 scripts/sfx.py --demo sfx_demo.wav`。
- **关闭**：`"cinema": {"sfx": "off"}`。

### 没有音乐？原创配乐（make_music.py）
不填 `music.file`（或写 `"music": {"generate": {"mood": "auto"}}`），构建时会**按场景逐小节**作曲：
- 段落恰好在切点变化：封面下是前奏铺底，功能段加入节奏，证明段加入鼓，高潮段编制最满；
- 高潮重拍前有半拍静默；
- 结尾页在长音和弦上自然收尾。

纯 numpy 实现：加法合成、FFT 滤波打击乐、卷积混响。固定随机种子（`seed`）可复现，原创且无版权问题。七种情绪见上方英文表格。

单独试听：`python3 scripts/make_music.py --mood warm-piano --bars 32 --out try.wav`。请对用户如实说明：这是有品味的配乐铺底，不是热门歌曲；旗舰宣传片仍建议使用用户喜爱的授权曲目。

