#!/usr/bin/env python3
"""Hook that keeps this workspace on Matt's Claude plan, never an Anthropic API key.

SessionStart: reports (never prints values) API key env vars, cloud-provider env vars,
apiKeyHelper in settings files, and a non-default ANTHROPIC_BASE_URL host.
PreToolUse Bash: exit 2 on key literals, api host use, SDK installs, setting a
non-empty key/token, apiKeyHelper. PreToolUse Write/Edit/NotebookEdit: exit 2 on the
same patterns in new content (.md files only checked for key literals).
Anything else, or malformed input: exit 0."""
import json, os, re, sys
from urllib.parse import urlparse

KEY_VARS = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")
PROVIDER_VARS = ("CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX", "CLAUDE_CODE_USE_FOUNDRY")
API_HOST = "api.anthropic" + ".com"
HEAD = ("BLOCKED by guard_auth: this workspace must use Matt's Claude plan, never an "
        "Anthropic API key or the Anthropic API directly.")

KEY_LITERAL = re.compile(r"sk-ant-[A-Za-z0-9]")
API_HOST_RE = re.compile(r"api\.anthropic\.com", re.I)
HELPER_RE = re.compile(r"apiKeyHelper")
V = r"(?:ANTHROPIC_API_KEY|ANTHROPIC_AUTH_TOKEN)"
# Bash: NAME=value where value is non-empty (NAME= or NAME="" or NAME='' pass).
BASH_SET = re.compile(r"\b" + V + r"""=(?!\s|$|;|&|\||""(?![^\s;&|])|''(?![^\s;&|]))""")
INSTALL_PY = re.compile(r"\b(?:pip3?|uv|poetry|pipx)\b[^;&|\n]*\b(?:add|install)\b[^;&|\n]*\banthropic\b")
INSTALL_JS = re.compile(r"\b(?:npm|pnpm|yarn|bun)\b[^;&|\n]*\b(?:add|install|i)\b[^;&|\n]*@anthropic-ai/")
RUN_PKG = re.compile(r"\b(?:npx|pnpx|bunx|uvx|pipx\s+run)\b[^;&|\n]*(?:@anthropic-ai/|\banthropic\b)")
SDK_USE = [
    re.compile(r"^\s*import\s+anthropic\b", re.M),
    re.compile(r"^\s*from\s+anthropic\b", re.M),
    re.compile(r"require\(\s*[\"']@anthropic-ai/"),
    re.compile(r"from\s+[\"']@anthropic-ai/"),
]
# File content: NAME: "x", NAME = 'x', "NAME": "x". Empty string value passes.
FILE_SET = re.compile(r"""\b""" + V + r"""["']?\s*[:=]\s*["']?[^\s"',;)}\]=]""")
KEY_READ = [
    re.compile(r"process\.env\.(?:ANTHROPIC_API_KEY|ANTHROPIC_AUTH_TOKEN)"),
    re.compile(r"os\.environ[^\n]*" + V),
    re.compile(r"os\.getenv\([^\n]*" + V),
]


def block(rule):
    sys.stderr.write(HEAD + " Rule: " + rule + "\n")
    sys.exit(2)


def check_bash(cmd):
    if KEY_LITERAL.search(cmd):
        block("Anthropic key literal in command")
    if API_HOST_RE.search(cmd):
        block("direct Anthropic API host in command")
    if INSTALL_PY.search(cmd) or INSTALL_JS.search(cmd):
        block("Anthropic SDK install")
    if RUN_PKG.search(cmd):
        block("Anthropic package run via npx/uvx")
    if BASH_SET.search(cmd):
        block("setting ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN to a value")
    if HELPER_RE.search(cmd):
        block("apiKeyHelper")


def check_content(path, text):
    if KEY_LITERAL.search(text):
        block("Anthropic key literal in file content")
    norm = path.replace("\\", "/")
    if norm.endswith(".md") or norm.endswith("scripts/guard_auth.py") \
            or re.search(r"(^|/)tests/[^/]*guard_auth[^/]*$", norm):
        return
    if API_HOST_RE.search(text):
        block("direct Anthropic API host in file content")
    if any(p.search(text) for p in SDK_USE):
        block("Anthropic SDK usage")
    if HELPER_RE.search(text):
        block("apiKeyHelper")
    if FILE_SET.search(text):
        block("non-empty ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN assignment")
    if any(p.search(text) for p in KEY_READ):
        block("code reading ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN")


def session_start():
    found = []
    for v in KEY_VARS + PROVIDER_VARS:
        if os.environ.get(v, "").strip():
            found.append(v + " is set")
    proj = os.environ.get("CLAUDE_PROJECT_DIR", "")
    files = [os.path.expanduser("~/.claude/settings.json")]
    if proj:
        files += [os.path.join(proj, ".claude", "settings.json"),
                  os.path.join(proj, ".claude", "settings.local.json")]
    for f in files:
        try:
            with open(f, encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:
            continue
        if isinstance(data, dict) and "apiKeyHelper" in data:
            found.append("apiKeyHelper present in " + f.replace(os.path.expanduser("~"), "~"))
    base = os.environ.get("ANTHROPIC_BASE_URL", "").strip()
    if base:
        host = urlparse(base if "//" in base else "//" + base).hostname or "unparseable"
        if host.lower() != API_HOST:
            found.append("ANTHROPIC_BASE_URL points to host " + host)
    if not found:
        return
    msg = "; ".join(found)
    out = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext":
           "AUTH GUARD: " + msg + ". Stop. Tell Matt this session may be billing an API key "
           "instead of his Claude plan, name the findings, and do no other work until he confirms."}}
    print(json.dumps(out))
    sys.stderr.write("AUTH GUARD: possible API billing: " + msg + "\n")


def main():
    try:
        data = json.loads(sys.stdin.read())
        if not isinstance(data, dict):
            return
    except Exception:
        return
    event = data.get("hook_event_name")
    if event == "SessionStart":
        session_start()
    elif event == "PreToolUse":
        tool = data.get("tool_name")
        ti = data.get("tool_input") or {}
        if not isinstance(ti, dict):
            return
        if tool == "Bash":
            check_bash(str(ti.get("command") or ""))
        elif tool in ("Write", "Edit", "NotebookEdit"):
            key = {"Write": "content", "Edit": "new_string", "NotebookEdit": "new_source"}[tool]
            path = str(ti.get("file_path") or ti.get("notebook_path") or "")
            check_content(path, str(ti.get(key) or ""))


if __name__ == "__main__":
    main()
