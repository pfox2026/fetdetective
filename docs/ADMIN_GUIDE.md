# Adding and updating documents

The site is static (HTML, CSS, JavaScript). **The CSV files in `data/` are the source of truth.** You edit those in Excel or Google Sheets, run one command, and the site updates. `assets/js/data.js` is generated; never edit it by hand.

## Everyday workflow (about 2 minutes per batch)
1. Open `data/documents.csv` in Excel or Google Sheets.
2. Add a row per document. Required columns: `id`, `etb`, `title`, `doc_type`, `url`, `status`, `checked`.
3. Run `python tools/build.py`. It checks every row and tells you exactly what to fix (for example a mistyped ETB id or a verified record with no evidence).
4. Reload `index.html` to see the change. Publish the folder.

### Rules for a row
| Column | What to enter |
|---|---|
| `id` | Permanent and unique: ETB prefix plus number, e.g. `lwetb-0060`. Never reuse or renumber. |
| `etb` | An `id` from `etbs.csv` (e.g. `longford-westmeath`). |
| `doc_type` | policy, procedure, guideline, strategy, service_plan, annual_report, financial_statements, performance_agreement, qqi_report, report, webpage |
| `category` | One of the categories in `topics.csv`, or "Strategy and reporting". |
| `url` | The original source link. Never host copies of documents. |
| `published` | Only a confirmed publication date (YYYY-MM-DD). Leave blank otherwise. |
| `uploaded` | Upload month if it comes from the file path (YYYY-MM). |
| `status` | `located` (found, not opened), `verified` (opened and read), `under_review`, `outdated`. |
| `checked` | The date you confirmed it on its source (YYYY-MM-DD). |
| `superseded_by` | The `id` of the newer document, if any. |
| `review_due` | A date to revisit it. The site flags "Review due" after this date. |

A **verified** record must also have `content_reviewed=yes`, `reviewed_at`, `reviewer` and `evidence_notes`. The build refuses it otherwise. This is what keeps the Verified badge meaningful.

### Other files
- `facts.csv`: one profile fact per row (ETB, field, HTML text with its source named, checked date, optional `source_url`).
- `coverage.csv`: a researcher's assessment of whether a document really covers a topic: status (`verified_coverage`, `located`, `under_review`, `not_located`, `outdated`, `not_assessed`), the `doc_id`, an evidence excerpt, page number, reviewer and confidence. Until rows exist here, the Coverage page only offers candidate documents.
- `topics.csv`: topics and the title patterns used to find candidates. `synonyms.csv`: related search terms.
- `etbs.csv`: set `policy_list_itemised` to `yes` once an ETB's policy list has been fully recorded.
- `national.csv`: national strategies.

## Keeping links healthy
`python tools/check_links.py` tests every URL and writes `data/link_report.csv`. Add `--update` to stamp `last_link_check` on the records that respond. Many ETB sites refuse automated requests; those show as "blocked", not "broken". Open them in a browser before changing anything.

## Convenience options, simplest first
1. **CSV plus script (what this folder does).** No accounts or servers. Best for one or two researchers.
2. **Google Sheets as the editing surface.** Keep the same columns in a shared Sheet, download each tab as CSV into `data/`, run the build. Good when several people add records and you want comments and version history.
3. **GitHub, with automation.** Put the folder in a GitHub repository with GitHub Pages. `.github/workflows/build.yml` re-runs the build whenever a CSV changes, so an editor can change a file in the browser and the site rebuilds itself. Pull-request review gives you an audit trail and a place to challenge a record before it goes live.
4. **A database and admin screen (later).** If you need logins, an approval workflow, uploaded PDFs, scheduled link checks and full-text search, move to a hosted database such as Supabase or Airtable with a small admin form. Keep the same column names and the migration is a straight import.

## Full-text search (the largest gap)
Search currently reads titles, topics and profile text. To search inside documents, extract text from verified PDFs (for example with `pdftotext` per page), store each page's text with the record `id`, and index it (Pagefind is a good static option, no server). Page numbers then come for free and can feed `coverage.csv` evidence.

## Corrections
Put a contact address in `meta.contact` in `tools/build.py` (and the Method page prompts for one). Correct the record, set `checked`, and rebuild.
