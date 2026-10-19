'use strict';
// Cinema layer: what a film director adds on top of good motion graphics. Deterministic, all a function of t.
//   COLOUR SCRIPT  each scene has a mood (cold → neutral → peak → warm); colour and exposure glide between
//                  moods, so the film has an emotional arc and not one flat grade.
//   LENS           handheld micro-drift, shallow depth of field at the frame edges (backdrop blur),
//                  a focus pull as each scene lands, and a camera kick on hit points.
//   LIGHT          a glint sweeping across every window, light rays behind the logo, an anamorphic flare
//                  on hit points, warm light leaks at cuts (gentle/playful), and floating bokeh for depth.
//   CUTS           'whip' (pan with motion blur) and 'push' (camera flies through the frame) in engine.js.
// Driven by CONFIG.CINEMA, which make_film.py writes from film.json ("cinema" + per-scene "mood", "cut", "hit").
// The grade (LUT), bloom, grain, motion blur and sound design are applied after rendering (make_film.py finish).
const CIN = (() => {
  const C = CONFIG.CINEMA;
  if (!C || C.on === false) return { on: false };
  // per motion language: how the camera and the light behave (the theme decides the lens, not just the look).
  // Restraint is the default: effects sit just under the threshold of notice. Premium = felt, not seen.
  // The flare fires on the ONE hero moment only; leaks and bokeh are opt-in (cinema.lens) for playful/soft briefs.
  const LENS = {
    'cinematic-3d':   { shake: 0.55, hz: 0.28, dof: 2.5, pull: 3, glint: 0.6, flare: 0.55, kick: 0.012, leak: 0, bokeh: 0 },
    'precision-data': { shake: 0,    hz: 0,    dof: 0,   pull: 0, glint: 0.4, flare: 0,    kick: 0.004, leak: 0, bokeh: 0 },
    'kinetic-launch': { shake: 0.45, hz: 0.7,  dof: 1.5, pull: 0, glint: 0.6, flare: 0.6,  kick: 0.022, leak: 0, bokeh: 0 },
    'gentle-story':   { shake: 0.8,  hz: 0.18, dof: 3,   pull: 4, glint: 0.5, flare: 0.35, kick: 0.006, leak: 0, bokeh: 0 },
    'playful-pop':    { shake: 0.35, hz: 0.45, dof: 1.5, pull: 0, glint: 0.6, flare: 0.35, kick: 0.016, leak: 0, bokeh: 0 },
    'editorial-type': { shake: 0,    hz: 0,    dof: 0,   pull: 0, glint: 0,   flare: 0,    kick: 0.005, leak: 0, bokeh: 0 },
  };
  const L = Object.assign({}, LENS[MO_ID] || LENS['cinematic-3d'], C.lens || {});
  const light = !!ST.light;   // light-background styles: light effects are tinted and gentler
  // moods: saturation, brightness, contrast, tint colour (soft-light) and tint strength
  const MOODS = {
    cold:    { sat: 0.62, bri: light ? 0.98 : 0.86, con: 1.03, tint: [80, 120, 190], k: 0.22 },
    neutral: { sat: 1,    bri: 1,    con: 1,    tint: [128, 128, 128], k: 0 },
    peak:    { sat: 1.07, bri: 1.02, con: 1.04, tint: null, k: 0.07 },   // tint = the accent colour
    warm:    { sat: 1.02, bri: 1.01, con: 1,    tint: [255, 176, 110], k: 0.1 },
    night:   { sat: 0.88, bri: light ? 0.96 : 0.88, con: 1.06, tint: [40, 30, 120], k: 0.18 },
  };
  const $ = (id) => document.getElementById(id);
  const css = getComputedStyle(document.documentElement);
  const hexRGB = (h) => { const m = (h || '').trim().match(/^#?([0-9a-f]{6})$/i); if (!m) return [46, 230, 197]; const n = parseInt(m[1], 16); return [n >> 16, (n >> 8) & 255, n & 255]; };
  const ACC = hexRGB(css.getPropertyValue('--accent'));
  MOODS.peak.tint = ACC;

  // seeded random for bokeh positions (deterministic across workers)
  let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  return {
    on: true, L, light,
    init() {
      const st = $('stage');
      const mk = (id, before) => { const d = document.createElement('div'); d.id = id; st.insertBefore(d, before ? $(before) : null); return d; };
      this.grade = mk('grade', 'flash'); this.dof = mk('dof', 'flash'); this.rays = mk('rays', 'flash'); this.leak = mk('leak', 'flash'); this.flare = mk('flare', 'flash');
      this.flare.innerHTML = '<i class="streak"></i><i class="core"></i>';
      if (L.dof > 0) { this.dof.style.backdropFilter = this.dof.style.webkitBackdropFilter = `blur(${L.dof}px)`; } else this.dof.style.display = 'none';
      const blend = light ? 'normal' : 'screen';
      this.rays.style.mixBlendMode = this.flare.style.mixBlendMode = blend;
      this.leak.style.mixBlendMode = light ? 'multiply' : 'screen';
      // bokeh: soft out-of-focus lights at three depths (dark styles only)
      this.bokeh = [];
      if (!light && L.bokeh > 0) {
        const host = document.createElement('div'); host.className = 'bokeh'; $('bg').appendChild(host);
        for (let i = 0; i < 16; i++) {
          const depth = 0.3 + rnd() * 0.7, size = 24 + depth * 70, b = document.createElement('i');
          Object.assign(b.style, { width: size + 'px', height: size + 'px', filter: `blur(${(4 + (1 - depth) * 14).toFixed(1)}px)`,
            background: `radial-gradient(circle, ${rnd() > 0.4 ? `rgba(${ACC.join(',')},0.9)` : 'rgba(255,255,255,0.8)'} 0%, transparent 70%)` });
          host.appendChild(b); this.bokeh.push({ b, depth, op: (0.06 + rnd() * 0.12) * L.bokeh, x0: rnd() * 2200 - 1100, y0: rnd() * 1300 - 650, ph: rnd() * 6.28 });
        }
      }
      this.scenes = $('scenes');
    },
    moodAt(t) {
      const M = C.moods || [];
      const at = (m) => MOODS[m] || MOODS.neutral;
      let i = M.findIndex(([a, b]) => t >= a && t < b);
      if (i < 0) return MOODS.neutral;
      const cur = at(M[i][2]), [a, b] = M[i];
      const blendW = 0.45;   // glide across a cut over ~0.9 s
      if (i > 0 && t < a + blendW) { const p = esoft(prog(t, a - blendW, a + blendW)); return this.mix(at(M[i - 1][2]), cur, p); }
      if (i < M.length - 1 && t > b - blendW) { const p = esoft(prog(t, b - blendW, b + blendW)); return this.mix(cur, at(M[i + 1][2]), p); }
      return cur;
    },
    mix(A, B, p) {
      const ta = A.tint || [128, 128, 128], tb = B.tint || [128, 128, 128];
      return { sat: lerp(A.sat, B.sat, p), bri: lerp(A.bri, B.bri, p), con: lerp(A.con, B.con, p), tint: ta.map((v, j) => lerp(v, tb[j], p)), k: lerp(A.k, B.k, p) };
    },
    // engine hook: per visible scene, after its transition and camera
    scene(sc, t, lt) {
      // focus pull as the scene lands (not on the first scene)
      if (L.pull > 0 && sc.s > 0) {
        const b = L.pull * (1 - eo(prog(lt, -0.15, 0.55)));
        if (b > 0.05) sc.root.style.filter = (sc.root.style.filter || '') + ` blur(${b.toFixed(2)}px)`;
      }
      // glint: a diagonal light sweep across each window shortly after it arrives
      if (L.glint > 0) {
        sc._gl = sc._gl || [...sc.root.querySelectorAll('.glint')];
        sc._gl.forEach((g, k) => {
          const p = prog(lt, 0.4 + k * 0.14, 1.35 + k * 0.14);
          g.style.transform = `translateX(${lerp(-120, 120, eio(p))}%)`;
          g.style.opacity = p > 0 && p < 1 ? L.glint * (light ? 0.6 : 1) : 0;
        });
      }
    },
    // engine hook: once per frame, after all scenes
    frame(t) {
      // colour script
      const m = this.moodAt(t);
      const f = Math.abs(m.sat - 1) + Math.abs(m.bri - 1) + Math.abs(m.con - 1) > 0.005 ? `saturate(${m.sat.toFixed(3)}) brightness(${m.bri.toFixed(3)}) contrast(${m.con.toFixed(3)})` : '';
      this.scenes.style.filter = f; $('bg').style.filter = f;
      this.grade.style.background = `rgb(${m.tint.map((v) => Math.round(v)).join(',')})`; this.grade.style.opacity = m.k;
      // lens: handheld drift + camera kick on hits
      const hits = C.hits || [];
      let kick = 0; for (const h of hits) { const d = t - h; if (d >= 0 && d < 1.2) kick = Math.max(kick, Math.exp(-d * 6) * (1 - Math.exp(-d * 60))); }
      const A = L.shake, w = 2 * Math.PI * (L.hz || 0.3);
      const sx = A * (1.1 * Math.sin(w * t + 1.3) + 0.5 * Math.sin(w * 2.31 * t + 0.4) + 0.2 * Math.sin(w * 4.7 * t + 2.2));
      const sy = A * (0.9 * Math.sin(w * 0.87 * t + 2.1) + 0.45 * Math.sin(w * 1.93 * t + 0.9) + 0.15 * Math.sin(w * 5.3 * t));
      const rz = A * 0.035 * Math.sin(w * 0.61 * t + 0.7);
      this.scenes.style.transform = A || kick ? `translate(${sx.toFixed(2)}px,${sy.toFixed(2)}px) rotate(${rz.toFixed(4)}deg) scale(${(1 + L.kick * kick).toFixed(4)})` : '';
      // light rays behind the logo / tagline
      const r = (C.rays || []).find(([a, b]) => t >= a - 0.5 && t < b + 0.5);
      if (r) {
        const [a, b, y, lvl = 1] = r;
        this.rays.style.opacity = (light ? 0.07 : 0.16) * lvl * Math.min(prog(t, a, a + 1.2), 1 - prog(t, b - 0.6, b));
        this.rays.style.transform = `translate(-50%,-50%) translateY(${y}px) rotate(${(t * 2.2).toFixed(2)}deg)`;
      } else this.rays.style.opacity = 0;
      // anamorphic flare on the hero moment only (one per film)
      let fl = 0; for (const h of (C.hero != null ? [C.hero] : [])) { const d = t - h; if (d > -0.06 && d < 0.9) fl = Math.max(fl, d < 0 ? (d + 0.06) / 0.06 : Math.exp(-d * 4.5)); }
      this.flare.style.opacity = fl * L.flare * (light ? 0.4 : 0.8);
      this.flare.firstChild.style.transform = `scaleX(${lerp(0.35, 1.15, eo(clamp(1 - fl)))})`;   // streak stretches, core stays round
      // warm light leak sweeping across cuts
      if (L.leak > 0) {
        const cuts = C.cuts_t || []; let lk = 0, lx = 0;
        for (const c of cuts) { const p = prog(t, c - 0.5, c + 0.7); if (p > 0 && p < 1) { lk = Math.sin(Math.PI * p); lx = lerp(-900, 900, p); } }
        this.leak.style.opacity = lk * L.leak * (light ? 0.22 : 0.5);
        this.leak.style.transform = `translate(-50%,-50%) translateX(${lx}px)`;
      }
      // bokeh drift with parallax against the handheld camera
      for (const o of this.bokeh) {
        let y = o.y0 - t * 9 * o.depth; y = ((y + 700) % 1400 + 1400) % 1400 - 700;
        place(o.b, { x: o.x0 + Math.sin(t * 0.07 + o.ph) * 40 * o.depth - sx * o.depth * 2, y: y - sy * o.depth * 2,
                     o: o.op * (0.75 + 0.25 * Math.sin(t * 0.9 + o.ph)) });
      }
    },
  };
})();
if (CIN.on) { FX.init.push(() => CIN.init()); FX.scene.push((sc, t, lt) => CIN.scene(sc, t, lt)); FX.frame.push((t) => CIN.frame(t)); }
