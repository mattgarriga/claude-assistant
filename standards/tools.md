# Tool Rules

## NetSuite
Never connect. No MCP, no API, no SDF deploy from this workspace. Ask Matt what exists in the account.

## Read AI (primary meeting source)
- Find meetings: `list_meetings` with a UTC range covering the full local calendar day (Central time; mind the CDT/CST offset), `expand: ["summary"]`.
- When a client folder exists, `list_folder_items` scoped to it is more reliable. Record the folder ID in that client's `client.md`.
- Full pull: `get_meeting_by_id` with `expand: ["summary","chapter_summaries","action_items","key_questions","topics"]`. Add `transcript` only for verbatim quotes or thin summaries. Add `metrics` only if asked.
- Only captures meetings the bot joined. No data means ask Matt for notes or a transcript. Never fabricate.
- Mistranscribes proper nouns. Known: Emagia->Imagia, Celigo->Saligo, Brightree->Brett Tree, kIQ Plus->Kick Plus. Each client's `client.md` has a Glossary for more. Cross-check before client-facing use.
- Misattributes in-room/shared-device people as "conference room participant" or "not attended". Use the Outlook invite for attendance and recipients.

## Microsoft 365 (Outlook)
- Read/search mail and calendar; create drafts, including reply and reply-all drafts that preserve the thread and CC.
- Cannot send (denied in settings). Cannot attach files.
- Drafts use HTML with `<p>` tags.
- Signature (canonical, confirmed by Matt 2026-10-06): every draft ends with the hard-coded block below. API-created drafts do not carry Matt's Outlook signature, so never rely on it. Do not add a second sign-off or name line above it.
  - Content: line 1 `Matthew Garriga`; line 2 `972.837.5259 | matt.garriga@ethosbusinesssolutions.com`; line 3 the text "Book time with Matthew Garriga" linked to `https://bookings.cloud.microsoft/book/MatthewGarrigasBookingPage@ethosbusiness.solutions/?ismsaljsauthenabled`.
  - HTML (final `<p>` of the body; one paragraph with `<br>` so the lines sit tight). The whole block is bold and the email address is a `mailto:` link (confirmed by Matt 2026-10-07); never revert:
    ```
    <p><b>Matthew Garriga<br>972.837.5259 | <a href="mailto:matt.garriga@ethosbusinesssolutions.com">matt.garriga@ethosbusinesssolutions.com</a><br><a href="https://bookings.cloud.microsoft/book/MatthewGarrigasBookingPage@ethosbusiness.solutions/?ismsaljsauthenabled">Book time with Matthew Garriga</a></b></p>
    ```
  - Plain text (chat preview and fallback):
    ```
    Matthew Garriga
    972.837.5259 | matt.garriga@ethosbusinesssolutions.com
    Book time with Matthew Garriga: https://bookings.cloud.microsoft/book/MatthewGarrigasBookingPage@ethosbusiness.solutions/?ismsaljsauthenabled
    ```
  - Applies to emails and Outlook drafts only; not to .docx outputs or paste-ready recap bodies unless Matt asks for them as an email.
- Email references by description: search by sender, subject keywords, or date. Multiple matches: list sender / subject / received / one-line summary and ask. No match: say so.
- Batch inbox work: pull unread, filter newsletters/automated/noreply, list with one-line needs, ask which to draft.
- Recipient not in `team/roster.md` or a client's contacts: flag it.
- Capability has varied historically; confirm a tool works before relying on it in a workflow.

## Smartsheet
- Used for RAIDE logs (HUT RAIDE, Cerio RAIDE), the Ethos Development Tracker, project plans, tasks.
- Get row and column IDs via `get_sheet_summary` / `get_columns` before any write.
- Omit unused columns instead of passing blanks.
- Every write: mapped preview, explicit confirmation. Deletes are denied.
- Record each client's key sheet IDs in `client.md`.

### Sheet registry
| Sheet | ID | Notes |
|---|---|---|
| Ethos Development Tracker | 8603558799691652 | Live dev tracker. Row ID EBS.#### is the ticket in branch names. The other "Development Tracker" sheet is not used |
| Matt Garriga - Action Log | 5639928991141764 | Matt's commitments, waiting-on items, internal-only actions, management and team items. Row ID AL.####. Matthew Garriga workspace |
| Matt Garriga - RAID Log (old) | 1858937004445572 | Stale. Never read or written. Matt archives it |
| Client RAIDEs and project plans | per client | MS RAIDE in each `client.md`; project RAIDE and plan in each `project.md` (seeded by bootstrap from `docs/build/phase6-discovery.md`) |

## Lucid
See `lucid-standards.md`.

## docx
- Build through `lib/docx/` (template-fill engine: `node lib/docx/cli.js`, schemas in `lib/docx/README.md`), normally via the doc-producer agent. See `branding.md`.
- Render to PDF and visually check before handoff.
