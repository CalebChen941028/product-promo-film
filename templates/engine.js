'use strict';
// Product film compositor v2 — deterministic DOM/CSS-3D. Every visual property is a pure function of t (s).
// The renderer calls window.renderFrame(t) (which may return a Promise while video clips seek) and screenshots.
// No CSS transitions/animations, no timers, no unseeded randomness.
//
// Look:   CONFIG.STYLE  → styles/<id>.css + styles/<id>.js (background, transitions, window chrome, beat pulse).
// Motion: CONFIG.MOTION → one of MOTIONS below (entrances, text reveals, highlights, focus moves, camera),
//         chosen from the material's theme; defaults to the style's motionDefault. Scenes use M.* only.
//
// API for scenes.js
//   scene(start, end, init(R, S), update(S, lt, dur, t))          register a scene (times in s; use bar(n))
//   win(parent, {srcs, crop, w, base, chrome, title, radius})     screenshot(s)/clip in a frame.
//       base = [w, h] of the source's coordinate space (default [1920,1080] = CSS px of a 2× capture);
//       crop = [x, y, w, h] in base units; srcs = 'a.png' | ['a.png','b.png'] | [{video:'c.webm'}]
//       chrome = 'auto' (style default) | 'mac-dark' | 'mac-light' | 'browser' | 'phone' | 'frame' (photo) | 'none'
//   setCrop(W, crop, w?) · showLayer(W, idx, mix?) · W.time(sec)  pan/zoom · switch state · seek video
//   hl/posHL · tag/posTag · cursor/posCursor                        highlight, callout, pointer (base coords)
//   pic(parent, src, w, h) · textEl(parent, html, css) · clip(parent, src, w, h) + clipTime(C, sec)
//   place(el, {x,y,z,rx,ry,rz,s,o})                                 transform about the stage centre
//   M.win(lt, dur, base) · M.enter · M.pop(lt, t0, base) · M.text(el, lt, t0, base) · M.focus(lt, steps)
//                                                                   motion language (CONFIG.MOTION) — see MOTIONS
//   kf · kfRect · prog · fade · clamp · lerp · eo eio ex eback      timing helpers
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, t) => a + (b - a) * t;
const prog = (t, a, b) => clamp((t - a) / (b - a));
const eo = (t) => 1 - Math.pow(1 - t, 3);
const eio = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const ex = (t) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t));
const eback = (t) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
const esoft = (t) => 0.5 - 0.5 * Math.cos(Math.PI * clamp(t));
const fade = (t, a, b, f = 0.4) => Math.min(prog(t, a, a + f), 1 - prog(t, b - f, b));
const SH = CONFIG.SHOTS, AS = CONFIG.ASSETS;
const FX = { init: [], scene: [], frame: [] };   // hooks for cinema.js (colour script, lens, light)
const CUTS = (CONFIG.CINEMA && CONFIG.CINEMA.cuts) || [];  // per scene index: 'style' | 'whip' | 'push' (cut INTO that scene)
const ST = Object.assign({ background: 'grid', transition: 'fade', chrome: 'mac-dark', pulse: 'glow', motionDefault: 'cinematic-3d', xf: 0.28 }, window.STYLE || {});

function div(cls, parent, html) { const d = document.createElement('div'); if (cls) d.className = cls; if (html != null) d.innerHTML = html; if (parent) parent.appendChild(d); return d; }
const IMGS = [], VIDS = [];
function img(src, parent, cls) { const i = new Image(); i.src = src; if (cls) i.className = cls; if (parent) parent.appendChild(i); IMGS.push(i); return i; }
function vid(src, parent, cls) { const v = document.createElement('video'); v.src = src; v.muted = true; v.preload = 'auto'; v.playsInline = true; if (cls) v.className = cls; if (parent) parent.appendChild(v); VIDS.push(v); return v; }
function place(el, { x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0, s = 1, o = 1 } = {}) {
  el.style.transform = `translate(-50%,-50%) translate3d(${x}px,${y}px,${z}px) rotateX(${rx}deg) rotateY(${ry}deg) rotateZ(${rz}deg) scale(${s})`;
  el.style.opacity = o;
}
function kf(t, keys) {
  if (t <= keys[0][0]) return { ...keys[0][1] };
  for (let i = 0; i < keys.length - 1; i++) {
    const [t0, a] = keys[i], [t1, b, e] = keys[i + 1];
    if (t <= t1) { const k = (e || eio)(prog(t, t0, t1)); const r = { ...a }; for (const p in b) r[p] = lerp(a[p] ?? 0, b[p], k); return r; }
  }
  return { ...keys[keys.length - 1][1] };
}
function kfRect(t, keys) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) { const [t0, a] = keys[i], [t1, b] = keys[i + 1]; if (t <= t1) { const k = eio(prog(t, t0, t1)); return a.map((v, j) => lerp(v, b[j], k)); } }
  return keys[keys.length - 1][1];
}

