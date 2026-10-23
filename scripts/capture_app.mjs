// Capture the REAL product UI from a shot list — no Playwright code to write.
// Works with an installed Electron desktop app (macOS .app / Windows .exe) or a web app / dev server URL.
//
// Usage:
//   node scripts/capture_app.mjs explore --app "/Applications/X.app" [--steps '[{"click":"New project"}]'] [--out shots]
//   node scripts/capture_app.mjs explore --url http://localhost:5173/ [--steps steps.json]
//       → <out>/explore.png + explore.json: what is on screen, every clickable text, every input. Read them, then write the shot list.
//   node scripts/capture_app.mjs shoot shots.json [--only name,name]
//       → one PNG per "shot" step (3840×2160 = a 1920×1080 window at 2×), plus downloads and tall captures.
//
// shots.json (see templates/shots.example.json):
//   { "app": "/Applications/X.app" | "url": "http://…", "out": "materials",
//     "reuse": false (default: a fresh launch per scenario; true = one launch, the window reloads between scenarios — faster, only if the app starts clean on reload),
//     "profile": "copy" (default: the user's saved settings, copied — the real profile is never touched) | "fresh",
//     "profile_extra": ["secrets"]  more profile entries to copy, only when the user asked (e.g. to film the AI they configured),
//     "storage": { "<localStorage key>": "<value>" },          seeded before the app's scripts run
//     "mock_llm": { "port": 11434, "replies": "replies.json" }, scripted local model for AI features (scripts/mock_llm.mjs)
//     "macros": { "load": [ …steps… ] },                        shared preludes, used as {"use": "load"}
//     "scenarios": [ { "name": "import", "steps": [ … ] } ] }   each scenario starts from a fresh launch
// Steps (one key each, plus options):
//   {"click": "visible text"}            {"click": "text", "exact": false, "nth": 0, "wait": 800}
//   {"css": "button.run"}                click a CSS selector
//   {"upload": "data/demo.csv"}          set the file on the first <input type=file> that accepts it ("input": n to pick)
//   {"open_dialog": "data/demo.csv"}     the app's native Open dialog returns this file (Electron)
//   {"click": "导出", "exact": false}    part of the text (buttons with icons or emoji)      {"click_xy": [1855, 1017]}  last resort
//   {"fill": "text", "into": "placeholder or label"}     {"type": "text typed key by key", "into": "placeholder"}
//   {"select": 1, "in": "select.method"}  {"key": "Enter"}   {"key": "Escape"}   {"hover": "text"}   {"wheel": [0, 260], "times": 6}
//   {"wait_for": "text that appears when ready", "timeout": 60000}            {"sleep": 1500}
//   {"scroll": "text inside a scroll area", "by": 600}
//   {"shot": "03-results"}               {"shot": "name", "clip": "@text"}  a crop around the card or panel that holds that text (+16 px), never through it
//                                        {"shot": "name", "clip": [x, y, w, h]}  (CSS px of the 1920×1080 window)
//                                        every shot (clipped ones too, in the clip's coordinates) writes <name>.regions.json: the exact boxes of the panels,
//                                        headings and buttons on screen, so a point in film.json can say "rect": "@APA 三线表"
//   {"tall": "text inside a scrolling panel", "name": "ai-answer"}   the whole scroll content as one tall image
//   {"download": "button text", "file": "report.docx"}  real export (browser download, Save dialog or will-download)
//   {"seq": "typing", "ms": 4000, "every": 80}            timestamped frames for a moving moment
//   {"use": "load"}                      run the steps saved under "macros": {"load": [ … ]} (the prelude most scenarios share)
// Rules: drive the product the way a user would; never fake the UI; never type a user's real API key or password;
// skip settings, licence, account and delete screens unless the user asked. A failed step saves _fail-<scenario>.png
// and lists what CAN be clicked there; the next scenario still runs.
import { loadPlaywright } from './_pw.mjs';
const { chromium, _electron } = await loadPlaywright();
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn, execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const W = 1920, H = 1080, DPR = 2;
const argv = process.argv.slice(2);
const mode = argv[0];
const opt = (k, d) => { const i = argv.indexOf(`--${k}`); return i >= 0 ? argv[i + 1] : d; };
const die = (msg, fix) => { console.error(`ERROR ${msg}${fix ? `\n  FIX: ${fix}` : ''}`); process.exit(1); };

