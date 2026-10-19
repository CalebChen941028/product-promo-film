// Placeholder materials for the "service" blind test: a fictional lakeside cabin stay, drawn in SVG (not real photos).
// node make_service_materials.mjs  → service/materials/*.jpg|png   (needs playwright; PLAYWRIGHT_NODE_MODULES or a local install)
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const req = createRequire(path.join(process.env.PLAYWRIGHT_NODE_MODULES || path.join(HERE, '..', 'node_modules'), 'x.js'));
const { chromium } = req('playwright');
const OUT = path.join(HERE, 'service', 'materials');

const noise = (o = 0.16, f = 0.85, seed = 7) => `<filter id="n${seed}"><feTurbulence type="fractalNoise" baseFrequency="${f}" numOctaves="3" seed="${seed}"/><feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.47  0 0 0 0 0.42  0 0 0 ${o} 0"/></filter><rect width="100%" height="100%" filter="url(#n${seed})"/>`;
const ridge = (w, y, amp, seed, fill, op = 1) => {
  let d = `M0 ${y}`; const n = 24;
  for (let i = 0; i <= n; i++) { const x = (w / n) * i; const yy = y - amp * (0.5 + 0.5 * Math.sin(i * 1.7 + seed) * Math.cos(i * 0.6 + seed * 2)); d += ` L${x.toFixed(0)} ${yy.toFixed(0)}`; }
  return `<path d="${d} L${w} 3000 L0 3000 Z" fill="${fill}" opacity="${op}"/>`;
};
const pine = (x, base, h, fill) => {
  const w = h * 0.34; let d = '';
  for (let k = 0; k < 5; k++) { const t = base - h * (k / 5); const ww = w * (1 - k / 6); d += `M${x - ww / 2} ${t} L${x} ${t - h * 0.32} L${x + ww / 2} ${t} Z `; }
  return `<path d="${d}" fill="${fill}"/><rect x="${x - h * 0.015}" y="${base - h * 0.06}" width="${h * 0.03}" height="${h * 0.08}" fill="${fill}"/>`;
};
const forest = (w, base, h, fill, seed, step = 70) => { let s = ''; for (let x = -20, i = 0; x < w + 40; x += step, i++) s += pine(x + 20 * Math.sin(i * seed), base + 10 * Math.cos(i), h * (0.75 + 0.35 * Math.abs(Math.sin(i * 2.3 + seed))), fill); return s; };
const cabin = (x, y, s, glow = true) => `<g transform="translate(${x},${y}) scale(${s})">
  <path d="M0 160 L180 20 L360 160 Z" fill="#1c1f22"/><rect x="30" y="150" width="300" height="190" fill="#2a2724"/>
  ${[0, 1, 2, 3, 4, 5, 6].map(i => `<rect x="30" y="${160 + i * 26}" width="300" height="2" fill="#1d1a18"/>`).join('')}
  <rect x="80" y="200" width="90" height="80" fill="${glow ? '#f2b45c' : '#3a3f44'}"/><rect x="123" y="200" width="4" height="80" fill="#2a2724"/>
  <rect x="220" y="210" width="70" height="130" fill="#1a1715"/></g>`;

