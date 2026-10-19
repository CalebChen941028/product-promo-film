'use strict';
// MedStat Pilot film v2 — deterministic DOM compositor. window.renderFrame(t) sets every style from t alone.
const SH = '../capture/shots/', AS = 'assets/';
const DUR = 206;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, t) => a + (b - a) * t;
const prog = (t, a, b) => clamp((t - a) / (b - a));
const eo = (t) => 1 - Math.pow(1 - t, 3);
const eio = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const ex = (t) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t));
const eback = (t) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
const fade = (t, a, b, f = 0.4) => Math.min(prog(t, a, a + f), 1 - prog(t, b - f, b));
const B = (b) => bar(b);

function div(cls, parent, html) { const d = document.createElement('div'); if (cls) d.className = cls; if (html != null) d.innerHTML = html; if (parent) parent.appendChild(d); return d; }
const IMGS = [];
function img(src, parent, cls) { const i = new Image(); i.src = src; if (cls) i.className = cls; if (parent) parent.appendChild(i); IMGS.push(i); return i; }
function place(el, { x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0, s = 1, o = 1 } = {}) {
  el.style.transform = `translate(-50%,-50%) translate3d(${x}px,${y}px,${z}px) rotateX(${rx}deg) rotateY(${ry}deg) rotateZ(${rz}deg) scale(${s})`;
  el.style.opacity = o;
}
// keyframes: [[t, {props}, ease?], ...]; every key should list the same props
function kf(t, keys) {
  if (t <= keys[0][0]) return { ...keys[0][1] };
  for (let i = 0; i < keys.length - 1; i++) {
    const [t0, a] = keys[i], [t1, b, e] = keys[i + 1];
    if (t <= t1) { const k = (e || eio)(prog(t, t0, t1)); const r = { ...a }; for (const p in b) r[p] = lerp(a[p] ?? 0, b[p], k); return r; }
  }
  return { ...keys[keys.length - 1][1] };
}
const lerpRect = (a, b, k) => a.map((v, i) => lerp(v, b[i], k));
function kfRect(t, keys) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) { const [t0, a] = keys[i], [t1, b] = keys[i + 1]; if (t <= t1) return lerpRect(a, b, eio(prog(t, t0, t1))); }
  return keys[keys.length - 1][1];
}

// ---------- UI window built from a 1920×1080 capture (crop in CSS px of the capture) ----------
function win(parent, { srcs, crop, w, chrome = true, title = 'MedStat Pilot', radius }) {
  const root = div('abs win', parent);
  if (radius != null) root.style.borderRadius = radius + 'px';
  if (chrome) div('win-bar', root, `<i></i><i></i><i></i><span>${title}</span>`);
  const body = div('win-body', root);
  const W = { root, body, layers: [], chrome };
  for (const s of [].concat(srcs)) { const i = img(s, body, 'shot'); W.layers.push(i); }
  W.ov = div('ov', body);
  setCrop(W, crop, w); showLayer(W, 0);
  return W;
}
function setCrop(W, crop, w = W.w) {
  const [x, y, cw, ch] = crop, s = w / cw;
  W.crop = crop; W.w = w; W.s = s; W.h = ch * s;
  W.root.style.width = w + 'px'; W.body.style.width = w + 'px'; W.body.style.height = W.h + 'px';
  for (const l of W.layers) { l.style.width = 1920 * s + 'px'; l.style.height = 1080 * s + 'px'; l.style.transform = `translate(${-x * s}px,${-y * s}px)`; }
}
function showLayer(W, idx, mix) { // mix: optional cross-fade amount toward idx+1
  W.layers.forEach((l, i) => {
    if (i === idx) { l.style.display = 'block'; l.style.opacity = 1; }
    else if (mix != null && i === idx + 1 && mix > 0) { l.style.display = 'block'; l.style.opacity = mix; }
    else l.style.display = 'none';
  });
}
const mapX = (W, x) => (x - W.crop[0]) * W.s, mapY = (W, y) => (y - W.crop[1]) * W.s;
function hl(W, rect) { return { d: div('hl', W.ov), rect }; }
function posHL(W, H, a, pad = 6) {
  const [x, y, w, h] = H.rect;
  Object.assign(H.d.style, { left: mapX(W, x) - pad + 'px', top: mapY(W, y) - pad + 'px', width: w * W.s + 2 * pad + 'px', height: h * W.s + 2 * pad + 'px', opacity: clamp(a), transform: `scale(${lerp(1.06, 1, eo(clamp(a)))})` });
}
function tag(W, zh, en) { return div('tag', W.ov, `${zh}<em>${en}</em>`); }
function posTag(W, T, x, y, a) {
  T.style.left = mapX(W, x) + 'px'; T.style.top = mapY(W, y) + 'px'; T.style.opacity = clamp(a);
  T.style.transform = `translate(-50%,-50%) translateY(${(1 - eo(clamp(a))) * 16}px)`;
}
const CURSOR_SVG = '<svg viewBox="0 0 24 24" width="34" height="34"><path d="M4 2 L4 19 L8.6 14.9 L11.6 22 L14.6 20.7 L11.7 13.9 L18 13.9 Z" fill="#fff" stroke="#111" stroke-width="1.3" stroke-linejoin="round"/></svg>';
function cursor(W) { return { c: div('cursor', W.ov, CURSOR_SVG), r: div('ripple', W.ov) }; }
// path: [[t, x, y], ...] in capture coords; clicks: [t, ...]
function posCursor(W, C, lt, path, clicks = [], vis = 1) {
  let x = path[0][1], y = path[0][2];
  for (let i = 0; i < path.length - 1; i++) {
    const [t0, x0, y0] = path[i], [t1, x1, y1] = path[i + 1];
    if (lt >= t0) { const k = eio(prog(lt, t0, t1)); x = lerp(x0, x1, k); y = lerp(y0, y1, k); }
  }
  const X = mapX(W, x), Y = mapY(W, y);
  let press = 0, rip = -1;
  for (const c of clicks) { const d = lt - c; if (d >= -0.08 && d < 0.12) press = 1; if (d >= 0 && d < 0.55) rip = d; }
  C.c.style.left = X - 6 + 'px'; C.c.style.top = Y - 4 + 'px'; C.c.style.opacity = vis; C.c.style.transform = `scale(${press ? 0.86 : 1})`;
  if (rip >= 0) { C.r.style.left = X + 'px'; C.r.style.top = Y + 'px'; C.r.style.opacity = 1 - rip / 0.55; C.r.style.transform = `scale(${0.3 + rip * 2.2})`; } else C.r.style.opacity = 0;
}
// plain picture card (non-capture images)
function pic(parent, src, w, h, cls = 'abs') {
  const root = div(cls, parent); root.style.width = w + 'px'; root.style.height = h + 'px';
  root.style.borderRadius = '14px'; root.style.overflow = 'hidden'; root.style.background = '#fff';
  root.style.boxShadow = '0 40px 100px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.08)';
  const i = img(src, root); Object.assign(i.style, { width: '100%', height: '100%', objectFit: 'contain', display: 'block' });
  return root;
}
function textEl(parent, html, css = {}) { const d = div('abs', parent, html); Object.assign(d.style, css); return d; }

// ---------- scenes ----------
const SCENES = [];
function scene(s, e, init, update, opts = {}) { SCENES.push({ s, e, init, update, ...opts }); }
const plotCrop = [400, 130, 1120, 860];

