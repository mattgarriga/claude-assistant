---
name: prep
description: Prep notes for any meeting (not only status meetings): context, open items, last decisions, risks, and questions to ask. Use for "/prep <meeting>", "prep me for the 3:30", or "what do I need to know before the call".
argument-hint: <meeting title, client, or time>
---
# Prep

For Matt only, so `internal.md` may be used. Label the output "Internal, do not forward." For a client status meeting, run the `agenda` skill instead of duplicating it.

1. Identify the meeting: argument, or today's calendar (one `outlook_calendar_search`). Several matches: list and ask. Resolve client and project via the roster.
2. Read `client.md` (contacts, glossary), the relevant `project.md` open items and status, the last 2 `decisions.md` entries, and `internal.md`.
3. Open RAIDE rows: only if asked or the meeting is a status or design meeting. One `scout` call by sheet ID using the cached schema in `client.md`: Matt's items, overdue, Blocked, Owner TBD, for the project only.
4. Output, tight, tables first:
   - **Meeting:** time, attendees with role from `client.md` (unknown roles marked unknown)
   - **Where we are:** status and last decisions, with dates
   - **Open items:** Item / Owner / Status / Source
   - **Risks and watch-outs:** from `project.md` and `internal.md`
   - **Questions to ask:** each tied to an open item or gap
   - **Proposed outcomes:** labeled proposed, not stated goals
7. Never invent owners, dates, or figures. Gaps are listed as gaps.
