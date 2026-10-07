#!/bin/bash
# Build all six fixtures into lib/docx/out/ and run check.js on each.
set -e
cd "$(dirname "$0")"
mkdir -p out
node cli.js sdd fixtures/sdd.json out/sdd.docx
node cli.js sow fixtures/sow-ff.json out/sow-ff.docx
node cli.js sow fixtures/sow-tm.json out/sow-tm.docx
node cli.js sow fixtures/co-ff.json out/co-ff.docx
node cli.js sow fixtures/co-tm.json out/co-tm.docx
node cli.js onepager fixtures/onepager.json out/onepager.docx
for k in sdd sow-ff sow-tm co-ff co-tm onepager; do node check.js $k out/$k.docx | grep -E "^(PASS|FAIL|Output)" | tr '\n' ' '; echo; done
