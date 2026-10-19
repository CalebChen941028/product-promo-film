// Film configuration — the only file most films need to change besides scenes.js.
// Times are on the music's bar grid: G and BAR come from scripts/beat_grid.py; DUR = final music length.
const CONFIG = {
  STYLE: 'midnight-tech',   // look:   midnight-tech | keynote-light | editorial-mono | aurora-glass | neon-cyber | paper-academic
  MOTION: '',               // motion: cinematic-3d | precision-data | kinetic-launch | gentle-story | playful-pop | editorial-type
                            //         '' = the style's default; pick by theme with scripts/recommend_style.py
  G: 0.4876,                // first beat offset (s)
  BAR: 2.0,                 // seconds per bar (4 beats); 120 BPM → 2.0
  DUR: 56,                  // film length (s) — the example storyboard below is 28 bars
  FADE_OUT: 2.6,
  CHORUS_BARS: [[10, 22]],  // background pulses on every beat inside these bar ranges
  // Chapter label: [fromBar, toBar, number, Chinese, ENGLISH]
  CHAPTERS: [[3, 10, '01', '功能', 'FEATURES'], [10, 19, '02', '能力', 'CAPABILITIES'], [19, 22, '03', '创新', 'WHAT IS NEW']],
  ONSCREEN: ['tagline', 'motto'], // spoken lines that are typeset on screen → no bottom caption
  SHOTS: 'assets/',         // captures / user screenshots folder (real film: '../capture/shots/' or '../materials/')
  ASSETS: 'assets/',
  // Brand & copy — scenes read these, so a new product = new values here (from the brief).
  BRAND: {
    name: 'Product', nameAccent: 'Name', logo: 'assets/logo.png',
    positioningZh: '一句话产品定位', positioningEn: 'ONE-LINE POSITIONING',
    taglineZh: '从数据，到发现', taglineEn: 'FROM DATA TO DISCOVERY',
    motto: ['一句理念，第一行——', '第二行落在重点上。', 'The motto in English — one sentence, plainly said.'],
    contacts: [['DEVELOPER', '开发者', '姓名', 'email@example.com'], ['WECHAT', '公众号', '公众号名', 'Official account'], ['GITHUB', '主页', 'username', 'github.com/username']],
    chips: ['macOS · Apple silicon', 'Windows · x64', 'Beta'],
  },
  // Media used by the example scenes (paths relative to film.html). Replace with the user's materials.
  MEDIA: {
    ui: 'assets/ui-sample.png',                 // a 2× desktop capture (base 1920×1080)
    plots: ['assets/plot-1.png', 'assets/plot-2.png', 'assets/plot-3.png'],
    clip: 'assets/clip.webm',                   // user video → scripts/intake.py converts to WebM
    phone: { src: 'assets/phone.png', base: [393, 852] }, // mobile screenshot + its point size
  },
};
const bar = (b) => CONFIG.G + CONFIG.BAR * b;
if (typeof window !== 'undefined') Object.assign(window, { CONFIG, bar });
