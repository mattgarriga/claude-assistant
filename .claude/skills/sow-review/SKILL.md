---
name: sow-review
description: Read-only review of a SOW or Change Order someone else drafted: template version, standard assumptions, pricing placeholders, scope creep, native-first, LOE sign-off, totals. Use for "/sow-review <file>" or "check this SOW before I approve."
argument-hint: <file>
---
# SOW / CO Review
Read-only; no edits. Read `standards/sow-format.md` and the file (docx via text extraction, for example pandoc). Resolve the client via the roster and read `decisions.md` and `project.md` for the amended SOW.

| Check | Pass condition |
|---|---|
| Template version | 2026 layout: no Document Control table, no address header; CO uses CO template wording |
| Standard assumptions | All 5 present (canonical wording in `standards/sow-format.md`); note any edited or removed |
| Pricing | `PRICING-PROVIDE-BEFORE-SENDING` left in where pricing is not confirmed; flag any figure with no source |
| Scope creep | Vague deliverables, unbounded verbs, missing typed deliverables ("Suitelet: ..."), Out of Scope is optional; if absent, at most an informational note, never a defect |
| Native-first | Custom script where saved search, workflow, form, or config would do |
| LOE sign-off | Cheyenne's sign-off on LOE is confirmed; if not stated, flag "Confirm Cheyenne has signed off on LOE" |
| Totals | If numbers present: 50% split and balance equal the Total Fee; T&M hours times rates sum correctly. Show the arithmetic |
| Signature block | Client signer matches `client.md`, Ethos signer Cedric Carter |

Output: findings table Check / Result (Pass, Flag, Fail) / Quoted text / Why / Suggested change, then a one-line verdict. Never fill gaps by assumption; gaps become questions with an owner.
