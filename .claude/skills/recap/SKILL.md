---
name: recap
description: Build an Ethos meeting recap from Read AI data. Use when Matt asks for a recap, meeting recap, status meeting recap, or recap email for any client or internal meeting, even if he doesn't name the meeting precisely.
argument-hint: [client] [meeting or date]
---

# Meeting Recap

Format is authoritative in `standards/recap-format.md`. This skill is the workflow.

## 1. Identify client and meeting
- Resolve the client via `clients/roster.md`. Read `clients/<slug>/client.md` (Read AI folder ID, glossary, contacts, active projects) and the relevant `project.md` files.
- Ambiguous date or client: check the Outlook calendar first for the exact window and attendee list.
- Finding the meeting: `scout` lists Read AI candidates (client folder when `client.md` has a folder ID, otherwise the full local day in UTC) and the Outlook invite.
- More than one candidate: list title, time, attendees and ask. Never guess.
- Bot never joined (no data, or `end_time_ms` null long after the slot): say so and ask for notes or a transcript.
- **Notes mode:** when Matt pastes notes or a transcript instead, skip step 2 (no `meeting-analyst`, no Read AI pull). Take attendees and times from the Outlook invite, build from his notes only, and mark every action owner or decision not stated in the notes as "Owner TBD" or leave it out. Steps 3 to 9 still apply, and the checklist adds "Built from Matt's notes, not a recording." Never fill gaps from the invite title or past meetings.

## 2. Pull
Send the meeting ID to `meeting-analyst`. It pulls the meeting (transcript only when needed), fixes names against the glossary, and returns structured JSON. Work from that JSON, not the raw meeting.

## 3. Clean
- Review `glossary_suspects` against `standards/tools.md` and the client glossary. Unresolvable names go to the checklist, never silently guessed.
- Attendance and recipients come from the Outlook invite, not Read AI.

## 4. Internal vs client-facing
- All attendees @ethosbusinesssolutions.com: internal variant, named owners in bullets.
- Any external attendee: client-facing. Exclude everything in `internal.md` and anything about budget internals, staffing, politics, escalations.

## 5. Build
- Group by workstream when the meeting covered several (use the project names in `projects/`).
- Decisions Made: only real decisions, past tense, complete.
- Budget Metrics table: source Estimated Hours, Case Total Hours, and Case Total Hours this month from the project RAIDE (or MS RAIDE) via `scout`, and cite the sheet. Otherwise only sourced numbers. Note missing ones in a line under the table; never invent.
- Omit Risks & Open Items if none.
- Run `scripts/lint_voice.py` on the draft.
- Client-facing: run `qa-gate` (client slug, type recap) and fix every FAIL before showing Matt. Internal recaps skip the gate.

## 6. Output
- Default: paste-ready subject + body in chat.
- Outlook draft only on request (attendees from the invite; internal recaps to Matt). Outlook drafts end with the signature block from `standards/tools.md`; chat paste-ready text does not include it.
- Dates are MM.DD.YYYY everywhere, including the subject line and the Budget Metrics "As of EOD" line.
- No .docx. Recaps are text or Outlook drafts only.

## 7. Verification checklist (client-facing, always)
- Names or terms possibly mistranscribed
- Action items where the owner or ask was inferred
- Recipient list used
- Budget figures without a clear source

## 8. RAIDE and project log proposals (client and internal meetings)
1. Use the meeting-analyst JSON (`raide_candidates`, `action_log_candidates`, `internal_only`). Get sheet IDs: MS RAIDE from `client.md`, project RAIDE and project plan from the relevant `project.md`. Pick the RAIDE per the raide routing rule. Missing ID: say so and skip that sheet.
2. Have `scout` pull the RAIDE rows. Rows created or modified between the meeting's start and end time mean the RAIDE was updated live. In that case, propose only items from this meeting that are still missing. If no rows changed in the window, propose every qualifying item.
3. Route by type. Risks, Issues, Decisions, Escalations and client-facing Actions go to the RAIDE. Task-level work (build, configure, test, deploy) goes to the project plan sheet.
4. Both sheets are client-visible. Apply the client-facing rules from step 4 to every proposal, even for internal meetings. An item that only makes sense with internal context is proposed for Matt's Action Log instead (sheet in `standards/tools.md`), and any stakeholder or budget dynamics go to the `internal.md` write-back.
5. Match against existing rows. Update a matching row rather than adding a duplicate.
6. Owner TBD stays TBD. Never assign an owner or a due date that wasn't stated.
7. Also propose Action Log rows for Matt's own commitments and for things he is waiting on from others, with Source = the meeting link.
8. Show the preview: Sheet / Action (Add/Update) / Row / Column / Old / New. Nothing is written until Matt confirms. On confirm, write through the raide and tasks rules.

## 9. Context write-back
Propose updates per the client-context skill: new decisions to `decisions.md`, status/budget/open items to `project.md`, sensitive dynamics to `internal.md`, new glossary corrections to `client.md`.
