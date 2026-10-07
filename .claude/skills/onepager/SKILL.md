---
name: onepager
description: Produce an Ethos Development Request One-Pager for the Smartsheet intake form. Use for bug fixes, config changes, reporting/data requests, and minor enhancements.
argument-hint: [client] [request]
---

# Dev Request One-Pager

Format: `standards/one-pager-format.md`. Template: `templates/template-dev-request-one-pager.docx` (filled, never rebuilt).

## 1. Load context
Client `client.md`, `projects/ad-hoc-support/project.md` (or the named project), `decisions.md`.

## 2. Gather (one batch, only what's genuinely unknown)
- Requester full name and role/company
- Request type (Bug Fix / Config Change / Reporting/Data / Minor Enhancement)
- Why it's needed; impact if not done
- Current behavior, step by step
- Desired behavior
- What specifically changes: scripts, records, fields, saved searches, workflows
- In scope / out of scope / client constraints
- Open questions and owners

Partial answers get a focused follow-up. Never fill gaps.

## 3. Native-first and simplicity check
Before writing Request Details: could this be a saved search, field sourcing, form change, or workflow instead of script work? Is the requested change bigger than the problem? If yes, say so and propose the smaller version. The requester can override with a reason.

If the request is actually larger than a one-pager (new integration, multiple scripts, cross-record redesign), say it should be an SDD or CO.

## 4. Build and hand off
- Write `data.json` per the `lib/docx/` README schema (One-Pager). The doc-producer agent fills the template (helper lines removed, footer line kept), renders, and lints the filled content. Inspect the render.
- Before showing Matt, run `qa-gate` on the `data.json` content (client slug, type one-pager) and fix every FAIL; re-run doc-producer after content fixes. Doc-producer reports lint and secret-scan results; resolve wording hits yourself.
- Save to the project's `outputs/`.
- Summary, verification checklist, context write-back proposal.
