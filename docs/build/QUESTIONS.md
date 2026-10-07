# Questions for Matt (grouped)

Answer in chat in any order. Items marked FYI need no answer unless you disagree.

## A. Quick actions (you)
1. Run the managed-settings `sudo` command (API key hard block), then restart the app.
2. Install the migrator plugin: Code tab, +, Plugins, Add plugin, pick `suitescript-migrator-v0.2.0.zip`.
3. HUT's PrintNode API key is in plain text in the Mobile Packing Slip One-Pager on OneDrive. Remove it and ask HUT to rotate it.

## B. Render approvals
4. Phase 1 cleaned templates: `docs/build/renders/phase1/clean-template-sdd/` (now Letter) and `clean-template-dev-request-one-pager/` (white value cells). Approve?
5. Phase 2 outputs vs templates, all 6 types: `docs/build/renders/phase2/<type>/{template,output}/`. Renders use LibreOffice look-alike fonts; the byte-identity check passed on every type. Open one real output in Word too: `lib/docx/out/`. Approve, or list fixes. Tester's visual notes (LibreOffice pagination, Word may differ): One-Pager OPEN QUESTIONS heading can strand at the bottom of page 1; SDD FR-01 table splits across pages 3 and 4; SDD page 1 has white space before the TOC (same as the template); T&M fee table placeholder wraps (see item 6). Want keep-with-next added to headings and no-split on short tables? That is formatting the engine would add beyond the template.

## C. Document engine calls
6. T&M fee table: `PRICING-PROVIDE-BEFORE-SENDING` wraps to 2 to 4 lines in the narrow Total column. Keep it (ugly, unmissable), or use `TBD` inside that table only with the full placeholder in the paragraph above it?
7. SOW/CO Out of Scope: added as the last numbered scope item "Out of Scope:" with sub-bullets. OK, or a separate heading?
8. SDD Lucid edit link: placed as a line after the Document Control table. OK, or a column in that table?
9. FYI: diagram titles get bold and keep-with-next so a title never strands on the previous page.
10. FYI: SDD 4.4 with no parameters omits the parameter label and table.
11. FYI: One-Pager bullets use the exact definition from your Workbook Export example (filled round bullet, hollow round for level 2).
12. FYI: SOW/CO level-3 bullet indent looks wide; it is the template's own numbering.

## D. Standards sign-off
13. `docs/build/phase1-standards-diff.md`: 20 rows marked NEEDS MATT, summarized at the top. Approve all, or call out rows to change.

## E. Phase 3a tests (run with you, since you judge quality)
14. Client recap test: OK to use the most recent HUT client-facing status meeting? (I confirm the title with you before running.)
15. Email test: name a real thread (sender or subject) to reply to. The draft lands in Outlook Drafts, never sent.

## F. Action Log (Phase 5)
16. Columns for the new "Matt Garriga - Action Log": Row ID, Type (Commitment / Waiting On / Internal Action / Management), Subject, Client (optional), Date Identified, Due Date, Assigned To, Priority, Status, Done, Details, Source (link), Comments. Approve and I create it.

## G. Bootstrap discovery (`docs/build/phase6-discovery.md`)
17. Which project RAIDEs and plans are still active? Several look closed (HUT Phase One/Two, ALTO Go-Live, CommSell Phase Zero, CORE Phase Zero, Cala Future State, old Boxes 4 U MEC months).
18. EVgo has no RAIDE in Smartsheet. Is there one elsewhere, or none?
19. Email domains for CommSell, Boxes 4 U, EVgo, LSN, ConcertAI, Hammitt (none showed in 90 days of meetings).
20. Dev Tracker picklist typos "Core Transfomers" and "Hammit": fix them in Smartsheet? (Skills work either way.)
21. When should the overnight bootstrap run (date and rough time)?

## H. Scheduling and models
22. Weekly /client-update sweep: day and time? (Creates a scheduled task; proposals only, never writes.)
23. Scout (Haiku) mistyped one sheet ID and missed two plans during discovery; I caught them by cross-checking. Keep scout on Haiku with my verification step, or move it to Sonnet (more reliable, more usage)?
