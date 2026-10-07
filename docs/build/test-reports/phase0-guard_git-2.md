# Phase 0 guard_git.py test report 2
Harnesses: tests/tester_guard_git.py (cycle 1, 155 cases), tests/tester_guard_git2.py (new, 80 cases, 8 informational). /usr/bin/python3 3.9.6. Builder suite tests/test_guard_git.py: 36 tests OK.

| Check | Result | Evidence | Fix needed |
|---|---|---|---|
| Builder suite | PASS | 36 OK | none |
| Cycle 1 suite | PASS | 155 total, 4 fail = the 4 accepted residuals only (git PUSH, GIT push, G=git; $G push, python os.system) | none |
| Docstring documents residuals | PASS (minor) | var indirection and "commands launched from inside other programs (python os.system...)" named. Uppercase only covered by vague "mixed-case tricks on case-insensitive tools" | optional: say "git is case sensitive, uppercase is not a real bypass" |
| Nested bash -c "sh -c 'git push'", triple nesting, bash -lc, bash -e -c, eval '...' | PASS | blocked | none |
| time -p, git -c k=v -C dir push, tab, `ls;git push`, backticks, xargs, find -exec, comment line then push, (cd && push), --force-with-lease, merge --ff-only, reset --hard, clean -fd | PASS | all blocked | none |
| cd /tmp then git -C (abs and relative) commit on Repos main | PASS | blocked | none |
| checkout main && commit under Repos | PASS | blocked | none |
| switch -c feature/EBS-1 && commit (cwd Repos main) and checkout -b | PASS | allowed | none |
| Heredoc prose then real push | PASS | blocked; prose-only heredoc, heredoc commit msg, python heredoc allowed | none |
| Legit commands (status/diff --stat, log, add+commit "handle merge of lines" on feature, npm test, node lib/docx/cli.js, lint_voice (+--design), grep "git push", pandoc, soffice, pdftoppm, sed, curl|jq, for loop lint, git -C Repos log, branch/-vv/--show-current, checkout --, clean -n, branch names containing -f/-d, commit msg mentioning git push) | PASS | ~50 cases, 0 false blocks | none |
| Performance | PASS | 100 runs each, median 31 ms (git status && diff pipeline in a repo), 33 ms (plain ls); max 40 ms. Limit 150 ms | none |
| Quirk: cd in subshell leaks scope | FAIL (minor, false block only) | `(cd Repos/rmain && git status); git commit -m x` from feature repo is BLOCKED. Needs a subshell cd into a Repos repo on a protected branch followed by a commit elsewhere; fail-safe direction | not required; builder may scope state per ( ) if cheap |
| Quirk: $( ) inside double quotes over-blocks | PASS (judged) | Only blocks if the substitution contains a real git push/commit-on-main etc. Common `commit -m "$(cat <<'EOF' ... EOF)"` and `"$(git log ...)"`, `"$(date)"`, `"$(cd docs && ls)"` all allowed | none |

Informational (accepted either way, reported as asked):
| Case | Result |
|---|---|
| eval $(echo git push) | ALLOWED (dynamic) |
| cat <<EOF \| bash with git push in body | ALLOWED (body stripped as heredoc) |
| bash <<EOF with git push in body | ALLOWED |
| echo 'git push' \| sh | ALLOWED |
| GIT_DIR=<Repos main>/.git git commit | ALLOWED |
| git pull | ALLOWED (can merge; push/merge rule says merge, builder may want to decide) |
| git config alias.p push (then git p) | ALLOWED |
| git commit --dry-run on main under Repos | BLOCKED (over-block, harmless) |

Piping or heredoc-feeding into a shell is a real bypass of the guard; settings.json deny rules remain the second layer. Recommend (optional) blocking `| bash/sh` and `<<` into a shell when the body contains git push.

Judgment on quirks: neither can plausibly block a normal command we run. Subshell leak needs a subshell cd into a protected-branch Repos repo followed by a commit in a different repo in the same call; rare and fail-safe.

Overall: PASS
