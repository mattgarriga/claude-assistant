# Phase 1 streams B and C test report 1

| Check | Result | Evidence | Fix needed |
|---|---|---|---|
| 1 commands gone, skill names/descriptions | PASS | .claude/commands absent; 24 skill folders, name equals folder, description in all | none |
| 2 CLAUDE.md table maps to skills | PASS | 23 command rows incl. /co, /health-check all map to folders; only client-context unlisted | none |
| 3 stale names | PASS | only hit is agent name code-reviewer (not the old skill); no hits for other names | none |
| 4 sow-format, sdd 4.4, one-pager, recap | PASS | 5 assumptions match sow1.docx text exactly; PRICING rule, no Document Control/address header, diagrams-only Process Overview, signer rules present; SDD 4.4 matches decision; section orders match template dumps | none |
| 5 lint_voice on changed md | PASS | all changed md, agents, and all 24 SKILL.md exit 0 | none |
| 6 agents | PASS | scout haiku-4-5-20251001, read-only tool names only (execute_discussions_read is a read tool); qa-gate Read/Glob/Grep; code-reviewer no Write/Edit (has Bash, within spec); meeting-analyst read-only; doc-producer sonnet; design-reviewer claude-opus-5-5; YAML valid | none |
| 7 unittest + secret scan | PASS | 59 tests OK; 5 fake secrets flagged; 6 benign strings (ids, SHA, URL, prose, signature) not flagged | none |
| 8 hook_lint_outputs | PASS | em dash md: exit 0 + additionalContext; secret: exit 2; outside path: exit 0 silent; draft banned phrase: warn; draft secret: exit 2; signature only: silent; docx em dash: warn | none |
| 9 settings.json | PASS | valid JSON; guard_git (Bash), guard_auth (SessionStart and Bash/Write/Edit/NotebookEdit), hook_lint (3 draft tools Pre, Write/Edit Post); env blanks present; 35 deny | none |
| 10 health-check skill | PASS | 5 steps cover connectors, denial tests, hooks, auth, conventions; fake IDs only | none |

Stream B: PASS. Stream C: PASS. Overall PASS.
Note: test hook runs briefly created and removed an empty clients/hut/projects/x/outputs dir.
