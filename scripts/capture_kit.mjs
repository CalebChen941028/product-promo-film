// Real-UI capture toolkit (Playwright). Copy next to your project's promo folder and edit SCENARIOS.
// Usage: node capture_kit.mjs <scenario> [more]     → PNGs in ./shots (1920×1080 CSS px at 2× = 3840×2160)
//
// Principles
// - Drive the product the way a user would (upload, click, assign, run). Never fake the UI.
// - One fresh browser context per scenario/analysis: modals that ignore Escape cannot leak into the next shot.
// - 2× DPR so crops can be zoomed 1.5–2× in the film and stay sharp.
// - Wait on visible text ("APA", "完成") rather than fixed sleeps where possible; add a settle wait for charts.
// - Sequences (seq) record frames with their timestamps; the film maps capture time → film time.
// - Element "tall" captures: unclip a scroll container and screenshot the element (sidebars, AI panels).
// - Downloads: Promise.all([waitForEvent('download'), click]) then saveAs — real Word/R/PDF exports.
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(here, 'shots');
const APP_URL = process.env.APP_URL || 'http://localhost:5173/';
fs.mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch();

// ---------- helpers ----------
export async function boot({ dpr = 2, locale = 'zh-CN', storage = {} } = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: dpr, locale, acceptDownloads: true });
  // Seed app settings before any script runs, e.g. point AI at a local model:
  // storage = { medstat_ai_config: JSON.stringify({ provider: 'ollama', base_url: 'http://localhost:11434/v1', model: 'qwen3.5:9b', api_key: '' }) }
  await ctx.addInitScript((kv) => { try { for (const [k, v] of Object.entries(kv)) localStorage.setItem(k, v); } catch {} }, storage);
  const page = await ctx.newPage();
  page.on('pageerror', (e) => console.error('pageerror', e.message));
  await page.goto(APP_URL);
  await page.waitForTimeout(1800);
  return page;
}
export const byText = (page, text, exact = true) => page.getByText(text, { exact }).first();
export async function click(page, text, { exact = true, wait = 600 } = {}) { await byText(page, text, exact).click({ timeout: 10000 }); await page.waitForTimeout(wait); }
export async function clickCss(page, css, wait = 600) { await page.locator(css).first().click({ timeout: 10000 }); await page.waitForTimeout(wait); }
export async function shot(page, name, clip) { await page.screenshot({ path: path.join(OUT, `${name}.png`), ...(clip ? { clip } : {}) }); console.log('shot', name); }
// Frame sequence with capture timestamps in the file names: NNNN_<ms>.png
export async function seq(page, name, ms, every = 60, clip) {
  const dir = path.join(OUT, name); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const t0 = Date.now(); let k = 0;
  while (Date.now() - t0 < ms) {
    const t = Date.now() - t0;
    await page.screenshot({ path: path.join(dir, `${String(k++).padStart(4, '0')}_${String(t).padStart(6, '0')}.png`), ...(clip ? { clip } : {}) });
    await page.waitForTimeout(every);
  }
  console.log('seq', name, k);
}
// Whole content of a scrolling container as one tall image. `labelText` = any text inside the container.
export async function tall(page, labelText, name) {
  const info = await page.evaluate((label) => {
    const leaf = [...document.querySelectorAll('*')].find((e) => e.childElementCount === 0 && e.textContent.trim() === label);
    let el = leaf; while (el && !(el.scrollHeight > el.clientHeight + 20 && /auto|scroll/.test(getComputedStyle(el).overflowY))) el = el.parentElement;
    if (!el) return null; el.setAttribute('data-film', 'tall'); return { sh: el.scrollHeight };
  }, labelText);
  if (!info) { console.error('no scroll container around', labelText); return; }
  const el = page.locator('[data-film=tall]');
  await el.evaluate((e) => { e.scrollTop = 0; e.style.height = e.scrollHeight + 'px'; e.style.maxHeight = 'none'; e.style.overflow = 'visible'; });
  await page.setViewportSize({ width: 1920, height: Math.min(16000, info.sh + 600) });
  await page.waitForTimeout(800);
  await el.screenshot({ path: path.join(OUT, `${name}.png`) });
  await page.setViewportSize({ width: 1920, height: 1080 });
}
export async function download(page, clickText, file) {
  const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 90000 }), byText(page, clickText).click()]);
  await dl.saveAs(path.join(OUT, file)); console.log('saved', file, '←', dl.suggestedFilename());
}
// Dump labels of visible buttons — use while exploring an unfamiliar UI.
export async function clickables(page) {
  return page.evaluate(() => [...new Set([...document.querySelectorAll('button,[role=button],a,[role=tab]')].filter((e) => e.offsetParent).map((e) => e.innerText.trim().replace(/\s+/g, ' ').slice(0, 40)).filter(Boolean))]);
}

// ---------- scenarios (edit for your product) ----------
const SCENARIOS = {
  async explore() { // first pass on an unfamiliar app: screenshot + list what can be clicked
    const page = await boot();
    await shot(page, 'explore_home');
    console.log(JSON.stringify(await clickables(page)));
    await page.context().close();
  },
  async home() {
    const page = await boot();
    await shot(page, 'home');
    // await page.setInputFiles('input[type=file]', path.join(here, 'data', 'demo.csv'));
    // await click(page, '开始解析', { wait: 4000 }); await shot(page, 'variables');
    await page.context().close();
  },
};

for (const name of process.argv.slice(2)) {
  console.log('== scenario', name);
  try { await SCENARIOS[name](); } catch (e) { console.error('scenario failed', name, e.message.split('\n').slice(0, 3).join(' | ')); }
}
await browser.close();
