---
name: migration-audit
description: Audit a client repo for SuiteScript 1.0/2.0 scripts needing 2.1 migration, User Events that should be Map/Reduce, dead scripts, and overlapping deployments. Use for migration inventories and tech-debt reviews.
---
# Migration Audit
1. Inventory every script and deployment in the repo: type, API version, record/trigger, last modified.
2. Flag: pre-2.1 API, UEs doing heavy or multi-record work, Scheduled scripts polling, multiple scripts on the same record and event, scripts with no active deployment.
3. Output a table: Script / Type / Version / Issue / Recommendation / Effort (S/M/L).
4. Ask Matt which items become one-pagers or COs. Note: this is distinct from the separate NetSuite audit tool; do not import from it.
