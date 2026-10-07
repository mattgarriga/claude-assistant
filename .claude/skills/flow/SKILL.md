---
name: flow
description: Build an Ethos-standard process flow diagram in Lucid, verify it, export PNG. Used by SDD and SOW skills and for standalone flow requests.
argument-hint: [client] [feature]
---

# Lucid Flow

Standards: `standards/lucid-standards.md`. Follow them exactly.

1. Confirm actors/systems and steps with Matt (or take them from the locked SDD design). Decide lanes by causal adjacency before placing anything.
2. Build via the Lucid connector using true `AdvancedSwimLaneBlock` lanes.
3. Re-fetch and verify every item in the "Mandatory verification" list. Fix and re-verify until clean.
4. File in Process Flows / [Client] as `[Client] - [Feature] Process Flow`.
5. Export PNG to the project's `outputs/`, return the PNG path and the edit link.
6. Record the Lucid doc link in the project's `project.md` (via write-back proposal).
