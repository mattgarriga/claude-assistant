# Solution Design Document (SDD) Format

Primary client-facing design artifact. Readable by technical and non-technical stakeholders. No code or code snippets: function names and plain-language descriptions only. Template: `templates/template-sdd.docx`.

## Structure (template order, do not reorder)
Fill `templates/template-sdd.docx` through `lib/docx/` (data.json, doc-producer agent). Heading text and numbering follow the template, including its quirks ("1 Business Context", then "2. Scope").

| Section | Contents |
|---|---|
| Header table | Title row "Client Solution Design Document", then Client Name, Project Name (NetSuite Support - [Project #]), Customization Name |
| Basic Business Overview | Callout table: Problem, Solution, Business Impact (1-2 sentences each), then Assumptions rows |
| Table of Contents | Rewritten from the real headings; field flagged to update on open (Word prompts once) |
| 1 Business Context | 1.1 Current State, 1.2 Desired State (bullets, ~5 each), 1.3 Open Questions (# / Question / Owner / Status) |
| 2. Scope | 2.1 In Scope, 2.2 Out of Scope (bullets) |
| 3. Functional Requirements | One Heading 2 per group ("FR-01 [Group name]") with a table. Exactly two columns: ID / Requirement (FR-01.1, FR-01.2). Never a Notes or Status column. Every row testable. |
| 4. Solution Design | 4.1 Process Flow, 4.2 Technical Approach, 4.3 Integrations and Dependencies, 4.4 Script Outlines |
| 5. Data Model | 5.1 New Custom Records, 5.2 Key Custom Fields (one bold record-type label and table per record: Field Label / Field ID / Type / Purpose) |
| 6. Approval and Sign-Off | Template sign-off sentence, table Name / Organization / Role / Date / Decision, then "Conditions:" bullets. Always include Matthew Garriga, Technical Lead. |
| 7. Document Control | Date / Author / Version / Change Reference. Include the Lucid edit link here. |

Assumptions live in the Basic Business Overview box only. No separate 2.3.

## 4.1 to 4.3
- 4.1 Process Flow: the template intro sentence, then the Lucid PNG export embedded at content width (required). The template INCLUDEPICTURE link is removed. The Lucid edit link goes in Document Control (section 7).
- 4.2 Technical Approach: title, one short details paragraph, component table (Component / Type / Purpose), then "Key Logic Notes" bullets.
- 4.3 Integrations and Dependencies: table System / Relationship / Notes.

## 4.4 Script Outline format (one block per script)
In this order:
1. Heading line: **EBS - [Script Name]** (dash. The template's "EBS | [Script Name]" pipe is replaced on fill.)
2. **Filename:** ebs_[type]_[feature].js
3. **Folder:** SDF folder path
4. **Script Type:** User Event / Client / Map/Reduce / Scheduled / Suitelet / RESTlet / Workflow Action / Portlet / Mass Update
5. **Script ID:** customscript_ebs_[type]_[feature]
6. **Script Parameters:** navy-header table, columns Name / Type / Value (Value may be TBD). Omit the table if there are none.
7. **Script Outline:** bullets of **functionName(params)** followed by one sentence, with sub-bullets for steps. Bold function names, never backticks.

## Writing rules
- Shortest document a client can approve and a developer can build.
- No restating: if it's in the FR table, don't repeat it in Section 4.
- Cut "This section describes" and "In order to" openers. One idea per sentence.
- Technical Approach is what gets built. One sentence of justification per script.
- Assumptions are testable statements the client can agree or disagree with.
- Empty section: "Not applicable to this solution." No padding. Tables are trimmed to the content row count.
- Banned words per `voice.md`.
- Resolved interview questions are never reintroduced as open items.
- File as `clients/<slug>/projects/<project>/outputs/[CLIENT]-[Feature] SDD v1.docx`.

The interview and gating process lives in `.claude/skills/sdd/SKILL.md`.
