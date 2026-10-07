---
name: sow
description: Produce an Ethos Statement of Work or Change Order (Fixed Fee or Time and Materials). Use when Matt asks for a SOW, CO, change order, or estimate document.
argument-hint: [client] [topic] [ff|tm]
---

# SOW / Change Order

Format: `standards/sow-format.md`. Templates: `templates/template-sow-*.docx` and `template-change-order-*.docx` (filled, never rebuilt).

## 1. Determine document
SOW vs CO, Fixed Fee vs T&M. Infer from context (a CO amends an existing SOW in `project.md`). If ambiguous, ask.

## 2. Gather (one batch, only unknowns)
- Client, project number, customization/CO name
- Problem, solution, business impact
- Assumptions beyond the 5 standard ones (default on, editable; wording in `standards/sow-format.md`), phrased "Client will..."
- Configuration and development deliverables, typed ("Suitelet: ...")
- Out of scope
- Whether pricing and hours are available. If not, every dollar amount and T&M hour stays `PRICING-PROVIDE-BEFORE-SENDING`
- Whether Cheyenne has signed off on LOE

Pull what's already known from `project.md`, `decisions.md`, and any SDD in `outputs/`.

## 3. Scope sanity
Push back if deliverables imply custom work where native config would do, or if scope is vague enough to invite creep. Out of Scope is always explicit.

## 4. Build
- Process Overview: titled Lucid diagrams only (flow skill), PNG 6.9in wide, no narrative.
- Scope and Deliverables nested up to 3 levels, Out of Scope explicit.
- Pricing never invented: Total Fee, 50% split, balance, and T&M hours are `PRICING-PROVIDE-BEFORE-SENDING`. T&M uses the template's native Estimated Hours and Fees table.
- Signature block: client signer from `client.md`, Ethos signer Cedric Carter, acceptance date blank.
- Write `data.json` per the `lib/docx/` README schema (kind sow|co, pricing ff|tm). The doc-producer agent fills the template, renders, and lints the filled content. Inspect the render.
- Before showing Matt, run `qa-gate` on the `data.json` content (client slug, type SOW or CO) and fix every FAIL; re-run doc-producer after content fixes. Doc-producer reports lint and secret-scan results; resolve wording hits yourself.

## 5. Handoff
Summary. If LOE sign-off unconfirmed: "Confirm Cheyenne has signed off on LOE before sending." Verification checklist. Context write-back (scope and pricing status to `project.md`).