// 0. Cover
scene(0, B(3), (R, S) => {
  S.back = div('abs', R); Object.assign(S.back.style, { width: '1920px', height: '1080px', filter: 'blur(3px) saturate(0.8)' });
  S.bw = [
    win(S.back, { srcs: SH + 'variables.png', crop: [0, 0, 1920, 1080], w: 860 }),
    win(S.back, { srcs: SH + 'km_plot.png', crop: plotCrop, w: 640, chrome: false }),
    win(S.back, { srcs: SH + 'tt_result.png', crop: [0, 0, 1920, 1080], w: 860 }),
  ];
  S.icon = img(AS + 'icon.png', R, 'abs'); S.icon.style.width = '300px';
  S.title = textEl(R, 'MedStat <span style="color:var(--teal)">Pilot</span>', { font: '700 132px var(--en)', letterSpacing: '1px', whiteSpace: 'nowrap', textShadow: '0 10px 50px rgba(0,0,0,0.6)' });
  S.sub = textEl(R, '医学科研统计工作台', { font: '500 40px var(--zh)', letterSpacing: '14px', whiteSpace: 'nowrap' });
  S.kick = textEl(R, 'RESEARCH STATISTICS WORKBENCH', { font: '700 19px var(--en)', letterSpacing: '9px', color: 'var(--teal)', whiteSpace: 'nowrap' });
  S.line = textEl(R, '从数据，到发现 &nbsp;·&nbsp; <span style="font-family:var(--en)">From data to discovery</span>', { font: '400 26px var(--zh)', color: 'var(--dim)', letterSpacing: '3px', whiteSpace: 'nowrap' });
  S.chips = textEl(R, '<span class="chip">macOS · Apple silicon</span>&nbsp;&nbsp;<span class="chip">Windows · x64</span>&nbsp;&nbsp;<span class="chip" style="border-color:var(--amber);color:var(--amber)">Beta</span>', { whiteSpace: 'nowrap' });
}, (S, lt, d) => {
  const push = eio(prog(lt, d - 0.9, d + 0.3));
  place(S.back, { s: 1 + lt * 0.012, o: 0.28 * prog(lt, 0.2, 1.6) * (1 - push) });
  place(S.bw[0].root, { x: -560, y: -60, z: -500, ry: 28, rx: 6, o: 1 });
  place(S.bw[1].root, { x: 0, y: 40, z: -900, rx: 10, o: 1 });
  place(S.bw[2].root, { x: 560, y: -40, z: -500, ry: -28, rx: 6, o: 1 });
  const zoom = 1 + push * 0.35;
  place(S.icon, { y: -230 - (1 - eo(prog(lt, 0.3, 1.5))) * 40, s: lerp(0.7, 1, eback(prog(lt, 0.3, 1.4))) * zoom, o: prog(lt, 0.3, 1.0) * (1 - push) });
  place(S.title, { y: 0 + (1 - eo(prog(lt, 0.8, 1.9))) * 40, s: zoom, o: prog(lt, 0.8, 1.7) * (1 - push) });
  place(S.sub, { y: 110, s: zoom, o: prog(lt, 1.4, 2.2) * (1 - push) });
  place(S.kick, { y: 162, s: zoom, o: prog(lt, 1.6, 2.4) * (1 - push) });
  place(S.line, { y: 252, o: prog(lt, 2.2, 3.0) * (1 - push) });
  place(S.chips, { y: 350, o: prog(lt, 2.8, 3.6) * (1 - push) });
});

// 1. The old way: scattered tools
const OLD = [['表格清洗', 'Spreadsheet', 'grid'], ['统计语法', 'Syntax', 'code'], ['单独作图', 'Plotting', 'bars'], ['手工排版', 'Formatting', 'doc']];
scene(B(3), B(7), (R, S) => {
  S.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  S.svg.setAttribute('width', 1920); S.svg.setAttribute('height', 1080); Object.assign(S.svg.style, { position: 'absolute', left: 0, top: 0 });
  R.appendChild(S.svg);
  S.pos = [[-470, -250, -6], [470, -260, 5], [-470, 110, 4], [470, 100, -5]];
  S.lines = [[0, 1], [1, 2], [2, 3], [3, 0], [0, 2]].map(([a, b]) => { const l = document.createElementNS('http://www.w3.org/2000/svg', 'line'); l.setAttribute('stroke', 'rgba(255,107,125,0.55)'); l.setAttribute('stroke-width', 2.5); l.setAttribute('stroke-dasharray', '10 10'); S.svg.appendChild(l); return { l, a, b }; });
  S.wins = OLD.map(([zh, en, kind]) => {
    const w = div('abs', R); Object.assign(w.style, { width: '400px', height: '262px', borderRadius: '12px', background: '#d9dee5', boxShadow: '0 30px 70px rgba(0,0,0,0.5)', overflow: 'hidden', filter: 'grayscale(1)' });
    let body = '';
    if (kind === 'grid') { for (let r = 0; r < 7; r++) { body += '<div style="display:flex;gap:4px;margin:4px 10px">'; for (let c = 0; c < 6; c++) body += `<div style="flex:1;height:22px;background:${(r + c) % 7 === 3 ? '#f2a3ad' : '#fff'};border-radius:3px"></div>`; body += '</div>'; } }
    if (kind === 'code') { for (let r = 0; r < 9; r++) body += `<div style="margin:9px 16px;height:10px;width:${30 + ((r * 37) % 60)}%;background:${r % 3 ? '#9aa7b6' : '#7b8aa0'};border-radius:5px"></div>`; }
    if (kind === 'bars') { body = '<div style="display:flex;align-items:flex-end;gap:16px;height:200px;margin:20px 40px;border-left:2px solid #8792a2;border-bottom:2px solid #8792a2;padding:0 16px">' + [60, 120, 90, 160, 70].map((h) => `<div style="flex:1;height:${h}px;background:#9aa7b6"></div>`).join('') + '</div>'; }
    if (kind === 'doc') { body = '<div style="margin:16px 40px;background:#fff;height:220px;padding:16px">' + [80, 95, 60, 90, 85, 40, 92].map((p) => `<div style="height:8px;width:${p}%;background:#c3cbd5;margin:10px 0;border-radius:4px"></div>`).join('') + '</div>'; }
    w.innerHTML = `<div style="height:30px;background:#aab3bf;display:flex;align-items:center;padding:0 12px;gap:7px"><i style="width:10px;height:10px;border-radius:50%;background:#7c8592;display:block"></i><i style="width:10px;height:10px;border-radius:50%;background:#7c8592;display:block"></i><i style="width:10px;height:10px;border-radius:50%;background:#7c8592;display:block"></i></div>${body}`;
    const lab = div('abs', R, `<div style="font:600 30px var(--zh);letter-spacing:3px">${zh}</div><div style="font:600 15px var(--en);letter-spacing:5px;color:var(--dim);margin-top:4px">${en.toUpperCase()}</div>`);
    lab.style.textAlign = 'center'; lab.style.whiteSpace = 'nowrap';
    return { w, lab };
  });
  S.x = textEl(R, '⇄', { font: '300 120px var(--en)', color: 'rgba(255,107,125,0.8)' });
}, (S, lt, d) => {
  const out = eio(prog(lt, d - 1.2, d));
  S.wins.forEach((W, i) => {
    const a = eback(prog(lt, 0.15 + i * 1.0, 0.75 + i * 1.0));
    const [x, y, r] = S.pos[i];
    const jit = lt > 4 ? Math.sin(lt * 23 + i * 2) * 3 * (1 - out) : 0;
    const k = 1 - out;
    place(W.w, { x: x * k + jit, y: y * k + jit, z: -out * 600, rz: r * k + out * 40, s: clamp(a, 0, 1.2) * lerp(1, 0.2, out), o: clamp(a) * (1 - out) });
    place(W.lab, { x: x * k, y: y * k + 172, o: prog(lt, 0.4 + i, 1.0 + i) * (1 - out) });
  });
  S.lines.forEach(({ l, a, b }, j) => {
    const A = S.pos[a], Bp = S.pos[b], v = prog(lt, 1.2 + j * 0.5, 1.6 + j * 0.5) * (1 - out);
    l.setAttribute('x1', 960 + A[0]); l.setAttribute('y1', 540 + A[1]); l.setAttribute('x2', 960 + Bp[0]); l.setAttribute('y2', 540 + Bp[1]);
    l.setAttribute('opacity', v); l.setAttribute('stroke-dashoffset', -lt * 40);
  });
  place(S.x, { o: prog(lt, 4.0, 4.6) * (1 - out) * (0.6 + 0.4 * Math.sin(lt * 6)), s: 1 + out });
});

// 2. Reveal: home → file drop
scene(B(7), B(10), (R, S) => {
  S.W = win(R, { srcs: [SH + 'home.png', SH + 'home_file.png'], crop: [0, 0, 1920, 1080], w: 1400 });
  S.sweep = div('', S.W.ov); Object.assign(S.sweep.style, { position: 'absolute', top: '-20%', width: '35%', height: '140%', background: 'linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.28), rgba(255,255,255,0))', transform: 'rotate(18deg)' });
  S.file = div('abs', R, '<div style="display:flex;align-items:center;gap:14px;padding:16px 24px;border-radius:14px;background:rgba(255,255,255,0.96);color:#1c2533;font:600 22px var(--en);box-shadow:0 20px 50px rgba(0,0,0,0.45)"><span style="display:inline-block;width:34px;height:42px;border-radius:5px;background:#21a366;color:#fff;font:800 12px var(--en);line-height:42px;text-align:center">CSV</span>demo_trial.csv</div>');
  S.C = cursor(S.W);
  S.t1 = tag(S.W, '拖入即可', 'Drag & drop');
}, (S, lt) => {
  const p = kf(lt, [[0, { z: -1800, rx: 38, ry: 0, y: 80, o: 0 }], [1.7, { z: 0, rx: 9, ry: -5, y: 10, o: 1 }, ex], [6, { z: 60, rx: 4, ry: 5, y: 0, o: 1 }]]);
  place(S.W.root, { ...p, x: 0 });
  S.sweep.style.left = lerp(-40, 120, prog(lt, 1.0, 2.6)) + '%';
  // file drag: from right edge to drop zone (906, 590)
  const fp = prog(lt, 2.6, 4.0);
  const fx = lerp(820, 120, eio(fp)), fy = lerp(300, 90, eio(fp));
  place(S.file, { x: fx, y: fy, s: lerp(1, 0.85, fp), o: prog(lt, 2.4, 2.7) * (1 - prog(lt, 4.1, 4.4)) });
  showLayer(S.W, lt > 4.2 ? 1 : 0);
  posCursor(S.W, S.C, lt, [[2.2, 1700, 900], [2.6, 1880, 700], [4.0, 960, 600], [4.6, 960, 600], [5.4, 1190, 735]], [5.4], prog(lt, 2.2, 2.5));
  posTag(S.W, S.t1, 906, 400, prog(lt, 3.0, 3.4) * (1 - prog(lt, 5.0, 5.4)));
});

