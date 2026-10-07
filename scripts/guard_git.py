#!/usr/bin/env python3
"""PreToolUse hook for Bash. Exit 2 blocks the tool call and shows stderr to Claude.

Global (any repo): blocks the NetSuite CLI, git merge/send-pack, and history
rewrites (reset --hard, rebase, filter-branch, branch -d/-D, and --force/-f on git
push, checkout, branch, reset, clean). git push is blocked everywhere except as
described under "Push" below. `git -c alias.X=...` is blocked when the alias
value contains push/merge/rebase/filter-branch or starts with `!`.

How matching works: heredoc bodies are stripped, then the command is tokenized
shell-style (quotes and backslashes removed from words, separators ; && || | & newline
( ) and backticks start new commands, $( ) inside double quotes is scanned too). For each
simple command the wrapper prefix is peeled (env assignments, keywords such as
then/do/else/!/{ , env, nice, timeout, sudo, xargs, find -exec, nohup, command, time,
exec, stdbuf), then the program is judged. Git checks use the real subcommand (first
non-option token, skipping -C <path>, -c k=v, --git-dir, --work-tree and similar).
`bash|sh|zsh|dash -c <string>` and `eval <args>` are checked recursively. The NetSuite
CLI is caught as a program, or as an argument to npx/pnpx/bunx/npm/pnpm/yarn/node.
Prose in heredocs and quoted strings passes.

Scoped: blocks commits on protected branches (main, master, develop, dev, release*)
only when the target repo lives under the client repos directory, i.e. the resolved
"$CLAUDE_PROJECT_DIR/../Repos" (or ../Repos next to this script's parent repo if the
env var is unset). Commits in the workspace repo itself, or any repo outside that
directory, are allowed. The target repo comes from `cd`/`pushd` before the commit,
`git -C`, `--git-dir`, `--work-tree`, resolved against the hook's cwd. Within one
command, `git checkout|switch <branch>` and `checkout -b|switch -c <new>` change the
branch the later commit is judged on. Client repo branches should be feature/,
hotfix/ or bugfix/; only the protected names above are blocked.

Push: allowed only for a repo under the client repos directory, and only when every
ref being pushed is a non-protected branch (or tag). Blocked: protected branches
(main, master, develop, dev, release*) on either side of a refspec, a bare push while
a protected branch is checked out, forced (+src, --force*, -f) or deleting (:dst,
--delete) refspecs, wildcard refspecs, --all/--mirror/--prune and any other flag not
in PUSH_FLAGS, `git -c remote.*/push.*/url.*` overrides, and any push where the target
repo cannot be resolved (including the workspace repo itself).

Known residual limits (a regex/tokenizer hook cannot cover these): variable indirection
(`G=git; $G push`), commands launched from inside other programs (python os.system,
node child_process, make targets, scripts run as `bash script.sh`), npm/yarn run
scripts that wrap the CLI, mixed-case tricks on case-insensitive tools. The deny rules
in .claude/settings.json are the second layer and must stay in place."""
import json, os, re, shlex, subprocess, sys

PROTECTED = {"main", "master", "develop", "dev"}
KEYWORDS = {"{", "}", "!", "then", "do", "else", "elif", "if", "while", "until"}
SHELLS = {"bash", "sh", "zsh", "dash", "ksh"}
RUNNERS = {"npx", "pnpx", "bunx", "npm", "pnpm", "yarn", "bun", "node", "corepack"}
GLOBAL_OPTS_WITH_ARG = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--super-prefix", "--config-env"}
FORCE_SUBS = {"push", "checkout", "branch", "reset", "clean"}
PUSH_FLAGS = {"-u", "--set-upstream", "-v", "--verbose", "-q", "--quiet", "-n", "--dry-run",
              "--no-verify", "--follow-tags", "--progress"}
ALIAS_BAD = re.compile(r"\b(push|merge|rebase|filter-branch)\b")


def block(msg):
    print(f"BLOCKED by guard_git: {msg}", file=sys.stderr)
    sys.exit(2)


