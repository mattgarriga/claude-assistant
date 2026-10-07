#!/bin/bash
# Usage: render-check.sh <file.docx> <outdir>
# Converts a .docx to PDF with soffice, then to 80 dpi PNG pages with pdftoppm.
set -euo pipefail
if [ $# -ne 2 ]; then echo "Usage: $0 <file.docx> <outdir>" >&2; exit 2; fi
DOCX="$1"; OUT="$2"
mkdir -p "$OUT"
# separate profile dir so a running LibreOffice does not block the conversion
PROFILE="$(mktemp -d)"
soffice -env:UserInstallation="file://$PROFILE" --headless --convert-to pdf --outdir "$OUT" "$DOCX" >/dev/null 2>&1
BASE="$(basename "${DOCX%.docx}")"
pdftoppm -r 80 -png "$OUT/$BASE.pdf" "$OUT/$BASE"
rm -rf "$PROFILE"
ls "$OUT"