// 3. Variable recognition
scene(B(10), B(13), (R, S) => {
  S.W = win(R, { srcs: SH + 'variables.png', crop: [0, 0, 1920, 1080], w: 1400 });
  S.h = [hl(S.W, [445, 150, 112, 790]), hl(S.W, [586, 150, 146, 790]), hl(S.W, [745, 150, 330, 790])];
  S.t = [tag(S.W, '类型识别', 'Types'), tag(S.W, '缺失比例', 'Missing'), tag(S.W, '取值范围', 'Ranges')];
}, (S, lt) => {
  setCrop(S.W, kfRect(lt, [[0, [0, 0, 1920, 1080]], [1.6, [0, 60, 1240, 698]], [5.6, [20, 100, 1200, 675]]]));
  place(S.W.root, { ...kf(lt, [[0, { rx: 6, ry: 16, z: -200, y: 0 }], [1.4, { rx: 4, ry: 4, z: 0, y: 0 }, ex], [6, { rx: 3, ry: -3, z: 40, y: 0 }]]), o: 1 });
  S.h.forEach((H, i) => posHL(S.W, H, prog(lt, 1.6 + i * 1.0, 1.9 + i * 1.0)));
  S.t.forEach((T, i) => posTag(S.W, T, [501, 659, 910][i], 140, prog(lt, 1.7 + i * 1.0, 2.1 + i * 1.0)));
});

// 4. Data preview — original untouched
scene(B(13), B(16), (R, S) => {
  S.W = win(R, { srcs: SH + 'preview.png', crop: [0, 0, 1440, 810], w: 1400 });
  S.h1 = hl(S.W, [338, 36, 202, 26]); S.t1 = tag(S.W, '原始文件未改动', 'Original untouched');
  S.h2 = hl(S.W, [1608, 36, 116, 26]); S.t2 = tag(S.W, '历史快照', 'Snapshots');
  S.h3 = hl(S.W, [1430, 36, 172, 26]); S.t3 = tag(S.W, '草稿编辑', 'Draft edits');
}, (S, lt) => {
  setCrop(S.W, kfRect(lt, [[0, [0, 0, 1440, 810]], [2.6, [0, 0, 1440, 810]], [4.0, [480, 0, 1440, 810]], [6, [480, 30, 1440, 810]]]));
  place(S.W.root, { ...kf(lt, [[0, { rx: 10, ry: -14, z: -300, y: 0 }], [1.2, { rx: 5, ry: -4, z: 0, y: 0 }, ex], [6, { rx: 4, ry: 4, z: 40, y: 0 }]]), o: 1 });
  posHL(S.W, S.h1, fade(lt, 0.9, 3.0, 0.3)); posTag(S.W, S.t1, 440, 112, fade(lt, 1.0, 3.0, 0.3));
  posHL(S.W, S.h3, fade(lt, 4.0, 6.2, 0.3)); posTag(S.W, S.t3, 1515, 112, fade(lt, 4.1, 6.2, 0.3));
  posHL(S.W, S.h2, fade(lt, 4.6, 6.2, 0.3)); posTag(S.W, S.t2, 1700, 170, fade(lt, 4.7, 6.2, 0.3));
});

// 5. Toolbox montage (7 tools × 1 bar, then a fan)
const TOOLS = [
  ['变量计算', 'Compute', [SH + 'tool_compute.png', SH + 'tool_compute_typed.png'], [480, 204, 960, 672]],
  ['重编码', 'Recode', SH + 'tool_recode.png', [480, 216, 960, 646]],
  ['批量操作', 'Batch edit', SH + 'tool_batch.png', [480, 202, 960, 674]],
  ['AI 文本编码', 'AI text coding', SH + 'tool_ai_encode.png', [480, 208, 960, 662]],
  ['医学标准', 'Medical standards', SH + 'tool_medical_bmi.png', [502, 204, 914, 670]],
  ['智能合并', 'Smart merge', SH + 'tool_merge.png', [470, 264, 978, 550]],
  ['导出数据', 'Export data', SH + 'tool_export.png', [752, 272, 414, 534]],
];
scene(B(16), B(24), (R, S) => {
  S.menu = div('abs', R); Object.assign(S.menu.style, { width: '360px' });
  S.items = TOOLS.map(([zh, en]) => div('', S.menu, `<div style="font:600 30px var(--zh);letter-spacing:2px">${zh}</div><div style="font:600 14px var(--en);letter-spacing:4px;color:var(--dim);margin-top:2px">${en.toUpperCase()}</div>`));
  S.items.forEach((it) => Object.assign(it.style, { padding: '14px 0 14px 26px', borderLeft: '3px solid rgba(255,255,255,0.12)', transition: 'none' }));
  S.title = textEl(R, '数据工具箱 <span style="font:700 18px var(--en);letter-spacing:6px;color:var(--teal);margin-left:12px">DATA TOOLBOX</span>', { font: '600 26px var(--zh)', whiteSpace: 'nowrap' });
  S.cards = TOOLS.map(([, , srcs, crop]) => { const fitW = Math.min(1000, (680 / crop[3]) * crop[2]); return win(R, { srcs, crop, w: fitW, chrome: false, radius: 18 }); });
}, (S, lt, d) => {
  const cur = clamp(Math.floor(lt / 2), 0, 6), fan = prog(lt, 14.0, 15.2);
  place(S.menu, { x: -660, y: 0, o: prog(lt, 0, 0.5) * (1 - fan) });
  place(S.title, { x: -660, y: -330, o: prog(lt, 0, 0.5) * (1 - fan) });
  S.items.forEach((it, i) => {
    const on = i === cur && fan < 0.5;
    it.style.borderLeftColor = on ? 'var(--teal)' : 'rgba(255,255,255,0.12)';
    it.style.color = on ? '#fff' : 'rgba(220,236,242,0.38)';
    it.style.background = on ? 'linear-gradient(90deg, rgba(46,230,197,0.14), rgba(46,230,197,0))' : 'none';
  });
  S.cards.forEach((C, i) => {
    const l = lt - i * 2;
    const enter = ex(prog(l, 0, 0.55)), leave = eio(prog(l, 2.0, 2.45));
    let p;
    if (fan > 0) {
      const ang = (i - 3) * 12;
      p = { x: lerp(170, (i - 3) * 230, eio(fan)), y: lerp(-20, 30, eio(fan)), z: lerp(0, -900 + Math.abs(i - 3) * 60, eio(fan)), ry: lerp(0, -ang * 1.6, eio(fan)), rx: 0, s: lerp(1, 0.62, eio(fan)), o: lt >= i * 2 ? 1 : 0 };
      if (i < 6) p.o = eio(fan);
    } else {
      p = { x: 170 + (1 - enter) * 260 - leave * 420, y: -20, z: (1 - enter) * -400 - leave * 300, ry: (1 - enter) * 38 - leave * 30, rx: 0, s: 1, o: enter * (1 - leave * 0.999) };
      if (i === 6) p.o = enter;
    }
    if (l < -0.01 && fan === 0) p.o = 0;
    place(C.root, p);
    if (i === 0) showLayer(C, 0, prog(l, 0.7, 0.9));
  });
});

