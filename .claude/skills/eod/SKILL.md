---
name: eod
description: End-of-day close: mark today's plan items done, queue write-backs, propose Action Log rows, and set carryover for tomorrow. Use for "/eod", "wrap up my day", or "close out today".
argument-hint: [sent]
---
# End of Day

No agents. Reads local files only, unless the argument is `sent`.

1. Read `daily/YYYY-MM-DD.md` (today). Missing: say so and offer to build one from this session's work.
2. Ask in one multi-select which open items and first passes are finished. Update statuses (open / in progress / done) in the file.
3. Context digest: show today's `state/context-log.md` lines as a table (client / file / change / source) so Matt can spot errors after the fact; he reverts any he dislikes by saying which. Then show remaining `state/writeback-queue.md` ask-first items and ask which to apply (multi-select). Offer one commit of the day's `clients/` changes (`docs: context updates YYYY-MM-DD`) and commit on yes.
4. Action Log: propose rows for commitments Matt made and things he is waiting on, from this session, today's recaps, and anything he adds. With `sent`, one `scout` call checks today's sent mail and calendar for unlogged commitments. Preview per the `log` skill; write only on confirmation.
5. Write a `## Carry to tomorrow` section in today's file: unfinished items with source, ranked, plus any meeting prep tomorrow needs. `/today` reads the latest one.
6. Reply with a 3-line summary: done count, carried count, rows logged.
