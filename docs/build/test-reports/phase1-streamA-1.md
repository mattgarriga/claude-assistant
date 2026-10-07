# Phase 1 stream A (1.1 to 1.3) test report 1

| Check | Result | Evidence | Fix needed |
|---|---|---|---|
| 1 md5 source vs OneDrive (7 files) | PASS | All 7 in templates/source/ equal originals | None |
| 1 md5 working copies (4 SOW/CO + xlsx) | PASS | 4 docx equal originals; xlsx md5 2d5fb369... equals original | None |
| 2 SDD cleaned diff | PASS | Only word/document.xml differs; only change pgSz 11906x16838 to 12240x15840; entry order identical | None |
| 2 One-Pager cleaned diff | PASS | Only document.xml differs; two fills D6E4F0 to FFFFFF, in the Requested By and Request Type value cells | None |
| 2 Files open | PASS | soffice converts both, exit 0 | None |
| 3 20 values vs XML | PASS | Verified: OP sectPr 12240x15840, margins 900/1080, hdr/ftr 708; OP grids 10080, 2400+6960, 4680x2; OP banner fill 1F4E79, margins 280/400; OP heading rule 2E75B6 sz6 space3; OP footer border CCCCCC sz4 space6, 8.5pt AAAAAA; OP status fill EBF5FB; OP logo 1195070x814705 inline, no table; OP docDefaults Arial; SDD margins 1440, hdr/ftr 708; SDD Calibri 11pt 333333; H1 2E74B5 32, H2 2E74B5 26, H3 1F4D78 24; SDD fill 1F3864, borders sz12/sz4; SDD content cellMar 72; SDD D0D4DA; SDD logo 1186815x817245; SDD footer 9pt 666666 centered PAGE/NUMPAGES; SOW sectPr 90/1152, hdr 432, ftr 360, titlePg; SOW Normal Arial 120/120 tab 2842; SOW docDefaults Times New Roman; SOW header grids 3446+6490 and 4074+5862, logo 1192013x819509; SOW cover grid 2362+7532; footer sz22; T&M grid 6702+1533, fills 000000/DAE9F8/E8E8E8, row height 315. 0 mismatches | None |
| 3 Removed rule and logo wording | PASS | grep for "body table" / "never header": 0 hits; logo described as inline in header for all templates | None |
| 3 Filled content rules vs decisions log | PASS | One-Pager Calibri 262626, real bullets (numId 2), labels stay Arial, helper lines removed, footer kept; SDD 11pt body / 10pt tables; 4.4 Name/Type/Value table; boilerplate exempt from dash rule; credentials rule. Matches log rows 2026-10-07 | None |
| 4 lint_voice.py on branding.md | PASS | Exit 0, no findings | None |
| 5 Renders exist | PASS | docs/build/renders/phase1/ has orig-* and clean-template-* for all 6 docx (SDD 7 pages, One-Pager 2) | None |
| 5 Visual: clean SDD p1 | PASS | Logo top-left inline, cover tables span the text width, no clipping or overflow, footer "1 of 7" centered | None |
| 5 Visual: clean One-Pager p1 | PASS | Logo top-left, banner, tables aligned, value cells all white. Observation only: "OQ-01" wraps to two lines in the narrow # column (template geometry, LibreOffice render); the Letter change did not cause it | None (Matt review item) |

Minor, non-failing: branding.md says tables span 9360 for the One-Pager while the banner is 10080; both confirmed in XML. Matt's render approval (plan 1.2) is not tested here.

Overall: PASS
