# Build Brief: Claude Assistant

You are building out Matt Garriga's personal Claude Code Claude assistant (`claude-assistant` repo) for Ethos Business Solutions. The repo is already scaffolded with migrated standards, skills, commands, templates, and seed client context from his claude.ai Project. Your job is to finish it, wire it up, test it, and seed client context. Read `CLAUDE.md` first; it governs how you work with Matt for the whole build.

## Build team
| Agent | Model | Where defined | Role |
|---|---|---|---|
| Senior engineer | Opus 5.5 (main session) | `docs/build/senior-engineer.md` | Talks to Matt, owns the plan and decisions, dispatches and reviews |
| app-builder | Sonnet 5.5 (subagent) | `.claude/agents/app-builder.md` | Implements task specs |
| tester | Sonnet 5.5 (subagent) | `.claude/agents/tester.md` | Verifies against acceptance criteria, never fixes |

Every phase below runs through the senior engineer loop: plan, dispatch to app-builder, verify with tester, iterate (max 3 cycles), senior review, phase close with Matt. Build artifacts live in `docs/build/` (plan, decisions log, test reports).

## Ground rules for the build
- Do not rewrite migrated standards or skills unless a phase calls for it or Matt approves. They encode decisions already made.
- Never connect to NetSuite.
- Ask Matt before installing anything outside `lib/docx/` dependencies.
- Stop at the end of each phase, show what changed and test results, and wait for Matt's go.
- No emojis, no em dashes in anything you write, including commit messages.

## Phase 0: Environment and connectors
1. Confirm the subagents load (`/agents` lists app-builder and tester on Sonnet 5.5) and that `~/.claude/CLAUDE.md` exists with Matt's user-level instructions.
2. `git init`, initial commit of the scaffold as-is (private, local; Matt picks a remote later if he wants one).
3. Confirm Node 18+, Python 3, LibreOffice (`soffice`) and `pdftoppm` (poppler) are installed. If missing, give Matt the install commands for his OS; don't run installers without asking.
4. Connect the remote MCP servers in `.mcp.json` (Read AI, Smartsheet, Lucid) and complete OAuth. For each, make one read-only call (list Read AI meetings for yesterday, list Smartsheet workspaces, search Lucid for "Process Flow") and report results.
5. Microsoft 365: the claude.ai connector may not be usable from Claude Code. Research options for an Outlook/Graph MCP server that runs locally with delegated auth to Matt's tenant, and present 2 to 3 options with tradeoffs (auth model, maintenance, tenant admin consent needs, draft/reply support). Install only the one Matt picks. Register it under the server name `m365` so the deny rules in `.claude/settings.json` apply. Verify deny rules actually block send.
6. Ask Matt the open decisions listed at the bottom of this file.

## Phase 1: Standards review
1. Diff each `standards/*.md` against its source in `standards/_source/*.docx` (`pandoc -t markdown`). The markdown versions were reconciled on purpose; list every material difference for Matt in one table (Item / Source said / Now says / Why) so he can confirm. Do not revert anything.
2. Apply any changes Matt asks for. After sign-off, `_source/` stays as an archive only.

## Phase 2: lib/docx
1. Build per `lib/docx/SPEC.md`.
2. Create fixtures for SDD, SOW FF, SOW T&M, CO FF, CO T&M, one-pager, recap.
3. Render each to PNG next to the matching template rendered the same way. Show Matt the pairs. Iterate until he signs off.
4. Add `lib/docx/README.md` with the data.json schema per builder.

