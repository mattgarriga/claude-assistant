# Meeting Recap Format

Recaps are paste-ready text plus an auto-created Outlook draft. There is no recap .docx or template. Matt's standing rules win over older formats.

## Subject line
`[Client Name] - Meeting Recap | [Topic] | [MM.DD.YYYY]`

## Client-facing body
```
Hello [Client Name] Team,

Thanks for your time in today's [status meeting / working session / meeting]. Below is a recap of key updates and action items[, and budgets for open projects and ad-hoc support (status meetings only)].

[Status meeting recaps only; omit for all other recaps]
**Budget Metrics** (As of EOD [MM.DD.YYYY], last business date):
| Project | Budgeted Hours | Actual Hours | Hours Remaining |

**Decisions Made**
- ...

**Action Items**
*Ethos:*
- ...
*[Client Name]:*
- ...

**Risks & Open Items**
- [Risk or open item]: [context and impact]
```

## Rules
- All dates use MM.DD.YYYY (subject line and Budget Metrics "As of EOD" line).
- First section after budget is **Decisions Made**. Only actual decisions reached. Past tense, complete thoughts, client-ready.
- When the meeting covered several workstreams (e.g., Ad-Hoc Support, Assembly Unbuild, Warranty Registration), group Decisions and Action Items by workstream, not chronologically.
- Client-facing action items: action text only. No owner names or due dates inside the bullet. Owner is the party heading. Ambiguous: "Owner TBD".
- Budget Metrics appears ONLY in the external status meeting recap (the client's recurring status meeting). Working sessions, design sessions, internal meetings, and other recaps never include it, not even an empty table or a "no figures" line.
- Budget table: only rows with real numbers from the source. If a named project had no figures this week, say so in one line under the table. Never invent.
- Fixed-fee rows: Budgeted Hours "N/A (fixed fee)", Actual Hours and Hours Remaining blank. Hourly rows (e.g. Ad-Hoc Support) show numbers only, such as 75 / 9 / 66.
- Outlook HTML styling (matches the 10.06.2026 HUT recap): bold "Budget Metrics" label with the as-of text, then a 4-column table with 1px solid #ABABAB borders, collapsed, header row fill #CCE4F6 with bold black text, body cells plain, font Aptos 11pt, column widths about 210 / 124 / 113 / 159 px.
- Risks & Open Items: omit the section entirely if none.
- No "Next Steps" section. Recap ends after Risks (or Action Items).
- No internal Ethos commentary: budget internals, staffing, resourcing, politics, escalations.

## Internal variant (all attendees @ethosbusinesssolutions.com)
- Greeting "Team,". Same sections, never a budget table.
- Action items list named individual owners in the bullet.
- Draft addressed to Matt.

## Output
- Default: paste-ready subject + body in chat.
- Outlook draft is created automatically with every recap (draft only, never sent), addressed to the calendar invite's attendees (not Read AI's participant list). Drafts end with the signature block in `standards/tools.md`. The chat copy has no signature and carries the verification checklist.
