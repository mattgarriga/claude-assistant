# SOW and Change Order Format

Four templates in `templates/`: SOW Fixed Fee, SOW T&M, Change Order Fixed Fee, Change Order T&M. Same structure; CO swaps "Statement of Work (SOW)" for "Change Order (CO)" and "Customization Name" for "Change Order Name". No section numbers.

## Sections
| Section | Contents |
|---|---|
| Header table | Client Name, Project Name (NetSuite Support - [Project #]), Customization / Change Order Name, Total Fee (FF) or Estimated Hours (T&M) |
| Basic Business Overview | Problem, Solution, Business Impact (1-2 sentences each) |
| Assumptions | Each starts with "Client will..." |
| Process Overview | Lucid PNG per `lucid-standards.md` |
| Scope and Deliverables | Hierarchical bullets. Leaf bullets as "Type: description" (e.g., "Suitelet: Order intake form with vendor lookup"). Standard bullets from the template stay (Project Management, Documentation, Configuration, Development, Enhancement Walk Through, UAT Updates, Cutover & Support). Explicit **Out of Scope** sub-list folded in. |
| Estimated Fees and Billing | FF: fixed fee, 50% on execution, 50% at UAT start, due 15 days. T&M: phase table (Design, Configuration, Development, UAT, Training, Cutover, Support, Project Oversight 20%, Hourly Totals, Estimated Fees), invoiced 15th and last day in arrears, due 15 days. |
| Signature block | Client signer / Cedric Carter for Ethos Business Solutions LLC |

## Rates and terms
- Standard $225/hr. Discounted $200/hr (only if Matt says so).
- Cutover support: 5 business days (Fixed Fee), two weeks (T&M), per templates.
- Project Oversight is 20% of the phase subtotal.

## Rules
- Never include pricing unless Matt provides it. Placeholder: `PRICING-PROVIDE-BEFORE-SENDING`.
- Cheyenne Johnson signs off on LOE before any SOW is issued. If unconfirmed, handoff says: "Confirm Cheyenne has signed off on LOE before sending."
- If FF vs T&M is ambiguous, ask.
- File as `clients/<slug>/projects/<project>/outputs/[CLIENT]-SOW-[topic-slug]-[YYYY-MM-DD].docx` (CO: `-CO-`).
