import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const htmlFile = process.argv[2] || 'comparison.html';
const receiptFile = process.argv[3] || 'browser_verification.json';
const screenshotPrefix = path.basename(htmlFile, '.html');
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const browser = await chromium.launch({ headless: true,
  ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}) });
const results = [];
const originals = new Map();
for (const name of fs.readdirSync(path.join(root, 'raw'))) {
  const match = /^(initial|baseline|candidate)_(D\d+)_(\d)\.json$/.exec(name);
  if (!match) continue;
  for (const c of JSON.parse(fs.readFileSync(path.join(root, 'raw', name), 'utf8')).cases)
    originals.set(`${c.id}/${match[3]}/${match[1]}`, c);
}
fs.mkdirSync(path.join(root, 'checks'), { recursive: true });
try {
  for (const viewport of [{ width: 1440, height: 1000 }, { width: 390, height: 844 }]) {
    const page = await browser.newPage({ viewport });
    const errors = [];
    page.on('pageerror', error => errors.push(String(error)));
    await page.goto(pathToFileURL(path.join(root, htmlFile)).href);
    assert.equal(await page.locator('article').count(), 108);
    assert.equal(await page.locator('article:visible').count(), 108);
    if (htmlFile === 'comparison-complete.html') {
      assert.equal(await page.locator('.secondary-audit').count(), 216);
      assert.equal(await page.locator('article[id="P06_s2_methods"]').count(), 1);
    }
    const displayed = await page.locator('article').evaluateAll(articles => articles.map(a => ({
      paper: a.dataset.paper, sample: a.dataset.sample, unit: a.dataset.unit,
      prose: [...a.querySelectorAll('.prose')].map(p => p.textContent),
      overflow: [...a.querySelectorAll('.prose')].some(p => p.scrollWidth > p.clientWidth)
    })));
    for (const a of displayed) {
      assert.deepEqual(a.prose, ['baseline', 'candidate', 'initial'].map(c =>
        originals.get(`${a.paper}/${a.sample}/${c}`)[a.unit]));
      assert(!a.overflow, 'Prose overflows column');
    }
    await page.selectOption('#paper', 'P01');
    assert.equal(await page.locator('article:visible').count(), 9);
    await page.selectOption('#unit', 'results');
    assert.equal(await page.locator('article:visible').count(), 3);
    await page.selectOption('#sample', '1');
    assert.equal(await page.locator('article:visible').count(), 1);
    const article = page.locator('article:visible');
    assert.equal(await article.locator('.prose').count(), 3);
    await article.locator('details').first().locator('summary').click();
    assert.equal(await article.locator('details').first().getAttribute('open'), '');
    const geometry = await article.evaluate(element => {
      const sections = [...element.querySelectorAll('.version')].map(e => {
        const r = e.getBoundingClientRect();
        return { left: r.left, right: r.right, top: r.top, bottom: r.bottom,
                 scrollWidth: e.scrollWidth, clientWidth: e.clientWidth };
      });
      return { sections, pageWidth: document.documentElement.scrollWidth,
               viewport: document.documentElement.clientWidth };
    });
    assert(geometry.pageWidth <= geometry.viewport, 'Page overflows viewport');
    assert(geometry.sections.every(s => s.scrollWidth <= s.clientWidth), 'Text column overflow');
    const [a, b] = geometry.sections;
    if (viewport.width > 760) assert(a.right <= b.left, 'Desktop columns overlap');
    else assert(a.bottom <= b.top, 'Mobile columns overlap');
    await article.evaluate(e => e.scrollIntoView({ block: 'start' }));
    await page.screenshot({ path: path.join(root, 'checks', `${screenshotPrefix}-${viewport.width}.png`) });
    await page.selectOption('#paper', 'all');
    await page.selectOption('#unit', 'all');
    await page.selectOption('#sample', 'all');
    await page.check('#concern');
    const expected = await page.locator('article[data-concern="true"]').count();
    assert.equal(await page.locator('article:visible').count(), expected);
    assert.equal(await page.locator('#count').textContent(), `${expected} pairs`);
    assert.deepEqual(errors, []);
    results.push({ html: htmlFile, viewport, checked: ['108 pairs, all 324 displayed prose strings match raw', 'paper/unit/sample filters',
      'details', 'source-concern filter', 'no text or viewport overflow', 'no overlaps', 'no page errors'] });
    await page.close();
  }
} finally {
  await browser.close();
}
const target = path.join(root, receiptFile);
assert(!fs.existsSync(target), 'Refusing to overwrite browser evidence');
fs.writeFileSync(target, JSON.stringify(results, null, 2) + '\n');
console.log(JSON.stringify(results));
