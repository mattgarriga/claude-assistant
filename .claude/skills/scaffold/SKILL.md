---
name: scaffold
description: Generate a new SuiteScript file and SDF deployment objects from a locked SDD Section 4.4 or a clear spec. Use for "build the script," "scaffold," or "start the code for."
---
# Scaffold
1. Source of truth: the SDD script outline (from the client's project outputs or `decisions.md`). No locked design: stop and route to the sdd or dev-one-pager skill.
2. Follow `standards/coding-standards.md` and Matt's Map/Reduce gold-standard pattern (`knowledge/netsuite-dev-patterns.md`). Reuse existing libraries in the repo; don't duplicate.
3. Create a feature branch. Generate: script file, script and deployment XML, any custom field/record XML, and a test-plan stub.
4. Mark anything not specified as a TODO with the open-question ID. Never invent field IDs.
5. Run code-review on the result. Show the diff and commit message; commit after Matt approves.
