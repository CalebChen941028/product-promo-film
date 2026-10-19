// Captures native MedStat Pilot UI (web build at :5173, R backend at :8001) for the promo film.
// Usage: node shoot.mjs <scenario> [more scenarios]   → PNGs in capture/shots (1920×1080 CSS px at 2×)
// AI features point at the local model on :11434 (mock_llm.mjs), exactly as an Ollama user would configure it.
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(here, 'shots');
const DATA = path.join(here, '..', 'data');
fs.mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch();
async function boot({ dpr = 2, locale = 'zh-CN' } = {}) {
  const ctx = await browser.newContext({ acceptDownloads: true, viewport: { width: 1920, height: 1080 }, deviceScaleFactor: dpr, locale });
  await ctx.addInitScript((loc) => {
    try {
      localStorage.setItem('medstat_ai_config', JSON.stringify({ provider: 'ollama', model: 'qwen3.5:9b', base_url: 'http://localhost:11434/v1', api_key: '' }));
      localStorage.setItem('medstat_locale', loc);
    } catch {}
  }, locale);
  const page = await ctx.newPage();
  page.on('pageerror', e => console.error('pageerror', e.message));
  await page.goto('http://localhost:5173/');
  await page.waitForTimeout(1800);
  return page;
}
const T = (page, text, exact = true) => page.getByText(text, { exact }).first();
async function click(page, text, { exact = true, wait = 600 } = {}) { await T(page, text, exact).click({ timeout: 10000 }); await page.waitForTimeout(wait); }
async function shot(page, name, clip) {
  await page.screenshot({ path: path.join(OUT, `${name}.png`), ...(clip ? { clip } : {}) });
  console.log('shot', name);
}
async function seq(page, name, ms, every = 120, clip) {
  const dir = path.join(OUT, name); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const t0 = Date.now(); let k = 0;
  while (Date.now() - t0 < ms) {
    const t = Date.now() - t0;
    await page.screenshot({ path: path.join(dir, `${String(k++).padStart(4, '0')}_${String(t).padStart(6, '0')}.png`), ...(clip ? { clip } : {}) });
    await page.waitForTimeout(every);
  }
  console.log('seq', name, k);
}
async function load(page, file = 'demo_trial.csv') {
  await page.setInputFiles('input[type=file]', path.join(DATA, file));
  await page.waitForTimeout(1200);
}
async function parse(page) { await click(page, '开始解析', { wait: 4000 }); await click(page, '稍后保存', { wait: 1500 }); }
async function toAnalysis(page) { await page.locator("button:has-text('开始分析')").first().click(); await page.waitForTimeout(3000); }
async function assign(page, v, slot) { await click(page, v, { wait: 350 }); await click(page, slot, { wait: 500 }); }
async function run(page, extra = 6000) {
  await click(page, '运行分析', { wait: 1500 });
  await page.getByText('APA', { exact: false }).first().waitFor({ timeout: 120000 }).catch(() => {});
  await page.waitForTimeout(extra);
}
async function method(page, label) { await click(page, label, { wait: 1500 }); }
const hideBot = (page) => page.addStyleTag({ content: '' });

