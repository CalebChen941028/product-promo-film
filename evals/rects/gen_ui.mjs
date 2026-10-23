// A product-agnostic benchmark for highlight boxes: random interfaces of many kinds, with the true box of every target.
// node evals/rects/gen_ui.mjs <out dir> [count] [seed]
//   → <out>/ui-NNN.png (2× screenshot), ui-NNN.regions.json (what capture_app.mjs records), ui-NNN.truth.json (targets)
// Variety on purpose: light / dark / low-contrast themes, borderless cards, dense tables, forms, charts, sidebars, dialogs,
// phone-width layouts, CJK and Latin text. Nothing here comes from any one product.
import { loadPlaywright } from '../../scripts/_pw.mjs';
const { chromium } = await loadPlaywright();
import fs from 'fs';
import path from 'path';

const [out = 'evals/runs/rects', N = '40', SEED = '7'] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
let s = +SEED;
const rnd = () => ((s = (s * 1664525 + 1013904223) % 4294967296) / 4294967296);
const pick = (a) => a[Math.floor(rnd() * a.length)];
const int = (a, b) => a + Math.floor(rnd() * (b - a + 1));
const WORDS = ['Revenue', 'Orders', 'Users', 'Sessions', 'Latency', 'Settings', 'Report', 'Analysis', 'Export', 'Inventory', 'Schedule', 'Messages',
  '数据', '分析', '报告', '用户', '订单', '库存', '设置', '导出', '统计', '任务', '项目', '消息', 'Ålesund', 'Nº 42'];
const ADJ = ['Active', 'Daily', 'Weekly', 'Regional', 'Pending', 'Shared', 'Archived', 'Monthly', 'Cohort', 'Patient', 'Field', 'Draft', 'Live', 'Global',
  '核心', '季度', '区域', '待办', '共享', '历史', '临床', '队列', '年度', '实时', '本地', '草稿'];
const NOUN = ['Revenue', 'Orders', 'Users', 'Sessions', 'Latency', 'Settings', 'Report', 'Analysis', 'Export', 'Inventory', 'Schedule', 'Messages', 'Variables', 'Samples', 'Invoices', 'Tickets', 'Devices', 'Visits',
  '数据', '分析', '报告', '用户', '订单', '库存', '设置', '导出', '统计', '任务', '项目', '消息', '变量', '样本', '随访', '设备'];
const title = () => `${pick(ADJ)} ${pick(NOUN)}`;   // a card's own name: like a real UI, mostly distinct on one screen
const phrase = (n) => Array.from({ length: n }, () => pick(WORDS)).join(' ');
const THEMES = [
  { bg: '#f5f7fa', card: '#ffffff', ink: '#1b2230', mute: '#6b7486', line: '#e3e7ee', acc: '#2563eb' },
  { bg: '#ffffff', card: '#ffffff', ink: '#111', mute: '#777', line: '#eeeeee', acc: '#16a34a' },       // borderless white on white
  { bg: '#0f141c', card: '#18202b', ink: '#e8edf5', mute: '#8a96a8', line: '#263142', acc: '#38bdf8' },  // dark
  { bg: '#1e1e1e', card: '#252526', ink: '#d4d4d4', mute: '#9a9a9a', line: '#333', acc: '#c586c0' },     // editor-like dark
  { bg: '#fbf7f0', card: '#fffdf8', ink: '#2b2118', mute: '#8c7b68', line: '#efe6d8', acc: '#c2410c' },  // warm, low contrast
  { bg: '#eef1f6', card: '#f7f9fc', ink: '#24324a', mute: '#7f8ba0', line: '#dde3ec', acc: '#7c3aed' },  // pastel, very low contrast
];

