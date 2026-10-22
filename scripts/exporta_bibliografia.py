#!/usr/bin/env python3
"""Exporta referências Crossref e overrides editoriais verificados para Typst."""
from __future__ import annotations
import json
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "data" / "bibliometria"
SOURCE = BIB / "crossref_metadata.json"
OVERRIDES = BIB / "metadados_revisados.json"
SELECTION = BIB / "dois_selecionados.txt"
ARTICLE = ROOT / "artigo"
ARTICLE.mkdir(parents=True, exist_ok=True)


def norm_doi(value: object) -> str:
    text = str(value or "").strip()
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", text, flags=re.I)
    return text.lower().strip().rstrip(".,; ")


def url_encode_parentheses(url: str) -> str:
    return str(url or "").replace("(", "%28").replace(")", "%29")


def typst_escape(value: object) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", "", str(value or "")))
    text = re.sub(r"\s+", " ", text).strip()
    for char in ("\\", "#", "*", "_", "[", "]", "$", "<", ">"):
        text = text.replace(char, "\\" + char)
    return text


def no_parentheses(text: str) -> str:
    return text.replace("(", ", ").replace(")", "")


data = json.loads(SOURCE.read_text(encoding="utf-8"))
editorial_overrides = json.loads(OVERRIDES.read_text(encoding="utf-8")) if OVERRIDES.exists() else {}
articles_all = [x for x in data.get("articles", []) if x.get("status") == "ok" and x.get("type") == "journal-article"]
if SELECTION.exists():
    selected = [norm_doi(line) for line in SELECTION.read_text(encoding="utf-8").splitlines()]
    selected = [doi for doi in selected if doi and not doi.startswith("#")]
    if len(set(selected)) != len(selected):
        raise SystemExit("A lista de seleção contém DOI duplicado.")
    by_doi = {norm_doi(x.get("doi")): x for x in articles_all}
    missing = [doi for doi in selected if doi not in by_doi]
    if missing:
        raise SystemExit("DOI selecionado sem metadado Crossref válido: " + ", ".join(missing))
    articles = [by_doi[doi] for doi in selected]
else:
    articles = articles_all


def author_sort_key(item: dict) -> tuple[str, int, str, str]:
    override = editorial_overrides.get(norm_doi(item.get("doi")), {})
    authors = str(override.get("authors_crossref") or item.get("authors_crossref") or item.get("authors") or "")
    lead = authors.split(";", 1)[0].split(",", 1)[0].strip().casefold()
    year = override.get("year") or item.get("agent_year") or item.get("year_crossref_print") or item.get("year_crossref_online") or item.get("year_crossref_issued") or 0
    try:
        year = int(year)
    except (TypeError, ValueError):
        year = 0
    return lead, year, str(item.get("title", "")).casefold(), norm_doi(item.get("doi"))

articles.sort(key=author_sort_key)
if len(articles) < 80:
    print(f"AVISO: há apenas {len(articles)} artigos de periódico verificados; mínimo solicitado: 80.")

citation_map: dict[str, dict] = {}
url_rows = []
typst_lines = [
    "// Gerado por scripts/exporta_bibliografia.py. Não editar manualmente.",
    "= Referências",
    "#set text(size: 8.6pt)",
    "#set par(leading: 0.92em, spacing: 0.35em, first-line-indent: 0pt)",
    "",
]
for idx, item in enumerate(articles, start=1):
    doi = norm_doi(item.get("doi"))
    override = editorial_overrides.get(doi, {})
    url = url_encode_parentheses("https://doi.org/" + doi)
    author = html.unescape(str(override.get("authors_crossref") or item.get("authors_crossref") or item.get("authors") or "Autoria não registrada"))
    year = override.get("year") or item.get("agent_year") or item.get("year_crossref_print") or item.get("year_crossref_online") or item.get("year_crossref_issued") or "s.d."
    title = html.unescape(re.sub(r"<[^>]+>", "", str(override.get("title") or item.get("title", ""))))
    journal = html.unescape(re.sub(r"<[^>]+>", "", str(override.get("journal") or item.get("journal", ""))))
    volume = str(override.get("volume") or item.get("volume", "") or "").strip()
    issue = str(override.get("issue") or item.get("issue", "") or "").strip()
    pages = str(override.get("page") or item.get("page", "") or item.get("article_number", "") or "").strip()
    vol_issue = volume + (f"({issue})" if issue else "") if volume else (f"n. {issue}" if issue else "")
    details = ", ".join(x for x in [vol_issue, pages] if x)
    author_t = typst_escape(author)
    title_t = typst_escape(title)
    journal_t = typst_escape(journal)
    details_t = typst_escape(details)
    year_t = typst_escape(year)
    details_chunk = f", {details_t}" if details_t else ""
    typst_lines.append(
        f'#par[*[{idx}]* {author_t}. ({year_t}). _{title_t}_. {journal_t}{details_chunk}. DOI: #link("{url}")[{typst_escape(doi)}].]'
    )
    desc_parts = [author, str(year), title, journal]
    if volume:
        desc_parts.append(volume + (f", issue {issue}" if issue else ""))
    if pages:
        desc_parts.append(pages)
    desc_parts.append("DOI " + doi)
    desc = no_parentheses(". ".join(x for x in desc_parts if x))
    desc = re.sub(r"\s+", " ", desc).replace('"', "'")
    url_rows.append(f'[{idx}]: {url} "{desc}"')
    citation_map[doi] = {"number": idx, "authors": author, "year": year, "title": title, "journal": journal, "volume": volume, "issue": issue, "pages": pages, "metadata_override": bool(override), "metadata_note": override.get("source_note", ""), "url": url}

typst_lines.extend(["", "#set text(size: 11pt)"])
(ARTICLE / "referencias.typ").write_text("\n".join(typst_lines) + "\n", encoding="utf-8")
reference_urls = "\n".join(f'  "{row["number"]}": "{row["url"]}",' for row in citation_map.values())
doi_numbers = "\n".join(f'  "{doi}": {row["number"]},' for doi, row in citation_map.items())
(ARTICLE / "citacoes.typ").write_text(
    "// Gerado por scripts/exporta_bibliografia.py. Não editar manualmente.\n" +
    "#let reference_urls = (\n" + reference_urls + "\n)\n" +
    "#let doi_to_number = (\n" + doi_numbers + "\n)\n" +
    "#let source_cite(n) = link(reference_urls.at(str(n)))[#text(\"[\" + str(n) + \"]\")]\n" +
    "#let source_doi(doi) = source_cite(doi_to_number.at(str(doi)))\n",
    encoding="utf-8",
)
(ARTICLE / "referencias_links.md").write_text(
    "# Definições de fontes citadas no artigo\n\n" + "\n".join(url_rows) + "\n",
    encoding="utf-8",
)
(BIB / "mapa_citacoes.json").write_text(json.dumps(citation_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Referências de artigos de periódico exportadas: {len(articles)}")
print(f"Typst: {ARTICLE / 'referencias.typ'}; links Markdown: {ARTICLE / 'referencias_links.md'}")
