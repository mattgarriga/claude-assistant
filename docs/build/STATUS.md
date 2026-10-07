# Build Status and Game Plan (resume point)

Paused 2026-10-07 at Matt's request (usage). On resume: read this file, then `plan.md` and `decisions-log.md`, then run the game plan below in order. Commit explicit paths only while builders are working (never `git commit -a`).

## Done
| Area | State |
|---|---|
| Phase 0: connectors, deny rules, guard_git, guard_auth (API key block), toolchain | Built, tested |
| Phase 1: 2026 templates in repo, cleaned SDD (Letter) and One-Pager (white fills), branding.md, format files, skills merged to short names | Built, tested |
| Phase 2: lib/docx template-fill engine, 6 types, check.js, TBD fee cells, Lucid link under 4.1, pagination | Built, tested |
| Phases 4, 5: dev and PM skills, agent routing, /agenda /invitra /sow-review /wrap, Action Log sheet (5639928991141764) | Built |
| Agents: scout (now Sonnet), meeting-analyst, doc-producer, qa-gate, code-reviewer | Built, tested |
| Phase 7: lint hooks, secret scan, /health-check, README, weekly Fri 3pm context sweep scheduled | Built |
| Phase 6: discovery table confirmed; core 7 bootstrap drafts in `state/bootstrap/<slug>/` (gitignored, not yet written to clients/) | Drafted |

## Changes 2026-10-07 (latest)
- Repo renamed to claude-assistant.
- .docx outputs approved (step 3 done).
- Bulk bootstrap dropped (steps 4 and 5): seed each client as work happens via /client-update with SharePoint folders from Matt. Core 7 drafts stay in state/bootstrap/ as optional reference.
- Remaining work runs only when Matt asks, favoring low-usage steps.

## Game plan for next window (in order)
| # | Step | Who | Est. usage |
|---|---|---|---|
| 1 | **Urgent flags** from bootstrap drafts (see below). Matt reads, decides | Matt | none |
| 2 | Standards sign-off: walk the 20 NEEDS MATT rows in `phase1-standards-diff.md` via 5 question rounds; apply changes | senior | low |
| 3 | Matt opens real .docx outputs in `lib/docx/out/` (folder already opened in Finder) and approves or lists fixes. PNGs in docs/build/renders are only previews for the tester | Matt | none |
| 4 | Phase 6.3: per-client review of the 7 core drafts, core order HUT, Cala, 4P, CommSell, IMI, CORE, Cerio. Show review.md top items plus a file summary; Matt approves; copy to clients/<slug>/; one commit per client | senior + Matt | medium |
| 5 | Re-run bootstrap drafts for the other 6 (TSS, Boxes 4 U, EVgo, LSN, ConcertAI, Hammitt). Stopped mid-run; prompts are in this session's history, same template as core. Then review and write | agents | high |
| 6 | Phase 3a live tests with Matt judging: /recap on "HUT x Ethos: Weekly Status Meeting" 2026-10-06 (Read AI 01M48SB3C19P2T4VG2BWJAD7R0, client-facing); /recap internal on HUT Internal Status 2026-10-06; /email reply to a thread Matt picks from the 5 candidates below; /review-design on HUT 3D Flight Cost SDD; /flow rebuild of 3D Flight into a "Claude Test" Lucid folder | senior + Matt | medium |
| 7 | Phase 3b: /onepager, /sdd, /sow on real examples Matt picks | senior + Matt | medium |
| 8 | Phase 4 tests on ../Repos/cerio and imi (/review, /debug with a real past error, /query); Phase 5 tests (/raide, /tasks, /status, /devboard, /today, /inbox, /agenda) with preview-only writes | senior + Matt | medium |
| 9 | /health-check run; final commit; one-paragraph summary | senior | low |

## Urgent flags surfaced by bootstrap (Matt)
1. CommSell: a 2026-07-14 CommSell status recap with budget metrics went to CORE recipients and a gocustomer.ai address under a Spark thread subject (details in `state/bootstrap/commsel/review.md`).
2. Credentials in email: CommSell thread with a Bitwarden credential link; CORE production credentials doc shared 2026-09-28; HUT PrintNode key in a OneDrive One-Pager. Locations only, in each review.md.
3. 4P NetSuite account number recorded in the 4P client.md draft: keep or drop.

## Email test candidates (pick one)
| # | From | Subject | Ask |
|---|---|---|---|
| 1 | Sarah Lippi (FFB Financial) | SFTP Setup and BAI2 Download Question | Schedule a 3-way call |
| 2 | Brenda Lim (Cala Health) | URGENT: Product Category missing for kIQ Plus items | Confirm accounting setup |
| 3 | Mena Her (Riveron/Cerio) | NetSuite JE Import Template | Create JE CSV import template |
| 4 | D'Andre Sanders (Ethos) | New Estimate Request: Cala Revenue reconciliation | Review Invitra ORR test findings |
| 5 | Nicholas (CommSell) | Loop Exchange Order Walkthrough | Confirm Thursday 2 to 4 PM CST |

## Still on Matt's list
- DONE 2026-10-07: managed-settings.json installed; /health-check all PASS (restart app to apply).
- Answer the engine and standards items as they come up in steps 2 and 3.
