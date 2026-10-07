# lib/docx

Template fill, not rebuild. The engine opens the real template from `templates/`, clones the template's own paragraphs, rows and cells as prototypes, and replaces text. It never sets fonts, sizes, colors, spacing or borders.

Usage, data.json schemas, fixtures and checks: see `README.md`. Rules: `standards/branding.md` (per-template spec and Filled content rules) and the `*-format.md` files.
