# Build Plan

Maintained by the senior engineer.

## Phase 0: Environment and connectors
| Task | Owner | Acceptance | Status |
|---|---|---|---|
| Subagents load on Sonnet 5.5 | senior | app-builder, tester listed with claude-sonnet-5-5 | Done |
| ~/.claude/CLAUDE.md installed | senior | File exists, repo copy removed | Done |
| Toolchain | senior | node 18+, python3, soffice, pdftoppm, pandoc on PATH | In progress |
| Connectors | senior | One read-only call each to Read AI, Smartsheet, Lucid, M365 | Done |
| Deny rules on connector names | senior | Send/delete calls denied before execution | Done |
| guard_git.py scope and false positives | app-builder, tester | tests/test_guard_git.py passes; 4 brief cases verified independently | In progress |
| git init + initial commit | senior | Commit on main after guard change | Pending |
| Open decisions 1 to 6 | Matt | Answered and recorded | Done |

Phase 0 open items: guard_git.py cycle 2 (bypass fixes) paused mid-edit on Matt's hold; initial commit pending.

## Phase 1: Standards review (revised 2026-10-07)
| # | Task | Owner | Acceptance |
|---|---|---|---|
| 1.1 | Copy the 7 2026 templates and the estimator xlsx into templates/; remove template-meeting-recap.docx | app-builder | md5 of repo copies equals OneDrive originals; old files only in git history |
| 1.2 | Cleaned copies: SDD A4 to US Letter (1in margins kept); One-Pager value-cell fills all white #FFFFFF (Requested By, Request Type change from #D6E4F0) | app-builder, tester | Only pgSz and the named shd fills differ from the originals (XML diff); renders approved by Matt |
| 1.3 | Rewrite standards/branding.md as a per-template spec extracted from template XML (paper, margins, fonts, sizes, colors, spacing, borders, cell margins, logo, header/footer) | app-builder, tester | Every value traceable to the template XML; no "body table, never header" rule; tester spot-checks 20 values |
| 1.4 | Align format files AND the sdd, sow, dev-one-pager skill files to the new templates and logged decisions: sdd-format (EBS - heading replaces template pipe), sow-format (native T&M estimate table, PRICING placeholder, Total Fee row), one-pager-format (new section list), recap-format (no .docx) | app-builder | Section lists match template order exactly |
| 1.5 | Import ETHOS_SUITESCRIPT_STANDARDS.md to standards/coding-standards.md with the 18 gaps as an open list; dev-workflow.md branches feature/EBS-####, hotfix/EBS-####, bugfix/<desc>, commits type: summary | app-builder | No conflicting branch rules left in the repo (grep) |
| 1.6 | Diff every standards/*.md against standards/_source/*.docx and the new templates; one table Item / Source said / Now says / Why, behavior changes first | tester, senior | Every material difference listed; Matt signs off |

## Phase 2: lib/docx (revised 2026-10-07)
Template-fill engine replaces the rebuild-in-code SPEC. Builders load the template, clone its own paragraphs/rows as prototypes, and replace text. They never set fonts, sizes, colors, spacing or borders. Node, jszip + @xmldom/xmldom. Types: SDD, SOW FF, SOW T&M, CO FF, CO T&M, One-Pager. Lint applies to filled content only, not template boilerplate. Acceptance: for each fixture, the XML of every untouched template part is byte-identical to the template, and the PNG render is side-by-side approved by Matt.

### Phase 2 tasks
| # | Task | Owner | Acceptance |
|---|---|---|---|
| 2.0 | Gate: Matt attaches completed example docs (SDD, SOW FF, SOW T&M, CO, One-Pager); extract filled-content formatting per type into branding.md | Matt, senior | Every fillable field has a defined filled style from a real example |
| 2.1 | Engine core: open template, locate anchors by heading/label text, clone prototype paragraphs/rows/cells, replace text, trim unused rows, remove helper lines, insert PNG at content width, save | app-builder | Untouched parts (styles, theme, numbering, headers, footers, sectPr) byte-identical to template |
| 2.2 | Builders per type with documented data.json schema (README) | app-builder | Every section in format files maps to a schema field |
| 2.3 | SDD TOC rewrite plus updateFields flag | app-builder | TOC lists real headings; Word updates page numbers on open |
| 2.4 | Fixtures for 6 types; render to PNG next to template render | tester | Byte-identity checks pass; lint clean on filled content; Matt approves pairs |

## Phase 3 (revised 2026-10-07)
| Part | Tests | Runs |
|---|---|---|
| 3a | /recap client (latest HUT status), /recap internal (HUT 10/06), /email (thread TBD), /flow (rebuild HUT 3D Flight in Claude Test folder), /review-design (HUT 3D Flight SDD) | Alongside Phase 1 |
| 3b | /onepager, /sdd, /sow FF no pricing | After Phase 2 |
