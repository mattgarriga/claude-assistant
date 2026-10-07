# Phase 0 guard_git.py test report 1
Harness: tests/tester_guard_git.py (155 cases, fresh temp repos, /usr/bin/python3 3.9.6). Builder suite: 29 tests OK. Script imports stdlib only (json, os, re, shlex, subprocess, sys).
All explicit criteria 1-8 PASS (incl. -C relative, cd relative, symlink into Repos, master/develop/release-1, all false positives).
Bypasses that WORK (not blocked): bash/sh/zsh -c (push, suitecloud, commit on main), eval, xargs, find -exec, $(git push) and backticks when not at command position start (echo $(git push)), (git push) in parens, quoted "git"/'git'/"suitecloud", \git, G=git; $G push, env -i / nice / timeout / sudo -u prefixes, { git push; }, if/for bodies, "! git push", git -c alias.p=push p, git send-pack, python os.system, npm run / yarn / pnpm exec / npm exec / npx -y / npx --yes suitecloud, git --git-dir=... commit, pushd, cd -- X, git -C=X / -CX commit, git checkout main && commit.
Blocked OK: double space, tab, newline, &, command/time/exec prefix, env FOO=1 git push, git -P/--no-pager push.
Not bypasses: uppercase (git is case sensitive).
