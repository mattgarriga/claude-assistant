---
name: tasks
description: Push recap action items to Smartsheet task sheets or the Ethos Development Tracker. Use after a recap or when Matt says "add these to Smartsheet."
argument-hint: [client] [details]
---
# Action Items Sync
Source is a meeting: have `meeting-analyst` extract the action items first (its `action_items` field); otherwise work from the recap or notes given.
Owner TBD items stay TBD; never assign. Map each item to sheet, columns, owner, due date. Preview (Sheet / Row / Column / Old / New), confirm, write. Development work routes to the Ethos Development Tracker only if Matt says it's a dev ticket.
