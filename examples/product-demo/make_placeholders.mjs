// Placeholder materials for the product demo: a fictional stoneware mug brand, drawn in SVG (not real photos).
// node make_placeholders.mjs  → materials/*.png|jpg   (needs playwright; PLAYWRIGHT_NODE_MODULES or a local install)
import { chromium } from 'playwright';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const OUT = path.join(path.dirname(fileURLToPath(import.meta.url)), 'materials');
const glaze = { sage: ['#9db59a', '#5f7d62', '#e7efe3'], cream: ['#efe6d6', '#b9a888', '#fffaf0'], clay: ['#c9825f', '#8a4b33', '#f2c3a6'] };
const mug = (g, x = 0, y = 0, s = 1, id = 'm') => {
  const [mid, dark, hi] = glaze[g];
  return `<g transform="translate(${x},${y}) scale(${s})">
  <defs><linearGradient id="${id}b" x1="0" x2="1"><stop offset="0" stop-color="${dark}"/><stop offset="0.35" stop-color="${mid}"/><stop offset="0.55" stop-color="${hi}"/><stop offset="0.8" stop-color="${mid}"/><stop offset="1" stop-color="${dark}"/></linearGradient>
  <radialGradient id="${id}t" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#3b2418"/><stop offset="0.8" stop-color="#5a3826"/><stop offset="1" stop-color="${dark}"/></radialGradient>
  <filter id="${id}g"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 0.3  0 0 0 0 0.25  0 0 0 0 0.2  0 0 0 0.25 0"/><feComposite in2="SourceGraphic" operator="in"/></filter></defs>
  <path d="M520 360 C700 330 720 560 540 600" fill="none" stroke="url(#${id}b)" stroke-width="46" stroke-linecap="round"/>
  <path d="M120 240 L520 240 L500 760 Q490 820 430 820 L210 820 Q150 820 140 760 Z" fill="url(#${id}b)"/>
  <path d="M120 240 L520 240 L500 760 Q490 820 430 820 L210 820 Q150 820 140 760 Z" filter="url(#${id}g)"/>
  <path d="M140 700 L500 700 L494 760 Q488 812 430 812 L210 812 Q152 812 146 760 Z" fill="#6b5a4a" opacity="0.55"/>
  <ellipse cx="320" cy="240" rx="200" ry="34" fill="url(#${id}t)"/><ellipse cx="320" cy="240" rx="200" ry="34" fill="none" stroke="${hi}" stroke-width="6"/></g>`;
};
const noise = (o = 0.18, f = 0.8) => `<filter id="n"><feTurbulence type="fractalNoise" baseFrequency="${f}" numOctaves="3" seed="9"/><feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.42  0 0 0 0 0.35  0 0 0 ${o} 0"/></filter><rect width="100%" height="100%" filter="url(#n)"/>`;
const scenes = {
  'mug-sage.png': { w: 1200, h: 1000, t: true, svg: mug('sage', 260, 60, 1) },
  'mug-cream.png': { w: 1200, h: 1000, t: true, svg: mug('cream', 260, 60, 1) },
  'mug-clay.png': { w: 1200, h: 1000, t: true, svg: mug('clay', 260, 60, 1) },
  'morning-table.jpg': { w: 2400, h: 1600, svg: `<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9dcc6"/><stop offset="1" stop-color="#cdb593"/></linearGradient><linearGradient id="tb" x1="0" y1="0" x2="1" y2="0.2"><stop offset="0" stop-color="#8a5f3e"/><stop offset="0.5" stop-color="#a87a52"/><stop offset="1" stop-color="#7a5134"/></linearGradient><radialGradient id="sun" cx="0.78" cy="0.2" r="0.7"><stop offset="0" stop-color="#fff3d8" stop-opacity="0.9"/><stop offset="1" stop-color="#fff3d8" stop-opacity="0"/></radialGradient><filter id="bl"><feGaussianBlur stdDeviation="18"/></filter></defs>
    <rect width="2400" height="1000" fill="url(#w)"/><rect y="1000" width="2400" height="600" fill="url(#tb)"/><rect width="2400" height="1600" fill="url(#sun)"/>
    <g opacity="0.55" filter="url(#bl)"><path d="M1300 380 C1260 300 1360 260 1320 180 C1300 130 1350 90 1330 40" stroke="#fff" stroke-width="40" fill="none"/></g>
    <ellipse cx="1300" cy="1330" rx="380" ry="60" fill="#3d2a1c" opacity="0.45" filter="url(#bl)"/>${mug('sage', 980, 420, 1.05, 'a')}${noise(0.22, 0.9)}` },
  'glaze-detail.jpg': { w: 2400, h: 1350, svg: `<defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#5f7d62"/><stop offset="0.5" stop-color="#a9c0a5"/><stop offset="1" stop-color="#4c6a50"/></linearGradient><filter id="t"><feTurbulence type="turbulence" baseFrequency="0.006 0.03" numOctaves="4" seed="3"/><feColorMatrix values="0 0 0 0 0.9  0 0 0 0 0.95  0 0 0 0 0.88  0 0 0 0.35 0"/></filter></defs>
    <rect width="2400" height="1350" fill="url(#g)"/><rect width="2400" height="1350" filter="url(#t)"/>${noise(0.25, 1.2)}` },
  'shelf.jpg': { w: 2400, h: 1350, svg: `<defs><linearGradient id="wl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#efe7da"/><stop offset="1" stop-color="#ddd0bb"/></linearGradient></defs>
    <rect width="2400" height="1350" fill="url(#wl)"/><rect y="980" width="2400" height="70" fill="#9a7352"/><rect y="1050" width="2400" height="300" fill="#e4d8c4"/>
    ${mug('cream', 420, 250, 0.9, 'b')}${mug('sage', 960, 250, 0.9, 'c')}${mug('clay', 1500, 250, 0.9, 'd')}${noise(0.2, 0.85)}` },
  'logo.png': { w: 600, h: 600, t: true, svg: `<circle cx="300" cy="300" r="270" fill="#3f7d58"/><text x="300" y="352" text-anchor="middle" font-family="Georgia, serif" font-size="170" fill="#f8f4ec">A</text>` },
};
const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 1 });
for (const [name, s] of Object.entries(scenes)) {
  await page.setViewportSize({ width: s.w, height: s.h });
  await page.setContent(`<html><body style="margin:0;background:transparent"><svg xmlns="http://www.w3.org/2000/svg" width="${s.w}" height="${s.h}" viewBox="0 0 ${s.w} ${s.h}">${s.svg}</svg></body></html>`);
  await page.screenshot({ path: path.join(OUT, name), omitBackground: !!s.t, type: name.endsWith('.jpg') ? 'jpeg' : 'png', quality: name.endsWith('.jpg') ? 90 : undefined });
}
await browser.close();
console.log('placeholders →', OUT);
