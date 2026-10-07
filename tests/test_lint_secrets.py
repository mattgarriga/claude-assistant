import os, subprocess, sys, unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "lint_voice.py")
sys.path.insert(0, os.path.dirname(SCRIPT))
from lint_voice import scan_secrets  # noqa: E402

ANT = "sk-ant-" + "api03-" + "abcDEF123456"
AWS = "AKIA" + "ABCDEFGHIJKLMNOP"
BEARER = "Bearer " + "eyJhbGciOi" + "JIUzI1NiJ9abc"
PEM = "-----BEGIN " + "RSA PRIVATE KEY-----"
ASSIGN = "api_key" + " = " + "Zx9Qw8Er7Ty6Ui5"
PASS = "password" + ": " + "hunter2hunter2hunter2"
ENT = "the key is " + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6"


def cli(text, *flags):
    return subprocess.run([sys.executable, SCRIPT, "-", *flags], input=text, capture_output=True, text=True)


class Secrets(unittest.TestCase):
    def test_hits(self):
        for s in (ANT, AWS, BEARER, PEM, ASSIGN, PASS, ENT):
            self.assertTrue(scan_secrets(s), s)
            self.assertEqual(cli(s).returncode, 1, s)

    def test_masked(self):
        p = cli(ANT)
        self.assertNotIn("abcDEF123456", p.stdout)

    def test_clean(self):
        for s in (
            "Matt will review the password reset flow with the client on Friday.",
            "Deploy customscript_ebs_ue_so_validate with custscript_ebs_approver_param_long_name.",
            "script_id: customscript_ebs_mr_invoice_rollup_nightly",
            "Internal ID 1234567 for the saved search, record 98765.",
            "See https://example.com/docs/some/very/long/path/with-key-name-abcdefghijklmnop123456",
            "Commit 270dbd4f3a9c8e1b2d4f6a8c0e2b4d6f8a0c2e4b has the token fix",
            "270dbd4f3a9c8e1b2d4f6a8c0e2b4d6f8a0c2e4b",
            "Token: pending",
            "The bearer of the news arrived.",
        ):
            self.assertEqual(scan_secrets(s), [], s)

    def test_secrets_only_flag(self):
        txt = "bad — dash"
        self.assertEqual(cli(txt).returncode, 1)
        self.assertEqual(cli(txt, "--secrets-only").returncode, 0)
        self.assertEqual(cli(ANT, "--secrets-only").returncode, 1)


if __name__ == "__main__":
    unittest.main()
