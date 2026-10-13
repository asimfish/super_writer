import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';
const root = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const read = name => JSON.parse(fs.readFileSync(path.join(root,name),'utf8'));
const mapping = read('mapping.json');
const raw = (condition,m) => read(`raw/${condition}_${m.group}_${m.sample}.json`).cases.find(r=>r.id===m.paper).abstract;
const browser = await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{})});
const results = [];
fs.mkdirSync(path.join(root,'checks'),{recursive:true});
try {
  for (const viewport of [{width:1440,height:1000},{width:390,height:844}]) {
    const page = await browser.newPage({viewport});
    const errors=[];
    page.on('pageerror',e=>errors.push(String(e)));
    await page.goto(pathToFileURL(path.join(root,'comparison.html')).href);
    assert.equal(await page.locator('article').count(),12);
    const rows=await page.locator('article').evaluateAll(as=>as.map(a=>({id:a.id,prose:[...a.querySelectorAll('.prose')].map(p=>p.textContent),initial:a.querySelector('.initial-prose').textContent})));
    for (const r of rows) {const m=mapping.find(m=>m.id===r.id);assert.deepEqual(r.prose,[raw('baseline',m),raw('candidate',m)]);assert.equal(r.initial,raw('initial',m));}
    const allGeometry=await page.locator('article').evaluateAll(as=>as.map(a=>[...a.querySelectorAll('.version')].map(v=>{const r=v.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,overflow:v.scrollWidth>v.clientWidth}})));
    for (const [a,b] of allGeometry) {assert(!a.overflow&&!b.overflow);if(viewport.width>760)assert(a.right<=b.left);else assert(a.bottom<=b.top);}
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=document.documentElement.clientWidth));
    for (const p of read('papers.json')) {
      await page.selectOption('#paper',p.id);
      assert.equal(await page.locator('article:visible').count(),2);
      for (const s of ['1','2']) {await page.selectOption('#sample',s);assert.equal(await page.locator('article:visible').count(),1);}
      await page.selectOption('#sample','all');
    }
    await page.selectOption('#paper','A01');
    await page.selectOption('#sample','1');
    const first=page.locator('article:visible').first();
    await first.locator('.version details').first().locator('summary').click();
    assert.equal(await first.locator('.version details').first().getAttribute('open'),'');
    const geometry=await first.evaluate(a=>({columns:[...a.querySelectorAll('.version')].map(v=>{const r=v.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,overflow:v.scrollWidth>v.clientWidth}}),width:document.documentElement.scrollWidth,viewport:document.documentElement.clientWidth}));
    assert(geometry.width<=geometry.viewport);assert(geometry.columns.every(c=>!c.overflow));
    const [a,b]=geometry.columns;if(viewport.width>760)assert(a.right<=b.left);else assert(a.bottom<=b.top);
    await first.evaluate(a=>a.scrollIntoView({block:'start'}));
    await page.screenshot({path:path.join(root,'checks',`abstract-${viewport.width}.png`)});
    assert.deepEqual(errors,[]);
    results.push({viewport,pairs:12,raw_prose_strings_verified:36,filters:true,details:true,no_overflow_or_overlap:true,page_errors:0});
    await page.close();
  }
} finally {await browser.close();}
assert(!fs.existsSync(path.join(root,'browser_verification.json')));
fs.writeFileSync(path.join(root,'browser_verification.json'),JSON.stringify(results,null,2)+'\n');
console.log(JSON.stringify(results));
