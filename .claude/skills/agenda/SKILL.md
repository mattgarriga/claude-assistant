---
name: agenda
description: Build a status meeting talk track for a client from RAIDE rows in Status Meeting status plus overdue, blocked, and new items. Use for "/agenda HUT," "prep for the status meeting," or inside /today prep blocks.
argument-hint: <client>
---
# Agenda
Read-only. Resolve the client via `clients/roster.md`; read `client.md` and each active `project.md` for RAIDE and plan sheet IDs and Read AI folder.

1. `scout` finds the last status meeting with this client (Read AI folder listings, most recent title or invite matching status) and returns its end time.
2. `scout` pulls from each project RAIDE (MS RAIDE for projects without one), with columns Project / Row / Type / Subject / Assigned To / Due / Status / Modified:
   - Status = "Status Meeting"
   - Overdue, or Status Blocked or On Hold
   - Rows added or modified since the last status meeting end time
3. Group by project. Within each: Status Meeting rows first (these are the agenda), then overdue, then blocked or on hold, then new or changed. Tag each row with why it is listed.
4. Output a talk track per project: 1 line per item (what to say or ask, owner, due), client-safe wording only; anything from `internal.md` stays out. Owner TBD stays TBD. Note budget burn in one line from the RAIDE hours columns when present.
5. Close with open questions for the client and a count of rows per reason. If no prior status meeting was found, say so and use the last 14 days as the window.
6. Offer to queue status changes (for example Status Meeting rows resolved in the meeting) through the `raide` skill: preview and confirm, nothing written here.
