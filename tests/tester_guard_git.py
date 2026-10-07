#!/usr/bin/env python3
"""Independent tester harness for scripts/guard_git.py. Fresh temp repos."""
import json, os, subprocess, sys, tempfile

GUARD = "/Users/mgarriga/executive-assistant/scripts/guard_git.py"
PY = sys.argv[1] if len(sys.argv) > 1 else "/usr/bin/python3"
SC = "suite" + "cloud"
GP = "git " + "push"

root = os.path.realpath(tempfile.mkdtemp())
ws = os.path.join(root, "ws"); repos = os.path.join(root, "Repos")
os.makedirs(ws); os.makedirs(repos)

def mk(path, branch):
    os.makedirs(path, exist_ok=True)
    subprocess.run(["git", "init", "-q", "-b", branch, path], check=True)
    subprocess.run(["git", "-C", path, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "i"], check=True)

mk(ws, "main")
for n, b in [("rmain", "main"), ("rfeat", "feature/x"), ("rmaster", "master"), ("rdev", "develop"), ("rrel", "release-1"), ("rfix", "fix/y")]:
    mk(os.path.join(repos, n), b)
elsewhere = os.path.join(root, "else"); os.makedirs(elsewhere)
mk(os.path.join(root, "outside"), "main")

def run(cmd, cwd=None):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=ws)
    p = subprocess.run([PY, GUARD], input=json.dumps({"tool_input": {"command": cmd}, "cwd": cwd or ws}),
                       capture_output=True, text=True, env=env)
    return p.returncode

R = lambda n: os.path.join(repos, n)
cases = []  # (label, cmd, cwd, expect_block, is_bypass_probe)
def c(label, cmd, exp, cwd=None, probe=False): cases.append((label, cmd, cwd, exp, probe))

# 1,2,5,8
c("1 commit main under Repos", "git commit -m x", True, R("rmain"))
c("2 commit feature under Repos", "git commit -m x", False, R("rfeat"))
c("2b commit fix/ under Repos", "git commit -m x", False, R("rfix"))
c("5 commit main in workspace", "git commit -m x", False, ws)
c("5b commit main outside repo", "git commit -m x", False, os.path.join(root, "outside"))
c("8 master", "git commit -m x", True, R("rmaster"))
c("8 develop", "git commit -m x", True, R("rdev"))
c("8 release-1", "git commit -m x", True, R("rrel"))
c("8 cd && commit main", f"cd {R('rmain')} && git commit -m x", True, elsewhere)
c("8 cd && commit feature", f"cd {R('rfeat')} && git commit -m x", False, elsewhere)
c("8 -C abs main", f"git -C {R('rmain')} commit -m x", True, elsewhere)
c("8 -C relative main", "git -C ../Repos/rmain commit -m x", True, ws)
c("8 -C relative from elsewhere", "git -C ../Repos/rmain commit -m x", True, os.path.join(repos))
c("8 cd relative", "cd ../Repos/rmain && git commit -am x", True, ws)
c("8 commit -a main", "git commit -am x", True, R("rmain"))
c("8 commit --amend main", "git commit --amend --no-edit", True, R("rmain"))
c("8 git add && commit main", "git add -A && git commit -m x", True, R("rmain"))
c("8 workspace -C to main repo from ws", f"git -C {R('rmain')} commit -m x", True, ws)
# 3
for l, cmd in [("push", GP), ("push origin", GP + " origin main"), ("-C push", "git -C x push"), ("env push", "FOO=1 " + GP),
               ("&& push", "ls && " + GP), ("; push", "ls; " + GP), ("| push", "echo a | " + GP), ("-c push", "git -c a=b push"),
               ("--git-dir push", "git --git-dir=.git push"), ("newline push", "ls\n" + GP), ("subshell push", "(" + GP + ")"),
               ("sudo push", "sudo " + GP), ("abs git push", "/usr/bin/git push"), ("|| push", "false || " + GP)]:
    c("3 " + l, cmd, True)
# 4
for l, cmd in [("bare", SC + " deploy"), ("npx", "npx " + SC + " project:deploy"), ("abs", "/usr/local/bin/" + SC + " x"),
               ("&&", "cd a && " + SC + " x"), ("env", "A=1 " + SC + " x"), ("npx -y", "npx -y @oracle/" + SC + "-cli x"),
               ("npm exec", "npm exec " + SC + " x"), ("npx --yes", "npx --yes " + SC + " x")]:
    c("4 " + l, cmd, True)
# 6
for l, cmd in [("merge", "git merge feature/x"), ("rebase", "git rebase main"), ("reset hard", "git reset --hard HEAD~1"),
               ("branch -D", "git branch -D foo"), ("branch -d", "git branch -d foo"), ("push --force", "git push --force"),
               ("push -f", "git push -f origin x"), ("push --force-with-lease", "git push --force-with-lease"),
               ("branch --delete", "git branch --delete foo"), ("branch -D combined", "git branch -fD foo"),
               ("-C merge", "git -C /x merge y"), ("rebase -i", "git rebase -i HEAD~2")]:
    c("6 " + l, cmd, True)
