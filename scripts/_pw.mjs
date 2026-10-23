// Finds Playwright for scripts that run from the installed skill folder (capture_app.mjs, record_ui.mjs, …).
// Order: the usual place (the skill's own node_modules) → PLAYWRIGHT_NODE_MODULES → the folder the skill was installed
// from (install.sh / install.ps1 write it to .source) → ./node_modules → the global npm folder. Nothing is downloaded.
import { createRequire } from 'module';
import { pathToFileURL, fileURLToPath } from 'url';
import { execFileSync } from 'child_process';
import fs from 'fs';
import path from 'path';

export async function loadPlaywright() {
  try { return await import('playwright'); } catch {}
  const here = path.dirname(fileURLToPath(import.meta.url));
  const cand = [process.env.PLAYWRIGHT_NODE_MODULES];
  try { cand.push(path.join(fs.readFileSync(path.join(here, '..', '.source'), 'utf8').trim(), 'node_modules')); } catch {}
  cand.push(path.join(process.cwd(), 'node_modules'));
  try { cand.push(execFileSync('npm', ['root', '-g'], { encoding: 'utf8' }).trim()); } catch {}
  for (const c of cand) {
    if (!c) continue;
    try { return createRequire(path.join(c, 'x.js'))('playwright'); } catch {}
  }
  console.error('ERROR Playwright is not installed.\n  FIX: in the Reelwright folder run: npm install && npx playwright install chromium   (then python3 scripts/doctor.py)');
  process.exit(2);
}
