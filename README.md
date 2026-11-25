# FET Detective

An independent research resource on Ireland's 16 Education and Training Boards (ETBs). Not an official website of SOLAS, ETBI or any ETB.

## Run it
No server needed. Open `index.html`, or host the folder on any static host (GitHub Pages, Netlify, S3).

## Structure
```
index.html              page shell and metadata
assets/css/styles.css   one token set, light and dark
assets/js/data.js       GENERATED from data/*.csv, do not edit
assets/js/app.js        routing, search, coverage, views
data/*.csv              the source of truth (edit these)
tools/build.py          validates the CSVs and generates data.js
tools/check_links.py    link checker and report
docs/ADMIN_GUIDE.md     how to add and update documents
.github/workflows/      optional automatic rebuild on GitHub
```

## Update the data
Edit the CSVs in `data/`, then run `python tools/build.py`. See `docs/ADMIN_GUIDE.md`.

## What the platform claims
- **Verified** means the document was opened and read, with reviewer, date and evidence recorded. **Located** means found on a source page, not opened.
- The Coverage page finds candidate documents by title. It does not assess policy coverage. Verified coverage appears only where a researcher recorded an assessment (`data/coverage.csv`).
- Research activity is not institutional performance. Do not rank ETBs by record counts.

## Known limits
No full-text PDF search, no database, no automated link checks on live data yet, no WCAG 2.2 AA audit.
