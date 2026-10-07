import json, os, subprocess, sys, tempfile, unittest, zipfile

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "hook_lint_outputs.py")
KEY = "sk-ant-" + "api03-abcDEF123456"
DASH = "bad — dash"
SIG = ("<p><b>Matthew Garriga<br>972.837.5259 | <a href=\"mailto:matt.garriga@ethosbusinesssolutions.com\">"
       "matt.garriga@ethosbusinesssolutions.com</a><br>"
       "<a href=\"https://bookings.cloud.microsoft/book/x\">Book time with Matthew Garriga</a></b></p>")
M365 = "mcp__d921cb44-54d6-4a58-8a0e-c34b9edb58ed__"


def run(payload):
    return subprocess.run([sys.executable, SCRIPT], input=json.dumps(payload), capture_output=True, text=True)


def post(path, tool="Write"):
    return run({"hook_event_name": "PostToolUse", "tool_name": tool, "tool_input": {"file_path": path}})


def pre(tool, body):
    return run({"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": {"body": body}})


def make_docx(path, text):
    xml = "<w:document><w:body><w:p><w:r><w:t>%s</w:t></w:r></w:p></w:body></w:document>" % text
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("word/document.xml", xml)


class Hook(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.out = os.path.join(self.d, "clients", "acme", "projects", "p1", "outputs")
        self.out2 = os.path.join(self.d, "clients", "acme", "outputs")
        os.makedirs(self.out)
        os.makedirs(self.out2)

    def w(self, folder, name, text):
        p = os.path.join(folder, name)
        if name.endswith(".docx"):
            make_docx(p, text)
        else:
            with open(p, "w", encoding="utf-8") as f:
                f.write(text)
        return p

    def test_md_warn(self):
        p = post(self.w(self.out, "a.md", DASH))
        self.assertEqual(p.returncode, 0)
        j = json.loads(p.stdout)["hookSpecificOutput"]
        self.assertEqual(j["hookEventName"], "PostToolUse")
        self.assertIn("LINT WARNINGS", j["additionalContext"])

    def test_client_level_outputs_and_edit(self):
        p = post(self.w(self.out2, "a.txt", DASH), "Edit")
        self.assertIn("LINT WARNINGS", p.stdout)

    def test_md_clean(self):
        p = post(self.w(self.out, "a.md", "All good here."))
        self.assertEqual((p.returncode, p.stdout), (0, ""))

    def test_md_secret_blocks(self):
        p = post(self.w(self.out, "a.md", "key " + KEY))
        self.assertEqual(p.returncode, 2)
        self.assertIn("Remove the secret now", p.stderr)
        self.assertNotIn("abcDEF123456", p.stderr)

    def test_docx(self):
        self.assertIn("LINT WARNINGS", post(self.w(self.out, "a.docx", DASH)).stdout)
        self.assertEqual(post(self.w(self.out, "b.docx", "token = " + "Zx9Qw8Er7Ty6Ui5")).returncode, 2)
        self.assertEqual(post(self.w(self.out, "c.docx", "Fine text")).stdout, "")

    def test_other_path_ignored(self):
        p = post(self.w(self.d, "a.md", DASH + KEY))
        self.assertEqual((p.returncode, p.stdout), (0, ""))
        self.assertEqual(post(os.path.join(self.out, "missing.md")).returncode, 0)

    def test_draft_warn_block_clean(self):
        for t in ("outlook_create_draft", "outlook_create_reply_draft", "outlook_create_reply_all_draft"):
            p = pre(M365 + t, "<p>Hi, " + DASH + "</p>" + SIG)
            self.assertEqual(p.returncode, 0)
            j = json.loads(p.stdout)["hookSpecificOutput"]
            self.assertEqual(j["hookEventName"], "PreToolUse")
            self.assertEqual(pre(M365 + t, "<p>Use " + KEY + "</p>").returncode, 2)
            self.assertEqual(pre(M365 + t, "<p>Hi Sam.</p>" + SIG).stdout, "")

    def test_other_tool_and_bad_input(self):
        self.assertEqual(pre(M365 + "outlook_email_search", DASH + KEY).returncode, 0)
        p = subprocess.run([sys.executable, SCRIPT], input="not json", capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)


if __name__ == "__main__":
    unittest.main()
