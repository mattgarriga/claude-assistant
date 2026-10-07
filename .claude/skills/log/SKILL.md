---
name: log
description: Capture commitments, waiting-on items, and internal actions into Matt's Action Log in Smartsheet, from a typed line, a meeting, or an email. Use for "/log", "log this", "I owe X", "/log from <meeting>", or "log that email".
argument-hint: <a line> | from <meeting title, client + date, or Read AI ID> | from email <description>
---
# Log

Action Log sheet ID and schema cache are in `standards/tools.md` (rows are AL.####). Writes to this sheet are auto-approved by `scripts/guard_actionlog.py`: no preview or confirmation step, but always report what was written. Never write to any other sheet from this skill.

## Modes
| Mode | Source of items |
|---|---|
| A typed line | Parse $ARGUMENTS directly. Several items in one message are fine |
| `from <meeting>` | Find the meeting (calendar and Read AI; ask if more than one match). Send the ID to `meeting-analyst` and use only its `action_log_candidates`: Matt's own commitments and what he is waiting on from others. Source = the meeting link |
| `from email <description>` | Find the thread by sender, subject, or date (`outlook_email_search`), read it, and take the ask directed at Matt, plus anything he is waiting on. Source = the email web link |

## Fields
Subject, Type (Commitment: Matt owes it; Waiting On: owed to Matt; Internal Action; Management), Client (roster; blank if none), Date Identified (the meeting or email date), Due Date, Assigned To (Matt for commitments; leave blank for waiting-on and name the other person at the start of the Subject, for example "Waiting on Jennifer Nasseripour: ...". Never assign external people or other contacts, since Smartsheet may notify them), Priority, Status (Not Started), Details, Source.
- Waiting-on status is "In Progress - At Client" (or At Partner); commitments start at Not Started.
- Owner defaults to Matt only for "I" or "I owe". Otherwise the named person; unclear: "Owner TBD".
- Never invent an owner or due date. Due blank unless stated. Dates MM.DD.YYYY in text.
- Keep it concise: one row per real commitment, merge sub-steps into Details, no rows for things already on a RAIDE row Matt owns unless he asks.

## Steps
1. Schema: use the cached column IDs and picklist values in `standards/tools.md` (Action Log schema cache). Cells go in by `columnId`. Refresh with one `get_columns` only if a write fails.
2. Dedupe: `find_in_sheet` on the Source value (and Subject plus Client). An exact source match means skip and say so; a near match means update that row's Details instead of adding.
3. Write all new rows with one `add_rows` call to the Action Log. Use only existing picklist values.
4. Reply in one line: "Logged N: AL.#### Subject (due), ...", plus any skipped duplicates or Owner TBD items.