## Phase 3: Skill tests (dry runs, nothing sent or written to Smartsheet)
The tester runs these; Matt picks the real examples and judges output quality on the first pass of each:
| Test | Pass criteria |
|---|---|
| `/recap` on a real HUT meeting | Correct meeting found, client-facing format exact, no internal content, checklist present, lint clean, write-back proposal shown |
| `/recap` on an internal meeting | Internal variant, named owners |
| `/email` reply to a real thread | Reply draft created in Outlook (not sent), HTML paragraphs, lint clean |
| `/onepager` from a real request | Native-first check happened, docx matches template |
| `/sdd` on a small real feature | Interview runs multiple rounds, Section 4 gate enforced, no draft before gate |
| `/sow` FF with no pricing | Placeholder used, LOE note present |
| `/flow` | Lucid verification step ran and passed before export |
| `/review-design` on an old SDD | Findings table, no edits made |
Fix skill text only where a test fails, and show Matt the diff.

## Phase 4: Dev skills
Gate: `standards/coding-standards.md` must have Matt's real standards (not the placeholder). Ask for it if missing.
1. Confirm `../Repos` access via `additionalDirectories`. List the client repos and ask Matt to map each to a client slug.
2. Test `scripts/guard_git.py` with the tester: commit on main blocked, commit on feature branch allowed, push blocked, suitecloud blocked. All four must behave correctly before any repo work.
3. Dry-run each dev skill on a real repo Matt picks:
| Test | Pass criteria |
|---|---|
| `/review` on a known script | Findings table cites coding standards; no edits made |
| `/debug` with a real past error | Ranked hypotheses, what to check in the account, minimal fix on a fix/ branch |
| `/scaffold` from a locked SDD | Feature branch, script + XML, TODOs for unknowns, no invented field IDs, diff shown before commit |
| `/query` | Correct SuiteQL or formula; flags field IDs it couldn't verify |
| `/migration-audit` | Complete inventory table for the repo |
| `/test-plan` | Includes the second idempotent run |
| `/handoff` | Literal, testable acceptance criteria |

## Phase 5: PM and daily skills
All Smartsheet writes stay preview-and-confirm for every write.
| Test | Pass criteria |
|---|---|
| `/raide hut` from a real meeting | Updates matched to existing rows, no duplicates, preview before write |
| `/tasks` after a recap | Owner TBD preserved, correct sheet routing |
| `/status` (one client, then all) | Read-only, reds first, stale-context flags |
| `/devboard` | Suggestions only, nothing written without confirm |
| `/today` | Three tables plus max 3 first moves |
| `/inbox` | Noise filtered, drafts saved, nothing sent |

## Phase 6: Bootstrap
Run `/bootstrap` per `.claude/skills/client-context/SKILL.md`. For each client, also record the repo path in `client.md` and propose a repo `CLAUDE.md` from `templates/repo-CLAUDE.md` (commit it on a feature branch after Matt approves). 7 core clients (HUT, Cala Health, 4Patriots, CommSel, IMI, Core Transformers, Cerio), 90 days of Read AI, Outlook, and Smartsheet. One client at a time, Matt approves each before writing. Seed lines tagged `[src: claude.ai memory]` are verified or replaced. Commit after each client.

## Phase 7: Hardening
1. Add a PostToolUse hook (or a pre-handoff convention if hooks don't fit) that runs `scripts/lint_voice.py` on any file written under `clients/*/projects/*/outputs/` and on draft text before an Outlook draft is created.
2. Write `README.md` usage section: daily commands, how write-back works, how to add a client.
3. Final commit and a one-paragraph summary to Matt.

## Open decisions to ask Matt in Phase 0
| # | Decision |
|---|---|
| 1 | Email signatures: leave Outlook drafts unsigned, or hard-code a signature block? (Older notes conflict.) |
| 2 | Budget date format in recaps: the source format file said DD.MM.YYYY. Workspace uses MM.DD.YYYY to match US convention. Confirm. |
| 3 | CommSel vs CommSell: canonical spelling for documents. |
| 4 | Client roster: confirm active status of Boxes 4 U and EVgo, and which roster clients are actually inactive. |
| 5 | Where generated outputs should also land, if anywhere besides the repo (OneDrive or SharePoint path). |
| 6 | Branch and commit conventions in `standards/dev-workflow.md` (proposed: feature/ or fix/ plus ticket ID; `type: summary` commits). |