// 6. Methods: 17 domains · 100+
const CATS = [['基础统计', 'Descriptive'], ['差异检验', 'Comparisons'], ['分类数据', 'Categorical'], ['回归与相关', 'Regression'], ['高级回归', 'Advanced regression'], ['中介与调节', 'Mediation'], ['生存分析', 'Survival'], ['诊断试验', 'Diagnostics'], ['循证医学', 'Meta-analysis'], ['心理测量', 'Psychometrics'], ['结构方程', 'SEM'], ['高级心理测量', 'IRT & LPA'], ['因果推断', 'Causal inference'], ['一致性分析', 'Agreement'], ['高级模型与功效', 'Models & power'], ['生物信息学', 'Bioinformatics'], ['智能研究', 'AI research']];
scene(B(24), B(28), (R, S) => {
  S.col = div('abs', R); Object.assign(S.col.style, { width: '330px', height: '840px', overflow: 'hidden', borderRadius: '18px', background: '#f5f7fa', boxShadow: '0 50px 120px rgba(0,0,0,0.55)' });
  S.side = img(SH + 'sidebar_full.png', S.col); Object.assign(S.side.style, { width: '330px', display: 'block' });
  S.fadeTop = div('', S.col); Object.assign(S.fadeTop.style, { position: 'absolute', inset: 0, background: 'linear-gradient(rgba(245,247,250,1), rgba(245,247,250,0) 12%, rgba(245,247,250,0) 88%, rgba(245,247,250,1))' });
  S.n1 = textEl(R, '', { font: '700 210px var(--en)', whiteSpace: 'nowrap' });
  S.l1 = textEl(R, '研究领域 <span style="font:700 18px var(--en);letter-spacing:6px;color:var(--dim);margin-left:8px">DOMAINS</span>', { font: '600 32px var(--zh)', whiteSpace: 'nowrap' });
  S.n2 = textEl(R, '', { font: '700 210px var(--en)', color: 'var(--teal)', whiteSpace: 'nowrap', textShadow: '0 0 60px rgba(46,230,197,0.45)' });
  S.l2 = textEl(R, '统计方法 <span style="font:700 18px var(--en);letter-spacing:6px;color:var(--dim);margin-left:8px">METHODS</span>', { font: '600 32px var(--zh)', whiteSpace: 'nowrap' });
  S.chips = CATS.map(([zh, en]) => textEl(R, `<span class="chip" style="font-size:20px">${zh}<span style="font:600 13px var(--en);color:var(--dim);letter-spacing:1px">${en}</span></span>`, { whiteSpace: 'nowrap' }));
}, (S, lt) => {
  const sideH = 330 * 11290 / 510;
  place(S.col, { x: -600, y: 0, rx: 4, ry: 24, z: -100 + prog(lt, 0, 1) * 100, o: prog(lt, 0, 0.4) });
  S.side.style.transform = `translateY(${-eio(prog(lt, 0.2, 7.6)) * (sideH - 840)}px)`;
  const c1 = Math.round(17 * eo(prog(lt, 0.3, 1.6))), c2 = Math.round(100 * eo(prog(lt, 0.8, 2.6)));
  S.n1.textContent = c1; S.n2.textContent = c2 + (c2 >= 100 ? '+' : '');
  const pulse = Math.exp(-(((lt) % 0.5)) * 8) * 0.03;
  place(S.n1, { x: 40, y: -250, s: lerp(0.6, 1, eback(prog(lt, 0.2, 0.9))) + pulse, o: prog(lt, 0.2, 0.5) });
  place(S.l1, { x: 40, y: -120, o: prog(lt, 0.5, 0.9) });
  place(S.n2, { x: 470, y: -250, s: lerp(0.6, 1, eback(prog(lt, 0.7, 1.4))) + pulse, o: prog(lt, 0.7, 1.0) });
  place(S.l2, { x: 470, y: -120, o: prog(lt, 1.0, 1.4) });
  S.chips.forEach((C, i) => {
    const col = i % 4, row = Math.floor(i / 4);
    const a = eback(prog(lt, 1.8 + i * 0.25, 2.2 + i * 0.25));
    place(C, { x: -120 + col * 270 + (row === 4 ? 405 : 0), y: -10 + row * 70, s: clamp(a, 0, 1.2), o: clamp(a) });
  });
});

// 7. Pick a method, drag variables, run
scene(B(28), B(32), (R, S) => {
  S.W = win(R, { srcs: [SH + 'tt_empty.png', SH + 'tt_assign1.png', SH + 'tt_assign2.png', SH + 'tt_assign3.png'], crop: [190, 40, 1000, 620], w: 1200 });
  S.C = cursor(S.W);
  S.hRun = hl(S.W, [985, 100, 80, 33]);
}, (S, lt) => {
  setCrop(S.W, kfRect(lt, [[0, [190, 40, 1000, 620]], [1.7, [190, 40, 1000, 620]], [2.3, [190, 300, 1000, 620]], [4.9, [190, 300, 1000, 620]], [5.6, [470, 40, 700, 434]]]));
  place(S.W.root, { ...kf(lt, [[0, { rx: 8, ry: 12, z: -300, y: 0 }], [1.0, { rx: 4, ry: 4, z: 0, y: 0 }, ex], [8, { rx: 3, ry: -4, z: 40, y: 0 }]]), o: 1 });
  showLayer(S.W, lt < 1.55 ? 0 : lt < 3.35 ? 1 : lt < 4.75 ? 2 : 3);
  posCursor(S.W, S.C, lt, [[0, 700, 560], [0.7, 300, 394], [1.5, 792, 236], [2.5, 300, 814], [3.3, 792, 376], [4.0, 300, 874], [4.7, 792, 376], [6.2, 1023, 116]], [0.8, 1.5, 2.6, 3.3, 4.05, 4.7, 6.6]);
  posHL(S.W, S.hRun, fade(lt, 6.0, 8.0, 0.3));
});

// 8. Results: table, figure, AI
scene(B(32), B(36), (R, S) => {
  S.W = win(R, { srcs: SH + 'tt_result.png', crop: [0, 0, 1920, 1080], w: 1400 });
  S.h = [hl(S.W, [1102, 108, 806, 120]), hl(S.W, [1102, 334, 324, 730]), hl(S.W, [1440, 322, 468, 748])];
  S.t = [tag(S.W, 'APA 三线表', 'APA table'), tag(S.W, '统计图', 'Figure'), tag(S.W, 'AI 解读', 'AI insight')];
  S.tab = win(R, { srcs: SH + 'tt_result.png', crop: [1102, 150, 806, 156], w: 1240, chrome: false, radius: 14 });
  S.fig = pic(R, AS + 'r_sbp_12w.png', 560, 407);
  S.stats = textEl(R, ['t = 5.255', 'df = 238', 'p < 0.001', 'Δ = 10.67 mmHg'].map((s) => `<div class="chip" style="font:600 26px var(--en);margin:10px 0;display:block;text-align:center">${s}</div>`).join(''), { width: '380px' });
}, (S, lt) => {
  const A = 1 - eio(prog(lt, 3.6, 4.2));
  place(S.W.root, { ...kf(lt, [[0, { rx: 6, ry: -14, z: -250, y: 0 }], [1.0, { rx: 4, ry: -5, z: 0, y: 0 }, ex], [4, { rx: 3, ry: 2, z: 50, y: 0 }]]), o: A });
  S.h.forEach((H, i) => posHL(S.W, H, prog(lt, 0.8 + i * 0.9, 1.1 + i * 0.9)));
  S.t.forEach((T, i) => posTag(S.W, T, [1505, 1264, 1674][i], [100, 320, 310][i], prog(lt, 0.9 + i * 0.9, 1.3 + i * 0.9)));
  const B2 = eio(prog(lt, 3.8, 4.5));
  place(S.tab.root, { y: lerp(-80, -250, B2), z: lerp(-300, 0, B2), o: B2 });
  place(S.fig, { x: -330, y: 150, ry: lerp(30, 8, B2), z: lerp(-400, 0, B2), o: prog(lt, 4.2, 4.8) });
  place(S.stats, { x: 380, y: 140, o: prog(lt, 4.8, 5.4), ry: -8 });
});
scene(B(36), B(40), (R, S) => {
  const fs = Array.from({ length: 173 }, (_, k) => k);
  S.frames = FRAMES.ai_stream;
  S.box = div('abs', R); Object.assign(S.box.style, { width: '600px', height: '954px', borderRadius: '18px', overflow: 'hidden', background: '#fff', boxShadow: '0 50px 120px rgba(0,0,0,0.55), 0 0 0 1px rgba(255,255,255,0.08), 0 0 90px rgba(46,230,197,0.18)' });
  S.imgs = S.frames.map(([f]) => { const i = img(SH + 'ai_stream/' + f, S.box); Object.assign(i.style, { width: '600px', display: 'none', position: 'absolute', left: 0, top: 0 }); return i; });
  S.secs = [['核心结论', 'Key finding'], ['临床意义', 'Clinical meaning'], ['方法学提示', 'Method notes'], ['论文写作建议', 'Manuscript wording']].map(([zh, en]) => textEl(R, `<div style="font:600 46px var(--zh);letter-spacing:4px">${zh}</div><div style="font:700 16px var(--en);letter-spacing:6px;color:var(--teal);margin-top:6px">${en.toUpperCase()}</div>`, { whiteSpace: 'nowrap' }));
  S.badge = textEl(R, '<span class="chip"><span style="color:var(--teal)">✦</span> 由真实 R 结果生成 · Grounded in the R output</span>', {});
}, (S, lt) => {
  // stream: capture time 3.0 s → 16.0 s mapped onto 0.4 → 7.4 s
  const ct = lerp(3000, 16500, prog(lt, 0.4, 7.4));
  let k = 0; S.frames.forEach(([, ms], i) => { if (ms <= ct) k = i; });
  S.imgs.forEach((im, i) => { im.style.display = i === k ? 'block' : 'none'; });
  place(S.box, { x: 330, y: -40, ry: lerp(-24, -10, eo(prog(lt, 0, 1))), z: lerp(-300, 0, ex(prog(lt, 0, 0.8))), o: prog(lt, 0, 0.4) });
  S.secs.forEach((T, i) => {
    const on = prog(lt, 1.2 + i * 1.6, 1.6 + i * 1.6);
    place(T, { x: -470, y: -270 + i * 150, o: lerp(0.18, 1, on), s: lerp(0.94, 1, on) });
  });
  place(S.badge, { x: -470, y: 330, o: prog(lt, 6.6, 7.2) });
});

