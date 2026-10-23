// Record the product's REAL UI in motion, run from its own source in a sandbox — smooth, real interactions instead of stills.
// Only with the user's permission for this product (they own the source and said yes): pass --approved-by-user.
//
// Usage:
//   node scripts/record_ui.mjs recipe.json --approved-by-user [--only take,take]
//     → <out>/<take>.webm (1920×1080 × scale, 30 fps, high quality) + <take>.png (poster, its last frame) per take.
//       The .webm files are real screen recordings: intake.py files them as screen clips; use them in clip / footage scenes.
//
// recipe.json (see templates/record.example.json):
//   { "serve": { "cmd": "npm run dev -- --port 5199 --strictPort", "cwd": "/path/to/repo/frontend", "env": {"VITE_DEMO": "1"},
//                "url": "http://localhost:5199", "ready_timeout": 90000 },   started here, in its own process group, stopped after
//     or "url": "http://localhost:5199"                                      a server the user already runs for this
//     or "static": "/path/to/repo/dist"                                      a built frontend, served here on a free port
//     "out": "materials", "viewport": [1920, 1080], "scale": 2 (a 3840×2160 recording: sharp when a scene zooms in; 1 = 1080p),
//     "network": "local" (default: only localhost / 127.0.0.1 / file / data are reachable; every other request is refused)
//              | "open" (only when the user said the product may reach its real services),
//     "mock": [ { "url": "**/api/analyze", "json": "mock/analyze.json", "status": 200, "delay": 900 } ],   demo responses for a backend
//     "storage": { "<localStorage key>": "<value>" },
//     "cursor": true (default: a soft cursor glides between targets, a ripple on each click),
//     "takes": [ { "name": "07-analysis-run", "steps": [ … ], "tail": 1200 } ] }   every take starts from a fresh, empty browser profile
// Steps (one key each, plus options):
//   {"goto": "/route"}  {"click": "visible text", "exact": false}  {"css": "button.run"}  {"hover": "text"}
//   {"type": "text typed key by key", "into": "placeholder or label", "delay": 70}   {"fill": "text", "into": "…"}
//   {"key": "Enter"}   {"upload": "demo/data.csv", "input": 0}   {"drag": "source text", "to": "target text"}
//   {"wheel": [0, 300], "times": 4}   {"select": "value", "in": "select css"}   {"wait_for": "text", "timeout": 30000}
//   {"hold": 1500}  keep recording what is on screen (let a result settle, let the eye read)
// Rules: a sandbox, never the user's installed app or profile, never their real data or keys; never kill anything but the
// server this script started; demo data only, and the film says so. A failed step saves _fail-<take>.png and moves on.
import { chromium } from 'playwright';
import { spawn, execFileSync } from 'child_process';
import { createServer } from 'http';
import fs from 'fs';
import path from 'path';
import os from 'os';

