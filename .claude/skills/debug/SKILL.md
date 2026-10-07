---
name: debug
description: Debug a NetSuite script or integration from an error, execution log, stack trace, or symptom. Use for "this is failing," "why is X happening," pasted logs, or SSS_ errors.
argument-hint: [client] [details]
---
# Debug
1. Get the evidence: error text, execution log, record/script IDs, when it started, what changed. If missing, ask (AskUserQuestion).
2. Locate the code in the client repo. Read the script and its deployment XML.
3. Form 2 to 3 hypotheses ranked by likelihood with the evidence for each. Common traps: null objects (ScriptNullObjectAdapter), internal ID vs display text, sublist line context, governance exhaustion, UE recursion, context type filters, date format/time zone, permissions/role context.
4. Say what Matt can check in the account to confirm (never query NetSuite yourself): a saved search, a record field, a log filter.
5. Once confirmed, propose the minimal fix, apply on a `bugfix/<short-desc>` branch (or `hotfix/EBS-####` for a production fix), run the review skill, show diff.
6. Propose a `knowledge/` entry if the root cause is reusable.
