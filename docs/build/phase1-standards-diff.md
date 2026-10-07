# Phase 1.6 Standards Diff

Source: `standards/_source/*.docx` (the original claude.ai Project files; they are plain markdown text despite the extension). Now: current `standards/*.md`, `CLAUDE.md`, `clients/roster.md`, `team/roster.md`. Compared 2026-10-07. Material differences only (behavior, structure, rules, values). Pure wording changes are skipped.

Status key: **Approved <date>** means a row in `docs/build/decisions-log.md` covers it. **Approved (standing rule)** means Matt's global or repo CLAUDE.md rule covers it, no log row. **NEEDS MATT** means no decision on record; confirm or reverse.

## Summary: NEEDS MATT (22)

| # | File | Item | Source said | Now says | Suggested call |
|---|---|---|---|---|---|
| 1 | voice | "Let me know if you have questions" | Listed under avoid, then called "works fine" (self-contradiction) | Banned | Keep banned (matches your global rule) |

| 3 | recap | First section | "Topics Covered", never "Decisions Made" (but the body structure itself shows Decisions Made) | First section after budget is Decisions Made | Keep |
| 4 | recap | Budget table rows | Fixed rows: Ad-Hoc Support, Project 1, Project 2 | Only rows with real numbers; one line if a project had none | Keep |
| 5 | recap | Group by workstream | Not stated | Group Decisions and Action Items by workstream when several | Keep |
| 6 | recap | Internal variant | "Same format", addressed to the user | Greeting "Team,", no budget table unless relevant, named owners in bullets | Keep |
| 7 | sdd | Resolved questions | Not stated | Resolved interview questions never reintroduced as open items | Keep |
| 8 | sow | T&M per-role pricing and not-to-exceed | T&M priced per role per hour with an NTE | Native template phase table (Design to Estimated Fees); no per-role rows, no NTE | Confirm NTE is intentionally gone |
| 9 | sow | $200 discounted rate | Standard $225, discounted $200 available | $225 in template wording; $200 only if you say so | Keep |
| 10 | one-pager | Request Type value | "Reporting and Data" | "Reporting/Data" | Confirm which string Smartsheet intake uses |
| 11 | one-pager | Requested By | Full name and role/company | Format file: full name only; skill still asks role/company | Pick one |
| 12 | one-pager | Open Questions with none | Not stated | One row "N/A" | Keep |
| 13 | lucid | Lane shading | All lanes shaded Lunar; none left white | Title bar Lunar, body white (real swimlane behavior) | Confirm acceptable |
| 14 | lucid | Lane type | Not stated | True AdvancedSwimLaneBlock containers only | Keep |
| 15 | lucid | Lane order | Not stated | Strict causal adjacency; no connector skips a lane | Keep |
| 16 | lucid | Terminator | Every flow ends in a terminator "End Process" | Exactly one; every branch and early exit routes into it | Keep |
| 17 | lucid | Label placement | Not stated | Labels live in the shape's own text field; no floating text boxes | Keep |
| 18 | lucid | Pre-export verification | Not stated | Mandatory re-fetch and checklist before export | Keep |
| 19 | branding | Fallback styling and callouts | Default style set for doc types without a template; Note and Warning callouts; page numbers over 3 pages | None. Only template specs. Callouts forbidden | Decide a fallback for TDD, training doc, etc. |
| 20 | tools/PI | Per-task override | A direct user instruction overrides defaults for that one task (emoji example); trust user over a knowledge file | Not carried over; CLAUDE.md says no emojis anywhere | Keep dropped, or restore |

| 22 | team | Additions | 13 people, no Gabe, no Invitra, no relationship notes | Gabe (role TBD), Invitra contacts, Tommy "brother, direct report", Grayson "direct report", Gage "Joined full time Q2" | Confirm each |

## 1. Communication_Voice_Guide to standards/voice.md