const args = process.argv.slice(2);
const recipePath = args.find((a) => !a.startsWith('--'));
if (!recipePath) { console.error('usage: node scripts/record_ui.mjs recipe.json --approved-by-user [--only a,b]'); process.exit(2); }
if (!args.includes('--approved-by-user')) {
  console.error('ERROR running a product from its source needs the user\'s permission for THIS product.\n  FIX: ask the user ("may I run <repo> in a sandbox, with demo data, to record it?"); on yes, add --approved-by-user');
  process.exit(2);
}
const only = (args[args.indexOf('--only') + 1] || '').split(',').filter((x) => args.includes('--only') && x);
const R = JSON.parse(fs.readFileSync(recipePath, 'utf8'));
const base = path.dirname(path.resolve(recipePath));
const rel = (p) => (path.isAbsolute(p) ? p : path.join(base, p));
const out = rel(R.out || 'materials'); fs.mkdirSync(out, { recursive: true });
const [VW, VH] = R.viewport || [1920, 1080], SC = R.scale || 1;   // scale 2 = a 4K recording, sharp when the film zooms in
const FFMPEG = (() => { try { return execFileSync('python3', ['-c', 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())']).toString().trim(); } catch { return 'ffmpeg'; } })();
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ---------- serve ----------
let child = null, staticServer = null, url = R.url;
async function waitFor(u, ms) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) { try { const r = await fetch(u); if (r.status < 500) return true; } catch {} await sleep(600); }
  return false;
}
if (R.serve) {
  console.log(`== serve: ${R.serve.cmd}  (in ${R.serve.cwd})`);
  child = spawn(R.serve.cmd, { cwd: rel(R.serve.cwd), env: { ...process.env, BROWSER: 'none', ...(R.serve.env || {}) }, shell: true, detached: true, stdio: ['ignore', 'pipe', 'pipe'] });
  const log = fs.createWriteStream(path.join(out, '_serve.log')); child.stdout.pipe(log); child.stderr.pipe(log);
  url = R.serve.url;
  if (!(await waitFor(url, R.serve.ready_timeout || 90000))) { console.error(`ERROR the server did not answer at ${url}.\n  FIX: read ${path.join(out, '_serve.log')}; check the command, the port and that dependencies are installed`); stop(); process.exit(1); }
} else if (R.static) {
  const root = rel(R.static);
  const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.wasm': 'application/wasm' };
  staticServer = createServer((req, res) => {
    let p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
    if (!p.startsWith(root)) { res.writeHead(403).end(); return; }
    if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) p = fs.existsSync(path.join(p, 'index.html')) ? path.join(p, 'index.html') : path.join(root, 'index.html');   // SPA fallback
    res.writeHead(200, { 'content-type': types[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res);
  });
  await new Promise((r) => staticServer.listen(0, '127.0.0.1', r));
  url = `http://127.0.0.1:${staticServer.address().port}`;
}
if (!url) { console.error('ERROR the recipe needs "serve", "url" or "static"'); process.exit(2); }
function stop() {
  if (child) { try { process.kill(-child.pid, 'SIGTERM'); } catch {} }   // only the server this script started (its own process group)
  if (staticServer) staticServer.close();
}
process.on('SIGINT', () => { stop(); process.exit(130); });

// ---------- cursor overlay (in the page: the recording sees it) ----------
const CURSOR = `(() => { if (window.__pfCursor) return; const c = document.createElement('div'); c.id = '__pf_cursor';
  c.innerHTML = '<svg viewBox="0 0 24 24" width="30" height="30"><path d="M4 2 L4 19 L8.6 14.9 L11.6 22 L14.6 20.7 L11.7 13.9 L18 13.9 Z" fill="#fff" stroke="#111" stroke-width="1.3" stroke-linejoin="round"/></svg>';
  Object.assign(c.style, { position: 'fixed', left: '-40px', top: '-40px', zIndex: 2147483647, pointerEvents: 'none', filter: 'drop-shadow(0 3px 5px rgba(0,0,0,.35))', transition: 'none' });
  const add = () => document.body && document.body.appendChild(c); add(); document.addEventListener('DOMContentLoaded', add);
  window.__pfCursor = (x, y) => { c.style.left = x + 'px'; c.style.top = y + 'px'; };
  window.__pfRipple = (x, y) => { const r = document.createElement('div'); Object.assign(r.style, { position: 'fixed', left: x - 24 + 'px', top: y - 24 + 'px', width: '48px', height: '48px', borderRadius: '50%', border: '3px solid rgba(80,170,255,.9)', zIndex: 2147483646, pointerEvents: 'none', transition: 'transform .45s ease-out, opacity .45s ease-out' });
    document.body.appendChild(r); requestAnimationFrame(() => { r.style.transform = 'scale(1.9)'; r.style.opacity = '0'; }); setTimeout(() => r.remove(), 600); }; })();`;

// ---------- recording: CDP screencast → constant 30 fps ----------
async function record(page, fn, file) {
  const cdp = await page.context().newCDPSession(page);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'pf-rec-')); const frames = [];
  cdp.on('Page.screencastFrame', async (f) => {
    const p = path.join(dir, `${String(frames.length).padStart(6, '0')}.jpg`);
    fs.writeFileSync(p, Buffer.from(f.data, 'base64')); frames.push({ p, t: f.metadata.timestamp });
    try { await cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }); } catch {}
  });
  await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 95, maxWidth: VW * SC, maxHeight: VH * SC, everyNthFrame: 1 });
  const t0 = Date.now() / 1000;
  const tEnd0 = Date.now();
  let err = null;
  try { await fn(); } catch (e) { err = e; }
  await sleep(250); const tStop = Date.now() / 1000; await cdp.send('Page.stopScreencast');
  if (frames.length < 2) { fs.rmSync(dir, { recursive: true, force: true }); throw err || new Error('no frames recorded'); }
  // a frame lasts until the next one: write a concat list with real durations, then resample to 30 fps
  if (frames.length && frames[0].t > t0) frames[0].t = t0;   // the first frame stands from the moment recording began
  const list = frames.map((f, i) => `file '${f.p}'\nduration ${Math.max(0.001, ((frames[i + 1] || { t: Math.max(tStop, f.t + 0.04) }).t - f.t)).toFixed(4)}`).join('\n') + `\nfile '${frames[frames.length - 1].p}'\n`;
  fs.writeFileSync(path.join(dir, 'list.txt'), list);
  execFileSync(FFMPEG, ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(dir, 'list.txt'), '-vf', `fps=30,scale=${VW * SC}:${VH * SC}:flags=lanczos,format=yuv420p`,
    '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '20', '-row-mt', '1', '-deadline', 'good', '-cpu-used', '3', file]);
  fs.copyFileSync(frames[frames.length - 1].p, file.replace(/\.webm$/, '.jpg'));
  execFileSync(FFMPEG, ['-y', '-loglevel', 'error', '-i', file.replace(/\.webm$/, '.jpg'), file.replace(/\.webm$/, '.png')]); fs.rmSync(file.replace(/\.webm$/, '.jpg'));
  fs.rmSync(dir, { recursive: true, force: true });
  console.log(`  ✓ ${path.basename(file)}  ${frames.length} frames over ${((Date.now() - tEnd0) / 1000).toFixed(1)} s`);
  if (err) throw err;
}

