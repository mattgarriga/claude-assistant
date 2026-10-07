#!/usr/bin/env python3
"""Independent tester harness for scripts/guard_auth.py. Run: /usr/bin/python3 tests/tester_guard_auth.py"""
import json, os, subprocess, sys, tempfile, time, statistics
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(ROOT, "scripts", "guard_auth.py")
PY = "/usr/bin/python3"
KEY = "sk-ant-" + "api03-FAKEFAKEFAKE"
HOST = "api.anthropic" + ".com"
BASE = {k: v for k, v in os.environ.items() if not k.startswith(("ANTHROPIC", "CLAUDE_CODE_USE"))}
res = []

def run(payload, env=None, home=None):
    e = dict(BASE); e.update(env or {})
    if home: e["HOME"] = home
    p = subprocess.run([PY, G], input=json.dumps(payload), capture_output=True, text=True, env=e)
    return p.returncode, p.stdout, p.stderr

def rec(name, ok, ev=""):
    res.append((name, ok, ev)); print(("PASS " if ok else "FAIL ") + name + ("  | " + ev if not ok else ""))

def bash(c): return run({"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": c}})[0]
def tool(t, path, text):
    k = {"Write": "content", "Edit": "new_string", "NotebookEdit": "new_source"}[t]
    pk = "notebook_path" if t == "NotebookEdit" else "file_path"
    return run({"hook_event_name": "PreToolUse", "tool_name": t, "tool_input": {pk: path, k: text}})[0]

# 1 SessionStart
SS = {"hook_event_name": "SessionStart"}
SECRET = "SECRETVALUE" + "12345"
for v in ["ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX", "CLAUDE_CODE_USE_FOUNDRY"]:
    val = KEY if "KEY" in v else SECRET
    rc, o, e = run(SS, {v: val})
    try: j = json.loads(o); ctx = j["hookSpecificOutput"]["additionalContext"]; ok = v in ctx
    except Exception: ok = False
    rec("SS finds " + v, rc == 0 and ok, o)
    rec("SS no secret leak " + v, val not in o and val not in e, "leak")
rc, o, e = run(SS, {"ANTHROPIC_BASE_URL": "https://proxy.example.net/x"})
rec("SS base url non-default", "proxy.example.net" in o and json.loads(o)["hookSpecificOutput"]["additionalContext"] != "")
rc, o, e = run(SS, {"ANTHROPIC_BASE_URL": "https://" + HOST})
rec("SS clean default base url", rc == 0 and o == "", o)
rc, o, e = run(SS, {"ANTHROPIC_BASE_URL": "https://" + HOST + "/"})
rec("SS default base url trailing slash clean", rc == 0 and o == "", o)
rc, o, e = run(SS, {"ANTHROPIC_API_KEY": "", "ANTHROPIC_AUTH_TOKEN": ""})
rec("SS empty strings clean", rc == 0 and o == "", o)
rc, o, e = run(SS, {"ANTHROPIC_API_KEY": "   "})
rec("SS whitespace key clean (info)", rc == 0 and o == "", o)
rc, o, e = run(SS)
rec("SS no env clean", rc == 0 and o == "" and e == "", o + e)
for where in ["home", "proj", "projlocal"]:
    with tempfile.TemporaryDirectory() as h, tempfile.TemporaryDirectory() as p:
        os.makedirs(h + "/.claude"); os.makedirs(p + "/.claude")
        f = {"home": h + "/.claude/settings.json", "proj": p + "/.claude/settings.json", "projlocal": p + "/.claude/settings.local.json"}[where]
        json.dump({"apiKeyHelper": "echo " + SECRET}, open(f, "w"))
        rc, o, e = run(SS, {"CLAUDE_PROJECT_DIR": p}, home=h)
        ok = "apiKeyHelper" in o
        rec("SS apiKeyHelper in " + where, ok and SECRET not in o + e, o)
with tempfile.TemporaryDirectory() as h, tempfile.TemporaryDirectory() as p:
    os.makedirs(p + "/.claude"); json.dump({"env": {"ANTHROPIC_API_KEY": ""}}, open(p + "/.claude/settings.json", "w"))
    rc, o, e = run(SS, {"CLAUDE_PROJECT_DIR": p}, home=h)
    rec("SS clean settings no finding", o == "", o)

