---
name: test-plan
description: Write sandbox test cases for a NetSuite change. Use for bug fixes and small changes built outside ethos-dev, for UAT prep, or when Matt asks for test cases. Work built with /ethos-dev:start already has UAT cases in its package; do not duplicate them.
argument-hint: [client] [details]
---
# Test Plan
Table: ID / Scenario / Setup / Steps / Expected Result. Always include: happy path, each FR from the SDD, error path, duplicate submission, governance-heavy volume, and a second idempotent run (the definitive correctness check). Save to the client project's `outputs/`. For UAT versions, rewrite steps in end-user language.
