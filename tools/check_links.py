#!/usr/bin/env python3
"""Check every URL in data/documents.csv and write data/link_report.csv.

Usage:  python tools/check_links.py            # report only
        python tools/check_links.py --update   # also set last_link_check on records that respond
Many ETB sites block automated requests (403/429). Those are reported as 'blocked', not 'broken': open them in a browser before concluding anything.
Standard library only."""
import csv, sys, datetime, urllib.request, urllib.error, concurrent.futures as cf
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
UA = {"User-Agent": "Mozilla/5.0 (compatible; FETDetective-linkcheck/1.0)"}

def check(row):
    url = row["url"].replace(" ", "%20")
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=UA, method=method)
            with urllib.request.urlopen(req, timeout=20) as r:
                return row["id"], "ok", r.status
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 999): return row["id"], "blocked", e.code
            if method == "HEAD" and e.code in (400, 405, 501): continue
            return row["id"], "broken", e.code
        except Exception as e:
            if method == "HEAD": continue
            return row["id"], "error", type(e).__name__
    return row["id"], "error", "unknown"

with open(DATA / "documents.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f); fields = reader.fieldnames; rows = list(reader)
with cf.ThreadPoolExecutor(8) as ex: results = list(ex.map(check, rows))
today = datetime.date.today().isoformat()
res = {i: (s, c) for i, s, c in results}
with open(DATA / "link_report.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["id", "etb", "title", "url", "result", "code", "checked"])
    for r in rows: w.writerow([r["id"], r["etb"], r["title"], r["url"], *res[r["id"]], today])
if "--update" in sys.argv:
    for r in rows:
        if res[r["id"]][0] == "ok": r["last_link_check"] = today
    with open(DATA / "documents.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
from collections import Counter
print(Counter(s for s, _ in res.values()))