// ---------- motion languages (independent of the visual style) ----------
// CONFIG.MOTION picks one; otherwise the style's default. Each language defines how things ENTER, how held
// shots BREATHE, how TEXT reveals, how HIGHLIGHTS appear, how FOCUS moves inside a screenshot, and what the
// CAMERA does on the beat. These are starting points: a film may define its own (keyframes in film.json or code).
const MOTIONS = {
  // serious tech / platforms: 3D fly-ins from depth, slow orbit drift, rise text, glowing grow highlights
  'cinematic-3d': { enter: 'fly', tilt: 1, drift: 1, text: 'rise', hl: 'grow', focus: { dur: 1.3, ease: eio }, camera: 'orbit', pop: 'back' },
  // science / data / research / finance: flat & exact, measured snaps on the beat, mask-wipe text, traced highlights
  'precision-data': { enter: 'snap', tilt: 0.15, drift: 0.25, text: 'mask', hl: 'draw', focus: { dur: 0.45, ease: ex }, camera: 'none', pop: 'snap' },
  // launches / dev tools / energetic music: punch-ins, whip slides, beat-punch camera, fast slide text, flash highlights
  'kinetic-launch': { enter: 'punch', tilt: 0.5, drift: 0.6, text: 'slide', hl: 'flash', focus: { dur: 0.25, ease: ex }, camera: 'punch', pop: 'punch' },
  // healthcare-for-people / education / mission stories: slow dolly, blur-in text, long eases, soft highlights
  'gentle-story': { enter: 'rise', tilt: 0.2, drift: 0.5, text: 'blur', hl: 'soft', focus: { dur: 2.0, ease: esoft }, camera: 'dolly', pop: 'soft' },
  // consumer / creator / kids / social: elastic bounces, tilt sway, bouncing stickers, overshooting focus
  'playful-pop': { enter: 'bloom', tilt: 0.6, drift: 0.8, text: 'bounce', hl: 'bounce', focus: { dur: 0.7, ease: eback }, camera: 'sway', pop: 'elastic' },
  // manifestos / brand / opinionated research: hard slides from the edge, mask-up type, no 3D, thick bars
  'editorial-type': { enter: 'slide', tilt: 0, drift: 0.1, text: 'maskup', hl: 'draw', focus: { dur: 0.4, ease: ex }, camera: 'none', pop: 'snap' },
};
// The film has ONE motion language (its grammar); a scene may borrow another for itself ("motion" in film.json).
// scenes.js calls shot({motion, camera, layout}) before each LIB call; scene() keeps it, and the frame loop switches
// MO/MO_ID to the scene's own before init and update, so every M.* call inside a scene speaks its language.
// the film's own motion languages (film.json "motions": {"id": {"like": "gentle-story", enter, text, hl, pop, camera, tilt,
// drift, focus: {dur, ease}}}): built on a language it names in "like", overriding any of its parts
const EASES = { eio: (t) => eio(t), eo: (t) => eo(t), ex: (t) => ex(t), esoft: (t) => esoft(t), eback: (t) => eback(t), linear: (t) => t };
for (const [id, m] of Object.entries(CONFIG.MOTIONS_EXTRA || {})) {
  const like = MOTIONS[m.like] || MOTIONS['cinematic-3d'], f = Object.assign({}, like.focus, m.focus || {});
  if (typeof f.ease === 'string') f.ease = EASES[f.ease] || like.focus.ease;
  MOTIONS[id] = Object.assign({}, like, m, { focus: f });
}
// the film's own camera moves and cuts, registered by its scripts (references/custom-scenes.md):
//   CAMERA.<name> = ({t, lt, dur, p, beat, bar}) => 'css transform'        p = eased 0→1 over the scene
//   CUT.<name> = ({p, inc}) => ({transform?, opacity?, filter?, clipPath?})  (optional CUT.<name>.len = × crossfade)
const CAMERA = {}, CUT = {};
// the film's own camera moves and cuts written as keyframes in film.json — no code (references/custom-scenes.md):
//   "cameras": {"name": {"from": {x, y, z, s, rx, ry, rz}, "to": {…}, "ease": "esoft", "pulse": 0.01, "at": [x, y]}}
//     at = the stage point (px, 1920 × 1080) the move scales and turns around: push into a button, a product, a chart peak
//     x/y/z px, s scale, rx/ry/rz degrees; the scene moves from "from" to "to" over its length; pulse = a scale kick on every beat
//   "cuts": {"name": {"from": {x, y, s, rz, o, blur, bright}, "to": {…}, "reveal": "left|right|up|down|circle|center", "ease": "eio", "len": 1.2}}
//     the incoming scene arrives from "from" (and reveals in that shape); the outgoing one leaves towards "to" (default: it stays)
//     at = [x, y] stage px: both scale around it and a circle reveal opens from it — a zoom-through: the outgoing scene dives
//     into the element the story continues from ("to": {"s": 3, "o": 0}) and the next scene grows out of the same point
const KF_KEYS = { x: 0, y: 0, z: 0, s: 1, rx: 0, ry: 0, rz: 0, o: 1, blur: 0, bright: 1 };
const kfMix = (a, b, e) => { const v = {}; for (const [k, d] of Object.entries(KF_KEYS)) v[k] = lerp(a[k] ?? d, b[k] ?? d, e); return v; };
const kfTf = (v, at) => (at ? `translate(${at[0] - 960}px,${at[1] - 540}px) ` : '') + `translate3d(${v.x.toFixed(2)}px,${v.y.toFixed(2)}px,${v.z.toFixed(1)}px) rotateX(${v.rx.toFixed(3)}deg) rotateY(${v.ry.toFixed(3)}deg) rotateZ(${v.rz.toFixed(3)}deg) scale(${v.s.toFixed(4)})` + (at ? ` translate(${960 - at[0]}px,${540 - at[1]}px)` : '');   // at = [x, y] stage px: scale and turn around that point
const kfReveal = (r, e, at) => {
  const q = ((1 - e) * 100).toFixed(2);
  if (r === 'circle' && at) return `circle(${(e * 2300).toFixed(1)}px at ${at[0]}px ${at[1]}px)`;   // opens from the anchor (a button, a product)
  return r === 'left' ? `inset(0 ${q}% 0 0)` : r === 'right' ? `inset(0 0 0 ${q}%)` : r === 'up' ? `inset(${q}% 0 0 0)` : r === 'down' ? `inset(0 0 ${q}% 0)`
    : r === 'circle' ? `circle(${(e * 115).toFixed(2)}% at 50% 50%)` : r === 'center' ? `inset(0 ${(q / 2).toFixed(2)}% 0 ${(q / 2).toFixed(2)}%)` : '';
};
for (const [id, c] of Object.entries(CONFIG.CAMERAS_EXTRA || {})) {
  const ease = EASES[c.ease] || EASES.esoft;
  CAMERA[id] = ({ lt, dur, beat }) => {
    const v = kfMix(c.from || {}, c.to || {}, ease(clamp(lt / Math.max(0.01, dur))));
    if (c.pulse) v.s *= 1 + c.pulse * Math.exp(-beat * 6);
    return kfTf(v, c.at);
  };
}
for (const [id, c] of Object.entries(CONFIG.CUTS_EXTRA || {})) {
  const ease = EASES[c.ease] || EASES.eio;
  CUT[id] = ({ p, inc }) => {
    const e = ease(clamp(p)), v = inc ? kfMix(c.from || { o: 0 }, {}, e) : kfMix({}, c.to || {}, e);
    return { transform: kfTf(v, c.at), opacity: clamp(v.o), filter: `blur(${Math.max(0, v.blur).toFixed(1)}px) brightness(${v.bright.toFixed(3)})`,
             clipPath: inc && c.reveal ? kfReveal(c.reveal, e, c.at) : '' };
  };
  CUT[id].len = Math.min(2, Math.max(0.4, c.len || 1.2));
}
const FILM_MO = MOTIONS[CONFIG.MOTION] ? CONFIG.MOTION : (MOTIONS[ST.motionDefault] ? ST.motionDefault : 'cinematic-3d');
let MO_ID = FILM_MO, MO = MOTIONS[FILM_MO];
let SHOT = {};
function useShot(sh) { MO_ID = (sh && MOTIONS[sh.motion]) ? sh.motion : FILM_MO; MO = MOTIONS[MO_ID]; }
function shot(o) { SHOT = o || {}; useShot(SHOT); }
const elastic = (t) => (t <= 0 ? 0 : t >= 1 ? 1 : Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * (2 * Math.PI / 3)) + 1);

