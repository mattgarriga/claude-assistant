---
name: sdd
description: Run the Ethos SDD design interview and produce a Solution Design Document. Use when Matt asks for an SDD, solution design, or design doc. Never draft before the interview gates pass.
argument-hint: [client] [feature]
---

# SDD

On invocation: load context and run the native-first pass. Do not draft until the gates pass.

Format: `standards/sdd-format.md`. Template: `templates/template-sdd.docx` (filled, never rebuilt).

An SDD is a stress-tested design, not a transcription. Matt (or the requester) owns the design; you find the holes before the client signs and before a developer builds. Multiple rounds of questions is correct behavior. Never offer a partial draft "to get started."

## 0. Load context
`client.md`, `decisions.md`, the project's `project.md`, and `knowledge/`. Anything already decided there is not re-asked. Prior patterns from `knowledge/` get proposed where they fit.

## 1. Native-first pass (before any script talk)
For each requirement, ask whether native NetSuite covers it: saved search, workflow, custom form, custom field with sourcing/defaulting, approval routing, native transaction flow, SuiteFlow, CSV import, standard reports, an existing bundle or SuiteApp already in the account. If native gets 90% of the way, propose it and say what the client gives up. Ask Matt what already exists in the account (never query NetSuite).

## 2. Simplicity pass
Trim to the simplest design that meets the testable requirements. Name what you cut and why. Push hard; Matt or the requester can override with a stated reason, which gets logged in `decisions.md`.

## 3. Design interview (batch questions, as many rounds as needed)
Cover at minimum:
- Trigger and timing: what starts it, frequency, volume per run
- Source of truth per field; what happens when systems disagree
- Records touched, statuses, legal transitions
- Failure: error, partial success, timeout, duplicate submission, governance limit
- Idempotency: what if it runs twice on the same record
- Permissions: who executes, who sees output
- Existing footprint: what in the account this touches or duplicates
- Rollback: how it's turned off in production
- Manual fallback if the automation is down

For every proposed approach, name at least two alternatives and why they lose. Unanswerable questions become open questions with an owner (Matt first; only genuine client decisions go in the doc).

## 4. Section 4 gate
Do not write Solution Design until every script has: a type, a trigger, and a one-sentence client-readable justification over alternatives. Challenge every time:
- User Event doing heavy or many-record work: should be Map/Reduce
- Scheduled script polling for changes a User Event could catch at the source
- Suitelet where a saved search, custom form, or workflow would do
- Client script validation that must also hold for CSV, web services, integrations: belongs server side
- RESTlet where SuiteTalk or REST record endpoints already cover it
- Workflow chosen for logic that will outgrow it within a release or two

Unjustified script: requirement stays in Section 3, decision logged as an open question with an owner, no script outline for it. An honest gap beats an invented architecture.

## 5. Draft gate
Draft only when all are true:
- Every FR is a testable statement
- Every script is typed and justified
- Every integration has direction, trigger, payload owner
- Every open question has an owner and doesn't block the sections being written

Before drafting, show Matt the locked design summary (components table + open questions) and get a go.

## 6. Build
- Process flow via the flow skill. Embed the Lucid PNG export in 4.1 and record the edit link in Document Control.
- Write the content to `data.json` per the `lib/docx/` README schema (SDD). Section list and order: `standards/sdd-format.md`.
- Hand off to the doc-producer agent: it fills `templates/template-sdd.docx`, renders to PNG, and runs `python3 scripts/lint_voice.py --design` on the filled content. Inspect the render.
- Before showing Matt, run `qa-gate` on the `data.json` content (client slug, type SDD) and fix every FAIL; re-run doc-producer after content fixes. Doc-producer reports lint and secret-scan results; resolve wording hits yourself.
- Save to `clients/<slug>/projects/<project>/outputs/`. Drafts as `-draft.docx` (not committed).

## 7. Handoff
Short summary, then the verification checklist (names, attribution gaps, sign-off table names, unresolved assumptions). Then context write-back: design decisions to `decisions.md`, reusable pattern candidates to `knowledge/` (propose, don't write without approval).