// 9. AI assistant + privacy
scene(B(40), B(47), (R, S) => {
  S.W = win(R, { srcs: [SH + 'chat_typed.png', SH + 'chat_consent.png', SH + 'chat_stream2.png', SH + 'chat_done.png'], crop: [320, 150, 1280, 780], w: 1320 });
  S.h = hl(S.W, [646, 610, 928, 130]); S.t = tag(S.W, '本机模型 · 数据不离开电脑', 'Local model');
  S.shield = textEl(R, '<svg width="150" height="170" viewBox="0 0 24 28"><path d="M12 1 L22 5 V13 C22 20 17.5 25 12 27 C6.5 25 2 20 2 13 V5 Z" fill="rgba(46,230,197,0.15)" stroke="#2ee6c5" stroke-width="1.3"/><path d="M7.5 14 L10.8 17.3 L16.8 10.8" fill="none" stroke="#2ee6c5" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>', { filter: 'drop-shadow(0 0 30px rgba(46,230,197,0.6))' });
}, (S, lt) => {
  showLayer(S.W, lt < 2.6 ? 0 : lt < 8.0 ? 1 : lt < 9.4 ? 2 : 3);
  setCrop(S.W, kfRect(lt, [[0, [320, 150, 1280, 780]], [3.0, [320, 150, 1280, 780]], [4.0, [560, 420, 1060, 646]], [7.6, [560, 420, 1060, 646]], [8.4, [320, 150, 1280, 780]]]));
  place(S.W.root, { ...kf(lt, [[0, { rx: 6, ry: 10, z: -250, y: 10, x: 0 }], [1.2, { rx: 3, ry: 3, z: 0, y: 10, x: 0 }, ex], [4, { rx: 2, ry: -3, z: 0, y: 10, x: 110 }], [8, { rx: 2, ry: -3, z: 0, y: 10, x: 110 }], [9, { rx: 3, ry: 2, z: 30, y: 10, x: 0 }], [14, { rx: 2, ry: -2, z: 60, y: 10, x: 0 }]]), o: 1 });
  posHL(S.W, S.h, fade(lt, 4.0, 7.8, 0.35));
  posTag(S.W, S.t, 1110, 590, fade(lt, 4.2, 7.8, 0.35));
  place(S.shield, { x: -760, y: -60, s: lerp(0.6, 1, eback(prog(lt, 3.8, 4.4))), o: fade(lt, 3.8, 8.0, 0.4) });
});

// 10. Method gallery (coverflow on bars)
const GAL = [['km_plot', 'Kaplan-Meier 生存曲线', 'Survival'], ['cox_plot', 'Cox 回归森林图', 'Cox regression'], ['roc_plot', 'ROC 曲线', 'Diagnostic accuracy'], ['logit_plot', 'Logistic 回归 OR 森林图', 'Logistic regression'], ['subgroup_plot', '亚组交互森林图', 'Subgroup analysis'], ['meta_plot', 'Meta 分析森林图', 'Meta-analysis'], ['dca_plot', '决策曲线分析', 'Decision curves']];
scene(B(47), B(56), (R, S) => {
  S.cards = GAL.map(([f, zh, en]) => {
    const W = win(R, { srcs: SH + f + '.png', crop: plotCrop, w: 940, chrome: false, radius: 18 });
    const L = div('', W.root, `<div style="font:600 24px var(--zh)">${zh}</div><div style="font:700 13px var(--en);letter-spacing:4px;color:#0f8f80;margin-top:2px">${en.toUpperCase()}</div>`);
    Object.assign(L.style, { position: 'absolute', left: '22px', top: '18px', padding: '10px 18px', borderRadius: '12px', background: 'rgba(255,255,255,0.92)', color: '#1c2533', boxShadow: '0 6px 20px rgba(0,0,0,0.15)' });
    return W;
  });
  S.ml = win(R, { srcs: SH + 'predict.png', crop: [1105, 245, 760, 182], w: 1100, chrome: false, radius: 16 });
  S.mlroc = win(R, { srcs: SH + 'predict_plot.png', crop: plotCrop, w: 430, chrome: false, radius: 16 });
  S.mlt = textEl(R, '临床预测模型 · 多算法对比 <span style="font:700 16px var(--en);letter-spacing:5px;color:var(--teal);margin-left:10px">MACHINE-LEARNING MODELS</span>', { font: '600 32px var(--zh)', whiteSpace: 'nowrap' });
}, (S, lt) => {
  let c = 0;
  for (let i = 0; i < 7; i++) { const l = lt - i * 2; if (l >= 0) c = i - 1 + ex(prog(l, 0, 0.45)); }
  if (lt < 0.45) c = -1 + ex(prog(lt, 0, 0.45)) * 1;
  const outML = eio(prog(lt, 13.6, 14.2));
  S.cards.forEach((W, i) => {
    const d = i - c;
    place(W.root, { x: d * 840 - outML * 300, y: 0, z: -Math.abs(d) * 560 - outML * 800, ry: clamp(-d * 42, -60, 60), s: lerp(1, 0.84, clamp(Math.abs(d))), o: clamp(1 - Math.abs(d) * 0.55) * (1 - outML) * (d > 1.6 ? 0 : 1) });
  });
  const m = eio(prog(lt, 14.0, 14.7));
  place(S.mlt, { y: -340, o: m });
  place(S.ml.root, { y: -170, z: lerp(-500, 0, m), rx: lerp(20, 0, m), o: m });
  place(S.mlroc.root, { x: 0, y: 225, z: lerp(-500, 0, m), o: prog(lt, 14.5, 15.0) });
});

// 11a. Figures: chart types + DPI
scene(B(56), B(60), (R, S) => {
  const figCrop = [1110, 420, 306, 460];
  S.figs = [['tt_result', '箱线图', 'Box'], ['chart_雨云图', '雨云图', 'Raincloud'], ['chart_柱状+散点', '柱状 + 散点', 'Bar + dots']].map(([f, zh, en]) => {
    const W = win(R, { srcs: SH + f + '.png', crop: figCrop, w: 400, chrome: false, radius: 16 });
    const L = div('', W.root, `${zh} <span style="font:700 12px var(--en);letter-spacing:3px;color:#0f8f80">${en.toUpperCase()}</span>`);
    Object.assign(L.style, { position: 'absolute', left: '50%', bottom: '14px', transform: 'translateX(-50%)', padding: '8px 16px', borderRadius: '10px', background: 'rgba(255,255,255,0.94)', color: '#1c2533', font: '600 20px var(--zh)', whiteSpace: 'nowrap', boxShadow: '0 6px 20px rgba(0,0,0,0.15)' });
    return W;
  });
  S.dl = win(R, { srcs: SH + 'dl_dialog.png', crop: [732, 388, 456, 302], w: 760, chrome: false, radius: 18 });
  S.h300 = hl(S.dl, [762, 506, 192, 98]); S.h600 = hl(S.dl, [968, 506, 192, 98]);
  S.fmt = textEl(R, ['PNG', 'TIFF', 'PDF'].map((s) => `<div class="chip" style="font:800 30px var(--en);padding:14px 34px;margin:16px 0;border-color:var(--teal);display:flex;justify-content:center">${s}</div>`).join(''), { width: '170px' });
}, (S, lt) => {
  const toDL = eio(prog(lt, 3.6, 4.3));
  S.figs.forEach((W, i) => {
    const a = ex(prog(lt, 0.1 + i * 0.5, 0.7 + i * 0.5));
    place(W.root, { x: (i - 1) * 470 - toDL * 0, y: lerp(-40, -260, toDL), z: lerp(-500, 0, a) - toDL * 500, ry: (1 - a) * 40 + (i - 1) * -6, s: lerp(1, 0.7, toDL), o: a * (1 - toDL * 0.6) });
  });
  place(S.dl.root, { x: -110, y: 90, z: lerp(-600, 0, toDL), rx: lerp(25, 0, toDL), o: toDL });
  posHL(S.dl, S.h300, prog(lt, 4.8, 5.1)); posHL(S.dl, S.h600, prog(lt, 5.4, 5.7));
  place(S.fmt, { x: 520, y: 90, o: prog(lt, 5.8, 6.3), s: lerp(0.8, 1, eback(prog(lt, 5.8, 6.4))) });
});

