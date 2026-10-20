'use strict';
// High-level presentation patterns — the same content laid out and animated differently per motion language.
// feature(start, end, opts) shows ONE screenshot (or clip) and walks through its key points.
//   opts = { srcs, base?, title: {zh, en}, points: [{ zh, en, rect: [x,y,w,h], focus?: [x,y,w,h] }], kicker? }
//   rect = the UI region the point is about (base coords); focus = crop to zoom to (default: rect padded to 16:9)
// Layout + behaviour by MO_ID:
//   cinematic-3d   3D window centre, focus pushes to each point, glowing highlight + tag
//   precision-data flat window left, numbered spec list right, leader lines drawn from list to highlight
//   kinetic-launch full-bleed window, punch-zoom burst into each point on the bar, headline slams in
//   gentle-story   soft window left, slow Ken Burns through the points, one line of text at a time on the right
//   playful-pop    tilted window, points pop as sticker bubbles around it, bouncy highlights
//   editorial-type split screen: giant index + title + list left, window right, hard snaps between points
function padTo169([x, y, w, h], base, k = 1.9) {
  let W = Math.max(w * k, h * k * 16 / 9), H = W * 9 / 16;
  W = Math.min(W, base[0]); H = Math.min(H, base[1]);
  const cx = x + w / 2, cy = y + h / 2;
  return [clamp(cx - W / 2, 0, base[0] - W), clamp(cy - H / 2, 0, base[1] - H), W, H];
}
function feature(start, end, opts) {
  const base = opts.base || [1920, 1080], n = Math.max(1, (opts.points || []).length);
  // points without a rect (e.g. a product photo) get a region in reading order and no highlight box
  const P = (opts.points || []).map((p, i) => (p.rect ? p : { ...p, nohl: true, rect: [base[0] * (0.12 + 0.76 * i / n), base[1] * 0.25, base[0] * 0.76 / n, base[1] * 0.5] }));
  const full = [0, 0, base[0], base[1]];
  const L = {
    'cinematic-3d': { w: 1320, x: 0, y: 40 }, 'precision-data': { w: 1120, x: -300, y: 10 }, 'kinetic-launch': { w: 1400, x: 0, y: 30 },
    'gentle-story': { w: 1120, x: -250, y: -10 }, 'playful-pop': { w: 1180, x: -120, y: 0 }, 'editorial-type': { w: 1000, x: 330, y: 20 },
  }[MO_ID] || { w: 1400, x: 0, y: 0 };
  scene(start, end, (R, S) => {
    S.W = win(R, { srcs: opts.srcs, base, w: L.w, chrome: opts.chrome || 'auto' });
    S.h = P.map((p) => hl(S.W, p.rect));
    S.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    S.svg.setAttribute('width', 1920); S.svg.setAttribute('height', 1080); Object.assign(S.svg.style, { position: 'absolute', left: 0, top: 0, pointerEvents: 'none' });
    R.appendChild(S.svg);
    const title = `<div class="h-zh" style="letter-spacing:4px;font-size:44px">${opts.title?.zh || ''}</div><div class="kicker" style="margin-top:10px">${opts.title?.en || ''}</div>`;
    if (MO_ID === 'precision-data' || MO_ID === 'editorial-type') {
      S.title = textEl(R, title, { width: '520px' });
      S.items = P.map((p, i) => textEl(R, `<div style="display:flex;gap:18px;align-items:flex-start"><div class="accent" style="font:700 22px var(--mono);min-width:42px">${String(i + 1).padStart(2, '0')}</div><div><div style="font:600 28px var(--zh)">${p.zh}</div><div class="muted" style="font:500 17px var(--en);margin-top:4px">${p.en || ''}</div></div></div>`, { width: '520px' }));
      S.lines = P.map(() => { const l = document.createElementNS('http://www.w3.org/2000/svg', 'path'); l.setAttribute('fill', 'none'); l.setAttribute('stroke', 'var(--accent)'); l.setAttribute('stroke-width', 2); S.svg.appendChild(l); return l; });
      if (MO_ID === 'editorial-type') S.index = textEl(R, '01', { whiteSpace: 'nowrap' }), S.index.className += ' big-num accent';
    } else if (MO_ID === 'gentle-story') {
      S.title = textEl(R, title, { width: '560px' });
      S.lines = P.map((p) => textEl(R, `<div style="font:500 36px var(--zh);line-height:1.5">${p.zh}</div><div class="muted" style="font:400 22px var(--en);margin-top:10px;line-height:1.4">${p.en || ''}</div>`, { width: '560px' }));
    } else if (MO_ID === 'kinetic-launch') {
      S.heads = P.map((p) => textEl(R, `<div class="h-zh" style="font-size:60px;letter-spacing:4px">${p.zh}</div><div class="kicker" style="margin-top:8px">${p.en || ''}</div>`, { whiteSpace: 'nowrap', padding: '22px 34px', background: 'var(--bg-edge)', borderLeft: '8px solid var(--accent)' }));
    } else if (MO_ID === 'playful-pop') {
      S.bubbles = P.map((p) => textEl(R, `<span class="chip" style="font-size:24px;padding:14px 26px">${p.zh}${p.en ? `<span class="muted" style="font:600 15px var(--en)">${p.en}</span>` : ''}</span>`, { whiteSpace: 'nowrap' }));
      S.title = textEl(R, title, { whiteSpace: 'nowrap' });
    } else {
      S.t = P.map((p) => tag(S.W, p.zh, p.en));
      S.title = textEl(R, title, { whiteSpace: 'nowrap' });
    }
  }, (S, lt, d) => {
    const t0 = opts.chrome === 'frame' ? 1.2 : 0.8, step = (d - t0 - 0.2) / n, T = P.map((_, i) => t0 + i * step);   // a dense screen is shown whole for < 1 s
    const cur = P.reduce((c, _, i) => (lt >= T[i] ? i : c), -1);
    // readable zoom: a screen's body text (opts.textPx base px, ~13 for desktop UI) must land at ≥ 18 px, so a crop is at
    // most L.w·textPx/18 wide. Points without a rect on a screen hold the full frame; photos (frame) keep the slow drift.
    const maxW = opts.chrome === 'frame' ? base[0] : L.w * (opts.textPx || 13) / 18;
    const readable = (r) => { const c = padTo169(r, base, MO_ID === 'kinetic-launch' ? 1.5 : 2.2); if (c[2] <= maxW) return c;
      const W = maxW, H = W * 9 / 16, cx = r[0] + r[2] / 2, cy = r[1] + r[3] / 2; return [clamp(cx - W / 2, 0, base[0] - W), clamp(cy - H / 2, 0, base[1] - H), W, H]; };
    const focusSteps = [[0, full], ...P.map((p, i) => [T[i] + MO.focus.dur * 0.6, p.focus || (p.nohl && opts.chrome !== 'frame' ? full : readable(p.rect))])];
    if (MO_ID === 'gentle-story') focusSteps.push([d, focusSteps[focusSteps.length - 1][1]]);
    setCrop(S.W, cur < 0 && MO_ID !== 'gentle-story' ? full : M.focus(lt, focusSteps));
    if (MO_ID === 'kinetic-launch') { // burst: punch scale on each point arrival
      const k = cur >= 0 ? Math.exp(-(lt - T[cur]) * 6) : 0;
      place(S.W.root, { ...M.win(lt, d, { x: L.x, y: L.y }), s: 1 + 0.06 * k });
    } else place(S.W.root, M.win(lt, d, { x: L.x, y: L.y, ry: MO_ID === 'playful-pop' ? -6 : 0 }));
    S.h.forEach((H, i) => posHL(S.W, H, P[i].nohl ? 0 : i === cur || (MO_ID === 'precision-data' && i < cur) ? fade(lt, T[i], i === cur ? d + 0.2 : T[i] + step * 0.9, 0.3) : 0));
    // stage coordinate of a point's centre (window is near-flat for these layouts)
    const stageXY = (i) => { const [x, y, w, h] = P[i].rect; const bar = S.W.root.firstElementChild?.classList?.contains('bar') ? 34 : 0; return [960 + L.x - S.W.w / 2 + mapX(S.W, x + w / 2), 540 + L.y - (S.W.h + bar) / 2 + bar + mapY(S.W, y + h / 2)]; };
    if (MO_ID === 'precision-data' || MO_ID === 'editorial-type') {
      const colX = MO_ID === 'precision-data' ? 640 : -560;
      const ed = MO_ID === 'editorial-type', ty = ed ? -170 : -330, iy = ed ? -40 : -170;
      M.text(S.title, lt, 0.3, { x: colX, y: ty });
      if (S.index) { S.index.textContent = String(Math.max(cur, 0) + 1).padStart(2, '0'); M.text(S.index, lt, 0.2, { x: -700, y: -360, o: 0.9 }); }
      S.items.forEach((it, i) => M.text(it, lt, T[i] - 0.2, { x: colX, y: iy + i * 120, o: i === cur ? 1 : 0.45 }));
      S.lines.forEach((ln, i) => {
        if (MO_ID !== 'precision-data' || P[i].nohl || lt < T[i] + MO.focus.dur * 0.6) { ln.setAttribute('d', ''); return; }
        const [hx, hy] = stageXY(i), lx = 960 + colX - 280, ly = 540 - 170 + i * 120 + 6, mid = (lx + hx) / 2;
        const len = Math.hypot(lx - hx, ly - hy) * 1.3, a = ex(prog(lt, T[i] + MO.focus.dur * 0.6, T[i] + MO.focus.dur * 0.6 + 0.5));
        ln.setAttribute('d', `M${lx},${ly} C${mid},${ly} ${mid},${hy} ${hx},${hy}`);
        ln.setAttribute('stroke-dasharray', len); ln.setAttribute('stroke-dashoffset', len * (1 - a)); ln.setAttribute('opacity', i === cur ? 1 : 0.35);
      });
    } else if (MO_ID === 'gentle-story') {
      M.text(S.title, lt, 0.4, { x: 640, y: -300 });
      S.lines.forEach((el, i) => { const on = i === cur ? 1 : 0; M.text(el, lt, T[i], { x: 640, y: -40, o: on ? 1 - prog(lt, (T[i + 1] ?? d + 1) - 0.6, T[i + 1] ?? d + 1) : 0 }); });
    } else if (MO_ID === 'kinetic-launch') {
      S.heads.forEach((el, i) => M.text(el, lt, T[i], { x: -430, y: -300, o: i === cur ? 1 - prog(lt, (T[i + 1] ?? d + 1) - 0.15, T[i + 1] ?? d + 1) : 0 }));
    } else if (MO_ID === 'playful-pop') {
      M.text(S.title, lt, 0.3, { x: 0, y: -440 });
      S.bubbles.forEach((el, i) => { const [hx, hy] = stageXY(i); const side = hx > 960 + L.x ? 1 : -1; const half = el.offsetWidth / 2 + 40; place(el, { ...M.pop(lt, T[i], { x: clamp(hx - 960 + side * 260, -960 + half, 960 - half), y: clamp(hy - 540 - 60, -380, 260), rz: side * 4 }) }); });
    } else {
      M.text(S.title, lt, 0.3, { x: 0, y: -462 });
      S.t.forEach((T2, i) => posTag(S.W, T2, P[i].rect[0] + P[i].rect[2] / 2, P[i].rect[1] - 18, i === cur ? fade(lt, T[i], d + 0.2, 0.3) : 0));
    }
  });
}
