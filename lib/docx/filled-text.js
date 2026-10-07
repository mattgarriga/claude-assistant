#!/usr/bin/env node
'use strict';
// Print the text Claude wrote into a docx: every paragraph in the output that is not template boilerplate.
// Usage: node filled-text.js <sdd|onepager|sow-ff|sow-tm|co-ff|co-tm|template.docx> <output.docx>   (pipe to scripts/lint_voice.py -)
const fs = require('fs');
const path = require('path');
const JSZip = require('jszip');
const { DOMParser } = require('@xmldom/xmldom');
const KEYS = {
  sdd: 'template-sdd.docx', onepager: 'template-dev-request-one-pager.docx',
  'sow-ff': 'template-sow-fixed-fee.docx', 'sow-tm': 'template-sow-time-and-materials.docx',
  'co-ff': 'template-change-order-fixed-fee.docx', 'co-tm': 'template-change-order-time-and-materials.docx',
};
async function paras(file) {
  const z = await JSZip.loadAsync(fs.readFileSync(file));
  const s = (await z.file('word/document.xml').async('string')).replace(/^﻿/, '');
  const d = new DOMParser().parseFromString(s, 'text/xml');
  const out = [];
  for (const p of Array.from(d.getElementsByTagNameNS('http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'p'))) {
    const t = Array.from(p.getElementsByTagNameNS('http://schemas.openxmlformats.org/wordprocessingml/2006/main', 't')).map((x) => x.textContent).join('');
    if (t.trim()) out.push(t);
  }
  return out;
}
(async () => {
  const [k, out] = process.argv.slice(2);
  const tpl = KEYS[k] ? path.resolve(__dirname, '..', '..', 'templates', KEYS[k]) : k;
  const boiler = new Set(await paras(tpl));
  (await paras(out)).filter((t) => !boiler.has(t)).forEach((t) => console.log(t));
})().catch((e) => { console.error('ERROR: ' + e.message); process.exit(1); });
