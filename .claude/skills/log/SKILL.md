---
name: log
description: Quick-capture a commitment, waiting-on item, or internal action into Matt's Action Log in Smartsheet. Use for "/log", "log this", "add to my action log", "I owe X".
argument-hint: <one line: what, who owes it, due date>
---
# Log

Fast capture. No agents, no research, no reads beyond the sheet. Action Log sheet ID is in `standards/tools.md` (AL.####).

1. Parse $ARGUMENTS into: Task, Owner, Due, Type (Commitment / Waiting-on / Internal), Client (resolve via `clients/roster.md`; blank if none). Several items in one message are fine.
2. Owner defaults to Matt only when the text says "I" or "I owe". Otherwise use the named person. If unclear, write "Owner TBD". Never invent an owner or a due date; leave Due blank if not stated.
3. First write of a session: one `get_columns` call on the sheet to map column names. Reuse the mapping after that.
4. Show a one-table preview (sheet, new row, column, value) and ask for a yes in one line. Smartsheet writes always need explicit confirmation.
5. On yes, `add_rows` once for all items. Reply with the row IDs, nothing else.

Dates as MM.DD.YYYY in text, ISO where the column requires it.
