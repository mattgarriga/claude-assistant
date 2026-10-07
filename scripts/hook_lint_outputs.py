#!/usr/bin/env python3
"""Lint hook for generated outputs and Outlook drafts.

PostToolUse Write|Edit: files under clients/*/projects/*/outputs/ or clients/*/outputs/
(.md, .txt, .docx) are linted. Voice issues warn (exit 0, additionalContext JSON).
Secret hits exit 2 with stderr telling Claude to remove the secret now.
PreToolUse on outlook_create_draft, outlook_create_reply_draft, outlook_create_reply_all_draft:
lints the body (HTML stripped, signature block lines skipped); voice warns, secrets block (exit 2).
Any other tool or path, or malformed input: exit 0."""
import html, io, json, os, re, sys, zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lint_voice import RULES, scan_secrets  # noqa: E402

DRAFT_TOOLS = ("outlook_create_draft", "outlook_create_reply_draft", "outlook_create_reply_all_draft")
OUTPUT_PATH = re.compile(r"(?:^|/)clients/[^/]+/(?:projects/[^/]+/)?outputs/")
SIG_LINES = (re.compile(r"^Matthew Garriga$"), re.compile(r"^972\.837\.5259 \|"),
             re.compile(r"^Book time with Matthew Garriga"))


def voice_issues(text):
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        for label, rx in RULES:
            for m in rx.finditer(line):
                out.append(f"{label} line {n}: '{m.group(0)}'")
    return out


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<w:tab/>|<w:br/>", " ", xml)
    return html.unescape(re.sub(r"<[^>]+>", "", xml))


def html_to_text(body):
    body = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</tr>", "\n", body)
    return html.unescape(re.sub(r"<[^>]+>", "", body))


def strip_signature(text):
    return "\n".join(l for l in text.splitlines() if not any(r.match(l.strip()) for r in SIG_LINES))


def emit(event, issues, label):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event,
                      "additionalContext": f"LINT WARNINGS ({label}): " + "; ".join(issues[:20])}}))


def check(event, text, label):
    secrets = scan_secrets(text)
    if secrets:
        lines = ", ".join(f"line {n}" for n, _, _ in secrets[:10])
        sys.stderr.write(f"BLOCKED: suspected secret in {label} ({lines}). Remove the secret now "
                         "and rewrite without it; never place credentials in outputs or drafts.\n")
        return 2
    issues = voice_issues(text)
    if issues:
        emit(event, issues, label)
    return 0


def main():
    try:
        data = json.loads(sys.stdin.read())
        tool = data.get("tool_name", "")
        inp = data.get("tool_input") or {}
        event = data.get("hook_event_name", "")
    except Exception:
        return 0
    short = tool.split("__")[-1]
    if event == "PreToolUse" and short in DRAFT_TOOLS:
        body = inp.get("body") or ""
        if not isinstance(body, str):
            return 0
        return check("PreToolUse", strip_signature(html_to_text(body)), "email draft")
    if event == "PostToolUse" and tool in ("Write", "Edit"):
        path = (inp.get("file_path") or "").replace("\\", "/")
        if not OUTPUT_PATH.search(path) or not os.path.isfile(path):
            return 0
        ext = os.path.splitext(path)[1].lower()
        try:
            if ext in (".md", ".txt"):
                text = open(path, encoding="utf-8", errors="replace").read()
            elif ext == ".docx":
                text = docx_text(path)
            else:
                return 0
        except Exception:
            return 0
        return check("PostToolUse", text, os.path.basename(path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
