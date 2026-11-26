# Contributing

The CSV files in `data/` are the source of truth. See `docs/ADMIN_GUIDE.md`.

1. Work on a branch and open a pull request. The **Tests** workflow validates your data and runs the accessibility checks.
2. Add a record only when you have found it on an official source page. Never infer or invent a document, person, date or figure.
3. Use `located` unless you opened and read the document. Use `verified` only with reviewer, date and evidence.
4. Do not commit PDFs. Link to the original and, if appropriate, add extracted text with `tools/extract_text.py`.
5. Do not describe a missing record as "the ETB has no policy". Use "not located".
