---
name: today
description: Matt's daily plan. Pulls today's calendar, emails and Teams asks needing his attention, and RAIDE and project plan items from the Ethos Clients Smartsheet workspace, builds a time-blocked day, saves it, and offers first passes. Use for "today," "morning brief," "plan my day," or "what's on my plate."
argument-hint: [client] [teams] [full]
---
# Today

Read-only until Matt picks first passes. Nothing is written to his calendar, mailbox, Teams, or Smartsheet. Times in Central.

## 1. Fetch (lean by default)
One `scout` call, all sources in parallel, compact tables only. Default scope:
- **Calendar:** today's Outlook events with attendees. Note gaps of 30 minutes or more.
- **Email:** last 3 business days, Matt on To, last message from someone else, asks for something or unanswered; plus flagged. Skip newsletters, automated, noreply, calendar notices. Cap 15 threads.
- **Action Log** (`standards/tools.md`): open items due or overdue, and waiting-on items older than 3 business days. No scan of sent mail.
- **Smartsheet:** only clients with a meeting today or named in the arguments, using sheet IDs from `client.md`. Read by ID; never browse the workspace. Matt's items overdue or due this week, plus Blocked or Owner TBD on those sheets.

Off by default, add by argument: `teams` (unanswered Teams asks), `full` (Smartsheet for every Active client, 5 business days of email, Teams, yesterday's sent mail and meetings for unlogged commitments), or a client name (that client only).

## 2. Meeting prep
For each client meeting, resolve the client via the roster and read open items in `project.md` and the last 2 `decisions.md` entries. For client status meetings, offer `agenda` as a first pass; do not run it unprompted.

## 3. Build the plan
- Rank: overdue client commitments, today's meeting prep, emails and Teams asks blocking someone, due-this-week items, everything else.
- Time-block: meetings fixed, a prep block before each client meeting, focus blocks in gaps for the top priorities, 15 minutes slack between back-to-back blocks.
- Output:
  1. **Day at a glance:** Time / Block / What.
  2. **Needs you:** emails, Teams asks, Smartsheet items (overdue first), Action Log items.
  3. **I can take a first pass at:** up to 3 numbered items (offer only; produce nothing until Matt picks), each with what Claude produces (reply draft, prep notes, recap of an unrecapped meeting, RAIDE update preview, one-pager draft). Only what Claude can do with its tools.
- Ask which to start (AskUserQuestion, multi-select). Do them in the order picked.

## 4. Write-back queue
If `state/writeback-queue.md` has entries, show them grouped by client after the plan and ask which to apply (multi-select). Include proposed Action Log adds in the same ask.

## 5. Save the plan
Write to `daily/YYYY-MM-DD.md` (gitignored): time blocks, every open item with its source, first-pass list with status (open / in progress / done). Update status as items finish. `/wrap` reads these files.
