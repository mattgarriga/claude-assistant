# Phase 0 guard_auth test report 1

Spec: task criteria 1-7 (no BUILD_BRIEF phase text supplied). Builder tests: 11/11 OK on /usr/bin/python3 3.9.6.
Harness: tests/tester_guard_auth.py, 186 checks, 180 pass, 6 advisory gaps (none are listed criteria).

| Check | Result | Evidence | Fix needed |
|---|---|---|---|
| Builder tests/test_guard_auth.py | PASS | 11 tests OK | none |
| 1 SessionStart findings (key, token, 3 provider vars, apiKeyHelper in home/proj/local, odd base URL) | PASS | all produce valid JSON hookSpecificOutput.additionalContext naming the var | none |
| 1 No secret printed | PASS | fake key/value absent from stdout and stderr in every case | none |
| 1 Clean env, default base URL (with and without trailing slash), empty-string vars | PASS | no output, exit 0 | none |
| 2 Bash blocks: key literal, host, pip/pip3/uv/poetry/pipx, npm/pnpm/yarn/bun, export/inline/env, apiKeyHelper | PASS | 50 of 56 block cases exit 2, including all listed evasions (pip install -U, python3 -m pip ==0.40, npm i -D, curl host, KEY=$(cat f), bash -c export) | none |
| 2 Advisory gaps (not in criteria) | NOTE | passes: `npx -y @anthropic-ai/sdk`, `uvx --from anthropic python` (run SDK without install); host obfuscation `api.anthropic\.com`, `api."anthropic".com`, `H=api.anthropic; curl $H.com`; `export ANTHROPIC_API_KEY = abc` (invalid bash, harmless) | Optional: add npx/uvx/pipx run to install regex; obfuscation is inherent to regex guards, accept |
| 3 Bash allows: printenv, [ -n ], unset, KEY=, git/npm test/node cli/lint_voice/grep anthropic docs/, pip install python-docx, npm install jszip @xmldom/xmldom, pip list/show/uninstall anthropic, chained commands with "anthropic" in grep | PASS | 31 of 31 exit 0, no false positives | none |
| 4 Write/Edit/NotebookEdit blocks (literal, host, SDK import/require, key assign, apiKeyHelper, env reads in js/py) | PASS | all three tools block each; .md skips all but key literals; JSON "ANTHROPIC_API_KEY": "" passes; normal code passes | none |
| 5 Edit .claude/settings.json adding empty env block | PASS | multi-line, compact, and full Write with hooks plus empty env all exit 0 | none |
| 6 Performance | PASS | median 28.2 ms over 50 runs | none |
| 7 Python 3.9 stdlib only | PASS | runs on /usr/bin/python3 3.9.6; imports json, os, re, sys, urllib.parse | none |
| Malformed/empty/non-dict input, unknown tool | PASS | exit 0, no traceback | none |
| Voice lint on scripts/guard_auth.py | PASS | clean | none |

Overall PASS (advisory gaps noted above; none violate a stated criterion).
