'use strict';
// Scene library — every scene type as a function of (start, end, options). make_film.py writes scenes.js as a
// list of these calls from film.json, so an agent only supplies DATA. All text/media follow the visual style
// (CSS) and the motion language (M.*). Options are documented per type; unknown keys are ignored.
// Media paths are relative to film.html. Rects/crops are in the media's base coordinates (see intake.py).
const LIB = (() => {
  const BR = () => CONFIG.BRAND;
  const nameHTML = () => `${BR().name} <span class="accent">${BR().nameAccent || ''}</span>`;
  const chipsHTML = (list, size = 20) => (list || []).map((c, i, a) => `<span class="chip${i === a.length - 1 && /beta|preview|内测|新/i.test(c) ? ' accent' : ''}" style="font-size:${size}px;margin:0 7px">${c}</span>`).join('');

  // cover { media?, base?, frame?: 'photo', open?: false, name?: false, focus?: [x,y,w,h] } — the hook first, then the name.
  // Cold open (default when there is media): the image plays full-bleed under the spoken hook and owns the first ~5 s
  // (a screen pushes into `focus`, a readable region); only then does the name arrive. "name": false keeps the whole
  // cover a cold open — the name lands at the hero and the end card (photo-led arcs).
  function cover(start, end, o = {}) {
    const base = o.base || [1920, 1080], named = o.name !== false;
    scene(start, end, (R, S) => {
      if (o.media && named) { S.back = win(R, { srcs: o.media, base: o.base, w: 1500, chrome: o.frame === 'photo' ? 'frame' : 'auto' }); S.back.root.style.filter = 'blur(3px) saturate(0.85)'; qaIgnore(S.back.root); }
      if (o.media && (o.open !== false || !named)) { S.full = backdrop(R, o.media, base); qaIgnore(S.full.root); }
      if (!named) return;
      S.icon = img(BR().logo, R, 'abs'); S.icon.style.width = '250px';
      S.title = textEl(R, nameHTML(), { whiteSpace: 'nowrap' }); S.title.className += ' h-display';
      S.sub = textEl(R, BR().positioningZh || '', { whiteSpace: 'nowrap' }); S.sub.className += ' h-zh';
      S.kick = textEl(R, BR().positioningEn || '', { whiteSpace: 'nowrap' }); S.kick.className += ' kicker';
      S.chips = textEl(R, chipsHTML(BR().chips), { whiteSpace: 'nowrap' });
    }, (S, lt, d) => {
      // H: the cold open. The name needs ~2.6 s to settle before the cover hands off, so the hook gets everything before that.
      const H = !S.full ? 0 : !named ? d + 1 : Math.max(Math.min(5.2, d - 3.3), Math.min(2.6, d * 0.38)), t = lt - Math.max(0, H - 0.7);
      const push = eio(prog(lt, d - 0.9, d + 0.3)), z = 1 + push * 0.35, out = 1 - push;
      if (S.full) {
        const f = fill169(base), k = named ? esoft(prog(lt, H - 0.7, H + 0.5)) : 0;
        if (o.focus && o.frame === 'photo') {   // a photograph: two beats — open on the subject, then the camera pulls back to reveal the place
          const tight = padTo169(o.focus, base, 1.0), drift = zoomIn(f, 1.04, 0.5, 0.5), reveal = esoft(prog(lt, 1.5, 3.4));
          setCrop(S.full, tight.map((v, j) => lerp(lerp(v, padTo169(o.focus, base, 0.92)[j], prog(lt, 0, 1.5)), lerp(f[j], drift[j], esoft(prog(lt, 3.4, d))), reveal)), 1920);
          S.full.root.style.filter = `brightness(${lerp(0.82, 1, esoft(prog(lt, 0, 2.4))).toFixed(3)})`;
        } else {
          const to = o.focus ? padTo169(o.focus, base, 1.0) : zoomIn(f, 1.06, 0.5, 0.5);
          const pushIn = o.focus ? esoft(prog(lt, 0.6, 2.2)) : esoft(prog(lt, 0, Math.min(H, d) + 0.5));   // a screen: a calm context frame, then into the readable region
          setCrop(S.full, f.map((v, j) => lerp(v, to[j], pushIn)), 1920);
        }
        place(S.full.root, { o: 1 - k });
        if (k > 0) S.full.root.style.filter = `blur(${(k * 8).toFixed(1)}px)`; else if (!(o.focus && o.frame === 'photo')) S.full.root.style.filter = '';
      }
      if (!named) return;
      if (S.back) place(S.back.root, { z: -700, rx: 8 * MO.tilt, s: 1 + lt * 0.01, o: 0.28 * prog(t, 0.2, 1.6) * out });
      place(S.icon, { ...M.pop(t, 0.3, { y: -250, s: z }), o: prog(t, 0.3, 0.9) * out });
      M.text(S.title, t, 0.8, { y: -20, s: z, o: out });
      M.text(S.sub, t, 1.3, { y: 100, s: z, o: out });
      M.text(S.kick, t, 1.6, { y: 156, s: z, o: out });
      place(S.chips, { ...M.pop(t, 2.2, { y: 262 }), o: Math.min(prog(t, 2.2, 2.8), out) });
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
  function featureScene(start, end, o) { feature(start, end, { srcs: o.media, base: o.base, title: o.title, points: o.points, chrome: o.frame === 'photo' ? 'frame' : o.frame }); }

  // carousel { title?: {zh, en}, panels: [{zh, en, media, base?, crop?}] } — one panel per equal slice, menu tracks it.
  function carousel(start, end, o) {
    const P = o.panels || [];
    if (layoutOf(o, ['menu', 'stack'], 'menu') === 'stack') return carouselStack(start, end, o);
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

  // carousel layout 'stack': no menu — panels land one per slice on a deck in the centre, the earlier ones step back
  // and up behind it; the current panel's name sits just above it (never in the caption band). Reads as "and this, and this" — breadth, calmly.
  function carouselStack(start, end, o) {
    const P = o.panels || [];
    scene(start, end, (R, S) => {
      if (o.title) S.head = textEl(R, `<div class="h-zh" style="font-size:30px;letter-spacing:4px;text-align:center">${o.title.zh}</div><div class="kicker" style="margin-top:8px;font-size:15px;text-align:center">${o.title.en || ''}</div>`, { whiteSpace: 'nowrap' });
      S.cards = P.map((p) => { const base = p.base || [1920, 1080], crop = p.crop || [0, 0, base[0], base[1]]; const w = Math.min(1180, (600 / crop[3]) * crop[2]); return win(R, { srcs: p.media, base, crop, w, chrome: 'none', radius: 18 }); });
      S.names = P.map((p) => textEl(R, `<span class="chip">${p.zh}${p.en ? ` <span class="muted" style="font:600 14px var(--en);letter-spacing:3px">${p.en.toUpperCase()}</span>` : ''}</span>`, { whiteSpace: 'nowrap' }));
    }, (S, lt, d) => {
      const n = Math.max(1, P.length), step = d / n, cur = clamp(Math.floor(lt / step), 0, n - 1);
      if (S.head) M.text(S.head, lt, 0, { y: -430 });
      S.cards.forEach((C, i) => {
        const l = lt - i * step, back = clamp((lt - (i + 1) * step) / step, 0, 3), e = M.enter(l, { y: 30 });
        const depth = i < cur ? cur - i : 0;
        place(C.root, { ...e, y: 30 + e.y - eio(clamp(back)) * 40 - depth * 34, z: e.z - depth * 160, s: (e.s || 1) * (1 - depth * 0.04), o: l < 0 ? 0 : Math.min(1, e.o * 2.5) * (depth > 2 ? 0 : depth === 2 ? 1 - eio(clamp(back - 1)) : 1) });
        // cards stay opaque (no ghost of the card behind); the ones that step back darken instead
        C.root.style.filter = back > 0 ? `brightness(${(1 - eio(clamp(back / 2)) * 0.6).toFixed(3)})` : '';
      });
      S.names.forEach((el, i) => M.text(el, lt, i * step + 0.3, { y: 30 - (S.cards[i].h || 600) / 2 - 46, z: 40, o: i === cur ? 1 - prog(lt, (i + 1) * step - 0.25, (i + 1) * step) : 0 }));
    });
  }

  // numbers { stats: [{value, suffix?, zh, en}] (1–3), chips?: [..], count?: false } — true values arrive on the downbeat (count: true = blurred count-up), chips on half beats.
  function numbers(start, end, o) {
    const ST2 = o.stats || [];
    scene(start, end, (R, S) => {
      S.n = ST2.map((s, i) => { const e = textEl(R, '', { whiteSpace: 'nowrap' }); e.className += ' big-num' + (i === ST2.length - 1 ? ' accent' : ''); return e; });
      S.l = ST2.map((s) => textEl(R, `${s.zh} <span class="muted" style="font:700 16px var(--en);letter-spacing:6px">${(s.en || '').toUpperCase()}</span>`, { font: '600 30px var(--zh)', whiteSpace: 'nowrap' }));
      S.c = (o.chips || []).map((c) => textEl(R, `<span class="chip">${c}</span>`, { whiteSpace: 'nowrap' }));
    }, (S, lt) => {
      const n = ST2.length, gap = 560;
      ST2.forEach((s, i) => {
        // Honest numbers: by default the TRUE value is the only value ever on screen (it arrives, it does not count),
        // so no frame, poster or still can show a number the product never claimed. "count": true opts into a
        // count-up, and then the in-between digits are blurred and dimmed until the final value lands.
        const x = (i - (n - 1) / 2) * gap, a = prog(lt, 0.2 + i * 0.4, 1.6 + i * 0.4);
        const counting = o.count && a < 1;
        S.n[i].textContent = (o.count ? Math.round(s.value * eo(a)) : s.value) + (counting ? '' : s.suffix || '');
        place(S.n[i], M.pop(lt, 0.1 + i * 0.4, { x, y: -200 }));
        if (counting) { S.n[i].style.filter = 'blur(22px)'; S.n[i].style.opacity = Math.min(+S.n[i].style.opacity, 0.22); } else S.n[i].style.filter = '';
        M.text(S.l[i], lt, 0.5 + i * 0.3, { x, y: -60 });
      });
      const per = 4, cw = 1500 / per;
      S.c.forEach((C, i) => place(C, M.pop(lt, 1.6 + i * 0.25, { x: -750 + cw / 2 + (i % per) * cw, y: 90 + Math.floor(i / per) * 80 })));
    });
  }

  // gallery { items: [{media, zh?, en?}], layout?: 'coverflow'|'grid'|'strip' } — one item per equal slice (name each in the voice-over).
  //   coverflow: the current item centre, its neighbours turned away · grid: all items on a calm grid, the current one
  //   lifts forward and the rest dim · strip: a film strip that slides left, the current frame large in the middle
  function gallery(start, end, o) {
    const I = o.items || [], lay = layoutOf(o, ['coverflow', 'grid', 'strip'], 'coverflow');
    const label = (c, it) => { if (!it.zh) return; const L = div('', c, `<div style="font:600 24px var(--zh)">${it.zh}</div><div style="font:700 13px var(--en);letter-spacing:4px;opacity:0.7;margin-top:2px">${(it.en || '').toUpperCase()}</div>`); Object.assign(L.style, { position: 'absolute', left: '22px', top: '18px', padding: '10px 18px', borderRadius: '12px', background: 'rgba(255,255,255,0.94)', color: '#1c2533' }); };
    const n = Math.max(1, I.length), cols = n <= 2 ? n : n <= 4 ? 2 : 3, rows = Math.ceil(n / cols);
    const cw = lay === 'grid' ? Math.min(760, 1640 / cols - 40) : lay === 'strip' ? 880 : 960, chh = cw * 0.625;
    scene(start, end, (R, S) => { S.cards = I.map((it) => { const c = pic(R, it.media, cw, chh); label(c, it); return c; }); }, (S, lt, d) => {
      const step = d / n, { dur, ease } = MO.focus;
      let c = 0; for (let i = 0; i < n; i++) { const l = lt - i * step; if (l >= 0) c = i - 1 + ease(prog(l, 0, Math.min(dur, 0.9))); }
      const cur = Math.round(clamp(c, 0, n - 1));
      S.cards.forEach((el, i) => {
        const dd = i - c;
        if (lay === 'grid') {
          const gx = (i % cols - (cols - 1) / 2) * (cw + 40), gy = (Math.floor(i / cols) - (rows - 1) / 2) * (chh + 40) + 30;
          const on = i === cur ? 1 : 0, e = M.pop(lt, i * Math.min(step, 0.5) * 0.6, { x: gx, y: gy });
          place(el, { ...e, z: on * 120, s: (e.s || 1) * (1 + on * 0.06), o: (e.o ?? 1) * (on ? 1 : 0.55) });
        } else if (lay === 'strip') {
          place(el, { x: dd * (cw + 60), y: 20, s: lerp(1.08, 0.78, clamp(Math.abs(dd))), o: clamp(1.25 - Math.abs(dd) * 0.45) * (Math.abs(dd) > 2.2 ? 0 : 1) });
        } else {
          place(el, { x: dd * 820, y: 0, z: -Math.abs(dd) * 540, ry: clamp(-dd * 40 * Math.max(MO.tilt, 0.35), -60, 60), s: lerp(1, 0.84, clamp(Math.abs(dd))), o: clamp(1 - Math.abs(dd) * 0.55) * (dd > 1.6 ? 0 : 1) });
        }
      });
    });
  }

  // clip { media: '*.webm', base?, title?: {zh, en}, offset?: 0, rate?: 1 } — screen recording in the style's frame.
  function clipScene(start, end, o) {
    scene(start, end, (R, S) => {
      S.ownVideo = true;   // it seeks its own clip (offset, rate)
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
  // Screen-led hero treatments (finale "hero": "result" | "rise" | "stack"): real outputs carry the hero moment, then
  // settle up and back so the name and tagline land beneath them. One move each; light comes from the window glint.
  //   result  one real result screen, near full-bleed, slow push            (software, finance: the work, done)
  //   rise    the one output that matters (o.image, optional o.crop) rises out of the blurred UI (o.backdrop)   (science)
  //   stack   up to 4 real outputs arrive one per beat in a calm cascade     (developer tools, apps: breadth of output)
  function screenHero(start, end, o) {
    const kind = o.hero, base = o.base || [1920, 1080];
    scene(start, end, (R, S) => {
      const bd = kind === 'rise' ? (o.backdrop || (o.media || [])[0]) : null;
      if (bd) { S.bd = backdrop(R, bd, o.backdropBase || [1920, 1080]); S.bd.root.style.filter = 'blur(10px) saturate(0.8)'; qaIgnore(S.bd.root); }
      const outs = kind === 'stack' ? (o.media || []).slice(0, 4) : [o.image || (o.media || [])[0]];
      S.group = qaIgnore(div('abs', R)); Object.assign(S.group.style, { width: '0px', height: '0px' });
      S.wins = outs.map((src, i) => {
        const W = win(S.group, { srcs: src, base: kind === 'stack' ? (o.bases || [])[i] || base : base, crop: kind === 'stack' ? (o.crops || [])[i] || undefined : o.crop,
          w: kind === 'result' ? 1560 : kind === 'rise' ? 1180 : 1000, chrome: kind === 'result' ? 'auto' : 'frame' });
        return W;
      });
      S.hmax = Math.max(...S.wins.map((W, i) => W.h + (kind === 'stack' ? (S.wins.length - 1) * 46 : 0)));   // settle so the outputs end above the line
      S.tag = textEl(R, `<div class="h-display" style="text-align:center">${nameHTML()}</div><div class="h-zh" style="text-align:center;margin-top:14px">${BR().taglineZh || ''}</div><div class="kicker" style="text-align:center;margin-top:10px">${BR().taglineEn || ''}</div>`, { whiteSpace: 'nowrap' });
    }, (S, lt, d) => {
      // staging: the music leaves a half-beat of silence before this downbeat; on it, ONE move — the output resolves
      // (sharpens, lifts) out of the hook's own screen. Then it holds alone (2–3 s, backdrop dimmed), then the name.
      const n = S.wins.length, per = kind === 'stack' ? Math.min(0.6, 1.6 / n) : 0, hold = Math.min(d * 0.55, 3.8);
      const settle = esoft(prog(lt, hold, hold + 1.1)), out = 1 - prog(lt, d - 0.7, d);
      if (S.bd) { place(S.bd.root, { o: lerp(0.7, 0.35, esoft(prog(lt, 0.2, 1.2))) * out }); const dim = ST.light ? 1 : lerp(1, 0.42, esoft(prog(lt, 0.2, 1.2)));   // a dark style: a light UI recedes into a dark texture, not a grey wash
        S.bd.root.style.filter = `blur(${lerp(2, 12, esoft(prog(lt, 0, 1.0))).toFixed(1)}px) saturate(0.8) brightness(${dim.toFixed(3)})`; }
      S.wins.forEach((W, i) => {
        const a = esoft(prog(lt, i * per, i * per + 0.9));
        const off = kind === 'stack' ? (i - (n - 1) / 2) : 0;
        place(W.root, { x: off * 70, y: off * 46 + lerp(kind === 'rise' ? 60 : 20, 0, a), z: kind === 'stack' ? i * 10 : 0,
          s: lerp(0.94, 1, a) * (kind === 'result' ? lerp(1, 1.025, esoft(prog(lt, 1, hold))) : 1), o: Math.min(1, a * 1.4) * out });
        W.root.style.filter = a < 1 ? `blur(${((1 - a) * 9).toFixed(1)}px)` : '';
      });
      place(S.group, { y: lerp(0, -175, settle), s: lerp(1, Math.min(0.72, 460 / S.hmax), settle) });
      M.text(S.tag, lt, hold + 0.5, { y: 290, o: out });
    });
  }

  function finale(start, end, o) {
    const srcs = o.media || [];
    if (['result', 'rise', 'stack'].includes(o.hero)) return screenHero(start, end, o);
    if (o.image) {   // bookend that transforms: the hook's photograph returns tight and dim; on the downbeat it pulls back to
      // the whole frame and lights up (detail → whole), holds alone for ~2.5 s, then the name and tagline arrive.
      const base = o.base || [1920, 1080], to = fill169(base), from = o.focus ? padTo169(o.focus, base, 1.0) : zoomIn(to, 1.6, 0.5, 0.55);
      scene(start, end, (R, S) => {
        S.W = backdrop(R, o.image, base); qaIgnore(S.W.root);
        S.dim = qaIgnore(div('', R)); Object.assign(S.dim.style, { position: 'absolute', inset: 0, background: 'linear-gradient(rgba(0,0,0,0.05) 40%, rgba(0,0,0,0.62) 92%)' });   // the product stays clear; the name sits in the lower third
        S.tag = textEl(R, `<div class="h-display" style="text-align:center;color:#fff">${BR().name} <span style="opacity:0.86">${BR().nameAccent || ''}</span></div><div class="h-zh" style="text-align:center;margin-top:16px;color:#fff">${BR().taglineZh || ''}</div><div style="text-align:center;margin-top:12px;font:500 22px var(--en);letter-spacing:5px;color:rgba(255,255,255,0.86)">${BR().taglineEn || ''}</div>`, { whiteSpace: 'nowrap' });
      }, (S, lt, d) => {
        const hold = Math.min(d * 0.5, 3.2);
        setCrop(S.W, from.map((v, j) => lerp(v, to[j], esoft(prog(lt, 0, 1.6)))), 1920);
        place(S.W.root, { o: prog(lt, 0, 0.4) * (1 - prog(lt, d - 0.8, d)) });
        S.W.root.style.filter = `brightness(${lerp(0.5, 1, esoft(prog(lt, 0.1, 1.8))).toFixed(3)})`;
        S.dim.style.opacity = prog(lt, hold, hold + 1.0) * (1 - prog(lt, d - 0.8, d));
        M.text(S.tag, lt, hold + 0.4, { y: 300, o: 1 - prog(lt, d - 0.6, d) });
      });
      return;
    }
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
      // the call to action (AIDA's A): one true next step from the docs — "申请内测 / Join the beta" — the last thing to arrive
      if (b.cta && (b.cta.zh || b.cta.en)) S.cta = textEl(R, `<span style="display:inline-block;padding:14px 34px;border-radius:999px;background:var(--accent);color:var(--bg-edge);font:700 24px var(--zh);letter-spacing:3px">${b.cta.zh || ''}${b.cta.en ? `<span style="font:700 15px var(--en);letter-spacing:3px;margin-left:14px;opacity:0.85">${b.cta.en.toUpperCase()}</span>` : ''}</span>`, { whiteSpace: 'nowrap' });
    }, (S, lt) => {
      const a = (t0, t1) => prog(lt, t0, t1);
      if (S.cta) { place(S.chips, { y: 418, o: a(3.6, 4.3) }); place(S.cta, M.pop(lt, 4.0, { y: 336 })); }
      place(S.icon, M.pop(lt, 0.1, { y: -372 }));
      M.text(S.name, lt, 0.4, { y: -238 });
      place(S.kick, { y: -170, o: a(0.8, 1.4) });
      place(S.rule1, { y: -118, s: eo(a(1.0, 1.8)), o: a(1.0, 1.4) });
      M.text(S.motto, lt, 1.6, { y: -6 });
      place(S.rule2, { y: 138, s: eo(a(2.6, 3.4)), o: a(2.6, 3.0) });
      M.text(S.info, lt, 3.0, { y: 236 });
      if (!S.cta) place(S.chips, { y: 354, o: a(3.6, 4.3) });
    });
  }

  // ---------- scenes for any product (photos, cut-outs, people, places) ----------
  const fill169 = (base) => { const [bw, bh] = base, w = Math.min(bw, bh * 16 / 9), h = w * 9 / 16; return [(bw - w) / 2, (bh - h) / 2, w, h]; };
  const zoomIn = (r, k, cx = 0.5, cy = 0.5) => { const w = r[2] / k, h = r[3] / k; return [r[0] + (r[2] - w) * cx, r[1] + (r[3] - h) * cy, w, h]; };
  const backdrop = (R, media, base) => { const W = win(R, { srcs: media, base, w: 1920, chrome: 'none', radius: 0 }); W.root.dataset.qa = 'backdrop'; W.root.style.boxShadow = 'none'; return W; };
  const SCRIM = { left: 'linear-gradient(90deg, rgba(0,0,0,0.62), rgba(0,0,0,0.25) 45%, rgba(0,0,0,0) 70%)', right: 'linear-gradient(270deg, rgba(0,0,0,0.62), rgba(0,0,0,0.25) 45%, rgba(0,0,0,0) 70%)',
    bottom: 'linear-gradient(rgba(0,0,0,0) 45%, rgba(0,0,0,0.55))', center: 'radial-gradient(ellipse at 50% 62%, rgba(0,0,0,0.55), rgba(0,0,0,0.18) 55%, rgba(0,0,0,0) 80%)' };
  const scrim = (R, side) => { const d = div('', R); Object.assign(d.style, { position: 'absolute', inset: 0, pointerEvents: 'none', background: SCRIM[side] || SCRIM.bottom }); return d; };
  const layoutOf = (o, allowed, dflt) => (allowed.includes(o.layout) ? o.layout : allowed.includes(SHOT.layout) ? SHOT.layout : dflt);
  // a product cut-out (transparent PNG) standing on the stage: soft contact shadow + faint floor reflection
  function cutout(R, src, w, h) {
    const root = div('abs', R); Object.assign(root.style, { width: w + 'px', height: h + 'px' }); root.dataset.qa = 'media';
    const sh = div('', root); Object.assign(sh.style, { position: 'absolute', left: '15%', right: '15%', bottom: '-4%', height: '9%', borderRadius: '50%',
      background: `radial-gradient(closest-side, rgba(0,0,0,${ST.light ? 0.28 : 0.6}), transparent)`, filter: 'blur(8px)' });
    const im = img(src, root); Object.assign(im.style, { position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain', filter: `drop-shadow(0 30px 40px rgba(0,0,0,${ST.light ? 0.18 : 0.45}))` });
    const rf = img(src, root); Object.assign(rf.style, { position: 'absolute', left: 0, top: '100%', width: '100%', height: '100%', objectFit: 'contain', transform: 'scaleY(-1)', opacity: ST.light ? 0.08 : 0.14,
      WebkitMaskImage: 'linear-gradient(rgba(0,0,0,0) 60%, rgba(0,0,0,1))', maskImage: 'linear-gradient(rgba(0,0,0,0) 60%, rgba(0,0,0,1))' });
    rf.dataset.qa = 'ignore';
    return { root, im };
  }

  // photo { media, base?, title?: {zh, en}, focus?: [x,y,w,h], side?|layout?: 'left'|'right'|'bottom'|'center'|'split' }
  //   left/right/bottom/center: full-bleed photograph, slow push-in, text on a scrim on that side
  //   split: the photograph as a tall card on the left 58 % (it drifts inside its frame), the line in clean space on the right
  function photo(start, end, o) {
    const base = o.base || [1920, 1080], from = fill169(base), to = o.focus || zoomIn(from, 1.12, 0.5, 0.45);
    const lay = layoutOf({ layout: o.side || o.layout }, ['left', 'right', 'bottom', 'center', 'split'], 'left');
    const titleHTML = (light) => `<div class="h-zh" style="${light ? 'color:#fff;text-shadow:0 4px 30px rgba(0,0,0,0.5);' : ''}font-size:52px;letter-spacing:8px">${o.title?.zh || ''}</div><div style="margin-top:14px;font:500 22px var(--en);letter-spacing:4px;${light ? 'color:rgba(255,255,255,0.86)' : ''}" class="${light ? '' : 'muted'}">${o.title?.en || ''}</div>`;
    if (lay === 'split') {
      const cw = 1040, ch = 860, aspect = cw / ch, k = Math.min(base[0], base[1] * aspect), cropW = k, cropH = k / aspect;
      const c0 = [(base[0] - cropW) / 2, (base[1] - cropH) / 2, cropW, cropH], c1 = zoomIn(c0, 1.1, 0.5, 0.45);
      scene(start, end, (R, S) => {
        S.W = win(R, { srcs: o.media, base, crop: c0, w: cw, chrome: 'none', radius: 18 }); S.W.root.dataset.qa = 'media';
        if (o.title) S.t = textEl(R, titleHTML(false), { width: '620px' });
      }, (S, lt, d) => {
        setCrop(S.W, c0.map((v, j) => lerp(v, c1[j], esoft(prog(lt, 0, d + ST.xf)))), cw);
        place(S.W.root, M.win(lt, d, { x: -960 + 96 + cw / 2, y: 0 }));
        if (S.t) M.text(S.t, lt, 0.6, { x: 960 - 96 - 310, y: 0 });
      });
      return;
    }
    scene(start, end, (R, S) => {
      S.W = backdrop(R, o.media, base);
      if (o.title) { S.scrim = scrim(R, lay); S.t = textEl(R, titleHTML(true), { width: '760px', textAlign: lay === 'center' ? 'center' : lay === 'right' ? 'right' : 'left' }); }
    }, (S, lt, d) => {
      const k = esoft(prog(lt, 0, d + ST.xf));
      setCrop(S.W, from.map((v, j) => lerp(v, to[j], k)), 1920); place(S.W.root, { o: 1 });
      if (S.t) {   // 120 px margin
        const pos = { left: { x: -960 + 120 + 380, y: 40 }, right: { x: 960 - 120 - 380, y: 40 }, bottom: { x: -960 + 120 + 380, y: 200 }, center: { x: 0, y: 220 } }[lay];
        M.text(S.t, lt, 0.6, pos); S.scrim.style.opacity = prog(lt, 0.2, 1.0);
      }
    });
  }

  // hero { media | [angles], base?, cutout?: bool, title: {zh, en}, kicker? } — the reveal: the product lights up, then breathes.
  function hero(start, end, o) {
    const srcs = [].concat(o.media || []);
    if (!o.cutout && srcs.length === 1) {   // one photograph: full bleed, it lights up while the camera eases in (no slide-like card)
      const base = o.base || [1920, 1080], from = fill169(base), to = zoomIn(from, 1.08, 0.5, 0.5);
      scene(start, end, (R, S) => {
        S.W = backdrop(R, srcs[0], base); S.scrim = scrim(R, 'left');
        S.t = textEl(R, `<div class="h-zh" style="color:#fff;font-size:60px;letter-spacing:10px;text-shadow:0 4px 30px rgba(0,0,0,0.5)">${o.title?.zh || ''}</div><div style="margin-top:14px;font:500 22px var(--en);letter-spacing:5px;color:rgba(255,255,255,0.86)">${o.title?.en || ''}</div>`, { width: '760px' });
      }, (S, lt, d) => {
        const on = esoft(prog(lt, 0.1, 1.6));
        setCrop(S.W, from.map((v, j) => lerp(v, to[j], esoft(prog(lt, 0, d + ST.xf)))), 1920); place(S.W.root, { o: 1 });
        S.W.root.style.filter = `brightness(${lerp(0.3, 1, on).toFixed(3)})`;
        S.scrim.style.opacity = prog(lt, 0.8, 1.6);
        M.text(S.t, lt, 1.0, { x: -960 + 120 + 380, y: 40 });   // 120 px margin, like photo()
      });
      return;
    }
    scene(start, end, (R, S) => {
      S.glow = div('', R); Object.assign(S.glow.style, { position: 'absolute', left: '50%', top: '52%', width: '1300px', height: '900px', margin: '-450px 0 0 -650px', borderRadius: '50%',
        background: `radial-gradient(closest-side, color-mix(in srgb, var(--accent) ${ST.light ? 10 : 16}%, transparent), transparent)`, filter: 'blur(20px)' });
      S.items = srcs.map((src) => (o.cutout ? cutout(R, src, 1000, 560) : (() => { const W = win(R, { srcs: src, base: o.base, w: 1100, chrome: 'frame' }); return { root: W.root, im: W.root }; })()));
      S.t = textEl(R, `<div class="h-zh" style="text-align:center">${o.title?.zh || ''}</div><div class="kicker" style="text-align:center;margin-top:12px">${o.title?.en || ''}</div>`, { whiteSpace: 'nowrap' });
    }, (S, lt, d) => {
      const on = esoft(prog(lt, 0.1, 1.4)), n = S.items.length, per = d / n;
      S.glow.style.opacity = on;
      S.items.forEach((it, i) => {
        const a = n === 1 ? 1 : clamp(1 - Math.abs((lt - per * i - per / 2) / (per * 0.62)) + 0.35);
        place(it.root, { y: o.cutout ? 20 : 30, s: lerp(0.94, 1, on) * (1 + 0.035 * prog(lt, 0, d)), ry: (o.cutout ? -4 + 8 * prog(lt, 0, d) : 0) * MO.tilt, o: clamp(a) * prog(lt, 0, 0.5) });
        it.im.style.filter = (o.cutout ? it.im.style.filter.replace(/ ?brightness\([^)]*\)/, '') : '') + ` brightness(${lerp(0.25, 1, on).toFixed(3)})`;
      });
      M.text(S.t, lt, 1.0, { y: -420 });
    });
  }

  // detail { media, base?, crops?: [{rect, zh?, en?}] (≤ 4) } — macro close-ups: texture before the whole (a tease).
  function detail(start, end, o) {
    const base = o.base || [1920, 1080], f = fill169(base);
    const C = (o.crops && o.crops.length ? o.crops : [{ rect: zoomIn(f, 2.6, 0.5, 0.45) }, { rect: zoomIn(f, 2.2, 0.25, 0.5) }, { rect: zoomIn(f, 2.2, 0.75, 0.55) }]).slice(0, 4);
    if (layoutOf(o, ['macro', 'split'], 'macro') === 'split') return detailSplit(start, end, o, base, C);
    scene(start, end, (R, S) => {
      S.layers = C.map(() => backdrop(R, o.media, base));
      S.labels = C.map((c) => (c.zh ? textEl(R, `<span class="chip">${c.zh}${c.en ? ` <span class="muted" style="font:500 15px var(--en)">${c.en}</span>` : ''}</span>`, { whiteSpace: 'nowrap' }) : null));
    }, (S, lt, d) => {
      const n = C.length, per = d / n;
      S.layers.forEach((W, i) => {
        const l = lt - i * per, inA = i === 0 ? 1 : prog(l, -0.25, 0.35), outA = i === n - 1 ? 1 : 1 - prog(l, per - 0.25, per + 0.35);
        const r = padTo169(C[i].rect, base, 1.0, 0.36), k = esoft(prog(l, -0.3, per + 0.4));   // 16:9 and at most ~2.8× — a strip or a button is never blown up
        setCrop(W, zoomIn(r, lerp(1, 1.1, k)), 1920); place(W.root, { o: clamp(Math.min(inA, outA)) });
        W.root.style.display = l > -0.3 && l < per + 0.4 ? 'block' : 'none';
        if (S.labels[i]) M.text(S.labels[i], l, 0.35, { x: -560, y: 300, o: clamp(Math.min(prog(l, 0.3, 0.7), 1 - prog(l, per - 0.3, per))) });
      });
    });
  }

  // detail layout 'split': the whole image small on the left with a box on the region, the region large on the right —
  // "here, and up close". The box travels to each crop in turn; the magnified view follows it.
  function detailSplit(start, end, o, base, C) {
    const sw = 700, bw = 960, R16 = C.map((c) => padTo169(c.rect, base, 1.0, 0.3));
    scene(start, end, (R, S) => {
      S.small = win(R, { srcs: o.media, base, w: sw, chrome: 'none', radius: 14 });
      S.box = div('', S.small.ov); Object.assign(S.box.style, { position: 'absolute', border: '3px solid var(--accent)', borderRadius: '8px', boxShadow: '0 0 0 9999px rgba(0,0,0,0.35)' });
      S.big = win(R, { srcs: o.media, base, crop: R16[0], w: bw, chrome: 'none', radius: 18 });
      S.labels = C.map((c) => (c.zh ? textEl(R, `<span class="chip">${c.zh}${c.en ? ` <span class="muted" style="font:500 15px var(--en)">${c.en}</span>` : ''}</span>`, { whiteSpace: 'nowrap' }) : null));
    }, (S, lt, d) => {
      const n = C.length, per = d / n, steps = R16.map((r, i) => [i * per + 0.6, r]);
      const r = M.focus(lt, [[0, R16[0]], ...steps]);
      setCrop(S.big, r, bw);
      const [x, y, w, h] = r, k = S.small.s;
      Object.assign(S.box.style, { left: `${(x - S.small.crop[0]) * k}px`, top: `${(y - S.small.crop[1]) * k}px`, width: `${w * k}px`, height: `${h * k}px`, opacity: prog(lt, 0.3, 0.8) });
      place(S.small.root, M.win(lt, d, { x: -960 + 96 + sw / 2, y: -20 }));
      place(S.big.root, M.win(lt - 0.25, d, { x: 960 - 96 - bw / 2, y: -20 }));
      S.labels.forEach((el, i) => { if (el) M.text(el, lt, i * per + 0.5, { x: 960 - 96 - bw / 2, y: 340, o: Math.min(prog(lt, i * per + 0.5, i * per + 0.9), 1 - prog(lt, (i + 1) * per - 0.3, (i + 1) * per)) }); });
    });
  }

  // lineup { items: [{media, zh?, en?}] (2–6), cutout?: bool, title?: {zh, en} } — the range, standing together.
  function lineup(start, end, o) {
    const I = (o.items || []).slice(0, 6), n = Math.max(1, I.length), bw = Math.min(380, 1560 / n), bh = 420;
    scene(start, end, (R, S) => {
      S.items = I.map((it) => (o.cutout ? cutout(R, it.media, bw - 30, bh) : { root: pic(R, it.media, bw - 30, bh) }));
      S.labels = I.map((it) => textEl(R, `<div style="font:600 26px var(--zh);text-align:center">${it.zh || ''}</div><div class="muted" style="font:500 15px var(--en);letter-spacing:3px;text-align:center;margin-top:6px">${(it.en || '').toUpperCase()}</div>`, { width: bw - 30 + 'px' }));
      if (o.title) S.t = textEl(R, `<div class="h-zh" style="text-align:center">${o.title.zh}</div><div class="kicker" style="text-align:center;margin-top:10px">${o.title.en || ''}</div>`, { whiteSpace: 'nowrap' });
    }, (S, lt, d) => {
      const drift = -20 + 40 * prog(lt, 0, d);
      I.forEach((_, i) => { const x = (i - (n - 1) / 2) * bw + drift; place(S.items[i].root, M.pop(lt, 0.3 + i * 0.22, { x, y: -10 })); M.text(S.labels[i], lt, 0.7 + i * 0.22, { x, y: 290 }); });
      if (S.t) M.text(S.t, lt, 0.1, { y: -400 });
    });
  }

  // quote { zh, en?, who, role? } — a REAL testimonial (with permission), large and quiet.
  function quote(start, end, o) {
    scene(start, end, (R, S) => {
      S.mark = textEl(R, '“', { font: '400 260px/1 var(--display)', color: 'var(--accent)', opacity: 0.35 }); S.mark.dataset.qa = 'ignore';
      S.q = textEl(R, `<div style="font:500 50px/1.45 var(--zh);letter-spacing:3px;text-align:center">${o.zh}</div>${o.en ? `<div class="muted" style="font:italic 400 27px/1.5 var(--en);text-align:center;margin-top:24px">${o.en}</div>` : ''}`, { width: '1300px' });
      S.who = textEl(R, `<div class="kicker" style="text-align:center">— ${o.who || ''}${o.role ? ` · ${o.role}` : ''}</div>`, { whiteSpace: 'nowrap' });
    }, (S, lt, d) => { place(S.mark, { x: -600, y: -300, o: prog(lt, 0.1, 0.8) * 0.35 }); M.text(S.q, lt, 0.3, { y: -40 }); M.text(S.who, lt, 1.4, { y: 230 }); });
  }

  // ---------- motion graphics: story built in code (no materials; never a fake product UI) ----------
  const svgEl = (tag, attrs = {}, parent) => { const e = document.createElementNS('http://www.w3.org/2000/svg', tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  const stageSVG = (R) => { const sv = svgEl('svg', { width: 1920, height: 1080, viewBox: '0 0 1920 1080' }); Object.assign(sv.style, { position: 'absolute', left: 0, top: 0, pointerEvents: 'none' }); R.appendChild(sv); return sv; };
  const emph = (s) => String(s || '').replace(/\*([^*]+)\*/g, '<span class="accent">$1</span>');

  // flow { steps: [{zh, en?}] (2–5) | "chapters", title?: {zh, en} } — the journey as a line of nodes: the line draws
  // itself, a light travels along it, each node lights up on its slice (say one step per line). "chapters" = the film's
  // own chapter names, so the map and the chapters always agree.
  function flow(start, end, o) {
    const ST_ = (o.steps || []).slice(0, 5), n = Math.max(1, ST_.length), span = Math.min(1500, 340 * n), x0 = 960 - span / 2, gap = n > 1 ? span / (n - 1) : 0, Y = 560;
    scene(start, end, (R, S) => {
      S.svg = stageSVG(R);
      S.track = svgEl('path', { d: `M${x0},${Y} L${x0 + span},${Y}`, fill: 'none', stroke: 'var(--faint)', 'stroke-width': 3 }, S.svg);
      S.line = svgEl('path', { d: `M${x0},${Y} L${x0 + span},${Y}`, fill: 'none', stroke: 'var(--accent)', 'stroke-width': 4, 'stroke-linecap': 'round' }, S.svg);
      S.dot = svgEl('circle', { r: 9, fill: 'var(--accent)' }, S.svg); S.dot.style.filter = 'drop-shadow(0 0 12px var(--accent))';
      S.nodes = ST_.map((st, i) => {
        const g = div('abs', R); g.dataset.qa = 'text';
        g.innerHTML = `<div style="width:84px;height:84px;border-radius:50%;margin:0 auto;display:flex;align-items:center;justify-content:center;font:700 30px var(--mono);border:3px solid var(--accent);background:var(--bg-edge)">${String(i + 1).padStart(2, '0')}</div>
          <div style="margin-top:22px;text-align:center;font:600 32px var(--zh);white-space:nowrap">${st.zh || ''}</div><div class="muted" style="margin-top:6px;text-align:center;font:600 15px var(--en);letter-spacing:4px;white-space:nowrap">${(st.en || '').toUpperCase()}</div>`;
        return g;
      });
      if (o.title) S.title = textEl(R, `<div class="h-zh" style="text-align:center;font-size:46px;letter-spacing:6px">${emph(o.title.zh)}</div><div class="kicker" style="text-align:center;margin-top:12px">${o.title.en || ''}</div>`, { whiteSpace: 'nowrap' });
    }, (S, lt, d) => {
      const t0 = 0.6, step = (d - t0 - 0.6) / n, T = ST_.map((_, i) => t0 + i * step), cur = T.reduce((c, ti, i) => (lt >= ti ? i : c), -1);
      if (S.title) M.text(S.title, lt, 0.1, { y: -300 });
      const reach = n > 1 ? clamp((lt - T[0]) / (T[n - 1] - T[0] + 1e-6)) : 1, len = span;
      S.line.setAttribute('stroke-dasharray', len); S.line.setAttribute('stroke-dashoffset', len * (1 - eio(reach)));
      S.dot.setAttribute('cx', x0 + span * eio(reach)); S.dot.setAttribute('cy', Y); S.dot.setAttribute('opacity', reach > 0 && reach < 1 ? 1 : 0);
      S.nodes.forEach((g, i) => { const on = i === cur, past = i < cur; place(g, { ...M.pop(lt, T[i] - 0.15, { x: x0 + i * gap - 960, y: Y - 540 + 70 }), s: on ? 1.08 : 1, o: lt < T[i] - 0.15 ? 0 : on ? 1 : past ? 0.75 : 0.35 }); });
    });
  }

  // hub { center?: {zh, en}, items: [{zh, en?}] (3–6), title? } — the scattered old way becomes one place: grey tools
  // drift apart, lines reach out from the hub, the tools glide into a calm ring and light up. "One workbench, not five tools."
  function hub(start, end, o) {
    const I = (o.items || []).slice(0, 6), n = Math.max(1, I.length), R0 = 330;
    const scatter = I.map((_, i) => { const a = (i / n) * Math.PI * 2 + 0.6; return [Math.cos(a) * 760 + Math.sin(i * 7.3) * 60, Math.sin(a) * 380 + Math.cos(i * 5.1) * 40, (i % 2 ? 1 : -1) * (6 + i * 2)]; });
    const ring = I.map((_, i) => { const a = (i / n) * Math.PI * 2 - Math.PI / 2; return [Math.cos(a) * R0 * 1.35, Math.sin(a) * R0]; });
    scene(start, end, (R, S) => {
      S.svg = stageSVG(R);
      S.lines = I.map(() => svgEl('line', { stroke: 'var(--accent)', 'stroke-width': 2, opacity: 0 }, S.svg));
      S.core = div('abs', R); S.core.dataset.qa = 'text';
      const c = o.center || { zh: CONFIG.BRAND?.name || '', en: '' };
      S.core.innerHTML = `<div style="width:260px;height:260px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;background:radial-gradient(circle, color-mix(in srgb, var(--accent) 22%, var(--bg-edge)), var(--bg-edge));box-shadow:0 0 80px color-mix(in srgb, var(--accent) 35%, transparent);border:2px solid var(--accent)">
        <div style="font:700 34px var(--zh);text-align:center;padding:0 20px">${c.zh || ''}</div><div class="muted" style="font:600 14px var(--en);letter-spacing:4px;margin-top:8px">${(c.en || '').toUpperCase()}</div></div>`;
      S.items = I.map((it) => { const e = textEl(R, `<span class="chip" style="font-size:24px;padding:14px 26px">${it.zh}${it.en ? ` <span class="muted" style="font:600 14px var(--en)">${it.en}</span>` : ''}</span>`, { whiteSpace: 'nowrap' }); return e; });
      if (o.title) S.title = textEl(R, `<div class="h-zh" style="text-align:center;font-size:44px;letter-spacing:6px">${emph(o.title.zh)}</div><div class="kicker" style="text-align:center;margin-top:12px">${o.title.en || ''}</div>`, { whiteSpace: 'nowrap' });
    }, (S, lt, d) => {
      const gather = esoft(prog(lt, d * 0.32, d * 0.62)), coreIn = prog(lt, d * 0.22, d * 0.4);
      if (S.title) M.text(S.title, lt, d * 0.55, { y: -440 });
      place(S.core, { ...M.pop(lt, d * 0.22, { y: 0 }), s: lerp(0.6, 1, eo(coreIn)) * (1 + 0.015 * Math.sin(lt * 2)) });
      S.items.forEach((el, i) => {
        const [sx, sy, sr] = scatter[i], [rx, ry] = ring[i], drift = (1 - gather) * Math.sin(lt * 0.9 + i) * 14;
        const x = lerp(sx, rx, gather), y = lerp(sy, ry, gather) + drift;
        place(el, { x, y, rz: lerp(sr, 0, gather), s: lerp(0.9, 1, gather), o: Math.min(prog(lt, i * 0.12, i * 0.12 + 0.5), 1) });
        el.style.filter = `grayscale(${(1 - gather).toFixed(2)})`; el.style.opacity = (+el.style.opacity * lerp(0.55, 1, gather)).toFixed(3);
        const ln = S.lines[i], a = prog(lt, d * 0.3 + i * 0.08, d * 0.6);
        ln.setAttribute('x1', 960); ln.setAttribute('y1', 540); ln.setAttribute('x2', 960 + x * a); ln.setAttribute('y2', 540 + y * a); ln.setAttribute('opacity', (a * 0.55).toFixed(3));
      });
    });
  }

  // type { lines: [{zh, en?}] (1–4) } — kinetic typography: one big line at a time rises through a mask, *word* in the
  // accent colour; earlier lines step back and dim. For a hook, a manifesto, a turn in the story.
  function type(start, end, o) {
    const Ls = (o.lines || []).slice(0, 4), n = Math.max(1, Ls.length);
    scene(start, end, (R, S) => {
      S.ls = Ls.map((l) => textEl(R, `<div class="h-zh" style="font-size:${n > 2 ? 64 : 76}px;letter-spacing:6px;text-align:center;white-space:nowrap">${emph(l.zh)}</div>${l.en ? `<div class="kicker" style="text-align:center;margin-top:16px">${emph(l.en)}</div>` : ''}`, { whiteSpace: 'nowrap' }));
    }, (S, lt, d) => {
      const step = (d - 0.4) / n, gapY = n > 2 ? 150 : 180, top = -((n - 1) * gapY) / 2;
      S.ls.forEach((el, i) => {
        const t0 = 0.3 + i * step, a = ex(prog(lt, t0, t0 + 0.6)), older = lt > t0 + step ? 1 : 0;
        el.style.clipPath = `inset(${((1 - a) * 100).toFixed(1)}% -10% -30% -10%)`;
        place(el, { y: top + i * gapY + (1 - a) * 50, s: older ? 0.94 : 1, o: lt < t0 ? 0 : older ? 0.42 : 1 });
      });
    });
  }

  // chart { kind?: 'bar'|'line', data: [{label, value}] (2–8), unit?, title?, source? } — real numbers from the user's
  // docs drawn on the beat. Bars grow (or the line draws) without in-between digits: each value appears only when its
  // bar has landed, so no frame shows a number the product never claimed.
  function chart(start, end, o) {
    const D = (o.data || []).slice(0, 8), n = Math.max(1, D.length), kind = o.kind === 'line' ? 'line' : 'bar';
    const W = Math.min(1400, 200 * n + 200), H = 520, X0 = 960 - W / 2, Y0 = 760, max = Math.max(...D.map((x) => +x.value || 0), 1);
    const px = (i) => X0 + (i + 0.5) * (W / n), py = (v) => Y0 - (v / max) * H;
    scene(start, end, (R, S) => {
      S.svg = stageSVG(R);
      svgEl('line', { x1: X0, y1: Y0, x2: X0 + W, y2: Y0, stroke: 'var(--faint)', 'stroke-width': 2 }, S.svg);
      if (kind === 'bar') S.bars = D.map((_, i) => svgEl('rect', { x: px(i) - Math.min(70, W / n * 0.32), width: Math.min(140, W / n * 0.64), rx: 8, fill: i === n - 1 ? 'var(--accent)' : 'color-mix(in srgb, var(--ink) 30%, transparent)' }, S.svg));
      else { S.path = svgEl('path', { d: D.map((x, i) => `${i ? 'L' : 'M'}${px(i)},${py(+x.value)}`).join(' '), fill: 'none', stroke: 'var(--accent)', 'stroke-width': 5, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }, S.svg); S.dots = D.map(() => svgEl('circle', { r: 9, fill: 'var(--accent)' }, S.svg)); }
      S.vals = D.map((x) => textEl(R, `<div style="font:700 34px var(--mono);text-align:center">${x.value}${o.unit || ''}</div>`, { whiteSpace: 'nowrap' }));
      S.labs = D.map((x) => textEl(R, `<div class="muted" style="font:600 22px var(--zh);text-align:center">${x.label}</div>`, { whiteSpace: 'nowrap' }));
      if (o.title) S.title = textEl(R, `<div class="h-zh" style="text-align:center;font-size:42px;letter-spacing:5px">${emph(o.title.zh)}</div><div class="kicker" style="text-align:center;margin-top:10px">${o.title.en || ''}</div>`, { whiteSpace: 'nowrap' });
      if (o.source) S.src = textEl(R, `<div class="muted" style="font:500 15px var(--en);letter-spacing:1px">${o.source}</div>`, { whiteSpace: 'nowrap' });
    }, (S, lt, d) => {
      const t0 = 0.6, step = Math.min(0.5, (d - 1.6) / n);
      if (S.title) M.text(S.title, lt, 0.1, { y: -430 });
      if (S.src) M.text(S.src, lt, 0.8, { x: X0 + W - 960 - 200, y: Y0 - 540 + 80 });
      D.forEach((x, i) => {
        const a = eio(prog(lt, t0 + i * step, t0 + i * step + 0.7)), v = +x.value || 0;
        if (S.bars) { const h = (v / max) * H * a; S.bars[i].setAttribute('y', Y0 - h); S.bars[i].setAttribute('height', Math.max(0, h)); }
        else { S.dots[i].setAttribute('cx', px(i)); S.dots[i].setAttribute('cy', py(v)); S.dots[i].setAttribute('opacity', a >= 0.99 ? 1 : 0); }
        M.text(S.labs[i], lt, t0 + i * step, { x: px(i) - 960, y: Y0 - 540 + 36 });
        place(S.vals[i], { x: px(i) - 960, y: py(v) - 540 - 34, o: a >= 0.99 ? prog(lt, t0 + i * step + 0.7, t0 + i * step + 0.9) : 0 });
      });
      if (S.path) { const L = S.path.getTotalLength ? S.path.getTotalLength() : 2000, a = eio(prog(lt, t0, t0 + n * step + 0.4)); S.path.setAttribute('stroke-dasharray', L); S.path.setAttribute('stroke-dashoffset', L * (1 - a)); }
    });
  }


  // mg { layers: [...] } — motion graphics designed in film.json, no code. Every layer has keyframes in BEATS from the
  // scene's start, so the motion lands on the music: "keys": [[beat, {x, y, s, sx, sy, rz, o, blur}], …] (x/y px from
  // the centre; a key may name its ease: [beat, {…}, "eback"]). Kinds:
  //   text    {zh, en?, size?, align?}  *word* in the accent     rect    {w, h, radius?, fill?, stroke?, width?}
  //   circle  {r, fill?, stroke?, width?, draw?: [b0, b1]}       line    {points: [[x, y], …], stroke?, width?, draw?}
  //   path    {d (SVG, stage px 0–1920 × 0–1080), stroke?, fill?, width?, draw?}
  //   number  {value, suffix?, zh?, en?, at: beat} — the true value appears on its beat, never counts through others
  //   image   {media (a real material), w, radius?}
  // Colours: "accent" | "accent2" | "ink" | "muted" | "faint" | "bg" | any CSS colour. draw: the stroke traces itself between two beats.
  function mg(start, end, o) {
    const B = CONFIG.BAR / 4, Ls = o.layers || [];
    const col = (c, d) => (!c ? d : ({ accent: 'var(--accent)', accent2: 'var(--accent2, var(--accent))', ink: 'var(--ink)', muted: 'color-mix(in srgb, var(--ink) 55%, transparent)', faint: 'var(--faint)', bg: 'var(--bg-edge)' })[c] || c);
    const keysOf = (L) => (L.keys && L.keys.length ? L.keys : [[0, { o: 0, y: 20 }], [1, { o: 1, y: 0 }]]).map(([b, v, e]) => [b * B, v, EASES[e] || EASES[L.ease] || eo]);
    scene(start, end, (R, S) => {
      S.svg = stageSVG(R);
      S.ls = Ls.map((L) => {
        const k = L.kind || 'text';
        if (k === 'text') return { L, el: textEl(R, `<div class="h-zh" style="font-size:${L.size || 64}px;letter-spacing:${Math.round((L.size || 64) / 12)}px;text-align:${L.align || 'center'};white-space:nowrap">${emph(L.zh)}</div>${L.en ? `<div class="kicker" style="text-align:${L.align || 'center'};margin-top:12px">${emph(L.en)}</div>` : ''}`, { whiteSpace: 'nowrap' }) };
        if (k === 'number') return { L, el: textEl(R, `<div class="big-num${L.accent === false ? '' : ' accent'}" style="text-align:center">${L.value}${L.suffix || ''}</div>${L.zh ? `<div style="font:600 28px var(--zh);text-align:center;margin-top:10px">${L.zh} <span class="muted" style="font:700 15px var(--en);letter-spacing:5px">${(L.en || '').toUpperCase()}</span></div>` : ''}`, { whiteSpace: 'nowrap' }) };
        if (k === 'rect') { const el = div('abs', R); Object.assign(el.style, { width: (L.w || 200) + 'px', height: (L.h || 6) + 'px', borderRadius: (L.radius || 0) + 'px', background: col(L.fill, L.stroke ? 'transparent' : 'var(--accent)'), border: L.stroke ? `${L.width || 2}px solid ${col(L.stroke)}` : 'none' }); return { L, el }; }
        if (k === 'image') { const el = div('abs pic', R); el.dataset.qa = 'media'; Object.assign(el.style, { width: (L.w || 600) + 'px', borderRadius: (L.radius ?? 14) + 'px', overflow: 'hidden', boxShadow: '0 30px 70px rgba(0,0,0,0.35)' }); const im = img(L.media, el); Object.assign(im.style, { width: '100%', display: 'block' }); return { L, el }; }
        const g = svgEl('g', {}, S.svg), attrs = { fill: col(L.fill, 'none'), stroke: col(L.stroke, k === 'circle' && L.fill ? 'none' : 'var(--accent)'), 'stroke-width': L.width || 3, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' };
        const sh = k === 'circle' ? svgEl('circle', { cx: 960, cy: 540, r: L.r || 100, ...attrs }, g)
          : k === 'line' ? svgEl('polyline', { points: (L.points || []).map(([x, y]) => `${960 + x},${540 + y}`).join(' '), ...attrs }, g)
          : svgEl('path', { d: L.d || '', ...attrs }, g);
        return { L, g, sh, svg: true };
      });
    }, (S, lt) => {
      S.ls.forEach(({ L, el, g, sh, svg }) => {
        const v = kf(lt, keysOf(L)), x = v.x || 0, y = v.y || 0, s = v.s ?? 1, o = v.o ?? 1, rz = v.rz || 0;
        if (svg) {
          g.setAttribute('transform', `translate(${960 + x} ${540 + y}) rotate(${rz}) scale(${s * (v.sx ?? 1)} ${s * (v.sy ?? 1)}) translate(-960 -540)`);
          g.setAttribute('opacity', clamp(o));
          if (L.draw) { const len = sh.getTotalLength ? sh.getTotalLength() : 2000, a = eio(prog(lt, L.draw[0] * B, L.draw[1] * B)); sh.setAttribute('stroke-dasharray', len); sh.setAttribute('stroke-dashoffset', len * (1 - a)); }
          return;
        }
        let oo = o;
        if (L.kind === 'number') oo = Math.min(o, lt >= (L.at ?? 0) * B ? prog(lt, (L.at ?? 0) * B, (L.at ?? 0) * B + 0.25) : 0);
        place(el, { x, y, s, rz, o: clamp(oo) });
        if (v.sx != null || v.sy != null) el.style.transform += ` scale(${v.sx ?? 1}, ${v.sy ?? 1})`;
        el.style.filter = v.blur ? `blur(${v.blur}px)` : '';
      });
    });
  }

  // footage { media: '*.webm', base?, offset?, rate?, title?, layout? } — real camera footage full-bleed (or framed:
  // layout 'split'), with the photo's scrims and text sides. The clip plays from the director's chosen moment.
  function footage(start, end, o) { photo(start, end, o); }

  return { cover, pain, feature: featureScene, carousel, numbers, gallery, clip: clipScene, phone, compare, statement, finale, endcard, photo, hero, detail, lineup, quote, flow, hub, type, chart, footage, mg };
})();
