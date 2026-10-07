import json, os, subprocess, sys, unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "guard_actionlog.py")
SS = "mcp__192da3ad-8ab5-42dd-b80a-9bae8541dbc4__"
AL = 5639928991141764


def run(payload=None, raw=None):
    return subprocess.run([sys.executable, SCRIPT], input=raw if raw is not None else json.dumps(payload),
                          capture_output=True, text=True)


def call(tool, sheet, rows=1, event="PreToolUse"):
    return {"hook_event_name": event, "tool_name": tool, "tool_input": {"sheet_id": sheet, "rows": [{"cells": []}] * rows}}


class Guard(unittest.TestCase):
    def allowed(self, p):
        self.assertEqual(p.returncode, 0)
        self.assertEqual(json.loads(p.stdout)["hookSpecificOutput"]["permissionDecision"], "allow")

    def silent(self, p):
        self.assertEqual(p.returncode, 0)
        self.assertEqual(p.stdout.strip(), "")

    def test_action_log_allowed(self):
        self.allowed(run(call(SS + "add_rows", AL)))
        self.allowed(run(call(SS + "add_rows", str(AL), rows=25)))

    def test_other_sheet_prompts(self):
        self.silent(run(call(SS + "add_rows", 6220027817578372)))

    def test_other_tools_prompt(self):
        for t in ("update_rows", "delete_rows", "delete_column", "add_columns"):
            self.silent(run(call(SS + t, AL)))

    def test_other_connector_prompts(self):
        self.silent(run(call("mcp__other__add_rows", AL)))
        self.silent(run(call("mcp__smartsheet__add_rows", AL)))

    def test_too_many_or_no_rows(self):
        self.silent(run(call(SS + "add_rows", AL, rows=26)))
        self.silent(run(call(SS + "add_rows", AL, rows=0)))

    def test_malformed(self):
        self.silent(run(raw="not json"))
        self.silent(run({"hook_event_name": "PreToolUse", "tool_name": SS + "add_rows", "tool_input": {}}))
        self.silent(run(call(SS + "add_rows", AL, event="PostToolUse")))


if __name__ == "__main__":
    unittest.main()