# 2 Bash blocks
blocks = [
 "echo " + KEY, "curl https://" + HOST + "/v1/messages", "curl " + HOST,
 "pip install anthropic", "pip3 install anthropic", "pip install -U anthropic", "python3 -m pip install anthropic==0.40",
 "uv pip install anthropic", "uv add anthropic", "poetry add anthropic", "pip install 'anthropic>=0.3'",
 "npm install @anthropic-ai/sdk", "npm i -D @anthropic-ai/sdk", "pnpm add @anthropic-ai/sdk", "yarn add @anthropic-ai/sdk", "bun add @anthropic-ai/sdk",
 "npm install -g @anthropic-ai/claude-code@latest",
 "export ANTHROPIC_API_KEY=abc", "ANTHROPIC_API_KEY=abc node x.js", "env ANTHROPIC_API_KEY=abc node x.js",
 "ANTHROPIC_API_KEY=$(cat f) node x.js", 'bash -c "export ANTHROPIC_API_KEY=abc"', "export ANTHROPIC_AUTH_TOKEN=tok",
 "export ANTHROPIC_API_KEY=\"$FOO\"", "export ANTHROPIC_API_KEY=$(cat ~/k)", "echo hi; export ANTHROPIC_API_KEY=abc",
 "echo '{\"apiKeyHelper\": \"x\"}' > a.json", "sed -i '' 's/a/apiKeyHelper/' x",
 "pip install --upgrade pip anthropic", "pip install requests anthropic", "cd x && pip install anthropic",
 "python3 -m pip install -U anthropic", "pipx install anthropic", "npx -y @anthropic-ai/sdk",
 "export ANTHROPIC_API_KEY = abc", "declare -x ANTHROPIC_API_KEY=abc", "ANTHROPIC_API_KEY=\"abc\" node x",
 "export ANTHROPIC_API_KEY=''x", "pip install anthropic[bedrock]", "npm install --save @anthropic-ai/sdk@0.30",
 "curl https://API.ANTHROPIC.COM/v1", "curl https://api.anthropic\\.com", "curl https://api.\"anthropic\".com",
 "H=api.anthropic; curl $H.com", "pip install anthropic" + " --quiet", "pip install -r req.txt anthropic",
 "python3 -m pip install --user anthropic", "pip install git+https://github.com/anthropics/anthropic-sdk-python",
 "uvx --from anthropic python", "uv pip install -U anthropic", "uv add --dev anthropic",
 "npm install @anthropic-ai/claude-agent-sdk", "npm install --save-dev @anthropic-ai/sdk",
 "export $(echo ANTHROPIC_API_KEY=abc)", "printf 'ANTHROPIC_API_KEY=abc' >> .env", "echo ANTHROPIC_API_KEY=abc >> .env",
]
for c in blocks:
    rc = bash(c); rec("Bash blocks: " + c, rc == 2, "rc=%d (PASSED THROUGH)" % rc)
allows = [
 "printenv", "printenv ANTHROPIC_API_KEY", "[ -n \"$ANTHROPIC_API_KEY\" ] && echo set", "unset ANTHROPIC_API_KEY", "unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN",
 "ANTHROPIC_API_KEY= claude", "ANTHROPIC_API_KEY=\"\" claude", "export ANTHROPIC_API_KEY=", "env -u ANTHROPIC_API_KEY claude",
 "git status", "git log --oneline -5", "npm test", "node lib/docx/cli.js build x.json", "python3 scripts/lint_voice.py x.md",
 "grep -rn anthropic docs/", "grep -rn ANTHROPIC_API_KEY .", "pip install python-docx", "npm install jszip @xmldom/xmldom",
 "ls -la", "cat BUILD_BRIEF.md", "pip install requests", "npm install --save-dev jest", "echo $ANTHROPIC_API_KEY | wc -c",
 "git commit -m 'docs: auth guard for anthropic usage'", "pip list | grep anthropic", "pip show anthropic", "pip uninstall anthropic",
 "npm ls @anthropic-ai/claude-code", "claude --version", "pip install python-docx; echo anthropic", "echo installing; pip install lxml && echo anthropic done",
 "npm install jszip && grep anthropic README.md", "pip install pytest\ngrep anthropic x",
]
for c in allows:
    rc = bash(c); rec("Bash allows: " + c, rc == 0, "rc=%d (FALSE POSITIVE)" % rc)

