# Music, voice-over, mix · 音乐、配音、混音

English first, 中文在后。

## English

### Music
- Only music the user owns or licensed. `make_film.py` converts it to 48 kHz WAV and runs `beat_grid.py` (BPM, first beat G, bar length, per-bar energy, section changes).
- **Too short?** Repeat a chorus: in film.json `"music": {"file": …, "extend": {"from_bar": 56, "to_bar": 72}}`. Pick a span whose last bar flows into its first (both downbeats with a strong hit) — look for two identical phrases in `film_out/audio/grid.json` (same energy pattern 16/32 bars apart). Verify the printed seam jump ≤ the song's p99.9.
- The film length = the (extended) music; the end card absorbs the remaining bars (`"bars": "rest"`).

### Voice-over (Kokoro, Apache-2.0 — commercial use OK)
Why not system voices: Apple/Windows voices are licensed for personal non-commercial use and sound robotic without premium packs.

**Kokoro setup** (ask the user first; downloads ≈ 650 MB: PyPI `kokoro` + PyTorch, Hugging Face `hexgrad/Kokoro-82M`, spaCy `en_core_web_sm` from GitHub):
```bash
uv venv -p python3.12 ~/.venvs/kokoro          # or: python3.12 -m venv ~/.venvs/kokoro
uv pip install -p ~/.venvs/kokoro/bin/python kokoro soundfile
uv pip install -p ~/.venvs/kokoro/bin/python "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl"
mkdir -p ~/.cache && cp -R ~/.venvs/kokoro/lib/python3.12/site-packages/espeakng_loader/espeak-ng-data ~/.cache/kes
```
Then in film.json: `"voice": {"engine": "kokoro", "python": "~/.venvs/kokoro/bin/python", "voice": "am_michael"}`. First run downloads the model (set `HF_HUB_DISABLE_XET=1` if Hugging Face transfers fail).
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

## 中文

### 音乐
- 只用用户拥有或已授权的音乐。`make_film.py` 会转成 48 kHz WAV 并运行 `beat_grid.py`（BPM、首拍 G、小节长度、逐小节能量、段落变化）。
- **太短**：重复一段副歌，在 film.json 写 `"music": {"file": …, "extend": {"from_bar": 56, "to_bar": 72}}`。选择“段尾能自然接回段首”的片段（两端都是带重音的强拍），可在 `film_out/audio/grid.json` 中找能量模式相同、相隔 16 / 32 小节的两段。确认打印的拼接跳变不超过全曲 p99.9。
- 片长等于（延长后的）音乐长度，剩余小节由结尾页（`"bars": "rest"`）吸收。

### 配音（Kokoro，Apache-2.0，可商用）
为什么不用系统语音：Apple / Windows 语音仅限个人非商业用途，且不装高级语音包时很机械。

**Kokoro 安装**（先征得用户同意；下载约 650 MB：PyPI 的 `kokoro` + PyTorch、Hugging Face 的 `hexgrad/Kokoro-82M`、GitHub 的 spaCy `en_core_web_sm`）：命令见上方英文代码块。之后在 film.json 写 `"voice": {"engine": "kokoro", "python": "~/.venvs/kokoro/bin/python", "voice": "am_michael"}`。首次运行会下载模型；Hugging Face 传输失败时设置 `HF_HUB_DISABLE_XET=1`。
音色：`am_michael` 低沉美式男声（预告片风格）、`af_heart` 温暖美式女声、`bf_emma` 英式女声、`bm_george` 英式男声。`lang`：`a` 美式英语、`b` 英式、`z` 普通话、`j` 日语。

写给耳朵听：约每秒 2.5 个词；每行一句；`en` 里数字写成单词，`cap` 里写阿拉伯数字。放不下的句子最多提速到 1.12 倍，仍显示 `OVER` 就删字。

用户自己录音：`"voice": {"engine": "files", "files": {"<say id>": "rec/line1.wav"}}`（给每条 `say` 加 `id`）。只要字幕：`"engine": "none"`。

### 混音目标
见上方英文表格：人声按 RMS 归一到约 −17 dBFS；有人声时音乐闪避约 −11 dB；人声比音乐高约 10 dB（中位数）；成片 −14 LUFS、真峰值 −1 dB。你听不到声音，要如实说明并请用户试听。