| Item | Source said | Now says | Why | Status |
|---|---|---|---|---|
| Principles | 5 principles incl. "Action-oriented" | Same set minus "Action-oriented" as a label; folded into "end with a next step"; adds "Should not read as AI-written" | Matt's global instruction | Approved (standing rule) |
| Open with point, specifics, active voice, acknowledge issues, end with ask | Present | Present | Carried over | Approved (carried over) |
| Hedge and filler list | 7 items (just, stacked hedges, sorry to bother, hope you're well, as discussed, don't hesitate, thanks in advance) | All 7 present, plus "As mentioned", "I hope this helps", "It's worth noting", "Thank you for reaching out", "I trust this email finds you well" | Merged from Project_Instructions and Matt's global list | Approved (standing rule) |
| "Let me know if you have questions" | Contradictory (avoid list, then "works fine") | Banned | Matt's global list bans it | NEEDS MATT (#1) |
| Em dashes | Used in examples and rules | Banned everywhere; examples rewritten | Matt's global rule | Approved (standing rule) |
| Hyphens and semicolons sparingly | Not stated | Added | Matt's global rule | Approved (standing rule) |
| Email length | In Project_Instructions: 2 to 5 sentences, three paragraphs too many | In voice.md hard rules | Moved | Approved (carried over) |
| Matt's outbound tone | Not stated | Leader voice, direct but fair, warmth matched to relationship | team/matt.md and global instruction | Approved (standing rule) |
| Banned words in SDDs | In SDD_Format | Moved to voice.md | Single home | Approved (carried over) |
| Signature | See Project_Instructions section 5 | voice.md points to tools.md | Consolidated | Approved 2026-10-06 (tools.md note) |
| Lint | Not stated | `scripts/lint_voice.py` on every draft | Workspace build | Approved 2026-10-07 (Phase 7 lint hook) |

## 2. Meeting_Recap_Format to standards/recap-format.md