const scenarios = {
  async home() {
    const page = await boot();
    await shot(page, 'home');
    await load(page);
    await shot(page, 'home_file');
    await click(page, '开始解析', { wait: 4000 });
    await shot(page, 'save_prompt');
    await click(page, '稍后保存', { wait: 1500 });
    await shot(page, 'variables');
    await click(page, '📊 查看数据', { wait: 2500 });
    await shot(page, 'preview');
    // scroll the grid for a moving sequence
    const grid = page.locator('div').filter({ hasText: 'PATIENT_ID' }).last();
    await page.mouse.move(900, 600);
    for (let i = 0; i < 6; i++) { await page.mouse.wheel(0, 260); await page.waitForTimeout(120); }
    await shot(page, 'preview_scrolled');
    for (let i = 0; i < 6; i++) { await page.mouse.wheel(500, 0); await page.waitForTimeout(120); }
    await shot(page, 'preview_scrolled_x');
    await page.close();
  },
  async tools() {
    const page = await boot(); await load(page); await parse(page);
    await page.locator("button:has-text('数据转换')").first().click(); await page.waitForTimeout(1500);
    await shot(page, 'tool_compute');
    const input = page.locator('input[placeholder*="new_var"]').first();
    await input.click();
    await input.pressSequentially('sbp_change = sbp_12w - sbp_baseline', { delay: 70 });
    await page.waitForTimeout(600);
    await shot(page, 'tool_compute_typed');
    await click(page, '重编码', { wait: 1200 }); await shot(page, 'tool_recode');
    await click(page, '批量操作', { wait: 1200 }); await shot(page, 'tool_batch');
    await click(page, 'AI 文本编码', { wait: 1200 }); await shot(page, 'tool_ai_encode');
    await page.keyboard.press('Escape'); await page.waitForTimeout(800);
    await page.locator("button:has-text('医学标准')").first().click(); await page.waitForTimeout(1800);
    await shot(page, 'tool_medical');
    const sel = page.locator('select').first();
    try { const opts = await sel.locator('option').allTextContents(); console.log('medical options', opts.slice(0, 12)); await sel.selectOption({ index: 1 }); await page.waitForTimeout(1200); await shot(page, 'tool_medical_bmi'); } catch (e) { console.error(e.message); }
    await click(page, '关闭', { wait: 800 });
    await page.locator("button:has-text('智能合并')").first().click(); await page.waitForTimeout(1800);
    await shot(page, 'tool_merge');
    await page.keyboard.press('Escape'); await page.waitForTimeout(600);
    try { await click(page, '关闭', { wait: 600 }); } catch {}
    await page.locator("button:has-text('导出数据')").first().click(); await page.waitForTimeout(1800);
    await shot(page, 'tool_export');
    await page.close();
  },
  async methods() {
    const page = await boot(); await load(page); await parse(page); await toAnalysis(page);
    await shot(page, 'workspace');
    const side = page.getByText('统计方法', { exact: true }).first();
    const box = await side.boundingBox();
    await page.mouse.move(130, 600);
    await seq(page, 'method_scroll', 0, 0);
    const dir = path.join(OUT, 'method_scroll');
    for (let k = 0; k < 40; k++) { await page.mouse.wheel(0, 140); await page.waitForTimeout(90); await page.screenshot({ path: path.join(dir, `${String(k).padStart(4, '0')}.png`), clip: { x: 0, y: 56, width: 256, height: 1024 } }); }
    console.log('box', box);
    await page.close();
  },
  async ttest() {
    const page = await boot(); await load(page); await parse(page); await toAnalysis(page);
    await shot(page, 'tt_empty');
    await assign(page, 'group', '分组变量'); await shot(page, 'tt_assign1');
    await assign(page, 'sbp_12w', '检验变量'); await shot(page, 'tt_assign2');
    await assign(page, 'ldl', '检验变量'); await shot(page, 'tt_assign3');
    for (const tab of ['🧪 假设检验', '⚙️ 模型参数', '📊 表格设置', '🎨 图表设置']) {
      try { await page.locator(`button:has-text('${tab.split(' ')[1]}')`).first().click({ timeout: 8000 }); await page.waitForTimeout(900); await shot(page, 'tt_opt_' + tab.split(' ')[1]); } catch (e) { console.error(tab, e.message.split('\n')[0]); }
    }
    await click(page, '运行分析', { wait: 300 });
    await seq(page, 'tt_run', 26000, 150);
    await shot(page, 'tt_result');
    await page.close();
  },
};

