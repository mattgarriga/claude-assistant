'use strict';
// Template-fill engine. Opens a real Ethos .docx template, locates anchors by text,
// clones the template's own paragraphs, rows and cells as prototypes, and replaces text.
// The engine never invents fonts, sizes, colors, spacing or borders.

const fs = require('fs');
const JSZip = require('jszip');
const { DOMParser, XMLSerializer } = require('@xmldom/xmldom');

const NS_W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main';
const NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships';
const XML_DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n';

const parser = new DOMParser({
  errorHandler: {
    warning() {},
    error(m) { throw new Error('XML error: ' + m); },
    fatalError(m) { throw new Error('XML fatal: ' + m); },
  },
});
const serializer = new XMLSerializer();

// ---------------------------------------------------------------- package

class Package {
  constructor(zip, file) {
    this.zip = zip;
    this.file = file;
    this.text = {};
    this.doms = {};
    this.dirty = new Set();
    this.binary = {};
  }

  static async open(file) {
    const zip = await JSZip.loadAsync(fs.readFileSync(file));
    const pkg = new Package(zip, file);
    for (const name of Object.keys(zip.files)) {
      if (zip.files[name].dir) continue;
      if (/\.(xml|rels)$/.test(name)) pkg.text[name] = (await zip.file(name).async('string')).replace(/^\uFEFF/, '');
    }
    pkg.doc = pkg.dom('word/document.xml');
    pkg.body = child(pkg.doc.documentElement, 'body');
    return pkg;
  }

  // Parsed DOM for a part. Marks the part as modified.
  dom(name) {
    if (!this.doms[name]) {
      if (this.text[name] === undefined) throw new Error('No such part: ' + name);
      this.doms[name] = parser.parseFromString(this.text[name], 'text/xml');
    }
    this.dirty.add(name);
    return this.doms[name];
  }

  setText(name, str) {
    this.text[name] = str;
    delete this.doms[name];
    this.dirty.add(name);
  }

  has(name) { return this.text[name] !== undefined || !!this.zip.files[name]; }

  addBinary(name, buf) { this.binary[name] = buf; }

  async toBuffer() {
    for (const name of this.dirty) {
      let str;
      if (this.doms[name]) {
        str = serializer.serializeToString(this.doms[name]);
        if (!/^<\?xml/.test(str)) str = XML_DECL + str;
      } else str = this.text[name];
      this.zip.file(name, str, { createFolders: false });
    }
    for (const name of Object.keys(this.binary)) {
      this.zip.file(name, this.binary[name], { createFolders: false });
    }
    return this.zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE', compressionOptions: { level: 6 } });
  }

  async save(out) {
    fs.writeFileSync(out, await this.toBuffer());
  }
}

// ---------------------------------------------------------------- dom helpers

const isEl = (n) => n && n.nodeType === 1;
const local = (n) => (n.localName || (n.nodeName || '').replace(/^.*:/, ''));
const kids = (n, name) => Array.from(n.childNodes || []).filter((c) => isEl(c) && (!name || local(c) === name));
const child = (n, name) => kids(n, name)[0] || null;
function desc(n, name, out = []) {
  for (const c of Array.from(n.childNodes || [])) {
    if (!isEl(c)) continue;
    if (!name || local(c) === name) out.push(c);
    desc(c, name, out);
  }
  return out;
}
const wval = (n) => (n ? n.getAttribute('w:val') : null);

function paraText(p) {
  return desc(p, 't').map((t) => t.textContent).join('');
}

function matcher(m) {
  if (typeof m === 'function') return m;
  if (m instanceof RegExp) return (t) => m.test(t);
  return (t) => t.trim() === String(m).trim();
}

// Find paragraphs (anywhere under root) whose text matches. Optional `after` limits to nodes following it in document order.
function findParas(root, m, opts = {}) {
  const f = matcher(m);
  let all = desc(root, 'p');
  if (opts.after) {
    const idx = all.indexOf(opts.after);
    all = all.slice(idx + 1);
  }
  return all.filter((p) => f(paraText(p), p));
}
function findPara(root, m, opts = {}) {
  const r = findParas(root, m, opts)[0];
  if (!r && !opts.optional) throw new Error('Anchor not found: ' + String(m));
  return r || null;
}

