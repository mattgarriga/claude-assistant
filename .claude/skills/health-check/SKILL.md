---
name: health-check
description: Verify the safety rails are live. Compares live claude.ai connector IDs to settings.json deny and ask rules, runs fake-ID send and delete tests, and checks hooks, auth env, managed settings, and the ethos-dev conventions file. Use on /health-check, after a connector is added or reconnected, or when a tool prefix may have changed.
---

# Health check

Read-only except for the denial tests, which use fake IDs and must be refused. Never use a real message, chat, sheet, or row ID. Never print secret values.

## Steps

1. **Connector IDs.** Load `session_connectors_status` through ToolSearch and call it. Read `.claude/settings.json`. For each claude.ai connector (M365, Smartsheet, Lucid, Read AI), take its current ID prefix (`mcp__<id>__`) and confirm it appears in at least one deny or ask rule. Report any connector whose ID has no rules. A connector that is disconnected is reported, not failed.
2. **Denial tests (fake IDs only).** Call each tool; permissions must refuse it before it runs.
   - M365 `outlook_send_draft` with messageId `AAMkFAKEHEALTHCHECK`
   - M365 `teams_send_chat_message` with chatId `19:fake-health@thread.v2` and a short test body
   - Smartsheet `delete_rows` with sheet_id `1` and row_ids `[1]`

   Use the current live ID prefix for each. A permission refusal is a pass. Any other result (API error, not found, validation error, success) means the rule is missing or mismatched: report **CRITICAL**, and do not retry.
3. **Hooks registered.** In `settings.json`, confirm hooks for `guard_git.py`, `guard_auth.py`, `guard_actionlog.py` (PreToolUse on the Smartsheet `add_rows` tool; it must auto-approve only sheet 5639928991141764), and `hook_lint_outputs.py` (PostToolUse on Write|Edit, PreToolUse on the three M365 draft tools).
4. **Auth.** Confirm `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` are blank (check the `env` block and the shell with `[ -z "$VAR" ]`; never echo values). Confirm `/Library/Application Support/ClaudeCode/managed-settings.json` exists and contains `forceLoginMethod` set to `claudeai` (read only, do not edit).
5. **Conventions file.** Confirm the ethos-dev conventions file exists at the path named in `standards/coding-standards.md`.

## Output

One table, nothing else except a closing line naming the first fix to make.

| Check | Result | Fix |
|---|---|---|

One row per connector for step 1, one per denial test for step 2, then one each for hooks, auth, managed settings, and conventions file. Result is PASS, FAIL, or CRITICAL. Fix is blank on PASS; otherwise the exact rule or setting to add (for example the full `mcp__<id>__outlook_send_draft` deny line). Do not edit `settings.json` yourself; propose the change for Matt.
