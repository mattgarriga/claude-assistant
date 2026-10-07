#!/usr/bin/env python3
"""PreToolUse hook: auto-approve Smartsheet add_rows ONLY for Matt's Action Log.

Any other sheet, tool, connector, or malformed input: no output, exit 0, so the
normal permission rules (ask for add_rows on every other sheet) still apply.
Deny rules are never overridden here; this hook only returns an allow decision.
"""
import json, sys

SMARTSHEET = "mcp__192da3ad-8ab5-42dd-b80a-9bae8541dbc4__"
TOOL = SMARTSHEET + "add_rows"
ACTION_LOG = 5639928991141764
MAX_ROWS = 25


def main():
    try:
        d = json.load(sys.stdin)
        if d.get("hook_event_name") != "PreToolUse" or d.get("tool_name") != TOOL:
            return
        ti = d.get("tool_input") or {}
        if int(ti.get("sheet_id")) != ACTION_LOG:
            return
        rows = ti.get("rows")
        if not isinstance(rows, list) or not 0 < len(rows) <= MAX_ROWS:
            return
    except Exception:
        return
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "permissionDecisionReason": "add_rows to Matt's Action Log is auto-approved (guard_actionlog.py)"}}))


main()
