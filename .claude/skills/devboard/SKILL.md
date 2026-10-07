---
name: devboard
description: Triage the Ethos Development Tracker in Smartsheet: unassigned, blocked, aging, missing one-pagers, mismatched status. Use for dev board review or assignment planning.
argument-hint: [client] [details]
---
# Dev Tracker Triage
Sheet: Ethos Development Tracker (ID in `standards/tools.md`). Row IDs are EBS.####, the same ticket number used in branch names (`feature/EBS-####`).

Flag, in this order:
1. Status Submitted or Backlog with no Assigned To.
2. On Hold, or Due Date passed and not Closed.
3. Not modified in 14 days and not Closed.
4. Documentation Needed checked with no Supporting Documentation link (missing one-pager or SDD).
5. Status that contradicts other columns (Closed but Done unchecked, In Development with no assignee).

Table: Ticket / Client / Issue / Suggested action / Suggested owner (team roster; Invitra for execution work). Suggestions only. Any status or assignment change goes through preview (Row / Column / Old / New) and confirm.
