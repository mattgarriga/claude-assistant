# Ethos Branding Standards (.docx)

All branded output is built through `lib/docx/`. The reference templates in `templates/` are the visual source of truth. If a template and this file disagree on layout, the template wins; on tokens below, this file wins.

## Tokens
| Element | Value |
|---|---|
| Font | Calibri (fallback Arial) |
| Body | 11pt, near-black (#262626), never pure black, never colored |
| Table text | 10pt |
| Primary navy (H1, table header fill) | #1F3864 |
| Accent blue (subheadings, emphasis) | #2E75B6 |
| Table borders | thin, #BFBFBF, all sides |
| Paragraph spacing | 0pt before, 0pt after, unless the template specifies otherwise |
| Paper | US Letter, 1 inch margins, single column |

## Logo
- File: `templates/ethos-logo.png` (source 1316x924).
- Render at 130x91 px. Never distort.
- Placement: top-left of page one in a **borderless two-column table in the document body**. Never the Word header object (it clips). This overrides the older "header" instruction.
- In docx-js, `ImageRun` must be wrapped in a `Paragraph`, never placed directly in section children.

## Tables
- Header row: navy fill, white bold text.
- Data rows: white, no shading, no alternating fills.
- Columns sized to content, not stretched.

## Callouts
- NOTE: light gray fill, navy left border, bold navy "NOTE:" label.
- WARNING: light gray fill, dark red left border, bold dark red "WARNING:" label.

## Layout
- Document title on page one as top-level heading.
- Page numbers in footer for documents over 3 pages.
- No clip art, decorative dividers, or imagery beyond the logo and diagrams.

## Verify
Render every generated .docx to PDF and inspect the pages before handoff (LibreOffice headless + pdftoppm).