function stripIds(n) {
  if (!isEl(n)) return;
  for (const a of ['w14:paraId', 'w14:textId']) if (n.hasAttribute && n.hasAttribute(a)) n.removeAttribute(a);
  for (const c of Array.from(n.childNodes || [])) stripIds(c);
}
function clone(n) {
  const c = n.cloneNode(true);
  stripIds(c);
  return c;
}
function remove(n) { if (n && n.parentNode) n.parentNode.removeChild(n); }
function insertAfter(ref, node) {
  if (ref.nextSibling) ref.parentNode.insertBefore(node, ref.nextSibling);
  else ref.parentNode.appendChild(node);
  return node;
}
function insertBefore(ref, node) { ref.parentNode.insertBefore(node, ref); return node; }
function nextEl(n) { let s = n.nextSibling; while (s && !isEl(s)) s = s.nextSibling; return s; }
function prevEl(n) { let s = n.previousSibling; while (s && !isEl(s)) s = s.previousSibling; return s; }

// Parse an XML snippet (children of a wrapper that declares the document namespaces) into nodes owned by pkg.doc.
function frag(pkg, xml) {
  const root = pkg.doc.documentElement;
  let ns = '';
  for (const a of Array.from(root.attributes)) if (/^xmlns/.test(a.name)) ns += ` ${a.name}="${a.value.replace(/"/g, '&quot;')}"`;
  const d = parser.parseFromString(`<w:frag${ns}>${xml}</w:frag>`, 'text/xml');
  return kids(d.documentElement).map((n) => pkg.doc.importNode(n, true));
}

// ---------------------------------------------------------------- runs and paragraphs

function runIsPlainText(r) {
  const k = kids(r).filter((c) => local(c) !== 'rPr' && local(c) !== 'lastRenderedPageBreak');
  return k.length > 0 && k.every((c) => local(c) === 't');
}
function rPrKey(r) {
  const rp = child(r, 'rPr');
  if (!rp) return '';
  return serializer.serializeToString(rp).replace(/ w:rsid\w*="[^"]*"/g, '');
}

function setT(t, text) {
  while (t.firstChild) t.removeChild(t.firstChild);
  t.appendChild(t.ownerDocument.createTextNode(text));
  t.setAttribute('xml:space', 'preserve');
}

// Remove field machinery (INCLUDEPICTURE etc.) from a paragraph, keep text runs.
function stripFields(p) {
  for (const r of kids(p, 'r')) {
    if (desc(r, 'fldChar').length || desc(r, 'instrText').length) remove(r);
  }
}

function mergeRuns(p) {
  for (const pe of kids(p, 'proofErr')) remove(pe);
  let prev = null;
  for (const r of kids(p, 'r')) {
    if (!runIsPlainText(r)) { prev = null; continue; }
    if (prev && rPrKey(prev) === rPrKey(r)) {
      const t0 = desc(prev, 't')[0];
      setT(t0, t0.textContent + desc(r, 't').map((t) => t.textContent).join(''));
      remove(r);
    } else prev = r;
  }
}

function newRun(doc, text) {
  const r = doc.createElementNS(NS_W, 'w:r');
  const t = doc.createElementNS(NS_W, 'w:t');
  setT(t, text);
  r.appendChild(t);
  return r;
}

// Replace paragraph text. `texts` is a string or array of strings assigned to successive text runs
// (template run formatting is kept). Extra runs are removed; a missing run is cloned from the last.
function setRunsText(p, texts, opts = {}) {
  if (!Array.isArray(texts)) texts = [texts];
  stripFields(p);
  mergeRuns(p);
  let runs = kids(p, 'r').filter((r) => desc(r, 't').length);
  if (!runs.length) {
    const r = newRun(p.ownerDocument, '');
    if (opts.proto) {
      const rp = child(opts.proto, 'rPr');
      if (rp) r.insertBefore(clone(rp), r.firstChild);
    }
    p.appendChild(r);
    runs = [r];
  }
  texts.forEach((txt, i) => {
    if (i < runs.length) {
      const ts = desc(runs[i], 't');
      setT(ts[0], txt);
      ts.slice(1).forEach(remove);
      kids(runs[i], 'tab').forEach(remove);
    } else {
      const last = runs[runs.length - 1];
      const c = clone(last);
      setT(desc(c, 't')[0], txt);
      insertAfter(runs[runs.length - 1], c);
      runs.push(c);
    }
  });
  runs.slice(texts.length).forEach(remove);
  return p;
}
const setParaText = (p, text, opts) => setRunsText(p, [text], opts);

// Regex or string replace across a paragraph whose runs share one format (collapses text into the first run).
function replaceInPara(p, pairs) {
  stripFields(p);
  mergeRuns(p);
  const runs = kids(p, 'r').filter((r) => desc(r, 't').length);
  if (!runs.length) return p;
  // runs with identical rPr are already merged; if more than one remains, merge into the first (body paragraphs only)
  let text = runs.map((r) => desc(r, 't').map((t) => t.textContent).join('')).join('');
  for (const [a, b] of pairs) text = text.replace(a, () => b);
  setRunsText(p, [text]);
  return p;
}

