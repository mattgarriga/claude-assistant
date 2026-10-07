---
name: raide
description: Update a client's Smartsheet RAIDE log from a meeting, email, or Matt's notes. Use for "update the RAIDE," "log this risk," or after recaps.
argument-hint: [client] [details]
---
# RAIDE Sync
0. Source is a meeting: have `meeting-analyst` extract it first and use its `raide_candidates`, `action_items`, and `internal_only` (never to a client-visible sheet). Email or notes: work directly.
1. Pick the sheet. If the item belongs to a project with its own active RAIDE (listed in that project's `project.md`), use it. Otherwise use the client's MS RAIDE from `client.md` and set the Project picklist. Every preview row shows the target sheet.
2. Pull columns and open rows (`get_columns`, `get_sheet_summary`). Only use existing picklist values; if a needed value is missing, say so instead of writing free text.
3. Map items to the RAIDE template:
   | Source item | Type | Assigned To | Status | Details starts with |
   |---|---|---|---|---|
   | Risk, Issue, Decision, Action, Enhancement | same | Ethos owner if stated | as stated, else Not Started | |
   | Escalation | Issue, Priority URGENT | Ethos owner if stated | as stated | "Escalation:" |
   | Client-owned action | Action | blank | In Progress - At Client | "[Client owner name]:" |
   | Owner unclear | as above | blank | Not Started | "Owner TBD." |
   Never assign an owner or due date that wasn't stated.
4. Match against existing open rows (subject and details, same project). Update a matching row instead of adding a duplicate.
5. Preview table: Sheet / Action (Add/Update) / Row / Column / Old / New. Omit unchanged columns.
6. Write only after Matt confirms. Then propose the context write-back.
