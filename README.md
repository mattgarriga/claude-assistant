# Claude Assistant

Matt's Claude Code assistant for Ethos delivery work: recaps, SDDs, SOWs, change orders, one-pagers, process flows, email drafts, code review, and persistent per-client context. Run `claude` from this folder. Full rules live in `CLAUDE.md`.

## Daily commands
| Command | Use |
|---|---|
| `/today` | Daily brief: calendar, email, RAIDE items, time-blocked plan |
| `/recap` | Meeting recap from Read AI (client or internal) |
| `/inbox` | Inbox triage and reply drafts |
| `/agenda` | Status meeting talk track |
| `/status` | Project health for one client or all |

## Document commands
| Command | Use |
|---|---|
| `/sdd` | Solution Design Document (design interview first) |
| `/sow`, `/co` | Statement of Work or Change Order |
| `/onepager` | Development Request One-Pager |
| `/flow` | Lucid process flow |
| `/sow-review` | Read-only review of a SOW or CO |
| `/review-design` | Native-first, anti-overengineering pass |

## Dev commands
| Command | Use |
|---|---|
| `/review` | Review a script, branch, or diff |
| `/debug` | Root-cause an error or log |
| `/query` | SuiteQL and saved search formulas |
| `/test-plan` | Sandbox and UAT test cases |
| `/handoff` | Invitra task brief |
| `/ethos-dev:start` | Plugin: build work from a locked design |
| `/suitescript-migrator:migrate` | Plugin: migration audit and conversion |

## Write-back
Recaps, SDDs, and design talks write durable facts straight into a client's `decisions.md`, `project.md`, `client.md`, or `internal.md`, each with a source tag and a line in `state/context-log.md` so any change can be undone. You review the day's changes in `/eod`. Pricing, scope or budget changes, conflicts with existing facts, and anything inferred are queued in `state/writeback-queue.md` for approval instead.

## Add a client
Run `/new-client`. It scaffolds `clients/<slug>/` and adds the roster row. Check `clients/roster.md` first for aliases.

## Safety rails
| Rail | What it does |
|---|---|
| Never sends | Email and Teams are draft-only; send tools are denied |
| Smartsheet | Every write shows a mapped preview and needs your confirmation; deletes denied |
| Git guard | `scripts/guard_git.py` blocks protected-branch commits in `../Repos`, push, merge, and suitecloud |
| Auth guard | `scripts/guard_auth.py` blocks API-key use; login stays on your Claude account |
| NetSuite | Never connected from here |
| `/health-check` | Verifies connector deny rules and runs a fake-ID send test |

## Where things live
| Path | What |
|---|---|
| `standards/` | Voice, formats, tool rules, coding standards |
| `templates/` | Word templates and logo |
| `lib/docx/` | Node builder that fills the templates |
| `clients/<slug>/` | Client context, decisions, projects, outputs |
| `knowledge/` | Reusable solution patterns |
| `team/` | Team roster and Matt's profile |
| `state/` | Write-back queue |
| `docs/build/` | Build brief, plan, decisions log, status |

## Backup
Time Machine only. No remote.
