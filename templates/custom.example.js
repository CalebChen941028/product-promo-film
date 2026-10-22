'use strict';
// The director's cut — a scene this film writes for itself (references/custom-scenes.md).
// List the file in film.json "scripts", then use {"type": "custom", "fn": "beforeAfter", "bars": 4, "assets": {…}, …}.
// Same API as the library: scene(start, end, init(R, S), update(S, lt, dur)) · win · setCrop · place · textEl · M.* · prog/eio/lerp.
// Every visual property is a pure function of lt (seconds into the scene): no timers, no CSS animations, no randomness.
// Colours and type come from the style (var(--accent), .h-zh, .kicker…), so the scene matches the film.

// beforeAfter { assets: {before, after}, base?, labels?: [[zh, en], [zh, en]] } — one frame, two states: a hard edge sweeps
// across on the downbeat and the "after" takes the frame. For a messy spreadsheet → the finished table, a raw room → the
// finished one. Both pictures must be real.
CUSTOM.beforeAfter = (start, end, o) => {
  const base = o.base || [1920, 1080], L = o.labels || [['之前', 'BEFORE'], ['之后', 'AFTER']];
  scene(start, end, (R, S) => {
    S.a = win(R, { srcs: o.assets.before, base, w: 1920, chrome: 'none', radius: 0 });
    S.b = win(R, { srcs: o.assets.after, base, w: 1920, chrome: 'none', radius: 0 });
    S.edge = textEl(R, '', { width: '4px', height: '1080px', background: 'var(--accent)', boxShadow: '0 0 30px var(--accent)' });
    S.la = textEl(R, `<span class="chip">${L[0][0]} <span class="muted" style="font:600 14px var(--en);letter-spacing:3px">${L[0][1]}</span></span>`, { whiteSpace: 'nowrap' });
    S.lb = textEl(R, `<span class="chip accent">${L[1][0]} <span style="font:600 14px var(--en);letter-spacing:3px">${L[1][1]}</span></span>`, { whiteSpace: 'nowrap' });
  }, (S, lt, d) => {
    const k = eio(prog(lt, d * 0.35, d * 0.65));                 // the sweep, centred in the scene
    place(S.a.root, { o: 1 }); place(S.b.root, { o: 1 });
    S.b.root.style.clipPath = `inset(0 ${((1 - k) * 100).toFixed(2)}% 0 0)`;
    place(S.edge, { x: lerp(-960, 960, k), o: k > 0 && k < 1 ? 1 : 0 });
    M.text(S.la, lt, 0.3, { x: -700, y: -420, o: 1 - k });
    M.text(S.lb, lt, d * 0.5, { x: 700, y: -420, o: k });
  });
};
