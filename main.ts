// make.fun entry for news-image-20261124 — Node 22, standard library only.
// The image is drawn at build time by tools/render_image.py and shipped as
// entry.png beside this file. This program copies those exact bytes to
// /output/entry.png; it reads nothing else and makes no network calls.
//
// CommonJS `require` is used deliberately: Node 22 runs a bare .ts entrypoint
// as CommonJS when the repository has no package.json, so this runs with
// `node main.ts` and needs no install and no flags.
// MAKEFUN_OUTPUT_DIR stands in for /output outside the grader:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const SOURCE = path.join(__dirname, 'entry.png');
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const DESTINATION = path.join(OUTPUT_DIR, 'entry.png');
const PNG_SIGNATURE = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);

// Check the shipped artifact before copying: a truncated PNG would be
// rejected by the gate, so fail loudly here instead of writing a bad entry.
const bytes = fs.readFileSync(SOURCE);
if (bytes.length > 1048576) {
  throw new Error('entry.png exceeds the one-megabyte gate cap');
}
if (!bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error('entry.png is missing the PNG signature');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error('entry.png exceeds the 1024 by 1024 gate cap');
}

fs.mkdirSync(OUTPUT_DIR, { recursive: true });
fs.writeFileSync(DESTINATION, bytes);

const digest = crypto.createHash('sha256').update(bytes).digest('hex');
console.log(`wrote ${DESTINATION}`);
console.log(`bytes ${bytes.length} dimensions ${width}x${height} sha256 ${digest}`);
