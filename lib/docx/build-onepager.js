'use strict';
// Development Request One-Pager builder. Fills templates/template-dev-request-one-pager.docx. Data schema in README.md.
const X = require('./engine');
const C = require('./common');

const TEMPLATE = 'template-dev-request-one-pager.docx';
const REQUEST_TYPES = ['Bug Fix', 'Config Change', 'Reporting/Data', 'Minor Enhancement'];

// Filled-content snippets, taken verbatim from standards/branding.md (HUT Workbook Export One-Pager).
// Element order follows the OOXML schema (rFonts, b, bCs, color); the property set is the one branding.md lists.
const RPR_FILLED = '<w:rFonts w:ascii="Calibri" w:eastAsia="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:color w:val="262626"/>';
const RPR_FILLED_BOLD = '<w:rFonts w:ascii="Calibri" w:eastAsia="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:b/><w:bCs/><w:color w:val="262626"/>';
const PPR_BULLET = (lvl) => `<w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="${lvl}"/><w:numId w:val="2"/></w:numPr><w:spacing w:after="40"/>`;
const PPR_AFTER = (n) => `<w:spacing w:after="${n}"/>`;

// numId 2 definition from branding.md: level 0 bullet U+25CF (left 720 hanging 360), level 1 U+25CB (left 1440 hanging 360), no font or size override.
const NUMBERING_ABSTRACT = (id) => `<w:abstractNum w:abstractNumId="${id}"><w:multiLevelType w:val="hybridMultilevel"/>` +
  '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="●"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl>' +
  '<w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="○"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="1440" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>';

function addBulletNumbering(pkg) {
  const name = 'word/numbering.xml';
  let s = pkg.text[name];
  if (/<w:num w:numId="2"[ >]/.test(s)) throw new Error('numId 2 already defined in template numbering.xml');
  const ids = [...s.matchAll(/w:abstractNumId="(\d+)"/g)].map((m) => +m[1]);
  const aid = Math.max(...ids) + 1;
  const i = s.search(/<w:num /);
  s = s.slice(0, i) + NUMBERING_ABSTRACT(aid) + s.slice(i);
  s = s.replace('</w:numbering>', `<w:num w:numId="2"><w:abstractNumId w:val="${aid}"/></w:num></w:numbering>`);
  pkg.setText(name, s);
}

