---
name: status
description: Project health for one client or all Active clients: budget burn, overdue items, stale context, upcoming milestones. Use for "status," "how's HUT looking," or weekly PM review. Also backs /status.
argument-hint: [client] [details]
---
# Project Health
Read-only. `scout` fetches RAIDE and plan rows and Development Tracker rows for the client(s); you read `project.md` files and judge.

Budget burn comes from the RAIDE columns Estimated Hours, Case Total Hours, Case Total Hours this month. Cite the sheet and row for every figure. Missing values are noted as "not in RAIDE", never invented or back-filled from memory.

Output per project: Phase / Budget (Estimated, Used, Used this month, % burn, source sheet) / Overdue items / Risks open / Next milestone / Flag (Green, Yellow, Red with one-line reason). Cross-client mode: one table, reds first. Flag any context file (`client.md`, `project.md`) last updated more than 30 days ago as stale and offer a `/client-update`.
