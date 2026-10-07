---
name: sow
description: Produce an Ethos Statement of Work or Change Order (Fixed Fee or Time and Materials). Use when Matt asks for a SOW, CO, change order, or estimate document.
---

# SOW / Change Order

Format: `standards/sow-format.md`. Templates: the four SOW/CO files in `templates/`.

## 1. Determine document
SOW vs CO, Fixed Fee vs T&M. Infer from context (a CO amends an existing SOW in `project.md`). If ambiguous, ask.

## 2. Gather (one batch, only unknowns)
- Client, project number, customization/CO name
- Problem, solution, business impact
- Assumptions (phrased "Client will...")
- Configuration and development deliverables, typed ("Suitelet: ...")
- Out of scope
- Pricing or hours by phase, and rate (standard $225 unless told $200)
- Whether Cheyenne has signed off on LOE

Pull what's already known from `project.md`, `decisions.md`, and any SDD in `outputs/`.

## 3. Scope sanity
Push back if deliverables imply custom work where native config would do, or if scope is vague enough to invite creep. Out of Scope is always explicit.

## 4. Build
- Process Overview via lucid-flow skill.
- Pricing never invented: `PRICING-PROVIDE-BEFORE-SENDING`.
- T&M: compute Oversight at 20% of phase subtotal and totals only from provided hours.
- `lib/docx/` `buildSow({ kind: "sow"|"co", pricing: "ff"|"tm" })`. Lint, render, inspect.

## 5. Handoff
Summary. If LOE sign-off unconfirmed: "Confirm Cheyenne has signed off on LOE before sending." Verification checklist. Context write-back (scope and pricing status to `project.md`).
