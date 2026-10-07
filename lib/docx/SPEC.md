# lib/docx Spec (Claude Code builds this in Phase 2)

One Node module that every branded document goes through, so styling lives in one place.

## Layout
```
lib/docx/
  package.json         # depends on "docx"
  brand.js             # tokens from standards/branding.md (single source in code)
  primitives.js        # logoBlock, headerTable, overviewCallout, navyTable, bullets, numbered, callout(note|warning), footerPageNumbers, imageFromPng
  build-sdd.js         # buildSdd(data) -> Buffer
  build-sow.js         # buildSow({kind:'sow'|'co', pricing:'ff'|'tm', ...}) -> Buffer
  build-one-pager.js   # buildOnePager(data) -> Buffer
  build-recap.js       # buildRecap(data) -> Buffer (only used when Matt asks for a file)
  cli.js               # node lib/docx/cli.js <type> <data.json> <out.docx>
  render-check.sh      # docx -> pdf -> png pages for visual inspection
  fixtures/            # sample data.json per type
```

## Contract
- Skills write a `data.json` matching each builder's schema, then call `cli.js`. Skills never write docx-js code inline.
- Schemas documented as JSDoc at the top of each builder.
- US Letter (12240x15840 DXA), 1 inch margins.
- Logo: borderless two-column body table, top-left, 130x91 px, `ImageRun` inside a `Paragraph`.
- Tables: `columnWidths` plus per-cell `width` in DXA; `ShadingType.CLEAR` for fills.
- Bullets via numbering config, never literal bullet characters.
- Headings use built-in `HeadingLevel` so the SDD TOC works.
- Placeholders like `PRICING-PROVIDE-BEFORE-SENDING` pass through untouched.

## Acceptance
For each fixture: generate, render to PNG, and compare side by side against the matching file in `templates/` (rendered the same way). Fonts, colors, table treatment, logo placement, and section order must match. Matt signs off on the four renders before skills are switched to the lib.
