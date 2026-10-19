'use strict';
// Example storyboard (28 bars ≈ 56 s at 120 BPM) — style-agnostic: colours/fonts come from the style CSS
// (classes .h-display .h-zh .kicker .big-num .chip .card .muted .accent); motion from M.* (CONFIG.MOTION):
// M.win for windows/cards, M.text for any text block, M.pop for small items, M.focus for crop moves.
// Copy to scenes.js, then replace MEDIA/BRAND in config.js and the rects below with your measured ones.
// Each pattern here is production-tested (see examples/medstat-pilot/film.js for the 13-scene 3:26 film).
const B = bar, BR = CONFIG.BRAND, MD = CONFIG.MEDIA;
const nameHTML = `${BR.name} <span class="accent">${BR.nameAccent}</span>`;

// 1 · Cover — logo, name, positioning, platform chips; blurred real UI behind; pushes forward to exit.
scene(0, B(3), (R, S) => {
  S.back = win(R, { srcs: MD.ui, w: 1500 }); S.back.root.style.filter = 'blur(3px) saturate(0.85)';
  S.icon = img(BR.logo, R, 'abs'); S.icon.style.width = '250px';
  S.title = textEl(R, nameHTML, { whiteSpace: 'nowrap' }); S.title.className += ' h-display';
  S.sub = textEl(R, BR.positioningZh, { whiteSpace: 'nowrap' }); S.sub.className += ' h-zh';
  S.kick = textEl(R, BR.positioningEn, { whiteSpace: 'nowrap' }); S.kick.className += ' kicker';
  S.chips = textEl(R, BR.chips.map((c, i) => `<span class="chip${i === BR.chips.length - 1 ? ' accent' : ''}" style="margin:0 8px">${c}</span>`).join(''), { whiteSpace: 'nowrap' });
}, (S, lt, d) => {
  const push = eio(prog(lt, d - 0.9, d + 0.3)), z = 1 + push * 0.35, out = 1 - push;
  place(S.back.root, { z: -700, rx: 8 * MO.tilt, s: 1 + lt * 0.01, o: 0.28 * prog(lt, 0.2, 1.6) * out });
  place(S.icon, { ...M.pop(lt, 0.3, { y: -250, s: z }), o: prog(lt, 0.3, 0.9) * out });
  M.text(S.title, lt, 0.8, { y: -20, s: z, o: out });
  M.text(S.sub, lt, 1.3, { y: 100, s: z, o: out });
  M.text(S.kick, lt, 1.6, { y: 156, s: z, o: out });
  place(S.chips, { ...M.pop(lt, 2.2, { y: 260 }), o: prog(lt, 2.2, 2.8) * out });
});

// 2 · Feature walkthrough — ONE call; layout and animation follow the motion language (see patterns.js).
feature(B(3), B(8), {
  srcs: MD.ui, title: { zh: '一屏看懂结果', en: 'Results at a glance' },
  points: [
    { zh: '拖入变量即可分析', en: 'Drag variables in', rect: [300, 160, 600, 300] },
    { zh: '三线表自动生成', en: 'APA table, automatic', rect: [960, 160, 600, 300] },
    { zh: '图表与解读同屏', en: 'Figures + insight together', rect: [300, 500, 1560, 540] },
  ],
});

// 3 · Carousel — panels (tools, dialogs) flip in one per bar beside a menu that tracks the current one.
const PANELS = [['工具一', 'Tool one', [200, 160, 760, 520]], ['工具二', 'Tool two', [960, 160, 760, 520]]];
scene(B(8), B(10), (R, S) => {
  S.menu = div('abs', R); S.menu.style.width = '320px';
  S.items = PANELS.map(([zh, en]) => div('', S.menu, `<div style="font:600 30px var(--zh)">${zh}</div><div class="muted" style="font:600 14px var(--en);letter-spacing:4px">${en.toUpperCase()}</div>`));
  S.items.forEach((it) => Object.assign(it.style, { padding: '14px 0 14px 26px', borderLeft: '3px solid var(--faint)' }));
  S.cards = PANELS.map(([, , crop]) => win(R, { srcs: MD.ui, crop, w: 960, chrome: 'none', radius: 18 }));
}, (S, lt) => {
  const cur = clamp(Math.floor(lt / 2), 0, PANELS.length - 1);
  place(S.menu, { x: -660, o: prog(lt, 0, 0.5) });
  S.items.forEach((it, i) => { it.style.borderLeftColor = i === cur ? 'var(--accent)' : 'var(--faint)'; it.style.opacity = i === cur ? 1 : 0.4; });
  S.cards.forEach((C, i) => {
    const l = lt - i * 2, leave = i < PANELS.length - 1 ? eio(prog(l, 2.0, 2.45)) : 0;
    const e = M.enter(l, { x: 170 });
    place(C.root, { ...e, x: e.x - leave * 420, z: e.z - leave * 300, ry: (e.ry || 0) - leave * 30 * Math.max(MO.tilt, 0.3), o: l < 0 ? 0 : e.o * (1 - leave) });
  });
});

