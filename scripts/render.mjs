// Deterministic frame renderer for a film page that exposes window.ready (Promise) and window.renderFrame(t).
// Usage:
//   node render.mjs stills <film.html> <outDir> <t1> <t2> ...
//   node render.mjs video  <film.html> <outPrefix> <ffmpeg> <durationSec> [workers=6] [fps=30] [samples=1] [from=0]
//     from = start second (render only from..durationSec, e.g. to check one cut)
//     samples > 1 = real motion blur: each output frame averages `samples` renders spread over a 180° shutter
//     (half the frame interval), exactly what a film camera records. Cost: samples × render time.
//     → <outPrefix>.partN.mp4 + <outPrefix>.list.txt, then:
//   ffmpeg -f concat -safe 0 -i <outPrefix>.list.txt -i mix.wav -map 0:v -map 1:a -c:v copy \
//          -af loudnorm=I=-14:TP=-1.0:LRA=11 -ar 48000 -c:a aac -b:a 256k -movflags +faststart -shortest film.mp4
// Memory: each worker holds every image the page loads. Pre-scale captures to their largest on-screen size,
// or lower the worker count, if the machine starts swapping (frames slow to seconds each).
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [mode, html, out, ...rest] = process.argv.slice(2);
const url = pathToFileURL(path.resolve(html)).href;
const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--allow-file-access-from-files'] });
async function openPage() {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => console.error('pageerror', e.message));
  await page.goto(url);
  const missing = await page.evaluate(() => window.ready);
  if (Array.isArray(missing) && missing.length) console.error('missing images', missing);
  return page;
}
const grab = async (page, t) => { await page.evaluate((tt) => window.renderFrame(tt), t); return page.screenshot({ type: 'png' }); };

if (mode === 'stills') {
  mkdirSync(out, { recursive: true });
  const page = await openPage();
  for (const ts of rest) writeFileSync(path.join(out, `t${Number(ts).toFixed(2).padStart(6, '0')}.png`), await grab(page, Number(ts)));
} else if (mode === 'video') {
  const [ffmpeg, durArg, workersArg, fpsArg, samplesArg, fromArg] = rest;
  const FROM = Number(fromArg || 0);
  const N = Math.max(1, Number(samplesArg || 1)), SHUTTER = 0.5;
  const FPS = Number(fpsArg || 30), workers = Number(workersArg || 6), total = Math.round(FPS * (Number(durArg) - FROM)), per = Math.ceil(total / workers);
  const parts = [];
  await Promise.all(Array.from({ length: workers }, async (_, w) => {
    const f0 = w * per, f1 = Math.min(total, f0 + per), part = `${out}.part${w}.mp4`;
    parts[w] = part;
    const blur = N > 1 ? ['-vf', `tmix=frames=${N},select='eq(mod(n,${N}),${N - 1})',setpts=N/(${FPS}*TB)`, '-r', String(FPS)] : [];
    const ff = spawn(ffmpeg, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS * N), '-c:v', 'png', '-i', '-', ...blur,
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', part], { stdio: ['pipe', 'inherit', 'inherit'] });
    const done = new Promise((res, rej) => ff.on('close', (c) => (c === 0 ? res() : rej(new Error('ffmpeg ' + c)))));
    const page = await openPage();
    let blurred = 0;
    for (let f = f0; f < f1; f++) {
      const tc = FROM + f / FPS;
      // adaptive motion blur: only frames where something moves ≥ 1.5 px across the shutter get N samples
      const moving = N > 1 && (await page.evaluate(([t, d]) => (window.motionAt ? window.motionAt(t, d) : 99), [tc, SHUTTER / FPS / 2])) >= 1.5;
      let still = null;
      for (let k = 0; k < N; k++) {
        const t = Math.min(Number(durArg), Math.max(0, tc + (moving ? ((k - (N - 1) / 2) / N) * SHUTTER / FPS : 0)));
        const buf = moving || !still ? await grab(page, t) : still;
        if (!moving) still = buf;
        if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
      }
      if (moving) blurred++;
      if ((f - f0) % 300 === 0) console.log(`worker ${w}: frame ${f}/${f1}`);
    }
    ff.stdin.end(); await done;
    if (N > 1) console.log(`worker ${w}: ${blurred}/${f1 - f0} frames moving → ${N} motion-blur samples`);
  }));
  writeFileSync(`${out}.list.txt`, parts.map((p) => `file '${path.resolve(p)}'`).join('\n'));
  console.log('parts done');
}
await browser.close();
