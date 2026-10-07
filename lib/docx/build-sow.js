'use strict';
// SOW and Change Order builder (FF and T&M). Fills the four 2026 templates. Data schema in README.md.
const X = require('./engine');
const C = require('./common');

const FILES = {
  sow: { ff: 'template-sow-fixed-fee.docx', tm: 'template-sow-time-and-materials.docx' },
  co: { ff: 'template-change-order-fixed-fee.docx', tm: 'template-change-order-time-and-materials.docx' },
};
const DIAGRAM_WIDTH_IN = 6.9; // content width 9936 dxa
const BLANK_DATE = '____ day of ________ 20__';

const numPr = (p) => X.child(X.child(p, 'pPr'), 'numPr');

async function buildSow(data, opts = {}) {
  const kind = data.kind;
  const pricing = data.pricing;
  if (!FILES[kind]) throw new Error('data.kind must be "sow" or "co"');
  if (!FILES[kind][pricing]) throw new Error('data.pricing must be "ff" or "tm"');
  const base = opts.baseDir || '.';
  const pkg = await X.Package.open(C.templatePath(FILES[kind][pricing]));
  const body = pkg.body;
  const val = (v) => (v === undefined || v === null || v === '' ? C.PLACEHOLDER : v);

  const tables = X.kids(body, 'tbl');
  const cover = tables[0];
  const overview = tables[1];
  const sig = tables[tables.length - 1];

  // ---- cover table
  const cr = X.rowsOf(cover);
  const valueRun = X.kids(X.child(X.cellsOf(cr[3])[1], 'p'), 'r').filter((r) => X.desc(r, 't').length)[0];
  X.setCell(X.cellsOf(cr[1])[1], C.need(data, 'client'), { proto: valueRun });
  X.setCell(X.cellsOf(cr[2])[1], C.need(data, 'project'), { proto: valueRun });
  X.setCell(X.cellsOf(cr[3])[1], C.need(data, 'name'), { proto: valueRun });
  X.setCell(X.cellsOf(cr[4])[1], val(pricing === 'ff' ? data.totalFee : data.estimatedHours), { proto: valueRun });

  // ---- Basic Business Overview
  const orows = X.rowsOf(overview);
  const ovCell = X.cellsOf(orows[0])[1];
  const asmCell = X.cellsOf(orows[1])[1];
  const bodyRun = X.kids(X.child(asmCell, 'p'), 'r').filter((r) => X.desc(r, 't').length)[0];
  const ps = X.kids(ovCell, 'p');
  [['problem'], ['solution'], ['impact']].forEach(([key], i) => C.leadIn(ps[i], C.need(data, key), bodyRun));
  X.setCell(asmCell, C.need(data, 'assumptions'));

  // ---- Process Overview
  const poHead = X.findPara(body, /^Process Overview:/);
  X.stripFields(poHead);
  const ph = X.findPara(body, /^\[Insert Lucid Chart Diagram/i);
  const diagrams = data.diagrams || [];
  const nodes = [];
  const blankAfter = X.nextEl(ph);
  const blankProto = X.clone(blankAfter);
  diagrams.forEach((d, i) => {
    if (i > 0) nodes.push(X.clone(blankProto));
    const t = X.clone(ph);
    X.stripFields(t);
    X.setRunsText(t, [C.need(d, 'title', 'diagrams[].title')]);
    X.makeBold(pkg, X.kids(t, 'r')[0]);
    X.keepWithNext(pkg, t);
    nodes.push(t);
    const ip = X.clone(ph);
    X.stripFields(ip);
    X.setParaImage(pkg, ip, C.readPng(base, C.need(d, 'png', 'diagrams[].png')), d.width || DIAGRAM_WIDTH_IN, d.title);
    nodes.push(ip);
  });
  if (!diagrams.length) {
    const na = X.clone(ph); X.stripFields(na); X.setRunsText(na, [C.NA]); nodes.push(na);
  }
  C.insertAllAfter(ph, nodes);
  X.remove(ph);

  // ---- Scope and Deliverables
  const scope = data.scope || {};
  const addTree = (labelP, items, ilvl, after) => {
    let cur = after || labelP;
    for (const it of items || []) {
      const node = typeof it === 'string' ? { text: it } : it;
      if (ilvl > 2) throw new Error('Scope bullets nest at most 3 levels');
      const p = X.clone(labelP);
      X.setRunsText(p, [C.need(node, 'text', 'scope item text')]);
      X.child(numPr(p), 'ilvl').setAttribute('w:val', String(ilvl));
      X.insertAfter(cur, p); cur = p;
      cur = addTree(labelP, node.children, ilvl + 1, cur);
    }
    return cur;
  };
  const confP = X.findPara(body, /^Configuration:/);
  const devP = X.findPara(body, /^Development:/);
  addTree(confP, scope.configuration, 1);
  addTree(devP, scope.development, 1);
  if ((scope.outOfScope || []).length) {
    const lastItem = X.findPara(body, /^Cutover &/);
    const oos = X.clone(confP);
    X.setRunsText(oos, ['Out of Scope:']);
    // after the last numbered item
    X.insertAfter(lastItem, oos);
    addTree(oos, scope.outOfScope, 1);
  }

  // ---- Estimated Fees and Billing
  const fees = data.fees || {};
  if (pricing === 'ff') {
    X.replaceInPara(X.findPara(body, /^Based upon the scope/), [[/\$X/, val(fees.total)]]);
    X.replaceInPara(X.findPara(body, /^Upon execution of this/), [[/\$X/, val(fees.deposit)], [/\$X/, val(fees.balance)]]);
  } else {
    const hrs = fees.hours || {};
    X.replaceInPara(X.findPara(body, /^Ethos is estimating a total of/), [[/\bX hours/, val(data.estimatedHours) + ' hours']]);
    const tbl = tables.find((t) => /Estimated Hours and Fees/.test(X.paraText(X.rowsOf(t)[0])));
    const map = { Design: 'design', Configuration: 'configuration', Development: 'development', UAT: 'uat', Training: 'training', Cutover: 'cutover', Support: 'support', 'Project Oversight 20%': 'oversight', 'Hourly Totals': 'total' };
    for (const row of X.rowsOf(tbl)) {
      const cs = X.cellsOf(row);
      const label = X.paraText(cs[0]).trim();
      if (map[label]) X.setCell(cs[1], val(hrs[map[label]]));
      else if (/^Estimated Fees/.test(label)) X.setCell(cs[1], val(fees.estimatedFees));
    }
  }

  // ---- Acceptance line (date left blank)
  X.replaceInPara(X.findPara(body, /^AGREED TO AND ACCEPTED/), [[/X day of Month YYYY/, BLANK_DATE]]);

  // ---- Signatures
  const sc = X.cellsOf(X.rowsOf(sig)[0]);
  const clientName = data.clientLegalName || data.client;
  const clientSigner = C.need(data, 'clientSigner');
  const ethosSigner = data.ethosSigner || 'Cedric Carter';
  const sigParas = (cell, party, signer) => {
    const p = X.kids(cell, 'p');
    if (party) X.setRunsText(p[0], [party]);
    const s = p.find((q) => /^Signor$/.test(X.paraText(q).trim()));
    X.setRunsText(s, [signer]);
  };
  sigParas(sc[0], clientName, clientSigner);
  sigParas(sc[1], null, ethosSigner);

  return pkg.toBuffer();
}

module.exports = { buildSow, FILES };
