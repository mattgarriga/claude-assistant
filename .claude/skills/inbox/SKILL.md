---
name: inbox
description: Batch inbox triage and reply drafting. Use for "clear my inbox," "draft replies for the last few emails."
argument-hint: [client] [details]
---
# Inbox Triage
1. `scout` fetches unread mail (noise filtered: newsletters, automated, noreply) and Teams chats with unanswered asks to Matt. Teams is read-only; no Teams writes. Teams items are listed in Needs attention, and any reply is drafted as text for Matt to post himself.
2. List Sender / Subject / Received / Needs, mail and Teams in separate tables. Ask which to draft and any direction (AskUserQuestion).
3. Draft each mail via the email skill and save as Outlook reply drafts, ending with the signature block from `standards/tools.md`. Never send.
4. In the step 2 multi-select, add a "Log it" choice for every email or chat that asks something of Matt or where he is waiting on someone. Chosen items go to the Action Log through the `log` skill (`from email` mode; auto-approved, Source = the email or chat link, deduped). Report one line of what was logged.
