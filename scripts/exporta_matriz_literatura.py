#!/usr/bin/env python3
"""Gera uma matriz temática de evidências a partir do corpus consolidado/selecionado."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "data" / "bibliometria"
SOURCE = BIB / "referencias_candidatas.json"
SELECTION = BIB / "dois_selecionados.txt"
OUTPUT = BIB / "matriz_literatura.md"


def norm_doi(value: object) -> str:
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", str(value or "").strip(), flags=re.I)
    return text.lower().strip().rstrip(".,; ")

payload = json.loads(SOURCE.read_text(encoding="utf-8"))
articles = payload.get("articles", [])
if SELECTION.exists():
    selected = [norm_doi(line) for line in SELECTION.read_text(encoding="utf-8").splitlines()]
    selected = [doi for doi in selected if doi and not doi.startswith("#")]
    selected_set = set(selected)
    articles = [a for a in articles if norm_doi(a.get("doi")) in selected_set]
    if len(articles) != len(selected):
        raise SystemExit("A seleção contém DOI ausente ou duplicado no corpus consolidado.")

# Um artigo pode pertencer a mais de um eixo; a matriz o registra uma vez por eixo,
# mas declara o total de obras distintas no início.
groups: dict[str, list[dict]] = {}
for article in articles:
    topics = article.get("topics") or ["Sem eixo temático registrado"]
    for topic in topics:
        groups.setdefault(topic, []).append(article)

lines = [
    "# Matriz de literatura científica",
    "",
    f"Corpus: **{len(articles)} obras distintas com DOI**. A matriz associa cada artigo ao achado resumido na triagem e ao eixo temático usado na seleção.",
    f"Organização temática: **{len(groups)} categorias**. Um artigo pode aparecer em mais de uma seção; por isso, as contagens das seções não devem ser somadas como se fossem DOI distintos.",
    "",
    "O resumo de achados serve à síntese do referencial e não substitui a consulta ao artigo original. Os vínculos de DOI e as evidências de publicação/revisão constam em `referencias_candidatas.json` e `crossref_metadata.json`.",
    "",
]
for topic in sorted(groups):
    lines.extend([f"## {topic}", ""])
    seen: set[str] = set()
    for article in sorted(groups[topic], key=lambda a: (int(a.get("year") or 0), a.get("authors", ""), a.get("title", ""))):
        doi = norm_doi(article.get("doi"))
        if doi in seen:
            continue
        seen.add(doi)
        findings_by_topic = article.get("findings_by_topic", {})
        finding = str(findings_by_topic.get(topic) or article.get("finding_and_relevance", "")).strip()
        doi_link = "https://doi.org/" + doi.replace("(", "%28").replace(")", "%29")
        lines.append(f"- **{article.get('authors', 'Autoria não informada')} ({article.get('year', 's.d.')}).** “{article.get('title', '')}”. *{article.get('journal', '')}*. [DOI]({doi_link}). {finding}")
    lines.append("")
while lines and lines[-1] == "":
    lines.pop()
OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Matriz gerada: {OUTPUT}; obras distintas: {len(articles)}; eixos: {len(groups)}")
