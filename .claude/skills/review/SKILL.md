---
name: review
description: Review NetSuite SuiteScript, SDF objects, or a git diff against Ethos coding standards. Use for "review this script," "check this PR/branch," or before any commit Claude makes.
argument-hint: [client] [details]
---
# Code Review
Reading goes to the `code-reviewer` agent; you reason over its table.

1. Resolve the client and repo path (`client.md`, Repo row). Repo missing from `../Repos`: tell Matt and ask for the clone URL; never guess.
2. Read `standards/dev-workflow.md` and the repo `CLAUDE.md`. Note the branch and `git status` (read-only). Dirty or mid-ticket checkout: stop and ask. Default offer: commit WIP on its branch, checkout main, create the new branch.
3. Delegate to `code-reviewer` with the repo, branch or diff range, and any SDD or ticket. Baseline is the conventions file (via `standards/coding-standards.md`) section 10.4 pre-handoff checklist. If the conventions file is missing, stop and tell Matt.
4. Add your own pass on correctness against the requirement and script type fit (SDD Section 4 gate).
5. Output: table Line / Severity (Blocker, Fix, Nit) / Finding / Section / Suggested change. Every finding cites a conventions section number. One-line verdict. Offer to apply fixes on a feature branch (`feature/EBS-####`, `hotfix/EBS-####`, `bugfix/<desc>`; commits `type: summary`; show diff and message before committing).

Link EBS-#### to its Ethos Development Tracker row (Row ID EBS.####) when the ticket matters to the finding.
