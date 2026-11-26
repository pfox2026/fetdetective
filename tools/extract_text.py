#!/usr/bin/env python3
"""Extract page-by-page text from a PDF you have already READ and verified, for the full-text search.

Usage:  python tools/extract_text.py <doc_id> path/to/file.pdf
Writes data/fulltext/<doc_id>.json ({id, source_file, pages: [...]}), then run tools/build.py.

Only extract documents whose record is in data/documents.csv and whose licence or terms allow it (most ETB documents are public-sector
publications, but check). The site shows short snippets with a page number and always links to the original PDF.
Uses `pdftotext` (poppler) if installed, otherwise `pypdf` (pip install pypdf). Scanned PDFs without a text layer need OCR first."""
import sys, re, json, shutil, subprocess
from pathlib import Path
doc_id, pdf = sys.argv[1], Path(sys.argv[2])
if shutil.which("pdftotext"):
    raw = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    pages = raw.split("\f")
    if pages and not pages[-1].strip(): pages.pop()
else:
    from pypdf import PdfReader
    pages = [p.extract_text() or "" for p in PdfReader(str(pdf)).pages]
pages = [re.sub(r"[ \t]+", " ", p).strip() for p in pages]
if sum(len(p) for p in pages) < 200: sys.exit("Very little text found: this PDF may be scanned. OCR it first.")
out = Path(__file__).resolve().parent.parent / "data" / "fulltext" / f"{doc_id}.json"
out.write_text(json.dumps({"id": doc_id, "source_file": pdf.name, "pages": pages}, ensure_ascii=False), encoding="utf-8")
print(f"{doc_id}: {len(pages)} pages written to {out}")
