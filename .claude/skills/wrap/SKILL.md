---
name: wrap
description: Friday wrap from the week's daily plans: done, slipped, next week priorities, a short update for Cedric and Cheyenne, and the write-back queue approval pass. Use for "/wrap," "Friday wrap," or "end of week."
argument-hint: [week of MM.DD.YYYY]
---
# Friday Wrap
1. Read `daily/YYYY-MM-DD.md` for the week (Monday to today). Missing days: say so, do not reconstruct.
2. Summarize in tables: **Done** (item, client, output), **Slipped** (item, why if recorded, new owner or date if stated), **Next week priorities** (ranked, from slipped items, open RAIDE and Action Log items, and upcoming client meetings; use `scout` for the forward calendar and open items).
3. Draft a short update for Cedric and Cheyenne in chat: 5 to 8 lines, what shipped, what is at risk, what is needed from them. Client-internal facts are fine here (internal audience) but no secrets or pricing guesses. Run `scripts/lint_voice.py`. Draft only; make an Outlook draft only if Matt asks (signature from `standards/tools.md`). Never send.
4. Write-back queue pass: show `state/writeback-queue.md` entries grouped by client, ask which to apply (multi-select), apply approved diffs through `client-context`, remove applied entries.
5. Reminder line: Time Machine is the only backup; confirm it ran this week.
