'use strict';
const fs = require('fs');
const path = require('path');
const X = require('./engine');

const TEMPLATES = path.resolve(__dirname, '..', '..', 'templates');
const PLACEHOLDER = 'PRICING-PROVIDE-BEFORE-SENDING';
const NA = 'Not applicable to this solution.';

const templatePath = (name) => path.join(TEMPLATES, name);

function need(data, key, label) {
  const v = key.split('.').reduce((o, k) => (o == null ? o : o[k]), data);
  if (v === undefined || v === null || v === '' || (Array.isArray(v) && !v.length)) {
    throw new Error(`data.json is missing required field: ${label || key}`);
  }
  return v;
}

function readPng(baseDir, p) {
  const abs = path.resolve(baseDir || '.', p);
  if (!fs.existsSync(abs)) throw new Error('PNG not found: ' + abs);
  return fs.readFileSync(abs);
}

// First sibling table after a node
function tableAfter(node) {
  for (const s of X.siblingsAfter(node)) if (X.local(s) === 'tbl') return s;
  throw new Error('No table after anchor: ' + X.paraText(node));
}

// Set "Lead: value" style paragraphs. The first run is the template's lead-in; the value goes in the second run.
// If the template paragraph has only the lead-in run, `bodyRun` (a template run for plain text) supplies the second.
function leadIn(p, value, bodyRun) {
  X.stripFields(p);
  X.mergeRuns(p);
  let runs = X.kids(p, 'r').filter((r) => X.desc(r, 't').length);
  if (runs.length === 1) {
    if (!bodyRun) throw new Error('leadIn needs a body run prototype');
    p.appendChild(X.clone(bodyRun));
    runs = X.kids(p, 'r').filter((r) => X.desc(r, 't').length);
  }
  const lead = X.desc(runs[0], 't')[0].textContent;
  X.setRunsText(p, [lead, (/\s$/.test(lead) ? '' : ' ') + value]);
}

// Insert a list of nodes after ref, in order
function insertAllAfter(ref, nodes) {
  let cur = ref;
  for (const n of nodes) { X.insertAfter(cur, n); cur = n; }
  return cur;
}

function stripBookmarks(node) {
  for (const n of ['bookmarkStart', 'bookmarkEnd']) X.desc(node, n).forEach(X.remove);
}

module.exports = { PLACEHOLDER, NA, templatePath, need, readPng, tableAfter, leadIn, insertAllAfter, stripBookmarks };
