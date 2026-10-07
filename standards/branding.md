# Ethos Branding Standards (.docx)

Per-template spec extracted from the XML of the 2026 templates. The templates win over every older token. Originals live in `templates/source/` (byte-identical to OneDrive); working copies are `templates/template-*.docx`. Builders in `lib/docx/` clone template paragraphs and rows and replace text. They never set fonts, sizes, colors, spacing, or borders (see Filled content rules for the only formatting that is not template-owned).

Source key: each value comes from `word/document.xml` (D), `word/styles.xml` (S), `word/numbering.xml` (N), `word/headerN.xml` / `footerN.xml` (H/F), or `word/theme/theme1.xml` (T). Units: 1 inch = 1440 twips (dxa); font sizes in the XML are half-points; borders `w:sz` in eighths of a point; EMU 914400 per inch.

Hex colors are written without a hash in XML. Navy fills differ by template on purpose (see each section).

## One-Pager (`template-dev-request-one-pager.docx`)

Working copy differs from the original in one way: the value cells for Requested By and Request Type use fill FFFFFF (original D6E4F0), matching Client / Project.

### Page, header, footer
| Item | Value | Src |
|---|---|---|
| Paper | 12240 x 15840 (US Letter), portrait | D sectPr |
| Margins | top 900 (0.625in), bottom 900, left 1080 (0.75in), right 1080; header 708, footer 708 | D sectPr |
| Content width | 10080 (7.0in); tables are 10080 (banner) or 9360 (all others), left aligned | D tblW |
| Header | default only. One paragraph, style Header, containing the logo as an inline image (no table, no anchor) | H header1 |
| Logo | 1195070 x 814705 EMU = 1.31 x 0.89in, inline, left (Header style tabs are center 4680 and right 9360, paragraph has no jc) | H, S |
| Footer | No footer part. A body paragraph at the end holds the footer text line (see Placeholders) | D |

### docDefaults and Normal
| Item | Value | Src |
|---|---|---|
| Font | Arial (ascii, hAnsi, eastAsia, cs) | S docDefaults |
| Size | Not set anywhere in docDefaults or Normal, so the Word default of 10pt applies unless a run sets `w:sz` | S |
| Color | Not set (auto) unless a run sets it | S |
| Paragraph spacing | None in docDefaults or Normal; paragraphs set spacing directly | S |
| Lists | Style ListParagraph is empty (no indent, no spacing); numbering.xml defines abstractNum 1 used by numId 1 | S, N |

### Headings
The template does not use Word heading styles. Section headings are Normal paragraphs with direct formatting.
| Item | Value | Src |
|---|---|---|
| Section heading text | UPPERCASE, Arial bold, color 1F4E79, size default (10pt) | D |
| Spacing | before 220, after 80 | D |
| Rule | Paragraph bottom border: single, sz 6, space 3, color 2E75B6 | D pBdr |