const M = {
  // entrance of a big element (window, card). base = resting {x,y,z,rx,ry,rz,s}
  enter(lt, base = {}) {
    const b = { x: 0, y: 0, z: 0, rx: 0, ry: 0, rz: 0, s: 1, ...base }, k = MO.tilt;
    switch (MO.enter) {
      case 'fly': { const e = ex(prog(lt, 0, 1.6)); return { ...b, z: lerp(-1600, b.z, e), rx: lerp(34 * k, b.rx, e), y: lerp(b.y + 60, b.y, e), o: prog(lt, 0, 0.5) }; }
      case 'snap': { const e = ex(prog(lt, 0, 0.45)); return { ...b, y: lerp(b.y + 24, b.y, e), s: lerp(b.s * 0.985, b.s, e), o: prog(lt, 0, 0.18) }; }
      case 'punch': { const e = ex(prog(lt, 0, 0.35)); return { ...b, s: lerp(b.s * 1.22, b.s, e), z: lerp(220, b.z, e), o: prog(lt, 0, 0.12) }; }
      case 'rise': { const e = esoft(prog(lt, 0, 1.6)); return { ...b, y: lerp(b.y + 70, b.y, e), s: lerp(b.s * 0.96, b.s, e), o: prog(lt, 0, 1.0) }; }
      case 'bloom': { const a = prog(lt, 0, 0.9); return { ...b, s: lerp(b.s * 0.7, b.s, elastic(a)), rz: lerp(-4, b.rz, eo(a)), rx: lerp(12 * k, b.rx, eo(a)), o: prog(lt, 0, 0.3) }; }
      case 'slide': { const e = ex(prog(lt, 0, 0.5)); return { ...b, x: lerp(b.x + 260, b.x, e), o: prog(lt, 0, 0.15) }; }
      default: return { ...b, o: prog(lt, 0, 0.4) };
    }
  },
  // slow motion while a shot is held (keeps a still screenshot alive)
  drift(lt, dur, base = {}) {
    const k = MO.tilt * MO.drift, p = prog(lt, 0, dur);
    return { rx: (base.rx || 0) + lerp(2, -1, p) * k, ry: (base.ry || 0) + lerp(-4, 4, p) * k, z: (base.z || 0) + p * 60 * MO.drift };
  },
  // entrance + drift for a whole window/card: the one call most scenes need
  win(lt, dur, base = {}) { const e = M.enter(lt, base), d = M.drift(lt, dur, base), w = prog(lt, 0, 1.2); return { ...e, rx: lerp(e.rx, d.rx, w), ry: lerp(e.ry, d.ry, w), z: e.z + (d.z - (base.z || 0)) * w }; },
  // small element appearing at t0 (chips, icons, numbers)
  pop(lt, t0, base = {}) {
    const s0 = base.s || 1;
    switch (MO.pop) {
      case 'snap': { const a = prog(lt, t0, t0 + 0.22); return { ...base, s: s0 * lerp(0.94, 1, ex(a)), o: a }; }
      case 'punch': { const a = prog(lt, t0, t0 + 0.3); return { ...base, s: s0 * lerp(1.4, 1, ex(a)), o: clamp(a * 3) }; }
      case 'soft': { const a = prog(lt, t0, t0 + 1.0); return { ...base, s: s0 * lerp(0.92, 1, esoft(a)), o: esoft(a) }; }
      case 'elastic': { const a = prog(lt, t0, t0 + 0.8); return { ...base, s: s0 * lerp(0.4, 1, elastic(a)), rz: (base.rz || 0) + lerp(-8, 0, eo(a)), o: clamp(a * 4) }; }
      default: { const a = prog(lt, t0, t0 + 0.5); return { ...base, s: s0 * lerp(0.7, 1, eback(a)), o: clamp(a * 2) }; }
    }
  },
  // text block reveal at t0 — sets transform AND clip/filter on the element itself
  text(el, lt, t0, base = {}) {
    const a = prog(lt, t0, t0 + ({ mask: 0.6, maskup: 0.5, slide: 0.35, blur: 1.1, bounce: 0.8, rise: 0.7 }[MO.text] || 0.7));
    let p = { ...base }, clip = '', filter = '';
    switch (MO.text) {
      case 'mask': clip = `inset(-20% ${(1 - ex(a)) * 100}% -20% 0)`; p.o = a > 0 ? 1 : 0; break;
      case 'maskup': clip = `inset(${(1 - ex(a)) * 100}% 0 -20% 0)`; p.y = (base.y || 0) + (1 - ex(a)) * 40; p.o = a > 0 ? 1 : 0; break;
      case 'slide': p.x = (base.x || 0) - (1 - ex(a)) * 90; p.o = clamp(a * 3); break;
      case 'blur': filter = `blur(${(1 - esoft(a)) * 14}px)`; p.s = (base.s || 1) * lerp(1.04, 1, esoft(a)); p.o = esoft(a); break;
      case 'bounce': p.s = (base.s || 1) * lerp(0.5, 1, elastic(a)); p.rz = lerp(-5, 0, eo(a)); p.o = clamp(a * 4); break;
      default: p.y = (base.y || 0) + (1 - eo(a)) * 30; p.o = a; break;
    }
    if (base.o != null) p.o = Math.min(p.o, base.o);
    place(el, p); el.style.clipPath = clip; el.style.filter = filter;
  },
  rise(lt, t0, base = {}) { const a = prog(lt, t0, t0 + 0.7); return { ...base, y: (base.y || 0) + (1 - eo(a)) * 30, o: a }; },
  // move the crop of a screenshot through focus points: steps = [[t, [x,y,w,h]], ...] (t = arrival time)
  focus(lt, steps) {
    const { dur, ease } = MO.focus;
    let r = steps[0][1];
    for (let i = 1; i < steps.length; i++) { const [t1, b] = steps[i]; const a = prog(lt, t1 - dur, t1); if (a > 0) r = r.map((v, j) => lerp(v, b[j], ease(a))); }
    return r;
  },
  // per-frame camera on the whole scene (beat-aware). Returns a CSS transform string. cam = the scene's own move
  // ("camera" in film.json, chosen by the director) or the motion language's default. Moves are slow and small:
  // felt, not seen (director.md) — a push is 5 %, a pan 70 px over the whole scene.
  camera(t, lt, dur, cam) {
    const beat = CONFIG.BAR / 4, ph = (((t - CONFIG.G) % beat) + beat) % beat, barPh = (((t - CONFIG.G) % CONFIG.BAR) + CONFIG.BAR) % CONFIG.BAR;
    const p = esoft(prog(lt, 0, dur));
    if (CAMERA[cam || MO.camera]) return CAMERA[cam || MO.camera]({ t, lt, dur, p, beat: ph, bar: barPh }) || '';
    switch (cam || MO.camera) {
      case 'push': return `scale(${(1 + 0.05 * p).toFixed(4)})`;
      case 'pull': return `scale(${(1.06 - 0.06 * p).toFixed(4)})`;
      case 'pan-l': return `translateX(${lerp(36, -36, p).toFixed(2)}px) scale(1.03)`;
      case 'pan-r': return `translateX(${lerp(-36, 36, p).toFixed(2)}px) scale(1.03)`;
      case 'crane': return `translateY(${lerp(26, -26, p).toFixed(2)}px) scale(1.03)`;
      case 'tilt': return `rotateX(${lerp(2.2, -1.2, p).toFixed(3)}deg) scale(1.02)`;
      case 'arc': return `rotateY(${lerp(-2.6, 2.6, p).toFixed(3)}deg) translateX(${lerp(-20, 20, p).toFixed(2)}px)`;
      // dolly zoom ("vertigo"): the frame pushes in while the 3D depth flattens — space seems to stretch, subject holds
      case 'vertigo': return `perspective(${lerp(900, 2600, p).toFixed(0)}px) scale(${(1 + 0.07 * p).toFixed(4)})`;
      // handheld: a slow, small breathing float (two incommensurate sines), never a jitter
      case 'handheld': return `translate(${(Math.sin(t * 0.9) * 5 + Math.sin(t * 2.3) * 2).toFixed(2)}px, ${(Math.cos(t * 0.7) * 4 + Math.sin(t * 1.9) * 1.5).toFixed(2)}px) rotate(${(Math.sin(t * 0.5) * 0.25).toFixed(3)}deg) scale(1.02)`;
      // reveal: starts high and close, settles down and out onto the whole frame (a tilt-down reveal)
      case 'reveal': return `translateY(${lerp(-40, 0, p).toFixed(2)}px) scale(${(1.08 - 0.08 * p).toFixed(4)})`;
      case 'orbit': return `rotateY(${Math.sin(lt * 0.25) * 0.8}deg) rotateX(${Math.cos(lt * 0.2) * 0.4}deg)`;
      case 'punch': return `scale(${1 + 0.028 * Math.exp(-barPh * 7) + 0.008 * Math.exp(-ph * 10)})`;
      case 'dolly': return `scale(${1 + prog(lt, 0, dur) * 0.035})`;
      case 'sway': return `rotate(${Math.sin(t * 1.3) * 0.35}deg) translateY(${Math.sin(t * 2.1) * 3}px)`;
      default: return '';
    }
  },
};

