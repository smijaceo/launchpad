// Site QA: screenshots every page at phone and desktop widths, checks basics, writes a JSON report.
// Usage: node qa/site-qa.js <base_url> <out_dir> [paths...]
const { chromium, devices } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [base, out, ...paths] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const report = [];
  for (const [label, opts] of [['phone', devices['iPhone 13']], ['desktop', { viewport: { width: 1366, height: 900 } }]]) {
    for (const color of ['light', 'dark']) {
      const ctx = await b.newContext({ ...opts, colorScheme: color });
      const p = await ctx.newPage();
      for (const u of paths) {
        const errors = [];
        p.on('pageerror', e => errors.push(String(e)));
        const res = await p.goto(base + u, { waitUntil: 'networkidle' });
        const r = await p.evaluate(() => ({
          h1: document.querySelectorAll('h1').length,
          overflowX: document.documentElement.scrollWidth > window.innerWidth + 1,
          imgsNoDims: [...document.images].filter(i => !i.getAttribute('width') || !i.getAttribute('height')).length,
          skip: !!document.querySelector('a.skip-link[href="#main"]'),
          lang: document.documentElement.lang,
        }));
        const name = `${label}-${color}-${u === '/' ? 'home' : u.replace(/\//g, '')}.png`;
        if (color === 'light' || u === '/') await p.screenshot({ path: path.join(out, name), fullPage: true });
        report.push({ device: label, color, path: u, status: res.status(), errors, ...r });
      }
      await ctx.close();
    }
  }
  await b.close();
  fs.writeFileSync(path.join(out, 'qa.json'), JSON.stringify(report, null, 1));
  const bad = report.filter(r => r.status !== 200 || r.h1 !== 1 || r.overflowX || r.imgsNoDims || !r.skip || r.errors.length);
  console.log(bad.length ? 'FAIL\n' + JSON.stringify(bad, null, 1) : `ok: ${report.length} page views`);
  process.exit(bad.length ? 1 : 0);
})();
