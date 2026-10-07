---
name: raide-sync
description: Update a client's Smartsheet RAIDE log from a meeting, email, or Matt's notes. Use for "update the RAIDE," "log this risk," or after recaps.
---
# RAIDE Sync
1. Sheet ID from `client.md`. Pull columns and current open rows (`get_sheet_summary`).
2. Extract Risks, Actions, Issues, Decisions, Escalations from the source. Match against existing rows to update instead of duplicating.
3. Preview table: Action (Add/Update) / Row / Column / Old / New. Omit unchanged columns.
4. Write only after Matt confirms. Then propose the context write-back.
