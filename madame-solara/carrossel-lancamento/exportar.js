// Exporta um slide: node exportar.js "<consulta>" saida.png
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [consulta, saida] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'slide.html') + '?' + consulta);
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
  await p.waitForTimeout(500);
  await p.screenshot({ path: saida, type: 'png' });
  await b.close();
})();