// ---------- frames ----------
const CHROME = {
  'mac-dark': (t) => `<div class="bar mac dark"><i></i><i></i><i></i><span>${t}</span></div>`,
  'mac-light': (t) => `<div class="bar mac light"><i></i><i></i><i></i><span>${t}</span></div>`,
  browser: (t) => `<div class="bar browser"><i></i><i></i><i></i><b>${t}</b></div>`,
  none: () => '',
  frame: () => '',
  phone: () => '',
};
function win(parent, { srcs, crop, w, base = [1920, 1080], chrome = 'auto', title = CONFIG.BRAND?.name || 'App', radius }) {
  const kind = chrome === 'auto' ? ST.chrome : chrome;   // 'frame' = a photo with soft corners + shadow, no title bar
  const root = div('abs win' + (kind === 'phone' ? ' phone' : '') + (kind === 'frame' ? ' photo' : ''), parent); root.dataset.qa = 'media';
  if (radius != null) root.style.borderRadius = radius + 'px';
  root.insertAdjacentHTML('beforeend', CHROME[kind] ? CHROME[kind](title) : '');
  const body = div('win-body', root);
  const W = { root, body, layers: [], base };
  // a .webm path is footage: it plays in place of a still (cover, photo, hero, footage…); scenes seek it each frame
  for (const s of [].concat(srcs)) W.layers.push(typeof s === 'string' ? (/\.webm$/i.test(s) ? vid(s, body, 'shot') : img(s, body, 'shot')) : vid(s.video, body, 'shot'));
  W.ov = div('ov', body);
  div('glint', root);   // light sweep (cinema.js)
  W.time = (sec) => W.layers.forEach((l) => { if (l.tagName === 'VIDEO') seekVideo(l, sec); });
  setCrop(W, crop || [0, 0, base[0], base[1]], w); showLayer(W, 0);
  return W;
}
function setCrop(W, crop, w = W.w) {
  const [x, y, cw, ch] = crop, s = w / cw;
  W.crop = crop; W.w = w; W.s = s; W.h = ch * s;
  W.root.style.width = w + 'px'; W.body.style.width = w + 'px'; W.body.style.height = W.h + 'px';
  for (const l of W.layers) { l.style.width = W.base[0] * s + 'px'; l.style.height = W.base[1] * s + 'px'; l.style.transform = `translate(${-x * s}px,${-y * s}px)`; }
}
function showLayer(W, idx, mix) {
  W.layers.forEach((l, i) => {
    if (i === idx) { l.style.display = 'block'; l.style.opacity = 1; }
    else if (mix != null && i === idx + 1 && mix > 0) { l.style.display = 'block'; l.style.opacity = mix; }
    else l.style.display = 'none';
  });
}
const mapX = (W, x) => (x - W.crop[0]) * W.s, mapY = (W, y) => (y - W.crop[1]) * W.s;
function hl(W, rect) { return { d: div('hl', W.ov), rect }; }
function posHL(W, H, a, pad = 6) {
  const [x, y, w, h] = H.rect, A = clamp(a);
  const st = { left: mapX(W, x) - pad + 'px', top: mapY(W, y) - pad + 'px', width: w * W.s + 2 * pad + 'px', height: h * W.s + 2 * pad + 'px', opacity: A, transform: '', clipPath: '' };
  switch (MO.hl) {
    case 'draw': st.clipPath = `inset(0 ${(1 - ex(prog(A, 0, 0.9))) * 100}% 0 0)`; st.opacity = A > 0 ? Math.min(1, A * 4) : 0; break;  // traced left→right
    case 'flash': st.transform = `scale(${lerp(1.18, 1, ex(A))})`; st.filter = `brightness(${1 + (1 - A) * 1.5})`; break;
    case 'soft': st.opacity = esoft(A) * 0.9; st.transform = `scale(${lerp(1.02, 1, esoft(A))})`; break;
    case 'bounce': st.transform = `scale(${lerp(0.6, 1, elastic(A))}) rotate(${lerp(-3, 0, eo(A))}deg)`; break;
    default: st.transform = `scale(${lerp(1.06, 1, eo(A))})`;
  }
  Object.assign(H.d.style, st);
}
function tag(W, zh, en) { return div('tag', W.ov, `<span class="tz">${zh}</span>${en ? `<em>${en}</em>` : ''}`); }
function posTag(W, T, x, y, a) { // display px: never scale tags by the crop factor
  const A = clamp(a), k = { snap: 0.94, punch: 1.3, soft: 0.96, elastic: 0.5 }[MO.pop] ?? 0.85;
  const s = MO.pop === 'elastic' ? lerp(k, 1, elastic(A)) : lerp(k, 1, ex(A));
  T.style.left = mapX(W, x) + 'px'; T.style.top = mapY(W, y) + 'px'; T.style.opacity = MO.pop === 'soft' ? esoft(A) : A;
  T.style.transform = `translate(-50%,-50%) translateY(${(1 - eo(A)) * (MO.enter === 'slide' ? 0 : 14)}px) scale(${s})`;
}
const CURSOR_SVG = '<svg viewBox="0 0 24 24" width="34" height="34"><path d="M4 2 L4 19 L8.6 14.9 L11.6 22 L14.6 20.7 L11.7 13.9 L18 13.9 Z" fill="#fff" stroke="#111" stroke-width="1.3" stroke-linejoin="round"/></svg>';
function cursor(W) { return { c: div('cursor', W.ov, CURSOR_SVG), r: div('ripple', W.ov) }; }
function posCursor(W, C, lt, path, clicks = [], vis = 1) {
  let x = path[0][1], y = path[0][2];
  for (let i = 0; i < path.length - 1; i++) { const [t0, x0, y0] = path[i], [t1, x1, y1] = path[i + 1]; if (lt >= t0) { const k = eio(prog(lt, t0, t1)); x = lerp(x0, x1, k); y = lerp(y0, y1, k); } }
  const X = mapX(W, x), Y = mapY(W, y);
  let press = 0, rip = -1;
  for (const c of clicks) { const d = lt - c; if (d >= -0.08 && d < 0.12) press = 1; if (d >= 0 && d < 0.55) rip = d; }
  C.c.style.left = X - 6 + 'px'; C.c.style.top = Y - 4 + 'px'; C.c.style.opacity = vis; C.c.style.transform = `scale(${press ? 0.86 : 1})`;
  if (rip >= 0) { C.r.style.left = X + 'px'; C.r.style.top = Y + 'px'; C.r.style.opacity = 1 - rip / 0.55; C.r.style.transform = `scale(${0.3 + rip * 2.2})`; } else C.r.style.opacity = 0;
}
function pic(parent, src, w, h, cls = 'abs pic') {
  const root = div(cls, parent); Object.assign(root.style, { width: w + 'px', height: h + 'px' }); root.dataset.qa = 'media';
  Object.assign(img(src, root).style, { width: '100%', height: '100%', objectFit: 'contain', display: 'block' });
  return root;
}
function clip(parent, src, w, h) { const root = div('abs pic clip', parent); root.dataset.qa = 'media'; Object.assign(root.style, { width: w + 'px', height: h + 'px' }); const v = vid(src, root); Object.assign(v.style, { width: '100%', height: '100%', objectFit: 'cover', display: 'block' }); return { root, v }; }
function clipTime(C, sec) { seekVideo(C.v, sec); }
function textEl(parent, html, css = {}) { const d = div('abs', parent, html); Object.assign(d.style, css); d.dataset.qa = 'text'; return d; }
function qaIgnore(el) { el.dataset.qa = 'ignore'; return el; }  // intentional overlap/off-frame (background walls, blurred backdrops)

