#!/usr/bin/env bash
# Install this skill for one or more AI coding agents (macOS / Linux; works with macOS's bash 3.2).
#   ./install.sh                 # universal ~/.agents/skills + Claude Code + Codex
#   ./install.sh all             # every known agent folder
#   ./install.sh claude codex opencode antigravity deepseek kimi gemini cursor copilot qwen trae
# Each target gets a COPY (some agents resolve or reject symlinks). Re-run after updating the skill.
set -eu
NAME=product-promo-film
SRC="$(cd "$(dirname "$0")" && pwd)"
ALL="agents claude codex opencode antigravity deepseek kimi gemini cursor copilot qwen trae"
dest() {
  case "$1" in
    agents) echo "$HOME/.agents/skills" ;;            # shared: OpenCode, DeepSeek Harness, Deep Code, Kimi Code, Cursor; ZCode via its importer
    claude) echo "$HOME/.claude/skills" ;;            # Claude Code (OpenCode / Copilot also read it)
    codex) echo "$HOME/.codex/skills" ;;              # OpenAI Codex
    opencode) echo "$HOME/.config/opencode/skills" ;; # OpenCode global
    antigravity) echo "$HOME/.gemini/antigravity/skills" ;;  # Google Antigravity global
    deepseek) echo "$HOME/.dsh/skills" ;;             # DeepSeek Harness personal
    kimi) echo "$HOME/.kimi-code/skills" ;;           # Kimi Code CLI
    gemini) echo "$HOME/.gemini/skills" ;;            # Gemini CLI (community convention)
    cursor) echo "$HOME/.cursor/skills" ;;            # Cursor
    copilot) echo "$HOME/.copilot/skills" ;;          # GitHub Copilot personal skills
    qwen) echo "$HOME/.qwen/skills" ;;                # Qwen Code (community convention)
    trae) echo "$HOME/.trae/skills" ;;                # Trae (community convention)
    *) echo "" ;;
  esac
}
targets="$*"; [ -z "$targets" ] && targets="agents claude codex"
[ "$targets" = "all" ] && targets="$ALL"
for t in $targets; do
  d="$(dest "$t")"; [ -z "$d" ] && { echo "unknown target: $t (known: $ALL)"; exit 1; }
  mkdir -p "$d"; rm -rf "${d:?}/$NAME"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude node_modules --exclude film_out --exclude .git "$SRC/" "$d/$NAME/"
  else
    mkdir -p "$d/$NAME"; (cd "$SRC" && tar --exclude node_modules --exclude film_out --exclude .git -cf - .) | (cd "$d/$NAME" && tar -xf -)
  fi
  # the capture and render tools need Playwright: share this folder's node_modules (local, nothing downloaded)
  if [ -d "$SRC/node_modules/playwright" ]; then ln -s "$SRC/node_modules" "$d/$NAME/node_modules"; fi
  echo "installed → $d/$NAME"
done
echo "Next: cd \"$SRC\" && npm i playwright && npx playwright install chromium && python3 scripts/doctor.py"
