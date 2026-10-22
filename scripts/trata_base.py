#!/usr/bin/env python3
"""Tratamento e análise descritiva da base fiscal P2 (2015-2024).

Entradas: JSON bruto do Siconfi e SIDRA, planilha e PDF oficiais do DIPRES.
Saídas: CSVs tratados, tabelas descritivas, figuras e uma planilha editável.
Não substitui observações ausentes por zero e não estima relações causais.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.comments import Comment

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "brutos"
OUT = ROOT / "data" / "tratados"
ANALYSIS = ROOT / "analise"
FIG = ROOT / "figuras"
for p in (OUT, ANALYSIS, FIG):
    p.mkdir(parents=True, exist_ok=True)

YEARS = list(range(2015, 2025))
MUNICIPIOS = {
    4301602: "Bagé/RS",
    4317103: "Sant'Ana do Livramento/RS",
}
SLUGS = {4301602: "Bage_RS", 4317103: "Santana_do_Livramento_RS"}
API_SICONFI = "https://apidatalake.tesouro.gov.br/docs/siconfi/"
SIDRA_POP = "https://apisidra.ibge.gov.br/values/t/6579/n6/4301602,4317103/v/9324/p/2015-2024?formato=json"
SIDRA_PIB = "https://apisidra.ibge.gov.br/values/t/5938/n6/4301602,4317103/v/all/p/2015-2023?formato=json"
SIDRA_IPCA = "https://apisidra.ibge.gov.br/values/t/1737/n1/1/v/2266/p/201501-202412?formato=json"
DIPRES_XLSX = RAW / "chile" / "dipres_efp_general_2016_2025.xlsx"
DIPRES_PDF = RAW / "chile" / "dipres_efp_2015_2024.pdf"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def numeric_or_none(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def account_label(row):
    text = str(row.get("conta") or "").strip()
    return text.split(" - ", 1)[1].strip() if " - " in text else text


def sum_rows(rows):
    vals = [numeric_or_none(r.get("valor")) for r in rows]
    vals = [v for v in vals if v is not None]
    return sum(vals) if vals else None


def exact_total(rows, code, col):
    matched = [r for r in rows if str(r.get("cod_conta")) == code and r.get("coluna") == col]
    return sum_rows(matched)


def exact_label_sum(rows, label, col):
    needle = label.casefold()
    matched = [r for r in rows if account_label(r).casefold() == needle and r.get("coluna") == col]
    return sum_rows(matched)


def deduction_sum(rows, code=None):
    matched = [r for r in rows if is_deduction_column(r.get("coluna")) and (code is None or str(r.get("cod_conta")) == code)]
    return sum_rows(matched)


def is_deduction_column(column):
    text = str(column or "")
    return text.startswith("Deduções - ") or text == "Outras Deduções da Receita"


def get_brazil_annual(year: int, code: int):
    slug = SLUGS[code]
    rev_path = RAW / "siconfi" / f"dca_{slug}_{year}_receitas_I_C.json"
    exp_path = RAW / "siconfi" / f"dca_{slug}_{year}_despesas_I_D.json"
    rev = read_json(rev_path).get("items", [])
    exp = read_json(exp_path).get("items", [])

    gross_total = exact_total(rev, "TotalReceitas", "Receitas Brutas Realizadas")
    total_ded = deduction_sum(rev, "TotalReceitas")
    # The DCA total includes intrabudgetary receipts. Remove only the top-level
    # intrabudgetary categories to prevent double counting; descendants are not summed.
    intra_labels = {"receitas correntes intraorçamentárias", "receitas de capital intraorçamentárias"}
    intra_roots = [r for r in rev if (str(r.get("cod_conta", "")).startswith("RI") and account_label(r).casefold() in intra_labels) or str(r.get("cod_conta")) == "ReceitasIntraOrcamentarias" or str(r.get("cod_conta", "")).startswith(("RO7.0.0.0", "RO8.0.0.0"))]
    intra_gross = sum_rows([r for r in intra_roots if r.get("coluna") == "Receitas Brutas Realizadas"])
    if intra_gross is None:
        excluded_gross = exact_total(rev, "ReceitasExcetoIntraOrcamentarias", "Receitas Brutas Realizadas")
        if excluded_gross is not None and gross_total is not None:
            intra_gross = gross_total - excluded_gross
        else:
            nonintra_roots = [r for r in rev if str(r.get("cod_conta", "")).startswith(("RO1.0.0.0", "RO2.0.0.0")) and r.get("coluna") == "Receitas Brutas Realizadas"]
            nonintra_gross = sum_rows(nonintra_roots)
            if nonintra_gross is not None and gross_total is not None and abs(gross_total - nonintra_gross) < 1.0:
                intra_gross = 0.0
    intra_ded = sum_rows([r for r in intra_roots if is_deduction_column(r.get("coluna"))])
    if intra_ded is None and intra_gross == 0:
        intra_ded = 0.0
    intra_net = None if intra_gross is None else intra_gross - (intra_ded or 0)

    net_revenue = None
    if gross_total is not None and total_ded is not None and intra_net is not None:
        net_revenue = gross_total - total_ded - intra_net

    transfer_current = exact_label_sum(rev, "Transferências Correntes", "Receitas Brutas Realizadas")
    transfer_capital = exact_label_sum(rev, "Transferências de Capital", "Receitas Brutas Realizadas")
    transfer_current_ded = sum_rows([r for r in rev if account_label(r).casefold() == "transferências correntes" and is_deduction_column(r.get("coluna"))])
    transfer_capital_ded = sum_rows([r for r in rev if account_label(r).casefold() == "transferências de capital" and is_deduction_column(r.get("coluna"))])
    broad_transfers_net = None
    if transfer_current is not None and transfer_capital is not None:
        broad_transfers_net = transfer_current + transfer_capital - (transfer_current_ded or 0) - (transfer_capital_ded or 0)

    # Harmonized current intergovernmental transfers: the older DCA layout
    # reports a single intergovernmental parent (1.7.2); the newer layout
    # separates Union, states/DF, and municipalities (1.7.1-1.7.3).
    intergov_prefixes = ("RO1.7.2.0",) if year <= 2017 else ("RO1.7.1.0", "RO1.7.2.0", "RO1.7.3.0")
    def is_intergov_root(row):
        account_code = str(row.get("cod_conta", ""))
        return any(account_code == prefix or account_code.startswith(prefix + ".") for prefix in intergov_prefixes)
    intergov_rows = [r for r in rev if is_intergov_root(r)]
    intergov_gross = sum_rows([r for r in intergov_rows if r.get("coluna") == "Receitas Brutas Realizadas"])
    intergov_ded = sum_rows([r for r in intergov_rows if is_deduction_column(r.get("coluna"))])
    intergov_net = None if intergov_gross is None else intergov_gross - (intergov_ded or 0)
    residual_revenue = None if net_revenue is None or intergov_net is None else net_revenue - intergov_net
    tax_revenue = None
    for tax_label in ["Impostos, Taxas e Contribuições de Melhoria", "Receita Tributária", "Receitas Tributárias"]:
        tax_revenue = exact_label_sum(rev, tax_label, "Receitas Brutas Realizadas")
        if tax_revenue is not None:
            break
    liquidated_exp = exact_total(exp, "TotalDespesas", "Despesas Liquidadas")

    return {
        "ano": year,
        "codigo_ibge": code,
        "municipio": MUNICIPIOS[code],
        "receita_total_bruta_incl_intra_R$": gross_total,
        "deducoes_receita_total_R$": total_ded,
        "receita_intra_liquida_removida_R$": intra_net,
        "receita_orcamentaria_liquida_R$": net_revenue,
        "transferencias_correntes_brutas_R$": transfer_current,
        "transferencias_capital_brutas_R$": transfer_capital,
        "transferencias_correntes_e_capital_liquidas_amplas_R$": broad_transfers_net,
        "transferencias_intergovernamentais_correntes_brutas_R$": intergov_gross,
        "deducoes_transferencias_intergovernamentais_correntes_R$": intergov_ded,
        "transferencias_intergovernamentais_liquidas_R$": intergov_net,
        "receita_liquida_residual_apos_transferencias_intergovernamentais_R$": residual_revenue,
        "receita_tributaria_propria_R$": tax_revenue,
        "despesa_liquidada_R$": liquidated_exp,
        "linhas_receita_anexo_I_C": len(rev),
        "linhas_despesa_anexo_I_D": len(exp),
    }

# Population estimates and 2022 Census population from official IBGE/SIDRA data.
pop_obj = read_json(RAW / "ibge" / "populacao_2015_2024.json")
pop_records = pop_obj.get("records", [])
pop_df = pd.DataFrame(pop_records[1:])
if not pop_df.empty:
    pop_df["ano"] = pd.to_numeric(pop_df["D3C"], errors="coerce")
    pop_df["codigo_ibge"] = pd.to_numeric(pop_df["D1C"], errors="coerce")
    pop_df["populacao"] = pd.to_numeric(pop_df["V"], errors="coerce")
    pop_df = pop_df[["ano", "codigo_ibge", "D1N", "populacao"]].rename(columns={"D1N": "municipio_ibge"})
    pop_df["fonte_populacao"] = "IBGE/SIDRA 6579, v. 9324 — estimativa anual"
else:
    pop_df = pd.DataFrame(columns=["ano", "codigo_ibge", "municipio_ibge", "populacao", "fonte_populacao"])
census_obj = read_json(RAW / "ibge" / "populacao_censo_2022.json")
census_records = census_obj.get("records", [])
census_df = pd.DataFrame(census_records[1:])
if not census_df.empty:
    census_df["ano"] = pd.to_numeric(census_df["D3C"], errors="coerce")
    census_df["codigo_ibge"] = pd.to_numeric(census_df["D1C"], errors="coerce")
    census_df["populacao"] = pd.to_numeric(census_df["V"], errors="coerce")
    census_df = census_df[["ano", "codigo_ibge", "D1N", "populacao"]].rename(columns={"D1N": "municipio_ibge"})
    census_df["fonte_populacao"] = "IBGE/SIDRA 4709, v. 93 — Censo Demográfico 2022"
    pop_df = pd.concat([pop_df, census_df], ignore_index=True)
pop_df = pop_df.sort_values(["codigo_ibge", "ano"]).drop_duplicates(["codigo_ibge", "ano"], keep="last")
pop_df.to_csv(OUT / "populacao_ibge_sidra.csv", index=False, encoding="utf-8-sig")

pib_obj = read_json(RAW / "ibge" / "pib_municipal_2015_2023.json")
pib_records = pib_obj.get("records", [])
pib_df = pd.DataFrame(pib_records[1:])
if not pib_df.empty:
    pib_df["ano"] = pd.to_numeric(pib_df["D3C"], errors="coerce")
    pib_df["codigo_ibge"] = pd.to_numeric(pib_df["D1C"], errors="coerce")
    pib_df["variavel"] = pd.to_numeric(pib_df["D2C"], errors="coerce")
    pib_df["valor_mil_R$" ] = pd.to_numeric(pib_df["V"], errors="coerce")
    pib_df["unidade"] = pib_df["MN"]
    pib_df = pib_df[pib_df["variavel"] == 37].copy()
    pib_df["pib_nominal_R$"] = pib_df["valor_mil_R$"] * 1000
    pib_df = pib_df[["ano", "codigo_ibge", "D1N", "D2N", "unidade", "valor_mil_R$", "pib_nominal_R$"]].rename(columns={"D1N": "municipio_ibge", "D2N": "variavel_ibge"})
else:
    pib_df = pd.DataFrame(columns=["ano", "codigo_ibge", "municipio_ibge", "variavel_ibge", "unidade", "valor_mil_R$", "pib_nominal_R$"])
pib_df.to_csv(OUT / "pib_municipal_ibge_sidra.csv", index=False, encoding="utf-8-sig")

# IPCA: annual-average index and annual-average-price deflator, with 2024=100 basis.
ipca_obj = read_json(RAW / "ibge" / "ipca_indice_2015_2024.json")
ipca_records = ipca_obj.get("records", [])
ipca = pd.DataFrame(ipca_records[1:])
if not ipca.empty:
    ipca["periodo"] = pd.to_numeric(ipca["D3C"], errors="coerce")
    ipca["ano"] = (ipca["periodo"] // 100).astype("Int64")
    ipca["indice"] = pd.to_numeric(ipca["V"], errors="coerce")
    ipca_annual = ipca.groupby("ano", as_index=False)["indice"].mean().rename(columns={"indice": "ipca_indice_medio_anual"})
else:
    ipca_annual = pd.DataFrame(columns=["ano", "ipca_indice_medio_anual"])
base_index = ipca_annual.loc[ipca_annual["ano"] == 2024, "ipca_indice_medio_anual"]
if len(base_index) == 0:
    raise RuntimeError("IPCA 2024 indisponível; não calcular valores reais sem deflator.")
base_index = float(base_index.iloc[0])
ipca_annual["fator_deflacao_base_2024"] = base_index / ipca_annual["ipca_indice_medio_anual"]
ipca_annual.to_csv(OUT / "ipca_anual_deflator_2024.csv", index=False, encoding="utf-8-sig")

# Annual Brazil municipal fiscal panel.
rows = [get_brazil_annual(year, code) for year in YEARS for code in MUNICIPIOS]
br = pd.DataFrame(rows)
br = br.merge(pop_df[["ano", "codigo_ibge", "populacao", "fonte_populacao"]], on=["ano", "codigo_ibge"], how="left")
br = br.merge(pib_df[["ano", "codigo_ibge", "pib_nominal_R$"]], on=["ano", "codigo_ibge"], how="left")
br = br.merge(ipca_annual[["ano", "fator_deflacao_base_2024"]], on="ano", how="left")
for raw_col, real_col in [
    ("receita_orcamentaria_liquida_R$", "receita_liquida_real_2024_R$"),
    ("transferencias_intergovernamentais_liquidas_R$", "transferencias_intergovernamentais_reais_2024_R$"),
    ("receita_liquida_residual_apos_transferencias_intergovernamentais_R$", "receita_residual_apos_transferencias_intergovernamentais_real_2024_R$"),
    ("receita_tributaria_propria_R$", "receita_tributaria_real_2024_R$"),
    ("despesa_liquidada_R$", "despesa_liquidada_real_2024_R$"),
]:
    br[real_col] = br[raw_col] * br["fator_deflacao_base_2024"]
for col, name in [
    ("receita_liquida_real_2024_R$", "receita_real_per_capita_2024_R$"),
    ("transferencias_intergovernamentais_reais_2024_R$", "transferencia_intergovernamental_real_per_capita_2024_R$"),
    ("receita_tributaria_real_2024_R$", "tributos_reais_per_capita_2024_R$"),
    ("despesa_liquidada_real_2024_R$", "despesa_real_liquidada_per_capita_2024_R$"),
]:
    br[name] = br[col] / br["populacao"]
br["participacao_transferencias_pct_receita"] = 100 * br["transferencias_intergovernamentais_liquidas_R$"] / br["receita_orcamentaria_liquida_R$"]
br["participacao_tributos_pct_receita"] = 100 * br["receita_tributaria_propria_R$"] / br["receita_orcamentaria_liquida_R$"]
br["receita_liquida_pct_PIB"] = 100 * br["receita_orcamentaria_liquida_R$"] / br["pib_nominal_R$"]
br["tributos_pct_PIB"] = 100 * br["receita_tributaria_propria_R$"] / br["pib_nominal_R$"]
br["despesa_liquidada_pct_PIB"] = 100 * br["despesa_liquidada_R$"] / br["pib_nominal_R$"]
br.to_csv(OUT / "painel_fiscal_municipios_2015_2024.csv", index=False, encoding="utf-8-sig")

# Chile: current DIPRES workbook carries finalized 2016-2024 series and a provisional 2025.
# The 2015 observation is taken from the official 2015-2024 edition; 2024 from that edition
# is not used because it was explicitly marked provisional.
def year_from_cell(x):
    m = re.search(r"(201[0-9]|202[0-9])", str(x))
    return int(m.group(1)) if m else None

chile_rows = []
if DIPRES_XLSX.exists():
    wb = load_workbook(DIPRES_XLSX, read_only=True, data_only=True)
    ws = wb["EOM%PIB"]
    header = None
    for row in ws.iter_rows(values_only=True):
        years_found = {i: year_from_cell(v) for i, v in enumerate(row) if year_from_cell(v)}
        if 2016 in years_found.values() and 2024 in years_found.values():
            header = years_found
            break
    if header is None:
        raise RuntimeError("Cabeçalho de anos 2016-2024 não localizado em EOM%PIB do DIPRES.")
    measures = {}
    for row in ws.iter_rows(values_only=True):
        label = str(row[0] or "").strip()
        key = re.sub(r"\d+$", "", label).strip().casefold()
        mapping = {
            "ingresos": "receita_total_pct_PIB",
            "ingresos tributarios netos": "receita_tributaria_pct_PIB",
            "donaciones": "donaciones_pct_PIB",
            "gastos": "despesa_total_pct_PIB",
            "resultado operativo neto": "resultado_operativo_neto_pct_PIB",
            "total ingresos": "receita_total_ampliada_pct_PIB",
            "total gastos": "despesa_total_ampliada_pct_PIB",
        }
        for label_key, col in mapping.items():
            if key.casefold() == label_key:
                for idx, year in header.items():
                    if 2016 <= year <= 2024 and idx < len(row):
                        measures.setdefault(year, {})[col] = numeric_or_none(row[idx])
    for year, vals in sorted(measures.items()):
        if 2016 <= year <= 2024:
            vals.update({"ano": year, "origem_vintage": "DIPRES EFP 2016-2025; revisão atual consultada em 2026; 2025 excluído por provisório"})
            chile_rows.append(vals)
    wb.close()
else:
    print(f"AVISO: arquivo DIPRES não encontrado: {DIPRES_XLSX}", file=sys.stderr)

# Obtain 2015 ratios from the published 2015-2024 DIPRES table (page printed 55).
if DIPRES_PDF.exists():
    proc = subprocess.run(["pdftotext", "-f", "57", "-l", "57", "-layout", str(DIPRES_PDF), "-"], capture_output=True, text=True, check=True)
    lines = proc.stdout.splitlines()
    map_2015 = {
        "ingresos": "receita_total_pct_PIB",
        "ingresos tributarios netos": "receita_tributaria_pct_PIB",
        "donaciones": "donaciones_pct_PIB",
        "gastos": "despesa_total_pct_PIB",
        "resultado operativo neto": "resultado_operativo_neto_pct_PIB",
        "total ingresos": "receita_total_ampliada_pct_PIB",
        "total gastos": "despesa_total_ampliada_pct_PIB",
    }
    vals = {}
    for line in lines:
        stripped = line.strip()
        parts = re.split(r"\s{2,}", stripped, maxsplit=1)
        if len(parts) != 2:
            continue
        label = re.sub(r"\d+$", "", parts[0]).strip().casefold()
        col = map_2015.get(label)
        nums = re.findall(r"-?\d+(?:,\d+)?", parts[1])
        if col and nums:
            vals[col] = float(nums[0].replace(",", "."))
    if "receita_total_pct_PIB" in vals:
        vals.update({"ano": 2015, "origem_vintage": "DIPRES EFP 2015-2024, tabela municipal p. 55; valor de 2015 (último ano não provisório nessa edição)"})
        chile_rows.append(vals)
else:
    print(f"AVISO: PDF DIPRES não encontrado: {DIPRES_PDF}", file=sys.stderr)

ch = pd.DataFrame(chile_rows).sort_values("ano")
if not ch.empty:
    ch["participacao_tributos_pct_receita"] = 100 * ch["receita_tributaria_pct_PIB"] / ch["receita_total_pct_PIB"]
    ch["participacao_donaciones_pct_receita"] = 100 * ch["donaciones_pct_PIB"] / ch["receita_total_pct_PIB"]
    ch["escopo"] = "Agregado consolidado das municipalidades do Chile"
ch.to_csv(OUT / "chile_municipalidades_dipres_pct_pib.csv", index=False, encoding="utf-8-sig")

# Validate data states and coverage.
manifest = read_json(RAW / "manifesto_coleta.json")
status = pd.DataFrame(manifest.get("siconfi_delivery_status", []))
if not status.empty and "codigo_ibge" in status:
    status["municipio"] = status["codigo_ibge"].map(MUNICIPIOS).fillna(status.get("municipio"))
status.to_csv(OUT / "status_entregas_siconfi.csv", index=False, encoding="utf-8-sig")
status_ok = status[status["status_relatorio"].astype(str).isin(["HO", "RE"])].copy() if not status.empty else pd.DataFrame()
coverage = {
    "periodo_fiscal_brasil": [2015, 2024],
    "n_municipio_anos_brasil": int(len(br)),
    "n_receita_ausente": int(br["receita_orcamentaria_liquida_R$"].isna().sum()),
    "n_despesa_ausente": int(br["despesa_liquidada_R$"].isna().sum()),
    "n_populacao_ausente": int(br["populacao"].isna().sum()),
    "anos_populacao_disponiveis": sorted(int(x) for x in pop_df["ano"].dropna().unique()),
    "anos_populacao_ausentes": sorted(int(x) for x in set(YEARS) - set(pop_df["ano"].dropna().astype(int))),
    "periodo_pib_municipal": [int(pib_df["ano"].min()) if len(pib_df) else None, int(pib_df["ano"].max()) if len(pib_df) else None],
    "n_pib_ausente": int(br["pib_nominal_R$"].isna().sum()),
    "status_dca_homologado_ou_retificado": int(len(status_ok)),
    "status_dca_total_ente_ano": int(len(status)),
    "periodo_chile": [int(ch["ano"].min()) if len(ch) else None, int(ch["ano"].max()) if len(ch) else None],
    "n_anos_chile": int(len(ch)),
    "observacao": "Ausências ficam como NaN/blank. População 2015-2021 e 2024: estimativas IBGE/SIDRA 6579; 2022: Censo 2022/SIDRA 4709; 2023: sem estimativa municipal anual, mantida ausente. Chile 2015 vem da edição DIPRES 2015-2024; anos 2016-2024 da edição atualizada 2016-2025, excluído 2025 provisório."
}
(ANALYSIS / "cobertura_e_validacoes.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8")

# Descriptive summary at the municipality level.
metric_cols = ["receita_real_per_capita_2024_R$", "transferencia_intergovernamental_real_per_capita_2024_R$", "tributos_reais_per_capita_2024_R$", "despesa_real_liquidada_per_capita_2024_R$", "participacao_transferencias_pct_receita", "participacao_tributos_pct_receita", "receita_liquida_pct_PIB"]
summary_rows = []
for (code, municipio), group in br.groupby(["codigo_ibge", "municipio"]):
    for metric in metric_cols:
        valid = group.dropna(subset=[metric]).sort_values("ano")
        summary_rows.append({
            "codigo_ibge": code, "municipio": municipio, "indicador": metric,
            "ano_inicial": int(valid["ano"].min()) if len(valid) else None,
            "valor_inicial": float(valid.iloc[0][metric]) if len(valid) else None,
            "ano_final": int(valid["ano"].max()) if len(valid) else None,
            "valor_final": float(valid.iloc[-1][metric]) if len(valid) else None,
            "variacao_pct": float((valid.iloc[-1][metric] / valid.iloc[0][metric] - 1) * 100) if len(valid) > 1 and valid.iloc[0][metric] not in (0, None) else None,
            "n_observacoes": int(len(valid)),
        })
summary = pd.DataFrame(summary_rows)
summary.to_csv(ANALYSIS / "resumo_descritivo.csv", index=False, encoding="utf-8-sig")

# Figures; all prices in annual-average 2024 reais, Chile ratios are not overlaid with city-level ratios.
plt.style.use("seaborn-v0_8-whitegrid")
colors = {4301602: "#245B8F", 4317103: "#D97706"}
fig, ax = plt.subplots(figsize=(9.5, 5.2))
for code, group in br.groupby("codigo_ibge"):
    group = group.sort_values("ano")
    valid = group.dropna(subset=["receita_real_per_capita_2024_R$"])
    ax.plot(valid["ano"], valid["receita_real_per_capita_2024_R$"], linestyle="none", marker="o", color=colors[code], label=MUNICIPIOS[code])
ax.set_title("Receita orçamentária líquida real por habitante")
ax.set_ylabel("R$ de 2024 por habitante")
ax.set_xlabel("Ano")
ax.set_xticks(YEARS)
ax.set_xticklabels([f"{year}*" if year == 2023 else str(year) for year in YEARS], fontsize=8)
ax.legend(frameon=False)
fig.text(0.5, 0.01, "*2023: população municipal anual indisponível; valor per capita não calculado.", ha="center", fontsize=8)
fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(FIG / "receita_per_capita_real.png", dpi=220); plt.close(fig)

fig, ax = plt.subplots(figsize=(9.5, 5.2))
for code, group in br.groupby("codigo_ibge"):
    group = group.sort_values("ano")
    ax.plot(group["ano"], group["participacao_transferencias_pct_receita"], marker="o", linewidth=2, color=colors[code], label=MUNICIPIOS[code])
    ax.set_title("Participação das transferências intergovernamentais correntes na receita municipal")
ax.set_ylabel("% da receita orçamentária líquida")
ax.set_xlabel("Ano")
ax.legend(frameon=False)
fig.tight_layout(); fig.savefig(FIG / "dependencia_transferencias.png", dpi=220); plt.close(fig)

fig, ax = plt.subplots(figsize=(9.5, 5.2))
for code, group in br.groupby("codigo_ibge"):
    group = group.sort_values("ano")
    ax.plot(group["ano"], group["receita_liquida_pct_PIB"], marker="o", linewidth=2, color=colors[code], label=MUNICIPIOS[code])
ax.set_title("Receita municipal líquida em relação ao PIB municipal")
ax.set_ylabel("% do PIB municipal")
ax.set_xlabel("Ano")
ax.legend(frameon=False)
fig.tight_layout(); fig.savefig(FIG / "receita_municipal_pct_pib.png", dpi=220); plt.close(fig)

fig, (ax_receita, ax_gastos) = plt.subplots(2, 1, figsize=(9.5, 7.2), sharex=True)
if not ch.empty:
    ax_receita.plot(ch["ano"], ch["participacao_tributos_pct_receita"], marker="o", linewidth=2, color="#245B8F", label="Ingresos tributarios netos / Ingresos")
    ax_receita.plot(ch["ano"], ch["participacao_donaciones_pct_receita"], marker="o", linewidth=2, color="#D97706", label="Donaciones / Ingresos")
    ax_gastos.plot(ch["ano"], ch["despesa_total_pct_PIB"], marker="s", linewidth=1.8, linestyle="--", color="#4B5563", label="Gastos / PIB nacional")
ax_receita.set_title("Composição dos Ingresos municipalizados")
ax_receita.set_ylabel("% de Ingresos")
ax_receita.set_ylim(0, 50)
ax_receita.legend(frameon=False, fontsize=8)
ax_gastos.set_title("Gastos das municipalidades")
ax_gastos.set_ylabel("% do PIB nacional")
ax_gastos.set_xlabel("Ano")
ax_gastos.set_ylim(0, 5)
ax_gastos.legend(frameon=False, fontsize=8)
fig.suptitle("Chile: composição das receitas e gastos municipais", y=0.99)
fig.text(0.5, 0.01, "2015: edição DIPRES 2015–2024; 2016–2024: edição atualizada 2016–2025.", ha="center", fontsize=8)
fig.tight_layout(rect=(0, 0.04, 1, 0.96)); fig.savefig(FIG / "chile_municipalidades_contexto.png", dpi=220); plt.close(fig)

# Workbook: editable source data and derived series, with source comments and unit-aware display.
wb = Workbook()
wb.remove(wb.active)
wb.properties.creator = "Ana Luiza Florêncio dos Santos"
wb.properties.lastModifiedBy = "Ana Luiza Florêncio dos Santos"
wb.properties.title = "Base fiscal — P2 Finanças do Setor Público — 2015–2024"
wb.properties.subject = "Ana Luiza Florêncio dos Santos — matrícula 211059333"
wb.properties.description = "Painel fiscal reproduzível de Bagé, Sant'Ana do Livramento e agregado municipal do Chile."
source_comment = "Fonte: Siconfi/STN, Declaração das Contas Anuais (DCA), Anexos I-C/I-D; exercício e ente identificados na linha. Extraído em 21/10/2026 pela API oficial."

def number_format(column, row_values):
    key = str(column).casefold()
    indicator = str(row_values.get("indicador", "")).casefold()
    if key in {"ano", "ano_inicial", "ano_final", "codigo_ibge"}:
        return "0"
    if key in {"populacao", "dca_registros", "n_observacoes"} or key.startswith("linhas_"):
        return '#,##0;(#,##0);"-"'
    if key == "variacao_pct":
        return '0.0"%";(0.0"%");"-"'
    if "pct" in key or (key in {"valor_inicial", "valor_final"} and "pct" in indicator):
        return '0.00"%";(0.00"%");"-"'
    if "r$" in key or "per_capita" in key or "pib_nominal" in key or key in {"valor_inicial", "valor_final"}:
        return '#,##0.00;(#,##0.00);"-"'
    return '#,##0.00;(#,##0.00);"-"'

def add_sheet(name, title, df, unit_note="", source=source_comment, subtitle=""):
    ws = wb.create_sheet(name)
    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 20
    last_col = 2 + len(df.columns)
    ws.cell(3, 3, title)
    for col_idx in range(3, last_col + 1):
        cell = ws.cell(3, col_idx)
        cell.fill = PatternFill("solid", fgColor="135B44")
        cell.font = Font(name="Arial", size=16, bold=True, color="FFFFFF")
    ws.cell(3, 3).alignment = Alignment(vertical="center")
    ws.row_dimensions[3].height = 26
    ws.cell(5, 3, subtitle)
    ws.cell(5, 3).font = Font(name="Arial", size=11, bold=True)
    ws.cell(5, 3).alignment = Alignment(wrap_text=True, vertical="center")
    ws.cell(6, 3, unit_note)
    ws.cell(6, 3).font = Font(name="Arial", size=10, italic=True)
    ws.cell(6, 3).alignment = Alignment(wrap_text=True, vertical="center")
    if last_col > 3:
        ws.merge_cells(start_row=5, start_column=3, end_row=5, end_column=last_col)
        ws.merge_cells(start_row=6, start_column=3, end_row=6, end_column=last_col)
    ws.row_dimensions[5].height = 24
    ws.row_dimensions[6].height = 30
    for j, col in enumerate(df.columns, 3):
        c = ws.cell(8, j, str(col))
        c.font = Font(name="Arial", bold=True)
        c.fill = PatternFill("solid", fgColor="CFE9E0")
        c.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[8].height = 42
    for i, row in enumerate(df.itertuples(index=False, name=None), 9):
        row_values = dict(zip(df.columns, row))
        for j, value in enumerate(row, 3):
            if pd.isna(value):
                value = None
            c = ws.cell(i, j, value.item() if hasattr(value, "item") else value)
            c.font = Font(name="Arial", color="0000FF")
            column_name = df.columns[j - 3]
            if pd.api.types.is_numeric_dtype(df[column_name].dtype):
                c.number_format = number_format(column_name, row_values)
                c.alignment = Alignment(horizontal="right", vertical="center")
            c.comment = Comment(source, "Fonte")
    ws.auto_filter.ref = f"C8:{ws.cell(8 + len(df), last_col).coordinate}"
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_area = f"B2:{ws.cell(8 + len(df), last_col).coordinate}"
    ws.oddFooter.center.text = f"{name} | Página &[Page]"
    for col_idx in range(3, last_col + 1):
        max_len = max([len(str(ws.cell(r, col_idx).value or "")) for r in range(8, min(100, 9 + len(df)))] + [12])
        ws.column_dimensions[ws.cell(8, col_idx).column_letter].width = min(max_len + 2, 42)
    return ws

add_sheet("Municipios_Tratados", "Dados tratados — municípios brasileiros", br, "Valores monetários nominais ou em R$ médios de 2024, conforme o cabeçalho; percentuais são expressos em % dos denominadores indicados; per capita usa população IBGE.", subtitle="Séries fiscais anuais de Bagé/RS e Sant'Ana do Livramento/RS.")
add_sheet("Chile_Dipres", "Chile — agregado das municipalidades", ch, "Colunas *_pct_PIB: % do PIB nacional; participações *_pct_receita: % da linha Ingresos. 2015 da edição 2015–2024; 2016–2024 da edição atualizada.", "Fonte: DIPRES, Estadísticas de las Finanzas Públicas 2015–2024 (p. 55) e EFP 2016–2025, folha EOM%PIB; extraído em 21/10/2026.", subtitle="Série agregada nacional; não representa uma comuna individual.")
add_sheet("Status_Siconfi", "Homologação DCA — municípios brasileiros", status, "Status de entrega anual; HO = homologado; RE = retificado/revisado.", "Fonte: Siconfi/STN, Extrato de Entregas, município e exercício identificados na linha; API oficial, consulta em 21/10/2026.", subtitle="Metadados de validação das declarações por município e exercício.")
add_sheet("Populacao_IBGE", "População municipal: estimativas e Censo 2022", pop_df, "Pessoas; 2015–2021 e 2024 são estimativas anuais; 2022 é população censitária; 2023 permanece ausente.", "Fonte: IBGE/SIDRA, tabela 6579, variável 9324, e tabela 4709, variável 93; consultadas em 21/10/2026.", subtitle="Estimativas anuais e observação censitária identificadas separadamente.")
add_sheet("PIB_IBGE", "PIB municipal a preços correntes", pib_df, "Tabela 5938: R$ mil; coluna em reais é calculada como mil reais × 1.000.", "Fonte: IBGE/SIDRA, tabela 5938, variável 37; consultada em 21/10/2026.", subtitle="Produto interno bruto municipal nominal; cobertura 2015–2023.")
add_sheet("IPCA_Deflator", "Deflator anual IPCA", ipca_annual, "Índice médio anual mensal; fator converte fluxo anual em R$ médios de 2024.", "Fonte: IBGE/SIDRA, tabela 1737, variável 2266 (número-índice); consultada em 21/10/2026.", subtitle="Deflator anual calculado a partir da média dos índices mensais.")
add_sheet("Resumo", "Estatísticas descritivas de ponta a ponta", summary, "Unidade conforme indicador: R$ médios de 2024 por habitante ou percentual; variação relativa em %. Janelas dependem da cobertura; sem inferência causal.", "Fonte: cálculos próprios reproduzidos em scripts/trata_base.py a partir dos arquivos brutos oficiais.", subtitle="Autora: Ana Luiza Florêncio dos Santos — matrícula 211059333.")
wb.save(ROOT / "base_atualizada_211059333.xlsx")

print(json.dumps(coverage, ensure_ascii=False, indent=2))
print("Wrote", OUT / "painel_fiscal_municipios_2015_2024.csv")
print("Wrote", OUT / "chile_municipalidades_dipres_pct_pib.csv")
print("Wrote", ROOT / "base_atualizada_211059333.xlsx")