// Deterministic video seeking: a frame waits until every touched <video> has finished seeking.
const PENDING = [];
function seekVideo(v, sec) {
  const target = Math.max(0, Math.min(sec, (v.duration || 1e9) - 0.04));
  if (Math.abs((v._t ?? -1) - target) < 1e-4) return;
  v._t = target;
  PENDING.push(new Promise((r) => { const done = () => { v.removeEventListener('seeked', done); r(); }; v.addEventListener('seeked', done); v.currentTime = target; setTimeout(r, 4000); }));
}

// ---------- backgrounds (one per style) ----------
const BG = {
  grid(host) {
    host.innerHTML = '<div class="bg-base"></div><div class="glow a"></div><div class="glow b"></div><div class="bg-grid"></div>';
    const [a, b, g] = [host.querySelector('.glow.a'), host.querySelector('.glow.b'), host.querySelector('.bg-grid')];
    return (t) => { place(a, { x: Math.sin(t * 0.11) * 400 - 200, y: Math.cos(t * 0.07) * 200 - 100 }); place(b, { x: Math.cos(t * 0.09) * 500 + 300, y: Math.sin(t * 0.06) * 260 + 120 }); g.style.transform = `translate(${-(t * 8) % 40}px, ${-(t * 4) % 40}px)`; };
  },
  keynote(host) {
    host.innerHTML = '<div class="bg-base"></div><div class="glow a"></div><div class="glow b"></div>';
    const [a, b] = [host.querySelector('.glow.a'), host.querySelector('.glow.b')];
    return (t) => { place(a, { x: Math.sin(t * 0.05) * 300 - 250, y: -200 + Math.cos(t * 0.04) * 80 }); place(b, { x: 380 + Math.cos(t * 0.06) * 220, y: 260 + Math.sin(t * 0.05) * 90 }); };
  },
  editorial(host) {
    host.innerHTML = '<div class="bg-base"></div><div class="rule h"></div><div class="rule v"></div><div class="mark"></div>';
    const [h, v, mark] = [host.querySelector('.rule.h'), host.querySelector('.rule.v'), host.querySelector('.mark')];
    return (t, ch) => { h.style.transform = `translateY(${Math.sin(t * 0.07) * 40}px)`; v.style.transform = `translateX(${Math.cos(t * 0.05) * 60}px)`; mark.textContent = ch ? ch[2] : ''; };
  },
  aurora(host) {
    host.innerHTML = '<div class="bg-base"></div>' + [0, 1, 2, 3].map((i) => `<div class="blob b${i}"></div>`).join('') + '<div class="bg-noise"></div>';
    const blobs = [...host.querySelectorAll('.blob')];
    return (t) => blobs.forEach((el, i) => place(el, { x: Math.sin(t * (0.07 + i * 0.02) + i * 1.7) * (380 + i * 60), y: Math.cos(t * (0.05 + i * 0.015) + i) * (220 + i * 40), s: 1 + 0.12 * Math.sin(t * 0.1 + i) }));
  },
  cyber(host) {
    host.innerHTML = '<div class="bg-base"></div><div class="floor"><div class="floor-grid"></div></div><div class="glow a"></div><div class="glow b"></div><div class="scan"></div>';
    const fg = host.querySelector('.floor-grid'), [a, b] = [host.querySelector('.glow.a'), host.querySelector('.glow.b')];
    return (t) => { fg.style.transform = `translateY(${(t * 60) % 80}px)`; place(a, { x: -520 + Math.sin(t * 0.1) * 120, y: -160 }); place(b, { x: 520 + Math.cos(t * 0.08) * 120, y: -120 }); };
  },
  luxe(host) {
    host.innerHTML = '<div class="bg-base"></div><div class="spot"></div><div class="floor"></div>';
    const spot = host.querySelector('.spot');
    return (t) => { spot.style.transform = `translateX(${Math.sin(t * 0.05) * 60}px) scale(${1 + 0.03 * Math.sin(t * 0.08)})`; };
  },
  natural(host) {
    host.innerHTML = '<div class="bg-base"></div><div class="sun"></div><div class="leaf"></div>';
    const [sun, leaf] = [host.querySelector('.sun'), host.querySelector('.leaf')];
    return (t) => { place(sun, { x: 420 + Math.sin(t * 0.04) * 80, y: -260 + Math.cos(t * 0.03) * 40 }); place(leaf, { x: -520 + Math.cos(t * 0.035) * 90, y: 300 + Math.sin(t * 0.05) * 50 }); };
  },
  paper(host) {
    host.innerHTML = '<div class="bg-base"></div><svg class="grain" width="1920" height="1080"><filter id="pg"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 0.35  0 0 0 0 0.3  0 0 0 0 0.25  0 0 0 0.08 0"/></filter><rect width="100%" height="100%" filter="url(#pg)"/></svg><div class="ink a"></div><div class="ink b"></div>';
    const [a, b] = [host.querySelector('.ink.a'), host.querySelector('.ink.b')];
    return (t) => { place(a, { x: -700 + Math.sin(t * 0.04) * 40, y: -380 }); place(b, { x: 760 + Math.cos(t * 0.05) * 40, y: 400 }); };
  },
};

