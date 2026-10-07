---
name: sdd-sync
description: Compare a meeting's outcomes to the project's SDD (open questions, requirements, scope, assumptions) and flag answers, conflicts, new requirements, and scope risk. Use for "/sdd-sync", "does this change the SDD", or after a design meeting.
argument-hint: <client> <project> [meeting or notes]
---
# SDD Sync

Read-only. Never edit the SDD. Output is proposals for Matt.

1. Resolve client and project. Find the SDD: `project.md` Artifacts row, else the OneDrive folder row in `client.md`, else ask for the path.
2. Extract the SDD as in the `ingest` skill, reading only: Open Questions, Scope (in and out), Functional Requirements, Assumptions, Dependencies, and the sign-off conditions.
3. Meeting outcomes: use the recap or `meeting-analyst` JSON already in this session, Matt's pasted notes, or a Read AI meeting ID he gives. Do not pull a new meeting unless told.
4. Compare and return one table: SDD ref / What the meeting said / Type / Proposed action.
   | Type | Meaning |
   |---|---|
   | Answers | Resolves an open question; propose the answer text and owner |
   | Conflicts | Contradicts a requirement, assumption, or earlier client answer |
   | New requirement | Implied by the meeting, not in the SDD |
   | Scope risk | Pushes into out-of-scope or changes effort |
   | Native check | A request that native NetSuite may already cover (apply native-first) |
5. End with a proposed change-log line (version, date, change reference), the list of questions that remain open with owners, and which items need a client decision versus an Ethos decision. Effort or pricing impact goes to Matt only, never into client text.
6. If Matt approves any item, route it to `/sdd` revision, `/co` for scope changes, and the write-back queue for context.