let cfg = {}, base = process.cwd();
if (mode === 'shoot') {
  const f = argv[1] || die('no shot list', 'node scripts/capture_app.mjs shoot shots.json');
  cfg = JSON.parse(fs.readFileSync(f, 'utf8')); base = path.dirname(path.resolve(f));
} else if (mode === 'explore') {
  cfg = { app: opt('app'), url: opt('url'), out: opt('out', 'shots'), profile: opt('profile', 'copy') };
  let s = opt('steps', '[]'); if (fs.existsSync(s)) s = fs.readFileSync(s, 'utf8');
  try { cfg.scenarios = [{ name: 'explore', steps: JSON.parse(s) }]; } catch { die('--steps is not JSON', `--steps '[{"click":"Button text"}]'`); }
} else {
  die('mode must be explore or shoot', 'node scripts/capture_app.mjs explore --app "/Applications/X.app"   (then)   node scripts/capture_app.mjs shoot shots.json');
}
if (!cfg.app && !cfg.url) die('no app or url', 'give --app "/Applications/X.app" (installed desktop app) or --url http://localhost:5173/ (web app)');
const rel = (p) => path.resolve(base, p);
const OUT = rel(cfg.out || 'shots'); fs.mkdirSync(OUT, { recursive: true });
const WORK = fs.mkdtempSync(path.join(os.tmpdir(), 'capture-app-'));

// ---------- launching ----------
function executableOf(app) {
  if (!fs.existsSync(app)) die(`${app} not found`, 'pass the installed app, e.g. "/Applications/My App.app" or "C:\\Program Files\\My App\\My App.exe"');
  if (!app.endsWith('.app')) return app;
  const plist = path.join(app, 'Contents', 'Info.plist');
  let exe = path.basename(app, '.app');
  try { exe = execFileSync('/usr/libexec/PlistBuddy', ['-c', 'Print :CFBundleExecutable', plist]).toString().trim(); } catch {}
  const isElectron = fs.existsSync(path.join(app, 'Contents', 'Frameworks', 'Electron Framework.framework')) || fs.existsSync(path.join(app, 'Contents', 'Resources', 'app.asar'));
  if (!isElectron) die(`${path.basename(app)} is not an Electron app, so it cannot be driven automatically`,
    'ask the user for screenshots (File ▸ open each screen, ⌘⇧4 then Space to grab the window), or run the product\'s web/dev build and use --url');
  return path.join(app, 'Contents', 'MacOS', exe);
}

const PROFILE_KEEP = ['Local Storage', 'IndexedDB', 'Preferences', 'Local State', 'Cookies', 'databases'];
let pristine = null;   // copy of the user's saved settings (never the real folder)
async function prepareProfile(exe) {
  if (cfg.profile === 'fresh') return;
  const probeDir = path.join(WORK, 'probe');
  const app = await _electron.launch({ executablePath: exe, args: [`--user-data-dir=${probeDir}`], timeout: 60000 });
  const [name, appData] = await app.evaluate(({ app }) => [app.getName(), app.getPath('appData')]);
  const tree = process.platform === 'win32' ? new Set() : treeOf([app.process()?.pid]);
  await Promise.race([app.close().catch(() => {}), new Promise((r) => setTimeout(r, 10000))]);
  reapOurs(tree);
  const real = path.join(appData, name);
  pristine = path.join(WORK, 'pristine'); fs.mkdirSync(pristine, { recursive: true });
  if (!fs.existsSync(real)) { console.log(`profile: none saved at ${real} — the app starts fresh (first-run screens may appear)`); return; }
  // "profile_extra": more entries of the user's profile to copy, opt-in — e.g. ["secrets"] when the user asked to film the AI
  // they configured (the app's own encrypted key store; it stays encrypted, lives only in this run's temp copy, deleted at exit)
  for (const k of [...PROFILE_KEEP, ...(cfg.profile_extra || [])]) if (fs.existsSync(path.join(real, k))) fs.cpSync(path.join(real, k), path.join(pristine, k), { recursive: true });
  console.log(`profile: copied the saved settings from ${real} (the real profile is not touched)`);
}