# 4 file tools
for t in ["Write", "Edit", "NotebookEdit"]:
    p = "x.ipynb" if t == "NotebookEdit" else "lib/x.js"
    rec(t + " blocks key literal", tool(t, p, "const k='" + KEY + "'") == 2)
    rec(t + " blocks api host", tool(t, p, "fetch('https://" + HOST + "/v1')") == 2)
    rec(t + " blocks SDK import js", tool(t, p, "const a = require('@anthropic-ai/sdk')") == 2)
    rec(t + " blocks SDK import py", tool(t, "x.py", "import anthropic\n") == 2)
    rec(t + " blocks from anthropic", tool(t, "x.py", "from anthropic import Anthropic\n") == 2)
    rec(t + " blocks non-empty key assign", tool(t, "x.sh", "ANTHROPIC_API_KEY=abc") == 2)
    rec(t + " blocks json non-empty key", tool(t, "a.json", '{"ANTHROPIC_API_KEY": "abc"}') == 2)
    rec(t + " blocks apiKeyHelper", tool(t, ".claude/settings.json", '{"apiKeyHelper": "x"}') == 2)
    rec(t + " blocks process.env read", tool(t, "x.js", "const k = process.env.ANTHROPIC_API_KEY") == 2)
    rec(t + " blocks os.environ read", tool(t, "x.py", "k = os.environ['ANTHROPIC_API_KEY']") == 2)
    rec(t + " blocks os.getenv read", tool(t, "x.py", "k = os.getenv('ANTHROPIC_API_KEY')") == 2)
    rec(t + " blocks yaml key", tool(t, "x.yml", "ANTHROPIC_API_KEY: abc123") == 2)
    rec(t + " blocks .env", tool(t, ".env", "ANTHROPIC_AUTH_TOKEN=abc") == 2)
    rec(t + " md skip host", tool(t, "docs/a.md", "calls " + HOST + " and apiKeyHelper and import anthropic") == 0)
    rec(t + " md blocks key literal", tool(t, "docs/a.md", "use " + KEY) == 2)
    rec(t + " json empty passes", tool(t, "a.json", '{"ANTHROPIC_API_KEY": ""}') == 0)
    rec(t + " normal code passes", tool(t, "lib/x.js", "const a = require('jszip');\nconsole.log('anthropic')") == 0)
    rec(t + " prose mention in py passes", tool(t, "x.py", "# note: we do not use the anthropic sdk\nx=1") == 0)
    rec(t + " empty single-quote passes", tool(t, "x.sh", "ANTHROPIC_API_KEY=''") == 0)
    rec(t + " empty bare assign passes", tool(t, "x.sh", "ANTHROPIC_API_KEY=\n") == 0)
rec("Write md with 'anthropic' skills text passes", tool("Write", ".claude/skills/x/SKILL.md", "Never set ANTHROPIC_API_KEY=abc") == 0)

# 5 settings edit
rec("Edit settings.json env empty block PASSES",
    tool("Edit", "/Users/mgarriga/claude-assistant/.claude/settings.json", '"env": {\n    "ANTHROPIC_API_KEY": "",\n    "ANTHROPIC_AUTH_TOKEN": ""\n  },') == 0)
rec("Edit settings.json env compact empty PASSES",
    tool("Edit", ".claude/settings.json", '"env": {"ANTHROPIC_API_KEY": "", "ANTHROPIC_AUTH_TOKEN": ""}') == 0)
rec("Write settings.json full w/ hooks and empty env PASSES",
    tool("Write", ".claude/settings.json", json.dumps({"env": {"ANTHROPIC_API_KEY": "", "ANTHROPIC_AUTH_TOKEN": ""}, "hooks": {"SessionStart": [{"hooks": [{"type": "command", "command": "python3 scripts/guard_auth.py"}]}]}}, indent=2)) == 0)
rec("Edit settings.json env single-quoted empties PASS", tool("Edit", ".claude/settings.json", "\"ANTHROPIC_API_KEY\": \"\"\n") == 0)

# robustness
for raw in ["", "not json", "[]", "null", '{"hook_event_name":"PreToolUse","tool_input":"x","tool_name":"Bash"}', '{"hook_event_name":"PreToolUse","tool_name":"Bash"}', '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":null}}', '{"hook_event_name":"PreToolUse","tool_name":"Read","tool_input":{"file_path":"x"}}']:
    p = subprocess.run([PY, G], input=raw, capture_output=True, text=True, env=BASE)
    rec("Robust exit0: " + raw[:40], p.returncode == 0 and "Traceback" not in p.stderr, p.stderr)
rc, o, e = run({"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": "echo " + KEY}})
rec("Block msg lacks key value", KEY not in o + e and "guard_auth" in e, e)
rec("Other tool Read with key passes", run({"hook_event_name": "PreToolUse", "tool_name": "Read", "tool_input": {"file_path": KEY}})[0] == 0)

# 6 perf
ts = []
for i in range(50):
    t = time.time(); run({"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": "git status"}}); ts.append((time.time() - t) * 1000)
med = statistics.median(ts); rec("Perf median <100ms (%.1fms)" % med, med < 100)
# 7 stdlib only
src = open(G).read()
import re
mods = set(re.findall(r"^\s*(?:import|from)\s+([A-Za-z_][\w.]*)", src, re.M))
print("imports:", mods)
rec("stdlib only", mods <= {"json", "os", "re", "sys", "urllib.parse"}, str(mods))
f = [r for r in res if not r[1]]
print("\n%d checks, %d failed" % (len(res), len(f)))
sys.exit(1 if f else 0)
