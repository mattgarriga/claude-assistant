---
name: handoff
description: Turn a locked design, one-pager, or ticket into a task brief for the Invitra offshore team (Deepak, Omkar, Supriya). Use for "hand this to Invitra," "brief for offshore," or "write the dev task."
argument-hint: [client] [details]
---
# Invitra Handoff
Only for work outside ethos-dev. Work built with /ethos-dev:start already carries a technical handoff in its deployment package; send that and offer only a short cover note.

Internal document; never client-facing, but strip `internal.md` content anyway.
Sections: Context (2 lines), Ticket (EBS-####, Dev Tracker Row ID EBS.####) and repo, Branch (`feature/EBS-####`, `hotfix/EBS-####`, or `bugfix/<desc>`; commits `type: summary`), What to build (script outlines or diff targets), Acceptance criteria (testable), Test cases (link test-plan), Coding standards (conventions section numbers incl. the 10.4 pre-handoff checklist, via `standards/coding-standards.md`), Out of scope, Open questions with owner, Hours estimate requested.
Repo missing from `../Repos`: ask Matt for the clone URL. Clear, literal language. No idioms. Output in chat; offer an Outlook draft to Deepak.
