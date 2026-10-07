# Build Status (resume point)

If a session restarts, read this file, then `plan.md` and `decisions-log.md`, then continue from "Next".

## Done
- Phase 0 complete (connectors, deny rules, guard_git, guard_auth, toolchain, decisions)
- Plan reviewed end to end with Matt (Phases 0 to 7 plus added scope S1 to S11)

## In progress (2026-10-07, Matt away; build-all-you-can mode)
| Stream | Owner | Scope |
|---|---|---|
| A | app-builder | Phase 1.1 to 1.3: templates into repo, cleaned SDD/One-Pager copies, branding.md per-template spec, renders |
| B | done, committed e056965 | Phase 1.4 format and skill files, S1 merge commands into skills (tester PASS) |
| C | done, committed e056965 | Day-to-day agents (S2), secret scan (7.2), lint hooks registered (7.1), /health-check (7.3) (tester PASS) |
| D | app-builder | Phase 4 and 5 skill text, new /agenda /invitra /sow-review /wrap, Phase 6 bootstrap rewrite |

## Next
1. Tester pass on A, B, C. Senior review. Commit per stream.
2. Phase 2 engine (needs A's templates).
3. Phase 4 and 5 skill work (needs B's rename).
4. Phase 6.1 discovery table (read-only).

## Blocked on Matt (collect into one grouped question list)
- Phase 1.6 standards diff sign-off
- Phase 1.2 / Phase 2 render approvals
- 3a: confirm HUT client meeting, pick email thread
- Action Log columns before creating the sheet
- Weekly /client-update scheduled task creation
- Phase 6 discovery table and per-client approvals
- Run sudo managed-settings command; install migrator plugin
