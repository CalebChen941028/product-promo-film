// MedStat Pilot film v2 — beat grid of the music (120 BPM): beats at G + 0.5k s, bars at G + 2b s.
// Narration and captions come from narration.json via make_vo.py (vo_timing.js).
const G = 0.4876;
const bar = (b) => G + 2 * b;
if (typeof window !== 'undefined') Object.assign(window, { G, bar });