def strip_heredocs(text):
    """Remove heredoc bodies (and terminators) so prose inside them is never matched."""
    out, pending = [], []
    for line in text.split("\n"):
        if pending:
            if line.strip() == pending[0]:
                pending.pop(0)
            continue
        out.append(line)
        pending = [m.group(1) for m in re.finditer(r"<<(?!<)-?\s*['\"]?(\w+)['\"]?", line)]
    return "\n".join(out)


def lex(text):
    """Split text into simple commands (lists of unquoted words). Returns (cmds, subs),
    where subs are $( ) and backtick bodies found inside double quotes."""
    cmds, cur, word, subs = [], [], [], []
    inword = False
    i, n = 0, len(text)

    def endword():
        nonlocal word, inword
        if inword:
            cur.append("".join(word))
        word, inword = [], False

    def endcmd():
        nonlocal cur
        endword()
        if cur:
            cmds.append(cur)
        cur = []

    while i < n:
        ch = text[i]
        if ch == "\\":
            if i + 1 < n:
                if text[i + 1] != "\n":
                    word.append(text[i + 1])
                    inword = True
                i += 2
            else:
                i += 1
        elif ch == "'":
            j = text.find("'", i + 1)
            j = n if j < 0 else j
            word.append(text[i + 1:j])
            inword = True
            i = j + 1
        elif ch == '"':
            inword = True
            i += 1
            while i < n and text[i] != '"':
                c = text[i]
                if c == "\\" and i + 1 < n:
                    word.append(text[i + 1] if text[i + 1] in '"\\$`' else c + text[i + 1])
                    i += 2
                elif c == "$" and text[i + 1:i + 2] == "(":
                    depth, j = 1, i + 2
                    while j < n and depth:
                        depth += {"(": 1, ")": -1}.get(text[j], 0)
                        j += 1
                    subs.append(text[i + 2:j - 1])
                    word.append(text[i:j])
                    i = j
                elif c == "`":
                    j = text.find("`", i + 1)
                    j = n if j < 0 else j
                    subs.append(text[i + 1:j])
                    word.append(text[i:j + 1])
                    i = j + 1
                else:
                    word.append(c)
                    i += 1
            i += 1
        elif ch in " \t":
            endword()
            i += 1
        elif ch in "\n;&|()`":
            endcmd()
            i += 1
        else:
            word.append(ch)
            inword = True
            i += 1
    endcmd()
    return cmds, subs


def is_sc(tok):
    t = re.sub(r"^@oracle/", "", tok).rsplit("/", 1)[-1]
    return re.fullmatch(r"suite" + r"cloud(-cli)?(@\S+)?", t) is not None


def drop_flags(words, with_arg=()):
    """Drop leading -flags (and the argument of flags in with_arg)."""
    while words and words[0].startswith("-") and words[0] != "-":
        takes = words[0] in with_arg
        words = words[2:] if takes else words[1:]
    return words


def unwrap(words):
    """Peel keywords, env assignments and wrapper programs; return words from the real program."""
    while words:
        w = words[0]
        b = os.path.basename(w)
        if w in KEYWORDS or re.match(r"^[A-Za-z_]\w*=", w):
            words = words[1:]
        elif b in ("command", "exec", "nohup", "time", "builtin"):
            words = drop_flags(words[1:])
        elif b == "env":
            words = words[1:]
            while words and (words[0].startswith("-") or re.match(r"^[A-Za-z_]\w*=", words[0])):
                words = words[2:] if words[0] in ("-u", "-C", "-S", "-P") else words[1:]
        elif b == "nice":
            words = drop_flags(words[1:], ("-n", "--adjustment"))
        elif b == "timeout":
            words = drop_flags(words[1:], ("-s", "-k", "--signal", "--kill-after"))
            if words and re.match(r"^[\d.]+[smhd]?$", words[0]):
                words = words[1:]
        elif b == "sudo":
            words = drop_flags(words[1:], ("-u", "-g", "-h", "-p", "-C", "-D", "-r", "-t", "-U", "-R", "-T"))
        elif b == "xargs":
            words = drop_flags(words[1:], ("-n", "-I", "-L", "-P", "-d", "-E", "-s", "-a"))
        elif b == "stdbuf":
            words = drop_flags(words[1:], ("-i", "-o", "-e"))
        elif b == "find":
            idx = [k for k, x in enumerate(words) if x in ("-exec", "-execdir", "-ok", "-okdir")]
            if not idx:
                break
            words = words[idx[0] + 1:]
        else:
            break
    return words


