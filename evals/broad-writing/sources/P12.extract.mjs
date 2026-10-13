import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = new URL('../', import.meta.url);
const metadata = JSON.parse(readFileSync(new URL('metadata/P12.json', root), 'utf8'));
const raw = readFileSync(new URL('sources/P12.extracted.txt', root));
const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
if (sha256(readFileSync(new URL('sources/P12.pdf', root))) !== metadata.pdf_sha256) {
  throw new Error('PDF checksum mismatch');
}
if (sha256(raw) !== metadata.extracted_sha256) throw new Error('Raw checksum mismatch');

// Byte slices retain Poppler output exactly, including form feeds and font artifacts.
let previousEnd = 0;
const parts = metadata.extraction_segments.map((segment) => {
  const startToken = Buffer.from(segment.start, 'utf8');
  const endToken = Buffer.from(segment.end, 'utf8');
  const start = raw.indexOf(startToken);
  const end = raw.indexOf(endToken, start + startToken.length);
  if (start < previousEnd || end <= start || raw.indexOf(startToken, start + 1) !== -1) {
    throw new Error(`Invalid or ambiguous boundaries: ${segment.label}`);
  }
  const pageAt = (offset) => raw.subarray(0, offset).toString('utf8').split('\f').length;
  if (pageAt(start) !== segment.pdf_pages[0] || pageAt(end - 1) !== segment.pdf_pages[1]) {
    throw new Error(`Page range mismatch: ${segment.label}`);
  }
  previousEnd = end;
  return raw.subarray(start, end);
});
const body = Buffer.concat(parts);
if (sha256(body) !== metadata.body_sha256) throw new Error('Body checksum mismatch');
const words = body.toString('utf8').trim().split(/\s+/u).length;
if (words !== metadata.body_word_count) throw new Error('Word count mismatch');
const output = new URL('inputs/P12.txt', root);
writeFileSync(output, body);
console.log(JSON.stringify({ id: 'P12', path: fileURLToPath(output), words, sha256: sha256(body) }));
