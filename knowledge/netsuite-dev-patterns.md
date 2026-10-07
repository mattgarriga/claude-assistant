# NetSuite Development Patterns

## Map/Reduce (Matt's preferred pattern) [src: claude.ai memory]
- getInputData: `ethos.getSavedSearchData` against a saved search.
- reduce: SuiteQL via N/query, parameterized queries.
- `TO_CHAR` for dates in SQL; MM/DD/YYYY strings for `submitFields`.
- Update in-memory arrays after writes so cascades stay correct.
- Detailed per-record JSON audit logging.
- Summarize stage iterates errors; never swallow them.
- Gold standard reference: `ebs_mr_fix_expected_pay_dates.js`.

## UE to Map/Reduce migration lessons (Atreus integration) [src: claude.ai memory]
- Let a saved search drive pickup of unprocessed records via a queue flag, instead of a UE doing the work inline.
- Bugs seen: flag writes inside a per-ID loop creating duplicate integration records; unmapped items looping forever; summarize swallowing errors.
- A second run on the same data (idempotency) is the definitive correctness test.
- Client: confirm during bootstrap.

## Saved search formulas [src: claude.ai memory]
- CASE WHEN syntax, NVL for nulls, ABS tolerance for floating point comparisons.
- Status fields: internal ID vs display text mismatches are a common trap.
- Conditional HTML output in formula fields via CASE WHEN.

## Celigo / Smartsheet [src: claude.ai memory]
- Ad-hoc ticket filter: "Ad-Hoc Support + no Case Number" beat a time-window filter.
- Column names are case-sensitive ("Assigned To").
- Watch name normalization mappings (a normalizeName bug routed one consultant's items to another).
