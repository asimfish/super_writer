import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const cases = JSON.parse(fs.readFileSync(path.join(root, 'cases.json'), 'utf8')).cases;
const browser = await chromium.launch({ headless: true,
  ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}) });
const results = [];
fs.mkdirSync(path.join(root, 'checks'), { recursive: true });
try {
  for (const viewport of [{ width: 1440, height: 1000 }, { width: 390, height: 844 }]) {
    const page = await browser.newPage({ viewport });
    const errors = [];
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto(pathToFileURL(path.join(root, 'comparison.html')).href);
    assert.equal(await page.locator('article').count(), 12);
    const texts = await page.locator('article').evaluateAll(rows => rows.map(a => ({
      id: a.id, prose: [...a.querySelectorAll('.prose')].map(p => p.textContent),
      overflow: [...a.querySelectorAll('.prose')].some(p => p.scrollWidth > p.clientWidth)
    })));
    for (const row of texts) {
      const original = cases.find(c => c.id === row.id);
      assert.deepEqual(row.prose, [original.variants.v1, original.variants.v2]);
      assert(!row.overflow);
    }
    for (const category of ['relation', 'metric', 'condition', 'neutral']) {
      await page.selectOption('#category', category);
      assert.equal(await page.locator('article:visible').count(), 3);
    }
    await page.selectOption('#category', 'relation');
    const first = page.locator('article:visible').first();
    await first.locator('details').first().locator('summary').click();
    assert.equal(await first.locator('details').first().getAttribute('open'), '');
    const geometry = await first.evaluate(a => ({
      columns: [...a.querySelectorAll('.version')].map(v => {
        const r = v.getBoundingClientRect();
        return { left: r.left, right: r.right, top: r.top, bottom: r.bottom,
          overflow: v.scrollWidth > v.clientWidth };
      }), pageWidth: document.documentElement.scrollWidth, viewport: document.documentElement.clientWidth
    }));
    assert(geometry.pageWidth <= geometry.viewport);
    assert(geometry.columns.every(c => !c.overflow));
    const [a, b] = geometry.columns;
    if (viewport.width > 760) assert(a.right <= b.left);
    else assert(a.bottom <= b.top);
    await first.evaluate(a => a.scrollIntoView({ block: 'start' }));
    await page.screenshot({ path: path.join(root, 'checks', `controls-${viewport.width}.png`) });
    assert.deepEqual(errors, []);
    results.push({ viewport, cases: 12, raw_prose_strings_verified: 24,
      category_filters: true, details: true, no_overflow_or_overlap: true, page_errors: 0 });
    await page.close();
  }
} finally {
  await browser.close();
}
const target = path.join(root, 'browser_verification.json');
assert(!fs.existsSync(target));
fs.writeFileSync(target, JSON.stringify(results, null, 2) + '\n');
console.log(JSON.stringify(results));
