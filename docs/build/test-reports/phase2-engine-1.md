# Phase 2 engine test report 1 (2026-10-07)

| Check | Result | Evidence | Fix needed |
|---|---|---|---|
| 1 build-all, check.js on 6 | PASS | All 6 built, check.js PASS each | none |
| 2 byte identity (styles, theme, fontTable, settings, header/footer, order) | PASS | 6/6 identical; only SDD settings.xml differs (updateFields, allowed); zip order preserved; extras are media only | none |
| 2 final sectPr identical | FAIL (strict) | One-Pager sectPr differs only in serialization (" />" vs "/>"); other 5 identical. Semantically identical | Serializer normalizes self-closing tags in One-Pager; confirm acceptable or preserve raw bytes |
| 2 One-Pager numbering diff | PASS | abstractNum 2 to 3, num 1 to 2 | none |
| 3 check.js negative test | PASS | 1 byte flipped in styles.xml gives FAIL "protected part changed: word/styles.xml", exit 1 | none |
| 4 content (fixtures present, no placeholders, pricing, SDD EBS heading and Name/Type/Value, N/A line, footer, signers, date blank) | PASS | All fixture strings found in 6 docs; no placeholder strings remain; PRICING-PROVIDE-BEFORE-SENDING in 4 SOW/CO; "EBS - " and N/A line in SDD; signers Pat Lindqvist and Cedric Carter; "____ day of ________ 20__" blank | none |
| 5 filled run formatting | PASS | No 999999/BBBBBB/888888 in any output; One-Pager filled runs Calibri 262626 non-italic; remaining italics are template banner and footer line (AAAAAA, kept) | none |
| 6 visual review | PASS with defects | See list in return message | Matt review |
| 7 lint_voice on filled text, secret scan | PASS | clean x6 (--design on SDD); no secrets in lib/docx | none |
| 8 unittest | PASS | 59 tests OK | none |

Visual defects: (1) One-Pager p1 OPEN QUESTIONS heading orphaned at page bottom, table on p2. (2) SDD p3 FR-01 table has only its first row at the bottom of the page, rest on p4. (3) SDD TOC page numbers blank until Word updates fields (expected). (4) SDD p1 mostly empty (cover then TOC break; check against template). (5) SOW stand-in diagram renders huge (logo image, full page) and pushes the Future Process title to next page; fixture artifact. (6) SOW T&M fees page: table narrower than text width and PRICING-PROVIDE-BEFORE-SENDING wraps three lines per cell (check template width); signature block spills to p6.
Overall: PASS (one strict nit on One-Pager sectPr serialization).