// 11b. Word report (real export, page rendered by macOS Quick Look)
scene(B(60), B(64), (R, S) => {
  const pg = (cls) => { const d = div(cls, R); Object.assign(d.style, { width: '680px', height: '760px', borderRadius: '8px', overflow: 'hidden', background: '#fff', boxShadow: '0 40px 100px rgba(0,0,0,0.5)' }); return d; };
  S.back = [pg('abs'), pg('abs')]; S.back.forEach((b) => { b.style.filter = 'brightness(0.84)'; img(AS + 'word_page1.png', b).style.cssText = 'width:680px;display:block;opacity:0.5'; });
  S.page = pg('abs');
  S.pimg = img(AS + 'word_page1.png', S.page); Object.assign(S.pimg.style, { width: '680px', display: 'block' });
  const fadeB = div('', S.page); Object.assign(fadeB.style, { position: 'absolute', left: 0, right: 0, top: '440px', height: '320px', background: 'linear-gradient(rgba(255,255,255,0), #fff 70%)' });
  S.hPar = div('hl', S.page); S.hTab = div('hl', S.page); S.hFig = div('hl', S.page);
  Object.assign(S.hPar.style, { left: '22px', top: '84px', width: '240px', height: '134px' });
  Object.assign(S.hTab.style, { left: '24px', top: '248px', width: '346px', height: '46px' });
  Object.assign(S.hFig.style, { left: '170px', top: '312px', width: '340px', height: '200px' });
  S.badge = textEl(R, '<div style="width:104px;height:104px;border-radius:24px;background:#2b579a;color:#fff;font:800 62px var(--en);display:flex;align-items:center;justify-content:center;box-shadow:0 20px 50px rgba(0,0,0,0.5)">W</div>', {});
  S.file = textEl(R, '<span class="chip" style="font:500 21px var(--mono)">MedStat_t_test_indep_Report.docx</span>', {});
  S.notes = [['分析参数', 'Parameters'], ['三线表', 'APA table'], ['统计图表', 'Figures']].map(([zh, en]) => textEl(R, `<div style="font:600 38px var(--zh);letter-spacing:3px">${zh}</div><div style="font:700 15px var(--en);letter-spacing:6px;color:var(--teal);margin-top:4px">${en.toUpperCase()}</div>`, { width: '340px' }));
}, (S, lt) => {
  const a = ex(prog(lt, 0, 0.8));
  place(S.back[0], { x: 160 + 56, y: -10 - 26, z: -120, rz: 4, o: a * 0.9 });
  place(S.back[1], { x: 160 + 28, y: -10 - 13, z: -60, rz: 2, o: a * 0.95 });
  place(S.page, { x: 160, y: -10, z: lerp(-400, 0, a), rx: lerp(25, 5, a), ry: -8, o: a });
  const steps = [[1.2, 3.2], [3.2, 5.2], [5.2, 7.6]];
  [S.hPar, S.hTab, S.hFig].forEach((h, i) => { h.style.opacity = fade(lt, steps[i][0], steps[i][1], 0.3); });
  S.notes.forEach((n, i) => place(n, { x: -520, y: -150 + i * 130, o: lerp(0.25, 1, fade(lt, steps[i][0], steps[i][1], 0.3)) * prog(lt, 0.8, 1.3) }));
  place(S.badge, { x: 480, y: -380, s: lerp(0.5, 1, eback(prog(lt, 0.5, 1.0))), o: prog(lt, 0.5, 0.8) });
  place(S.file, { x: 160, y: -440, o: prog(lt, 1.0, 1.5) });
});

