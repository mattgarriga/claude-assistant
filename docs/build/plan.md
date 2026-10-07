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

## Phase 4 (revised 2026-10-07)
Dev skills in scope: /review, /debug, /query, /test-plan, /handoff (scaffold and migration-audit removed; ethos-dev and suitescript-migrator plugins cover them). Rewrite each to cite coding-standards (ethos-dev conventions) sections and the 10.4 checklist. Tests on ../Repos/cerio and ../Repos/imi; dirty or mid-ticket checkout means stop and ask. guard_git verified in Phase 0.

## Phase 5 (revised 2026-10-07)
/raide, /tasks, /status, /devboard, /today, /inbox against real sheets, all writes preview and confirm. Create "Matt Garriga - Action Log" (RAIDE columns plus Source) with Matt's confirm, record its ID in standards/tools.md.

## Phase 6 (revised 2026-10-07)
| # | Task | Owner | Acceptance |
|---|---|---|---|
| 6.1 | Discovery table for 13 active clients: email domains, Read AI folder, MS RAIDE, project RAIDEs and plans, Dev Tracker client value, Lucid folder, repo path | senior | Matt confirms the table |
| 6.2 | Parallel read-only drafts per client (90 days Read AI, Outlook, Smartsheet) | app-builder x N | Every line source-tagged; claude.ai seed lines verified or replaced; conflicts and low-confidence items listed |
| 6.3 | Per-client review and write, core first | senior, Matt | Written only after approval; one commit per client |
| 6.4 | Local repo CLAUDE.md for clients with a repo, excluded via .git/info/exclude | app-builder | Not in git status of the client repo |

## Phase 7 (revised 2026-10-07)
| # | Task | Acceptance |
|---|---|---|
| 7.1 | PostToolUse hook: lint (warn) on writes under clients/*/projects/*/outputs/ (docx via text extraction); PreToolUse warn on outlook draft tools | Warning shown, write not blocked |
| 7.2 | Secret scan in lint_voice.py (keys, tokens, passwords); blocks on outputs, drafts, clients/** | Test strings blocked, normal text passes |
| 7.3 | /health-check command: live connector IDs vs settings.json deny rules, fake-ID send and delete tests | Detects a mismatched ID in a test copy |
| 7.4 | Weekly scheduled /client-update sweep proposing diffs (no auto-write) | Scheduled task listed; dry run produces proposals |
| 7.5 | README usage section; final commit; one-paragraph summary | Matt reads it |

## Added scope (2026-10-07)
| # | Item | Phase | Acceptance |
|---|---|---|---|
| S1 | Merge .claude/commands into .claude/skills, short names (recap, sdd, onepager, sow, co, flow, email, raide, tasks, status, devboard, today, inbox, review, debug, query, test-plan, handoff, client-update, new-client, bootstrap, review-design); update CLAUDE.md table | 1 | Every slash command still resolves; no commands/ folder |
| S2 | Day-to-day agents in .claude/agents: scout (claude-haiku-4-5-20251001, read-only Read AI/Outlook/Teams/Smartsheet/calendar fetch and filter), meeting-analyst (claude-sonnet-5-5, structured meeting extraction with glossary name fixes), doc-producer (claude-sonnet-5-5, lib/docx fill, render, lint, secret scan), qa-gate (claude-sonnet-5-5, client-facing leakage/format/owner/checklist gate), code-reviewer (claude-sonnet-5-5, conventions review in client repos); design-reviewer pinned to claude-opus-5-5. Skills route to them; tool lists least-privilege (scout and qa-gate have no write tools) | 5 (doc-producer in 2, code-reviewer in 4) | Each skill's raw data stays in the agent; main session gets summaries; tester confirms tool restrictions |
| S11 | Auth guard: scripts/guard_auth.py registered for SessionStart and PreToolUse (Bash, Write, Edit, NotebookEdit); ANTHROPIC_API_KEY and ANTHROPIC_AUTH_TOKEN blanked in user and project settings env; Matt sets managed forceLoginMethod | 0 | tests/test_guard_auth.py passes; managed file present |
| S3 | Gitignore *-draft.docx in outputs; only finals committed | 1 | git status ignores drafts |
| S4 | /agenda <client>: RAIDE rows in "Status Meeting" status plus overdue, blocked, and items new since last meeting; /today prep blocks include it | 5 | Real HUT agenda reviewed by Matt |
| S5 | Teams chats (read-only) in /today and /inbox needs-attention lists | 5 | Unanswered asks to Matt appear; no Teams writes possible |
| S6 | Budget burn from RAIDE Estimated Hours / Case Total Hours / Case Total Hours this month for recap Budget Metrics and /status | 5 | Numbers sourced and cited; missing values noted, never invented |
| S7 | /invitra: weekly digest of Dev Tracker rows assigned to Invitra, aging, open branches in local repos | 5 | Read-only; matches tracker |
| S8 | /sow-review: read-only check of a SOW/CO (standard assumptions, placeholders left, scope creep risk, template version, LOE sign-off) | 3b | Findings table on a real SOW, no edits |
| S9 | /wrap: Friday wrap from the week's daily/ files: done, slipped, next week, sendable update for Cedric and Cheyenne (draft only) | 5 | Lint clean, not sent |
| S10 | Move BUILD_BRIEF.md and KICKOFF.md into docs/build/ | 7 | Root holds only usage files |
