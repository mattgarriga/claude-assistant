---
name: client-context
description: Maintain per-client and per-project context files. Handles the post-task write-back, /client-update from a source, /new-client scaffolding, and the one-time /bootstrap seed.
---

# Client Context

## File roles
| File | Holds | Client-facing safe? |
|---|---|---|
| `client.md` | Overview, contacts, NetSuite footprint, integrations, conventions, glossary, tool IDs (Read AI folder, Smartsheet sheets, Lucid folder), active projects list | Yes, as source material |
| `decisions.md` | Dated, append-only log: decision, why, who decided, source | Yes |
| `internal.md` | Stakeholder dynamics, escalations, budget/resourcing internals, decisions made against Ethos advice, relationship notes | **Never** |
| `projects/<p>/project.md` | Scope, SOW/CO refs, status, budget hours, open items, artifacts (SDD, Lucid links) | Yes |

## Line rules
- Every fact carries a source tag: `[src: ReadAI 2026-09-14 "HUT Weekly Status"]`, `[src: Outlook 2026-09-10 from j.doe]`, `[src: Smartsheet HUT RAIDE r123]`, `[src: Matt]`.
- Facts, not interpretation. If you're inferring, don't write it.
- Prefer durable phrasing over figures that go stale; dated figures live in `project.md` Status with an "as of" date.
- `decisions.md` is append-only. Superseded decisions get a new entry referencing the old one.

## Write-back (end of every task)
Propose a compact diff:
```
clients/hut/decisions.md  + 2026-10-06 | Warranty registrations will sync nightly, not real time | Client preference to reduce API load | Decided by: HUT ops lead | [src: ReadAI ...]
clients/hut/projects/warranty-registration/project.md  ~ Status: UAT start moved to 10/20
```
Append the diff to `state/writeback-queue.md` under the client heading with date and source, and tell Matt in one line that it was queued. Ask immediately instead only when the next step depends on it (decision on an SDD or SOW in progress, scope or pricing change, a fact the current task relies on). Apply only after Matt approves, then remove the applied entries from the queue. If nothing durable came out of the task, say "No context updates."

## /client-update <client> [source]
Pull the given source (a Read AI meeting, an email thread, a Smartsheet sheet) or the last 14 days if none given, extract durable facts, and propose a diff using the rules above.

## /new-client <name>
Copy `clients/_template/`, add the roster entry with aliases, ask Matt for contacts' domain, Read AI folder, key Smartsheet sheets.

## /bootstrap (one-time)
Seed the 7 core clients from the last 90 days: HUT, Cala Health, 4Patriots, CommSell, IMI, Core Transformers, Cerio.

For each client, in order:
1. Ask Matt (all clients batched in one message up front): client email domain(s), Read AI folder name if any, key Smartsheet sheet names.
2. Read AI: list meetings in the client folder or matching the domain over 90 days. Pull summaries, decisions, action items, topics. Transcripts only if needed.
3. Outlook: threads with the client domain over 90 days. Subjects and bodies of substantive threads only; skip automated mail.
4. Smartsheet: the client's RAIDE log, plan, and Ethos Development Tracker rows for that client (read only).
5. Draft `client.md`, `decisions.md`, `internal.md`, and one `project.md` per workstream, with source tags on every line. Merge with the existing seed content (lines marked `[src: claude.ai memory]`), resolving conflicts in favor of the newer source and flagging them.
6. Present a per-client review: proposed files, conflicts, low-confidence items, mistranscription suspects. Write only after Matt approves that client.

Stop after each client for review. Don't batch-write all seven.
