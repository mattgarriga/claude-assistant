---
name: query-helper
description: Write or fix SuiteQL queries and saved search formulas (CASE WHEN, NVL, DECODE, TO_CHAR, HTML formula fields). Use for any query or formula question.
---
# Query Helper
- Ask for the record types, fields, and expected output if not given. Never guess field IDs; ask Matt or check the client repo for references.
- Return the query or formula, then a 2 to 4 line explanation of non-obvious parts.
- Known traps: status internal IDs vs display text, NVL on nulls before math, ABS tolerance for float comparisons, TO_CHAR for dates in SuiteQL, joins that multiply rows.
- If the query will run inside a script, use parameterized N/query.
