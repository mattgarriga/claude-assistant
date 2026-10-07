# Ethos Coding Standards

Single source: the ethos-dev plugin's conventions file, installed at
`~/.claude/plugins/marketplaces/local-desktop-app-uploads/ethos-dev/conventions/ethos-suitescript-conventions.md`.
Read that file for every dev task (review, debug, query, test plan, handoff). Section 0 holds the resolved decisions; sections 1 to 11 the standards. Cite sections by number in findings.

If the file is missing (plugin moved or reinstalled), stop and tell Matt. Never fall back to memory or older copies.

## Workspace overrides
| Topic | Conventions file says | This workspace uses | Why |
|---|---|---|---|
| Commit message format (decision 12) | `EBS-####: short imperative summary` | `<type>: <summary>` (feat, fix, refactor, docs, test, chore) | Matt's call 2026-10-07. Branch names still follow decision 12. Flag to Matt if he wants decision 12 changed in the plugin so the team matches |
| Deploys (decision 11) | SuiteCloud CLI validate and deploy | Never from this workspace | Matt or Invitra deploys. Hook-enforced |
