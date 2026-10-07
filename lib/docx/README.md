# lib/docx: template-fill engine

Fills the six Ethos templates in `templates/` from a `data.json`. Untouched parts (styles, theme, fontTable, headers, footers, sectPr) stay byte-identical to the template.

## Run
```
cd lib/docx && npm install          # first time only (jszip, @xmldom/xmldom)
node lib/docx/cli.js <sdd|sow|onepager> <data.json> <out.docx>
node lib/docx/check.js <sdd|onepager|sow-ff|sow-tm|co-ff|co-tm> <out.docx>      # exit 1 on violation
node lib/docx/filled-text.js <same key> <out.docx> | python3 scripts/lint_voice.py - [--design]
lib/docx/render-check.sh <docx> <outdir>                                          # soffice to pdf, pdftoppm -r 80 png
lib/docx/build-all.sh                                                             # all fixtures into lib/docx/out/ plus check.js
```
PNG paths in data.json resolve relative to the data.json file. PNGs must be real PNGs (the engine rejects other formats). `templates/ethos-logo.png` is a JPEG with a .png name; fixtures use `fixtures/standin-diagram.png`.

## Engine behavior
| Rule | Behavior |
|---|---|
| Anchors | Found by heading or label text, never by position alone |
| Prototypes | Paragraphs, rows and cells are cloned from the template; text is replaced, first run's rPr kept |
| Tables | Trimmed to content row count (body rows cloned from the template's first and second body rows) |
| Empty section | Reads "Not applicable to this solution." |
| Spacer paragraphs | Kept as the template ships them |
| Placeholders | `PRICING-PROVIDE-BEFORE-SENDING`, `TBD`, `Owner TBD` pass through untouched. Missing SOW/CO money fields default to `PRICING-PROVIDE-BEFORE-SENDING` |
| Diagram titles | Bold added to a cloned body run, plus keepNext so a title stays with its image |
| Images | Inline PNG; width in inches, height from PNG aspect. Media, relationship and content type added |
| One-Pager formatting | Only the named Filled content snippets in `build-onepager.js` (Calibri 262626, real bullets numId 2) |

## SDD (`sdd`)
| Field | Type | Notes |
|---|---|---|
| client, project, customization | string | Cover table. project is the full text, e.g. "NetSuite Support - 4521" |
| problem, solution, impact | string | Basic Business Overview |
| assumptions | string[] | Assumptions rows ("N/A" if empty) |
| currentState, desiredState | string[] | 1.1 and 1.2 bullets |
| openQuestions | {question, owner?, status?}[] | owner defaults "Owner TBD", status "Open"; empty gives the not-applicable line |
| inScope, outOfScope | string[] | 2.1 and 2.2 |
| functionalRequirements | {name, requirements: (string or {id,text})[]}[] | FR-01.. numbered by order; ids FR-01.1 auto |
| processFlow | {png, title?, width?}[] | Required. 4.1 images at 6.5in |
| technical | {title, details, components?: {component,type,purpose}[], keyLogic?: string[]} | 4.2; omit for not-applicable |
| integrations | {system, relationship, notes}[] | 4.3 |
| scripts | {name, filename, folder, scriptType, scriptId, parameters?: {name,type,value}[], outline: {function, description?, steps?: string[]}[]}[] | 4.4. Heading is "EBS - name". No parameters means the Script Parameters label and table are omitted |
| customRecords | string[] | 5.1 paragraphs |
| customFields | {record, fields: {label,id,type,purpose}[]}[] | 5.2 |
| approvers | {name, organization, role, date?, decision?}[] | Matthew Garriga, Technical Lead is added first if absent |
| conditions | string[] | Conditions bullets |
| documentControl | {date, author, version, change}[] | Required |
| lucidLinks | (string or {label,url})[] | Paragraphs after the Document Control table |

The TOC is rewritten from the real Heading 1 and Heading 2 paragraphs (cached page numbers blank) and `w:updateFields` is set in settings.xml so Word fills page numbers on open.

Minimal example:
```json
{ "client": "Acme", "project": "NetSuite Support - 100", "customization": "Order Intake",
  "problem": "...", "solution": "...", "impact": "...",
  "processFlow": [ { "png": "flow.png" } ],
  "documentControl": [ { "date": "10/07/2026", "author": "Matthew Garriga", "version": "1.0", "change": "Initial Draft" } ] }
```

## SOW and CO (`sow`)
Template chosen by `kind` ("sow" or "co") and `pricing` ("ff" or "tm").
| Field | Type | Notes |
|---|---|---|
| kind, pricing | string | Required |
| client, project, name | string | name is Customization Name (SOW) or Change Order Name (CO) |
| totalFee | string | FF cover row |
| estimatedHours | string | T&M cover row and estimate paragraph |
| problem, solution, impact | string | |
| assumptions | string[] | The skill supplies the 5 standard assumptions plus client ones; engine only fills. CO assumption 4 says "this CO" |
| diagrams | {title, png, width?}[] | Process Overview, 6.9in; empty gives the not-applicable line. Template INCLUDEPICTURE field removed |
| scope.configuration, scope.development | node[] | node = string or {text, children: node[]}. Nests to 3 levels total (the standard bullet is level 1). Leaf text "Type: description" |
| scope.outOfScope | node[] | Appended as a final numbered item "Out of Scope:" with sub-bullets |
| fees (FF) | {total, deposit, balance} | Each defaults to PRICING-PROVIDE-BEFORE-SENDING |
| fees (T&M) | {estimatedFees, hours: {design, configuration, development, uat, training, cutover, support, oversight, total}} | Native table cells; each defaults to the placeholder |
| clientSigner | string | Required. Name under the client "By:" line |
| clientLegalName | string | Optional party name, defaults to client |
| ethosSigner | string | Defaults to "Cedric Carter" |
The acceptance line is written as "this ____ day of ________ 20__".

Minimal example:
```json
{ "kind": "sow", "pricing": "ff", "client": "Acme", "project": "NetSuite Support - 100", "name": "Order Intake",
  "problem": "...", "solution": "...", "impact": "...", "assumptions": ["..."],
  "diagrams": [ { "title": "Future Process", "png": "flow.png" } ],
  "scope": { "configuration": ["Custom Record: Order header"], "development": ["Suitelet: Intake form"] },
  "clientSigner": "Jane Doe" }
```

## One-Pager (`onepager`)
| Field | Type | Notes |
|---|---|---|
| clientProject, requestedBy | string | Request Overview |
| requestType | string | Exactly one of Bug Fix, Config Change, Reporting/Data, Minor Enhancement |
| businessContext, currentState, desiredState, requestDetails | block[] | Required. See blocks |
| inScope, outOfScope | string[] | Bullets; empty gives "N/A" |
| openQuestions | {question, owner?}[] | OQ-01.. numbered; owner defaults "Owner TBD"; status "Open". Empty gives one N/A row |
Blocks: a string (paragraph), `{label, text}` (bold label then text), or `{bullets: (string or {text, sub: string[]})[]}`. Helper lines under headings are removed; the footer line is kept.

Minimal example:
```json
{ "clientProject": "Acme - Support 100", "requestedBy": "Jane Doe", "requestType": "Bug Fix",
  "businessContext": ["..."], "currentState": ["..."], "desiredState": ["..."], "requestDetails": ["..."],
  "inScope": ["..."], "outOfScope": ["..."], "openQuestions": [ { "question": "...", "owner": "Owner TBD" } ] }
```

## Fixtures
`fixtures/` holds one data.json per type for the fictional client Northwind Components (sdd, sow-ff, sow-tm, co-ff, co-tm, onepager). `out/` is gitignored.

## check.js
Compares output to template. Allowed to differ: `word/document.xml`, `word/_rels/document.xml.rels`, `[Content_Types].xml`, `word/media/*`, `docProps/*`, `word/numbering.xml` (One-Pager only), `word/settings.xml` (SDD only). Also asserts sectPr is unchanged, no entry is missing, and entry order matches the template.
