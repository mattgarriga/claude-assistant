# RMA and Refund Flow (Shopify)

| Field | Value |
|---|---|
| Client | 4Patriots |
| Type | Project / Ad-Hoc Support (not yet scoped) |
| SOW / CO | none |
| Pricing | |
| Budgeted hours | |
| Ethos owner | Matt Garriga with Brian Webb [src: ReadAI 2026-10-07 4P - RMA/Refund Flow Review] |
| Phase | Design |

## Status (as of 2026-10-08)
- Internal working session 2026-10-07 (Matt, Brian). No client sign-off. Proposed direction: create an RMA at return initiation instead of going straight to a cash refund, then Item Receipt against the RMA. [src: ReadAI 2026-10-07 4P - RMA/Refund Flow Review]
- Aubrey Nickell's direction, relayed by Brian: focus on Shopify. [src: ReadAI 2026-10-07]
- Draft proposed-state flow built in Lucid 2026-10-08. Brian has his own draft ("4Patriots RMA Flow") that is separate. [src: Lucid]

## Scope summary
- Proposed state only; current-state page not built. Partial vs full refund, restock vs scrap, TikTok (returns handled offline), Sticky, and BigCommerce were not settled. [src: ReadAI 2026-10-07]

## Open items
| # | Item | Owner | Status |
|---|---|---|---|
| 1 | How does Ryder handle returns and refunds today, and what is exchanged with NetSuite? | Brian Webb (ask Amber) | Open |
| 2 | Unmatched return at Ryder: blind RMA, keep inventory adjustment, or standalone receipt | Owner TBD (client decision) | Open |
| 3 | Who issues the refund in Shopify, and is it released only after Ryder receipt? | Brian Webb (via Amber, Aubrey) | Open |
| 4 | Replace placeholder items with real items on refund lines? | Brian Webb (ask Aubrey) | Open |
| 5 | What event triggers RMA creation, and which component creates it (script or Celigo)? | Owner TBD | Open |
| 6 | NetSuite record created at refund time (customer refund, cash refund, credit memo) | Owner TBD | Open |
| 7 | Does the unshipped-cancellation path stay in script or move to Celigo? | Owner TBD | Open |
| 8 | Risk of duplicate data if Shopify refund sync continues alongside RMA and Item Receipt | Owner TBD | Open |

## Artifacts
| Artifact | Link / Path |
|---|---|
| Process flow (Lucid, proposed state) | https://lucid.app/lucidchart/9348af80-e623-432e-8fd5-ca7e0f4d2810/edit |
| Process flow PNG | outputs/4Patriots - RMA Process Flow.png |
| Read AI meeting | https://app.read.ai/analytics/meetings/01M4BP4RS107MYQC899AVZYA5M |