async function buildOnePager(data, opts = {}) {
  const pkg = await X.Package.open(C.templatePath(TEMPLATE));
  const body = pkg.body;
  addBulletNumbering(pkg);

  const type = C.need(data, 'requestType');
  if (!REQUEST_TYPES.includes(type)) throw new Error(`requestType must be one of: ${REQUEST_TYPES.join(', ')}`);

  // remove helper (instruction) lines: italic 9pt 888888 paragraphs
  for (const p of X.kids(body, 'p')) {
    const r = X.kids(p, 'r')[0];
    const rp = r && X.child(r, 'rPr');
    const c = rp && X.child(rp, 'color');
    if (c && X.wval(c) === '888888') X.remove(p);
  }

  const head = (t) => X.findPara(body, (txt, p) => txt.trim() === t && X.kids(body, 'p').includes(p));

  const filledRun = (p, text, bold) => {
    const r = X.newRun(pkg.doc, text);
    X.setRPr(r, bold ? RPR_FILLED_BOLD : RPR_FILLED, pkg);
    p.appendChild(r);
  };

  // Build paragraphs for a cell from blocks (string | {label,text} | {bullets:[string|{text,sub:[]}]}).
  const fillCell = (tc, blocks) => {
    if (!Array.isArray(blocks)) blocks = [blocks];
    const proto = X.clone(X.kids(tc, 'p')[0]);
    X.kids(tc, 'p').forEach(X.remove);
    const out = [];
    blocks.forEach((b, i) => {
      const last = i === blocks.length - 1;
      const mk = (ppr, runs) => {
        const p = X.clone(proto);
        X.kids(p, 'r').forEach(X.remove);
        X.setPPr(p, ppr, pkg);
        runs.forEach(([t, bold]) => filledRun(p, t, bold));
        out.push(p);
      };
      if (typeof b === 'string') mk(PPR_AFTER(last ? 60 : 120), [[b, false]]);
      else if (b.bullets) {
        for (const it of b.bullets) {
          const node = typeof it === 'string' ? { text: it } : it;
          mk(PPR_BULLET(0), [[node.text, false]]);
          for (const sub of node.sub || []) mk(PPR_BULLET(1), [[sub, false]]);
        }
      } else if (b.label) mk(PPR_AFTER(last ? 60 : 120), [[b.label + ': ', true], [b.text || '', false]]);
      else throw new Error('Unknown content block: ' + JSON.stringify(b));
    });
    out.forEach((p) => tc.appendChild(p));
  };
  // Single-value cell (overview): one paragraph, filled run, template paragraph properties kept.
  const fillValue = (tc, text) => {
    const p = X.kids(tc, 'p')[0];
    X.kids(p, 'r').forEach(X.remove);
    filledRun(p, text, false);
  };

  // ---- Request Overview
  const ov = C.tableAfter(head('REQUEST OVERVIEW'));
  const orows = X.rowsOf(ov);
  fillValue(X.cellsOf(orows[0])[1], C.need(data, 'clientProject', 'clientProject'));
  fillValue(X.cellsOf(orows[1])[1], C.need(data, 'requestedBy'));
  fillValue(X.cellsOf(orows[2])[1], type);

  // ---- Business Context
  fillCell(X.cellsOf(X.rowsOf(C.tableAfter(head('BUSINESS CONTEXT')))[0])[0], C.need(data, 'businessContext'));

  // ---- Current vs Desired
  const cd = X.rowsOf(C.tableAfter(head('CURRENT STATE VS. DESIRED STATE')))[1];
  fillCell(X.cellsOf(cd)[0], C.need(data, 'currentState'));
  fillCell(X.cellsOf(cd)[1], C.need(data, 'desiredState'));

  // ---- Request Details
  fillCell(X.cellsOf(X.rowsOf(C.tableAfter(head('REQUEST DETAILS')))[0])[0], C.need(data, 'requestDetails'));

  // ---- Scope and guardrails
  const sc = X.rowsOf(C.tableAfter(head('SCOPE & CLIENT GUARDRAILS')))[1];
  const bl = (v) => (v && v.length ? [{ bullets: v }] : ['N/A']);
  fillCell(X.cellsOf(sc)[0], bl(data.inScope));
  fillCell(X.cellsOf(sc)[1], bl(data.outOfScope));

  // ---- Open Questions
  const oqTbl = C.tableAfter(head('OPEN QUESTIONS'));
  const oqs = data.openQuestions || [];
  const rows = X.fitRows(oqTbl, Math.max(oqs.length, 1));
  if (!oqs.length) {
    const cs = X.cellsOf(rows[0]);
    X.setCell(cs[0], 'N/A'); fillCell(cs[1], 'N/A'); fillCell(cs[2], 'N/A'); X.setCell(cs[3], 'N/A');
  } else {
    oqs.forEach((q, i) => {
      const cs = X.cellsOf(rows[i]);
      X.setCell(cs[0], 'OQ-' + String(i + 1).padStart(2, '0'));
      const plain = (tc, t) => { const p = X.kids(tc, 'p')[0]; X.kids(p, 'r').forEach(X.remove); filledRun(p, t, false); };
      plain(cs[1], C.need(q, 'question', 'openQuestions[].question'));
      plain(cs[2], q.owner || 'Owner TBD');
      X.setCell(cs[3], q.status || 'Open');
    });
  }

  X.paginate(pkg);
  return pkg.toBuffer();
}

module.exports = { buildOnePager, REQUEST_TYPES };
