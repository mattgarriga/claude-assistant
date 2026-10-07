# Development Request One-Pager Format

Formal intake doc for the Smartsheet development ticketing system. Not a task brief (that's internal delegation). Template: `templates/template-dev-request-one-pager.docx`, filled through `lib/docx/` (data.json, doc-producer agent). Not applicable for Lucid diagrams.

## Sections (template order)
| Section | Contents |
|---|---|
| Title banner | "ETHOS BUSINESS SOLUTIONS", "Development Request One-Pager", and the template subtitle line |
| REQUEST OVERVIEW | Table: Client / Project, Requested By (full name), Request Type |
| BUSINESS CONTEXT | Why this is needed; impact if not resolved |
| CURRENT STATE VS. DESIRED STATE | Two-column table: Current State / Desired State |
| REQUEST DETAILS | Specific change: scripts, records, fields, saved searches, workflows. Repro steps for bugs. |
| SCOPE & CLIENT GUARDRAILS | Two-column table: In Scope / Out of Scope / Constraints |
| OPEN QUESTIONS | Table: # / Question / Owner / Status |
| Footer text line | "Ethos Business Solutions  |  Development Request One-Pager  |  Attach to Smartsheet Intake Form" (kept) |

## Rules
- Helper and instruction lines under each section heading (the grey italic guidance) are removed in output. The footer text line stays.
- Request Type is exactly one of: Bug Fix, Config Change, Reporting/Data, Minor Enhancement. Never invent a type.
- Open Questions: numbered OQ-01, OQ-02; every row has an owner; Status starts as Open. If none, one row "N/A".
- Never fill gaps with assumptions. Partial answer means a focused follow-up.
- Lists use real Word bullets or numbering.
- File as `clients/<slug>/projects/<project>/outputs/one-pager-[topic]-[YYYY-MM-DD].docx` (ad-hoc requests go under `projects/ad-hoc-support/`).
