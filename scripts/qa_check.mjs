// Automatic layout QA for a film page — so agents without strong vision still ship clean frames.
// Usage: node qa_check.mjs <film.html> <outDir>   → outDir/qa_report.json + contact sheets (stills + sheet*.png)
// Samples every scene at 40% / 75% / 95% of its length (cover and end card after their build-up) and checks:
//   E offstage        text, or more than 20% of a media frame, outside the 1920×1080 stage
//   E text-overlap    two visible text blocks overlap > 12% of the smaller one
//   E chapter-hit     the chapter label overlaps a window/picture/text
//   E caption-hit     the bottom caption overlaps a visible text block (> 10%)
//   W caption-media   the caption covers > 35% of a media frame's lower area (often fine; check the sheet)
//   W small-text      rendered text smaller than 14 px
//   E missing-media   an image/video failed to load
// Elements are found by data-qa="text|media" (set by engine/library); data-qa="ignore" subtrees are skipped.
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [html, out] = process.argv.slice(2);
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(pathToFileURL(path.resolve(html)).href);
const missing = await page.evaluate(() => window.ready);
const errors = [], warnings = [];
if (missing.length) errors.push(`missing-media: ${missing.join(', ')}`);
const scenes = await page.evaluate(() => SCENES.map((s, i) => ({ i, s: s.s, e: s.e })));
const times = [];
scenes.forEach(({ i, s, e }) => {
  const d = e - s, last = i === scenes.length - 1;
  const fr = i === 0 ? [0.75] : last ? [Math.min(0.9, 6 / d), 0.6] : [0.4, 0.75, 0.95];
  fr.forEach((f) => times.push({ scene: i, t: +(s + d * f - (f === 0.95 ? 0.3 : 0)).toFixed(2) }));
});
const area = (r) => Math.max(0, r.w) * Math.max(0, r.h);
const inter = (a, b) => area({ w: Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x), h: Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y) });
const shots = [];
for (const { scene, t } of times) {
  await page.evaluate((tt) => window.renderFrame(tt), t);
  const info = await page.evaluate(() => {
    const vis = (el) => { let o = 1, n = el; while (n && n !== document.body) { const cs = getComputedStyle(n); if (cs.display === 'none' || cs.visibility === 'hidden') return 0; o *= parseFloat(cs.opacity); n = n.parentElement; } return o; };
    const rect = (el) => { const r = el.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height }; };
    const label = (el) => (el.innerText || el.className || el.tagName).replace(/\s+/g, ' ').trim().slice(0, 40);
    const els = [...document.querySelectorAll('[data-qa="text"],[data-qa="media"]')].filter((el) => !el.closest('[data-qa="ignore"]'))
      .map((el) => { const r = rect(el), cs = getComputedStyle(el); const fs = parseFloat(getComputedStyle(el.querySelector('*') || el).fontSize) * (el.offsetHeight ? r.h / el.offsetHeight : 1);
        const bg = cs.backgroundColor.match(/[\d.]+/g); return { kind: el.dataset.qa, r, o: vis(el), label: label(el), fs, solid: bg && bg.length === 4 ? +bg[3] > 0.5 : !!(bg && bg.length === 3) }; })
      .filter((e) => e.o > 0.6 && e.r.w > 2 && e.r.h > 2);
    const ch = document.getElementById('chapter'), cz = document.getElementById('capzh'), ce = document.getElementById('capen');
    const capR = [cz, ce].filter((c) => vis(c) > 0.5 && c.textContent.trim()).map((c) => { const r = c.getBoundingClientRect(); const w = Math.min(r.width, (c.scrollWidth || r.width)); const tw = (() => { const rg = document.createRange(); rg.selectNodeContents(c); const b = rg.getBoundingClientRect(); return { x: b.x, y: b.y, w: b.width, h: b.height }; })(); return tw; });
    return { els, chapter: vis(ch) > 0.5 ? rect(ch) : null, captions: capR };
  });
  const tag = `scene ${scene} @ ${t}s`;
  const texts = info.els.filter((e) => e.kind === 'text'), medias = info.els.filter((e) => e.kind === 'media');
  for (const e of info.els) {
    const r = e.r, out = area(r) - inter(r, { x: 0, y: 0, w: 1920, h: 1080 });
    if (e.kind === 'text' && out > 0.02 * area(r)) errors.push(`offstage ${tag}: text "${e.label}" leaves the frame`);
    if (e.kind === 'media' && out > 0.2 * area(r) && e.o > 0.9) errors.push(`offstage ${tag}: media "${e.label}" is ${Math.round(100 * out / area(r))}% outside the frame`);
    if (e.kind === 'text' && e.fs && e.fs < 14) warnings.push(`small-text ${tag}: "${e.label}" ≈ ${e.fs.toFixed(0)} px`);
  }
  for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
    const a = texts[i], b = texts[j], ov = inter(a.r, b.r);
    if (ov > 0.12 * Math.min(area(a.r), area(b.r)) && !(a.r.x <= b.r.x && a.r.y <= b.r.y && a.r.x + a.r.w >= b.r.x + b.r.w && a.r.y + a.r.h >= b.r.y + b.r.h)) errors.push(`text-overlap ${tag}: "${a.label}" × "${b.label}"`);
  }
  if (info.chapter) for (const e of info.els) if (inter(info.chapter, e.r) > 0.15 * area(info.chapter)) errors.push(`chapter-hit ${tag}: chapter label overlaps "${e.label}"`);
  for (const c of info.captions) {
    for (const e of texts) if (inter(c, e.r) > 0.1 * Math.min(area(c), area(e.r)) && !e.solid) errors.push(`caption-hit ${tag}: caption overlaps text "${e.label}"`);
    for (const e of medias) if (inter(c, e.r) > 0.35 * area(c)) warnings.push(`caption-media ${tag}: caption sits on "${e.label}" — fine if nothing important is under it`);
  }
  const file = path.join(out, `t${t.toFixed(2).padStart(6, '0')}.png`);
  writeFileSync(file, await page.screenshot({ type: 'png' }));
  shots.push(file);
}
// contact sheets: 3×3 per image, drawn in the page itself (no Python needed)
for (let k = 0; k < shots.length; k += 9) {
  const group = shots.slice(k, k + 9).map((f) => path.basename(f));
  const sheetHtml = path.join(out, `_sheet${k / 9}.html`);   // a real file next to the stills, so file:// images load
  writeFileSync(sheetHtml, `<!doctype html><body style="margin:0;background:#000;display:grid;grid-template-columns:repeat(3,640px)">${group.map((f) => `<div style="position:relative"><img src="${f}" style="width:640px;height:360px;display:block"><span style="position:absolute;left:6px;top:4px;color:#ff0;font:14px monospace">${f}</span></div>`).join('')}</body>`);
  const sheet = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await sheet.goto(pathToFileURL(sheetHtml).href);
  await sheet.evaluate(() => Promise.all([...document.images].map((i) => i.complete ? 0 : new Promise((r) => { i.onload = i.onerror = r; }))));
  await sheet.screenshot({ path: path.join(out, `sheet${k / 9}.png`) });
  await sheet.close();
}
const uniq = (a) => [...new Set(a)];
writeFileSync(path.join(out, 'qa_report.json'), JSON.stringify({ errors: uniq(errors), warnings: uniq(warnings), frames: shots.map((f) => path.basename(f)) }, null, 1));
console.log(`qa: ${uniq(errors).length} errors, ${uniq(warnings).length} warnings, ${shots.length} frames`);
await browser.close();
