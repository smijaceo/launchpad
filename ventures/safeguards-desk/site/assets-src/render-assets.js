// Renders og.png (1200x630) and apple-touch-icon.png (180x180) into ../static/.
// Run: node ventures/safeguards-desk/site/assets-src/render-assets.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const here = __dirname, out = path.join(here, '..', 'static');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + path.join(here, 'og.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(out, 'og.png') });
  const q = await b.newPage({ viewport: { width: 180, height: 180 } });
  await q.goto('file://' + path.join(here, '..', '..', 'brand', 'logo', 'avatar.svg'));
  await q.screenshot({ path: path.join(out, 'apple-touch-icon.png'), omitBackground: true });
  await b.close();
})();
