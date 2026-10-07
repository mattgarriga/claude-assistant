---
name: raide
description: Update a client's Smartsheet RAIDE log from a meeting, email, or Matt's notes. Use for "update the RAIDE," "log this risk," or after recaps.
argument-hint: [client] [details]
---
# RAIDE Sync
0. Source is a meeting: have `meeting-analyst` extract it first and use its `raide_candidates`, `action_items`, and `internal_only` (never to a client-visible sheet). Email or notes: work directly.
1. Pick the sheet. If the item belongs to a project with its own active RAIDE (listed in that project's `project.md`), use it. Otherwise use the client's MS RAIDE from `client.md` and set the Project picklist. Every preview row shows the target sheet.
2. Use the cached schema in `client.md` (Sheet schemas). Call `get_columns` only when the sheet has no cached entry, or a write fails; after a fresh read, record the schema in `client.md`. Pull open rows with `get_sheet_summary` or a filtered find. Only use existing picklist values; if a needed value is missing, say so instead of writing free text.
3. Map items to the RAIDE template:
   | Source item | Type | Assigned To | Status | Details starts with |
   |---|---|---|---|---|
   | Risk, Issue, Decision, Action, Enhancement | same | Ethos owner if stated | as stated, else Not Started | |
   | Escalation | Issue, Priority URGENT | Ethos owner if stated | as stated | "Escalation:" |
   | Client-owned action | Action | blank | In Progress - At Client | "[Client owner name]:" |
   | Owner unclear | as above | blank | Not Started | "Owner TBD." |
   Never assign an owner or due date that wasn't stated.
**Keep it concise.** Propose the fewest rows that capture the meeting, normally 1 to 3, never one row per sub-step.
- Merge actions that share an owner and workstream into one row; put the steps in Details.
- One row per real outcome: a decision, a risk, an issue, or a distinct owned deliverable.
- Fold dependencies into the action that needs them ("Complete routing-definition file", not a separate Dependency row). Skip assumptions, events, and target dates unless Matt asks, or the item blocks a deadline.
- Do not add a row for a follow-up that an existing row already covers; update that row's Details instead.
- If more than 3 rows seem needed, show the 3 most important and list the rest in one line for Matt to pick from.
4. Match against existing open rows (subject and details, same project). Update a matching row instead of adding a duplicate.
5. Preview table: Sheet / Action (Add/Update) / Row / Column / Old / New. Omit unchanged columns.
6. Write only after Matt confirms. Then propose the context write-back.