// 11c. Reproducible R script, rerun outside the app
const RLINES = [
  ['c', '# Independent-samples t test - Reproducible R Script'],
  ['c', '# Generated by MedStat Pilot. Data file: demo_trial.csv'],
  ['', ''],
  ['p', 'group <- <s>"group"</s>'],
  ['p', 'vars <- <f>c</f>(<s>"sbp_12w"</s>, <s>"ldl"</s>)'],
  ['p', 'download_dpi <- <n>600</n>'],
  ['', ''],
  ['p', 'welch <- <f>isTRUE</f>(<f>levene_p</f>(w$.y, w$.g) < <n>0.05</n>)'],
  ['p', 'tt <- stats::<f>t.test</f>(.y ~ .g, data = w, var.equal = !welch)'],
  ['p', 'result <- <f>do.call</f>(rbind, rows)'],
  ['p', '<f>print</f>(result)'],
  ['p', '<f>save_figure</f>(<f>group_plot</f>(w, group, v), v)'],
];
scene(B(64), B(68), (R, S) => {
  S.ed = div('abs card', R); Object.assign(S.ed.style, { width: '1060px', padding: '0 0 22px 0', background: 'rgba(8,16,28,0.97)' });
  S.ed.innerHTML = '<div class="win-bar" style="border-radius:18px 18px 0 0"><i></i><i></i><i></i><span>t_test_indep_analysis.R</span></div>';
  S.code = div('code', S.ed); S.code.style.padding = '20px 30px';
  S.term = div('abs card', R); Object.assign(S.term.style, { width: '1060px', background: 'rgba(3,8,14,0.97)', padding: '18px 26px', font: '500 18px/1.6 var(--mono)', whiteSpace: 'pre', color: '#d6e2ea' });
  S.ok = textEl(R, '<div style="display:flex;align-items:center;gap:22px"><div class="chip" style="font:600 22px var(--en)">App · 应用内 &nbsp;<b style="color:var(--teal)">t = 5.255 · 10.667 [6.668, 14.665]</b></div><div style="width:58px;height:58px;border-radius:50%;background:var(--teal);color:#04201c;font:800 34px var(--en);display:flex;align-items:center;justify-content:center;box-shadow:0 0 40px rgba(46,230,197,0.7)">=</div><div class="chip" style="font:600 22px var(--en)">R rerun · 独立重跑 &nbsp;<b style="color:var(--teal)">t = 5.255 · 10.667 [6.668, 14.665]</b></div></div>', { whiteSpace: 'nowrap' });
  S.consoleLines = R_CONSOLE;
}, (S, lt) => {
  const total = RLINES.reduce((s, [, l]) => s + l.replace(/<[^>]+>/g, '').length + 1, 0);
  let shown = Math.floor(total * prog(lt, 0.3, 2.8)), html = '';
  RLINES.forEach(([k, l], i) => {
    const plain = l.replace(/<[^>]+>/g, '');
    const n = clamp(shown, 0, plain.length); shown -= plain.length + 1;
    let vis = n >= plain.length ? l : escapeHtml(plain.slice(0, n));
    if (n >= plain.length) vis = l.replace(/<s>/g, '<span class="s">').replace(/<\/s>/g, '</span>').replace(/<f>/g, '<span class="f">').replace(/<\/f>/g, '</span>').replace(/<n>/g, '<span class="n">').replace(/<\/n>/g, '</span>');
    html += `<span class="c">${String(i + 1).padStart(2, ' ')}  </span>${k === 'c' ? `<span class="c">${vis}</span>` : vis}\n`;
  });
  S.code.innerHTML = html;
  const a = ex(prog(lt, 0, 0.6)), up = eio(prog(lt, 3.0, 3.6));
  place(S.ed, { y: lerp(-40, -160, up), z: lerp(-300, 0, a), rx: 6, ry: lerp(14, 4, a), o: a });
  const tl = prog(lt, 3.3, 3.7);
  const cons = ['$ Rscript t_test_indep_analysis.R'].concat(S.consoleLines);
  const nlines = Math.floor(lerp(0, cons.length, prog(lt, 3.6, 5.2)));
  S.term.textContent = cons.slice(0, Math.max(1, nlines)).join('\n');
  place(S.term, { y: 250, ry: 4, rx: 6, z: lerp(-300, 0, tl), o: tl });
  place(S.ok, { y: 420, s: lerp(0.8, 1, eback(prog(lt, 5.4, 6.0))), o: prog(lt, 5.4, 5.8) });
});
function escapeHtml(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

// 11d. AI-R Studio
scene(B(68), B(72), (R, S) => {
  S.W = win(R, { srcs: SH + 'air_studio.png', crop: [256, 60, 1664, 936], w: 1400 });
  S.h1 = hl(S.W, [600, 140, 1290, 66]); S.t1 = tag(S.W, '六步闭环', 'Six-step loop');
  S.h2 = hl(S.W, [606, 532, 608, 50]); S.t2 = tag(S.W, 'R 脚本在本机运行', 'Runs locally');
}, (S, lt) => {
  setCrop(S.W, kfRect(lt, [[0, [256, 60, 1664, 936]], [2.0, [256, 60, 1664, 936]], [3.4, [560, 100, 1360, 765]], [8, [520, 110, 1360, 765]]]));
  place(S.W.root, { ...kf(lt, [[0, { rx: 10, ry: -16, z: -300, y: -20 }], [1.0, { rx: 5, ry: -5, z: 0, y: -20 }, ex], [8, { rx: 3, ry: 3, z: 40, y: -20 }]]), o: 1 });
  posHL(S.W, S.h1, fade(lt, 1.0, 4.4, 0.3)); posTag(S.W, S.t1, 1245, 230, fade(lt, 1.1, 4.4, 0.3));
  posHL(S.W, S.h2, fade(lt, 4.6, 7.8, 0.3)); posTag(S.W, S.t2, 910, 610, fade(lt, 4.7, 7.8, 0.3));
});

// 12. What's different (rows on bars 74–84), then platforms
const CMP = [
  ['清洗、统计、作图、排版分散在多个软件', 'Scattered across several tools', '一个工作台，从数据到论文', 'One workbench, data to manuscript'],
  ['菜单繁杂，或需编写语法', 'Menus and syntax to learn', '引导式流程，拖拽即分析', 'Guided flow: drag, then run'],
  ['结果需手工整理成三线表', 'Tables retyped by hand', 'APA 三线表与期刊级图表自动生成', 'APA tables & journal figures, automatic'],
  ['结果解读与写作全靠自己', 'Interpretation is on you', 'AI 解读与论文写作建议', 'AI interpretation & writing help'],
  ['分析过程难以复现', 'Hard to reproduce', 'Word 报告 + 可复现 R 脚本', 'Word report + reproducible R script'],
  ['前沿方法需另学编程', 'Modern methods need coding', '因果推断、机器学习、生信分析内置', 'Causal, ML and bioinformatics built in'],
];
scene(B(72), B(88), (R, S) => {
  S.head = div('abs', R); S.head.style.width = '1500px';
  S.head.innerHTML = '<div class="row" style="width:1500px"><div style="text-align:right;font:600 34px var(--zh);color:rgba(220,236,242,0.55)">传统统计软件<div style="font:700 15px var(--en);letter-spacing:6px;margin-top:6px">TRADITIONAL SOFTWARE</div></div><div style="text-align:center;font:300 40px var(--en);color:var(--dim)">vs</div><div style="font:700 40px var(--en)">MedStat <span style="color:var(--teal)">Pilot</span><div style="font:700 15px var(--en);letter-spacing:6px;margin-top:6px;color:var(--teal)">A NEW WAY TO WORK</div></div></div>';
  S.rows = CMP.map(([lz, le, rz, re]) => {
    const r = div('abs', R); r.style.width = '1500px';
    r.innerHTML = `<div class="row" style="width:1500px"><div style="text-align:right;color:rgba(220,236,242,0.5)"><div style="font:500 28px var(--zh)">${lz} <span style="color:rgba(255,107,125,0.75);margin-left:8px">✕</span></div><div style="font:500 15px var(--en);letter-spacing:1px;margin-top:4px">${le}</div></div><div style="text-align:center;font:300 34px var(--en);color:var(--teal)">→</div><div><div style="font:600 30px var(--zh)"><span style="color:var(--teal);margin-right:10px">✓</span>${rz}</div><div style="font:500 16px var(--en);letter-spacing:1px;color:var(--dim);margin-top:4px">${re}</div></div></div>`;
    return r;
  });
  S.plat = textEl(R, '<div style="display:flex;gap:30px;align-items:center"><span class="chip" style="font-size:30px;padding:18px 34px">macOS · Apple silicon</span><span class="chip" style="font-size:30px;padding:18px 34px">Windows · x64</span><span class="chip" style="font-size:30px;padding:18px 34px">中文 / English</span></div>', { whiteSpace: 'nowrap' });
}, (S, lt) => {
  const toPlat = eio(prog(lt, 27.6, 28.4));
  place(S.head, { y: lerp(-330, -500, toPlat), o: prog(lt, 0.2, 0.9) * (1 - toPlat) });
  S.rows.forEach((r, i) => {
    const a = ex(prog(lt, 4 + i * 4, 4.6 + i * 4));
    const glow = Math.exp(-Math.max(0, lt - (4 + i * 4)) * 1.2);
    place(r, { y: -190 + i * 92, x: (1 - a) * 80, o: a * (1 - toPlat) });
    r.style.filter = `drop-shadow(0 0 ${glow * 24}px rgba(46,230,197,${glow * 0.6}))`;
  });
  place(S.plat, { y: -40, s: lerp(0.85, 1, eback(prog(lt, 28.0, 28.7))), o: prog(lt, 28.0, 28.5) * (1 - prog(lt, 31.4, 32)) });
});

// 13. Finale: UI wall + kinetic tagline
const WALL = ['home', 'variables', 'preview', 'tool_compute_typed', 'tool_medical_bmi', 'tool_merge', 'workspace', 'tt_result', 'chat_done', 'km_plot', 'cox_plot', 'roc_plot', 'logit_plot', 'meta_plot', 'dca_plot', 'subgroup_plot', 'predict', 'air_studio', 'tool_export', 'tt_assign3', 'chart_雨云图', 'dl_dialog', 'tool_ai_encode', 'chat_consent'];
const WORDS = [['数据', 'DATA'], ['方法', 'METHODS'], ['结果', 'RESULTS'], ['解读', 'INSIGHT'], ['报告', 'REPORTS'], ['复现', 'REPRODUCIBILITY']];
scene(B(88), B(96), (R, S) => {
  S.wall = div('abs', R); Object.assign(S.wall.style, { width: '3000px', height: '3000px', transformStyle: 'preserve-3d' });
  S.tiles = [];
  for (let r = 0; r < 8; r++) for (let c = 0; c < 6; c++) {
    const f = WALL[(r * 6 + c * 5) % WALL.length];
    const t = div('', S.wall); Object.assign(t.style, { position: 'absolute', left: c * 500 + (r % 2) * 250 + 'px', top: r * 300 + 'px', width: '470px', height: '264px', borderRadius: '12px', overflow: 'hidden', boxShadow: '0 20px 50px rgba(0,0,0,0.5)' });
    const i = img(SH + f + '.png', t); Object.assign(i.style, { width: '100%', height: '100%', objectFit: 'cover', display: 'block' });
    S.tiles.push(t);
  }
  S.dim = div('', R); Object.assign(S.dim.style, { position: 'absolute', inset: 0, background: 'radial-gradient(ellipse at center, rgba(2,6,13,0.55), rgba(2,6,13,0.92) 70%)' });
  S.words = WORDS.map(([zh, en]) => textEl(R, `<div style="font:700 150px var(--zh);letter-spacing:20px;text-shadow:0 0 60px rgba(46,230,197,0.4)">${zh}</div><div style="font:700 24px var(--en);letter-spacing:14px;color:var(--teal);text-align:center;margin-top:8px">${en}</div>`, { whiteSpace: 'nowrap', textAlign: 'center' }));
  S.tag = textEl(R, '<div style="font:700 110px var(--en);white-space:nowrap">MedStat <span style="color:var(--teal)">Pilot</span></div><div style="font:500 44px var(--zh);letter-spacing:12px;margin-top:18px;text-align:center">从数据，到发现</div><div style="font:600 22px var(--en);letter-spacing:10px;color:var(--dim);margin-top:12px;text-align:center">FROM DATA TO DISCOVERY</div>', { textAlign: 'center' });
  S.flash = div('', R); Object.assign(S.flash.style, { position: 'absolute', inset: 0, background: 'radial-gradient(circle at 50% 45%, rgba(220,255,248,0.9), rgba(46,230,197,0.25) 30%, rgba(2,6,13,0) 60%)' });
}, (S, lt, d) => {
  place(S.wall, { y: 300 - lt * 60, x: -100, rx: 52, rz: -20, z: -500 + lt * 20, o: prog(lt, 0, 0.6) * (1 - prog(lt, 14.6, 15.6)) });
  S.dim.style.opacity = 1;
  S.words.forEach((W, i) => { const t0 = 0.0 + i * 1.0; const a = fade(lt, t0, t0 + 1.0, 0.18); place(W, { y: -40, s: lerp(1.25, 1, ex(prog(lt, t0, t0 + 0.5))), o: a }); });
  place(S.tag, { y: -40, s: lerp(0.9, 1, ex(prog(lt, 7.6, 8.6))) + prog(lt, 8.6, 16) * 0.04, o: prog(lt, 7.6, 8.3) * (1 - prog(lt, 15.0, 16)) });
  S.flash.style.opacity = Math.max(Math.exp(-Math.max(0, lt - 6.0) * 4) * prog(lt, 5.9, 6.0), prog(lt, 15.3, 16) * 0.9);
});

// 14. End card: logo + motto + developer
scene(B(96), DUR, (R, S) => {
  S.icon = img(AS + 'icon.png', R, 'abs'); S.icon.style.width = '190px';
  S.name = textEl(R, 'MedStat <span style="color:var(--teal)">Pilot</span>', { font: '700 84px var(--en)', whiteSpace: 'nowrap' });
  S.kick = textEl(R, '医学科研统计工作台 &nbsp;·&nbsp; <span style="font:700 17px var(--en);letter-spacing:7px;color:var(--teal)">RESEARCH STATISTICS WORKBENCH</span>', { font: '500 24px var(--zh)', letterSpacing: '6px', whiteSpace: 'nowrap' });
  S.rule1 = div('abs', R); Object.assign(S.rule1.style, { width: '860px', height: '1px', background: 'linear-gradient(90deg, rgba(46,230,197,0), rgba(46,230,197,0.6), rgba(46,230,197,0))' });
  S.motto = textEl(R, '<div style="font:500 40px var(--zh);letter-spacing:4px">把繁琐交给 AI，把时间还给研究者——</div><div style="font:600 40px var(--zh);letter-spacing:4px;margin-top:14px;color:var(--teal)">去想清楚一个真正的科学问题。</div><div style="font:400 23px var(--en);color:var(--dim);margin-top:22px;letter-spacing:0.5px">Hand the tedium to AI. Give researchers their time back — to think through the questions that truly matter.</div>', { textAlign: 'center', whiteSpace: 'nowrap' });
  S.rule2 = div('abs', R); Object.assign(S.rule2.style, { width: '1300px', height: '1px', background: 'rgba(220,236,242,0.16)' });
  const col = (lab, en, val, sub) => `<div style="text-align:center;padding:0 46px"><div style="font:600 14px var(--en);letter-spacing:5px;color:var(--teal)">${en}</div><div style="font:500 18px var(--zh);color:var(--dim);margin-top:6px">${lab}</div><div style="font:600 26px var(--zh);margin-top:10px">${val}</div>${sub ? `<div style="font:400 19px var(--en);color:var(--dim);margin-top:6px">${sub}</div>` : ''}</div>`;
  S.info = textEl(R, `<div style="display:flex;align-items:flex-start">${col('开发者', 'DEVELOPER', '陈亮亮', 'blingblingchen@126.com')}<div style="width:1px;align-self:stretch;background:rgba(220,236,242,0.18)"></div>${col('微信公众号', 'WECHAT', '科研牛马研习社', 'Official account')}<div style="width:1px;align-self:stretch;background:rgba(220,236,242,0.18)"></div>${col('开源主页', 'GITHUB', '<span style="font-family:var(--en)">CalebChen941028</span>', 'github.com/CalebChen941028')}</div>`, { whiteSpace: 'nowrap' });
  S.chips = textEl(R, '<span class="chip" style="font-size:17px;padding:8px 18px">macOS · Apple silicon</span>&nbsp;&nbsp;<span class="chip" style="font-size:17px;padding:8px 18px">Windows · x64</span>&nbsp;&nbsp;<span class="chip" style="font-size:17px;padding:8px 18px;border-color:var(--amber);color:var(--amber)">Beta</span>', { whiteSpace: 'nowrap' });
}, (S, lt) => {
  const a = (t0, t1) => prog(lt, t0, t1);
  place(S.icon, { y: -372, s: lerp(0.6, 1, eback(a(0.1, 0.8))), o: a(0.1, 0.5) });
  place(S.name, { y: -238 + (1 - eo(a(0.4, 1.2))) * 24, o: a(0.4, 1.0) });
  place(S.kick, { y: -170, o: a(0.8, 1.4) });
  place(S.rule1, { y: -118, s: eo(a(1.0, 1.8)), o: a(1.0, 1.4) });
  place(S.motto, { y: -6, o: a(1.6, 2.4) });
  place(S.rule2, { y: 138, s: eo(a(2.6, 3.4)), o: a(2.6, 3.0) });
  place(S.info, { y: 236, o: a(3.0, 3.8) });
  place(S.chips, { y: 354, o: a(3.6, 4.3) });
});

// ---------- chapters ----------
const CHAPTERS = [
  [B(7), B(16), '01', '数据', 'DATA'], [B(16), B(24), '02', '工具箱', 'TOOLBOX'], [B(24), B(36), '03', '分析', 'ANALYSIS'],
  [B(36), B(47), '04', 'AI 解读', 'AI INSIGHT'], [B(47), B(56), '05', '方法全景', 'METHODS'], [B(56), B(72), '06', '产出与导出', 'OUTPUTS'], [B(72), B(88), '07', '创新', 'WHAT IS NEW'],
];
const CH_FADE = 0.35;
const ONSCREEN = new Set(['tagline', 'motto']); // spoken lines already typeset in the scene

// ---------- engine ----------
const scenesEl = document.getElementById('scenes');
for (const sc of SCENES) { sc.root = div('scene', scenesEl); sc.S = {}; sc.init(sc.root, sc.S); }
const chapter = document.getElementById('chapter');
const capzh = document.getElementById('capzh'), capen = document.getElementById('capen'), capband = document.getElementById('capband');
const glowA = document.getElementById('glowA'), glowB = document.getElementById('glowB'), gridEl = document.getElementById('grid'), pulseEl = document.getElementById('pulse'), fadeEl = document.getElementById('fade');
const CHORUS = [[B(24), B(40)], [B(56), B(96)]];
const XF = 0.28;
function renderFrame(t) {
  for (const sc of SCENES) {
    const vis = t >= sc.s - XF && t < sc.e + XF;
    sc.root.style.display = vis ? 'block' : 'none';
    if (!vis) continue;
    const a = Math.min(sc.s === 0 ? 1 : prog(t, sc.s - XF, sc.s + XF * 0.4), sc.e >= DUR ? 1 : 1 - prog(t, sc.e - XF * 0.4, sc.e + XF));
    sc.root.style.opacity = a;
    sc.update(sc.S, t - sc.s, sc.e - sc.s, t);
  }
  // background motion
  place(glowA, { x: Math.sin(t * 0.11) * 400 - 200, y: Math.cos(t * 0.07) * 200 - 100 });
  place(glowB, { x: Math.cos(t * 0.09) * 500 + 300, y: Math.sin(t * 0.06) * 260 + 120 });
  gridEl.style.transform = `translate(${-(t * 8) % 40}px, ${-(t * 4) % 40}px)`;
  const inCh = CHORUS.some(([a, b]) => t >= a && t < b);
  const ph = ((t - G) % 0.5 + 0.5) % 0.5;
  pulseEl.style.opacity = inCh ? Math.exp(-ph * 9) * 0.9 : 0;
  // chapter label
  const ch = CHAPTERS.find(([a, b]) => t >= a && t < b);
  if (ch) {
    chapter.querySelector('b').textContent = ch[2]; chapter.querySelector('.z').textContent = ch[3]; chapter.querySelector('.e').textContent = ch[4];
    chapter.style.opacity = Math.min(prog(t, ch[0] + 0.2, ch[0] + 0.7), 1 - prog(t, ch[1] - CH_FADE, ch[1]));
  } else chapter.style.opacity = 0;
  // captions from the voice-over timing
  const c = VO.find((v) => !ONSCREEN.has(v.id) && t >= v.s - 0.1 && t < v.e + 0.45);
  if (c) {
    const a = Math.min(prog(t, c.s - 0.1, c.s + 0.2), 1 - prog(t, c.e + 0.15, c.e + 0.45));
    capzh.textContent = c.zh; capen.textContent = c.en;
    capzh.style.opacity = capen.style.opacity = a; capband.style.opacity = a;
    const rise = (1 - eo(prog(t, c.s - 0.1, c.s + 0.35))) * 10;
    capzh.style.transform = capen.style.transform = `translateY(${rise}px)`;
  } else { capzh.style.opacity = capen.style.opacity = 0; capband.style.opacity = 0; }
  fadeEl.style.opacity = Math.max(1 - prog(t, 0, 0.9), prog(t, DUR - 2.6, DUR));
}
window.renderFrame = renderFrame;
window.ready = (async () => {
  await document.fonts.ready;
  await Promise.all(IMGS.map((i) => (i.complete ? Promise.resolve() : new Promise((r) => { i.onload = i.onerror = r; }))));
  await Promise.all(IMGS.map((i) => i.decode().catch(() => {})));
  renderFrame(0);
  return IMGS.filter((i) => !i.naturalWidth).map((i) => i.src);
})();
