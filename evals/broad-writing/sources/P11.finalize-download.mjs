import { readFileSync, truncateSync } from 'node:fs';

const path = new URL('P11.pdf', import.meta.url);
const bytes = readFileSync(path);
const responseBytes = 1468508;
// The completed proceedings response declares this length in its linearization header.
if (!bytes.subarray(0, 200).includes(Buffer.from(`/L ${responseBytes} `))) {
  throw new Error('Proceedings response length does not match the PDF header');
}
if (!bytes.subarray(responseBytes - 6, responseBytes).equals(Buffer.from('%%EOF\n'))) {
  throw new Error('Proceedings response does not end at its declared EOF');
}
if (bytes.length < responseBytes) throw new Error('Incomplete response');
if (bytes.length > responseBytes) truncateSync(path, responseBytes);
console.log(JSON.stringify({ id: 'P11', response_bytes: responseBytes, discarded_trailing_bytes: bytes.length - responseBytes }));
