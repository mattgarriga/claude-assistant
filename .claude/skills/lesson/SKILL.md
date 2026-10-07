---
name: lesson
description: Quick-capture a reusable NetSuite pattern, gotcha, or mistake into knowledge/. Use for "/lesson", "remember this pattern", or after solving something reusable.
argument-hint: <one or two lines: what happened or what works>
---
# Lesson

No agents, no research. Applies immediately; no approval needed (logged for review in `/eod`).

1. Read `knowledge/README.md` and grep `knowledge/` for the topic. If a matching entry exists, add the new detail to it instead of creating a duplicate; if it contradicts the entry, show both and ask.
2. Write the entry in this shape, in the matching topic file (or a new `knowledge/<topic>.md`):
   - **Problem** (one line)
   - **Pattern** (what works, with the key detail)
   - **Where used** (client and project links, no confidential specifics)
   - **Caveats** (one line, or omit)
   - Source tag: `[src: Matt <MM.DD.YYYY>]`, or the meeting or ticket it came from.
3. Facts only. No credentials, keys, or client-confidential data.
4. Append one line to `state/context-log.md`: date | knowledge/<file> | add or edit | old | new | source.
5. Reply in one line: what was added and where.
