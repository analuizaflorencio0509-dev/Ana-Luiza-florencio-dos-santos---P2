#!/usr/bin/env python3
"""Seleciona de forma reprodutível o corpus bibliométrico final de 80 artigos."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "data" / "bibliometria"
CANDIDATES = BIB / "referencias_candidatas.json"
CROSSREF = BIB / "crossref_metadata.json"
SELECTION = BIB / "dois_selecionados.txt"
CRITERIA = BIB / "criterios_selecao.md"


def norm_doi(value: object) -> str:
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", str(value or "").strip(), flags=re.I)
    return text.lower().strip().rstrip(".,; ")

candidate_payload = json.loads(CANDIDATES.read_text(encoding="utf-8"))
candidates = candidate_payload.get("articles", [])
by_doi = {norm_doi(a.get("doi")): a for a in candidates}

# Preserve all distinct works in the ten original thematic axes and the professor's
# required Baker et al. reference; add the complete property-tax cluster and five
# direct, methodologically diverse municipal tax-capacity studies.
base_dois = {
    doi for doi, article in by_doi.items()
    if any(str(source).startswith("eixo_") for source in article.get("source_files", []))
    or "Artigo de referência metodológica indicado pelo professor" in article.get("topics", [])
}
property_dois = {
    norm_doi(x) for x in [
        "10.1086/711902",
        "10.1590/0034-7612160295",
        "10.1016/j.ejpoleco.2023.102396",
        "10.1016/j.landusepol.2022.106235",
        "10.1371/journal.pone.0319994",
        "10.1177/0308518X241276871",
        "10.1016/j.jpubeco.2021.104422",
        "10.1016/j.worlddev.2017.02.005",
    ]
}
capacity_dois = {
    norm_doi(x) for x in [
        "10.32586/rcda.v17i1.456",       # frontier of municipal IPTU effort
        "10.4270/ruc.2020320",           # tax efficiency and transfer dependence
        "10.1016/j.ejpoleco.2023.102396", # rural property-tax decentralization
        "10.61673/ren.2022.1317",         # NFS-e and ISS collection
        "10.11606/rco.v10i26.107117",     # NFS-e: contrasting evidence
        "10.18829/rp3.v0i09.21252",       # fiscal effort in Minas Gerais
    ]
}
# The ITR study also occurs in the property-tax cluster; one canonical work counts once.
selected = base_dois | property_dois | capacity_dois
missing = sorted(doi for doi in selected if doi not in by_doi)
if missing:
    raise SystemExit("DOI selecionado ausente do corpus consolidado: " + ", ".join(missing))
if len(base_dois) != 67:
    raise SystemExit(f"Esperados 67 trabalhos-base e Baker; encontrados {len(base_dois)}. Rever fontes e deduplicação.")
if len(property_dois) != 8:
    raise SystemExit("A lista do eixo de imposto predial deve conter oito DOI distintos.")
if len(capacity_dois) != 6:
    raise SystemExit("A lista de capacidade tributária deve conter seis DOI distintos, incluindo o ITR já contado no eixo predial.")
if len(selected) != 80:
    raise SystemExit(f"A seleção precisa conter 80 obras únicas; calculadas: {len(selected)}.")

metadata = json.loads(CROSSREF.read_text(encoding="utf-8")).get("articles", [])
meta_by_doi = {norm_doi(x.get("doi")): x for x in metadata}
for doi in sorted(selected):
    meta = meta_by_doi.get(doi)
    if not meta or meta.get("status") != "ok" or meta.get("type") != "journal-article":
        raise SystemExit(f"Crossref não confirma artigo de periódico para {doi}.")

ordered = sorted(selected)
SELECTION.write_text(
    "# Corpus bibliométrico final — 80 artigos de periódico, DOI normalizados\n"
    "# Seleção: 67 obras originais + 8 do eixo predial + 5 novas obras do eixo de capacidade; ITR é contado uma vez.\n"
    + "\n".join(ordered) + "\n",
    encoding="utf-8",
)
CRITERIA.write_text(
    "# Seleção do corpus bibliométrico\n\n"
    f"A triagem consolidou **{len(candidates)} obras distintas**; Crossref confirmou DOI e tipo `journal-article` para todos os registros. "
    "A amostra final contém **80 artigos**, o mínimo definido no enunciado.\n\n"
    "Foram preservadas 67 obras dos dez eixos temáticos originais, incluindo o artigo Baker, Larcker e Wang indicado como referência metodológica pelo professor. "
    "A seleção acrescenta os oito artigos do eixo de tributação imobiliária municipal e cinco estudos brasileiros adicionais de capacidade/eficiência tributária. "
    "O estudo sobre descentralização do ITR pertence aos dois eixos, mas é contado uma única vez; os complementos incluem fronteira/eficiência do IPTU, esforço fiscal e duas avaliações da NFS-e/ISS com resultados distintos.\n\n"
    "Os demais 11 candidatos suplementares — oito estudos exclusivamente sobre transparência/participação e três estudos adicionais de capacidade tributária — permanecem nos arquivos de triagem, mas não integram o corpus final. "
    "A decisão reduz a sobre-representação de temas já cobertos nos eixos originais e privilegia aderência às variáveis de receitas tributárias próprias, administração da arrecadação e transferências. "
    "A amostra é intencional, temática e não probabilística; portanto, os resultados bibliométricos descrevem somente este corpus e não devem ser tratados como censo da literatura internacional.\n\n"
    "A lista canônica de DOI está em `dois_selecionados.txt`. `scripts/bibliometria.R`, `scripts/exporta_bibliografia.py` e `scripts/exporta_matriz_literatura.py` leem a mesma seleção. "
    "Cada DOI selecionado deve aparecer ao menos uma vez no texto do artigo; a conferência final de cobertura é feita antes da compilação do PDF.\n",
    encoding="utf-8",
)
print(f"Corpus final: {len(selected)} artigos; base: {len(base_dois)}; imposto predial: {len(property_dois)}; capacidade: {len(capacity_dois)} (5 trabalhos novos, após deduplicar o ITR).")
print(f"DOI: {SELECTION}\nCritérios: {CRITERIA}")
