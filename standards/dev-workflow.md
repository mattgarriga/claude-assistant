# Dev Workflow

## Repos
- Location: `../Repos/` (sibling of this repo), granted via `additionalDirectories`.
- One git repo per client, each an SDF project. The path is recorded in that client's `client.md` (Tool IDs table, "Repo" row).
- Each client repo should have its own `CLAUDE.md` built from `templates/repo-CLAUDE.md` (client conventions, script prefixes, account quirks). Propose it; Matt approves before it's committed.

## What Claude can do
| Allowed | Not allowed |
|---|---|
| Read any client repo | Push, merge, rebase onto shared branches, force anything |
| Create feature branches | Commit to main, master, develop, or release branches (hook-enforced) |
| Edit files and commit on feature branches | `suitecloud` CLI of any kind (no deploys, no account connections) |
| Run local lint, unit tests, static analysis | `git reset --hard`, deleting branches, rewriting history |

Matt pushes and merges. Matt or Invitra deploys.

## Conventions (confirmed by Matt 2026-10-06)
- Branch: `feature/<short-slug>` or `fix/<short-slug>`; include the Smartsheet ticket ID when one exists.
- Commit: `<type>: <summary>` (types: feat, fix, refactor, docs, test, chore). No emojis, no em dashes.
- Before any commit: show Matt the diff summary and proposed message.

## Every code task
1. Read `standards/coding-standards.md`, the repo's `CLAUDE.md`, the client's `client.md`, and relevant `knowledge/`.
2. Check `git status` and current branch. If on a protected branch, create a feature branch first.
3. Work, then self-review with the code-review skill before showing Matt.
4. Never put credentials, account IDs, or tokens in code or commits.
