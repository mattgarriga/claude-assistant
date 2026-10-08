---
name: invitra
description: Weekly Invitra digest from the Invitra Project Tracker and the Dev Tracker: aging, blocked, overdue, LOE waiting on approval, and open local branches for EBS tickets. Use for "/invitra," "what's with offshore," or the weekly Invitra check.
argument-hint: [client]
---
# Invitra Digest
Read-only. Invitra team: Deepak, Omkar, Supriya (`team/`). Sheet IDs and the cached Invitra Project Tracker schema are in `standards/tools.md`; read by ID and skip `get_columns`.

1. **Invitra Project Tracker (primary).** `scout` pulls rows where Status is not Closed, optionally filtered by Client (match aliases; the Client column is free text). Columns: ID (INV-####) / Project Name / Client / Status / NS Project / Case / Invitra LOE / Ethos PM / Invitra Assigned / Invitra Due Date / Client UAT Date / Client Go-Live Date / Date Created.
2. **Dev Tracker (secondary).** `scout` pulls Ethos Development Tracker rows not Closed where Assigned To is an Invitra member or Notes/Comments mention Invitra or those names. Columns: Ticket (EBS.####) / Client / Issue / Assigned To / Status / Due / Last modified.
3. **Flags.** Compute age (days since modified, or since created if unmodified) and flag:
   - Invitra Due Date, Client UAT Date, or Client Go-Live Date in the past with Status not Closed
   - LOE Requested or LOE Pending Approval for more than 7 days
   - In Progress with no Invitra Assigned
   - Blocked or On Hold (Dev Tracker), or no update in 7 days
   - Missing Invitra LOE on anything past Backlog
4. **Local branches.** For each client repo in `../Repos/*`, list branches matching `EBS-` with read-only git (`git branch`, `git log -1`, `git status`). Match to Dev Tracker ticket numbers. Flag tickets in development with no branch, and branches whose ticket is Closed. Invitra Project Tracker rows have no EBS number; do not guess a match.
5. **Output.** One table per tracker: ID or Ticket / Client / Status / Invitra Assigned / Age / Next date / Flag. Then 3 suggested actions (for example a nudge draft to Deepak, a handoff brief, a status question), each with the row. Offer to draft but never send.
