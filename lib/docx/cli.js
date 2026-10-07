#!/usr/bin/env node
'use strict';
// node lib/docx/cli.js <sdd|sow|onepager> <data.json> <out.docx>
const fs = require('fs');
const path = require('path');

async function main() {
  const [type, dataFile, out] = process.argv.slice(2);
  if (!type || !dataFile || !out) {
    console.error('Usage: node lib/docx/cli.js <sdd|sow|onepager> <data.json> <out.docx>');
    process.exit(2);
  }
  const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
  const opts = { baseDir: path.dirname(path.resolve(dataFile)) };
  let buf;
  if (type === 'sdd') buf = await require('./build-sdd').buildSdd(data, opts);
  else if (type === 'sow') buf = await require('./build-sow').buildSow(data, opts);
  else if (type === 'onepager') buf = await require('./build-onepager').buildOnePager(data, opts);
  else { console.error('Unknown type: ' + type); process.exit(2); }
  fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
  fs.writeFileSync(out, buf);
  console.log('Wrote ' + out);
}
main().catch((e) => { console.error('ERROR: ' + e.message); process.exit(1); });
