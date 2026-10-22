#!/usr/bin/env python3
"""Valida DOI e coleta metadados editoriais Crossref para os artigos selecionados."""
from __future__ import annotations
import concurrent.futures
import json
import re
import time
from pathlib import Path
from urllib.parse import quote
import requests

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "data" / "bibliometria"
INPUT = BIB / "referencias_candidatas.json"
OUTPUT_JSON = BIB / "crossref_metadata.json"
OUTPUT_CSV = BIB / "crossref_metadata.csv"


def norm_doi(value: str) -> str:
    value = str(value or "").strip()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value, flags=re.I)
    return value.lower().rstrip(".")


def fetch_doi(doi: str) -> dict:
    url = "https://api.crossref.org/works/" + quote(doi, safe="/:._-")
    headers = {"User-Agent": "P2-FSP-211059333/1.0 (academic metadata validation)"}
    last_error = None
    for attempt in range(5):
        try:
            r = requests.get(url, headers=headers, timeout=35)
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(min(2 ** attempt, 15))
                continue
            r.raise_for_status()
            m = r.json()["message"]
            authors = []
            for a in m.get("author", []):
                given = a.get("given", "").strip()
                family = a.get("family", "").strip()
                authors.append(", ".join(x for x in [family, given] if x))
            def first(field):
                value = m.get(field)
                return value[0] if isinstance(value, list) and value else ""
            def date_year(field):
                value = m.get(field, {}).get("date-parts", [])
                return value[0][0] if value and value[0] else None
            return {
                "doi": norm_doi(m.get("DOI", doi)),
                "title": first("title"),
                "authors_crossref": "; ".join(authors),
                "journal": first("container-title"),
                "year_crossref_print": date_year("published-print"),
                "year_crossref_online": date_year("published-online"),
                "year_crossref_issued": date_year("issued"),
                "volume": m.get("volume", ""),
                "issue": m.get("issue", ""),
                "page": m.get("page", ""),
                "article_number": m.get("article-number", ""),
                "type": m.get("type", ""),
                "publisher": m.get("publisher", ""),
                "crossref_cited_by_count": m.get("is-referenced-by-count", 0),
                "url": m.get("URL", ""),
                "status": "ok",
                "error": "",
            }
        except Exception as exc:
            last_error = str(exc)
            time.sleep(min(2 ** attempt, 15))
    return {"doi": doi, "status": "error", "error": last_error or "retries_exhausted"}


payload = json.loads(INPUT.read_text(encoding="utf-8"))
articles = payload.get("articles", [])
unique = {}
for row in articles:
    doi = norm_doi(row.get("doi", ""))
    if doi:
        unique[doi] = row

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    metadata = list(pool.map(fetch_doi, unique.keys()))

lookup = {x.get("doi"): x for x in metadata}
merged = []
for doi, article in unique.items():
    row = dict(article)
    row.update(lookup.get(doi, {"doi": doi, "status": "missing"}))
    row["agent_year"] = article.get("year")
    merged.append(row)

OUTPUT_JSON.write_text(json.dumps({"count": len(merged), "articles": merged}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

import csv
fields = ["doi", "authors", "agent_year", "title", "journal", "volume", "issue", "page", "article_number", "type", "publisher", "publisher_or_index_url", "finding_and_relevance", "verified_peer_review_evidence", "topics", "status", "year_crossref_print", "year_crossref_online", "year_crossref_issued", "crossref_cited_by_count", "url", "error"]
with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for row in merged:
        writer.writerow({**row, "topics": "; ".join(row.get("topics", [])) if isinstance(row.get("topics"), list) else row.get("topics", "")})

ok = sum(x.get("status") == "ok" for x in merged)
print(f"Crossref validou {ok}/{len(merged)} DOI(s).")
print(f"JSON: {OUTPUT_JSON}")
print(f"CSV: {OUTPUT_CSV}")
