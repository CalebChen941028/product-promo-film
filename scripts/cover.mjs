// Cover poster = one frame of the film rendered at 2× (3840×2160).
// Usage: node cover.mjs <film.html> <out.png> [t=4.2]   (pick t where the cover scene is fully built)
// Then a thumbnail: python -c "from PIL import Image; Image.open('out.png').convert('RGB').resize((1280,720)).save('cover-1280.jpg', quality=92)"
import { chromium } from 'playwright';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [html, out, t = '4.2'] = process.argv.slice(2);
const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
await page.goto(pathToFileURL(path.resolve(html)).href);
await page.evaluate(() => window.ready);
await page.evaluate((tt) => window.renderFrame(tt), Number(t));
await page.screenshot({ path: out });
await browser.close();
console.log('cover', out);
