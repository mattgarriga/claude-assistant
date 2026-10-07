# OS Process Automations (OS WO)

| Field | Value |
|---|---|
| Client | Heads Up Technologies |
| Type | Project (Managed Services, NetSuite Support 0006) |
| SOW / CO | |
| Pricing | FF / T&M |
| Budgeted hours | |
| Ethos owner | |
| Phase | Design (SDD v1.0 draft, 08.28.2026; open questions still being worked 10.07.2026) [src: OS SDD v1.0 08.28.2026] [src: ReadAI 10.07.2026 OS WO Questions] |

## Status (as of 2026-10-07)
- Design phase. SDD v1.0 authored by Matthew Garriga 08.28.2026; sign-off table lists Matthew Garriga, Cheyenne Johnson, Jennifer Nasseripour (HUT), David Wilson (STG Aerospace) [src: OS SDD v1.0 08.28.2026]
- 10.07.2026 working session (OS WO Questions) covered WIP reporting, picking and labels, serial numbers, and fulfillment control before final inspection; no decisions reached [src: ReadAI 10.07.2026 OS WO Questions]
- Target raised: routings in the system and tested before 02.01.2027 (year inferred); optional small work-order subset around 12.01.2026, not confirmed [src: ReadAI 10.07.2026 OS WO Questions]

## Scope summary
- Add a finished good assembly above each outsourced part (outsourced item carries the -OS suffix); automate creation of the finished good work order from each outsourced PO line and the component issue on receipt; receiving guidance on the item receipt; line-level status, retry, and automation log; Quality inspection saved search [src: OS SDD v1.0 08.28.2026]
- Out of scope: routing step definition (client-owned), creating finished good assemblies and renumbering items, changes to the native outsourced PO and work order process, Waypoint or MRP [src: OS SDD v1.0 08.28.2026]
- Built in NetSuite with SuiteScript 2.1: 2 User Events, 2 Map/Reduce, 1 library, saved searches [src: OS SDD v1.0 08.28.2026]

## Open items
| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Draft proof-of-concept WIP detail report and assess feasibility and level of effort | Cheyenne Johnson | Open [src: ReadAI 10.07.2026 OS WO Questions] |
| 2 | Configure and demonstrate the standard work-order process end to end (picking, routing, reporting) | Cheyenne Johnson | Open [src: ReadAI 10.07.2026 OS WO Questions] |
| 3 | Review whether staging and issuing can be combined | Cheyenne Johnson | Open [src: ReadAI 10.07.2026 OS WO Questions] |
| 4 | Validate serial-number touchpoints and label fit, including label printing | Cheyenne Johnson | Open [src: ReadAI 10.07.2026 OS WO Questions] |
| 5 | Confirm whether picking uses the same record type for routed work orders | Cheyenne Johnson | Open [src: ReadAI 10.07.2026 OS WO Questions] |
| 6 | Confirm whether a finished good can be fulfilled while a later routing step is open | Cheyenne Johnson | Open [src: ReadAI 10.07.2026 OS WO Questions] |
| 7 | Arrange demonstration of the mobile workflow (SDD says HUT will use David's LogBook app, not Manufacturing Mobile, for confirmations; clarify which) | Cheyenne Johnson | Open [src: ReadAI 10.07.2026 OS WO Questions] [src: OS SDD v1.0 08.28.2026] |
| 8 | Provide example of the current WIP report (Lynette) | Jennifer Nasseripour | Open [src: ReadAI 10.07.2026 OS WO Questions] |
| 9 | Complete and send the routing-definition file | Jennifer Nasseripour | Open [src: ReadAI 10.07.2026 OS WO Questions] |
| 10 | SDD open question 3: how to determine receiving guidance for disposition location | HUT | Open [src: OS SDD v1.0 08.28.2026] |

## Artifacts
| Artifact | Link / Path |
|---|---|
| SDD v1.0 | OneDrive: Clients/Heads Up Technologies/Projects/Managed Services/0006 - OS Process Automations/02 - Design/Ethos - HUT OS Process Automations SDD.docx |