async function analyze(page, label, pairs, name, { big = true, wait = 7000 } = {}) {
  await method(page, label);
  for (const [v, slot] of pairs) await assign(page, v, slot);
  await run(page, wait);
  await shot(page, name);
  if (big) {
    try {
      await page.locator('button[title="放大预览"]').first().click({ timeout: 8000 });
      await page.waitForTimeout(2500);
      await shot(page, name + '_plot');
      await page.keyboard.press('Escape'); await page.waitForTimeout(800);
    } catch (e) { console.error('big plot', name, e.message.split('\n')[0]); }
  }
  // close the result tab so the next method starts clean
  try { await page.locator('button:has-text("返回上一步")').first(); } catch {}
}
Object.assign(scenarios, {
  async gallery() {
    const jobs = [
      ['Kaplan-Meier 生存分析', [['time_months', '时间变量'], ['event', '结局状态变量'], ['group', '分组变量']], 'km'],
      ['Cox 比例风险回归', [['time_months', '时间变量'], ['event', '结局状态变量'], ['group', '预测变量'], ['age', '预测变量'], ['diabetes', '预测变量'], ['biomarker', '预测变量']], 'cox'],
      ['ROC 曲线分析', [['biomarker', '检验变量'], ['crp', '检验变量'], ['event', '状态变量']], 'roc'],
      ['二元 Logistic 回归', [['event', '因变量 (Y)'], ['group', '自变量 (X)'], ['age', '自变量 (X)'], ['biomarker', '自变量 (X)'], ['diabetes', '自变量 (X)']], 'logit'],
      ['限制性立方样条（RCS）', [['event', '结局变量'], ['biomarker', '暴露变量'], ['age', '协变量']], 'rcs'],
      ['亚组交互森林图', [['event', '结局变量'], ['group', '处理变量'], ['sex', '亚组变量'], ['diabetes', '亚组变量'], ['smoking', '亚组变量']], 'subgroup'],
      ['PROCESS 中介效应', [['qol_score', '因变量 (Y)'], ['sbp_baseline', '自变量 (X)'], ['sbp_12w', '中介变量 (M)']], 'process'],
      ['随机效应 Meta 分析', [['effect', '效应量'], ['se', '标准误'], ['study', '研究标签']], 'meta'],
      ['决策曲线分析 (DCA)', [['event', '结局变量'], ['biomarker', '预测变量'], ['age', '预测变量']], 'dca'],
    ];
    const only = process.env.ONLY ? process.env.ONLY.split(',') : null;
    for (const [label, pairs, name] of jobs) {
      if (only && !only.includes(name)) continue;
      const page = await boot(); await load(page, name === 'meta' ? 'demo_meta.csv' : 'demo_trial.csv'); await parse(page); await toAnalysis(page);
      try { await analyze(page, label, pairs, name); } catch (e) { console.error('job', name, e.message.split('\n')[0]); await shot(page, name + '_fail'); }
      await page.context().close();
    }
  },
  async meta() {
    const page = await boot(); await load(page, 'demo_meta.csv'); await parse(page); await toAnalysis(page);
    await method(page, '随机效应 Meta 分析');
    await shot(page, 'meta_setup');
    console.log(await page.evaluate(() => [...document.querySelectorAll('div')].filter(e => e.childElementCount < 8 && /最多/.test(e.innerText || '') && (e.innerText || '').length < 60 && e.offsetParent).map(e => e.innerText.replace(/\s+/g, ' ')).filter((v, i, a) => a.indexOf(v) === i).slice(0, 10)));
    await page.close();
  },
  async exports() {
    const page = await boot(); await load(page); await parse(page); await toAnalysis(page);
    await assign(page, 'group', '分组变量'); await assign(page, 'sbp_12w', '检验变量');
    await run(page, 6000);
    for (const ct of ['小提琴图', '雨云图', '蜂群图', '柱状+散点']) {
      try { await page.locator(`button:has-text('图表设置')`).first().click({ timeout: 3000 }).catch(() => {}); await click(page, ct, { wait: 400 }); await run(page, 5000); await shot(page, 'chart_' + ct); } catch (e) { console.error(ct, e.message.split('\n')[0]); }
    }
    try { await page.locator('button[title^="选择分辨率"]').first().click({ timeout: 8000 }); await page.waitForTimeout(1500); await shot(page, 'dl_dialog'); await page.keyboard.press('Escape'); await page.waitForTimeout(600); } catch (e) { console.error('dl', e.message.split('\n')[0]); }
    try { await page.locator('button[title="导出可复现 R 代码"]').first().click({ timeout: 8000 }); await page.waitForTimeout(3000); await shot(page, 'r_code'); await page.keyboard.press('Escape'); await page.waitForTimeout(600); } catch (e) { console.error('r', e.message.split('\n')[0]); }
    try { await page.locator('button:has-text("导出报告")').first().click({ timeout: 8000 }); await page.waitForTimeout(3000); await shot(page, 'word_export'); await page.keyboard.press('Escape'); } catch (e) { console.error('word', e.message.split('\n')[0]); }
    await page.close();
  },
});