const scenes = {
  'lake-dawn.jpg': { w: 2400, h: 1350, svg: `<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fa6b8"/><stop offset="0.45" stop-color="#e9c9a8"/><stop offset="0.62" stop-color="#f4dcc0"/></linearGradient>
    <linearGradient id="lk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9c2a8"/><stop offset="1" stop-color="#5c7282"/></linearGradient><filter id="b"><feGaussianBlur stdDeviation="22"/></filter><filter id="b2"><feGaussianBlur stdDeviation="3 0"/></filter></defs>
    <rect width="2400" height="820" fill="url(#sk)"/>${ridge(2400, 700, 260, 1, '#8c97a3', 0.75)}${ridge(2400, 780, 180, 3, '#5e6c78')}${forest(2400, 830, 120, '#2e3a40', 1.3, 46)}
    <rect y="820" width="2400" height="530" fill="url(#lk)"/><g transform="translate(0,1650) scale(1,-1)" opacity="0.35" filter="url(#b2)">${ridge(2400, 780, 180, 3, '#5e6c78')}${forest(2400, 830, 120, '#2e3a40', 1.3, 46)}</g>
    <rect y="760" width="2400" height="120" fill="#f6eadb" opacity="0.55" filter="url(#b)"/>
    ${[0, 1, 2, 3, 4, 5, 6, 7].map(i => `<rect x="${200 + i * 260}" y="${930 + i * 45}" width="${500 - i * 30}" height="3" fill="#f3e4cf" opacity="0.35"/>`).join('')}${noise(0.14, 0.9, 3)}` },
  'cabin-dusk.jpg': { w: 2400, h: 1600, svg: `<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d2a3a"/><stop offset="0.6" stop-color="#47566a"/><stop offset="0.75" stop-color="#8a7a72"/></linearGradient>
    <radialGradient id="gl" cx="0.44" cy="0.6" r="0.12"><stop offset="0" stop-color="#ffcf8a" stop-opacity="0.5"/><stop offset="1" stop-color="#ffcf8a" stop-opacity="0"/></radialGradient><filter id="b2"><feGaussianBlur stdDeviation="4 0"/></filter></defs>
    <rect width="2400" height="1600" fill="url(#sk)"/>${ridge(2400, 900, 200, 5, '#2b3644')}${forest(2400, 1060, 300, '#141b20', 2.1, 90)}
    ${cabin(880, 720, 1.0)}<rect width="2400" height="1600" fill="url(#gl)"/>
    <rect y="1060" width="2400" height="540" fill="#26313d"/><g opacity="0.5" filter="url(#b2)"><rect x="960" y="1090" width="90" height="220" fill="#f2b45c" opacity="0.6"/></g>
    ${[0, 1, 2, 3, 4].map(i => `<rect x="${300 + i * 380}" y="${1180 + i * 70}" width="420" height="2" fill="#8fa0b3" opacity="0.3"/>`).join('')}${noise(0.18, 0.9, 5)}` },
  'window-view.jpg': { w: 2400, h: 1350, svg: `<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9c8d2"/><stop offset="0.7" stop-color="#e2e6e2"/></linearGradient>
    <linearGradient id="wd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6e4f36"/><stop offset="1" stop-color="#4a3424"/></linearGradient>
    <filter id="g"><feTurbulence type="turbulence" baseFrequency="0.004 0.08" numOctaves="3" seed="2"/><feColorMatrix values="0 0 0 0 0.25  0 0 0 0 0.16  0 0 0 0 0.1  0 0 0 0.35 0"/></filter></defs>
    <rect width="2400" height="1350" fill="url(#sk)"/>${ridge(2400, 760, 160, 2, '#7d8a94')}${forest(2400, 820, 140, '#3a4a44', 0.7, 55)}<rect y="820" width="2400" height="530" fill="#8396a3"/>
    <path d="M0 0 H2400 V1350 H0 Z M420 180 V1000 H1980 V180 Z" fill="url(#wd)" fill-rule="evenodd"/><path d="M0 0 H2400 V1350 H0 Z M420 180 V1000 H1980 V180 Z" filter="url(#g)" fill-rule="evenodd"/>
    <rect x="1185" y="180" width="30" height="820" fill="url(#wd)"/><rect x="340" y="1000" width="1720" height="70" fill="#5a3f2b"/>
    <rect x="560" y="930" width="300" height="70" fill="#d8cdb8"/><rect x="560" y="930" width="300" height="10" fill="#b8ab93"/><rect x="580" y="880" width="260" height="50" fill="#9b5a3a"/>${noise(0.16, 0.85, 9)}` },
  'sauna-wood-detail.jpg': { w: 2400, h: 1350, svg: `<defs><linearGradient id="w" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9a6a43"/><stop offset="0.5" stop-color="#c08d5e"/><stop offset="1" stop-color="#8d5f3b"/></linearGradient>
    <filter id="g"><feTurbulence type="turbulence" baseFrequency="0.002 0.045" numOctaves="4" seed="11"/><feColorMatrix values="0 0 0 0 0.3  0 0 0 0 0.18  0 0 0 0 0.08  0 0 0 0.55 0"/></filter></defs>
    <rect width="2400" height="1350" fill="url(#w)"/><rect width="2400" height="1350" filter="url(#g)"/>
    ${[0, 1, 2, 3, 4].map(i => `<rect y="${i * 290 + 270}" width="2400" height="8" fill="#4d3220" opacity="0.7"/>`).join('')}
    <ellipse cx="1650" cy="420" rx="60" ry="26" fill="#5c3a22" opacity="0.8"/>${noise(0.2, 1.1, 4)}` },
  'forest-trail.jpg': { w: 2400, h: 1600, svg: `<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfd8cf"/><stop offset="1" stop-color="#8fa08c"/></linearGradient><filter id="b"><feGaussianBlur stdDeviation="8"/></filter></defs>
    <rect width="2400" height="1600" fill="url(#sk)"/><g filter="url(#b)" opacity="0.6">${forest(2400, 900, 520, '#6d7f6c', 0.4, 120)}</g>${forest(2400, 1000, 700, '#3c4c3b', 1.9, 210)}
    <rect y="980" width="2400" height="620" fill="#5f6a4c"/><path d="M1080 980 L1320 980 L1900 1600 L500 1600 Z" fill="#a89a7a"/>
    ${[0, 1, 2, 3, 4, 5].map(i => `<rect x="${120 + i * 420}" y="0" width="${36 + i * 6}" height="1100" fill="#2e2a22" opacity="0.85"/>`).join('')}${noise(0.18, 0.9, 6)}` },
  'logo.png': { w: 600, h: 600, t: true, svg: `<circle cx="300" cy="300" r="270" fill="#2f3b36"/><path d="M180 400 L300 170 L420 400 Z" fill="none" stroke="#e9dfcf" stroke-width="18"/><rect x="292" y="300" width="16" height="100" fill="#e9dfcf"/>` },
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