// ---------- scenes + engine ----------
const SCENES = [];
// the director's cut: scenes the film writes itself (film.json "scripts"), registered as CUSTOM.<name> = (start, end, o) => {…}
// with the same API as the library (scene, win, setCrop, place, textEl, M.*, svg…); used as {"type": "custom", "fn": "<name>"}
const CUSTOM = {};
function scene(s, e, init, update) { SCENES.push({ s, e, init, update, shot: SHOT }); }

// camera cuts shared by all styles. p: 0→1 across the cut; inc = the incoming scene (drawn above the outgoing one)
//   whip  pan with motion blur      push   fly through the frame      slide-up  the next scene rises from below
//   wipe  a hard edge sweeps across  iris  a circle opens from the centre   zoom  the next scene settles from 125 %
//   blur  a defocus dissolve         dip   out to the background, then in (a breath)
//   doors split open: the next scene appears in a centre slit that opens to both edges
//   light a warm light leak blooms over the cut and the next scene appears through it    rack  focus pulls from the
//         outgoing scene (it blurs away) to the incoming one (it sharpens), with a slight scale breath
const CUT_KINDS = ['style', 'whip', 'push', 'slide-up', 'wipe', 'iris', 'zoom', 'blur', 'dip', 'doors', 'light', 'rack'];
function cutFX(root, kind, p, inc) {
  let tf = '', o = 1, filter = '', clip = '';
  if (CUT[kind]) {   // the film's own cut
    const r = CUT[kind]({ p, inc }) || {};
    root.style.opacity = r.opacity ?? 1; root.style.transform = r.transform || ''; root.style.filter = r.filter || ''; root.style.clipPath = r.clipPath || '';
    return;
  }
  if (kind === 'slide-up') {
    const e = eio(p); tf = `translateY(${inc ? (1 - e) * 1080 : -e * 540}px)`; o = inc ? 1 : 1 - prog(p, 0.3, 1);
    const sp = Math.sin(Math.PI * p); if (sp > 0.05) filter = `blur(${(sp * 5).toFixed(1)}px)`;
  } else if (kind === 'wipe') {
    if (inc) clip = `inset(0 0 0 ${((1 - eio(p)) * 100).toFixed(2)}%)`;
  } else if (kind === 'iris') {
    if (inc) clip = `circle(${(eio(p) * 115).toFixed(2)}% at 50% 50%)`;
  } else if (kind === 'zoom') {
    if (inc) { tf = `scale(${lerp(1.25, 1, eo(p)).toFixed(4)})`; o = prog(p, 0, 0.6); }
    else { tf = `scale(${lerp(1, 0.92, eio(p)).toFixed(4)})`; o = 1 - prog(p, 0.3, 1); }
  } else if (kind === 'blur') {
    const sp = Math.sin(Math.PI * p); filter = `blur(${(sp * 16).toFixed(1)}px)`; o = inc ? prog(p, 0.25, 0.75) : 1 - prog(p, 0.25, 0.75);
  } else if (kind === 'dip') {
    o = inc ? prog(p, 0.55, 1) : 1 - prog(p, 0, 0.45);
  } else if (kind === 'doors') {   // split open: the incoming scene appears in a centre slit that opens to both edges
    if (inc) { const x = ((1 - eio(p)) * 50).toFixed(2); clip = `inset(0 ${x}% 0 ${x}%)`; }
    else tf = `scale(${lerp(1, 0.97, eio(p)).toFixed(4)})`;
  } else if (kind === 'light') {   // brightness bloom on both sides of the cut, the light carries the change
    const sp = Math.sin(Math.PI * p); filter = `brightness(${(1 + sp * 1.4).toFixed(3)}) saturate(${(1 - sp * 0.3).toFixed(3)}) blur(${(sp * 3).toFixed(1)}px)`;
    o = inc ? prog(p, 0.4, 0.6) : 1 - prog(p, 0.4, 0.6);
  } else if (kind === 'rack') {
    const b = inc ? (1 - prog(p, 0.4, 1)) * 14 : prog(p, 0, 0.6) * 14; filter = `blur(${b.toFixed(1)}px)`;
    tf = `scale(${inc ? lerp(1.03, 1, eo(prog(p, 0.4, 1))).toFixed(4) : lerp(1, 0.985, p).toFixed(4)})`; o = inc ? prog(p, 0.3, 0.6) : 1 - prog(p, 0.45, 0.75);
  } else if (kind === 'whip') {
    const e = eio(p); tf = `translateX(${inc ? (1 - e) * 1920 : -e * 1920}px)`;
    const sp = Math.sin(Math.PI * p); if (sp > 0.05) filter = `blur(${(sp * (CONFIG.CINEMA && CONFIG.CINEMA.mb > 1 ? 4 : 10)).toFixed(1)}px)`;  // smooths the steps between motion-blur samples
  } else {  // push
    if (inc) { tf = `scale(${lerp(0.8, 1, eo(prog(p, 0.3, 1)))})`; o = prog(p, 0.35, 0.75); filter = `blur(${((1 - prog(p, 0.35, 0.9)) * 8).toFixed(1)}px)`; }
    else { tf = `scale(${lerp(1, 1.7, Math.pow(p, 1.6))})`; o = 1 - prog(p, 0.3, 0.65); filter = `blur(${(prog(p, 0.2, 0.7) * 10).toFixed(1)}px)`; }
  }
  root.style.opacity = o; root.style.transform = tf; root.style.filter = filter; root.style.clipPath = clip;
}
const CUT_LEN = { whip: 1, push: 1, 'slide-up': 1.2, wipe: 1.4, iris: 1.5, zoom: 1.2, blur: 1.6, dip: 2, doors: 1.5, light: 1.6, rack: 1.8 };   // × the style's crossfade
function transitionFX(root, t, s, e, DUR, kIn = 'style', kOut = 'style') { // per-style look of a scene's in/out edge
  const len = (k) => (CUT[k] && CUT[k].len) || CUT_LEN[k] || 1;
  const wi = ST.xf * 0.9 * len(kIn), wo = ST.xf * 0.9 * len(kOut);
  if (s > 0 && kIn !== 'style' && t < s + wi) return cutFX(root, kIn, prog(t, s - wi, s + wi), true);
  if (e < DUR && kOut !== 'style' && t > e - wo) return cutFX(root, kOut, prog(t, e - wo, e + wo), false);
  const xf = ST.xf, inP = s === 0 ? 1 : prog(t, s - xf, s + xf * 0.4), outP = e >= DUR ? 1 : 1 - prog(t, e - xf * 0.4, e + xf);
  let o = Math.min(inP, outP), tf = '', filter = '', clipPath = '';
  const edgeIn = 1 - inP, edgeOut = 1 - outP;
  switch (ST.transition) {
    case 'zoom': tf = `scale(${1 - edgeIn * 0.06 + edgeOut * 0.08})`; filter = `blur(${(edgeIn + edgeOut) * 6}px)`; break;
    case 'wipe': if (edgeIn > 0) clipPath = `inset(0 0 0 ${edgeIn * 100}%)`; o = outP; break;
    case 'glitch': { const g = Math.max(edgeIn, edgeOut); if (g > 0.05) { tf = `translateX(${Math.sin(t * 173) * 24 * g}px)`; filter = `drop-shadow(${8 * g}px 0 0 rgba(255,0,90,0.8)) drop-shadow(${-8 * g}px 0 0 rgba(0,240,255,0.8))`; } break; }
    case 'page': tf = `translateY(${edgeIn * 40 - edgeOut * 30}px)`; break;
    default: break; // 'fade' and 'flash' (flash is drawn on #flash)
  }
  root.style.opacity = o; root.style.transform = tf; root.style.filter = filter; root.style.clipPath = clipPath;
}

