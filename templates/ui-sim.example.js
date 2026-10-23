// A UI redrawn in code from the product's source, to show its LOGIC in motion (references/custom-scenes.md, "Redrawn UI").
// Use it only when the user agreed, and mark the scene "illustrative": true — the film then labels it 界面示意 · Illustrative UI.
// Take everything from the source, invent nothing: the tokens from its CSS/theme (colours, radius, font), the labels from
// its components or i18n files, the flow from its handlers (what is typed, what is clicked, what appears), demo values only.
//
// film.json:
//   "scripts": ["scenes/ui-sim.js"],
//   {"type": "custom", "fn": "uiSim", "bars": 6, "illustrative": true, "say": [{"en": "…", "zh": "…"}],
//    "tokens": {"bg": "#f4f6fa", "panel": "#ffffff", "line": "#e3e7ee", "ink": "#1d2433", "muted": "#6b7486", "accent": "#2a8f86", "radius": 12, "font": "PingFang SC, sans-serif"},
//    "ui": {"title": "MedStat Pilot", "field": {"label": "结局变量", "value": "hba1c_24"}, "button": "运行分析",
//           "table": {"cols": ["组别", "n", "均值 ± SD"], "rows": [["Programme", "160", "5.76 ± 0.34"], ["Usual care", "160", "6.05 ± 0.32"]]},
//           "bars": [{"label": "Programme", "value": 5.76}, {"label": "Usual care", "value": 6.05}]},
//    "beats": {"type": 1, "click": 4, "rows": 5, "bars": 6}}          when each step happens, in beats from the scene start
CUSTOM.uiSim = (start, end, o) => {
  const T = { bg: '#f4f6fa', panel: '#fff', line: '#e3e7ee', ink: '#1d2433', muted: '#6b7486', accent: 'var(--accent)', radius: 12, font: 'sans-serif', ...(o.tokens || {}) };
  const U = o.ui || {}, B = CONFIG.BAR / 4, at = { type: 1, click: 4, rows: 5, bars: 6, ...(o.beats || {}) };
  const W = 1360, rows = (U.table && U.table.rows) || [], bars = U.bars || [], max = Math.max(1e-9, ...bars.map((b) => +b.value || 0));
  const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;');
  scene(start, end, (R, S) => {
    S.win = div('abs', R); S.win.dataset.qa = 'media';
    Object.assign(S.win.style, { width: W + 'px', background: T.bg, borderRadius: '16px', overflow: 'hidden', boxShadow: '0 40px 100px rgba(0,0,0,0.35)', font: `15px ${T.font}`, color: T.ink });
    S.win.innerHTML = `
      <div style="height:48px;display:flex;align-items:center;gap:8px;padding:0 18px;background:${T.panel};border-bottom:1px solid ${T.line}">
        <i style="width:12px;height:12px;border-radius:50%;background:#ff5f57"></i><i style="width:12px;height:12px;border-radius:50%;background:#febc2e"></i><i style="width:12px;height:12px;border-radius:50%;background:#28c840"></i>
        <b style="margin-left:14px;font-weight:600">${esc(U.title)}</b></div>
      <div style="display:grid;grid-template-columns:380px 1fr;gap:22px;padding:22px">
        <div style="background:${T.panel};border-radius:${T.radius}px;padding:22px;border:1px solid ${T.line}">
          <div style="color:${T.muted};font-size:14px;margin-bottom:8px">${esc(U.field && U.field.label)}</div>
          <div class="sim-in" style="height:44px;border:1.5px solid ${T.line};border-radius:${T.radius - 2}px;padding:0 14px;display:flex;align-items:center;font:16px ui-monospace,monospace"></div>
          <div class="sim-btn" style="margin-top:18px;height:46px;border-radius:${T.radius - 2}px;background:${T.accent};color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600">${esc(U.button)}</div>
          <div style="margin-top:18px;height:6px;border-radius:3px;background:${T.line};overflow:hidden"><div class="sim-prog" style="height:100%;width:0;background:${T.accent}"></div></div>
        </div>
        <div style="background:${T.panel};border-radius:${T.radius}px;padding:22px;border:1px solid ${T.line}">
          <table style="width:100%;border-collapse:collapse;font-size:16px"><thead><tr>${((U.table && U.table.cols) || []).map((c) => `<th style="text-align:left;padding:10px 8px;border-bottom:2px solid ${T.ink}">${esc(c)}</th>`).join('')}</tr></thead>
          <tbody>${rows.map((r) => `<tr class="sim-row">${r.map((c) => `<td style="padding:10px 8px;border-bottom:1px solid ${T.line}">${esc(c)}</td>`).join('')}</tr>`).join('')}</tbody></table>
          <div style="margin-top:26px">${bars.map((b) => `<div style="display:flex;align-items:center;gap:12px;margin:12px 0"><div style="width:120px;color:${T.muted}">${esc(b.label)}</div><div style="flex:1;height:26px;background:${T.bg};border-radius:6px;overflow:hidden"><div class="sim-bar" style="height:100%;width:0;background:${T.accent};border-radius:6px"></div></div><div class="sim-val" style="width:70px;font:600 16px ui-monospace,monospace;opacity:0">${esc(b.value)}</div></div>`).join('')}</div>
        </div></div>`;
    S.inp = S.win.querySelector('.sim-in'); S.btn = S.win.querySelector('.sim-btn'); S.prog = S.win.querySelector('.sim-prog');
    S.rows = [...S.win.querySelectorAll('.sim-row')]; S.bars = [...S.win.querySelectorAll('.sim-bar')]; S.vals = [...S.win.querySelectorAll('.sim-val')];
    S.cur = div('abs', R, '<svg viewBox="0 0 24 24" width="30" height="30"><path d="M4 2 L4 19 L8.6 14.9 L11.6 22 L14.6 20.7 L11.7 13.9 L18 13.9 Z" fill="#fff" stroke="#111" stroke-width="1.3" stroke-linejoin="round"/></svg>');
    S.rip = div('abs', R); Object.assign(S.rip.style, { width: '56px', height: '56px', borderRadius: '50%', border: `3px solid ${T.accent}`, opacity: 0 });
  }, (S, lt, d) => {
    place(S.win, M.win(lt, d, { y: 10 }));
    // stage positions (px from the centre) of the field and the button inside the window
    const H = S.win.offsetHeight || 600, X0 = -W / 2, Y0 = -H / 2 + 10, field = [X0 + 22 + 22 + 170, Y0 + 48 + 22 + 22 + 30 + 22], btn = [X0 + 22 + 190, Y0 + 48 + 22 + 22 + 30 + 44 + 18 + 23];   // the window is as tall as its content
    const tType = at.type * B, tClick = at.click * B, tRows = at.rows * B, tBars = at.bars * B;
    const val = String((U.field && U.field.value) || ''), n = Math.floor(clamp(prog(lt, tType + 0.3, tClick - 0.6)) * val.length);
    S.inp.textContent = val.slice(0, n) + (lt > tType && lt < tClick && Math.floor(lt * 2.5) % 2 ? '|' : '');
    S.inp.style.borderColor = lt > tType && lt < tClick ? T.accent : T.line;
    // the cursor glides to the field, then to the button
    const a1 = eio(prog(lt, tType - 0.5, tType)), a2 = eio(prog(lt, tClick - 0.6, tClick));
    const cx = lerp(lerp(260, field[0], a1), btn[0], a2), cy = lerp(lerp(260, field[1], a1), btn[1], a2);
    place(S.cur, { x: cx + 12, y: cy + 14, o: fade(lt, tType - 0.6, tBars + 1.2, 0.3) });
    const r = prog(lt, tClick, tClick + 0.5);
    place(S.rip, { x: btn[0], y: btn[1], s: lerp(0.4, 1.8, eo(r)), o: r > 0 && r < 1 ? 1 - r : 0 });
    S.btn.style.transform = `scale(${1 - 0.04 * Math.sin(Math.PI * clamp(prog(lt, tClick, tClick + 0.25)))})`;
    S.prog.style.width = (100 * eio(prog(lt, tClick + 0.1, tRows))).toFixed(1) + '%';
    S.rows.forEach((tr, i) => { const k = eo(prog(lt, tRows + i * 0.18, tRows + i * 0.18 + 0.4)); tr.style.opacity = k; tr.style.transform = `translateY(${(1 - k) * 10}px)`; });
    bars.forEach((b, i) => {   // the bar grows; its true value appears only when it has landed (no in-between numbers)
      const k = eo(prog(lt, tBars + i * 0.2, tBars + i * 0.2 + 0.8));
      S.bars[i].style.width = (100 * k * (+b.value || 0) / max).toFixed(2) + '%';
      S.vals[i].style.opacity = k >= 0.99 ? 1 : 0;
    });
  });
};
