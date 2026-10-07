# /time plan (daily time entry to NetSuite CSV)

Status: planned 2026-10-07. Not built. Waiting on the items under "Open".

## Input (Matt's OneNote format, pasted per day)
```
Client - Label: hours |
* task | task | task
```
- `Ethos - General` is internal time.
- Hours are already quarter hours. Round to 0.25 and reconcile any difference to the day total on the largest entry.
- Source of truth for notes is OneNote. The M365 connector can find `.one` files but cannot read them (no Notes scope), so Matt pastes the day, or exports a month page to .docx or PDF.

## Resolution
- Label is RAIDE subject text. Resolve through the client's MS RAIDE (and project RAIDE if listed in `project.md`) using the Case Number column and the cached schema in `client.md`.
- Known labels come from `time/lookup.md` (label to case number and NetSuite project). Only new labels trigger a Smartsheet find. Unresolved or ambiguous labels are asked, never guessed, then saved.
- Standing buckets (for example `HUT - Status`) are stored once in the lookup.

## Memo
- Client-visible. For client projects, rewrite tasks into client-safe wording (no internal chatter, no names of internal staff conflicts). Internal project memos use Matt's text as written.
- Join tasks with semicolons.

## Output
- Preview table: Project / Case-Task-Event / Duration / Memo, plus the day total.
- On confirmation, write `time/YYYY-MM-DD.csv` in the exact column layout of Matt's NetSuite time export.
- No NetSuite connection. Matt imports with NetSuite's import assistant.
- Keep a record of dates already exported to prevent duplicates.

## Open
| Item | Owner |
|---|---|
| NetSuite saved search export of recent time entries (CSV) to match column names and project values | Matt |
| Name of the internal NetSuite project for `Ethos - General` | Matt |
| Whether to also use calendar and sent mail to catch unlogged time (optional) | Matt |

## Notes
- RAIDE columns Case Number, Case URL, Case Total Hours, Case Total Hours this month already exist, so time entered here feeds the budget burn used by `/recap` and `/status`.
- Today's Read AI note "Dashboard feedback" mentions a time-tracking assistant using Smartsheet and Read AI data. Check whether that is a team effort before building to avoid duplication.
