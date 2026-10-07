---
name: today
description: Matt's daily plan. Pulls today's calendar, emails needing his attention, and RAIDE and project plan items from the Ethos Clients Smartsheet workspace, builds a time-blocked day, saves it, and offers first passes. Use for "today," "morning brief," "plan my day," or "what's on my plate."
---
# Today

Read-only until Matt picks first passes. Nothing is written to his calendar, mailbox, or Smartsheet. Times in Central.

## 1. Calendar
- Today's events from Outlook. For each client meeting: client (via `clients/roster.md`), attendees, open items from the client's `project.md`, last 2 entries in `decisions.md`.
- Note gaps of 30 minutes or more. These become focus blocks.

## 2. Email needing attention
- Threads from the last 5 business days where Matt is on To, the last message is from someone else, and it asks for something or is unanswered. Plus anything flagged.
- Filter noise: newsletters, automated, noreply, calendar notifications.
- One line each: Sender / Subject / Received / What it needs.

## 3. Smartsheet (Ethos Clients workspace, folder "Clients")
- For each Active client in `clients/roster.md`, read the RAIDE and project plan sheets listed in `client.md`. If a client has no sheet IDs recorded yet, browse its folder under Ethos Clients > Clients, use what you find, and propose recording the IDs in `client.md`.
- Pull: items Matt owns that are overdue, due today, or due this week. On Matt's projects, also pull anything overdue, Blocked, or Owner TBD regardless of owner.
- One line each: Client / Sheet / Item / Owner / Due / Status.

## 3b. Action Log
- Read Matt's Action Log (`standards/tools.md`). Pull open commitments that are due or overdue, and waiting-on items older than 3 business days (candidates for a nudge draft).
- Scan yesterday's sent mail and meetings for new commitments or waiting-on items not yet logged, and list them as proposed Action Log adds.

## 4. Build the plan
- Rank: overdue client commitments, then today's meeting prep, then emails blocking someone, then due-this-week items, then everything else.
- Time-block the day: meetings fixed, a prep block before each client meeting, focus blocks in the gaps assigned to the top priorities. Leave 15 minutes of slack between back-to-back blocks.
- Output:
  1. **Day at a glance:** one table, Time / Block / What.
  2. **Needs you:** emails table, Smartsheet items table (overdue first).
  3. **I can take a first pass at:** 3 to 5 numbered items, each with what Claude produces (reply draft, meeting prep notes, recap of an unrecapped meeting, RAIDE update preview, one-pager draft). Only items Claude can actually do with its tools.
- Ask which to start (AskUserQuestion, multi-select). Do them in the order picked.

## 4b. Write-back queue
If `state/writeback-queue.md` has entries, show them grouped by client after the plan and ask which to apply (multi-select).

## 5. Save the plan
Write the plan to `daily/YYYY-MM-DD.md` (gitignored): the time blocks, every open item with its source, and the first-pass list with status (open / in progress / done). Update the status as items finish during the day. The "take off my plate" prompt after each task draws from this file.