// 4 · Kinetic numbers — counters on the downbeat, labels, chips popping on half beats.
const CATS = ['领域一', '领域二', '领域三', '领域四', '领域五', '领域六', '领域七', '领域八'];
scene(B(10), B(12), (R, S) => {
  S.n1 = textEl(R, '', { whiteSpace: 'nowrap' }); S.n1.className += ' big-num';
  S.n2 = textEl(R, '', { whiteSpace: 'nowrap' }); S.n2.className += ' big-num accent';
  S.l1 = textEl(R, '研究领域 <span class="muted" style="font:700 16px var(--en);letter-spacing:6px">DOMAINS</span>', { font: '600 30px var(--zh)', whiteSpace: 'nowrap' });
  S.l2 = textEl(R, '统计方法 <span class="muted" style="font:700 16px var(--en);letter-spacing:6px">METHODS</span>', { font: '600 30px var(--zh)', whiteSpace: 'nowrap' });
  S.chips = CATS.map((c) => textEl(R, `<span class="chip">${c}</span>`, {}));
}, (S, lt) => {
  const c1 = Math.round(17 * eo(prog(lt, 0.2, 1.4))), c2 = Math.round(100 * eo(prog(lt, 0.6, 2.2)));
  S.n1.textContent = c1; S.n2.textContent = c2 + (c2 >= 100 ? '+' : '');
  place(S.n1, M.pop(lt, 0.1, { x: -300, y: -200 })); place(S.n2, M.pop(lt, 0.5, { x: 260, y: -200 }));
  M.text(S.l1, lt, 0.5, { x: -300, y: -60 }); M.text(S.l2, lt, 0.8, { x: 260, y: -60 });
  S.chips.forEach((C, i) => place(C, M.pop(lt, 1.6 + i * 0.25, { x: -540 + (i % 4) * 360, y: 90 + Math.floor(i / 4) * 80 })));
});

// 5 · Gallery — coverflow of result images, one per bar (name each in the voice-over on the cut).
scene(B(12), B(15), (R, S) => {
  S.cards = MD.plots.map((p) => pic(R, p, 900, 560));
}, (S, lt) => {
  const { dur, ease } = MO.focus;  // the motion language sets how fast/how the coverflow advances
  let c = 0; for (let i = 0; i < S.cards.length; i++) { const l = lt - i * 2; if (l >= 0) c = i - 1 + ease(prog(l, 0, Math.min(dur, 0.9))); }
  S.cards.forEach((el, i) => { const dd = i - c; place(el, { x: dd * 800, y: -10, z: -Math.abs(dd) * 520, ry: clamp(-dd * 40 * Math.max(MO.tilt, 0.35), -60, 60), s: lerp(1, 0.84, clamp(Math.abs(dd))), o: clamp(1 - Math.abs(dd) * 0.55) * (dd > 1.6 ? 0 : 1) }); });
});

// 6 · Video clip — a user-supplied screen recording inside the style's window frame, seeked frame-exactly.
scene(B(15), B(17), (R, S) => {
  S.W = win(R, { srcs: [{ video: MD.clip }], w: 1300 });
  S.t = tag(S.W, '真实录屏', 'Screen recording');
}, (S, lt, d) => {
  S.W.time(lt);                       // clip time = scene time (offset/scale it if needed)
  place(S.W.root, M.win(lt, d, { y: -10 }));
  posTag(S.W, S.t, 960, 120, fade(lt, 0.8, d, 0.3));
});

// 7 · Phone — a mobile screenshot in a device frame beside a headline.
scene(B(17), B(19), (R, S) => {
  S.P = win(R, { srcs: MD.phone.src, base: MD.phone.base, w: 360, chrome: 'phone' });
  S.head = textEl(R, '<div class="h-zh" style="letter-spacing:6px">移动端同样顺手</div><div class="kicker" style="margin-top:14px">ALSO ON YOUR PHONE</div>', { whiteSpace: 'nowrap' });
}, (S, lt, d) => {
  place(S.P.root, M.win(lt, d, { x: 360, ry: -12 * MO.tilt }));
  M.text(S.head, lt, 0.4, { x: -360 });
});

// 8 · What's different — two-column comparison, one row per bar.
const CMP = [['分散在多个软件', 'Scattered tools', '一个工作台', 'One workbench'], ['手工整理结果', 'Retyped by hand', '自动生成', 'Generated for you'], ['难以复现', 'Hard to reproduce', '可复现脚本', 'Reproducible script']];
scene(B(19), B(22), (R, S) => {
  S.rows = CMP.map(([lz, le, rz, re]) => textEl(R, `<div class="row" style="width:1400px"><div class="muted" style="text-align:right"><div style="font:500 30px var(--zh)">${lz} <span class="warn">✕</span></div><div style="font:500 15px var(--en)">${le}</div></div><div class="accent" style="text-align:center;font:300 34px var(--en)">→</div><div><div style="font:600 32px var(--zh)"><span class="accent">✓</span> ${rz}</div><div class="muted" style="font:500 16px var(--en)">${re}</div></div></div>`, { width: '1400px' }));
}, (S, lt) => {
  S.rows.forEach((r, i) => M.text(r, lt, 0.3 + i * 2, { y: -130 + i * 115 }));
});