async function launch(n) {
  if (cfg.url) {
    const browser = await chromium.launch();
    const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: DPR, locale: cfg.locale || 'zh-CN', acceptDownloads: true });
    await ctx.addInitScript((kv) => { try { for (const [k, v] of Object.entries(kv)) localStorage.setItem(k, v); } catch {} }, cfg.storage || {});
    const page = await ctx.newPage();
    await page.goto(cfg.url); await page.waitForTimeout(cfg.boot_ms || 2000);
    return { page, close: () => browser.close(), electron: null };
  }
  const ud = path.join(WORK, `ud${n}`);
  if (pristine) fs.cpSync(pristine, ud, { recursive: true }); else fs.mkdirSync(ud, { recursive: true });
  const app = await _electron.launch({ executablePath: EXE, args: [`--user-data-dir=${ud}`, `--force-device-scale-factor=${DPR}`], timeout: 90000 });   // the flag makes screenshots 2× (CDP emulation alone does not)
  const close = async () => {   // never hang; then end only what this run started (the app and anything it spawned from our temp profile)
    const tree = process.platform === 'win32' ? new Set() : treeOf([app.process()?.pid]);   // before closing: children are re-parented after
    await Promise.race([app.close().catch(() => {}), new Promise((r) => setTimeout(r, 10000))]);
    reapOurs(tree);
  };
  const page = await app.firstWindow();
  if (cfg.storage && Object.keys(cfg.storage).length) {
    await page.evaluate((kv) => { for (const [k, v] of Object.entries(kv)) localStorage.setItem(k, v); }, cfg.storage);
    await page.reload();
  }
  const cdp = await page.context().newCDPSession(page);
  const size = (h = H) => cdp.send('Emulation.setDeviceMetricsOverride', { width: W, height: h, deviceScaleFactor: DPR, mobile: false });
  await size();
  page._filmSize = size;
  await page.waitForTimeout(cfg.boot_ms || 5000);
  return { page, close, electron: app };
}

// Kill only processes whose command line contains this run's temp folder (e.g. a backend the app spawned from our profile copy).
// Never pkill/killall by app name: that would hit the user's own running copy of the app.
// Their children go too (an R or Python worker started by that backend does not carry the folder in its command line).
function procTable() {
  try { return execFileSync('ps', ['-A', '-o', 'pid=,ppid=,command=']).toString().split('\n').map((l) => l.trim().match(/^(\d+)\s+(\d+)\s+(.*)$/)).filter(Boolean).map((m) => [+m[1], +m[2], m[3]]); } catch { return []; }
}
function treeOf(roots, table = procTable()) {   // roots + every descendant, plus anything running from our temp folder
  const set = new Set([...roots.filter(Boolean), ...table.filter(([, , cmd]) => cmd.includes(WORK)).map(([pid]) => pid)]);
  for (let grew = true; grew;) { grew = false; for (const [pid, ppid] of table) if (set.has(ppid) && !set.has(pid)) { set.add(pid); grew = true; } }
  set.delete(process.pid); return set;
}
function reapOurs(known = new Set()) {
  if (process.platform === 'win32') return;
  for (const pid of new Set([...known, ...treeOf([])])) { try { process.kill(pid, 'SIGKILL'); } catch {} }
}

// ---------- steps ----------
const byText = (page, text, { exact = true, nth = 0 } = {}) => page.getByText(text, { exact }).nth(nth);
async function clickables(page) {
  return page.evaluate(() => {
    const vis = (e) => { const r = e.getBoundingClientRect(); return r.width > 2 && r.height > 2 && r.bottom > 0 && r.top < innerHeight && getComputedStyle(e).visibility !== 'hidden'; };
    const lab = (e) => (e.innerText || e.getAttribute('aria-label') || e.title || '').trim().split('\n')[0].trim().slice(0, 40);   // first line = the text to click
    const sel = 'button,[role=button],a,[role=tab],[role=menuitem],[role=option],summary,label,[onclick],li[class*=item],div[class*=item]';
    const all = [...document.querySelectorAll(sel)].filter(vis);
    const clicks = all.filter((e) => !all.some((o) => o !== e && e.contains(o) && lab(o)))   // innermost only
      .map((e) => ({ text: lab(e), disabled: !!e.disabled, xy: (({ x, y }) => [Math.round(x), Math.round(y)])(e.getBoundingClientRect()) })).filter((c) => c.text);
    const seen = new Set(); const uniq = clicks.filter((c) => !seen.has(c.text) && seen.add(c.text));
    const inputs = [...document.querySelectorAll('input,textarea,select')].map((e, i) => ({ i, type: e.type, placeholder: e.placeholder || '', accept: e.accept || '', label: e.labels?.[0]?.innerText?.trim() || '' }));
    const headings = [...document.querySelectorAll('h1,h2,h3,[class*=title]')].filter(vis).map(lab).filter(Boolean).slice(0, 30);
    return { clickables: uniq.slice(0, 150), inputs, headings };
  });
}