// Add bold to a run (b + bCs, placed after rFonts as the schema requires).
function makeBold(pkg, r) {
  let rp = child(r, 'rPr');
  if (!rp) { rp = frag(pkg, '<w:rPr/>')[0]; r.insertBefore(rp, r.firstChild); }
  if (child(rp, 'b')) return r;
  const nodes = frag(pkg, '<w:b/><w:bCs/>');
  const ref = child(rp, 'rFonts') || child(rp, 'rStyle');
  let cur = ref;
  for (const n of nodes) {
    if (cur) { insertAfter(cur, n); cur = n; } else { rp.insertBefore(n, rp.firstChild); cur = n; }
  }
  return r;
}

// Keep a paragraph on the same page as the next one (used for diagram titles). Pagination only, no visual formatting.
function keepWithNext(pkg, p) {
  let pp = child(p, 'pPr');
  if (!pp) { pp = frag(pkg, '<w:pPr/>')[0]; p.insertBefore(pp, p.firstChild); }
  if (child(pp, 'keepNext')) return p;
  const k = frag(pkg, '<w:keepNext/>')[0];
  const st = child(pp, 'pStyle');
  if (st) insertAfter(st, k); else pp.insertBefore(k, pp.firstChild);
  return p;
}

// Pagination only: keepNext on section headings and on the label paragraph(s) before a table; cantSplit rows and
// keepNext on all but the last row for tables of 6 rows or fewer. Adds no visual formatting.
function paginate(pkg) {
  const body = pkg.body;
  const els = kids(body);
  els.forEach((n, i) => {
    if (local(n) === 'p' && isHeading(n) && paraText(n).trim()) keepWithNext(pkg, n);
    if (local(n) !== 'tbl') return;
    for (let j = i - 1; j >= 0 && local(els[j]) === 'p'; j--) {
      keepWithNext(pkg, els[j]);
      if (!isBlankPara(els[j])) break;
    }
    const rows = rowsOf(n);
    if (rows.length > 6) return;
    rows.forEach((tr, ri) => {
      let trPr = child(tr, 'trPr');
      if (!trPr) {
        trPr = frag(pkg, '<w:trPr/>')[0];
        const first = kids(tr).find((c) => local(c) !== 'tblPrEx');
        tr.insertBefore(trPr, first);
      }
      if (!child(trPr, 'cantSplit')) {
        const cs = frag(pkg, '<w:cantSplit/>')[0];
        const later = kids(trPr).find((c) => ['trHeight', 'tblHeader', 'tblCellSpacing', 'jc', 'hidden', 'ins', 'del', 'trPrChange'].includes(local(c)));
        if (later) trPr.insertBefore(cs, later); else trPr.appendChild(cs);
      }
      if (ri < rows.length - 1) desc(tr, 'p').forEach((p) => keepWithNext(pkg, p));
    });
  });
}

function setPPr(p, xml, pkg) {
  const old = child(p, 'pPr');
  if (old) remove(old);
  const n = frag(pkg, '<w:pPr>' + xml + '</w:pPr>')[0];
  p.insertBefore(n, p.firstChild);
}
function setRPr(r, xml, pkg) {
  const old = child(r, 'rPr');
  if (old) remove(old);
  const n = frag(pkg, '<w:rPr>' + xml + '</w:rPr>')[0];
  r.insertBefore(n, r.firstChild);
}

function hasPageBreak(p) {
  return desc(p, 'br').some((b) => b.getAttribute('w:type') === 'page');
}
const isBlankPara = (n) => isEl(n) && local(n) === 'p' && paraText(n).trim() === '' && !desc(n, 'drawing').length;
function paraStyle(p) {
  const pp = child(p, 'pPr');
  return pp ? wval(child(pp, 'pStyle')) : null;
}
const isHeading = (n) => isEl(n) && local(n) === 'p' && /^Heading[123]$/.test(paraStyle(n) || '');

// ---------------------------------------------------------------- tables

function cellsOf(tr) { return kids(tr, 'tc'); }
function rowsOf(tbl) { return kids(tbl, 'tr'); }
function tablesIn(root) { return desc(root, 'tbl'); }

// Set a cell's paragraphs. `items` is a list; each item is a string or an array of run strings.
// The cell's first paragraph is the prototype for every paragraph.
function setCell(tc, items, opts = {}) {
  if (!Array.isArray(items)) items = [items];
  const ps = kids(tc, 'p');
  const proto = clone(ps[0]);
  ps.forEach(remove);
  let tail = null;
  for (const it of items) {
    const p = clone(proto);
    setRunsText(p, Array.isArray(it) ? it : [it], opts);
    tc.appendChild(p);
    tail = p;
  }
  return tail;
}