function block(T, kind, id) {
  const border = rnd() < 0.6 ? `1px solid ${T.line}` : 'none', shadow = rnd() < 0.5 ? '0 1px 3px rgba(0,0,0,.08)' : 'none', rad = pick([0, 6, 10, 14]);
  const box = `background:${T.card};border:${border};box-shadow:${shadow};border-radius:${rad}px;padding:${int(12, 24)}px`;
  const tgt = `data-target="${id}" data-kind="${kind}"`;
  if (kind === 'card') return `<div ${tgt} style="${box}"><div style="color:${T.mute};font-size:13px">${title()}</div><div style="font-size:${int(22, 34)}px;font-weight:700;margin:6px 0">${int(10, 9999).toLocaleString()}</div>${Array.from({ length: int(0, 3) }, () => `<div style="color:${T.mute};font-size:13px">${phrase(3)}</div>`).join('')}</div>`;
  if (kind === 'table') {
    const cols = int(3, 6), rows = int(3, 9);
    return `<div ${tgt} style="${box}"><div style="font-weight:600;margin-bottom:8px">${title()}</div><table style="border-collapse:collapse;width:100%;font-size:13px">${'<tr>' + Array.from({ length: cols }, () => `<th style="text-align:left;padding:6px;border-bottom:1px solid ${T.line};color:${T.mute}">${pick(WORDS)}</th>`).join('') + '</tr>'}${Array.from({ length: rows }, () => '<tr>' + Array.from({ length: cols }, () => `<td style="padding:6px;border-bottom:1px solid ${T.line}">${rnd() < 0.5 ? int(1, 999) : pick(WORDS)}</td>`).join('') + '</tr>').join('')}</table></div>`;
  }
  if (kind === 'chart') {
    const n = int(4, 10), h = int(120, 220);
    return `<div ${tgt} style="${box}"><div style="font-weight:600;margin-bottom:8px">${title()}</div><svg width="100%" height="${h}" viewBox="0 0 ${n * 30} ${h}" preserveAspectRatio="none">${Array.from({ length: n }, (_, i) => { const v = int(15, h - 10); return `<rect x="${i * 30 + 6}" y="${h - v}" width="18" height="${v}" fill="${T.acc}" opacity="${0.5 + rnd() / 2}"/>`; }).join('')}</svg></div>`;
  }
  if (kind === 'form') return `<div ${tgt} style="${box}">${Array.from({ length: int(2, 4) }, () => `<div style="color:${T.mute};font-size:13px;margin-top:8px">${phrase(1)}</div><div style="height:36px;border:1px solid ${T.line};border-radius:8px;margin-top:4px"></div>`).join('')}<div style="margin-top:14px;display:inline-block;padding:9px 18px;border-radius:8px;background:${T.acc};color:#fff">${pick(WORDS)}</div></div>`;
  if (kind === 'button') return `<div ${tgt} style="display:inline-block;padding:${int(8, 12)}px ${int(14, 24)}px;border-radius:${rad}px;background:${T.acc};color:#fff;font-weight:600">${title()}</div>`;
  if (kind === 'list') return `<div ${tgt} style="${box}">${Array.from({ length: int(3, 7) }, () => `<div style="display:flex;gap:10px;align-items:center;padding:8px 0;border-bottom:1px solid ${T.line}"><div style="width:26px;height:26px;border-radius:50%;background:${T.line}"></div><div>${phrase(2)}</div><div style="margin-left:auto;color:${T.mute}">${int(1, 99)}</div></div>`).join('')}</div>`;
  return `<div ${tgt} style="${box}"><div style="font-weight:600">${title()}</div><p style="color:${T.mute};font-size:14px;line-height:1.6">${phrase(int(12, 30))}</p></div>`;
}

function page(i) {
  const T = pick(THEMES), phone = rnd() < 0.2, W = phone ? 430 : 1920, H = phone ? 932 : 1080;
  let id = 0; const B = (k) => block(T, k, `t${id++}`);
  const kinds = ['card', 'table', 'chart', 'form', 'list', 'text'];
  let body;
  if (phone) body = `<div style="padding:16px;display:flex;flex-direction:column;gap:12px">${Array.from({ length: int(3, 5) }, () => B(pick(kinds))).join('')}</div>`;
  else {
    const side = rnd() < 0.6 ? `<div style="width:${int(200, 260)}px;background:${T.card};border-right:1px solid ${T.line};padding:16px;flex:none">${Array.from({ length: int(6, 12) }, () => `<div style="padding:8px;color:${T.mute}">${phrase(1)}</div>`).join('')}</div>` : '';
    const cols = int(2, 4);
    const grid = `<div style="display:grid;grid-template-columns:repeat(${cols},1fr);gap:${int(12, 24)}px;padding:${int(16, 28)}px;flex:1;align-content:start">${Array.from({ length: int(4, 8) }, () => { const k = pick(kinds); const span = k === 'table' || k === 'chart' ? Math.min(cols, int(1, 2)) : 1; return `<div style="grid-column:span ${span}">${B(k)}</div>`; }).join('')}<div>${B('button')}</div></div>`;
    body = `<div style="height:56px;background:${T.card};border-bottom:1px solid ${T.line};display:flex;align-items:center;padding:0 20px;font-weight:700">${phrase(2)}</div><div style="display:flex;height:calc(100% - 56px)">${side}${grid}</div>`;
  }
  return { W, H, html: `<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;height:100%;overflow:hidden;background:${T.bg};color:${T.ink};font-family:-apple-system,"PingFang SC",sans-serif}</style></head><body>${body}</body></html>` };
}

const REGIONS = () => {   // the same element boxes capture_app.mjs records (kept in step with it)
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
  return out;
};

const b = await chromium.launch();
for (let i = 0; i < +N; i++) {
  const { W, H, html } = page(i);
  const ctx = await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
  const p = await ctx.newPage(); await p.setContent(html);
  const name = path.join(out, `ui-${String(i).padStart(3, '0')}`);
  await p.screenshot({ path: name + '.png' });
  const truth = await p.evaluate(() => [...document.querySelectorAll('[data-target]')].map((e) => { const r = e.getBoundingClientRect();
    return { kind: e.dataset.kind, rect: [r.x, r.y, r.width, r.height].map(Math.round), text: (e.innerText || '').split('\n').map((t) => t.trim()).filter(Boolean).slice(0, 3) }; }).filter((t) => t.rect[2] > 20 && t.rect[3] > 14 && t.rect[1] + t.rect[3] <= innerHeight + 2));
  fs.writeFileSync(name + '.truth.json', JSON.stringify({ base: [W, H], targets: truth }));
  fs.writeFileSync(name + '.regions.json', JSON.stringify({ base: [W, H], regions: await p.evaluate(REGIONS) }));
  await ctx.close();
}
await b.close();
console.log(`${N} interfaces → ${out}`);
