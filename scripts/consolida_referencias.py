#!/usr/bin/env python3
"""Consolida artigos de periódicos, deduplicando DOI e obras com DOI alternativo."""
from __future__ import annotations
import csv
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "data" / "bibliometria"

# A SciELO/Crossref expõe o mesmo artigo em português e inglês sob dois DOI.
# Mantemos o DOI do título original em português e preservamos o alternativo.
CANONICAL_DOI_OVERRIDES = {
    "10.1590/0034-761220240010x": "10.1590/0034-761220240010",
}


def norm_doi(value: str) -> str:
    value = str(value or "").strip()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value, flags=re.I)
    return value.lower().strip().rstrip(".,; ")


def norm_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def work_key(row: dict) -> tuple[str, str, str]:
    title = norm_text(row.get("title", ""))
    authors = str(row.get("authors", "")).split(";")[0]
    author = norm_text(authors)
    year = str(row.get("year", ""))
    return title, author, year


def merge_metadata(existing: dict, incoming: dict, topic: str, source_file: str, doi: str) -> None:
    if topic and topic not in existing.setdefault("topics", []):
        existing["topics"].append(topic)
    if source_file and source_file not in existing.setdefault("source_files", []):
        existing["source_files"].append(source_file)
    alternate_dois = existing.setdefault("alternate_dois", [])
    if doi and doi != existing.get("doi") and doi not in alternate_dois:
        alternate_dois.append(doi)
    second = incoming.get("finding_and_relevance", "")
    findings_by_topic = existing.setdefault("findings_by_topic", {})
    if topic and second and not findings_by_topic.get(topic):
        findings_by_topic[topic] = second
    for field in ("publisher_or_index_url", "verified_peer_review_evidence", "journal", "authors", "title"):
        if not existing.get(field) and incoming.get(field):
            existing[field] = incoming[field]


articles_by_doi: dict[str, dict] = {}
articles_by_work: dict[tuple[str, str, str], dict] = {}
errors: list[dict] = []
inputs = sorted(BIB.glob("eixo_*.txt")) + sorted(BIB.glob("complemento_*.json"))

for path in inputs:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append({"file": path.name, "error": str(exc)})
        continue
    topic = payload.get("topic", path.stem)
    for raw in payload.get("articles", []):
        row = dict(raw)
        doi_original = norm_doi(row.get("doi", ""))
        if not doi_original:
            errors.append({"file": path.name, "title": row.get("title"), "error": "DOI ausente"})
            continue
        doi = CANONICAL_DOI_OVERRIDES.get(doi_original, doi_original)
        row["doi"] = doi
        key = work_key(row)
        duplicate = articles_by_doi.get(doi) or articles_by_work.get(key)
        if duplicate is None:
            row["topics"] = [topic] if topic else []
            row["source_files"] = [path.name]
            row["alternate_dois"] = []
            row["findings_by_topic"] = {topic: row.get("finding_and_relevance", "")} if topic and row.get("finding_and_relevance") else {}
            articles_by_doi[doi] = row
            articles_by_work[key] = row
        else:
            merge_metadata(duplicate, row, topic, path.name, doi_original)
            # Reindex by the canonical DOI if an alternate identifier appeared first.
            canonical = norm_doi(duplicate.get("doi", ""))
            articles_by_doi[canonical] = duplicate
            articles_by_work[key] = duplicate

unique_rows = {norm_doi(row.get("doi", "")): row for row in articles_by_doi.values()}
rows = sorted(unique_rows.values(), key=lambda x: (int(x.get("year") or 0), x.get("authors", ""), x.get("title", "")))
json_path = BIB / "referencias_candidatas.json"
csv_path = BIB / "referencias_candidatas.csv"
json_path.write_text(json.dumps({"unique_count": len(rows), "articles": rows, "parse_errors": errors}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
fields = ["authors", "year", "title", "journal", "doi", "alternate_dois", "publisher_or_index_url", "finding_and_relevance", "verified_peer_review_evidence", "topics", "source_files"]
with csv_path.open("w", encoding="utf-8-sig", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow({**row,
                         "alternate_dois": "; ".join(row.get("alternate_dois", [])),
                         "topics": "; ".join(row.get("topics", [])),
                         "source_files": "; ".join(row.get("source_files", []))})
print(f"Obras únicas com DOI: {len(rows)}; erros de leitura/DOI: {len(errors)}")
print(f"JSON: {json_path}")
print(f"CSV: {csv_path}")
