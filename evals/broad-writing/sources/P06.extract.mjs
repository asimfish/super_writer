import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const metadata = JSON.parse(fs.readFileSync(path.join(root, 'metadata/P06.json'), 'utf8'));
const raw = fs.readFileSync(path.join(root, 'sources/P06.extracted.txt'));
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
assert.equal(sha256(raw), metadata.extracted_sha256);
assert.equal(sha256(fs.readFileSync(path.join(root, 'sources/P06.pdf'))), metadata.pdf_sha256);
const pageStarts = [0];
for (let i = 0; i < raw.length; i++) if (raw[i] === 12) pageStarts.push(i + 1);
assert.equal(pageStarts.length - 1, metadata.pages.total_pdf_pages);

function uniqueBoundary(text) {
  const needle = Buffer.from(text, 'utf8');
  const position = raw.indexOf(needle);
  assert(position >= 0, `Missing boundary: ${JSON.stringify(text)}`);
  assert.equal(raw.indexOf(needle, position + 1), -1, `Ambiguous boundary: ${JSON.stringify(text)}`);
  return position;
}

let previousEnd = 0;
const pieces = metadata.ordered_extraction_segments.map(segment => {
  const [start, end] = segment.mode === 'full_pdf_pages'
    ? [pageStarts[segment.pdf_page_range[0] - 1], pageStarts[segment.pdf_page_range[1]]]
    : [uniqueBoundary(segment.start_string), uniqueBoundary(segment.end_string)];
  assert(start >= previousEnd && end > start, `Invalid segment order: ${segment.name}`);
  previousEnd = end;
  const piece = raw.subarray(start, end);
  console.log(JSON.stringify({ segment: segment.name, start_byte: start, end_byte: end, bytes: piece.length }));
  return piece;
});
// Concatenate source byte slices only: no trimming, repair, or inserted delimiters.
const body = Buffer.concat(pieces);
assert.equal(sha256(body), metadata.body_sha256);
assert.equal(body.toString('utf8').split(/\s+/u).filter(Boolean).length, metadata.body_word_count);
fs.writeFileSync(path.join(root, 'inputs/P06.txt'), body);
console.log(JSON.stringify({ output: 'inputs/P06.txt', sha256: sha256(body), bytes: body.length }));
