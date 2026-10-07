"""Tests for scripts/guard_git.py. Run: python3 tests/test_guard_git.py"""
import json, os, subprocess, sys, tempfile, unittest

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "guard_git.py")
NS_CLI = "suite" + "cloud project:deploy"


def git(repo, *args):
    subprocess.run(["git", "-C", repo] + list(args), check=True, capture_output=True)


def make_repo(path, branch):
    os.makedirs(path)
    git(path, "init", "-q")
    git(path, "symbolic-ref", "HEAD", "refs/heads/" + branch)
    git(path, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "init")


class GuardGit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = os.path.realpath(cls.tmp.name)
        cls.ws = os.path.join(root, "workspace")
        cls.repos = os.path.join(root, "Repos")
        cls.other = os.path.join(root, "elsewhere")
        os.makedirs(cls.other)
        make_repo(cls.ws, "main")
        cls.main_repo = os.path.join(cls.repos, "client-a")
        cls.feat_repo = os.path.join(cls.repos, "client-b")
        make_repo(cls.main_repo, "main")
        make_repo(cls.feat_repo, "feature/x")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def run_hook(self, command, cwd=None):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=self.ws)
        p = subprocess.run(
            [sys.executable, SCRIPT],
            input=json.dumps({"tool_input": {"command": command}, "cwd": cwd or self.other}),
            capture_output=True, text=True, env=env)
        return p.returncode

    def test_1_commit_main_under_repos(self):
        self.assertEqual(self.run_hook("git commit -m x", cwd=self.main_repo), 2)

    def test_2_commit_feature_under_repos(self):
        self.assertEqual(self.run_hook("git commit -m x", cwd=self.feat_repo), 0)

    def test_3_commit_main_outside_repos(self):
        self.assertEqual(self.run_hook("git commit -m x", cwd=self.ws), 0)

    def test_4_push(self):
        self.assertEqual(self.run_hook("git push origin x", cwd=self.ws), 2)

    def test_5_merge(self):
        self.assertEqual(self.run_hook("git merge x", cwd=self.ws), 2)

    def test_6_netsuite_cli(self):
        self.assertEqual(self.run_hook(NS_CLI), 2)

    def test_7_cd_then_commit(self):
        self.assertEqual(self.run_hook("cd %s && git commit -m x" % self.main_repo), 2)

    def test_7b_relative_cd(self):
        self.assertEqual(self.run_hook("cd client-a && git commit -m x", cwd=self.repos), 2)

    def test_7c_cd_feature_ok(self):
        self.assertEqual(self.run_hook("cd %s && git commit -m x" % self.feat_repo, cwd=self.main_repo), 0)

    def test_8_git_dash_C(self):
        self.assertEqual(self.run_hook("git -C %s commit -m x" % self.main_repo), 2)

    def test_8b_relative_dash_C(self):
        self.assertEqual(self.run_hook("git -C client-a commit -m x", cwd=self.repos), 2)

    def test_10_heredoc_prose_passes(self):
        cmd = "cat >> notes.md <<'EOF'\nmerge blocks for " + "suite" + "cloud stay global\ngit push is Matt's job\nEOF"
        self.assertEqual(self.run_hook(cmd), 0)

    def test_11_echo_quoted_passes(self):
        self.assertEqual(self.run_hook('echo "git push"'), 0)

    def test_12_npx_cli_blocked(self):
        self.assertEqual(self.run_hook("npx " + NS_CLI), 2)

    def test_13_env_assignment_push_blocked(self):
        self.assertEqual(self.run_hook("FOO=1 git push"), 2)

    def test_14_chained_push_blocked(self):
        self.assertEqual(self.run_hook("ls && git push origin x"), 2)

    def test_15_heredoc_then_push_blocked(self):
        self.assertEqual(self.run_hook("cat <<EOF\nhello\nEOF\ngit push"), 2)

    def test_16_commit_message_prose_passes(self):
        self.assertEqual(self.run_hook('git commit -m "block push and merge"', cwd=self.feat_repo), 0)

    def test_17_dash_C_push_blocked(self):
        self.assertEqual(self.run_hook("git -C ../Repos/x push"), 2)

    def test_18_dash_c_merge_blocked(self):
        self.assertEqual(self.run_hook("git -c a=b merge y"), 2)

    def test_19_log_grep_passes(self):
        self.assertEqual(self.run_hook("git log --grep=merge"), 0)

    def test_20_checkout_force_blocked(self):
        self.assertEqual(self.run_hook("git checkout -f"), 2)

    def test_21_branch_force_blocked(self):
        self.assertEqual(self.run_hook("git branch -f x"), 2)

    def test_22_clean_force_blocked(self):
        self.assertEqual(self.run_hook("git clean -fd"), 2)

    def test_23_rm_force_passes(self):
        self.assertEqual(self.run_hook("rm --force tmp.txt"), 0)

    def test_24_reset_hard_blocked(self):
        self.assertEqual(self.run_hook("git --no-pager reset --hard HEAD~1"), 2)

    def test_25_branch_delete_blocked(self):
        self.assertEqual(self.run_hook("git branch -D x"), 2)

    def test_26_reset_soft_passes(self):
        self.assertEqual(self.run_hook("git reset --soft HEAD~1"), 0)

    # cycle 2: recursion, command position, unquoting, wrappers, aliases, branch tracking
    def blocked(self, cmd, cwd=None):
        self.assertEqual(self.run_hook(cmd, cwd=cwd), 2, cmd)

    def allowed(self, cmd, cwd=None):
        self.assertEqual(self.run_hook(cmd, cwd=cwd), 0, cmd)

    def test_30_shell_dash_c(self):
        for c in ["bash -c 'git push'", 'sh -lc "git push"', "zsh -ec 'ls && git merge x'",
                  "bash -c '" + NS_CLI + "'", 'eval "git push"']:
            self.blocked(c)
        self.blocked("bash -c 'git commit -m x'", cwd=self.main_repo)
        self.allowed("bash -c 'echo hi'")

    def test_31_command_position_anywhere(self):
        for c in ["echo $(git push)", "echo `git push`", "echo \"$(git push)\"", "(git push)",
                  "{ git push; }", "if true; then git push; fi", "for i in 1; do git push; done", "! git push"]:
            self.blocked(c)

    def test_32_unquote(self):
        for c in ['"git" push', "'git' push", "\\git push", '"' + "suite" + 'cloud" x', 'git "push"']:
            self.blocked(c)

    def test_33_wrappers(self):
        for c in ["env -i git push", "env -u X git push", "nice -n 5 git push", "timeout 5 git push",
                  "timeout -s KILL 5 git push", "sudo -u bob git push", "echo x | xargs -n1 git push",
                  "find . -exec git push \\;", "nohup git push", "stdbuf -oL git push",
                  "pnpm dlx " + "suite" + "cloud x", "npm x " + "suite" + "cloud", "yarn dlx " + "suite" + "cloud",
                  "npx -y @oracle/" + "suite" + "cloud-cli x", "./node_modules/.bin/" + "suite" + "cloud x"]:
            self.blocked(c)
        self.allowed("env -i ls")
        self.allowed("grep -r " + "suite" + "cloud .")

    def test_34_alias_and_send_pack(self):
        self.blocked("git -c alias.p=push p")
        self.blocked("git -c alias.x='!sh -c foo' x")
        self.blocked("git send-pack x")
        self.allowed("git -c alias.st=status st")

    def test_35_git_dir_pushd_cd_dashdash(self):
        self.blocked("git --git-dir=%s/.git --work-tree=%s commit -m x" % (self.main_repo, self.main_repo))
        self.blocked("git --git-dir %s/.git commit -m x" % self.main_repo)
        self.blocked("pushd %s && git commit -m x" % self.main_repo)
        self.blocked("cd -- %s && git commit -m x" % self.main_repo)

    def test_36_branch_tracking(self):
        self.allowed("git switch -c feature/q && git commit -m x", cwd=self.main_repo)
        self.allowed("git checkout -b hotfix/q && git commit -m x", cwd=self.main_repo)
        self.blocked("git checkout main && git commit -m x", cwd=self.feat_repo)
        self.blocked("git switch main && git commit -m x", cwd=self.feat_repo)
        self.blocked("git checkout -b feature/q && git checkout main && git commit -m x", cwd=self.feat_repo)

    def test_9_non_git(self):
        self.assertEqual(self.run_hook("ls -la"), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
