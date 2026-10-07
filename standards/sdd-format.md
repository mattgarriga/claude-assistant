# Solution Design Document (SDD) Format

Primary client-facing design artifact. Readable by technical and non-technical stakeholders. No code or code snippets: function names and plain-language descriptions only. Template: `templates/template-sdd.docx`. Section numbers below match the template (the old format file's 4.5 and "Section 6" references were errors).

## Structure
| Section | Contents |
|---|---|
| Header table | Client Name, Project Name (NetSuite Support - [Project #]), Customization Name |
| Basic Business Overview | Callout table: Problem, Solution, Business Impact (1-2 sentences each). Assumptions row. |
| Table of Contents | |
| 1 Business Context | 1.1 Current State, 1.2 Desired State (bullets, ~5 each), 1.3 Open Questions (# / Question / Owner / Status) |
| 2 Scope | 2.1 In Scope, 2.2 Out of Scope |
| 3 Functional Requirements | One table per group FR-01, FR-02. Exactly two columns: ID / Requirement. Never a Notes or Status column. Every row testable. |
| 4 Solution Design | 4.1 Process Flow (Lucid PNG, required), 4.2 Technical Approach (component table: Component / Type / Purpose, plus Key Logic Notes), 4.3 Integrations and Dependencies (System / Relationship / Notes), 4.4 Script Outlines |
| 5 Data Model | 5.1 New Custom Records, 5.2 Key Custom Fields (per record: Field Label / Field ID / Type / Purpose) |
| 6 Approval and Sign-Off | Name / Organization / Role / Date / Decision. Always include Matthew Garriga, Technical Lead. Sign-off text references open questions in Section 1.3. |
| 7 Document Control | Date / Author / Version / Change Reference. Include the Lucid edit link. |

Assumptions live in the Basic Business Overview box only. No separate 2.3.

## 4.4 Script Outline format (one per script)
- Heading: **EBS - [Script Name]** (dash, never pipe)
- **Filename:** ebs_[type]_[feature].js
- **Script ID:** customscript_ebs_[type]_[feature]
- **Script Type:** User Event / Client / Map/Reduce / Scheduled / Suitelet / RESTlet / Workflow Action / Portlet / Mass Update
- **Script Parameters:** (omit if none) `[Label] (custscript_ebs_param) - [Type]: [Value or TBD]`
- **Script Outline:** bullets of **functionName(params)** followed by one sentence. Bold function names, never backticks.

## Writing rules
- Shortest document a client can approve and a developer can build.
- No restating: if it's in the FR table, don't repeat it in Section 4.
- Cut "This section describes" and "In order to" openers. One idea per sentence.
- Technical Approach is what gets built. One sentence of justification per script.
- Assumptions are testable statements the client can agree or disagree with.
- Empty section: "Not applicable to this solution." No padding.
- Banned words per `voice.md`.
- Resolved interview questions are never reintroduced as open items.
- File as `clients/<slug>/projects/<project>/outputs/[CLIENT]-[Feature] SDD v1.docx`.

The interview and gating process lives in `.claude/skills/sdd/SKILL.md`.