| Item | Source said | Now says | Why | Status |
|---|---|---|---|---|
| Subject line | `[Client] (em dash) Meeting Recap, [Topic], [Date]` | Hyphen instead of em dash; date MM.DD.YYYY | No-dash rule; date | Dash: Approved (standing rule). Date: Approved 2026-10-06 |
| Opening paragraph | Longer, ends with "don't hesitate to reach out" | Shorter, no banned phrase | Voice rules | Approved (standing rule) |
| Budget line | "As of EOD [Last Business Date DD.MM.YYYY)" | "As of EOD [MM.DD.YYYY], last business day" | Fix of malformed source | Approved 2026-10-06 |
| Budget rows | Fixed three rows | Only rows with real numbers; note if none; never invent | Never invent | NEEDS MATT (#4) |
| First section | Rule says "Topics Covered" never "Decisions Made"; template shows Decisions Made | Decisions Made, actual decisions only, past tense | Resolves the source conflict | NEEDS MATT (#3) |
| Workstream grouping | Not stated | Group by workstream | New | NEEDS MATT (#5) |
| Action items | Action text only, owner is the party heading, "Owner TBD" | Same | Carried over | Approved (carried over) |
| Risks | Em dash separator; omit if none | Colon separator; omit if none | No-dash rule | Approved (standing rule) |
| No Next Steps section | Present | Present | Carried over | Approved (carried over) |
| No internal commentary | General | Lists budget internals, staffing, resourcing, politics, escalations | CLAUDE.md internal.md rule | Approved (standing rule) |
| Internal variant | Same format, addressed to the user | Own section: "Team,", no budget table unless relevant, named owners | New detail | NEEDS MATT (#6); internal recap itself Approved 2026-10-07 (3a scope) |
| Outlook draft | M365 connector, attendees from calendar, do not send | Attendees from the invite (not Read AI list); signature block; only when asked | Tools rules | Approved 2026-10-06 (connector decisions) |
| Output | Plain text in chat; .docx only when requested | Text or Outlook draft only; recap .docx removed | Scope cut | Approved 2026-10-07 (recap .docx dropped) |
| RAIDE and project-log proposals after a recap | Not stated | In the recap skill (step 8), not this file | Workflow | Approved 2026-10-07 |

## 3. SDD_Format to standards/sdd-format.md

| Item | Source said | Now says | Why | Status |
|---|---|---|---|---|
| Design interview, gating, alternatives, challenge list, draft gate, push back | Full text in format file | Moved to `.claude/skills/sdd/SKILL.md` (all items present, plus native-first and simplicity passes); sdd-format.md ends with a pointer | Format file is output spec only | Approved 2026-10-07 (skill text updated in Phase 1 task 1.4) |
| Template | "Read template-sdd.docx in project knowledge" | Fill `templates/template-sdd.docx` through lib/docx | Document engine | Approved 2026-10-07 |
| Section list | 8 numbered items, numbering skips 7, Overview first | Header table, Overview, TOC, sections 1 to 7 per template (quirks kept) | Templates win | Approved 2026-10-07 |
| Overview box | Summary plus Assumptions | Problem / Solution / Business Impact, 1-2 sentences each, then Assumptions | Template | Approved 2026-10-07 |
| 2.3 Assumptions | Separate subsection | Removed; assumptions only in Overview | Template has none | Approved 2026-10-07 (templates win) |
| FR table | Two columns "# / Requirement", FR-01 | "ID / Requirement", FR-01.1 rows, heading per group; still two columns, never Notes or Status | Template | Approved 2026-10-07 |
| Script outline section | 4.5; "leave 4.5 out" for unjustified scripts | 4.4 | Template numbering; 4.4 decisions | Approved 2026-10-07 |
| Script block | Filename, Script ID, Script Type, params as bullets with custscript ID | Heading, Filename, Folder, Script Type, Script ID, params table Name / Type / Value, outline | 3D Flight SDD | Approved 2026-10-07 |
| Script heading pipes | Use dash | "EBS - [Name]", template pipe replaced | Same rule | Approved 2026-10-07 |
| 4.1 Process Flow | Build in Lucid, export PNG, embed | Same, plus INCLUDEPICTURE link removed, edit link in Document Control | Flow decision | Approved 2026-10-07 |
| 4.2, 4.3, 5.x, 6 table columns | Not specified | Component / Type / Purpose; System / Relationship / Notes; Field Label / Field ID / Type / Purpose; sign-off Name / Organization / Role / Date / Decision | Template | Approved 2026-10-07 |
| Data tables | Navy header, white body, no alternating fills | In branding.md as template spec | Branding rewrite | Approved 2026-10-07 |
| TOC | Not stated | Rewritten from real headings, update-on-open flag | New | Approved 2026-10-07 |
| Matt in approvals | Always include as Technical Lead | Same | Carried over | Approved (carried over) |
| Writing rules (no code, shortest doc, no restating, bullets for states, one sentence justification, testable assumptions, "Not applicable", banned words) | Present | Present; "Not applicable" adds "tables trimmed to content row count" | Carried over; trim rule | Approved 2026-10-07 |
| Resolved questions | Not stated | Never reintroduced as open items | New | NEEDS MATT (#7) |
| Filing | `[CLIENT]-[Feature] SDD v1.docx` | Same name, inside `clients/<slug>/projects/<project>/outputs/` | Repo-only outputs | Approved (standing rule) |
| Emojis, filler | Listed in rules | In voice.md and CLAUDE.md | Single home | Approved (standing rule) |

## 4. SOW_Format to standards/sow-format.md

| Item | Source said | Now says | Why | Status |
|---|---|---|---|---|
| Types | FF or T&M; ask if ambiguous | Four templates (SOW and CO, each FF and T&M); ask if ambiguous | CO added; templates | Approved 2026-10-07 |
| Overview | "Basic Business Needs Overview", 2 to 4 sentences | Problem / Solution / Business Impact, 1-2 sentences each | 2026 layout | Approved 2026-10-07 |
| Assumptions | Own section, each "Client will..." | 5 standard assumptions on by default, editable; client-specific ones added after, "Client will..." | Standard assumptions | Approved 2026-10-07 |
| Process Overview | Build in Lucid, export, embed | Titled Lucid diagrams only, 6.9in, no narrative | Decision | Approved 2026-10-07 |
| Scope and Deliverables | Hierarchical bullets, "Type: description" leaves | Same, nested to 3 levels, plus standard bullets (Project Management ... Cutover and Support) | Template | Approved 2026-10-07 (2026 layout) |
| Fees (FF) | Per-phase or per-deliverable pricing | Fixed fee paragraph, 50% at execution, balance at UAT start, net 15 | Template | Approved 2026-10-07 (placeholders and layout) |
| Fees (T&M) | Per role per hour, estimated hours, not-to-exceed | Native Estimated Hours and Fees phase table, Project Oversight 20%, invoicing paragraph | Template | Table: Approved 2026-10-07. NTE and per-role dropped: NEEDS MATT (#8) |
| Rates | $225 standard, $200 discounted | $225 in template; $200 only if Matt says | Never invent | NEEDS MATT (#9) |
| Pricing | Placeholder unless user provides | Every dollar and T&M hour figure is the placeholder until provided | Never invent pricing | Approved 2026-10-07 |
| Signature | Client signer / Cedric Carter | Same; client signer from client.md; acceptance date blank | Decision | Approved 2026-10-07 |
| Out of Scope | Fold into Scope and Deliverables | Same | Carried over | Approved (carried over) |
| Cheyenne LOE sign-off | Note in handoff | Same wording | Carried over | Approved (carried over) |
| Cutover support | Not stated | 5 business days FF, 2 weeks T&M | Templates | Approved 2026-10-07 |
| Document Control and address header | Not stated | None in 2026 layout | Decision | Approved 2026-10-07 |
| Filing | `[CLIENT]-SOW-[topic-slug]-[date].docx` | Same in outputs/, CO uses `-CO-`, drafts `-draft.docx` uncommitted | Repo structure | Approved 2026-10-07 (gitignore drafts) |

## 5. Development_Request_One-Pager_Format to standards/one-pager-format.md

| Item | Source said | Now says | Why | Status |
|---|---|---|---|---|
| Questions before drafting | 9 questions, batch, do not re-ask | Moved to the onepager skill (step 2); same set, one batch, focused follow-ups | Skill text updated | Approved 2026-10-07 |
| Sections | Header, Context, Current, Desired, Details, In Scope, Out of Scope, OQ | Template order: Overview table, Business Context, Current vs Desired table, Details, Scope and Client Guardrails (adds Constraints), OQ, footer line | Template | Approved 2026-10-07 |
| Requested By | Full name and role/company | Format file says full name; skill asks role/company | Inconsistent | NEEDS MATT (#11) |
| Request Type | Bug Fix, Config Change, Reporting and Data, Minor Enhancement | "Reporting/Data" | Template or typo? | NEEDS MATT (#10) |
| OQ table | OQ-## / Question / Owner / Status | OQ-01 format; owner required; Status starts Open; none means one "N/A" row | CLAUDE.md owner rule; N/A new | Owner: Approved (standing rule). N/A row: NEEDS MATT (#12) |
| Helper lines, bullets, value-cell fill | Not stated | Helper lines removed, real bullets, footer kept | Decisions | Approved 2026-10-07 |
| Never fill gaps | Present | Present | Carried over | Approved (carried over) |
| Filing | `one-pager-[topic]-[date].docx` | Same in outputs/; ad-hoc under `projects/ad-hoc-support/` | Repo structure | Approved (standing rule) |

## 6. Ethos_Branding_Standards to standards/branding.md

| Item | Source said | Now says | Why | Status |
|---|---|---|---|---|
| Nature of file | General rules plus default style | Per-template spec extracted from template XML; templates win | Conflicts found | Approved 2026-10-07 |
| Template list | Includes template-meeting-recap.docx | Recap template removed; CO templates added | Scope | Approved 2026-10-07 |
| Auto-follow template updates | "No instruction updates needed" | Re-sync copies on request; branding.md is the extracted record | Decision | Approved 2026-10-07 |
| Logo | Top-left first-page header, 130x91 px | Per template (inline in header, sizes in EMU per template) | Templates win | Approved 2026-10-07 |
| Paper and margins | Letter, 1in | Per template; SDD A4 changed to Letter, One-Pager 0.75in side margins | Decision | Approved 2026-10-07 |
| Body, heading, table fonts | Calibri or Arial, 11pt body, 10pt tables, navy headings | Per template (One-Pager Arial 10pt, filled text Calibri 262626; SDD body 11pt, tables 10pt) | Decisions | Approved 2026-10-07 |
| Spacing | 0 before, 0 after unless template says | Per template | Templates win | Approved 2026-10-07 |
| Table rules | White data rows, no shading, thin gray borders | Template fills kept (label cells F2F2F2, status EBF5FB); value cells made uniform white | Template | Approved 2026-10-07 |
| Default styling for docs without a template; callouts; page numbers over 3 pages; title as top heading | Defined | Removed; callouts forbidden | Not covered by a decision | NEEDS MATT (#19) |
| No emojis, no clip art, no dividers | Present | Present | Carried over | Approved (carried over) |
| Render check | Not in source (in tools.md) | Verify section: PDF render, compare to template render | Quality gate | Approved (standing rule) |

## 7. Lucid_Diagram_Standards to standards/lucid-standards.md

| Item | Source said | Now says | Why | Status |
|---|---|---|---|---|
| Scope | SDD 4.1, SOW/CO, standalone; not one-pagers | Same | Carried over | Approved (carried over) |
| Lane count, naming, sizing, 40pt margin, 60pt spacing, left to right | Present | Present | Carried over | Approved (carried over) |
| Lane shading | All lanes Lunar, none white | Title bar Lunar, body white | Real swimlane behavior | NEEDS MATT (#13) |
| Lane type | Not stated | AdvancedSwimLaneBlock only | Build experience | NEEDS MATT (#14) |
| Lane order | Not stated | Strict adjacency | New | NEEDS MATT (#15) |
| Terminator | One per flow ending "End Process" | Exactly one, all branches route in | Tightened | NEEDS MATT (#16) |
| Shapes table sizes and styles | Present | Present (border #3A414A) | Carried over | Approved (carried over) |
| Palette | Table of 4 colors incl. lane border | Inline values; lane border color not restated | Reorganized | Approved (carried over) |
| Typography | Lane 10pt, shape 8pt (7 if needed), branch 8pt bold | Same | Carried over | Approved (carried over) |
| Connectors | Elbow, 12pt, arrow at target, #3A414A, branches Yes/No or equivalent | Same; Yes/No bold 8pt #333333 attached to connector | Carried over | Approved (carried over) |
| Label placement | Not stated | In shape text field only | New | NEEDS MATT (#17) |
| Pre-export verification | Not stated | Mandatory checklist | New | NEEDS MATT (#18) |
| Filing | Folder, title, page titles, separate current and proposed pages | Same | Carried over | Approved (carried over) |
| Export and edit link | PNG, embed, link in Document Control, file in Lucid | Same | Carried over | Approved 2026-10-07 |
| Test | Not stated | /flow test goes to a "Claude Test" folder | Test plan | Approved 2026-10-07 |

## 8. Project_Instructions to standards/tools.md and CLAUDE.md

| Item | Source said | Now says | Why | Status |
|---|---|---|---|---|
| Audience | Shared assistant for a team of 13 | Matt's personal assistant | Decision | Approved 2026-10-07 (personal only) |
| Question behavior | Ask only what you need, batch, no onboarding | Ask when underspecified, even small gaps; AskUserQuestion, batched | Matt's global instruction | Approved (standing rule) |
| SDD exception | Interview before any output | Same, in sdd skill | Carried over | Approved (carried over) |
| Capability list | 6 outputs; out-of-list gets help and a format note | Full command table; out-of-list line kept | Workspace build | Approved 2026-10-07 |
| No emojis, no filler, tone | Present | CLAUDE.md and voice.md | Carried over | Approved (carried over) |
| Owner TBD, no internal commentary | Present | CLAUDE.md, with internal.md rule | Carried over | Approved (carried over) |
| M365 connector | Read mail and calendar, create drafts and calendar events | Read and draft only; calendar writes and chat creation denied | Draft-only rule | Approved 2026-10-06 |
| Find email by description, list on multiple matches, say if none | Present | tools.md | Carried over | Approved (carried over) |
| Batch inbox | Present | tools.md and inbox skill | Carried over | Approved (carried over) |
| Drafts | HTML p tags; 2 to 5 sentences; flag unknown recipients; "never include a signature block, Outlook adds it" | HTML kept; hard-coded signature block (API drafts carry no Outlook signature) | tools.md says Matt confirmed 2026-10-06 | Approved 2026-10-06 (tools.md note, not in log) |
| Recap behavior | Identify client, use calendar, draft to attendees, flag owners | recap-format.md, tools.md, recap skill | Carried over | Approved (carried over) |
| Document behavior | Read format, read template, branded .docx, tight postamble, SOW pricing and LOE | Format files, lib/docx, CLAUDE.md, verification checklist | Carried over | Approved 2026-10-07 |
| Branded output and logo | docx matches template, logo top-left | branding.md and lib/docx | Carried over | Approved 2026-10-07 |
| When unsure | Stop and ask | CLAUDE.md | Carried over | Approved (standing rule) |
| Per-task override and trust user over knowledge file | Present | Not carried over | Conflicts with non-negotiable no-emoji rule | NEEDS MATT (#20) |
| Trusted sources | Knowledge files, templates, M365 | standards/, templates/, connectors; tools.md adds Read AI, Smartsheet, Lucid, NetSuite sections | Connector setup | Approved 2026-10-06 |
| Added rules not in source | None | Context write-back, never post to Teams, Smartsheet preview and confirm, git rules, 2 to 3 offers after each task | Workspace build | Approved 2026-10-07 |

## 9. Client_Roster to clients/roster.md

| Item | Source said | Now says | Why | Status |
|---|---|---|---|---|
| Header | "11 currently active", list of 32 | Status column; 13 Active, rest Inactive | Source count was wrong | Approved 2026-10-06 (statuses confirmed) |
| Added clients | Not listed | Boxes 4 U (B4U), Cerio, EVgo, ConcertAI, Hammitt (Active), Enovix (Inactive) | Seeded from history | ConcertAI, Hammitt, Enovix: Approved 2026-10-07. Boxes 4 U, EVgo, Cerio: Approved 2026-10-06 (roster note) |
| CommSel | Spelled CommSel | CommSell, alias CommSel and PlugUp | Spelling and alias | Approved 2026-10-06 |
| Aliases | Inline in parentheses | Aliases column, adds 4P, Core, CORE | Structure | Approved (carried over) |
| Core, Slug columns | Not present | Added | Bootstrap and folders | Approved 2026-10-07 |
| Contacts not kept in roster | Ask the user | Contacts live in client.md | Per-client context | Approved 2026-10-07 |
| Unknown name rule | Ask new engagement or variant | CLAUDE.md "Before any task" step 1 | Carried over | Approved (carried over) |
| Sensitive data stays in chat | Present | internal.md rule in CLAUDE.md | Carried over | Approved (standing rule) |

## 10. Ethos_Team_Roster to team/roster.md

| Item | Source said | Now says | Why | Status |
|---|---|---|---|---|
| People and roles | 14 listed in 3 groups | Same roles, flat table | Structure | Approved (carried over) |
| Email format, roles overlap | Present | Present | Carried over | Approved (carried over) |
| Notes column | None | Cedric SOW signer; Cheyenne signs off on LOE; Matt SDD Technical Lead; Gage "Joined full time Q2"; Tommy "Matt's brother, direct report"; Grayson "Direct report" | From team/matt.md | NEEDS MATT (#22) |
| Name forms | Thomas Garriga | Thomas (Tommy) Garriga; Matthew (Matt) Garriga | Aliases | NEEDS MATT (#22) |
| Gabe | Not listed | "(confirm role)", intern pipeline hire | Added | NEEDS MATT (#22) |
| Invitra offshore partner | Not listed | Deepak Tilloo, Omkar, Supriya | Offshore oversight is in scope | NEEDS MATT (#22) |
