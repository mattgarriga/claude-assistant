import json, os, subprocess, sys, tempfile, unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "guard_auth.py")
KEY = "sk-ant-" + "test000"
HOST = "api.anthropic" + ".com"
AK = "ANTHROPIC_API_KEY"
AT = "ANTHROPIC_AUTH_TOKEN"


def run(payload, env=None, raw=None):
    e = {k: v for k, v in os.environ.items() if not k.startswith(("ANTHROPIC_", "CLAUDE_CODE_USE_"))}
    e.update(env or {})
    p = subprocess.run([sys.executable, SCRIPT], input=raw if raw is not None else json.dumps(payload),
                       capture_output=True, text=True, env=e)
    return p


def bash(cmd):
    return run({"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": cmd}})


def wr(path, content, tool="Write"):
    k = {"Write": "content", "Edit": "new_string", "NotebookEdit": "new_source"}[tool]
    return run({"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": {"file_path": path, k: content}})


class Bash(unittest.TestCase):
    def blocked(self, cmd):
        p = bash(cmd)
        self.assertEqual(p.returncode, 2, cmd)
        self.assertIn("BLOCKED by guard_auth", p.stderr)

    def ok(self, cmd):
        self.assertEqual(bash(cmd).returncode, 0, cmd)

    def test_blocks(self):
        for c in ["echo " + KEY, "curl https://" + HOST + "/v1/messages",
                  "pip install anthropic", "pip3 install anthropic", "uv add anthropic",
                  "poetry add anthropic", "uv pip install anthropic",
                  "npm install @anthropic-ai/sdk", "pnpm add @anthropic-ai/sdk",
                  "yarn add @anthropic-ai/claude-code", "bun add @anthropic-ai/sdk", "npm i @anthropic-ai/sdk",
                  "export %s=abc" % AK, "%s=abc python x.py" % AK, "env %s=abc ls" % AT,
                  "export %s='abc'" % AT, "echo apiKeyHelper"]:
            self.blocked(c)

    def test_passes(self):
        for c in ["printenv " + AK, '[ -n "$%s" ] && echo set' % AK, "unset " + AK,
                  AK + "= claude", AK + '="" claude', "export %s=" % AT, "ls -la", "pip install requests",
                  "npm install lodash", "git status"]:
            self.ok(c)


class Files(unittest.TestCase):
    def blocked(self, path, content, tool="Write"):
        p = wr(path, content, tool)
        self.assertEqual(p.returncode, 2, content)
        self.assertIn("BLOCKED by guard_auth", p.stderr)

    def ok(self, path, content, tool="Write"):
        self.assertEqual(wr(path, content, tool).returncode, 0, content)

    def test_blocks(self):
        for c in ["k = '%s'" % KEY, "import anthropic", "from anthropic import Anthropic",
                  'const a = require("@anthropic-ai/sdk")', 'import A from "@anthropic-ai/sdk"',
                  "url = 'https://%s/v1'" % HOST, '{"apiKeyHelper": "x.sh"}',
                  '{"env": {"%s": "abc"}}' % AK, "export %s=abc" % AK, '%s = "abc"' % AT,
                  "const k = process.env." + AK, 'os.environ["%s"]' % AK, 'os.getenv("%s")' % AK]:
            self.blocked("/x/app.py", c)

    def test_tools(self):
        self.blocked("/x/a.py", "import anthropic", "Edit")
        self.blocked("/x/a.ipynb", "import anthropic", "NotebookEdit")

    def test_md_key_still_blocked(self):
        self.blocked("/x/notes.md", "key " + KEY)

    def test_passes(self):
        self.ok("/x/settings.json", '{"env": {"%s": ""}}' % AK)
        self.ok("/x/notes.md", "import anthropic and %s and apiKeyHelper" % HOST)
        self.ok("/x/scripts/guard_auth.py", "import anthropic; apiKeyHelper")
        self.ok("/x/tests/test_guard_auth.py", "import anthropic")
        self.ok("/x/app.py", "print('hello')")


class Other(unittest.TestCase):
    def test_other(self):
        self.assertEqual(run({"hook_event_name": "PreToolUse", "tool_name": "Read", "tool_input": {}}).returncode, 0)
        self.assertEqual(run({"hook_event_name": "Stop"}).returncode, 0)
        self.assertEqual(run(None, raw="not json{").returncode, 0)
        self.assertEqual(run(None, raw="").returncode, 0)


class Session(unittest.TestCase):
    def start(self, env):
        return run({"hook_event_name": "SessionStart"}, env)

    def test_clean(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.start({"HOME": d, "CLAUDE_PROJECT_DIR": d})
            self.assertEqual((p.returncode, p.stdout, p.stderr), (0, "", ""))

    def test_env_findings(self):
        with tempfile.TemporaryDirectory() as d:
            for v in [AK, AT, "CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX", "CLAUDE_CODE_USE_FOUNDRY"]:
                p = self.start({"HOME": d, "CLAUDE_PROJECT_DIR": d, v: "secretvalue"})
                self.assertEqual(p.returncode, 0)
                out = json.loads(p.stdout)
                ctx = out["hookSpecificOutput"]["additionalContext"]
                self.assertTrue(ctx.startswith("AUTH GUARD:"))
                self.assertIn(v, ctx)
                self.assertNotIn("secretvalue", p.stdout + p.stderr)
                self.assertTrue(p.stderr.strip())

    def test_helper_files(self):
        for rel in ["settings.json", "settings.local.json"]:
            with tempfile.TemporaryDirectory() as d:
                os.makedirs(os.path.join(d, ".claude"))
                with open(os.path.join(d, ".claude", rel), "w") as f:
                    json.dump({"apiKeyHelper": "x"}, f)
                p = self.start({"HOME": d + "/h", "CLAUDE_PROJECT_DIR": d})
                self.assertIn("apiKeyHelper", p.stdout)
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(d + "/.claude")
            with open(d + "/.claude/settings.json", "w") as f:
                json.dump({"apiKeyHelper": "x"}, f)
            p = self.start({"HOME": d, "CLAUDE_PROJECT_DIR": d + "/none"})
            self.assertIn("apiKeyHelper", p.stdout)

    def test_base_url(self):
        with tempfile.TemporaryDirectory() as d:
            base = {"HOME": d, "CLAUDE_PROJECT_DIR": d}
            p = self.start(dict(base, ANTHROPIC_BASE_URL="https://proxy.example.com/v1?token=zzz"))
            self.assertIn("proxy.example.com", p.stdout)
            self.assertNotIn("zzz", p.stdout)
            p = self.start(dict(base, ANTHROPIC_BASE_URL="https://" + HOST))
            self.assertEqual(p.stdout, "")


if __name__ == "__main__":
    unittest.main()