// ---------- steps ----------
let mouse = [VW / 2, VH / 2];
async function glide(page, x, y, ms = 650) {
  const n = Math.max(8, Math.round(ms / 16)), [x0, y0] = mouse;
  for (let i = 1; i <= n; i++) {
    const k = i / n, e = k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;   // ease in-out
    const px = x0 + (x - x0) * e, py = y0 + (y - y0) * e;
    await page.mouse.move(px, py); if (R.cursor !== false) await page.evaluate(([a, b]) => window.__pfCursor && window.__pfCursor(a, b), [px, py]);
    await sleep(ms / n);
  }
  mouse = [x, y];
}
const byText = (page, text, exact = false) => page.getByText(text, { exact }).first();
const field = (page, label) => page.getByPlaceholder(label).or(page.getByLabel(label)).first();
async function center(loc) { await loc.scrollIntoViewIfNeeded(); const b = await loc.boundingBox(); if (!b) throw new Error('not visible'); return [b.x + b.width / 2, b.y + b.height / 2]; }
async function clickAt(page, loc) {
  const [x, y] = await center(loc); await glide(page, x, y);
  if (R.cursor !== false) await page.evaluate(([a, b]) => window.__pfRipple && window.__pfRipple(a, b), [x, y]);
  await page.mouse.down(); await sleep(70); await page.mouse.up();
}
async function run(page, s) {
  if (s.goto) await page.goto(new URL(s.goto, url).href, { waitUntil: 'networkidle' }).catch(() => {});
  else if (s.click) await clickAt(page, byText(page, s.click, s.exact));
  else if (s.css) await clickAt(page, page.locator(s.css).nth(s.nth || 0));
  else if (s.hover) { const [x, y] = await center(byText(page, s.hover, s.exact)); await glide(page, x, y); }
  else if (s.type != null) { const f = field(page, s.into); await clickAt(page, f); await f.pressSequentially(String(s.type), { delay: s.delay || 70 }); }
  else if (s.fill != null) { const f = field(page, s.into); await clickAt(page, f); await f.fill(String(s.fill)); }
  else if (s.key) await page.keyboard.press(s.key);
  else if (s.upload) await page.locator('input[type=file]').nth(s.input || 0).setInputFiles(rel(s.upload));
  else if (s.drag) {
    const [x0, y0] = await center(byText(page, s.drag, s.exact)), [x1, y1] = await center(byText(page, s.to, s.exact));
    await glide(page, x0, y0); await page.mouse.down(); await glide(page, x1, y1, 900); await page.mouse.up();
  } else if (s.wheel) { for (let i = 0; i < (s.times || 1); i++) { await page.mouse.wheel(s.wheel[0], s.wheel[1]); await sleep(120); } }
  else if (s.select != null) await page.locator(s.in).first().selectOption(String(s.select));
  else if (s.wait_for) await byText(page, s.wait_for).waitFor({ timeout: s.timeout || 30000 });
  else if (s.hold) { /* recording continues */ }
  await sleep(s.hold || s.wait || 350);
}

// ---------- takes ----------
const browser = await chromium.launch();
let failed = 0;
try {
  for (const take of R.takes || []) {
    if (only.length && !only.includes(take.name)) continue;
    console.log(`== take ${take.name}`);
    const ctx = await browser.newContext({ viewport: { width: VW, height: VH }, deviceScaleFactor: SC, acceptDownloads: true });   // a fresh, empty profile per take
    const allow = (u) => /^(data:|blob:|file:|about:)/.test(u) || /^https?:\/\/(localhost|127\.0\.0\.1|\[::1\])(:\d+)?\//.test(u);
    if ((R.network || 'local') === 'local') await ctx.route('**/*', (r) => (allow(r.request().url()) ? r.continue() : r.abort()));
    for (const m of R.mock || []) {
      await ctx.route(m.url, async (r) => { if (m.delay) await sleep(m.delay);
        r.fulfill({ status: m.status || 200, contentType: 'application/json', body: m.json ? fs.readFileSync(rel(m.json), 'utf8') : JSON.stringify(m.body ?? {}) }); });
    }
    if (R.storage) await ctx.addInitScript((kv) => { for (const [k, v] of Object.entries(kv)) localStorage.setItem(k, v); }, R.storage);
    if (R.cursor !== false) await ctx.addInitScript(CURSOR);
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: 'networkidle' }).catch(() => {});
    mouse = [VW / 2, VH / 2];
    try {
      await record(page, async () => { for (const s of take.steps || []) await run(page, s); await sleep(take.tail ?? 1000); }, path.join(out, `${take.name}.webm`));
    } catch (e) {
      failed++; await page.screenshot({ path: path.join(out, `_fail-${take.name}.png`) }).catch(() => {});
      console.error(`  ✗ ${take.name}: ${String(e.message || e).split('\n')[0]}  (see _fail-${take.name}.png)`);
    }
    await ctx.close();
  }
} finally { await browser.close(); stop(); }
console.log(failed ? `${failed} take(s) failed` : 'all takes recorded');
process.exit(failed ? 1 : 0);
