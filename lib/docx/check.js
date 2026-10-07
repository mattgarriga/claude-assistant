#!/usr/bin/env node
'use strict';
// Compare an output .docx with its template.
// Usage: node check.js <sdd|onepager|sow-ff|sow-tm|co-ff|co-tm|path/to/template.docx> <output.docx>
// Exit 1 when a protected part differs, an entry is missing, or entry order changed.
const fs = require('fs');
const path = require('path');
const JSZip = require('jszip');
const { DOMParser, XMLSerializer } = require('@xmldom/xmldom');

const T = path.resolve(__dirname, '..', '..', 'templates');
const KEYS = {
  sdd: 'template-sdd.docx',
  onepager: 'template-dev-request-one-pager.docx',
  'sow-ff': 'template-sow-fixed-fee.docx',
  'sow-tm': 'template-sow-time-and-materials.docx',
  'co-ff': 'template-change-order-fixed-fee.docx',
  'co-tm': 'template-change-order-time-and-materials.docx',
};

function allowedDiff(name, key) {
  if (name === 'word/document.xml' || name === 'word/_rels/document.xml.rels' || name === '[Content_Types].xml') return true;
  if (name.startsWith('word/media/')) return true;
  if (name.startsWith('docProps/')) return true;
  if (name === 'word/numbering.xml' && key === 'onepager') return true;
  if (name === 'word/settings.xml' && key === 'sdd') return true;
  return false;
}

const ser = new XMLSerializer();
const canon = (s) => ser.serializeToString(new DOMParser().parseFromString(s, 'text/xml'));
function sectPrs(xml) {
  const d = new DOMParser().parseFromString(xml, 'text/xml');
  const out = [];
  const walk = (n) => { for (const c of Array.from(n.childNodes || [])) { if (c.nodeType === 1) { if (c.localName === 'sectPr') out.push(ser.serializeToString(c)); walk(c); } } };
  walk(d);
  return out.join('\n');
}

async function main() {
  const [tplArg, outFile] = process.argv.slice(2);
  if (!tplArg || !outFile) { console.error('Usage: node check.js <type|template.docx> <output.docx>'); process.exit(2); }
  const key = KEYS[tplArg] ? tplArg : (tplArg.includes('sdd') ? 'sdd' : tplArg.includes('one-pager') ? 'onepager' : '');
  const tplFile = KEYS[tplArg] ? path.join(T, KEYS[tplArg]) : tplArg;
  const A = await JSZip.loadAsync(fs.readFileSync(tplFile));
  const B = await JSZip.loadAsync(fs.readFileSync(outFile));
  const an = Object.keys(A.files), bn = Object.keys(B.files);
  const violations = [];
  const differ = [];

  for (const n of an) if (!B.files[n]) violations.push('missing entry in output: ' + n);
  for (const n of bn) if (!A.files[n] && !n.startsWith('word/media/')) violations.push('unexpected new entry: ' + n);
  const common = bn.filter((n) => A.files[n]);
  const orderA = an.filter((n) => B.files[n]);
  if (JSON.stringify(common) !== JSON.stringify(orderA)) violations.push('entry order differs from template');

  for (const n of common) {
    if (A.files[n].dir) continue;
    const a = await A.file(n).async('nodebuffer');
    const b = await B.file(n).async('nodebuffer');
    if (!a.equals(b)) {
      differ.push(n);
      if (!allowedDiff(n, key)) violations.push('protected part changed: ' + n);
    }
  }
  // sectPr must match even though document.xml differs
  const sa = sectPrs(await A.file('word/document.xml').async('string'));
  const sb = sectPrs(await B.file('word/document.xml').async('string'));
  if (sa !== sb) violations.push('sectPr changed in document.xml');
  // document-level sanity: the document must still parse
  try { canon(await B.file('word/document.xml').async('string')); } catch (e) { violations.push('document.xml does not parse: ' + e.message); }

  console.log('Template: ' + path.basename(tplFile));
  console.log('Output:   ' + outFile);
  console.log('Entries that differ from template (' + differ.length + '): ' + (differ.join(', ') || 'none'));
  const added = bn.filter((n) => !A.files[n]);
  if (added.length) console.log('Entries added: ' + added.join(', '));
  console.log('sectPr identical: ' + (sa === sb));
  if (violations.length) { console.log('FAIL'); violations.forEach((v) => console.log('  - ' + v)); process.exit(1); }
  console.log('PASS');
}
main().catch((e) => { console.error('ERROR: ' + e.message); process.exit(1); });
