---
name: today
description: Matt's daily plan. Pulls today's calendar, emails and Teams asks needing his attention, and RAIDE and project plan items from the Ethos Clients Smartsheet workspace, builds a time-blocked day, saves it, and offers first passes. Use for "today," "morning brief," "plan my day," or "what's on my plate."
argument-hint: [client] [details]
---
# Today

Read-only until Matt picks first passes. Nothing is written to his calendar, mailbox, Teams, or Smartsheet. Times in Central.

## 1. Fetch (scout)
Send `scout` one batched request per source and work only from its compact tables:
- **Calendar:** today's Outlook events with attendees. Note gaps of 30 minutes or more (focus blocks).
- **Email:** threads from the last 5 business days where Matt is on To, the last message is from someone else, and it asks for something or is unanswered; plus flagged. Skip newsletters, automated, noreply, calendar notices.
- **Teams chats:** unanswered asks to Matt (read-only).
- **Smartsheet:** for each Active client in `clients/roster.md`, RAIDE and plan sheets from `client.md`/`project.md`. No IDs recorded: scout browses Ethos Clients > Clients and you propose recording them. Pull Matt's items overdue, due today or this week; on his projects also anything overdue, Blocked, or Owner TBD.
- **Action Log** (`standards/tools.md`): open commitments due or overdue; waiting-on items older than 3 business days; plus yesterday's sent mail and meetings for unlogged commitments (proposed adds).

## 2. Meeting prep
For each client meeting, resolve the client via the roster and read open items in `project.md` and the last 2 `decisions.md` entries. For client status meetings, run the `agenda` skill and put its talk track in the prep block.

## 3. Build the plan
- Rank: overdue client commitments, today's meeting prep, emails and Teams asks blocking someone, due-this-week items, everything else.
- Time-block: meetings fixed, a prep block before each client meeting, focus blocks in gaps for the top priorities, 15 minutes slack between back-to-back blocks.
- Output:
  1. **Day at a glance:** Time / Block / What.
  2. **Needs you:** emails, Teams asks, Smartsheet items (overdue first), Action Log items.
  3. **I can take a first pass at:** 3 to 5 numbered items, each with what Claude produces (reply draft, prep notes, recap of an unrecapped meeting, RAIDE update preview, one-pager draft). Only what Claude can do with its tools.
- Ask which to start (AskUserQuestion, multi-select). Do them in the order picked.

## 4. Write-back queue
If `state/writeback-queue.md` has entries, show them grouped by client after the plan and ask which to apply (multi-select). Include proposed Action Log adds in the same ask.

## 5. Save the plan
Write to `daily/YYYY-MM-DD.md` (gitignored): time blocks, every open item with its source, first-pass list with status (open / in progress / done). Update status as items finish. `/wrap` reads these files.
