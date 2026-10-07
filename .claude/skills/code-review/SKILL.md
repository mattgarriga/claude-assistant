---
name: code-review
description: Review NetSuite SuiteScript, SDF objects, or a git diff against Ethos coding standards. Use for "review this script," "check this PR/branch," or before any commit Claude makes.
---
# Code Review
Read: `standards/coding-standards.md`, `standards/dev-workflow.md`, the repo `CLAUDE.md`, `knowledge/netsuite-dev-patterns.md`.

Check, in order:
1. Correctness against the requirement (SDD or ticket if referenced).
2. Script type fit (same challenges as the SDD skill's Section 4 gate).
3. Governance: units per entry point, searches/loads in loops, yield/reschedule needs.
4. Idempotency and duplicate handling.
5. Error handling: nothing swallowed, summarize iterates errors, useful log context.
6. SuiteScript 2.1 compliance, N/query parameterization, date handling (TO_CHAR, MM/DD/YYYY for submitFields).
7. Coding standards file items.
8. Hard-coded IDs, credentials, environment-specific values.

Output a table: Line/Area / Severity (Blocker, Fix, Nit) / Finding / Suggested change. Then a 1-line verdict. Offer to apply fixes on a feature branch.