async function stubDialogs(electron, { open, save }) {
  if (!electron) return;
  await electron.evaluate(({ dialog, session }, { open, save }) => {
    if (open) { dialog.showOpenDialog = async () => ({ canceled: false, filePaths: [open] }); dialog.showOpenDialogSync = () => [open]; }
    if (save) {
      dialog.showSaveDialog = async () => ({ canceled: false, filePath: save }); dialog.showSaveDialogSync = () => save;
      session.defaultSession.removeAllListeners('will-download');
      session.defaultSession.on('will-download', (_e, item) => item.setSavePath(save));
    }
  }, { open, save });
}

async function run(ctx, s) {
  const { page, electron } = ctx;
  if (s.use) {   // a named list of steps from "macros" (e.g. open the demo data and parse it)
    const m = (cfg.macros || {})[s.use]; if (!m) throw new Error(`no macro "${s.use}" in "macros"`);
    for (const x of m) await run(ctx, x);
    return;
  }
  const wait = s.wait ?? 800;
  if (s.click !== undefined) { await byText(page, s.click, s).click({ timeout: s.timeout || 15000, force: !!s.force }); await page.waitForTimeout(wait); }
  else if (s.css) { await page.locator(s.css).nth(s.nth || 0).click({ timeout: s.timeout || 15000 }); await page.waitForTimeout(wait); }
  else if (s.upload) {
    const file = rel(s.upload); if (!fs.existsSync(file)) throw new Error(`file ${file} not found`);
    const ext = path.extname(file).toLowerCase();
    let idx = s.input;
    if (idx === undefined) idx = await page.evaluate((ext) => { const xs = [...document.querySelectorAll('input[type=file]')]; const k = xs.findIndex((e) => !e.accept || e.accept.toLowerCase().split(',').some((a) => a.trim() === ext || a.trim() === '*/*')); return k < 0 ? 0 : k; }, ext);
    await page.locator('input[type=file]').nth(idx).setInputFiles(file); await page.waitForTimeout(s.wait ?? 1500);
  }
  else if (s.open_dialog) { await stubDialogs(electron, { open: rel(s.open_dialog) }); }
  else if (s.fill !== undefined) {
    const into = s.into ? page.getByPlaceholder(s.into).or(page.getByLabel(s.into)).first() : page.locator('textarea, input[type=text], input:not([type])').last();
    await into.fill(s.fill); await page.waitForTimeout(s.wait ?? 300);
  }
  else if (s.type !== undefined) {   // types key by key, so a typing moment can be filmed with seq
    if (s.into) await page.getByPlaceholder(s.into).or(page.getByLabel(s.into)).first().click();
    await page.keyboard.type(s.type, { delay: s.delay ?? 35 }); await page.waitForTimeout(s.wait ?? 300);
  }
  else if (s.click_xy) { await page.mouse.click(s.click_xy[0], s.click_xy[1]); await page.waitForTimeout(wait); }
  else if (s.select !== undefined) { await page.locator(s.in || 'select').nth(s.nth || 0).selectOption(typeof s.select === 'number' ? { index: s.select } : s.select); await page.waitForTimeout(wait); }
  else if (s.wheel) { for (let i = 0; i < (s.times || 5); i++) { await page.mouse.wheel(s.wheel[0], s.wheel[1]); await page.waitForTimeout(100); } await page.waitForTimeout(wait); }
  else if (s.key) { await page.keyboard.press(s.key); await page.waitForTimeout(wait); }
  else if (s.hover) { await byText(page, s.hover, s).hover(); await page.waitForTimeout(wait); }
  else if (s.wait_for) { await page.getByText(s.wait_for, { exact: s.exact ?? false }).first().waitFor({ state: 'visible', timeout: s.timeout || 60000 }); await page.waitForTimeout(s.settle ?? 1200); }
  else if (s.sleep) { await page.waitForTimeout(s.sleep); }
  else if (s.scroll) {
    await page.evaluate(([label, by]) => {
      const leaf = [...document.querySelectorAll('*')].find((e) => e.childElementCount === 0 && e.textContent.trim().includes(label));
      let el = leaf; while (el && !(el.scrollHeight > el.clientHeight + 20 && /auto|scroll/.test(getComputedStyle(el).overflowY))) el = el.parentElement;
      (el || document.scrollingElement).scrollBy(0, by);
    }, [s.scroll, s.by || 600]); await page.waitForTimeout(wait);
  }
  else if (s.shot) {
    // "clip": [x, y, w, h] (CSS px) or "@text": the smallest card or panel around that text, with a margin — a crop
    // that follows an element never cuts through a table or a paragraph the way a guessed rectangle does
    let clip = s.clip;
    if (typeof clip === 'string') {
      clip = await page.evaluate(([want, pad]) => {
        const t = want.replace(/^@/, '').trim().toLowerCase();
        const leaf = [...document.querySelectorAll('body *')].find((e) => e.childElementCount === 0 && (e.textContent || '').trim().toLowerCase().includes(t) && e.getBoundingClientRect().width > 0);
        if (!leaf) return null;
        let el = leaf, best = null;
        while (el && el !== document.body) {
          const r = el.getBoundingClientRect(), cs = getComputedStyle(el), a = (r.width * r.height) / (innerWidth * innerHeight);
          const boxy = (parseFloat(cs.borderTopWidth) > 0 && cs.borderTopStyle !== 'none') || !/rgba\(0, 0, 0, 0\)|transparent/.test(cs.backgroundColor) || cs.boxShadow !== 'none';
          if (boxy && a > 0.02) { best = r; break; }
          el = el.parentElement;
        }
        if (!best) return null;
        const x = Math.max(0, best.x - pad), y = Math.max(0, best.y - pad);
        return [x, y, Math.min(innerWidth - x, best.width + 2 * pad), Math.min(innerHeight - y, best.height + 2 * pad)].map(Math.round);
      }, [clip, s.pad ?? 16]).catch(() => null);
      if (!clip) throw new Error(`clip "${s.clip}": no card or panel holds that text on screen`);
    }
    await page.screenshot({ path: path.join(OUT, `${s.shot}.png`), ...(clip ? { clip: { x: clip[0], y: clip[1], width: clip[2], height: clip[3] } } : {}) });
    // the exact boxes of what is on screen (panels, cards, headings, buttons, with their text), read from the page itself:
    // a highlight can then name its target ("rect": "@APA 三线表") instead of guessing pixel coordinates by eye.
    // A clipped shot gets them too, in the clip's own coordinates.
    const regions = await page.evaluate(() => {
      const vw = innerWidth, vh = innerHeight, out = [];
      for (const e of document.querySelectorAll('body *')) {
        const r = e.getBoundingClientRect();
        if (r.width < 24 || r.height < 14 || r.right <= 0 || r.bottom <= 0 || r.left >= vw || r.top >= vh) continue;
        const area = (r.width * r.height) / (vw * vh); if (area > 0.6) continue;
        const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || +cs.opacity === 0 || cs.display === 'none') continue;
        const own = [...e.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent.trim()).join(' ').trim();
        const boxy = (parseFloat(cs.borderTopWidth) > 0 && cs.borderTopStyle !== 'none') || !/rgba\(0, 0, 0, 0\)|transparent/.test(cs.backgroundColor) || cs.boxShadow !== 'none';
        const kind = /^H[1-6]$/.test(e.tagName) ? 'heading' : e.tagName === 'BUTTON' || e.getAttribute('role') === 'button' ? 'button'
          : ['TABLE', 'CANVAS', 'SVG', 'svg', 'IMG'].includes(e.tagName) && area > 0.004 ? 'panel' : boxy && area > 0.004 ? 'panel' : own ? 'text' : '';
        if (!kind) continue;
        const text = (own || (e.innerText || '').trim().split('\n')[0] || '').replace(/\s+/g, ' ').slice(0, 48);
        const x = Math.max(0, r.x), y = Math.max(0, r.y);
        out.push({ kind, text, rect: [x, y, Math.min(vw, r.right) - x, Math.min(vh, r.bottom) - y].map(Math.round) });
      }
      return out.slice(0, 1500);
    }).catch(() => []);
    let reg = regions, base = [W, H];
    if (clip) {
      const [cx, cy, cw, ch] = clip; base = [Math.round(cw), Math.round(ch)];
      reg = regions.map((r) => { const [x, y, w, h] = r.rect, x0 = Math.max(x, cx), y0 = Math.max(y, cy), x1 = Math.min(x + w, cx + cw), y1 = Math.min(y + h, cy + ch);
        return x1 - x0 >= 12 && y1 - y0 >= 10 ? { ...r, rect: [x0 - cx, y0 - cy, x1 - x0, y1 - y0].map(Math.round) } : null; }).filter(Boolean);
    }
    fs.writeFileSync(path.join(OUT, `${s.shot}.regions.json`), JSON.stringify({ base, regions: reg }));
    // a film never shows a failure: flag visible error / not-configured / empty-state messages in the shot
    const bad = await page.evaluate(() => {
      // precise phrases only: statistics UIs say 异常值 (outlier), "Std. Error" and "未设置…时" in ordinary help text
      const re = /失败|出错|发生错误|出现错误|错误[：:]|未配置|尚未填写完整|暂无数据|请求超时|\berror:|failed to|request failed|not configured|exception:|something went wrong/i;
      return [...document.querySelectorAll('body *')].filter((e) => e.childElementCount === 0 && e.offsetParent && re.test(e.textContent || '') && (e.textContent || '').trim().length < 160)
        .map((e) => e.textContent.trim().replace(/\s+/g, ' ')).slice(0, 3);
    }).catch(() => []);
    if (bad.length) { flagged.push(s.shot); console.log(`  shot ${s.shot}  ⚠ shows: "${bad.join('" | "')}"\n    FIX: a film never shows an error or an unconfigured feature — fix the cause (wait longer, set up mock_llm, pick other inputs) and reshoot, or drop the shot`); }
    else console.log('  shot', s.shot);
  }
  else if (s.tall) {
    const sh = await page.evaluate((label) => {
      const leaf = [...document.querySelectorAll('*')].find((e) => e.childElementCount === 0 && e.textContent.trim().includes(label));
      let el = leaf; while (el && !(el.scrollHeight > el.clientHeight + 20 && /auto|scroll/.test(getComputedStyle(el).overflowY))) el = el.parentElement;
      if (!el) return 0; el.setAttribute('data-film', 'tall'); el.scrollTop = 0; el.style.height = el.scrollHeight + 'px'; el.style.maxHeight = 'none'; el.style.overflow = 'visible'; return el.scrollHeight;
    }, s.tall);
    if (!sh) throw new Error(`no scrolling panel around the text "${s.tall}"`);
    const h = Math.min(16000, sh + 600);
    if (page._filmSize) await page._filmSize(h); else await page.setViewportSize({ width: W, height: h });
    await page.waitForTimeout(800);
    await page.locator('[data-film=tall]').screenshot({ path: path.join(OUT, `${s.name || 'tall'}.png`) });
    if (page._filmSize) await page._filmSize(); else await page.setViewportSize({ width: W, height: H });
    console.log('  tall', s.name || 'tall', sh, 'px');
  }
  else if (s.download) {
    const target = path.join(OUT, s.file || 'download.bin'); fs.rmSync(target, { force: true });
    await stubDialogs(electron, { save: target });
    const dl = page.waitForEvent('download', { timeout: s.timeout || 90000 }).catch(() => null);
    await byText(page, s.download, s).click({ timeout: 15000 });
    const t0 = Date.now();
    while (!fs.existsSync(target) && Date.now() - t0 < (s.timeout || 90000)) {
      const d = await Promise.race([dl, new Promise((r) => setTimeout(() => r('tick'), 500))]);
      if (d && d !== 'tick') { await d.saveAs(target); break; }
    }
    if (!fs.existsSync(target)) throw new Error(`no file was saved after clicking "${s.download}"`);
    console.log('  saved', path.basename(target));
    if (/\.(docx?|pdf|pptx?|xlsx?)$/i.test(target) && process.platform === 'darwin') {   // page 1 as an image for the film
      try { execFileSync('qlmanage', ['-t', '-s', '1600', '-o', OUT, target], { stdio: 'ignore' }); console.log('  preview', path.basename(target) + '.png'); } catch {}
    }
  }
  else if (s.seq) {
    const dir = path.join(OUT, s.seq); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const t0 = Date.now(); let k = 0;
    while (Date.now() - t0 < (s.ms || 3000)) { await page.screenshot({ path: path.join(dir, `${String(k++).padStart(4, '0')}_${String(Date.now() - t0).padStart(6, '0')}.png`) }); await page.waitForTimeout(s.every || 80); }
    console.log('  seq', s.seq, k, 'frames');
  }
  else throw new Error(`unknown step ${JSON.stringify(s)}`);
}

