---
name: check
description: Check text Matt wrote himself (email, Teams message, doc text) for voice, internal leakage, invented owners, and dates before it goes out. Use for "/check", "look this over", or "is this safe to send".
argument-hint: <client> [email | message | doc] then paste the text
---
# Check

Read-only. Never rewrites unless asked. Never sends.

1. Resolve the client from the argument or the text (roster aliases). Internal-only text (all Ethos recipients): lint only, skip step 3.
2. Save the text to the scratchpad and run `python3 scripts/lint_voice.py <file>`. Report every hit with its line.
3. Client-facing: run `qa-gate` with the client slug, output type (email, message, or other), and the file path. It checks leakage against `internal.md`, invented owners, date format, banned phrases, and the checklist.
4. Output one table: Check / Result / Quoted line / Why. Then a verdict: Ready, Fix first (list), or Ask Matt (list).
5. Offer a corrected version in Matt's voice (direct, concise, no filler) only if Matt wants it. Corrections change only what failed a check.
6. Client-facing text always ends with the verification checklist (recipients, uncertain names, inferred commitments or dates).