# 7
c("7 heredoc prose", f"cat <<'EOF'\nrun {SC} and {GP} later\nEOF", False)
c("7 heredoc then git commit msg", f"git commit -m \"$(cat <<'EOF'\nfix {GP} and {SC} merge\nEOF\n)\"", False, R("rfeat"))
c("7 echo push", f'echo "{GP}"', False)
c("7 echo suitecloud", f'echo "{SC} deploy"', False)
c("7 commit fix push handling", 'git commit -m "fix push handling"', False, R("rfeat"))
c("7 log --grep=merge", "git log --grep=merge", False)
c("7 rm --force", "rm --force x", False)
c("7 grep suitecloud", f"grep -r {SC} .", False)
c("7 git status", "git status", False)
c("7 git diff", "git diff", False)
c("7 git checkout -b", "git checkout -b feature/z", False)
c("7 git branch list", "git branch -a", False)
c("7 git stash", "git stash", False)
c("7 git pull", "git pull", False)
c("7 git fetch", "git fetch", False)
c("7 git log --merges", "git log --merges", False)
c("7 git commit msg with merge word", 'git commit -m "merge notes"', False, R("rfeat"))
c("7 git commit msg mentions push; ", f'git commit -m "x; {GP}"', False, R("rfeat"))
c("7 git commit msg 'git push' quoted", f"git commit -m 'docs: explain {GP}'", False, R("rfeat"))
c("7 git log --oneline -n", "git log --oneline -n 5", False)
c("7 git remote -v", "git remote -v", False)
c("7 python script mentioning", f"python3 -c \"print('{GP}')\"", False)
c("7 ls Repos suitecloud-named file", "ls my-" + SC + "-notes.md", False)
c("7 cat path with suitecloud dir", "cat docs/" + SC + ".md", False)
c("7 git commit on main msg mentions suitecloud", f'git commit -m "no {SC}"', True, R("rmain"))
# 9 bypass probes
c("9 bash -c push", f"bash -c '{GP}'", True, probe=True)
c("9 sh -c push", f'sh -c "{GP}"', True, probe=True)
c("9 zsh -c push", f'zsh -c "{GP}"', True, probe=True)
c("9 bash -c suitecloud", f"bash -c '{SC} deploy'", True, probe=True)
c("9 sh -c suitecloud", f'sh -c "{SC} deploy"', True, probe=True)
c("9 eval push", f'eval "{GP}"', True, probe=True)
c("9 eval suitecloud", f'eval "{SC} x"', True, probe=True)
c("9 xargs push", "echo x | xargs git push", True, probe=True)
c("9 xargs suitecloud", f"echo x | xargs {SC}", True, probe=True)
c("9 find -exec push", f"find . -exec git push \\;", True, probe=True)
c("9 $() push", f"echo $({GP})", True, probe=True)
c("9 backtick push", f"echo `{GP}`", True, probe=True)
c("9 double space push", "git  push", True, probe=True)
c("9 tab push", "git\tpush", True, probe=True)
c("9 uppercase PUSH", "git PUSH", True, probe=True)  # git is case sensitive; this is not a real bypass
c("9 uppercase GIT push", "GIT push", True, probe=True)
c("9 newline push", "echo a\n" + GP, True, probe=True)
c("9 backslash-newline push", "git \\\npush", True, probe=True)
c("9 quoted subcommand", 'git "push"', True, probe=True)
c("9 quoted git", '"git" push', True, probe=True)
c("9 quoted suitecloud", '"' + SC + '" x', True, probe=True)
c("9 single-quoted git", "'git' push", True, probe=True)
c("9 backslash git", "\\git push", True, probe=True)
c("9 var indirection", "G=git; $G push", True, probe=True)
c("9 alias-like command prefix", "command git push", True, probe=True)
c("9 env -i git push", "env -i git push", True, probe=True)
c("9 env VAR git push", "env FOO=1 git push", True, probe=True)
c("9 time git push", "time git push", True, probe=True)
c("9 nice git push", "nice git push", True, probe=True)
c("9 timeout git push", "timeout 5 git push", True, probe=True)
c("9 sudo -u git push", "sudo -u bob git push", True, probe=True)
c("9 exec git push", "exec git push", True, probe=True)
c("9 { git push; }", "{ " + GP + "; }", True, probe=True)
c("9 if then push", "if true; then " + GP + "; fi", True, probe=True)
c("9 for do push", "for i in 1; do " + GP + "; done", True, probe=True)
c("9 ! git push", "! " + GP, True, probe=True)
c("9 background & push", "sleep 1 & " + GP, True, probe=True)
c("9 &-then push", "ls &\n" + GP, True, probe=True)
c("9 git alias via -c", "git -c alias.p=push p", True, probe=True)
c("9 git --no-pager push", "git --no-pager push", True, probe=True)
c("9 git -P push", "git -P push", True, probe=True)
c("9 git -C with spaces push", 'git -C "my dir" push', True, probe=True)
c("9 git --exec-path= push", "git --exec-path=/x push", True, probe=True)
c("9 git push via refspec delete", "git send-pack x", True, probe=True)
c("9 python subprocess push", f"python3 -c \"import os;os.system('{GP}')\"", True, probe=True)
c("9 script file run", "bash script.sh", False, probe=True)  # unknowable, informational
c("9 relative path ./suitecloud", "./" + SC + " x", True, probe=True)
c("9 node_modules/.bin", "node_modules/.bin/" + SC + " x", True, probe=True)
c("9 npx pkg@ver suitecloud", "npx @oracle/" + SC + "-cli@1 x", True, probe=True)
c("9 npm run suitecloud", "npm run " + SC + "", True, probe=True)
c("9 yarn suitecloud", "yarn " + SC + " x", True, probe=True)
c("9 pnpm exec suitecloud", "pnpm exec " + SC + " x", True, probe=True)
c("9 git reset --hard via -C", "git -C x reset --hard", True, probe=True)
c("9 git reset --merge-ish", "git reset --keep HEAD~1", False, probe=True)
c("9 git commit main bash -c", f"bash -c 'git commit -m x'", True, R("rmain"), probe=True)
c("9 git commit main subshell", "(git commit -m x)", True, R("rmain"), probe=True)
c("9 git commit main env", "FOO=1 git commit -m x", True, R("rmain"), probe=True)
c("9 git commit main -c", "git -c user.name=a commit -m x", True, R("rmain"), probe=True)
c("9 git commit main --git-dir", f"git --git-dir={R('rmain')}/.git --work-tree={R('rmain')} commit -m x", True, ws, probe=True)
c("9 git commit main -C relative nested", "cd .. && git -C Repos/rmain commit -m x", True, ws, probe=True)
c("9 git commit main pushd", f"pushd {R('rmain')} && git commit -m x", True, elsewhere, probe=True)
c("9 git commit main cd -- ", f"cd -- {R('rmain')} && git commit -m x", True, elsewhere, probe=True)
c("9 git commit main cd quoted", f"cd '{R('rmain')}' && git commit -m x", True, elsewhere, probe=True)
c("9 git commit main cd ~ style", "cd ../Repos/rmain; git commit -m x", True, ws, probe=True)
c("9 git commit main newline", f"cd {R('rmain')}\ngit commit -m x", True, elsewhere, probe=True)
c("9 git commit main -C=", f"git -C={R('rmain')} commit", True, elsewhere, probe=True)
c("9 git commit main -C joined", f"git -C{R('rmain')} commit -m x", True, elsewhere, probe=True)
c("9 git commit-tree", "git commit-tree HEAD^{tree}", True, R("rmain"), probe=True)
c("9 git commit main symlink", None, True, probe=True)  # placeholder replaced below
c("9 git switch + commit feature then main", f"cd {R('rmain')} && git switch -c feature/q && git commit -m x", False, probe=True)
c("9 git checkout main && commit (switches to main)", f"cd {R('rfeat')} && git checkout main && git commit -m x", True, probe=True)
c("9 git commit with -m 'a && b'", 'git commit -m "a && b"', True, R("rmain"), probe=True)
c("9 git commit -m with ;", 'git commit -m "a; b"', True, R("rmain"), probe=True)
c("9 echo then commit ||", 'false || git commit -m x', True, R("rmain"), probe=True)
c("9 git commit | cat", 'git commit -m x | cat', True, R("rmain"), probe=True)
c("9 git commit & bg", 'git commit -m x &', True, R("rmain"), probe=True)
c("9 commit in $(cd)", f"echo $(cd {R('rmain')} && git commit -m x)", True, elsewhere, probe=True)
c("9 git commit: ws repo to Repos via cd .. glitch", f"cd {R('rfeat')} && cd ../rmain && git commit -m x", True, ws, probe=True)

# symlink case: ws/link -> Repos/rmain
link = os.path.join(root, "linkmain"); os.symlink(R("rmain"), link)
cases = [x for x in cases if x[1] is not None]
cases.append(("9 symlink into Repos main", "git commit -m x", link, True, True))

fails = []
for label, cmd, cwd, exp, probe in cases:
    rc = run(cmd, cwd)
    blocked = rc == 2
    ok = blocked == exp and rc in (0, 2)
    if not ok:
        fails.append((label, cmd, cwd, exp, rc, probe))
print(f"python={PY} total={len(cases)} fail={len(fails)}")
for label, cmd, cwd, exp, rc, probe in fails:
    print(f"FAIL [{'probe' if probe else 'criteria'}] {label}: expected {'BLOCK' if exp else 'ALLOW'} got rc={rc} cmd={cmd!r}")
