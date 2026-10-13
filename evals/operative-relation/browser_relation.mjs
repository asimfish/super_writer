import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const mapping = JSON.parse(fs.readFileSync(path.join(root, 'mapping.json'), 'utf8'));
const raw = (condition, m) => JSON.parse(fs.readFileSync(path.join(root, 'raw', `${condition}_${m.paper}_${m.sample}.json`), 'utf8'))[m.unit];
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
    const rows = await page.locator('article').evaluateAll(articles => articles.map(a => ({
      id: a.id, prose: [...a.querySelectorAll('.prose')].map(p => p.textContent),
      initial: a.querySelector('.initial-prose').textContent
    })));
    for (const row of rows) {
      const m = mapping.find(m => m.id === row.id);
      assert.deepEqual(row.prose, [raw('baseline', m), raw('candidate', m)]);
      assert.equal(row.initial, raw('initial', m));
    }
    for (const pid of ['N1', 'N2']) {
      await page.selectOption('#paper', pid);
      assert.equal(await page.locator('article:visible').count(), 6);
      for (const unit of ['abstract', 'methods', 'results']) {
        await page.selectOption('#unit', unit);
        assert.equal(await page.locator('article:visible').count(), 2);
      }
      await page.selectOption('#unit', 'all');
    }
    await page.selectOption('#paper', 'N1');
    await page.selectOption('#unit', 'methods');
    const first = page.locator('article:visible').first();
    await first.locator('.version details').first().locator('summary').click();
    assert.equal(await first.locator('.version details').first().getAttribute('open'), '');
    const geometry = await first.evaluate(a => ({
      columns: [...a.querySelectorAll('.version')].map(v => {
        const r = v.getBoundingClientRect();
        return { left: r.left, right: r.right, top: r.top, bottom: r.bottom, overflow: v.scrollWidth > v.clientWidth };
      }), pageWidth: document.documentElement.scrollWidth, viewport: document.documentElement.clientWidth
    }));
    assert(geometry.pageWidth <= geometry.viewport);
    assert(geometry.columns.every(c => !c.overflow));
    const [a, b] = geometry.columns;
    if (viewport.width > 760) assert(a.right <= b.left);
    else assert(a.bottom <= b.top);
    await first.evaluate(a => a.scrollIntoView({ block: 'start' }));
    await page.screenshot({ path: path.join(root, 'checks', `relation-${viewport.width}.png`) });
    assert.deepEqual(errors, []);
    results.push({ viewport, pairs: 12, raw_prose_strings_verified: 36,
      filters: true, details: true, no_overflow_or_overlap: true, page_errors: 0 });
    await page.close();
  }
} finally {
  await browser.close();
}
const target = path.join(root, 'browser_verification.json');
assert(!fs.existsSync(target));
fs.writeFileSync(target, JSON.stringify(results, null, 2) + '\n');
console.log(JSON.stringify(results));
