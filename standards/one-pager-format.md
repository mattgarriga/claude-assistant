# Development Request One-Pager Format

Formal intake doc for the Smartsheet development ticketing system. Not a task brief (that's internal delegation). Template: `templates/template-dev-request-one-pager.docx`. Not applicable for Lucid diagrams.

## Sections
| Section | Contents |
|---|---|
| Request Overview | Client / Project, Requested By (full name), Request Type |
| Business Context | Why this is needed; impact if not resolved |
| Current State vs. Desired State | Two-column table |
| Request Details | Specific change: scripts, records, fields, saved searches, workflows. Repro steps for bugs. |
| Scope & Client Guardrails | Two-column: In Scope / Out of Scope and Constraints |
| Open Questions | OQ-## / Question / Owner / Status |

## Rules
- Request Type is exactly one of: Bug Fix, Config Change, Reporting/Data, Minor Enhancement. Never invent a type.
- Never fill gaps with assumptions. Partial answer means a focused follow-up.
- Footer: "Ethos Business Solutions | Development Request One-Pager | Attach to Smartsheet Intake Form".
- File as `clients/<slug>/projects/<project>/outputs/one-pager-[topic]-[YYYY-MM-DD].docx` (ad-hoc requests go under `projects/ad-hoc-support/`).
