---
name: status
description: Project health for one client or all core clients: budget burn, overdue items, stale RAIDE entries, upcoming milestones. Use for "status," "how's HUT looking," or weekly PM review. Also backs /status.
argument-hint: [client] [details]
---
# Project Health
Read-only. Sources: client `project.md` files, RAIDE and plan sheets, Development Tracker rows for the client.
Output per project: Phase / Budget used vs budgeted / Overdue items / Risks open / Next milestone / Flag (Green, Yellow, Red with one-line reason). Cross-client mode: one table, reds first. Note any context file older than 30 days as stale.