// ---------- main ----------
let EXE = null, mock = null;
const flagged = [];
if (cfg.app) { EXE = executableOf(cfg.app); await prepareProfile(EXE); }
if (cfg.mock_llm) {
  const m = cfg.mock_llm;
  mock = spawn(process.execPath, [path.join(HERE, 'mock_llm.mjs'), String(m.port || 11434), rel(m.replies || 'replies.json')], { cwd: OUT, stdio: 'ignore', env: { ...process.env, DELAY: String(m.delay || 45) } });
  await new Promise((r) => setTimeout(r, 800));
  console.log(`mock model on :${m.port || 11434} (scripted replies — tell the user the AI text in the film was scripted)`);
}
const only = (opt('only', '') || '').split(',').filter(Boolean);
const scenarios = (cfg.scenarios || []).filter((s) => !only.length || only.includes(s.name));
let failed = 0, n = 0;
// Each scenario gets a fresh launch. "reuse": true keeps one launch and reloads the window between scenarios instead
// (faster when a slow engine starts once) — only for apps that come back clean on a reload; a failure still relaunches.
let live = null;
for (const sc of scenarios) {
  console.log(`== ${sc.name}`);
  let ctx; let k = -1;
  try {
    if (live && cfg.reuse && !sc.relaunch) {
      ctx = live; live = null;
      await ctx.page.reload(); await ctx.page.waitForTimeout(cfg.reload_ms || 2500);
    } else { await live?.close(); live = null; ctx = await launch(n++); }
    const limit = (sc.timeout_s || cfg.scenario_timeout_s || 420) * 1000, t0 = Date.now();
    for (k = 0; k < sc.steps.length; k++) {
      if (Date.now() - t0 > limit) throw new Error(`scenario took longer than ${limit / 1000} s (raise "timeout_s" only if the app is genuinely slow)`);
      await run(ctx, sc.steps[k]);
    }
    if (mode === 'explore') {
      await ctx.page.screenshot({ path: path.join(OUT, 'explore.png') });
      const info = await clickables(ctx.page);
      fs.writeFileSync(path.join(OUT, 'explore.json'), JSON.stringify(info, null, 1));
      console.log(`  screen: ${path.join(OUT, 'explore.png')} (look at it)\n  headings: ${info.headings.join(' | ')}`);
      console.log(`  clickable: ${info.clickables.map((c) => c.text + (c.disabled ? ' (disabled)' : '')).join(' | ')}`);
      console.log(`  inputs: ${JSON.stringify(info.inputs)}`);
      const store = await ctx.page.evaluate(() => {   // where the app keeps its settings (e.g. which AI provider it calls); secrets masked
        const mask = (v) => v.replace(/("?(?:api[_-]?key|key|token|secret|password)"?\s*:\s*")([^"]+)"/gi, '$1***"');
        return Object.keys(localStorage).map((k) => [k, /ai|llm|model|provider|openai|ollama/i.test(k) ? mask(localStorage.getItem(k) || '').slice(0, 300) : '']);
      }).catch(() => []);
      if (store.length) console.log(`  localStorage: ${store.map(([k, v]) => (v ? `${k} = ${v}` : k)).join(' | ')}`);
    }
  } catch (e) {
    failed++;
    const msg = e.message.split('\n')[0];
    console.error(`  FAILED at step ${k + 1} ${JSON.stringify(sc.steps[k] || {})}: ${msg}`);
    if (ctx) {
      try {
        await ctx.page.screenshot({ path: path.join(OUT, `_fail-${sc.name}.png`) });
        const info = await clickables(ctx.page);
        console.error(`  on screen now (${path.join(OUT, `_fail-${sc.name}.png`)}): ${info.clickables.map((c) => c.text).slice(0, 60).join(' | ')}`);
      } catch {}
    }
    console.error('  FIX: look at the _fail image, use a text from the list above (exact spelling), add {"wait_for": …} before slow steps, then rerun with --only ' + sc.name);
    try { await ctx?.close(); } catch {}
    ctx = null;
  }
  if (ctx) live = ctx;
}
try { await live?.close(); } catch {}
mock?.kill();
reapOurs();
fs.rmSync(WORK, { recursive: true, force: true });
if (mode === 'shoot' && cfg.app && process.platform === 'darwin') {   // the product's name, version and icon, from the app bundle
  const plist = path.join(cfg.app, 'Contents', 'Info.plist');
  const read = (k) => { try { return execFileSync('/usr/libexec/PlistBuddy', ['-c', `Print :${k}`, plist]).toString().trim(); } catch { return ''; } };
  const name = read('CFBundleDisplayName') || read('CFBundleName') || path.basename(cfg.app, '.app');
  const info = path.join(OUT, 'app-info.md');
  if (!fs.existsSync(info)) fs.writeFileSync(info, `# ${name}\n\nCaptured from the installed app ${path.basename(cfg.app)}, version ${read('CFBundleShortVersionString') || '?'}, on demo data (not real user data).\n`);
  let icon = read('CFBundleIconFile'); if (icon && !icon.endsWith('.icns')) icon += '.icns';
  const src = icon && path.join(cfg.app, 'Contents', 'Resources', icon), logo = path.join(OUT, 'logo.png');
  if (src && fs.existsSync(src) && !fs.existsSync(logo)) { try { execFileSync('sips', ['-s', 'format', 'png', '-Z', '1024', src, '--out', logo], { stdio: 'ignore' }); console.log('  logo.png ← the app icon'); } catch {} }
}
const shots = fs.readdirSync(OUT).filter((f) => f.endsWith('.png') && !f.startsWith('_') && f !== 'explore.png' && f !== 'logo.png');
console.log(`\n${scenarios.length - failed}/${scenarios.length} scenarios ok · ${shots.length} images in ${OUT}`);
if (mode === 'shoot') {   // coverage: the film runs ~9 s per image, and the hero needs real outputs
  const outs = shots.filter((f) => /plot|chart|graph|curve|roc|km|forest|result|report|export|answer|output/i.test(f));
  const ai = shots.filter((f) => /(^|[-_])ai[-_]|assistant|chat|answer/i.test(f));
  console.log(`coverage: ${shots.length} shots (${outs.length} outputs, ${ai.length} AI) → a film of about ${Math.max(45, 20 + 9 * shots.length)} s`);
  if (shots.length < 12) console.log(`WARN only ${shots.length} shots: the film will be short and thin.\n  FIX: add scenarios — one per feature the product is known for (each analysis or tool with its enlarged result), the exports (report, code, files), and the AI feature. Aim for 12–25 shots.`);
  if (outs.length < 3) console.log('WARN fewer than 3 real outputs (results, plots, reports): the hero and the proof beats need them.\n  FIX: run more analyses or jobs to their result and shoot each output enlarged.');
  if (flagged.length) console.log(`WARN ${flagged.length} shot(s) show an error or empty state: ${flagged.join(', ')} — reshoot or delete them before autofilm.`);
  if (!ai.length) console.log('note: no AI shot. If the product has AI features, film them with "mock_llm" (references/capture.md → Filming AI features honestly).');
}
if (failed) process.exit(2);
