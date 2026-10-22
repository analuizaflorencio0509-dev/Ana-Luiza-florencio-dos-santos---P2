#!/usr/bin/env python3
"""Coleta de dados oficiais para a P2 de Finanças do Setor Público.

Fontes principais: API Siconfi/STN e API SIDRA/IBGE.
O Siconfi limita consultas a uma requisição por segundo; o código respeita esse limite.
Execução: python3 scripts/coleta_dados.py
"""
from __future__ import annotations
import json
import time
from datetime import datetime, timezone
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "brutos"
for sub in ["siconfi", "ibge"]:
    (RAW / sub).mkdir(parents=True, exist_ok=True)

BASE_SICONFI = "https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt"
BASE_SIDRA = "https://apisidra.ibge.gov.br/values"
YEARS = list(range(2015, 2025))
MUNICIPIOS = {4301602: "Bage_RS", 4317103: "Santana_do_Livramento_RS"}
NOMES_MUNICIPIOS = {4301602: "Bagé/RS", 4317103: "Sant'Ana do Livramento/RS"}
ANNEXES = ["DCA-Anexo I-C", "DCA-Anexo I-D"]
S = requests.Session()
S.headers.update({"User-Agent": "P2-FSP-211059333/1.0 (academic data collection)"})
_last_siconfi_call = 0.0

def siconfi_get(endpoint: str, params: dict) -> dict:
    global _last_siconfi_call
    delay = 1.1 - (time.monotonic() - _last_siconfi_call)
    if delay > 0:
        time.sleep(delay)
    url = f"{BASE_SICONFI}/{endpoint}"
    r = S.get(url, params=params, timeout=60)
    _last_siconfi_call = time.monotonic()
    r.raise_for_status()
    data = r.json()
    items = data.get("items", [])
    # Respect API pagination if any response exceeds its first page.
    while data.get("hasMore"):
        offset = int(data.get("offset", 0)) + int(data.get("limit", 5000))
        p = dict(params, offset=offset)
        delay = 1.1 - (time.monotonic() - _last_siconfi_call)
        if delay > 0:
            time.sleep(delay)
        r = S.get(url, params=p, timeout=60)
        _last_siconfi_call = time.monotonic()
        r.raise_for_status()
        data = r.json()
        items.extend(data.get("items", []))
    return {"items": items, "source_url": r.url, "retrieved_at_utc": datetime.now(timezone.utc).isoformat()}

def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# Homologation metadata: do not treat missing or unhomologated annual reports as zero.
status_rows = []
for year in YEARS:
    for code, slug in MUNICIPIOS.items():
        data = siconfi_get("extrato_entregas", {"an_referencia": year, "id_ente": code})
        save_json(RAW / "siconfi" / f"extrato_{slug}_{year}.json", data)
        dca = [x for x in data["items"] if x.get("entregavel") == "Balanço Anual (DCA)" and x.get("periodicidade") == "A"]
        status_rows.append({
            "ano": year, "codigo_ibge": code, "municipio": NOMES_MUNICIPIOS[code],
            "dca_registros": len(dca),
            "status_relatorio": ";".join(str(x.get("status_relatorio")) for x in dca) or None,
            "data_status": ";".join(str(x.get("data_status")) for x in dca) or None,
            "forma_envio": ";".join(str(x.get("forma_envio")) for x in dca) or None,
        })

# Annual DCA revenue and expenditure annexes.
count = 0
for year in YEARS:
    for code, slug in MUNICIPIOS.items():
        for annex in ANNEXES:
            count += 1
            data = siconfi_get("dca", {"an_exercicio": year, "id_ente": code, "no_anexo": annex})
            short = "receitas_I_C" if annex.endswith("I-C") else "despesas_I_D"
            data["query"] = {"an_exercicio": year, "id_ente": code, "no_anexo": annex}
            save_json(RAW / "siconfi" / f"dca_{slug}_{year}_{short}.json", data)
            if count % 10 == 0:
                print(f"DCA requests saved: {count}/{len(YEARS)*len(MUNICIPIOS)*len(ANNEXES)}", flush=True)

# IBGE SIDRA: annual population estimates, municipal GDP (latest complete series), and monthly IPCA.
queries = {
    "populacao_2015_2024.json": f"{BASE_SIDRA}/t/6579/n6/4301602,4317103/v/9324/p/2015-2024?formato=json",
    "populacao_censo_2022.json": f"{BASE_SIDRA}/t/4709/n6/4301602,4317103/v/93/p/2022?formato=json",
    "pib_municipal_2015_2023.json": f"{BASE_SIDRA}/t/5938/n6/4301602,4317103/v/all/p/2015-2023?formato=json",
    "ipca_indice_2015_2024.json": f"{BASE_SIDRA}/t/1737/n1/1/v/2266/p/201501-202412?formato=json",
}
for filename, url in queries.items():
    r = S.get(url, timeout=90)
    r.raise_for_status()
    payload = {
        "source_url": r.url,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "records": r.json(),
    }
    save_json(RAW / "ibge" / filename, payload)
    print(f"Saved {filename}: {len(payload['records'])} rows", flush=True)

# Record the retrieval and source basis for reproducibility.
manifest = {
    "retrieval_timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "analysis_period": [2015, 2024],
    "municipalities": {str(code): NOMES_MUNICIPIOS[code] for code in MUNICIPIOS},
    "municipality_file_slugs": {str(code): slug for code, slug in MUNICIPIOS.items()},
    "siconfi_api": "https://apidatalake.tesouro.gov.br/docs/siconfi/",
    "siconfi_rate_limit_respected_seconds": 1.1,
    "siconfi_delivery_status": status_rows,
    "sidra_sources": queries,
    "notes": [
        "DCA (Anexo I-C) e DCA (Anexo I-D) foram coletadas separadamente para cada município e ano.",
        "As contas anuais sem declaração homologada devem ser tratadas como ausentes, nunca como zero.",
        "A população anual para per capita vem do IBGE/SIDRA, não do campo populacional constante no Siconfi.",
        "A tabela SIDRA 6579 não contém estimativas municipais para 2022 e 2023; a população de 2022 foi obtida separadamente do Censo Demográfico 2022 (tabela SIDRA 4709, variável 93), e 2023 permanece ausente.",
        "A série de PIB municipal do IBGE tem cobertura mais curta que a série fiscal e será identificada como tal."
    ]
}
save_json(RAW / "manifesto_coleta.json", manifest)
print("Collection completed.", flush=True)
