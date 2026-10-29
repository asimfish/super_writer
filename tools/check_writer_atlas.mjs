#!/usr/bin/env node
// Source-only browser checks; rendering dependencies are supplied by the operator.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const args = new Map();
for (let i = 2; i < process.argv.length; i += 2) {
  const flag = process.argv[i];
  assert(['--html', '--output-dir', '--overview-png'].includes(flag), `Unknown flag: ${flag}`);
  assert(process.argv[i + 1] && !args.has(flag), `Missing or duplicate argument: ${flag}`);
  args.set(flag, path.resolve(process.argv[i + 1]));
}
for (const flag of ['--html', '--output-dir', '--overview-png']) {
  assert(args.has(flag), `Required: ${flag}`);
}

async function checkDestination(destination) {
  for (let item = destination; ; item = path.dirname(item)) {
    const stat = await fs.lstat(item).catch(error => {
      if (error.code === 'ENOENT') return null;
      throw error;
    });
    assert(!stat?.isSymbolicLink(), `Output must not traverse a symlink: ${item}`);
    if (item === path.dirname(item)) break;
  }
}

await checkDestination(args.get('--output-dir'));
await checkDestination(args.get('--overview-png'));
await fs.mkdir(args.get('--output-dir'), { recursive: true });
await fs.mkdir(path.dirname(args.get('--overview-png')), { recursive: true });
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright-core');
const browser = await chromium.launch({
  headless: true,
  ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}),
});
const errors = [];
const remoteRequests = [];
const views = [];
const spec = JSON.parse(await fs.readFile(new URL('../references/ai-writing-spec.json', import.meta.url), 'utf8'));
const recordCount = spec.entries.length;
try {
  for (const viewport of [{ width: 1600, height: 1100 }, { width: 900, height: 1000 }, { width: 390, height: 844 }]) {
    const page = await browser.newPage({ viewport });
    page.on('pageerror', error => errors.push(error.message));
    page.on('console', message => {
      if (message.type() === 'error') errors.push(message.text());
    });
    await page.route(/https?:\/\//, route => {
      remoteRequests.push(route.request().url());
      return route.abort();
    });
    await page.goto(pathToFileURL(args.get('--html')).href);
    await page.locator('#count').filter({ hasText: `${recordCount} / ${recordCount} entries` }).waitFor();
    await page.locator('#kind').selectOption('sentence_pattern');
    const patterns = spec.entries.filter(entry => entry.kind === 'sentence_pattern');
    assert.equal(await page.locator('.record:not([hidden])').count(), patterns.length);
    const pattern = page.locator(`[data-id="${patterns[0].id}"]`);
    await pattern.locator('summary').click();
    for (const value of Object.values(patterns[0].discourse)) {
      assert((await pattern.innerText()).includes(value), 'Pattern discourse boundary omitted');
    }
    await pattern.locator('summary').click();
    await page.locator('#kind').selectOption('');
    const actualRecords = await page.locator('.record').evaluateAll(records => records.map(record => ({
      id: record.id, topics: JSON.parse(record.dataset.topics), levels: JSON.parse(record.dataset.levels),
      text: record.textContent,
    })));
    assert.deepEqual(actualRecords.map(r => r.id), spec.entries.map(e => e.id));
    for (const [i, entry] of spec.entries.entries()) {
      const actual = actualRecords[i];
      assert.deepEqual(actual.topics, entry.topics);
      assert.deepEqual(actual.levels, entry.levels);
      for (const field of ['meaning', 'guidance', 'avoid', 'example_context']) assert(actual.text.includes(entry[field]));
      for (const field of ['conditions', 'exceptions', 'evidence_required', 'examples']) {
        for (const text of entry[field]) assert(actual.text.includes(text));
      }
      for (const example of entry.counter_examples) {
        assert(actual.text.includes(example.text)); assert(actual.text.includes(example.why));
      }
      for (const note of entry.source_notes) {
        assert(actual.text.includes(note.location)); assert(actual.text.includes(note.observation));
      }
    }
    for (const [selector, field] of [['#topic', 'topics'], ['#level', 'levels']]) {
      assert.deepEqual(await page.locator(`${selector} option`).evaluateAll(options =>
        options.map(o => o.value).filter(Boolean)), spec.taxonomy[field]);
    }
    const layout = await page.evaluate(() => {
      const svg = document.querySelector('.flow-wrap svg');
      const nodes = [...svg.querySelectorAll('[data-node]')];
      const labelFailures = [];
      for (const node of nodes) {
        const rect = node.querySelector('rect').getBBox();
        for (const text of node.querySelectorAll('text')) {
          const box = text.getBBox();
          if (box.x < rect.x + 3 || box.x + box.width > rect.x + rect.width - 3 ||
              box.y < rect.y || box.y + box.height > rect.y + rect.height) {
            labelFailures.push({ text: text.textContent, label: { x: box.x, y: box.y, width: box.width, height: box.height },
              node: { x: rect.x, y: rect.y, width: rect.width, height: rect.height }, font: getComputedStyle(text).font });
          }
        }
      }
      const panels = [...document.querySelectorAll('.panel')].map(p => p.getBoundingClientRect());
      let overlappingPanels = 0;
      for (let i = 0; i < panels.length; i++) {
        for (let j = i + 1; j < panels.length; j++) {
          const a = panels[i]; const b = panels[j];
          if (Math.min(a.right, b.right) - Math.max(a.left, b.left) > 1 &&
              Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 1) overlappingPanels++;
        }
      }
      return {
        nodeCount: nodes.length,
        edgeCount: svg.querySelectorAll('[data-edge]').length,
        recordCount: document.querySelectorAll('.record').length,
        overflow: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - innerWidth,
        labelFailures, overlappingPanels,
        controls: [...document.querySelectorAll('.search-row input, .search-row select')].map(control => {
          const box = control.getBoundingClientRect();
          return { id: control.id, left: box.left, right: box.right, top: box.top, bottom: box.bottom };
        }),
      };
    });
    assert.equal(layout.nodeCount, 8);
    assert.equal(layout.edgeCount, 9);
    assert.equal(layout.recordCount, recordCount);
    assert(layout.overflow <= 1, `Page overflow: ${layout.overflow}px`);
    assert.equal(layout.overlappingPanels, 0);
    assert.deepEqual(layout.labelFailures, [], `SVG labels escape nodes: ${layout.labelFailures}`);
    for (const [i, a] of layout.controls.entries()) {
      assert(a.left >= 0 && a.right <= viewport.width + 1, `Control outside viewport: ${a.id}`);
      for (const b of layout.controls.slice(i + 1)) {
        assert(!(Math.min(a.right, b.right) - Math.max(a.left, b.left) > 1 &&
          Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 1), `Overlapping controls: ${a.id}, ${b.id}`);
      }
    }
    let mobileDiagramScroll = 'not applicable';
    if (viewport.width < 1000) {
      const scroll = await page.locator('.flow-wrap').evaluate(wrap => {
        wrap.scrollLeft = wrap.scrollWidth;
        const node = wrap.querySelector('[data-node="guards"]').getBoundingClientRect();
        const bounds = wrap.getBoundingClientRect();
        const result = { needed: wrap.scrollWidth > wrap.clientWidth + 1, moved: wrap.scrollLeft > 0,
          visible: node.left >= bounds.left && node.right <= bounds.right + 1 };
        wrap.scrollLeft = 0;
        return result;
      });
      assert((!scroll.needed || scroll.moved) && scroll.visible, 'Diagram cannot reach the delivery node');
      mobileDiagramScroll = 'pass';
    }

    const links = await page.locator('a[href]').evaluateAll(elements =>
      elements.map(a => new URL(a.getAttribute('href'), document.baseURI).href));
    let localLinks = 0;
    for (const href of links) {
      const url = new URL(href);
      if (url.protocol !== 'file:') continue;
      await fs.access(fileURLToPath(url));
      localLinks++;
    }

    await page.locator('#search').fill('\u96f6\u6837\u672c');
    await page.locator('#kind').selectOption('technical_term');
    assert.equal(await page.locator('.record:not([hidden])').count(), 1);
    const zeroShot = page.locator('[data-id="ai.term.zero-shot"]');
    await zeroShot.locator('summary').click();
    assert(await zeroShot.getAttribute('open') !== null);
    assert((await zeroShot.innerText()).includes('Exceptions'));
    assert((await zeroShot.innerText()).includes('Evidence needed'));
    await page.locator('#search').fill('');
    await page.locator('#topic').selectOption('embodied_control');
    await page.locator('#level').selectOption('word');
    const expected = spec.entries.filter(e => e.kind === 'technical_term' && e.topics.includes('embodied_control') && e.levels.includes('word'));
    assert.deepEqual(await page.locator('.record:not([hidden])').evaluateAll(records => records.map(r => r.id)), expected.map(e => e.id));
    await page.locator('#topic').selectOption('grounding_faithfulness');
    await page.locator('#search').fill('\u89c6\u89c9\u5b9a\u4f4d');
    assert.deepEqual(await page.locator('.record:not([hidden])').evaluateAll(records => records.map(r => r.id)), ['ai.term.visual-grounding']);
    const grounding = page.locator('[data-id="ai.term.visual-grounding"]');
    await grounding.locator('summary').click();
    assert((await grounding.innerText()).includes('full PDF body was not reviewed'));
    await grounding.evaluate(record => { record.open = false; });
    await page.locator('#search').fill('');
    if (viewport.width === 1600) {
      for (const topic of spec.taxonomy.topics) {
        for (const level of spec.taxonomy.levels) {
          await page.locator('#topic').selectOption(topic);
          await page.locator('#level').selectOption(level);
          const ids = spec.entries.filter(e => e.kind === 'technical_term' && e.topics.includes(topic) && e.levels.includes(level)).map(e => e.id);
          assert.deepEqual(await page.locator('.record:not([hidden])').evaluateAll(records => records.map(r => r.id)), ids);
        }
      }
    }
    await page.locator('#search').fill('no-match-9b6e2');
    assert.equal(await page.locator('.record:not([hidden])').count(), 0);
    assert(await page.locator('#empty').isVisible());
    await page.locator('#search').fill('');
    await page.locator('#kind').selectOption('');
    await page.locator('#topic').selectOption('');
    await page.locator('#level').selectOption('');
    assert.equal(await page.locator('.record:not([hidden])').count(), recordCount);
    await zeroShot.evaluate(record => { record.open = false; });
    await page.evaluate(() => { location.hash = 'ai.term.action-chunking'; });
    await page.waitForFunction(() => document.getElementById('ai.term.action-chunking').open);
    assert((await page.locator('[data-id="ai.term.action-chunking"]').innerText()).includes('Research anchor'));
    await page.evaluate(() => {
      document.getElementById('ai.term.action-chunking').open = false;
      history.replaceState(null, '', location.pathname);
    });
    await page.locator('#search').fill('no-match-before-fragment');
    await page.locator('#kind').selectOption('technical_term');
    await page.evaluate(() => { location.hash = 'ai.usage.faithful'; });
    await page.waitForFunction(() => document.getElementById('ai.usage.faithful').open);
    assert(await page.locator('[data-id="ai.usage.faithful"]').isVisible());
    assert.equal(await page.locator('#search').inputValue(), '');
    assert.equal(await page.locator('#kind').inputValue(), '');
    await page.evaluate(() => {
      document.getElementById('ai.usage.faithful').open = false;
      history.replaceState(null, '', location.pathname);
    });

    const pixels = await page.evaluate(async () => {
      const source = new XMLSerializer().serializeToString(document.querySelector('.flow-wrap svg'));
      const url = URL.createObjectURL(new Blob([source], { type: 'image/svg+xml' }));
      try {
        const image = new Image(); image.src = url;
        await image.decode();
        const canvas = document.createElement('canvas'); canvas.width = 950; canvas.height = 335;
        const ctx = canvas.getContext('2d'); ctx.fillStyle = 'white'; ctx.fillRect(0, 0, 950, 335);
        ctx.drawImage(image, 0, 0, 950, 335);
        const data = ctx.getImageData(0, 0, 950, 335).data;
        let nonwhite = 0;
        for (let i = 0; i < data.length; i += 4) {
          if (Math.min(data[i], data[i + 1], data[i + 2]) < 230) nonwhite++;
        }
        return nonwhite;
      } finally { URL.revokeObjectURL(url); }
    });
    assert(pixels > 4000, `Blank or nearly blank flow: ${pixels} pixels`);
    await page.evaluate(() => scrollTo(0, 0));
    if (viewport.width > 1000) {
      await page.locator('#atlas').screenshot({ path: args.get('--overview-png') });
    } else {
      const prefix = viewport.width === 390 ? 'writer-atlas-mobile' : 'writer-atlas-tablet';
      const mobilePath = path.join(args.get('--output-dir'), `${prefix}.png`);
      await checkDestination(mobilePath);
      await page.screenshot({ path: mobilePath, fullPage: true });
      const viewportPath = path.join(args.get('--output-dir'), `${prefix}-viewport.png`);
      await checkDestination(viewportPath);
      await page.screenshot({ path: viewportPath });
    }
    views.push({ viewport, ...layout, localLinks, nonwhiteFlowPixels: pixels,
      chineseFilter: 'pass', facetIntersection: 'pass', deepLink: 'pass',
      groundingAliasAndScope: 'pass', filteredFaithfulnessDeepLink: 'pass',
      emptyFilterAndRestore: 'pass', completeRecord: 'pass', mobileDiagramScroll });
    await page.close();
  }
  assert.deepEqual(remoteRequests, [], 'Atlas attempted remote requests');
  assert.deepEqual(errors, [], 'Browser errors');
  const report = { browser: browser.version(), views, remoteRequests, errors,
    scope: 'Engineering and visual checks only; not a writing-quality or semantic-truth evaluation.' };
  const reportPath = path.join(args.get('--output-dir'), 'writer-atlas-browser.json');
  await checkDestination(reportPath);
  await fs.writeFile(reportPath, JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report));
} finally {
  await browser.close();
}