Object.assign(scenarios, {
  async chat() {
    const page = await boot(); await load(page); await parse(page); await toAnalysis(page);
    await page.mouse.click(1855, 1017); await page.waitForTimeout(2000);
    await shot(page, 'chat_open');
    const box = page.locator('textarea').last();
    await box.click(); await box.pressSequentially('我想比较两组患者治疗 12 周后的收缩压，该用什么方法？', { delay: 40 });
    await shot(page, 'chat_typed');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1500); await shot(page, 'chat_stream1');
    await page.waitForTimeout(2500); await shot(page, 'chat_stream2');
    await page.waitForTimeout(8000); await shot(page, 'chat_done');
    await page.close();
  },
  async airstudio() {
    const page = await boot(); await load(page); await parse(page); await toAnalysis(page);
    await click(page, 'AI-R 研究工作台', { exact: false, wait: 3000 });
    await shot(page, 'air_studio');
    await page.close();
  },
  async settings() {
    const page = await boot();
    await page.mouse.click(1749, 156); await page.waitForTimeout(2000);
    await shot(page, 'settings');
    await page.close();
  },
  async predict() {
    const page = await boot(); await load(page); await parse(page); await toAnalysis(page);
    await analyze(page, '临床预测模型', [['event', '结局变量'], ['group', '预测变量'], ['age', '预测变量'], ['biomarker', '预测变量'], ['diabetes', '预测变量'], ['sbp_12w', '预测变量']], 'predict', { wait: 15000 });
    await page.close();
  },
});

Object.assign(scenarios, {
  async exports2() {
    const page = await boot(); await load(page); await parse(page); await toAnalysis(page);
    await assign(page, 'group', '分组变量'); await assign(page, 'sbp_12w', '检验变量'); await assign(page, 'ldl', '检验变量');
    await run(page, 8000);
    try { await page.getByText('R 代码', { exact: true }).first().click({ timeout: 8000 }); await page.waitForTimeout(4000); await shot(page, 'r_code'); } catch (e) { console.error('r', e.message.split('\n')[0]); }
    await page.mouse.click(30, 1060); await page.keyboard.press('Escape'); await page.waitForTimeout(800);
    await shot(page, 'after_r');
    try { await page.getByText('导出报告', { exact: true }).first().click({ timeout: 8000 }); await page.waitForTimeout(4000); await shot(page, 'word_export'); } catch (e) { console.error('word', e.message.split('\n')[0]); }
    await page.close();
  },
  async chat2() {
    const page = await boot(); await load(page); await parse(page); await toAnalysis(page);
    await page.mouse.click(1855, 1017); await page.waitForTimeout(2000);
    const box = page.locator('[placeholder*="输入"], [contenteditable=true]').last();
    console.log('candidates', await page.locator('[placeholder]').evaluateAll(es => es.map(e => e.tagName + ':' + e.getAttribute('placeholder')).slice(-6)));
    await box.click({ timeout: 8000 }); await page.keyboard.type('我想比较两组患者治疗 12 周后的收缩压，该用什么方法？', { delay: 30 });
    await shot(page, 'chat_typed');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1500); await shot(page, 'chat_stream1');
    await page.waitForTimeout(2500); await shot(page, 'chat_stream2');
    await page.waitForTimeout(9000); await shot(page, 'chat_done');
    await page.close();
  },
});

Object.assign(scenarios, {
  async files() {
    const page = await boot(); await load(page); await parse(page); await toAnalysis(page);
    await assign(page, 'group', '分组变量'); await assign(page, 'sbp_12w', '检验变量'); await assign(page, 'ldl', '检验变量');
    await run(page, 9000);
    const grab = async (label, file) => {
      const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 90000 }), page.getByText(label, { exact: true }).first().click()]);
      await dl.saveAs(path.join(OUT, file)); console.log('saved', file, dl.suggestedFilename());
    };
    try { await grab('R 代码', 'export_ttest.R'); } catch (e) { console.error('r', e.message.split('\n')[0]); }
    await page.waitForTimeout(1500);
    try { await grab('导出报告', 'export_ttest.docx'); } catch (e) { console.error('docx', e.message.split('\n')[0]); await shot(page, 'docx_fail'); }
    await page.waitForTimeout(1500); await shot(page, 'after_exports');
    await page.close();
  },
  async chat3() {
    const page = await boot(); await load(page); await parse(page); await toAnalysis(page);
    await page.mouse.click(1855, 1017); await page.waitForTimeout(2000);
    const box = page.locator('[placeholder*="输入你的问题"]').last();
    await box.click({ timeout: 8000 }); await page.keyboard.type('我想比较两组患者治疗 12 周后的收缩压，该用什么方法？', { delay: 30 });
    await shot(page, 'chat_typed');
    await page.keyboard.press('Enter'); await page.waitForTimeout(1200);
    await shot(page, 'chat_consent');
    console.log(await page.evaluate(() => [...document.querySelectorAll('button')].filter(b => /授权/.test(b.innerText)).map(b => b.innerText + '|' + b.disabled + '|' + !!b.offsetParent)));
    await page.locator('button:has-text("确认授权")').last().click({ timeout: 8000, force: true });
    await page.waitForTimeout(1200); await shot(page, 'chat_stream1');
    await page.waitForTimeout(1500); await shot(page, 'chat_stream2');
    await page.waitForTimeout(9000); await shot(page, 'chat_done');
    await page.close();
  },
});

