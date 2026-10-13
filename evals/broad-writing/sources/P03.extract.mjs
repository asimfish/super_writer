import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const root = new URL('../', import.meta.url);
const path = (name) => fileURLToPath(new URL(name, root));
const id = 'P03';
execFileSync('pdftotext', ['-raw', path(`sources/${id}.pdf`), path(`sources/${id}.extracted.txt`)]);
const raw = readFileSync(path(`sources/${id}.extracted.txt`));
const text = raw.toString('utf8');
assert(raw.equals(Buffer.from(text, 'utf8')), 'Extraction must round-trip unchanged as UTF-8');

const recipe = [
  {
    label: 'Complete main-body Sections 2-4: attention background, methods, and empirical validation',
    start: '2 BACKGROUND\n',
    end: '5 DISCUSSION AND FUTURE DIRECTIONS\n',
    end_inclusive: false,
    expected_pdf_pages: [2, 9],
  },
  {
    label: 'Separately located device, data-type, and programmability scope; excludes Section 5 summary paragraph',
    start: 'Inthenearfuture,weplantocollaboratewithresearchersandengineerstomakeFlashAttentionwidely\n',
    end: '9\fACKNOWLEDGMENTS\n',
    end_inclusive: false,
    expected_pdf_pages: [9, 9],
  },
  {
    label: 'Complete referenced supporting Appendices A-B: Algorithm 2 and all panels of Figures 6-8',
    start: 'A FLASHATTENTION-2 BACKWARD PASS\n',
    end: 'Figure 8: Attention forward + backward speed on H100 GPU\n14\f',
    end_inclusive: true,
    expected_pdf_pages: [12, 14],
  },
];

function uniqueIndex(marker) {
  const index = text.indexOf(marker);
  assert(index >= 0, `Missing boundary: ${JSON.stringify(marker)}`);
  assert(text.indexOf(marker, index + 1) === -1, 'Boundary must be unique');
  return index;
}
const pageAt = (index) => text.slice(0, index).split('\f').length;
let previousEnd = 0;
const pieces = [];
const segments = recipe.map((segment, index) => {
  const start = uniqueIndex(segment.start);
  const markerEnd = uniqueIndex(segment.end);
  const end = markerEnd + (segment.end_inclusive ? segment.end.length : 0);
  assert(start >= previousEnd && end > start, 'Segments must be ordered and nonoverlapping');
  previousEnd = end;
  const selected = text.slice(start, end);
  const lastVisible = end - (selected.match(/\s*$/u)?.[0].length ?? 0) - 1;
  const pdfPages = [pageAt(start), pageAt(lastVisible)];
  assert.deepEqual(pdfPages, segment.expected_pdf_pages, 'Unexpected physical PDF pages');
  pieces.push(Buffer.from(selected, 'utf8'));
  const { expected_pdf_pages, ...boundaries } = segment;
  return {
    order: index + 1,
    ...boundaries,
    start_inclusive: true,
    pdf_pages: pdfPages,
    raw_utf8_byte_range: [Buffer.byteLength(text.slice(0, start)), Buffer.byteLength(text.slice(0, end))],
  };
});
// Concatenate original byte slices without cleaning, labels, or added separators.
const body = Buffer.concat(pieces);
writeFileSync(path(`inputs/${id}.txt`), body);
const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
console.log(JSON.stringify({
  id,
  pdf_sha256: sha256(readFileSync(path(`sources/${id}.pdf`))),
  extracted_sha256: sha256(raw),
  body_sha256: sha256(body),
  body_words_whitespace: body.toString('utf8').split(/\s+/u).filter(Boolean).length,
  extracted_bytes: raw.length,
  body_bytes: body.length,
  extraction_segments: segments,
}, null, 2));