// Fit a table's body rows (everything after `headerRows`) to n rows. Prototypes are cloned from the template's
// own first body row (for the first row) and second body row (for the rest, falling back to the first).
function fitRows(tbl, n, headerRows = 1) {
  const rows = rowsOf(tbl);
  const body = rows.slice(headerRows);
  if (!body.length) throw new Error('Table has no body rows to clone');
  const first = clone(body[0]);
  const rest = clone(body[1] || body[0]);
  body.forEach(remove);
  const out = [];
  for (let i = 0; i < n; i++) {
    const r = clone(i === 0 ? first : rest);
    tbl.appendChild(r);
    out.push(r);
  }
  // keep any trailing sectPr-like nodes order: rows were appended after the last remaining node (tblGrid/tr), fine
  return out;
}

// ---------------------------------------------------------------- sections (body-level flows)

function siblingsAfter(node) {
  const out = [];
  for (let s = node.nextSibling; s; s = s.nextSibling) if (isEl(s)) out.push(s);
  return out;
}
// Nodes between a heading paragraph and the next heading (or sectPr). Trailing blank / page-break paragraphs are
// reported separately so section rewrites never remove them.
function sectionNodes(h) {
  const nodes = [];
  for (const s of siblingsAfter(h)) {
    if (isHeading(s) && paraText(s).trim() !== '') break;
    if (local(s) === 'sectPr') break;
    nodes.push(s);
  }
  let end = nodes.length;
  while (end > 0 && isEl(nodes[end - 1]) && local(nodes[end - 1]) === 'p' && paraText(nodes[end - 1]).trim() === '' && !desc(nodes[end - 1], 'drawing').length) end--;
  return { content: nodes.slice(0, end), trailing: nodes.slice(end), all: nodes };
}

// ---------------------------------------------------------------- images

function pngSize(buf) {
  if (buf.readUInt32BE(0) !== 0x89504e47) throw new Error('Not a PNG');
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}

function nextRelId(pkg) {
  const s = pkg.text['word/_rels/document.xml.rels'];
  let max = 0;
  for (const m of s.matchAll(/Id="rId(\d+)"/g)) max = Math.max(max, +m[1]);
  return 'rId' + (max + 1);
}

function nextDocPrId(pkg) {
  let max = 0;
  for (const d of desc(pkg.doc.documentElement, 'docPr')) max = Math.max(max, +d.getAttribute('id') || 0);
  return max + 1;
}

function addImageRel(pkg, buf, hint) {
  let n = 1;
  let name;
  do { name = `word/media/${hint}${n}.png`; n++; } while (pkg.has(name) || pkg.binary[name]);
  const rId = nextRelId(pkg);
  pkg.addBinary(name, buf);
  const relsName = 'word/_rels/document.xml.rels';
  pkg.setText(relsName, pkg.text[relsName].replace('</Relationships>',
    `<Relationship Id="${rId}" Type="${NS_R}/image" Target="${name.replace('word/', '')}"/></Relationships>`));
  const ct = '[Content_Types].xml';
  if (!/Extension="png"/i.test(pkg.text[ct])) {
    pkg.setText(ct, pkg.text[ct].replace(/(<Types[^>]*>)/, '$1<Default Extension="png" ContentType="image/png"/>'));
  }
  return rId;
}

// Build an inline picture run (width in inches, height from the PNG aspect). Optional rPr node is cloned onto the run.
function imageRun(pkg, buf, widthIn, descr, rPrNode) {
  const { w, h } = pngSize(buf);
  const cx = Math.round(widthIn * 914400);
  const cy = Math.round((cx * h) / w);
  const rId = addImageRel(pkg, buf, 'ethos_img');
  const id = nextDocPrId(pkg);
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
  const xml = `<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="${cx}" cy="${cy}"/>` +
    `<wp:docPr id="${id}" name="Picture ${id}" descr="${esc(descr || '')}"/>` +
    `<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>` +
    `<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">` +
    `<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="${id}" name="Picture ${id}"/><pic:cNvPicPr/></pic:nvPicPr>` +
    `<pic:blipFill><a:blip r:embed="${rId}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>` +
    `<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="${cx}" cy="${cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>` +
    `</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>`;
  const r = frag(pkg, xml)[0];
  if (rPrNode) r.insertBefore(clone(rPrNode), r.firstChild);
  return r;
}

