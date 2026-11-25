#!/usr/bin/env python3
"""Validate the CSV files in data/ and generate assets/js/data.js.

Usage:   python tools/build.py            # validate + generate
         python tools/build.py --check    # validate only
         python tools/build.py --stats    # also print a summary by ETB
Standard library only (Python 3.8+). Exits with status 1 if any error is found."""
import csv, json, re, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOC_STATUS = {"located", "verified", "under_review", "outdated"}
COV_STATUS = {"verified_coverage", "located", "under_review", "not_located", "outdated", "not_assessed"}
NAT_STATUS = {"located", "verified", "under_review", "outdated", "not_assessed"}
DOC_TYPES = {"policy", "webpage", "strategy", "service_plan", "annual_report", "financial_statements",
             "performance_agreement", "qqi_report", "report", "procedure", "guideline"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
errors, warnings = [], []

def read(name):
    with open(DATA / name, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def err(msg): errors.append(msg)
def warn(msg): warnings.append(msg)

def check_date(row_id, field, value):
    if value and not DATE.match(value):
        err(f"{row_id}: {field} '{value}' must be YYYY-MM-DD")

etbs = read("etbs.csv")
etb_ids = {e["id"] for e in etbs}
if len(etb_ids) != len(etbs): err("etbs.csv: duplicate id")
fields = read("fields.csv")
field_names = {f["field"] for f in fields}
topics = read("topics.csv")
topic_names = {t["topic"] for t in topics}
for t in topics:
    try: re.compile(t["title_pattern"])
    except re.error as e: err(f"topics.csv: bad pattern for '{t['topic']}': {e}")

docs = read("documents.csv")
doc_ids = set()
for i, d in enumerate(docs, start=2):
    rid = d["id"] or f"documents.csv line {i}"
    if not d["id"]: err(f"{rid}: missing id")
    elif d["id"] in doc_ids: err(f"{rid}: duplicate id")
    doc_ids.add(d["id"])
    for req in ("etb", "title", "doc_type", "url", "status", "checked"):
        if not d[req]: err(f"{rid}: missing {req}")
    if d["etb"] and d["etb"] not in etb_ids: err(f"{rid}: unknown etb '{d['etb']}'")
    if d["url"] and not d["url"].startswith(("http://", "https://")): err(f"{rid}: url must start with http(s)://")
    if d["status"] not in DOC_STATUS: err(f"{rid}: status '{d['status']}' not in {sorted(DOC_STATUS)}")
    if d["doc_type"] and d["doc_type"] not in DOC_TYPES: warn(f"{rid}: unusual doc_type '{d['doc_type']}'")
    for f in ("published", "checked", "reviewed_at", "review_due", "last_link_check"): check_date(rid, f, d[f])
    if d["status"] == "verified":
        for req in ("reviewed_at", "reviewer", "evidence_notes"):
            if not d[req]: err(f"{rid}: verified records need {req}")
        if d["content_reviewed"] != "yes": err(f"{rid}: verified records need content_reviewed=yes")
for d in docs:
    if d["superseded_by"] and d["superseded_by"] not in doc_ids: err(f"{d['id']}: superseded_by '{d['superseded_by']}' not found")
seen = {}
for d in docs:
    k = (d["etb"], d["url"])
    if k in seen and d["title"] == seen[k]: warn(f"{d['id']}: duplicate of an earlier record (same ETB, URL and title)")
    seen[k] = d["title"]

facts = read("facts.csv")
for f in facts:
    if f["etb"] not in etb_ids: err(f"facts.csv: unknown etb '{f['etb']}'")
    if f["field"] not in field_names: err(f"facts.csv: unknown field '{f['field']}'")
    check_date(f"facts {f['etb']}/{f['field']}", "checked", f["checked"])

coverage = read("coverage.csv")
for c in coverage:
    cid = f"coverage {c['etb']}/{c['topic']}"
    if c["etb"] not in etb_ids: err(f"{cid}: unknown etb")
    if c["topic"] not in topic_names: err(f"{cid}: topic not in topics.csv")
    if c["status"] not in COV_STATUS: err(f"{cid}: status '{c['status']}' not in {sorted(COV_STATUS)}")
    if c["doc_id"] and c["doc_id"] not in doc_ids: err(f"{cid}: doc_id '{c['doc_id']}' not found")
    check_date(cid, "reviewed_at", c["reviewed_at"])
    if c["status"] == "verified_coverage":
        for req in ("doc_id", "evidence", "reviewed_at", "assessor"):
            if not c[req]: err(f"{cid}: verified_coverage needs {req}")

national = read("national.csv")
for n in national:
    if n["status"] not in NAT_STATUS: err(f"national.csv: '{n['title']}' has bad status '{n['status']}'")
synonyms = {}
for s in read("synonyms.csv"):
    term, rel = list(s.values())[0], list(s.values())[1]
    synonyms[term.strip().lower()] = [x.strip().lower() for x in rel.split(";") if x.strip()]

for w in warnings: print("warning:", w)
for e in errors: print("ERROR:", e)
print(f"{len(docs)} documents, {len(facts)} facts, {len(coverage)} coverage assessments, {len(errors)} errors, {len(warnings)} warnings")
if errors: sys.exit(1)

if "--stats" in sys.argv:
    for e in etbs:
        mine = [d for d in docs if d["etb"] == e["id"]]
        print(f"  {e['abbr']:<20}{len(mine):>4} records, {sum(d['status']=='verified' for d in mine)} verified")
if "--check" in sys.argv: sys.exit(0)

fd = {
    "meta": {"built": datetime.date.today().isoformat(), "contact": ""},
    "etbs": [{"id": e["id"], "name": e["name"], "abbr": e["abbr"], "area": e["area"], "itemised": e["policy_list_itemised"] == "yes"} for e in etbs],
    "fields": [{"field": f["field"], "section": f["section"]} for f in sorted(fields, key=lambda x: int(x["order"]))],
    "facts": {},
    "docs": [{k: d[k] for k in d} for d in docs],
    "coverage": coverage,
    "national": national,
    "topics": [{"category": t["category"], "topic": t["topic"], "pattern": t["title_pattern"]} for t in topics],
    "synonyms": synonyms,
}
for f in facts: fd["facts"].setdefault(f["etb"], {})[f["field"]] = {"html": f["html"], "checked": f["checked"], "source": f["source_url"]}
out = ROOT / "assets" / "js" / "data.js"
out.write_text("/* GENERATED by tools/build.py from data/*.csv. Do not edit by hand. */\nwindow.FD=" + json.dumps(fd, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
print("wrote", out.relative_to(ROOT))
