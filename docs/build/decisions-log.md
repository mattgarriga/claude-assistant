# Decisions Log

| Date | Decision | Why | Reversible |
|---|---|---|---|
| 2026-10-06 | Use claude.ai connectors (Read AI, Smartsheet, Lucid, M365) instead of .mcp.json servers; removed .mcp.json | Project servers failed (Smartsheet no DCR; Read AI and Lucid need OAuth); connectors already authorized and working. Matt approved | Y |
| 2026-10-06 | Deny/ask rules duplicated onto connector-ID tool names (mcp__<uuid>__*); legacy m365/smartsheet names kept | Old rules matched nothing. Verified: outlook_send_draft, teams_send_chat_message, smartsheet delete_rows all denied pre-execution. Matt approved | Y |
| 2026-10-06 | Calendar writes (create, delete, respond), teams_create_chat, outlook_delete_draft moved to deny | Invites and RSVPs send mail on Matt's behalf; draft-only rule | Y |
| 2026-10-06 | Smartsheet create/sharing/automation writes and Read AI share/create_meeting_agent added to ask; Read AI delete_folder denied | Outward-facing or structural writes the original list did not cover | Y |
| 2026-10-06 | guard_git.py protected-branch commit block scoped to ../Repos; push/merge/rewrite/CLI blocks stay global | Workspace repo commits on main. Matt approved | Y |
| 2026-10-06 | guard_git.py matches only invoked commands, not words in heredocs or quoted text | False positive blocked a docs write | Y |
| 2026-10-06 | Deleted empty stray `{.claude...` directory tree | Artifact of a failed brace-expansion mkdir, contained no files | N/A |
| 2026-10-07 | Document engine: fill Matt's real .docx templates (clone template paragraphs/rows, replace text); builders never set formatting. SPEC.md rebuild-in-code approach dropped | Only way to match templates exactly. Matt approved | Y |
| 2026-10-07 | Templates win over branding.md; branding.md rewritten as a per-template spec extracted from template XML | Templates and branding.md conflicted on logo placement, fonts, paper, borders. Matt approved | Y |
| 2026-10-07 | Template fixes in approved cleaned copies: SDD A4 to US Letter; One-Pager value-cell fills made uniform white #FFFFFF. All other quirks kept (incl. SDD heading numbering) | Matt approved | Y |
| 2026-10-07 | SDD 4.4 script heading stays "EBS - [Name]" (template text "EBS \| [Script Name]" is replaced on fill) | Matt approved | Y |
| 2026-10-07 | Template boilerplate exempt from the no-dash rule; only Claude-written content is linted | Matt approved | Y |
| 2026-10-07 | T&M "Estimated Hours and Fees": native template table, numbers left as PRICING-PROVIDE-BEFORE-SENDING | Matt approved | Y |
| 2026-10-07 | Branches per coding standards: feature/EBS-####, hotfix/EBS-####, bugfix/<desc>. Commits: type: summary | Supersedes 2026-10-06 dev-workflow confirmation. Matt approved | Y |
| 2026-10-07 | Coding standards imported to standards/coding-standards.md; its 18 gaps answered at Phase 4 kickoff | Matt approved | Y |
| 2026-10-07 | Recap .docx dropped from scope (template and builder); recaps are text or Outlook drafts only | Matt approved | Y |
| 2026-10-07 | 2026 templates and estimator xlsx copied into templates/; re-sync on request when OneDrive originals change | Matt approved | Y |
| 2026-10-07 | lib/docx stays Node; template fill via jszip + @xmldom/xmldom (no system installs) | Senior decision within lib/docx authority | Y |
| 2026-10-07 | Filled-content formatting derived from Matt's completed example docs (he attaches 1 to 2 per type); no guessed styling | Templates only show placeholder styling. Matt approved | Y |
| 2026-10-07 | One-Pager helper/instruction lines removed in output; footer text line kept | Matt approved | Y |
| 2026-10-07 | Tables trimmed to content row count; empty sections get "Not applicable to this solution."; template spacer paragraphs kept | Matt approved | Y |
| 2026-10-07 | SDD TOC entries rewritten from real headings, field flagged to update on open (Word prompts once) | Matt approved | Y |
| 2026-10-07 | Process flows embedded as Lucid PNG export at content width; Lucid edit link in SDD Document Control; template INCLUDEPICTURE link removed | Matt approved | Y |
| 2026-10-07 | Git guard residuals accepted: uppercase variants, variable indirection, program-launched commands, piping into a shell; settings.json deny rules are the second layer | Tester cycle 2 PASS, 0 false blocks on ~50 normal commands, ~31ms median | Y |
| 2026-10-07 | One-Pager filled text: Calibri #262626 (prototype runs, ListParagraph style, spacing after 40/60 taken from the HUT Workbook Export One-Pager); labels and headings stay template Arial | Matt chose over the Arial #404040 hand-built examples | Y |
| 2026-10-07 | One-Pager lists use real Word bullets/numbering; numbering.xml is the one One-Pager part allowed to differ from the template | Matt approved | Y |
| 2026-10-07 | SDD filled sizes follow the 2026 template: body 11pt, tables 10pt | Template is newer than the 3D Flight example. Matt approved | Y |
| 2026-10-07 | SDD 4.4: Filename, Folder, Script Type, Script ID lines, then Script Parameters as a navy-header Name / Type / Value table (per 3D Flight SDD); sdd-format.md updated in Phase 1 | Matt approved | Y |
| 2026-10-07 | HUT PrintNode API key found in plaintext in a shared One-Pager; scratch copies deleted, file excluded from repo and fixtures; flagged to Matt | Credential exposure | N/A |
| 2026-10-07 | SOW/CO follow the 2026 layout (no Document Control table, no address header); CO uses the CO template's own wording | Older SOW examples predate the 2026 templates | Y |
| 2026-10-07 | SOW/CO dollar amounts (Total Fee, 50% split, balance) all PRICING-PROVIDE-BEFORE-SENDING | Never invent pricing | Y |
| 2026-10-07 | T&M builders validated on template structure plus FF filled conventions; Matt reviews T&M renders closely | No T&M example available. Matt approved | Y |
| 2026-10-07 | 5 standard assumptions default on for every SOW and CO, editable per doc; canonical wording in sow-format.md | Matt approved | Y |
| 2026-10-07 | Process Overview is titled Lucid diagrams only (6.9in wide), no narrative | Matt approved | Y |
| 2026-10-07 | Signature block: client signer from client.md, Ethos signer Cedric Carter; acceptance date left blank | Matt approved | Y |
| 2026-10-07 | Phase 3 split: 3a (recap client + internal, email, flow, review-design) runs alongside Phase 1; 3b (one-pager, SDD, SOW) after Phase 2 | Daily skills sooner; 3a has no docx dependency. Matt approved | Y |
| 2026-10-07 | 3a examples: latest HUT client status (confirm before run), HUT Internal Status 10/06, email thread TBD (senior proposes candidates, Matt confirms), /review-design on HUT 3D Flight Cost SDD | Matt approved | Y |
| 2026-10-07 | /flow test rebuilds HUT 3D Flight Cost flow into a "Claude Test" Lucid folder; Matt deletes after comparison | Claude cannot delete Lucid docs. Matt approved | Y |
| 2026-10-07 | SDD, SOW, One-Pager skill text updated in Phase 1 task 1.4 alongside format files, diff shown to Matt | Matt approved | Y |
| 2026-10-07 | Recap step 8: RAIDE/project log proposals for client and internal meetings; live-update detected from RAIDE rows modified in the meeting window; routed by type; client-facing filter on both sheets (project plan assumed client-visible, pending Matt) | Matt approved | Y |
| 2026-10-07 | Dirty or mid-ticket client checkout: Claude stops and asks; default offered = commit WIP on its branch, checkout main, create new branch. No worktrees | Matt's call | Y |
| 2026-10-07 | Missing client repo: Claude tells Matt, Matt supplies the clone URL, Claude clones | Matt's call | Y |
| 2026-10-07 | Repo CLAUDE.md stays personal (points into this workspace); standards not committed to client repos | Matt's call | Y |
| 2026-10-07 | Dev skills (review, debug, scaffold, query, migration-audit, test-plan, handoff) rewritten in Phase 4 to cite coding-standards sections, use feature/hotfix/bugfix branches, and use the 10.4 checklist as the review baseline | Skills predate the standards | Y |
| 2026-10-07 | Coding standards 18 gaps: Matt has a finished version from another app; it replaces the draft after a diff review | Pending file | Y |
| 2026-10-07 | /migration-audit removed; replaced by Matt's suitescript-migrator plugin (Matt installs the zip via the Code tab) | Matt's call | Y |
| 2026-10-07 | Coding standards: single source is the installed ethos-dev conventions file; standards/coding-standards.md points to it and lists workspace overrides | Avoids drift between copies | Y |
| 2026-10-07 | Commit format stays `type: summary` (overrides ethos-dev decision 12); branch names follow decision 12 | Matt's call | Y |
| 2026-10-07 | /scaffold removed; build work routes to /ethos-dev:start. /test-plan and /handoff kept only for work outside ethos-dev | Matt approved | Y |
| 2026-10-07 | /today rewritten: calendar, email needing attention, RAIDE and project plans in Ethos Clients (Matt's items plus overdue/blocked/Owner TBD on his projects), time-blocked plan, Matt picks first passes; plan saved to gitignored daily/YYYY-MM-DD.md. Manual trigger | Matt approved | Y |
| 2026-10-07 | CLAUDE.md rule: after every task, offer 2 or 3 things to take off Matt's plate from follow-ons and today's plan | Matt's request | Y |
| 2026-10-07 | Roster: ConcertAI and Hammitt added Active, Enovix Inactive | Matt's call | Y |
| 2026-10-07 | RAIDE field mapping: Escalation = Issue + URGENT + "Escalation:"; client-owned = Assigned To blank, Status In Progress - At Client, client owner first in Details; Owner TBD = blank + "Owner TBD." in Details. No schema changes | RAIDE template has no Escalation type and Assigned To is Ethos-only. Matt approved | Y |
| 2026-10-07 | RAIDE routing: project-specific RAIDE when the project has an active one (in project.md), else client MS RAIDE with Project picklist | Most clients have several RAIDEs. Matt approved | Y |
| 2026-10-07 | Live Dev Tracker is "Ethos Development Tracker" (8603558799691652); Row ID EBS.#### is the branch ticket | Matt's call | Y |
| 2026-10-07 | New personal sheet "Matt Garriga - Action Log" (RAIDE columns plus Source) created in Phase 5 with Matt's confirm; holds commitments, waiting-on, internal-only actions, management/team. Fed by /recap, /inbox, /today; old RAID Log archived by Matt | Old log stale; deletion is denied by design. Matt approved | Y |
| 2026-10-07 | Bootstrap covers all 13 active clients; senior discovers domains, Read AI folders, sheet IDs and repo paths for Matt to confirm in one table; agents draft in parallel read-only; Matt approves and commits per client, core clients first | Matt approved | Y |
| 2026-10-07 | Client repo CLAUDE.md written locally and excluded via .git/info/exclude, never committed | Matt approved | Y |
| 2026-10-07 | Phase 7: lint hook warns (does not block); add /health-check (connector IDs vs deny rules, fake-ID send test), secret scan in linter (blocks keys/tokens in outputs, drafts, context files), weekly scheduled /client-update sweep proposing diffs | Matt approved | Y |
