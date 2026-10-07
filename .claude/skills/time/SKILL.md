---
name: time
description: Turn Matt's daily time notes into a NetSuite time import CSV with the right project and case. Use for "/time", "do my time", "time entry for yesterday", or end-of-day time.
argument-hint: [YYYY-MM-DD] [notes pasted or file path]
---
# Time Entry

No NetSuite connection. Output is a CSV in `time/` for NetSuite's import assistant. Plan and open items: `docs/build/time-entry-plan.md`. Mappings live in `time/lookup.json`.

## 1. Get the notes
Matt pastes the day's block (or gives a .docx or PDF path; extract with `pandoc` or `pdftotext`). Date comes from the argument; if absent, ask. Check `time/exported.json`: if the date is already exported, say so and stop unless Matt says to redo.

Format:
```
Client - Label: hours |
* task | task | task
```
Save the notes to the scratchpad and run `python3 scripts/time_entry.py parse <file>`. Report any `unparsed` line instead of guessing.

## 2. Resolve each entry (project, task, item)
| Case | Rule |
|---|---|
| `Ethos - ...` | Internal: project, task, and item from `internal` in `time/lookup.json` (Ethos Internal Project, General Admin) |
| Label already in `labels` (key `client|label`, lowercase) | Use it |
| New label | Find the label text in that client's MS RAIDE (sheet ID in `client.md`, cached schema, `find_in_sheet`; project RAIDE if `project.md` lists one). Take the Case Number from the matching row |
| RAIDE row has a Case Number | Support work: project = the client's `support_project`, task = `Case # <number>` |
| RAIDE row belongs to a named project (no case) | Project work: pick the matching entry in `project_tasks` (project and task) |
| Standing labels (Status, Internal) | Ask once which case or project, then save |
| No match, several matches, or label looks like a ticket number you cannot place | Ask with AskUserQuestion, listing candidates. Never guess |

Item is `Consulting Services` unless the lookup says otherwise. First run only: confirm with Matt that the RAIDE Case Number equals the number after `Case #` in NetSuite before relying on it.
Save every confirmed mapping to `labels` in `time/lookup.json`.

## 3. Memos
Memos are client-visible on client projects. Rewrite each task list into client-safe wording in Matt's style: past-tense action phrases joined with ` | `, specific but without internal chatter (internal-only items such as "catch up" or staffing become neutral work phrases, or are folded into a related item). Never invent work that is not in the notes. Flag any rewrite that changes meaning. Internal project memos stay as Matt wrote them. EVgo: check `clients/evgo/internal.md` before wording the memo.

## 4. Preview
Table: Client / Label / Project / Case-Task-Event / Hours / Memo. Show raw total versus rounded total (quarter hours, any difference placed on the largest entry) and list any unresolved or flagged items. Ask for confirmation.

## 5. Write
On yes, write the final entries (fields `client`, `label`, `project`, `task`, `item`, `memo`, `hours_raw`) to a JSON file in the scratchpad and run `python3 scripts/time_entry.py build <file> --date YYYY-MM-DD`. It validates, rounds to 0.25, reconciles, writes `time/YYYY-MM-DD.csv`, and records the date in `time/exported.json`. Link the CSV. The first import should be one test row: Matt confirms the import mapping (Name = project, Case/Task/Event, Item, Duration, Note).

Reply with: rows, total hours, file link, and any mappings saved.