const FILM = {
  start() {
    const { DUR, FADE_OUT, CHORUS_BARS, CHAPTERS, ONSCREEN } = CONFIG;
    const onscreen = new Set(ONSCREEN || []);
    const chorus = (CHORUS_BARS || []).map(([a, b]) => [bar(a), bar(b)]);
    const chapters = (CHAPTERS || []).map(([a, b, n, z, e]) => [bar(a), bar(b), n, z, e]);
    const $ = (id) => document.getElementById(id);
    document.body.dataset.style = ST.id || CONFIG.STYLE; document.body.dataset.motion = MO_ID;
    // the colour director's palette (film.json "palette", scripts/palette.py) replaces the style's accents; background and ink stay
    const PAL = CONFIG.PALETTE || {};
    if (PAL.accent) document.documentElement.style.setProperty('--accent', PAL.accent);
    if (PAL.accent2) document.documentElement.style.setProperty('--accent-2', PAL.accent2);
    const bgUpdate = (BG[ST.background] || BG.grid)($('bg'));
    const host = $('scenes');
    for (const sc of SCENES) { sc.root = div('scene', host); sc.S = {}; useShot(sc.shot); const v0 = VIDS.length; sc.init(sc.root, sc.S); sc.vids = VIDS.slice(v0); }
    useShot(null);
    FX.init.forEach((f) => f());
    const illus = (CONFIG.ILLUSTRATIVE || []).map(([a, b]) => [bar(a), bar(b)]), illusEl = $('illus');   // a UI redrawn in code is always labelled
    if (illusEl) illusEl.textContent = CONFIG.ILLUS_LABEL || '界面示意 · Illustrative UI';
    const chapter = $('chapter'), capzh = $('capzh'), capen = $('capen'), capband = $('capband'), flash = $('flash'), pulse = $('pulse');
    const cuts = SCENES.map((s) => s.s).filter((s) => s > 0);
    window.renderFrame = (t) => {
      PENDING.length = 0;
      for (let i = 0; i < SCENES.length; i++) {
        const sc = SCENES[i];
        const vis = t >= sc.s - ST.xf * 2 && t < sc.e + ST.xf * 2;   // long cuts (dip, blur) reach ~2× the crossfade
        sc.root.style.display = vis ? 'block' : 'none';
        if (!vis) continue;
        useShot(sc.shot);
        transitionFX(sc.root, t, sc.s, sc.e, DUR, CUTS[i] || 'style', CUTS[i + 1] || 'style');
        const cam = M.camera(t, t - sc.s, sc.e - sc.s, sc.shot.camera);
        if (cam) sc.root.style.transform = (sc.root.style.transform || '') + ' ' + cam;
        sc.update(sc.S, t - sc.s, sc.e - sc.s, t);
        // footage plays with the scene, from the moment the director picked ("offset", scripts/footage.py), at "rate"
        if (!sc.S.ownVideo) for (const v of sc.vids) seekVideo(v, Math.max(0, (sc.shot.offset || 0) + (t - sc.s) * (sc.shot.rate || 1)));
        FX.scene.forEach((f) => f(sc, t, t - sc.s));
      }
      useShot(null);
      const ch = chapters.find(([a, b]) => t >= a && t < b);
      bgUpdate(t, ch);
      FX.frame.forEach((f) => f(t));
      const beat = CONFIG.BAR / 4, ph = (((t - CONFIG.G) % beat) + beat) % beat, inCh = chorus.some(([a, b]) => t >= a && t < b);
      pulse.style.opacity = inCh && ST.pulse !== 'none' ? Math.exp(-ph * 9) * (ST.pulse === 'flash' ? 0.5 : 0.9) : 0;
      const near = cuts.reduce((m, c) => Math.min(m, Math.abs(t - c)), 99);
      flash.style.opacity = ST.transition === 'flash' || ST.transition === 'glitch' ? Math.exp(-near * 14) * 0.55 : 0;
      if (ch) {
        chapter.querySelector('b').textContent = ch[2]; chapter.querySelector('.z').textContent = ch[3]; chapter.querySelector('.e').textContent = ch[4];
        chapter.style.opacity = Math.min(prog(t, ch[0] + 0.2, ch[0] + 0.7), 1 - prog(t, ch[1] - 0.35, ch[1]));
      } else chapter.style.opacity = 0;
      if (illusEl) { const r = illus.find(([a, b]) => t >= a - 0.3 && t < b + 0.3); illusEl.style.opacity = r ? Math.min(prog(t, r[0] - 0.3, r[0]), 1 - prog(t, r[1], r[1] + 0.3)) : 0; }
      const c = (window.VO || []).find((v) => !onscreen.has(v.id) && t >= v.s - 0.1 && t < v.e + 0.45);
      if (c) {
        const a = Math.min(prog(t, c.s - 0.1, c.s + 0.2), 1 - prog(t, c.e + 0.15, c.e + 0.45));
        capzh.textContent = c.zh || ''; capen.textContent = c.en || '';
        capzh.style.opacity = capen.style.opacity = capband.style.opacity = a;
        capzh.style.transform = capen.style.transform = `translateY(${(1 - eo(prog(t, c.s - 0.1, c.s + 0.35))) * 10}px)`;
      } else capzh.style.opacity = capen.style.opacity = capband.style.opacity = 0;
      $('fade').style.opacity = Math.max(1 - prog(t, 0, 0.9), prog(t, DUR - FADE_OUT, DUR));
      return PENDING.length ? Promise.all(PENDING) : undefined;
    };
    // Motion probe for the renderer: how far (px) anything on screen moves between t-dt and t+dt.
    // render.mjs renders extra motion-blur samples only where this is ≥ ~1.5 px — holds and fades cost one sample.
    const probeEls = () => [...host.querySelectorAll('[data-qa="media"], [data-qa="text"], .win, .pic')];
    window.motionAt = async (t, dt) => {
      const els = probeEls(), snap = () => els.map((e) => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; });
      await window.renderFrame(Math.max(0, t - dt)); const a = snap();
      await window.renderFrame(t + dt); const b = snap();
      let m = 0; for (let i = 0; i < a.length; i++) for (let j = 0; j < 4; j++) m = Math.max(m, Math.abs(a[i][j] - b[i][j]));
      return m;
    };
    window.ready = (async () => {
      await document.fonts.ready;
      // a long product name never runs off the frame: every display title is measured once and shrunk to the safe width
      for (const sc of SCENES) {
        const was = sc.root.style.display; sc.root.style.display = 'block';
        for (const el of sc.root.querySelectorAll('.h-display')) {
          const max = 1920 - 2 * 96 - 40, w = el.scrollWidth;
          if (w > max) { const fs = parseFloat(getComputedStyle(el).fontSize); el.style.fontSize = (fs * max / w).toFixed(1) + 'px'; }
        }
        sc.root.style.display = was;
      }
      await Promise.all(IMGS.map((i) => (i.complete ? null : new Promise((r) => { i.onload = i.onerror = r; }))));
      await Promise.all(IMGS.map((i) => i.decode().catch(() => {})));
      await Promise.all(VIDS.map((v) => (v.readyState >= 2 ? null : new Promise((r) => { v.onloadeddata = v.onerror = r; setTimeout(r, 8000); }))));
      await window.renderFrame(0);
      return [...IMGS.filter((i) => !i.naturalWidth).map((i) => i.src), ...VIDS.filter((v) => !v.videoWidth).map((v) => v.src)];
    })();
  },
};
