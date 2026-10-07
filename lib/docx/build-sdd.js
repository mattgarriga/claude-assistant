'use strict';
// SDD builder: fills templates/template-sdd.docx. Data schema in README.md.
const X = require('./engine');
const C = require('./common');

const TEMPLATE = 'template-sdd.docx';
const CONTENT_WIDTH_IN = 6.5; // 9360 dxa on US Letter with 1.0in margins

const numOf = (p) => { const pp = X.child(p, 'pPr'); const n = pp && X.child(pp, 'numPr'); return n ? { id: X.wval(X.child(n, 'numId')), lvl: X.wval(X.child(n, 'ilvl')) } : null; };
const isList = (n) => X.local(n) === 'p' && X.paraStyle(n) === 'ListParagraph' && numOf(n);

async function buildSdd(data, opts = {}) {
  const base = opts.baseDir || '.';
  const pkg = await X.Package.open(C.templatePath(TEMPLATE));
  const body = pkg.body;
  const doc = pkg.doc;

  // ---- prototypes captured before any edit
  const spacer = X.clone(X.kids(body, 'p').find((p) => !X.child(p, 'pPr') && !X.kids(p).length));
  const boldTitleProto = X.clone(X.findPara(body, 'Technical Approach Title'));
  const boldRPr = X.child(X.kids(boldTitleProto, 'r')[0], 'rPr');
  const navyTableProto = X.clone(X.tablesIn(body).find((t) => /Component/.test(X.paraText(X.rowsOf(t)[0]))));
  const protoBullet0 = X.clone(X.kids(body, 'p').find((p) => { const n = numOf(p); return n && n.id === '2' && n.lvl === '0'; }));
  const protoBullet1 = X.clone(X.kids(body, 'p').find((p) => { const n = numOf(p); return n && n.id === '2' && n.lvl === '1'; }));
  const protoFile = X.clone(X.findPara(body, /^Filename:/));
  const protoScriptId = X.clone(X.findPara(body, /^Script ID:/));
  const protoScriptType = X.clone(X.findPara(body, /^Script Type:/));
  const protoEbs = X.clone(X.findPara(body, /^EBS \|/));
  const protoParamsLabel = X.clone(X.findPara(body, 'Script Parameters:'));
  const protoOutlineLabel = X.clone(X.findPara(body, 'Script Outline:'));

  const naPara = (text = C.NA) => { const p = X.clone(spacer); X.setRunsText(p, [text]); return p; };
  const heading = (re) => X.findPara(body, (t, p) => X.isHeading(p) && re.test(t));

  const setNA = (h) => {
    const sec = X.sectionNodes(h);
    sec.content.forEach(X.remove);
    X.insertAfter(h, naPara());
  };

  const fillBullets = (h, items) => {
    const sec = X.sectionNodes(h);
    const lists = sec.content.filter(isList);
    if (!items || !items.length) { setNA(h); return; }
    const proto = X.clone(lists[0]);
    const ps = items.map((t) => { const p = X.clone(proto); X.setRunsText(p, [t]); return p; });
    C.insertAllAfter(lists[lists.length - 1], ps);
    lists.forEach(X.remove);
  };

  const tables = X.kids(body, 'tbl');

  // ---- cover table
  const cover = tables[0];
  X.setCell(X.cellsOf(X.rowsOf(cover)[1])[1], C.need(data, 'client'));
  X.setCell(X.cellsOf(X.rowsOf(cover)[2])[1], C.need(data, 'project'));
  X.setCell(X.cellsOf(X.rowsOf(cover)[3])[1], C.need(data, 'customization'));

  // ---- Basic Business Overview
  const ov = tables[1];
  const ovRows = X.rowsOf(ov);
  const ovCell = X.cellsOf(ovRows[0])[1];
  const ps = X.kids(ovCell, 'p');
  const leads = [['Problem', 'problem'], ['Solution', 'solution'], ['Business Impact', 'impact']];
  leads.forEach(([lead, key], i) => {
    const bodyRun = X.kids(ps[i], 'r').filter((r) => X.desc(r, 't').length).pop();
    C.leadIn(ps[i], C.need(data, key), bodyRun);
  });
  X.setCell(X.cellsOf(ovRows[1])[1], data.assumptions && data.assumptions.length ? data.assumptions : ['N/A']);

  // ---- 1 Business Context
  fillBullets(heading(/^1\.1 Current State/), data.currentState);
  fillBullets(heading(/^1\.2 Desired State/), data.desiredState);

  const oqH = heading(/^1\.3 Open Questions/);
  const oqTbl = C.tableAfter(oqH);
  const oqs = data.openQuestions || [];
  if (!oqs.length) {
    X.insertBefore(oqTbl, naPara());
    X.remove(oqTbl);
  } else {
    const rows = X.fitRows(oqTbl, oqs.length);
    oqs.forEach((q, i) => {
      const cs = X.cellsOf(rows[i]);
      X.setCell(cs[0], String(i + 1));
      X.setCell(cs[1], C.need(q, 'question', 'openQuestions[].question'));
      X.setCell(cs[2], q.owner || 'Owner TBD');
      X.setCell(cs[3], q.status || 'Open');
    });
  }

  // ---- 2 Scope
  fillBullets(heading(/^2\.1 In Scope/), data.inScope);
  fillBullets(heading(/^2\.2 Out of Scope/), data.outOfScope);

  // ---- 3 Functional Requirements
  const h3 = heading(/^3\. Functional Requirements/);
  const hFr = X.kids(body, 'p').filter((p) => X.isHeading(p) && /^FR-\d+/.test(X.paraText(p)));
  const h4 = heading(/^4\. Solution Design/);
  const unitOf = (start, endNode) => { const out = []; for (let n = start; n && n !== endNode; n = n.nextSibling) if (X.isEl(n)) out.push(n); return out; };
  const unit1 = unitOf(hFr[0], hFr[1]).map(X.clone);
  const unit2 = unitOf(hFr[1], h4).map(X.clone);
  unitOf(hFr[0], h4).forEach(X.remove);
  const groups = data.functionalRequirements || [];
  if (!groups.length) {
    X.insertAfter(h3, naPara());
  } else {
    groups.forEach((g, gi) => {
      const gid = 'FR-' + String(gi + 1).padStart(2, '0');
      const unit = (gi === groups.length - 1 ? unit2 : unit1).map(X.clone);
      unit.forEach(C.stripBookmarks);
      X.setRunsText(unit[0], [`${gid} ${C.need(g, 'name', 'functionalRequirements[].name')}`]);
      const tbl = unit.find((n) => X.local(n) === 'tbl');
      const reqs = C.need(g, 'requirements', 'functionalRequirements[].requirements');
      const rows = X.fitRows(tbl, reqs.length);
      reqs.forEach((r, ri) => {
        const cs = X.cellsOf(rows[ri]);
        const id = (typeof r === 'object' && r.id) || `${gid}.${ri + 1}`;
        X.setCell(cs[0], id);
        X.setCell(cs[1], typeof r === 'string' ? r : r.text);
      });
      unit.forEach((n) => X.insertBefore(h4, n));
    });
  }

  // ---- 4.1 Process Flow
  const flows = C.need(data, 'processFlow', 'processFlow (4.1 diagram is required)');
  const flowPh = X.findPara(body, /^\[Insert Lucid Chart Process Flow/);
  const flowNodes = [];
  flows.forEach((f, i) => {
    if (i > 0) flowNodes.push(X.clone(spacer));
    if (f.title) { const t = X.clone(boldTitleProto); X.setRunsText(t, [f.title]); X.keepWithNext(pkg, t); flowNodes.push(t); }
    const ip = X.clone(flowPh);
    X.setParaImage(pkg, ip, C.readPng(base, C.need(f, 'png', 'processFlow[].png')), f.width || CONTENT_WIDTH_IN, f.title || 'Process flow');
    flowNodes.push(ip);
  });
  C.insertAllAfter(flowPh, flowNodes);
  X.remove(flowPh);

  // ---- 4.2 Technical Approach
  const h42 = heading(/^4\.2 Technical Approach/);
  const ta = data.technical;
  if (!ta || !ta.title) setNA(h42);
  else {
    const titleP = X.findPara(body, 'Technical Approach Title');
    X.setRunsText(titleP, [ta.title]);
    const detP = X.findPara(body, 'Technical approach details');
    const details = Array.isArray(ta.details) ? ta.details : [ta.details || ''];
    C.insertAllAfter(detP, details.map((d) => { const p = X.clone(detP); X.setRunsText(p, [d]); return p; }));
    X.remove(detP);
    const compLabel = X.findPara(body, 'Component Table');
    const compTbl = C.tableAfter(compLabel);
    const comps = ta.components || [];
    if (!comps.length) {
      const nx = X.nextEl(compLabel);
      if (X.isBlankPara(nx)) X.remove(nx);
      X.remove(compTbl); X.remove(compLabel);
    } else {
      const rows = X.fitRows(compTbl, comps.length);
      comps.forEach((c, i) => {
        const cs = X.cellsOf(rows[i]);
        X.setCell(cs[0], c.component); X.setCell(cs[1], c.type || ''); X.setCell(cs[2], c.purpose || '');
      });
    }
    const klLabel = X.findPara(body, 'Key Logic Notes');
    const klList = X.siblingsAfter(klLabel).find(isList);
    const kl = ta.keyLogic || [];
    if (!kl.length) {
      const nx = X.nextEl(klLabel);
      X.remove(klList); if (X.isBlankPara(nx)) X.remove(nx); X.remove(klLabel);
    } else {
      C.insertAllAfter(klList, kl.map((t) => { const p = X.clone(klList); X.setRunsText(p, [t]); return p; }));
      X.remove(klList);
    }
  }

  // ---- 4.3 Integrations
  const h43 = heading(/^4\.3 Integrations/);
  const intTbl = C.tableAfter(h43);
  const ints = data.integrations || [];
  if (!ints.length) { X.insertBefore(intTbl, naPara()); X.remove(intTbl); } else {
    const rows = X.fitRows(intTbl, ints.length);
    ints.forEach((r, i) => {
      const cs = X.cellsOf(rows[i]);
      X.setCell(cs[0], r.system); X.setCell(cs[1], r.relationship || ''); X.setCell(cs[2], r.notes || '');
    });
  }

  // ---- 4.4 Script Outlines
  const h44 = heading(/^4\.4 Script Outlines/);
  const scripts = data.scripts || [];
  const sec44 = X.sectionNodes(h44);
  sec44.content.forEach(X.remove);
  if (!scripts.length) X.insertAfter(h44, naPara());
  else {
    const out = [];
    scripts.forEach((s, si) => {
      if (si > 0) out.push(X.clone(spacer));
      const e = X.clone(protoEbs); X.setRunsText(e, [`EBS - ${C.need(s, 'name', 'scripts[].name')}`]); out.push(e);
      const mk = (proto, lead, value) => {
        const p = X.clone(proto);
        X.stripFields(p); X.mergeRuns(p);
        const runs = X.kids(p, 'r').filter((r) => X.desc(r, 't').length);
        X.setRunsText(p, [lead + ' ', value]);
        if (runs.length < 2) throw new Error('Unexpected 4.4 line structure for ' + lead);
        return p;
      };
      out.push(mk(protoFile, 'Filename:', C.need(s, 'filename', 'scripts[].filename')));
      out.push(mk(protoFile, 'Folder:', C.need(s, 'folder', 'scripts[].folder')));
      out.push(mk(protoScriptType, 'Script Type:', C.need(s, 'scriptType', 'scripts[].scriptType')));
      out.push(mk(protoScriptId, 'Script ID:', C.need(s, 'scriptId', 'scripts[].scriptId')));
      const params = s.parameters || [];
      if (params.length) {
        out.push(X.clone(protoParamsLabel));
        const t = X.clone(navyTableProto);
        const hdr = X.cellsOf(X.rowsOf(t)[0]);
        ['Name', 'Type', 'Value'].forEach((h, i) => X.setCell(hdr[i], h));
        const rows = X.fitRows(t, params.length);
        params.forEach((pr, i) => {
          const cs = X.cellsOf(rows[i]);
          X.setCell(cs[0], pr.name); X.setCell(cs[1], pr.type || ''); X.setCell(cs[2], pr.value || 'TBD');
        });
        out.push(t);
        out.push(X.clone(spacer));
      }
      out.push(X.clone(protoOutlineLabel));
      for (const o of C.need(s, 'outline', 'scripts[].outline')) {
        const p = X.clone(protoBullet0);
        X.setRunsText(p, o.description ? [o.function, ': ' + o.description] : [o.function]);
        const r0 = X.kids(p, 'r')[0];
        const old = X.child(r0, 'rPr'); if (old) X.remove(old);
        r0.insertBefore(X.clone(boldRPr), r0.firstChild);
        out.push(p);
        for (const st of o.steps || []) { const sp = X.clone(protoBullet1); X.setRunsText(sp, [st]); out.push(sp); }
      }
    });
    C.insertAllAfter(h44, out);
  }

  // ---- 5 Data Model
  const h51 = heading(/^5\.1 New Custom Records/);
  const recs = data.customRecords || [];
  const sec51 = X.sectionNodes(h51);
  const recProto = X.clone(sec51.content.find((n) => /Insert custom record/.test(X.paraText(n))));
  if (!recs.length) setNA(h51);
  else {
    const first = sec51.content.find((n) => /Insert custom record/.test(X.paraText(n)));
    C.insertAllAfter(first, recs.map((t) => { const p = X.clone(recProto); X.setRunsText(p, [t]); return p; }));
    X.remove(first);
  }

  const h52 = heading(/^5\.2 Key Custom Fields/);
  const lab = X.kids(body, 'p').filter((p) => /^\[Insert Record Type \d\]/.test(X.paraText(p)));
  const h6 = heading(/^6\. Approval/);
  const breakP = X.siblingsAfter(lab[1]).find((n) => X.local(n) === 'p' && X.hasPageBreak(n));
  const cu1 = unitOf(lab[0], lab[1]).map(X.clone);
  const cu2 = unitOf(lab[1], breakP).map(X.clone);
  const fields = data.customFields || [];
  if (!fields.length) {
    const sec = X.sectionNodes(h52);
    sec.content.forEach(X.remove);
    X.insertAfter(h52, naPara());
  } else {
    unitOf(lab[0], breakP).forEach(X.remove);
    const all = [];
    fields.forEach((f, i) => {
      const unit = (i === fields.length - 1 ? cu2 : cu1).map(X.clone);
      X.setRunsText(unit[0], [C.need(f, 'record', 'customFields[].record')]);
      const tbl = unit.find((n) => X.local(n) === 'tbl');
      const fl = C.need(f, 'fields', 'customFields[].fields');
      const rows = X.fitRows(tbl, fl.length);
      fl.forEach((r, ri) => {
        const cs = X.cellsOf(rows[ri]);
        X.setCell(cs[0], r.label); X.setCell(cs[1], r.id || ''); X.setCell(cs[2], r.type || ''); X.setCell(cs[3], r.purpose || '');
      });
      all.push(...unit);
    });
    all.forEach((n) => X.insertBefore(breakP, n));
  }

  // ---- 6 Approval
  const apTbl = C.tableAfter(h6);
  const approvers = (data.approvers || []).slice();
  if (!approvers.some((a) => /matthew garriga/i.test(a.name))) {
    approvers.unshift({ name: 'Matthew Garriga', organization: 'Ethos Business Solutions', role: 'Technical Lead' });
  }
  const apRows = X.fitRows(apTbl, approvers.length);
  approvers.forEach((a, i) => {
    const cs = X.cellsOf(apRows[i]);
    X.setCell(cs[0], a.name); X.setCell(cs[1], a.organization || ''); X.setCell(cs[2], a.role || '');
    X.setCell(cs[3], a.date || ''); X.setCell(cs[4], a.decision || '');
  });
  const condLabel = X.findPara(body, 'Conditions:');
  const condList = X.siblingsAfter(condLabel).find(isList);
  const conds = data.conditions || [];
  if (!conds.length) { X.insertBefore(condList, naPara()); X.remove(condList); } else {
    C.insertAllAfter(condList, conds.map((t) => { const p = X.clone(condList); X.setRunsText(p, [t]); return p; }));
    X.remove(condList);
  }

  // ---- 7 Document Control
  const h7 = heading(/^7\. Document Control/);
  const dcTbl = C.tableAfter(h7);
  const dc = C.need(data, 'documentControl');
  const dcRows = X.fitRows(dcTbl, dc.length);
  dc.forEach((r, i) => {
    const cs = X.cellsOf(dcRows[i]);
    X.setCell(cs[0], r.date); X.setCell(cs[1], r.author); X.setCell(cs[2], r.version); X.setCell(cs[3], r.change);
  });
  const links = data.lucidLinks || [];
  if (links.length) {
    const nodes = [X.clone(spacer)];
    for (const l of links) {
      const p = X.clone(spacer);
      const lead = X.clone(X.kids(boldTitleProto, 'r')[0]);
      X.setT(X.desc(lead, 't')[0], (l.label || 'Lucid edit link') + ': ');
      p.appendChild(lead);
      p.appendChild(X.newRun(doc, typeof l === 'string' ? l : l.url));
      nodes.push(p);
    }
    C.insertAllAfter(dcTbl, nodes);
  }

  X.rewriteToc(pkg);
  X.enableUpdateFields(pkg);
  return pkg.toBuffer();
}

module.exports = { buildSdd, TEMPLATE };
