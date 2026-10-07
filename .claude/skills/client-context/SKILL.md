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
Seed all 13 Active clients in `clients/roster.md` from the last 90 days. Core clients (Core = Yes) are reviewed first. Nothing is written to `clients/` until Matt approves that client.

1. **Discovery (senior session, one confirmation table).** For each client find: email domains (Read AI participant emails), Read AI folder, MS RAIDE and project RAIDE/plan sheet IDs (Smartsheet search under Ethos Clients > Clients), Dev Tracker client picklist value, Lucid folder, repo path in `../Repos`. Use `scout` for listings. Show ONE table (client / domains / Read AI folder / sheets / Dev Tracker value / Lucid folder / repo) with unknowns marked. Matt corrects it once; do not ask per client.
2. **Parallel read-only drafts.** Run in an evening or overnight window. One worker per client, using `scout` for listings (Read AI, Outlook, Smartsheet RAIDE and plans, Dev Tracker rows) and `meeting-analyst` for meeting content, 90 days back. Transcripts only if a summary is thin. Skip automated mail. Each worker drafts `client.md`, `decisions.md`, `internal.md`, and one `project.md` per workstream into the scratchpad, not `clients/`. Every line carries a source tag. Merge with existing seed lines marked `[src: claude.ai memory]`: each is verified against a newer source (retag it) or replaced; unverifiable lines are listed, not kept silently. Also list conflicts, low-confidence items, and mistranscription suspects.
3. **Per-client review, core first.** Present proposed files plus the conflict, low-confidence, and suspect lists. Write only after Matt approves that client; one commit per client (`docs: bootstrap <slug> context`), shown with diff before committing, feature-branch rules do not apply to this workspace but never push.
4. **Repo CLAUDE.md.** For each client with a repo, write `../Repos/<repo>/CLAUDE.md` from `templates/repo-CLAUDE.md` (fill client slug, script prefix, shared libraries, quirks from the drafts; leave unknowns blank) and append `CLAUDE.md` to that repo's `.git/info/exclude`. Never commit it; confirm `git status` in the repo does not list it.

Stop after each client for review. Don't batch-write all thirteen.
