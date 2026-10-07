---
name: chase
description: Draft nudges for Action Log "waiting on" items that have gone quiet. Use for "/chase", "who owes me something", or "follow up on what I'm waiting on".
argument-hint: [days, default 3 business] [client]
---
# Chase

Drafts only. Never send.

1. One `scout` call on the Action Log (ID in `standards/tools.md`): open Waiting-on rows older than the threshold (default 3 business days), optionally for one client. Columns: Row / Item / Owed by / Client / Logged / Due / Source. Empty sheet: say so and stop.
2. Group by person. Table: Person / Items / Oldest / Client.
3. Ask which to chase (multi-select).
4. For each, follow the `email` skill: short, direct, fair; name the specific item and the date it was asked for; one clear ask. Client contacts come from `client.md`; external names not in context are flagged. Same thread via reply-draft when a source email exists.
5. Client-facing drafts end with the verification checklist. Never include `internal.md` content.
6. After Matt sends them, offer to update the Action Log rows (preview and confirm first).
