---
name: estimate
description: Rough level-of-effort ranges for a one-pager, SDD, or scope description, by phase, using the estimator sheet and past work. Hours only, never pricing. Use for "/estimate", "how many hours is this", or before a SOW or CO.
argument-hint: <client> <scope text, one-pager, or SDD path>
---
# Estimate

Output is hours by phase for Matt to refine. Never dollars: fees stay `PRICING-PROVIDE-BEFORE-SENDING`. Cheyenne Johnson signs off on LOE before any SOW is issued; say so in the output.

1. Read the scope (pasted text, or extract an SDD or one-pager with `pandoc`). Resolve the client; read `client.md`, the relevant `project.md` (budgeted hours of similar past work), and `knowledge/`.
2. Native-first: for each item, say whether native NetSuite can cover it. Estimate only what truly needs build or config. If the design is not final, say so and list the open questions that move the number.
3. Break the scope into rows like `templates/estimation-template.xlsx`:
   | Tab | Row shape |
   |---|---|
   | Functional | Task / Design / Configuration / UAT / Training / Cutover / Support |
   | Technical NetSuite | Task / Script type / Design / Development / UAT / Training / Cutover / Support |
   | Integration | Flow / Method / Source and target / Design / Development / UAT / Training / Cutover / Support |
4. Hours: anchor to the sheet's placeholder rows as a shape (for example Map/Reduce 4 design, 12 development, 4 UAT, 2 cutover, 4 support), then adjust with similar past projects from `project.md` and Matt's input. Give a likely figure and a low to high range per row. Mark every figure with its basis (sheet shape, past project, Matt) and never invent a basis.
5. Output: the three tables, a phase totals table (Design through Support), Project Oversight shown as a separate line using the percent Matt confirms, assumptions, and open questions with owners.
6. Known template conflict to ask Matt before totals go into a SOW: the estimator sheet uses 15 percent oversight and a $300 standard rate, while `standards/sow-format.md` says 20 percent and the template wording says $225. Do not pick one; list both and ask.
7. Offer to fill a copy of the estimation sheet in `clients/<slug>/projects/<project>/outputs/` (hours only, rate cells left blank) and to hand the totals to `/sow`.