Object.assign(scenarios, {
  async aistream() {
    const page = await boot(); await load(page); await parse(page); await toAnalysis(page);
    await assign(page, 'group', '分组变量'); await assign(page, 'sbp_12w', '检验变量'); await assign(page, 'ldl', '检验变量');
    await click(page, '运行分析', { wait: 300 });
    await seq(page, 'ai_stream', 42000, 40, { x: 1436, y: 316, width: 478, height: 760 });
    await shot(page, 'ai_final');
    await page.close();
  },
  async sidebar() {
    const page = await boot(); await load(page); await parse(page); await toAnalysis(page);
    const info = await page.evaluate(() => {
      const label = [...document.querySelectorAll('*')].find(e => e.childElementCount === 0 && e.textContent.trim() === '描述性统计');
      let el = label; while (el && !(el.scrollHeight > el.clientHeight + 20 && getComputedStyle(el).overflowY !== 'visible')) el = el.parentElement;
      if (!el) return null;
      el.setAttribute('data-film', 'side');
      const r = el.getBoundingClientRect();
      return { sh: el.scrollHeight, ch: el.clientHeight, x: r.x, y: r.y, w: r.width };
    });
    console.log(info);
    const el = page.locator('[data-film=side]');
    await el.evaluate(e => { e.style.height = e.scrollHeight + 'px'; e.style.maxHeight = 'none'; e.style.overflow = 'visible'; });
    await page.setViewportSize({ width: 1920, height: Math.min(16000, info.sh + 200) });
    await page.waitForTimeout(800);
    await el.screenshot({ path: path.join(OUT, 'sidebar_full.png') });
    await page.close();
  },
});

Object.assign(scenarios, {
  async aitall() {
    const page = await boot(); await load(page); await parse(page); await toAnalysis(page);
    await assign(page, 'group', '分组变量'); await assign(page, 'sbp_12w', '检验变量'); await assign(page, 'ldl', '检验变量');
    await run(page, 40000);
    const info = await page.evaluate(() => {
      const label = [...document.querySelectorAll('h1,h2,h3,h4,strong,p,div,span')].find(e => e.childElementCount === 0 && e.textContent.trim() === '核心结论');
      let el = label; while (el && !(el.scrollHeight > el.clientHeight + 20 && /auto|scroll/.test(getComputedStyle(el).overflowY))) el = el.parentElement;
      if (!el) return null;
      el.setAttribute('data-film', 'ai'); const r = el.getBoundingClientRect();
      return { sh: el.scrollHeight, ch: el.clientHeight, x: r.x, y: r.y, w: r.width };
    });
    console.log(info);
    const el = page.locator('[data-film=ai]');
    await el.evaluate(e => { e.scrollTop = 0; e.style.height = e.scrollHeight + 'px'; e.style.maxHeight = 'none'; e.style.overflow = 'visible'; });
    await page.setViewportSize({ width: 1920, height: Math.min(8000, info.sh + 600) });
    await page.waitForTimeout(800);
    await el.screenshot({ path: path.join(OUT, 'ai_tall.png') });
    await page.close();
  },
});

for (const name of process.argv.slice(2)) {
  console.log('== scenario', name);
  try { await scenarios[name](); } catch (e) { console.error('scenario failed', name, e.message.split('\n').slice(0, 3).join(' | ')); }
}
await browser.close();
