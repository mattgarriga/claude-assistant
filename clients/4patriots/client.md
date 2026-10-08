# 4Patriots

## Overview
> SEED from claude.ai memory. /bootstrap verifies and replaces.
- Workstreams: chargebacks, Emagia AR integration, installments [src: claude.ai memory]
- Glossary: Read AI hears Emagia as 'Imagia' [src: claude.ai memory]
- Industry / what they do:
- Engagement type: Managed services, Starter package (Ethos's smallest tier, 15 hours per month). Ethos account lead: Matt Garriga. [src: Matt 2026-10-07]
- Relationship tone notes (client-safe):

## Contacts
| Name | Role | Email | Notes |
|---|---|---|---|
| Aubrey Nickell | Controller | | [src: Matt 2026-10-07, dictated; spelling unconfirmed] |
| Jacque Davis | Aubrey Nickell's boss (title unknown) | | [src: Matt 2026-10-07, dictated; spelling unconfirmed] |
| Michelle Newberry | CFO | | [src: Matt 2026-10-07, dictated; spelling unconfirmed] |
| Robert Fort | CIO | | [src: Matt 2026-10-07, dictated; spelling unconfirmed] |
| Matt Green | Director of Operations | | [src: Matt 2026-10-07, dictated; spelling unconfirmed] |
| Jess Adcock | Accounting; technically the NetSuite admin | | [src: Matt 2026-10-07, dictated; spelling unconfirmed] |
| Joel A | Collections | | surname unknown; [src: Matt 2026-10-07, dictated; spelling unconfirmed] |
| William Adams | Product manager | | [src: Matt 2026-10-07, dictated; spelling unconfirmed] |
| Steph Long | Lead developer | | [src: Matt 2026-10-07, dictated; spelling unconfirmed] |
| Daniel Brooks | Director of IT | | [src: Matt 2026-10-07, dictated; spelling unconfirmed] |

## Tool IDs
| Tool | ID / Name |
|---|---|
| Email domain(s) | 4patriots.com |
| Repo | ../Repos/ |
| Read AI folder | 4P |
| Smartsheet: RAIDE | 4Patriots MS - RAIDE (3047468116692868) |
| Smartsheet: project plan | none |
| Dev Tracker value | 4P |
| Lucid folder | Process Flows / [Client] |
| OneDrive folder (read-only source docs; never write outputs here) | |

## Sheet schemas (cache)
Record once after the first `get_columns` on each sheet so later runs skip the read. Refresh only if a write fails or Matt says the sheet changed.
| Sheet | Columns | Picklists |
|---|---|---|

## NetSuite footprint
| Area | Notes |
|---|---|
| Edition / modules | |
| Key customizations | |
| Key scripts | |

## Integrations
| System | Direction | Middleware | Notes |
|---|---|---|---|
| Shopify | to NetSuite (refunds) | Celigo (unconfirmed) | Refund staging record plus MapReduce script creates cash refund [src: ReadAI 2026-10-07] |
| AfterShip | to Shopify (return notice) | | Returns intake [src: ReadAI 2026-10-07] |
| Ryder (3PL) | NetSuite to Ryder | VSLEGO (unconfirmed) | Integrated with NetSuite, not Shopify; receipts booked as inventory adjustments today [src: ReadAI 2026-10-07] |

## Conventions
-

## Glossary (Read AI corrections, internal terms)
| Heard as | Correct |
|---|---|
| Saligo, writer | Celigo (spelling unconfirmed) [src: ReadAI 2026-10-07 4P RMA/Refund Flow Review] |
| Rider | Ryder (3PL) [src: ReadAI 2026-10-07] |
| aftership, after ship | AfterShip (returns intake) [src: ReadAI 2026-10-07] |
| VSLEGO | Unknown; path to Ryder, spelling unconfirmed [src: ReadAI 2026-10-07] |

## Active projects
| Project | Folder | Status |
|---|---|---|
| chargebacks | projects/chargebacks/ | (bootstrap) |
| emagia-ar-integration | projects/emagia-ar-integration/ | (bootstrap) |
| rma-shopify | projects/rma-shopify/ | Design |
