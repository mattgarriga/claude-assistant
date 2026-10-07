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
