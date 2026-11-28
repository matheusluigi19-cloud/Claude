// Gera as camadas transparentes (logo e frase) em PNG 1080x1920.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  for (const c of ['logo', 'frase']) {
    await p.goto('file://' + path.join(__dirname, 'sobreposicao.html') + '?camada=' + c);
    await p.evaluate(() => document.fonts.ready);
    await p.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
    await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(__dirname, 'assets', 'camada-' + c + '.png'), omitBackground: true });
  }
  await b.close();
})();
