# SOW and Change Order Format

Four templates in `templates/`: `template-sow-fixed-fee.docx`, `template-sow-time-and-materials.docx`, `template-change-order-fixed-fee.docx`, `template-change-order-time-and-materials.docx`. 2026 layout: no Document Control table, no address header, no section numbers. Fill through `lib/docx/` (data.json, doc-producer agent). A CO uses the CO template's own wording; it is not a SOW with words swapped.

## Sections (template order)
| Section | Contents |
|---|---|
| Header table | Title row ("Ethos Business Solutions Statement of Work ("SOW")" or "...Change Order ("CO")"), Client Name, Project Name (NetSuite Support - [Project #]), Customization Name (SOW) or Change Order Name (CO), then Total Fee (FF) or Estimated Hours (T&M) |
| Basic Business Overview | Callout table: Problem, Solution, Business Impact (1-2 sentences each), then Assumptions |
| Process Overview | Titled Lucid diagrams only, PNG 6.9in wide. No narrative text. |
| Scope and Deliverables | Bullets nested up to 3 levels. Standard bullets stay: Project Management, Documentation, Configuration, Development, Enhancement Walk Through, UAT Updates, Cutover & Support. Leaf bullets as "Type: description" (e.g., "Suitelet: Order intake form with vendor lookup"). |
| Estimated Fees and Billing | FF: fixed fee paragraph, change-order paragraph, 50% invoice at execution, balance at start of UAT, invoices due within 15 days. T&M: estimate paragraph, the template's native Estimated Hours and Fees table (Design, Configuration, Development, UAT, Training, Cutover, Support, Project Oversight 20%, Hourly Totals, Estimated Fees), then the invoicing paragraph (15th and last calendar day, in arrears, due within 15 days). |
| Signature block | "AGREED TO AND ACCEPTED" line with the acceptance date left blank. Client: signer from `client.md`. Ethos Business Solutions LLC: Cedric Carter. |

Out of Scope is stated explicitly as a sub-list under Scope and Deliverables.

## Standard assumptions
Default on for every SOW and CO, editable per document. Client-specific assumptions are added after them ("Client will..." phrasing).
1. Client will perform necessary testing to confirm the solution is working.
2. Any material changes to the scope estimated to exceed 8 hours of effort will require a formal change order for client approval.
3. Any material changes to the scope estimated at 8 hours or less of effort will be addressed under the existing ad-hoc support agreement.
4. Following deployment to production, the solution will be supported under this SOW for 5 business days. Thereafter, ongoing support will transition to the existing ad-hoc support agreement.
5. Effort estimates will be determined by Ethos in good faith based on initial review.

In a CO, assumption 4 reads "under this CO" instead of "under this SOW".

## Pricing and terms
- Every dollar amount (Total Fee, the 50% invoice, the remaining balance, Estimated Fees) and every T&M hour figure is `PRICING-PROVIDE-BEFORE-SENDING` until Matt provides it. Never invent or compute from guesses.
- Rate wording in the T&M template stays ($225 standard). A $200 discounted rate only if Matt says so.
- Cutover support: five business days (FF), two weeks (T&M), per templates.
- Project Oversight is 20% of the phase subtotal, computed only from hours Matt provides.

## Rules
- Cheyenne Johnson signs off on LOE before any SOW is issued. If unconfirmed, handoff says: "Confirm Cheyenne has signed off on LOE before sending."
- If FF vs T&M is ambiguous, ask.
- Template boilerplate is exempt from the voice lint; only content Claude writes is linted.
- File as `clients/<slug>/projects/<project>/outputs/[CLIENT]-SOW-[topic-slug]-[YYYY-MM-DD].docx` (CO: `-CO-`). Drafts use `-draft.docx` and are not committed.