def repos_dir():
    proj = os.environ.get("CLAUDE_PROJECT_DIR")
    if not proj:
        proj = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.realpath(os.path.join(proj, "..", "Repos"))


def resolve(base, path):
    return os.path.normpath(os.path.join(base, os.path.expanduser(path)))


def under(child, parent):
    try:
        return os.path.commonpath([child, parent]) == parent
    except ValueError:
        return False


def git_run(prefix, args):
    try:
        r = subprocess.run(["git"] + prefix + args, capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def git_ok(prefix, args):
    try:
        return subprocess.run(["git"] + prefix + args, capture_output=True).returncode == 0
    except Exception:
        return False


def is_protected(br):
    return bool(br) and (br in PROTECTED or br.startswith("release"))


def is_force(arg):
    return arg.startswith("--force") or re.match(r"^-[A-Za-z]*f[A-Za-z]*$", arg) is not None


def parse_git(args):
    """Return (opts, sub, subargs) skipping global git options."""
    opts = {"C": [], "c": [], "git_dir": None, "work_tree": None}
    i = 0
    while i < len(args):
        t = args[i]
        nxt = args[i + 1] if i + 1 < len(args) else ""
        if t == "-C":
            opts["C"].append(nxt)
            i += 2
        elif t.startswith("-C") and len(t) > 2:
            opts["C"].append(t[2:].lstrip("="))
            i += 1
        elif t == "-c":
            opts["c"].append(nxt)
            i += 2
        elif t.startswith("--git-dir="):
            opts["git_dir"] = t.split("=", 1)[1]
            i += 1
        elif t == "--git-dir":
            opts["git_dir"] = nxt
            i += 2
        elif t.startswith("--work-tree="):
            opts["work_tree"] = t.split("=", 1)[1]
            i += 1
        elif t == "--work-tree":
            opts["work_tree"] = nxt
            i += 2
        elif t in GLOBAL_OPTS_WITH_ARG:
            i += 2
        elif t.startswith("-"):
            i += 1
        else:
            return opts, t, args[i + 1:]
    return opts, "", []


def locate(opts, base):
    """Return (key_dir, prefix) for running git against the target repo, or (None, None)."""
    repo = base
    for p in opts["C"]:
        repo = resolve(repo, p)
    if opts["git_dir"]:
        gd = resolve(repo, opts["git_dir"])
        if opts["work_tree"]:
            repo = resolve(repo, opts["work_tree"])
        else:
            repo = os.path.dirname(gd) if os.path.basename(gd) == ".git" else gd
        return os.path.realpath(repo), ["--git-dir", gd]
    top = git_run(["-C", repo], ["rev-parse", "--show-toplevel"])
    if not top:
        return None, None
    top = os.path.realpath(top)
    return top, ["-C", top]


def push_check(opts, sargs, state):
    """Allow a push only for non-protected branches in a repo under REPOS; else block."""
    for kv in opts["c"]:
        if kv.partition("=")[0].lower().startswith(("remote.", "push.", "url.", "core.sshcommand", "core.hookspath")):
            block("git -c overrides of remote/push/url settings are not allowed on push.")
    key, prefix = locate(opts, state["dir"])
    if not key or not under(key, REPOS):
        block("push is only allowed from a client repo under ../Repos, on a feature branch.")
    words = []
    for a in sargs:
        if a.startswith("-") and a != "-":
            if a not in PUSH_FLAGS:
                block(f"git push flag '{a}' is not allowed (no force, delete, all, or mirror pushes).")
            continue
        words.append(a)
    refspecs = words[1:]

    def current():
        return state["br"].get(key) or git_run(prefix, ["symbolic-ref", "--short", "HEAD"])

    def side_ok(name):
        name = current() if name == "HEAD" else re.sub(r"^refs/heads/", "", name)
        return bool(name) and not is_protected(name)

    if not refspecs:
        if not side_ok("HEAD"):
            block("pushing main, master, develop, dev, or release branches is not allowed. Push a feature/, hotfix/ or bugfix/ branch.")
        return
    for r in refspecs:
        if r.startswith(("+", ":")) or "*" in r or r.endswith(":"):
            block(f"refspec '{r}' is not allowed (force, delete, or wildcard).")
        if not all(side_ok(side) for side in r.split(":")):
            block("pushing main, master, develop, dev, or release branches is not allowed. Push a feature/, hotfix/ or bugfix/ branch.")


def git_check(args, state):
    opts, sub, sargs = parse_git(args)
    for kv in opts["c"]:
        key, _, val = kv.partition("=")
        if key.lower().startswith("alias.") and (val.startswith("!") or ALIAS_BAD.search(val)):
            block("git aliases that run push/merge/rewrite commands are not allowed.")
    if sub in ("merge", "send-pack"):
        block("merge is Matt's job.")
    if sub == "push":
        push_check(opts, sargs, state)
    if (sub in ("rebase", "filter-branch")
            or (sub == "reset" and "--hard" in sargs)
            or (sub == "branch" and any(a == "--delete" or re.match(r"^-[A-Za-z]*[dD][A-Za-z]*$", a) for a in sargs))):
        block("history rewrites, branch deletes, and force operations are not allowed.")
    if sub in FORCE_SUBS and any(is_force(a) for a in sargs):
        block("history rewrites, branch deletes, and force operations are not allowed.")

    if sub in ("checkout", "switch"):
        key, prefix = locate(opts, state["dir"])
        if key:
            newb, cand = None, None
            for k, a in enumerate(sargs):
                if a == "--":
                    break
                if a in ("-b", "-B", "-c", "-C") and k + 1 < len(sargs):
                    newb = sargs[k + 1]
                    break
                if not a.startswith("-") and cand is None:
                    cand = a
            if newb:
                state["br"][key] = newb
            elif cand and (is_protected(cand) or git_ok(prefix, ["show-ref", "--verify", "--quiet", "refs/heads/" + cand])):
                state["br"][key] = cand
    elif sub in ("commit", "commit-tree"):
        key, prefix = locate(opts, state["dir"])
        if not key or not under(key, REPOS):
            return
        br = state["br"].get(key) or git_run(prefix, ["symbolic-ref", "--short", "HEAD"]) \
            or git_run(prefix, ["rev-parse", "--abbrev-ref", "HEAD"])
        if is_protected(br):
            block(f"commits on protected branch '{br}' are not allowed. Create a feature/, hotfix/ or bugfix/ branch first.")


def analyze(words, state):
    words = unwrap(words)
    if not words:
        return
    prog, args = os.path.basename(words[0]), words[1:]
    if is_sc(words[0]) or (prog in RUNNERS and any(is_sc(a) for a in args)):
        block("suitecloud CLI is not allowed. No NetSuite connections or deploys from this workspace.")
    if prog in SHELLS:
        for k, a in enumerate(args):
            if a.startswith("-") and not a.startswith("--") and "c" in a[1:]:
                if k + 1 < len(args):
                    check(args[k + 1], state)
                break
            if not a.startswith("-"):
                break
    elif prog == "eval":
        check(" ".join(args), state)
    elif prog in ("cd", "pushd"):
        rest = [a for a in args if a not in ("--", "-L", "-P", "-e", "-@")]
        if not rest:
            state["dir"] = os.path.expanduser("~")
        elif rest[0] != "-":
            state["dir"] = resolve(state["dir"], rest[0])
    elif prog == "git":
        git_check(args, state)


def check(text, state):
    cmds, subs = lex(strip_heredocs(text))
    for words in cmds:
        analyze(words, state)
    for s in subs:
        check(s, state)


REPOS = repos_dir()

if __name__ == "__main__":
    data = json.load(sys.stdin)
    command = (data.get("tool_input") or {}).get("command", "") or ""
    start = data.get("cwd") or "."
    check(command, {"dir": os.path.realpath(start), "br": {}})
    sys.exit(0)
