# Using the skill in different AI agents · 在不同智能体中使用

English first, 中文在后。The skill is plain files: `SKILL.md` (frontmatter `name` + `description`, both required by the strictest loaders) + scripts. Any agent that can read files and run shell commands can use it. `AGENTS.md` at the root is a short entry for agents that read AGENTS.md instead of skills.

## English

### Install
```bash
./install.sh            # ~/.agents/skills + Claude Code + Codex (copies, not symlinks)
./install.sh all        # every folder below
./install.sh antigravity deepseek kimi
```
Windows: `.\install.ps1` (same targets). After installing: `npm install && npx playwright install chromium` in the folder you cloned (the installed copies read Playwright from it through the `.source` file the installer writes, in any order), then `python3 scripts/doctor.py`. If you move the cloned folder, run the installer again.

| Agent | Global skills folder | Project folder | Source |
| --- | --- | --- | --- |
| Universal (shared) | `~/.agents/skills/` | `.agents/skills/` | read by OpenCode, DeepSeek Harness, Deep Code, Kimi Code, Cursor |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | Anthropic docs |
| OpenAI Codex | `~/.codex/skills/` | — | Codex |
| OpenCode | `~/.config/opencode/skills/` (+ `~/.claude/skills`, `~/.agents/skills`) | `.opencode/skills/` | opencode.ai/docs/skills |
| Google Antigravity | `~/.gemini/antigravity/skills/` | `.agent/skills/` | Google Antigravity codelab |
| DeepSeek Harness (dsh) | `~/.dsh/skills/`, `~/.agents/skills/` | `.dsh/skills/`, `.agents/skills/` | community write-up (v0.1.0-rc.5) |
| DeepSeek Deep Code | `~/.agents/skills/` | `.deepcode/skills/` | api-docs.deepseek.com |
| Kimi Code CLI | `~/.kimi-code/skills/`, `~/.agents/skills/` | `.kimi-code/skills/`, `.agents/skills/` | kimi.com docs |
| ZCode (Zhipu) | via Settings → Skills (import), `~/.agents/skills/` used by importers | — | community guides; check in-app |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/`, `.agents/skills/` | cursor.com/docs/skills |
| GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` | community guides |
| Gemini CLI · Qwen Code · Trae | `~/.gemini/skills/` · `~/.qwen/skills/` · `~/.trae/skills/` | `.gemini/` · `.qwen/` · `.trae/` `skills/` | community conventions; verify in each tool |

Paths change between versions — if the agent does not list the skill, check its docs, or simply tell it: "Read `<path>/SKILL.md` and follow it."

### Agents without skill support
Point them at `AGENTS.md` (copy it into the project root, or paste: *"Follow the procedure in `<skill>/SKILL.md`; use the scripts in `<skill>/scripts`."*).

### Why it works with mid-sized models
- The film is **data** (`film.json`), not code: scene types, bars, texts, rects.
- `make_film.py --stage check` validates everything with `FIX:` instructions.
- `--stage qa` measures overlaps, off-frame elements and caption collisions numerically — no visual judgement required.
- Defaults (sizes, timings, mix levels) are the tuned values from a finished commercial film.

## 中文

### 安装
```bash
./install.sh            # 复制到 ~/.agents/skills、Claude Code、Codex（复制，不用软链接）
./install.sh all        # 复制到下表全部目录
./install.sh antigravity deepseek kimi
```
Windows 用 `.\install.ps1`。安装后在你克隆的文件夹里运行 `npm install && npx playwright install chromium`（安装好的副本通过安装器写入的 `.source` 文件读取这里的 Playwright，先后顺序不限），再运行 `python3 scripts/doctor.py`。移动了克隆的文件夹时，请重新运行安装器。

各智能体的目录见上方英文表格。路径会随版本变化：如果智能体没有列出这个 skill，查它的文档，或直接告诉它“读取 `<路径>/SKILL.md` 并照做”。

### 不支持 skill 的智能体
把 `AGENTS.md` 复制到项目根目录，或在对话里说明：“按 `<skill>/SKILL.md` 的流程执行，脚本在 `<skill>/scripts`。”

### 为什么中等规模模型也能做出好效果
- 片子是**数据**（`film.json`）而不是代码：只需填写场景类型、小节、文字、坐标。
- `make_film.py --stage check` 逐项校验，并给出 `FIX:` 修复指令。
- `--stage qa` 用数值检查遮挡、出画、字幕冲突，不依赖视觉判断。
- 尺寸、节奏、混音电平等默认值，都取自一部完成的商业成片。
