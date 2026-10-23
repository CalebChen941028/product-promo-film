# Install Reelwright (片匠) for AI coding agents on Windows (PowerShell).
#   .\install.ps1                      # %USERPROFILE%\.agents\skills + Claude Code + Codex
#   .\install.ps1 all                  # every known agent folder
#   .\install.ps1 claude codex antigravity
param([string[]]$Targets = @('agents', 'claude', 'codex'))
$Name = 'reelwright'
$Src = Split-Path -Parent $MyInvocation.MyCommand.Path
$H = $env:USERPROFILE
$Dest = @{
  agents = "$H\.agents\skills"; claude = "$H\.claude\skills"; codex = "$H\.codex\skills"; opencode = "$H\.config\opencode\skills"
  antigravity = "$H\.gemini\antigravity\skills"; deepseek = "$H\.dsh\skills"; kimi = "$H\.kimi-code\skills"; gemini = "$H\.gemini\skills"
  cursor = "$H\.cursor\skills"; copilot = "$H\.copilot\skills"; qwen = "$H\.qwen\skills"; trae = "$H\.trae\skills"
}
if ($Targets -contains 'all') { $Targets = $Dest.Keys }
foreach ($t in $Targets) {
  if (-not $Dest.ContainsKey($t)) { Write-Error "unknown target: $t"; exit 1 }
  $d = Join-Path $Dest[$t] $Name
  New-Item -ItemType Directory -Force -Path $Dest[$t] | Out-Null
  if (Test-Path $d) { Remove-Item -Recurse -Force $d }
  robocopy $Src $d /E /XD node_modules film_out .git /NFL /NDL /NJH /NJS | Out-Null
  Set-Content -Path (Join-Path $d ".source") -Value $Src -Encoding UTF8   # the installed copy finds Playwright in the folder it came from
  Write-Host "installed -> $d"
}
Write-Host "Next: cd `"$Src`"; npm install; npx playwright install chromium; python scripts\doctor.py"
Write-Host "(keep this folder: the installed copies read Playwright from it; if you move it, run .\install.ps1 again)"