### Tables
| Table | Treatment | Src |
|---|---|---|
| Banner (1 cell) | tblW 10080; cell fill 1F4E79; cell borders all none; cell margins top 280, left 400, bottom 280, right 400; table cellMar left 10, bottom 200, right 10. Line 1: "ETHOS BUSINESS SOLUTIONS" bold 9pt BDD7EE centered, after 60. Line 2: title bold 18pt FFFFFF centered, after 60. Line 3: italic 9.5pt BDD7EE centered | D |
| Request Overview (2 cols, 3 rows) | grid 2400 + 6960, tblW 9360. Label cell: fill F2F2F2, text bold 404040. Value cell: fill FFFFFF (cleaned copy), text italic 999999. Cell borders single sz 1 CCCCCC all sides; cell margins top 80, left 120, bottom 80, right 120 | D |
| Free text box (1 cell, 9360) | No fill. Cell borders single sz 1 CCCCCC; margins top 120, left 120, bottom 300 (Business Context) or 320 (Request Details), right 120. Text italic BBBBBB | D |
| Two column compare (Current vs Desired State) | grid 4680 + 4680. Header row fill 1F4E79, text bold FFFFFF, margins 80/120/80/120. Body row margins top 120, left 120, bottom 300, right 120, text italic BBBBBB | D |
| Scope (In Scope / Out of Scope) | Same as compare table. Body row margins top 100, left 120, bottom 240, right 120 | D |
| Open Questions (4 cols) | grid 540 + 5820 + 1800 + 1200, tblW 9360. Header row fill 1F4E79, text bold FFFFFF. Body rows margins 80/120/80/120 (# column 80/80/80/80). # cell: centered, 9.5pt, 404040 ("OQ-01" format). Status cell: fill EBF5FB, centered, 9.5pt, color 2E75B6, text "Open". Question and Owner cells: empty paragraph, no run formatting | D |
| All tables | tblBorders single sz 4 auto (overridden per cell by the sz 1 CCCCCC borders, except banner which is none); tblCellMar left 10, right 10, plus top 60 / bottom 160 (or 200 on the banner). No tblHeader rows, no row heights | D |

### Placeholders
| Item | Styling | Src |
|---|---|---|
| Helper (instruction) line under each heading | Italic 9pt color 888888; spacing before 60, after 60 | D |
| Value cell placeholders (Client / Project, Requested By, Request Type) | Italic 999999 (size default 10pt) | D |
| Body cell placeholders | Italic BBBBBB | D |
| Banner subtitle | Italic 9.5pt BDD7EE (permanent text, not a placeholder) | D |
| Footer text line | Last body paragraph: before 160, centered, top border single sz 4 space 6 color CCCCCC; run italic 8.5pt AAAAAA. Text: "Ethos Business Solutions  |  Development Request One-Pager  |  Attach to Smartsheet Intake Form". A blank paragraph (before 160) precedes it | D |
| Open Questions Status text | Template ships "Open" in 2E75B6 on EBF5FB | D |

## SDD (`template-sdd.docx`)

Working copy differs from the original in one way: pgSz changed from 11906 x 16838 (A4) to 12240 x 15840 (US Letter). Margins unchanged.

### Page, header, footer
| Item | Value | Src |
|---|---|---|
| Paper | 12240 x 15840 (US Letter) in the cleaned copy; no orient attribute (portrait) | D sectPr |
| Margins | top, bottom, left, right 1440 (1.0in); header 708, footer 708 | D sectPr |
| Content width | 9360 on Letter. Table grids and tcW values were built for A4 (cover tables sum to 8985, FR tables 9016); tblW is 5000 or 4994 pct, so tables scale to the text width | D |
| Header | default only. One paragraph (Normal, tab center 4513) with an inline logo image, no table | H header1 |
| Logo | 1186815 x 817245 EMU = 1.30 x 0.89in, inline, left | H |
| Footer | default only. One centered paragraph: field PAGE, text " of ", field NUMPAGES ("1 of 2" cached). All runs 9pt (sz 18), color 666666 | F footer1 |
| Title page | titlePg not set; same header and footer on every page | D |

### docDefaults and Normal
| Item | Value | Src |
|---|---|---|
| Font | Calibri (ascii, hAnsi, eastAsia, cs) | S docDefaults |
| Size | 11pt (sz 22, szCs 22) | S |
| Color | 333333 | S |
| Paragraph spacing | None (pPrDefault empty; Normal has no pPr) | S |
| Theme fonts | major Aptos Display, minor Aptos (used only by TOC styles) | T |

### Heading styles
| Style | Color | Size | Other | Src |
|---|---|---|---|---|
| Heading1 | 2E74B5 | 16pt (sz 32) | outlineLvl 0; no bold, no spacing, no font override (Calibri) | S |
| Heading2 | 2E74B5 | 13pt (sz 26) | outlineLvl 1; same | S |
| Heading3 | 1F4D78 | 12pt (sz 24) | outlineLvl 2; not used in the template body | S |
| TOCHeading | 0F4761 (accent1 shade BF) | 14pt (sz 28) | based on Heading1; bold; major theme font; spacing before 480, line 276 auto | S |
| TOC1 | inherits | 12pt (sz 24) | minor theme font, bold italic, spacing before 120 | S |
| TOC2 | inherits | 11pt | minor theme font, bold, spacing before 120, indent left 220 | S |

Template headings carry typed numbers: "1 Business Context" (no period) but "2. Scope", "3. Functional Requirements", "4. Solution Design", "5. Data Model", "6. Approval and Sign-Off", "7. Document Control" (period). Subheadings "1.1", "4.1" etc. are typed text, not Word list numbering. These inconsistencies are kept as is (decisions log 2026-10-07).

### Tables
Three treatments exist.
| Treatment | Used for | Values | Src |
|---|---|---|---|
| Cover and Document Control | Cover (title row plus Client Name, Project Name, Customization Name), Basic Business Overview / Assumptions, Document Control | tblW 4994 pct (Document Control 5000); tblBorders top, left, bottom, right single sz 12 auto; insideH, insideV single sz 4 auto; tblCellMar left 10, right 10; cell margins top 60, left 100, bottom 60, right 100; paragraph spacing before 40, after 40; text 10pt. Cover title row: one cell spanning 2 columns, fill 1F3864, bold 10pt, color auto. Label column fill 1F3864 (Basic Business Overview, Assumptions rows) with bold 10pt auto text; value column no fill. Document Control header row fill 1F3864; Date and Author headers color auto, Version and Change Reference headers FFFFFF; body rows have top and bottom borders single sz 4 auto | D |
| Open Questions | 1.3 | tblW 5000 pct; same borders and cell margins as the cover treatment (sz 12 outer, sz 4 inner, margins 60/100/60/100, spacing 40/40); header row fill 1F3864 with bold 10pt FFFFFF text; grid 615 + 4010 + 2162 + 2209; body rows 10pt with top and bottom borders single sz 4 auto | D |
| Content tables | Functional Requirements, Component Table, Integrations, Custom Fields, Approval | tblW 5000 pct; tblBorders all six single sz 4 auto; tblCellMar top 72, left 72, bottom 72, right 72 (no paragraph spacing, so lines sit tight); header row fill 1F3864 (tblHeader), bold 10pt, color FFFFFF (theme background1); body cells bottom and top borders single sz 4 color D0D4DA; first body row cells fill FFFFFF (others none); ID and name cells 10pt, empty cells and free text cells carry no run size (11pt Normal) | D |
| Auto text color | Cover table header cells and Document Control Date and Author headers | `w:color w:val="auto"` on a 1F3864 cell; Word renders it white. Kept as in the template | D |

### Lists and numbering
| numId | Used for | Definition | Src |
|---|---|---|---|
| 1 | Bullets in Business Context, Scope, Key Logic Notes, Conditions | Level 0: bullet U+25CF, size sz 15 on the bullet, indent left 720 hanging 360. Level 1: bullet U+25CB, left 1440 hanging 360 | N abstractNum 1 |
| 2 | 4.4 Script Outline | Level 0: Symbol bullet U+F0B7, left 720 hanging 360. Level 1: Courier New "o", left 1440 hanging 360 | N abstractNum 0 |
Both use paragraph style ListParagraph, which is empty (no indent, no spacing, no contextualSpacing).

### Other elements
| Item | Value | Src |
|---|---|---|
| Table of Contents | Content control (sdt) with TOCHeading "Table of Contents", then TOC1 / TOC2 paragraphs inside a TOC field `TOC \o "1-3" \h \z \u` with PAGEREF fields. Preceded by a page break | D |
| Page breaks | After the cover block, after the TOC, before 6. Approval and Sign-Off | D |
| Bold lead-in lines | Plain paragraphs with a bold run: "Technical Approach Title", "Component Table", "Key Logic Notes", "Conditions:", record type labels | D |
| 4.4 script label lines | "EBS | [Script Name]" bold; "Filename:", "Script ID:", "Script Type:" lines bold with run color 1A1A1A; "Script Parameters:" and "Script Outline:" bold 1A1A1A | D |
| Process flow placeholder | Plain text "[Insert Lucid Chart Process Flow Diagram, required]" | D |

### Placeholders
Placeholders are plain text in square brackets, "N/A", "Role", "MM/DD/YYYY", or numbered stand-ins such as "Deliverable 1". They carry no special color, highlight, or italics.

## SOW / CO Fixed Fee (`template-sow-fixed-fee.docx`, `template-change-order-fixed-fee.docx`)

Working copies are byte-identical to the originals. The CO template is the SOW layout with its own wording (title "Change Order (\"CO\")", label "Change Order Name", "this Change Order", "this CO", "total CO").

### Page, header, footer
| Item | Value | Src |
|---|---|---|
| Paper | 12240 x 15840 (US Letter, code 1) | D sectPr |
| Margins | top 90 (0.06in), bottom 90, left 1152 (0.8in), right 1152; header 432, footer 360. Content width 9936 | D sectPr |
| Title page | titlePg on: first page uses first header and footer, later pages use default. Even header and footer parts exist but evenAndOddHeaders is not set in settings, so they are unused | D, settings |
| First page header (header3) | Table, 2 cols (grid 4074 + 5862), bottom border single sz 4 auto only. Left cell: logo, Header style, jc left. Right cell empty. Followed by an empty Header paragraph | H header3 |
| Later page header (header2) | Same table shape (grid 3446 + 6490). Left cell empty, right cell: logo in a Header style paragraph (style jc right). Followed by an empty paragraph | H header2 |
| Logo | 1192013 x 819509 EMU = 1.30 x 0.90in, inline | H |
| Footer, first and later pages | Empty Footer paragraph, then a centered Footer paragraph "Page " PAGE " of " NUMPAGES. Calibri 11pt (sz 22) | F footer2, footer3 |
| Unused parts | header1 (5 empty paragraphs) and footer1 (page number plus empty paragraphs) are the even-page parts, not shown | H, F |

### docDefaults and Normal
| Item | Value | Src |
|---|---|---|
| docDefaults font | Times New Roman | S |
| Normal | Arial; spacing before 120, after 120; left tab 2842; szCs 24; language en-CA. No w:sz, so 10pt when a run does not set a size | S |
| Theme fonts | major Calibri Light, minor Calibri (runs reference minorHAnsi, so body text is Calibri) | T |
| BodyText | Based on Normal; font Book Antiqua; indent left 2520; clears the 2842 tab. Template paragraphs override indent to 0 and runs override the font to minorHAnsi, so the style's own look never shows | S, D |
| Style "paragraph" | Referenced by the Estimated Fees paragraphs but not defined in styles.xml, so those paragraphs resolve to Normal | S, D |
| ListParagraph | Based on Normal; indent left 720; contextualSpacing | S |

### Headings
There are no heading styles. Section titles ("Process Overview:", "Scope and Deliverables:", "Estimated Fees and Billing:", and "Estimated Hours and Fees" in the T&M table) are BodyText paragraphs with ind left 0 and a minorHAnsi bold 12pt run (before/after follow Normal, or 0/0 where set directly). Color is not set (auto).

### Tables
| Table | Treatment | Src |
|---|---|---|
| Cover (title row, Client Name, Project Name, Customization Name or Change Order Name, Total Fee) | tblW 4994 pct; tblBorders outer sz 12 auto, inner sz 4 auto; tblCellMar left 10, right 10; cell margins top 60, left 100, bottom 60, right 100; paragraph spacing before 40, after 40; runs minorHAnsi (Calibri), no size (10pt), labels bold. Title row: one cell spanning 2 columns, fill 1F3864, bold, no color set (renders white on the dark fill). Grid 2362 + 7532 (cell widths 2145 + 6840) | D |
| Business Overview (2 rows) | Same treatment. Label column fill 1F3864, bold, no color set. Value column paragraphs "Problem:", "Solution:", "Business Impact:" (bold lead-in, normal text), and Assumptions lines, one paragraph per line, spacing 40/40 | D |
| Signature (2 cols) | Style TableGrid; tblW 10098 dxa; every cell border nil; row height 2339; each cell holds bold 11pt party name, two empty paragraphs, "By:" line with underscores (11pt), and "Signor" (11pt, color 242424; the right cell paragraph is jc both) | D |
| Layout | The cover table and business overview table sit before the first page break. A spacer paragraph (spacing 0/0) sits between sections | D |

### Lists
| Item | Value | Src |
|---|---|---|
| Scope and Deliverables | numId 34 on BodyText: decimal "%1." level 0 (left 720 hanging 360), lowerLetter "%2." level 1 (left 1440 hanging 360). Runs minorHAnsi 11pt | D, N |

### Body text
Body paragraphs (Process Overview note, Scope items, Estimated Fees and Billing, AGREED TO line) use runs of minorHAnsi 11pt (sz 22). The three Estimated Fees paragraphs are justified (jc both) with spacing 0/0 and are separated by whitespace-only paragraphs. The AGREED TO line has spacing after 200, line 276 auto.

### Placeholders
Plain text in square brackets ("[Insert Lucid Chart Diagram Here]"), "$", "$X", "X day of Month YYYY", "Signor". No special styling. The Process Overview diagram line contains an INCLUDEPICTURE field to a Lucid URL (to be replaced by an embedded PNG).

## SOW / CO Time and Materials (`template-sow-time-and-materials.docx`, `template-change-order-time-and-materials.docx`)

Working copies are byte-identical to the originals. Page, header, footer, docDefaults, styles, cover treatment, lists, and signature table are identical to the Fixed Fee section. Differences:
| Item | Fixed Fee | Time and Materials | Src |
|---|---|---|---|
| Cover last row | "Total Fee" with "$" | "Estimated Hours" with an empty value paragraph | D |
| Business Overview lines | "Problem: [1-2 sentence problem statement]" etc. | "Problem:", "Solution:", "Business Impact:" only (bold, no brackets) | D |
| Process Overview | Heading, then the INCLUDEPICTURE placeholder paragraph | Heading carries the INCLUDEPICTURE field; placeholder line "[Insert Lucid Chart Diagram here]" follows | D |
| Estimated Fees section | Three justified paragraphs (50% on execution, balance on completion, change order language) | One paragraph "Ethos is estimating a total of X hours..." then the Estimated Hours and Fees table, then the "Per the consulting agreement..." invoicing paragraph | D |
| Signature "Signor" (right cell, Ethos) | color 242424 | No color set | D |

### Estimated Hours and Fees table
| Item | Value | Src |
|---|---|---|
| Grid | 6702 + 1533 (8235 total), tblW 0 auto, no tblBorders; borders set per cell | D |
| Cell margins | top 15, left 15, right 15 (no bottom); vAlign bottom on every cell | D |
| Row height | 315 (last row 330) | D |
| Title row | Fill 000000; text "Estimated Hours and Fees" bold 12pt, color FFFFFF (background1). Outer borders sz 8, inner sz 4 | D |
| Phase row | Left cell fill DAE9F8, right cell fill E8E8E8; text "Phase" and "Total", bold 12pt, color 000000 (text1) | D |
| Task rows (Design, Configuration, Development, UAT, Training, Cutover, Support, Project Oversight 20%) | Left cell fill E8E8E8, bold 12pt text1; right cell no fill, right aligned, minorHAnsi (10pt), value "X" | D |
| Hourly Totals row | Both cells fill DAE9F8; label bold 12pt, value right aligned 10pt "X" | D |
| Estimated Fees row | Both cells fill DAE9F8; label "Estimated Fees (Standard Rate: $225)" bold 12pt; value "$X" bold 12pt right aligned. Bottom border sz 8 | D |
| Borders | Outer frame sz 8 (top of title row, bottom of last row, left of first column, right of last column); every other edge sz 4, color auto | D |
| Paragraph spacing | before 0, after 0 in the label cells | D |

## Filled content rules

These rules apply to text Claude writes into a template. Everything else stays exactly as the template ships it. Template boilerplate is exempt from the voice dash rule; only Claude-written content is linted (decisions log 2026-10-07).

### One-Pager
| Element | Rule | Src |
|---|---|---|
| Filled text | Calibri, color 262626, no size set (inherits 10pt). Run properties exactly: `<w:rFonts w:ascii="Calibri" w:eastAsia="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:color w:val="262626"/>` | HUT Workbook Export One-Pager |
| Bold filled text (sub-labels inside a cell) | Same run plus `<w:b/><w:bCs/>` | HUT example |
| Lists | Real bullets. Paragraph properties exactly: `<w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr><w:spacing w:after="40"/>`; nested level uses ilvl 1 | HUT example |
| Plain filled paragraphs in cells | spacing after 60 (short blocks) or after 120 (between paragraphs); centered cells use jc center | HUT example |
| Numbering definition | numId 2 maps to abstractNum 0: level 0 bullet U+25CF, indent left 720 hanging 360; level 1 bullet U+25CB, left 1440 hanging 360; no font or size override on the bullet. The template has the same definition under numId 1. numbering.xml is the one One-Pager part allowed to differ from the template | HUT example numbering.xml, template |
| Labels and headings | Stay template Arial (bold labels 404040, headings 1F4E79). Never restyle | Template |
| Helper instruction lines | Removed from output (the 9pt 888888 lines under each heading) | Decisions log |
| Footer text line | Kept as in the template | Decisions log |
| Placeholder italics | Removed when a cell is filled (the filled run has no italic and uses the filled style above) | Decisions log |
| Value cells | Requested By and Request Type use the same FFFFFF fill as Client / Project (cleaned template) | Decisions log |
| Credentials | Never copy secrets from example documents (the HUT example contains a plaintext key; it is excluded from repo and fixtures) | Decisions log |

### SDD
| Element | Rule | Src |
|---|---|---|
| Body text | 11pt Calibri 333333 from docDefaults; no direct run formatting | Template |
| Tables | 10pt where the template sets sz 20; use the template's cells as prototypes | Template, decisions log |
| 4.4 Script Outlines heading | "EBS - [Name]" (the template pipe text is replaced on fill) | Decisions log |
| 4.4 detail lines | Filename, Folder, Script Type, Script ID lines, in that order, then Script Parameters as a navy-header (1F3864) Name / Type / Value table using the content table treatment, then Script Outline | Decisions log, 3D Flight SDD |
| Process flows | Lucid PNG at content width; Lucid edit link in Document Control; the INCLUDEPICTURE link is removed | Decisions log |
| TOC | Entries rewritten from real headings; field flagged to update on open | Decisions log |
| Empty tables and sections | Rows trimmed to content count; an empty section reads "Not applicable to this solution." | Decisions log |
| Heading numbering | Template typing kept (see SDD Heading styles note) | Decisions log |

### SOW and CO
| Element | Rule | Src |
|---|---|---|
| Layout | 2026 template layout: cover table, Business Overview, Process Overview, Scope and Deliverables, Estimated Fees and Billing, signatures. No Document Control table and no address header | Decisions log |
| CO | Uses the CO template's own wording | Decisions log |
| Money | Total Fee, 50% invoice amount, balance, and T&M hours and fees all stay `PRICING-PROVIDE-BEFORE-SENDING` until Matt supplies them | Decisions log |
| T&M | Native Estimated Hours and Fees table filled with the template cells; numbers stay as placeholders until supplied | Decisions log |
| Process Overview | Lucid diagrams only, 6.9in wide, no narrative | Decisions log |
| Assumptions | The 5 standard assumptions are on by default and editable per document (wording in `sow-format.md`) | Decisions log |
| Signatures | Client signer from `client.md`; Ethos signer Cedric Carter; acceptance date left blank | Decisions log |
| Formatting | Filled text inherits the template run properties (minorHAnsi, 10pt cover cells, 11pt body). Table rows are cloned from the template, not rebuilt | Template |

### All documents
| Rule | Detail |
|---|---|
| No emojis, no em dashes in Claude-written content | Template boilerplate (en dashes, em dashes, curly quotes) is left untouched |
| Untouched parts | Styles, theme, headers, footers, and sectPr stay byte-identical to the template. Exceptions: One-Pager numbering.xml; document.xml body text |
| Callouts and extras | Not part of the templates. Do not add callouts, clip art, or dividers |

## Verify
1. Render every generated .docx to PDF with `soffice --headless --convert-to pdf`, then `pdftoppm -png -r 80`, and inspect every page next to the template render in `docs/build/renders/`.
2. Check the logo placement and size against the section for that template, the table fills, and page count.
3. LibreOffice substitutes fonts (Calibri renders as Carlito, Arial as Liberation Sans, Aptos as a fallback). Judge spacing and layout, not glyph shapes. Word is the final authority for fonts.
4. Run `python3 scripts/lint_voice.py` on the filled text before handoff.