// Turn a cloned paragraph into an image paragraph: removes all runs, adds the picture run (rPr from the paragraph's first run).
function setParaImage(pkg, p, buf, widthIn, descr) {
  const first = kids(p, 'r')[0];
  const rp = first ? child(first, 'rPr') : null;
  kids(p, 'r').forEach(remove);
  kids(p, 'proofErr').forEach(remove);
  p.appendChild(imageRun(pkg, buf, widthIn, descr, rp));
  return p;
}

// ---------------------------------------------------------------- SDD table of contents

function rewriteToc(pkg) {
  const doc = pkg.doc;
  const sdt = desc(pkg.body, 'sdt').find((s) => desc(s, 'docPartGallery').some((g) => wval(g) === 'Table of Contents'));
  if (!sdt) throw new Error('TOC content control not found');
  const content = child(sdt, 'sdtContent');
  const paras = kids(content, 'p');
  const styleOf = (p) => paraStyle(p);
  const firstEntry = paras.find((p) => styleOf(p) === 'TOC1');
  const toc1 = paras.filter((p) => styleOf(p) === 'TOC1')[1];
  const toc2 = paras.find((p) => styleOf(p) === 'TOC2');
  const protoFirst = clone(firstEntry);
  const proto1 = clone(toc1);
  const proto2 = clone(toc2);
  const endPara = paras[paras.length - 1];
  const entries = paras.filter((p) => /^TOC[12]$/.test(styleOf(p)));
  entries.forEach(remove);

  // headings outside the sdt
  let bmMax = 0;
  for (const b of desc(doc.documentElement, 'bookmarkStart')) bmMax = Math.max(bmMax, +b.getAttribute('w:id') || 0);
  const heads = kids(pkg.body, 'p').filter((p) => /^Heading[12]$/.test(paraStyle(p) || '') && paraText(p).trim());
  let k = 0;
  let first = true;
  for (const h of heads) {
    let bm = kids(h, 'bookmarkStart').find((b) => /^_Toc/.test(b.getAttribute('w:name')));
    if (!bm) {
      bmMax++; k++;
      const name = '_Toc9' + String(100000 + bmMax) + String(k).padStart(2, '0');
      const [s, e] = frag(pkg, `<w:bookmarkStart w:id="${bmMax}" w:name="${name}"/><w:bookmarkEnd w:id="${bmMax}"/>`);
      const pPr = child(h, 'pPr');
      if (pPr) insertAfter(pPr, s); else h.insertBefore(s, h.firstChild);
      h.appendChild(e);
      bm = s;
    }
    const name = bm.getAttribute('w:name');
    const level = paraStyle(h) === 'Heading1' ? 1 : 2;
    const e = clone(first ? protoFirst : level === 1 ? proto1 : proto2);
    first = false;
    const link = child(e, 'hyperlink');
    link.setAttribute('w:anchor', name);
    const lruns = kids(link, 'r');
    setT(desc(lruns[0], 't')[0], paraText(h));
    for (const it of desc(link, 'instrText')) setT(it, ` PAGEREF ${name} \\h `);
    // cached page number run: the plain text run after the separate fldChar
    const pg = lruns.filter((r) => desc(r, 't').length).pop();
    if (pg && pg !== lruns[0]) setT(desc(pg, 't')[0], '');
    content.insertBefore(e, endPara);
  }
}

function enableUpdateFields(pkg) {
  const name = 'word/settings.xml';
  let s = pkg.text[name];
  if (/<w:updateFields[ />]/.test(s)) return;
  const tag = '<w:updateFields w:val="true"/>';
  const i = s.search(/<w:hdrShapeDefaults[ >\/]|<w:footnotePr[ >\/]/);
  if (i < 0) throw new Error('settings.xml insertion point not found');
  pkg.setText(name, s.slice(0, i) + tag + s.slice(i));
}

// ---------------------------------------------------------------- misc

function removeAll(nodes) { nodes.forEach(remove); }

module.exports = {
  Package, NS_W, NS_R,
  isEl, local, kids, child, desc, wval, paraText, findPara, findParas, clone, remove, insertAfter, insertBefore,
  nextEl, prevEl, frag, setT, newRun, setRunsText, setParaText, replaceInPara, makeBold, keepWithNext, paginate, stripFields, mergeRuns, setPPr, setRPr,
  hasPageBreak, isBlankPara, paraStyle, isHeading, cellsOf, rowsOf, tablesIn, setCell, fitRows, siblingsAfter,
  sectionNodes, pngSize, imageRun, setParaImage, rewriteToc, enableUpdateFields, removeAll, serializer, parser,
};
