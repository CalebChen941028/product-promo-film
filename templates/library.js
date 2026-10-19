'use strict';
// Scene library — every scene type as a function of (start, end, options). make_film.py writes scenes.js as a
// list of these calls from film.json, so an agent only supplies DATA. All text/media follow the visual style
// (CSS) and the motion language (M.*). Options are documented per type; unknown keys are ignored.
// Media paths are relative to film.html. Rects/crops are in the media's base coordinates (see intake.py).
const LIB = (() => {
  const BR = () => CONFIG.BRAND;
  const nameHTML = () => `${BR().name} <span class="accent">${BR().nameAccent || ''}</span>`;
  const chipsHTML = (list, size = 20) => (list || []).map((c, i, a) => `<span class="chip${i === a.length - 1 && /beta|preview|内测|新/i.test(c) ? ' accent' : ''}" style="font-size:${size}px;margin:0 7px">${c}</span>`).join('');

  // cover { media?, base? } — logo, name, positioning, platform chips; blurred real UI behind.
  function cover(start, end, o = {}) {
    scene(start, end, (R, S) => {
      if (o.media) { S.back = win(R, { srcs: o.media, base: o.base, w: 1500 }); S.back.root.style.filter = 'blur(3px) saturate(0.85)'; qaIgnore(S.back.root); }
      S.icon = img(BR().logo, R, 'abs'); S.icon.style.width = '250px';
      S.title = textEl(R, nameHTML(), { whiteSpace: 'nowrap' }); S.title.className += ' h-display';
      S.sub = textEl(R, BR().positioningZh || '', { whiteSpace: 'nowrap' }); S.sub.className += ' h-zh';
      S.kick = textEl(R, BR().positioningEn || '', { whiteSpace: 'nowrap' }); S.kick.className += ' kicker';
      S.chips = textEl(R, chipsHTML(BR().chips), { whiteSpace: 'nowrap' });
    }, (S, lt, d) => {
      const push = eio(prog(lt, d - 0.9, d + 0.3)), z = 1 + push * 0.35, out = 1 - push;
      if (S.back) place(S.back.root, { z: -700, rx: 8 * MO.tilt, s: 1 + lt * 0.01, o: 0.28 * prog(lt, 0.2, 1.6) * out });
      place(S.icon, { ...M.pop(lt, 0.3, { y: -250, s: z }), o: prog(lt, 0.3, 0.9) * out });
      M.text(S.title, lt, 0.8, { y: -20, s: z, o: out });
      M.text(S.sub, lt, 1.3, { y: 100, s: z, o: out });
      M.text(S.kick, lt, 1.6, { y: 156, s: z, o: out });
      place(S.chips, { ...M.pop(lt, 2.2, { y: 262 }), o: Math.min(prog(lt, 2.2, 2.8), out) });
    });
  }

  // pain { items?: [[zh, en], ...4] } — the old way: grey tool windows appear and tangle, then collapse.
  function pain(start, end, o = {}) {
    const items = o.items || [['表格清洗', 'Spreadsheet'], ['统计语法', 'Syntax'], ['单独作图', 'Plotting'], ['手工排版', 'Formatting']];
    const pos = [[-470, -250, -6], [470, -260, 5], [-470, 110, 4], [470, 100, -5]];
    scene(start, end, (R, S) => {
      S.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); S.svg.setAttribute('width', 1920); S.svg.setAttribute('height', 1080);
      Object.assign(S.svg.style, { position: 'absolute', left: 0, top: 0 }); R.appendChild(S.svg);
      S.lines = [[0, 1], [1, 2], [2, 3], [3, 0]].map(([a, b]) => { const l = document.createElementNS('http://www.w3.org/2000/svg', 'line'); l.setAttribute('stroke', 'var(--warn)'); l.setAttribute('stroke-width', 2.5); l.setAttribute('stroke-dasharray', '10 10'); S.svg.appendChild(l); return { l, a, b }; });
      S.wins = items.slice(0, 4).map(([zh, en], k) => {
        const w = div('abs card', R); w.dataset.qa = 'media'; Object.assign(w.style, { width: '400px', height: '250px', filter: 'grayscale(1)', overflow: 'hidden' });
        w.innerHTML = '<div style="height:28px;background:var(--faint)"></div>' + Array.from({ length: 6 }, (_, r) => `<div style="margin:14px 22px;height:12px;width:${40 + ((r * 37 + k * 13) % 50)}%;background:var(--faint);border-radius:6px"></div>`).join('');
        const lab = textEl(R, `<div style="font:600 30px var(--zh);letter-spacing:3px">${zh}</div><div class="muted" style="font:600 15px var(--en);letter-spacing:5px;margin-top:4px">${(en || '').toUpperCase()}</div>`, { textAlign: 'center', whiteSpace: 'nowrap' });
        return { w, lab };
      });
    }, (S, lt, d) => {
      const out = eio(prog(lt, d - 1.2, d)), k = 1 - out, step = (d - 1.6) / 4;
      S.wins.forEach((W, i) => {
        const a = prog(lt, 0.15 + i * step, 0.75 + i * step), [x, y, r] = pos[i];
        place(W.w, { ...M.pop(lt, 0.15 + i * step, { x: x * k, y: y * k, z: -out * 600, rz: r * k + out * 40, s: lerp(1, 0.2, out) }), o: clamp(a) * k });
        place(W.lab, { x: x * k, y: y * k + 168, o: prog(lt, 0.4 + i * step, 1.0 + i * step) * k });
      });
      S.lines.forEach(({ l, a, b }, j) => { const A = pos[a], Bp = pos[b]; l.setAttribute('x1', 960 + A[0]); l.setAttribute('y1', 540 + A[1]); l.setAttribute('x2', 960 + Bp[0]); l.setAttribute('y2', 540 + Bp[1]); l.setAttribute('opacity', prog(lt, 1.2 + j * 0.5, 1.6 + j * 0.5) * k); l.setAttribute('stroke-dashoffset', -lt * 40); });
    });
  }

  // feature { media, base?, title: {zh, en}, points: [{zh, en, rect, focus?}] (≤ 4) } — see patterns.js
  function featureScene(start, end, o) { feature(start, end, { srcs: o.media, base: o.base, title: o.title, points: o.points }); }

  // carousel { title?: {zh, en}, panels: [{zh, en, media, base?, crop?}] } — one panel per equal slice, menu tracks it.
  function carousel(start, end, o) {
    const P = o.panels || [];
    scene(start, end, (R, S) => {
      S.menu = div('abs', R); S.menu.style.width = '340px';
      if (o.title) S.head = textEl(R, `<div class="h-zh" style="font-size:28px;letter-spacing:4px">${o.title.zh}</div><div class="kicker" style="margin-top:8px;font-size:15px">${o.title.en || ''}</div>`, { width: '340px' });
      S.items = P.map((p) => { const it = div('', S.menu, `<div style="font:600 30px var(--zh)">${p.zh}</div><div class="muted" style="font:600 14px var(--en);letter-spacing:4px">${(p.en || '').toUpperCase()}</div>`); Object.assign(it.style, { padding: '14px 0 14px 26px', borderLeft: '3px solid var(--faint)' }); return it; });
      S.cards = P.map((p) => { const base = p.base || [1920, 1080], crop = p.crop || [0, 0, base[0], base[1]]; const w = Math.min(1000, (680 / crop[3]) * crop[2]); return win(R, { srcs: p.media, base, crop, w, chrome: 'none', radius: 18 }); });
    }, (S, lt, d) => {
      const n = Math.max(1, P.length), step = d / n, cur = clamp(Math.floor(lt / step), 0, n - 1);
      if (S.head) M.text(S.head, lt, 0, { x: -660, y: -330 });
      place(S.menu, { x: -660, y: 20, o: prog(lt, 0, 0.5) });
      S.items.forEach((it, i) => { it.style.borderLeftColor = i === cur ? 'var(--accent)' : 'var(--faint)'; it.style.opacity = i === cur ? 1 : 0.4; });
      S.cards.forEach((C, i) => {
        const l = lt - i * step, leave = i < n - 1 ? eio(prog(l, step, step + 0.45)) : 0, e = M.enter(l, { x: 170 });
        place(C.root, { ...e, x: e.x - leave * 420, z: e.z - leave * 300, ry: (e.ry || 0) - leave * 30 * Math.max(MO.tilt, 0.3), o: l < 0 ? 0 : e.o * (1 - leave) });
      });
    });
  }

  // numbers { stats: [{value, suffix?, zh, en}] (1–3), chips?: [..] } — counters on the downbeat, chips on half beats.
  function numbers(start, end, o) {
    const ST2 = o.stats || [];
    scene(start, end, (R, S) => {
      S.n = ST2.map((s, i) => { const e = textEl(R, '', { whiteSpace: 'nowrap' }); e.className += ' big-num' + (i === ST2.length - 1 ? ' accent' : ''); return e; });
      S.l = ST2.map((s) => textEl(R, `${s.zh} <span class="muted" style="font:700 16px var(--en);letter-spacing:6px">${(s.en || '').toUpperCase()}</span>`, { font: '600 30px var(--zh)', whiteSpace: 'nowrap' }));
      S.c = (o.chips || []).map((c) => textEl(R, `<span class="chip">${c}</span>`, { whiteSpace: 'nowrap' }));
    }, (S, lt) => {
      const n = ST2.length, gap = 560;
      ST2.forEach((s, i) => {
        const x = (i - (n - 1) / 2) * gap, v = Math.round(s.value * eo(prog(lt, 0.2 + i * 0.4, 1.6 + i * 0.4)));
        S.n[i].textContent = v + (v >= s.value ? s.suffix || '' : '');
        place(S.n[i], M.pop(lt, 0.1 + i * 0.4, { x, y: -200 })); M.text(S.l[i], lt, 0.5 + i * 0.3, { x, y: -60 });
      });
      const per = 4, cw = 1500 / per;
      S.c.forEach((C, i) => place(C, M.pop(lt, 1.6 + i * 0.25, { x: -750 + cw / 2 + (i % per) * cw, y: 90 + Math.floor(i / per) * 80 })));
    });
  }

  // gallery { items: [{media, zh?, en?}] } — coverflow, one item per equal slice (name each in the voice-over).
  function gallery(start, end, o) {
    const I = o.items || [];
    scene(start, end, (R, S) => {
      S.cards = I.map((it) => { const c = pic(R, it.media, 960, 600); if (it.zh) { const L = div('', c, `<div style="font:600 24px var(--zh)">${it.zh}</div><div style="font:700 13px var(--en);letter-spacing:4px;opacity:0.7;margin-top:2px">${(it.en || '').toUpperCase()}</div>`); Object.assign(L.style, { position: 'absolute', left: '22px', top: '18px', padding: '10px 18px', borderRadius: '12px', background: 'rgba(255,255,255,0.94)', color: '#1c2533' }); } return c; });
    }, (S, lt, d) => {
      const n = Math.max(1, I.length), step = d / n, { dur, ease } = MO.focus;
      let c = 0; for (let i = 0; i < n; i++) { const l = lt - i * step; if (l >= 0) c = i - 1 + ease(prog(l, 0, Math.min(dur, 0.9))); }
      S.cards.forEach((el, i) => { const dd = i - c; place(el, { x: dd * 820, y: 0, z: -Math.abs(dd) * 540, ry: clamp(-dd * 40 * Math.max(MO.tilt, 0.35), -60, 60), s: lerp(1, 0.84, clamp(Math.abs(dd))), o: clamp(1 - Math.abs(dd) * 0.55) * (dd > 1.6 ? 0 : 1) }); });
    });
  }

  // clip { media: '*.webm', base?, title?: {zh, en}, offset?: 0, rate?: 1 } — screen recording in the style's frame.
  function clipScene(start, end, o) {
    scene(start, end, (R, S) => {
      S.W = win(R, { srcs: [{ video: o.media }], base: o.base, w: 1300 });
      if (o.title) S.t = tag(S.W, o.title.zh, o.title.en);
    }, (S, lt, d) => {
      S.W.time((o.offset || 0) + lt * (o.rate || 1));
      place(S.W.root, M.win(lt, d, { y: 20 }));
      if (S.t) posTag(S.W, S.t, (o.base || [1920, 1080])[0] / 2, 60, fade(lt, 0.8, d, 0.3));
    });
  }

  // phone { media, base: [w,h] points, title: {zh, en} } — mobile screenshot in a device frame + headline.
  function phone(start, end, o) {
    scene(start, end, (R, S) => {
      S.P = win(R, { srcs: o.media, base: o.base || [393, 852], w: 360, chrome: 'phone' });
      S.head = textEl(R, `<div class="h-zh" style="letter-spacing:6px">${o.title?.zh || ''}</div><div class="kicker" style="margin-top:14px">${o.title?.en || ''}</div>`, { whiteSpace: 'nowrap' });
    }, (S, lt, d) => { place(S.P.root, M.win(lt, d, { x: 360, ry: -12 * MO.tilt })); M.text(S.head, lt, 0.4, { x: -360 }); });
  }

  // compare { rows: [[oldZh, oldEn, newZh, newEn]] (≤ 6), header?: {old: {zh,en}, new: {zh,en}} }
  function compare(start, end, o) {
    const rows = o.rows || [];
    scene(start, end, (R, S) => {
      const h = o.header || { old: { zh: '传统方式', en: 'THE OLD WAY' }, new: { zh: BR().name + ' ' + (BR().nameAccent || ''), en: 'A NEW WAY TO WORK' } };
      S.head = textEl(R, `<div class="row" style="width:1400px"><div class="muted" style="text-align:right;font:600 32px var(--zh)">${h.old.zh}<div style="font:700 14px var(--en);letter-spacing:6px;margin-top:6px">${h.old.en}</div></div><div class="muted" style="text-align:center;font:300 38px var(--en)">vs</div><div style="font:700 36px var(--display)">${h.new.zh}<div class="accent" style="font:700 14px var(--en);letter-spacing:6px;margin-top:6px">${h.new.en}</div></div></div>`, { width: '1400px' });
      S.rows = rows.map(([lz, le, rz, re]) => textEl(R, `<div class="row" style="width:1400px"><div class="muted" style="text-align:right"><div style="font:500 28px var(--zh)">${lz} <span class="warn">✕</span></div><div style="font:500 15px var(--en);margin-top:4px">${le}</div></div><div class="accent" style="text-align:center;font:300 34px var(--en)">→</div><div><div style="font:600 30px var(--zh)"><span class="accent">✓</span> ${rz}</div><div class="muted" style="font:500 16px var(--en);margin-top:4px">${re}</div></div></div>`, { width: '1400px' }));
    }, (S, lt, d) => {
      const n = Math.max(1, rows.length), step = (d - 0.6) / n, top = -((n - 1) * 92) / 2 + 40;
      M.text(S.head, lt, 0.1, { y: top - 140 });
      S.rows.forEach((r, i) => M.text(r, lt, 0.4 + i * step, { y: top + i * 92 }));
    });
  }

  // statement { zh, en } — one big line, centred (manifesto beat, chapter opener).
  function statement(start, end, o) {
    scene(start, end, (R, S) => { S.t = textEl(R, `<div class="h-zh" style="font-size:72px;letter-spacing:8px;text-align:center">${o.zh}</div><div class="kicker" style="text-align:center;margin-top:18px">${o.en || ''}</div>`, { whiteSpace: 'nowrap' }); },
      (S, lt, d) => M.text(S.t, lt, 0.2, { y: -40, o: 1 - prog(lt, d - 0.5, d) }));
  }

  // finale { media: [paths] } — tilted wall of real screens + name + tagline.
  function finale(start, end, o) {
    const srcs = o.media || [];
    scene(start, end, (R, S) => {
      S.wall = qaIgnore(div('abs', R)); Object.assign(S.wall.style, { width: '3000px', height: '2400px', transformStyle: 'preserve-3d' });
      for (let r = 0; r < 7; r++) for (let c = 0; c < 6; c++) {
        const t = div('pic', S.wall); Object.assign(t.style, { position: 'absolute', left: c * 500 + (r % 2) * 250 + 'px', top: r * 320 + 'px', width: '470px', height: '284px' });
        if (srcs.length) Object.assign(img(srcs[(r * 6 + c * 5) % srcs.length], t).style, { width: '100%', height: '100%', objectFit: 'cover' });
      }
      S.dim = qaIgnore(div('', R)); Object.assign(S.dim.style, { position: 'absolute', inset: 0, background: 'radial-gradient(ellipse at center, color-mix(in srgb, var(--bg-edge) 45%, transparent), var(--bg-edge) 75%)' });
      S.tag = textEl(R, `<div class="h-display" style="text-align:center">${nameHTML()}</div><div class="h-zh" style="text-align:center;margin-top:16px">${BR().taglineZh || ''}</div><div class="kicker" style="text-align:center;margin-top:12px">${BR().taglineEn || ''}</div>`, { whiteSpace: 'nowrap' });
    }, (S, lt, d) => {
      place(S.wall, { y: 300 - lt * 60, x: -100, rx: 52, rz: -20, z: -500 + lt * 20, o: prog(lt, 0, 0.6) * (1 - prog(lt, d - 0.8, d)) });
      M.text(S.tag, lt, 1.0, { y: -30, o: 1 - prog(lt, d - 0.6, d) });
    });
  }

  // endcard {} — centred and symmetric: logo · name · positioning · rule · motto · rule · contacts · chips.
  function endcard(start, end) {
    scene(start, end, (R, S) => {
      const b = BR();
      S.icon = img(b.logo, R, 'abs'); S.icon.style.width = '170px';
      S.name = textEl(R, nameHTML(), { whiteSpace: 'nowrap', fontSize: '84px' }); S.name.className += ' h-display';
      S.kick = textEl(R, `<span class="h-zh" style="font-size:24px;letter-spacing:6px">${b.positioningZh || ''}</span> &nbsp;·&nbsp; <span class="kicker" style="font-size:16px">${b.positioningEn || ''}</span>`, { whiteSpace: 'nowrap' });
      S.rule1 = div('abs', R); Object.assign(S.rule1.style, { width: '860px', height: '1px', background: 'linear-gradient(90deg, transparent, var(--accent), transparent)' });
      const m = b.motto || ['', '', ''];
      S.motto = textEl(R, `<div style="font:500 40px var(--zh);letter-spacing:4px">${m[0]}</div><div class="accent" style="font:600 40px var(--zh);letter-spacing:4px;margin-top:12px">${m[1]}</div><div class="muted" style="font:400 23px var(--en);margin-top:18px">${m[2]}</div>`, { textAlign: 'center', whiteSpace: 'nowrap' });
      S.rule2 = div('abs', R); Object.assign(S.rule2.style, { width: '1300px', height: '1px', background: 'var(--faint)' });
      const col = ([en, zh, val, sub]) => `<div style="text-align:center;padding:0 46px"><div class="accent" style="font:600 14px var(--en);letter-spacing:5px">${en}</div><div class="muted" style="font:500 18px var(--zh);margin-top:6px">${zh}</div><div style="font:600 26px var(--zh);margin-top:8px">${val}</div><div class="muted" style="font:400 19px var(--en);margin-top:4px">${sub || ''}</div></div>`;
      S.info = textEl(R, `<div style="display:flex">${(b.contacts || []).map(col).join('<div style="width:1px;align-self:stretch;background:var(--faint)"></div>')}</div>`, { whiteSpace: 'nowrap' });
      S.chips = textEl(R, chipsHTML(b.chips, 17), { whiteSpace: 'nowrap' });
    }, (S, lt) => {
      const a = (t0, t1) => prog(lt, t0, t1);
      place(S.icon, M.pop(lt, 0.1, { y: -372 }));
      M.text(S.name, lt, 0.4, { y: -238 });
      place(S.kick, { y: -170, o: a(0.8, 1.4) });
      place(S.rule1, { y: -118, s: eo(a(1.0, 1.8)), o: a(1.0, 1.4) });
      M.text(S.motto, lt, 1.6, { y: -6 });
      place(S.rule2, { y: 138, s: eo(a(2.6, 3.4)), o: a(2.6, 3.0) });
      M.text(S.info, lt, 3.0, { y: 236 });
      place(S.chips, { y: 354, o: a(3.6, 4.3) });
    });
  }

  return { cover, pain, feature: featureScene, carousel, numbers, gallery, clip: clipScene, phone, compare, statement, finale, endcard };
})();
