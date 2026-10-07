---
name: usage
description: Check remaining plan quota and this session's context fill, then recommend lean or full mode. Use for "/usage", "how much usage do I have", or before a heavy task.
argument-hint: [task you are about to run]
---
# Usage

One call, no agents. Call `mcp__ccd_session_mgmt__get_usage` (load it with ToolSearch if deferred).

Report in four lines: 5-hour used and reset time, weekly used and reset time, any per-model weekly limit that is above 50 percent, and this session's context percent.

Recommend a mode (defaults, Matt can change them):
| Highest limit used | Mode |
|---|---|
| Under 50 percent | Full: any skill, agents allowed where `CLAUDE.md` says so |
| 50 to 80 percent | Lean: lean `/today`, no live-test runs, no agents except for large raw pulls |
| Over 80 percent | Essentials only: replies, recaps for meetings that just happened |

If context is over 60 percent, suggest a new session before the next big task. If $ARGUMENTS names a task, say which mode it fits and its rough cost (low, medium, high). If status is `not_applicable` or `unavailable`, say so and stop.