// 9 · Finale — a tilted wall of the real screens with the tagline on top.
scene(B(22), B(25), (R, S) => {
  S.wall = div('abs', R); Object.assign(S.wall.style, { width: '3000px', height: '2400px', transformStyle: 'preserve-3d' });
  const srcs = [MD.ui, ...MD.plots];
  for (let r = 0; r < 7; r++) for (let c = 0; c < 6; c++) {
    const t = div('pic', S.wall); Object.assign(t.style, { position: 'absolute', left: c * 500 + (r % 2) * 250 + 'px', top: r * 320 + 'px', width: '470px', height: '284px' });
    Object.assign(img(srcs[(r * 6 + c) % srcs.length], t).style, { width: '100%', height: '100%', objectFit: 'cover' });
  }
  S.dim = div('', R); Object.assign(S.dim.style, { position: 'absolute', inset: 0, background: 'radial-gradient(ellipse at center, color-mix(in srgb, var(--bg-edge) 45%, transparent), var(--bg-edge) 75%)' });
  S.tag = textEl(R, `<div class="h-display" style="text-align:center">${nameHTML}</div><div class="h-zh" style="text-align:center;margin-top:16px">${BR.taglineZh}</div><div class="kicker" style="text-align:center;margin-top:12px">${BR.taglineEn}</div>`, { whiteSpace: 'nowrap' });
}, (S, lt, d) => {
  place(S.wall, { y: 300 - lt * 60, x: -100, rx: 52, rz: -20, z: -500 + lt * 20, o: prog(lt, 0, 0.6) * (1 - prog(lt, d - 0.8, d)) });
  M.text(S.tag, lt, 1.0, { y: -30, o: 1 - prog(lt, d - 0.6, d) });
});

// 10 · End card — centred and symmetric: logo · name · positioning · rule · motto · rule · contacts · chips.
scene(B(25), CONFIG.DUR, (R, S) => {
  S.icon = img(BR.logo, R, 'abs'); S.icon.style.width = '170px';
  S.name = textEl(R, nameHTML, { whiteSpace: 'nowrap', fontSize: '84px' }); S.name.className += ' h-display';
  S.kick = textEl(R, `<span class="h-zh" style="font-size:24px;letter-spacing:6px">${BR.positioningZh}</span> &nbsp;·&nbsp; <span class="kicker" style="font-size:16px">${BR.positioningEn}</span>`, { whiteSpace: 'nowrap' });
  S.rule1 = div('abs', R); Object.assign(S.rule1.style, { width: '860px', height: '1px', background: 'linear-gradient(90deg, transparent, var(--accent), transparent)' });
  S.motto = textEl(R, `<div style="font:500 40px var(--zh);letter-spacing:4px">${BR.motto[0]}</div><div class="accent" style="font:600 40px var(--zh);letter-spacing:4px;margin-top:12px">${BR.motto[1]}</div><div class="muted" style="font:400 23px var(--en);margin-top:18px">${BR.motto[2]}</div>`, { textAlign: 'center', whiteSpace: 'nowrap' });
  S.rule2 = div('abs', R); Object.assign(S.rule2.style, { width: '1300px', height: '1px', background: 'var(--faint)' });
  const col = ([en, zh, val, sub]) => `<div style="text-align:center;padding:0 46px"><div class="accent" style="font:600 14px var(--en);letter-spacing:5px">${en}</div><div class="muted" style="font:500 18px var(--zh);margin-top:6px">${zh}</div><div style="font:600 26px var(--zh);margin-top:8px">${val}</div><div class="muted" style="font:400 19px var(--en);margin-top:4px">${sub}</div></div>`;
  S.info = textEl(R, `<div style="display:flex">${BR.contacts.map(col).join('<div style="width:1px;align-self:stretch;background:var(--faint)"></div>')}</div>`, { whiteSpace: 'nowrap' });
  S.chips = textEl(R, BR.chips.map((c, i) => `<span class="chip${i === BR.chips.length - 1 ? ' accent' : ''}" style="font-size:17px;padding:8px 18px;margin:0 6px">${c}</span>`).join(''), { whiteSpace: 'nowrap' });
}, (S, lt) => {
  const a = (t0, t1) => prog(lt, t0, t1);
  place(S.icon, { ...M.pop(lt, 0.1, { y: -372 }) });
  M.text(S.name, lt, 0.4, { y: -238 });
  place(S.kick, { y: -170, o: a(0.8, 1.4) });
  place(S.rule1, { y: -118, s: eo(a(1.0, 1.8)), o: a(1.0, 1.4) });
  M.text(S.motto, lt, 1.6, { y: -6 });
  place(S.rule2, { y: 138, s: eo(a(2.6, 3.4)), o: a(2.6, 3.0) });
  M.text(S.info, lt, 3.0, { y: 236 });
  place(S.chips, { y: 354, o: a(3.6, 4.3) });
});
