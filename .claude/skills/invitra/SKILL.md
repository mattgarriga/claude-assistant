---
name: invitra
description: Weekly Invitra digest: Dev Tracker rows assigned to or noting Invitra, aging, blocked, and open local branches for EBS tickets. Use for "/invitra," "what's with offshore," or the weekly Invitra check.
argument-hint: [client]
---
# Invitra Digest
Read-only. Invitra team: Deepak, Omkar, Supriya (`team/`).

1. `scout` pulls Ethos Development Tracker rows (ID in `standards/tools.md`) not Closed where Assigned To is an Invitra member or Notes/Comments mention Invitra or those names, optionally filtered by client. Columns: Ticket (EBS.####) / Client / Issue / Assigned To / Status / Due / Last modified.
2. Compute age (days since modified or since created if unmodified), and flag Blocked or On Hold, overdue, and no update in 7 days.
3. Local branches: for each client repo in `../Repos/*`, list branches matching `EBS-` with read-only git (`git branch`, `git log -1`, `git status`). Match to ticket numbers. Flag tickets in development with no branch, and branches whose ticket is Closed.
4. Output: table Ticket / Client / Assigned / Status / Age / Branch / Flag. Then 3 suggested actions (for example a nudge draft to Deepak, a handoff brief, a status question), each with the ticket. Offer to draft but never send.
