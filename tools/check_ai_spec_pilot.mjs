#!/usr/bin/env node
// Operator-supplied browser; offline archive checks, not writing-quality scores.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

assert.equal(process.argv.length, 3, 'Usage: node tools/check_ai_spec_pilot.mjs OUTPUT_DIR');
const output = path.resolve(process.argv[2]);
const root = fileURLToPath(new URL('../evals/ai-spec-pilot/', import.meta.url));
const packet = JSON.parse(await fs.readFile(path.join(root, 'blind/reader.json'), 'utf8'));
const mapping = JSON.parse(await fs.readFile(path.join(root, 'mapping.json'), 'utf8'));
const freeze = JSON.parse(await fs.readFile(path.join(root, 'freeze.json'), 'utf8'));
const initials = Object.fromEntries(await Promise.all(freeze.writers.map(async writer => [writer.id,
  JSON.parse(await fs.readFile(path.join(root, 'raw', `${writer.id}_initial.json`), 'utf8'))])));
await fs.mkdir(output, { recursive: true });
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright-core');
const browser = await chromium.launch({ headless: true,
  ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}) });
const errors = [];
const remoteRequests = [];
const views = [];
try {
  for (const viewport of [{ width: 1600, height: 1100 }, { width: 900, height: 1000 }, { width: 390, height: 844 }]) {
    const page = await browser.newPage({ viewport });
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    await page.route(/https?:\/\//, route => {
      remoteRequests.push(route.request().url());
      return route.abort();
    });
    await page.goto(pathToFileURL(path.join(root, 'comparison.html')).href);
    assert.equal(await page.locator('article').count(), 12);
    for (const pair of packet.pairs) {
      for (const side of ['A', 'B']) {
        const selector = `#${pair.id} .prose[data-side="${mapping[pair.id][side]}"]`;
        assert.equal(await page.locator(selector).textContent(), pair[side]);
        const writer = freeze.writers.find(w => w.condition === mapping[pair.id][side] && w.replicate === pair.sample);
        const initial = initials[writer.id].cases.find(c => c.id === pair.paper)[pair.unit];
        const column = mapping[pair.id][side] === 'baseline' ? 0 : 1;
        assert.equal(await page.locator(`#${pair.id} .initial`).nth(column).textContent(), initial);
      }
    }
    const layout = await page.evaluate(() => {
      let overlap = 0;
      for (const columns of document.querySelectorAll('.columns')) {
        const [a, b] = [...columns.children].map(el => el.getBoundingClientRect());
        if (Math.min(a.right, b.right) - Math.max(a.left, b.left) > 1 &&
            Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 1) overlap++;
      }
      const first = [...document.querySelector('.columns').children].map(el => el.getBoundingClientRect());
      return { overflow: document.documentElement.scrollWidth > innerWidth,
        overlap, horizontal: Math.abs(first[0].top - first[1].top) < 1 };
    });
    assert.equal(layout.overflow, false);
    assert.equal(layout.overlap, 0);
    assert.equal(layout.horizontal, viewport.width > 760);
    await page.selectOption('#paper', 'R02');
    await page.selectOption('#unit', 'methods');
    assert.equal(await page.locator('article:visible').count(), 2);
    await page.selectOption('#sample', '2');
    assert.equal(await page.locator('article:visible').count(), 1);
    for (const selector of ['#paper', '#unit', '#sample']) await page.selectOption(selector, 'all');
    assert.equal(await page.locator('article:visible').count(), 12);
    await page.locator('details').evaluateAll(items => items.forEach(item => { item.open = true; }));
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    assert.equal(await page.locator('details[open]').count(), 60);
    await page.locator('details').evaluateAll(items => items.forEach(item => { item.open = false; }));
    const links = await page.locator('a').evaluateAll(items => items.map(a => a.href));
    for (const url of links) assert((await fs.stat(fileURLToPath(url))).isFile());
    const screenshot = path.join(output, `comparison-${viewport.width}.png`);
    await fs.writeFile(screenshot, await page.screenshot(), { flag: 'wx' });
    views.push({ ...viewport, ...layout, exact_final_passages: 24, exact_initial_passages: 24,
      expanded_details: 60, links: links.length, filter_journey: 'pass' });
    await page.close();
  }
  assert.deepEqual(errors, []);
  assert.deepEqual(remoteRequests, []);
  const result = { browser: browser.version(), views, errors, remoteRequests,
    scope: 'Offline text integrity, layout and filtering, not evidence of writing effectiveness.' };
  await fs.writeFile(path.join(output, 'receipt.json'), JSON.stringify(result, null, 2) + '\n', { flag: 'wx' });
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
} finally {
  await browser.close();
}
