---
name: ingest
description: Pull facts from a local .docx or PDF (SDD, SOW, notes, one-pager) into context write-back proposals. Use for "/ingest <path>", "read this SDD for context", or when Matt points at a file.
argument-hint: <file path> [client]
---
# Ingest

Source documents live in OneDrive (path in each `client.md`). Read them only. Never write outputs there.

1. Resolve the client from the argument, the path (folder name matches roster), or the document. Ambiguous: ask.
2. Extract text to the scratchpad: `pandoc <file> -t plain --wrap=none` for .docx, `pdftotext` for PDF. Do not paste the extract into chat. If it is over about 40,000 characters, read headings first, then only sections relevant to context (contacts, scope, assumptions, open questions, decisions, sign-off table).
3. Pull facts, each tagged `[src: <doc title> v<version> <MM.DD.YYYY>]`:
   - Contacts and roles (sign-off tables, attendees)
   - Glossary and term meanings
   - Decisions and client answers to open questions
   - Scope, assumptions, out-of-scope, dependencies
   - Document identity: project, version, status, location (for the `project.md` Artifacts row)
4. Facts only. No interpretation. Conflicts with existing context files go in a separate list.
5. Secrets: if the document holds a credential or key, omit it and name only its location.
6. Output: write the proposals to `state/writeback-queue.md` under the client, then show a short table (file / change). Apply nothing until Matt approves. Ask immediately only when the next step depends on a fact.
