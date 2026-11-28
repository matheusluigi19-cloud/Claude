// node exportar-triconjunto.js <cor> <saida.png> [fundo.png]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [cor, saida, fundo] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(__dirname, 'triconjunto.html') + '?cor=' + cor + (fundo ? '&fundo=' + encodeURIComponent('file://' + fundo) : ''));
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
  await p.waitForTimeout(300);
  await p.screenshot({ path: saida, omitBackground: !fundo });
  await b.close();
})();
