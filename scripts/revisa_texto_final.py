#!/usr/bin/env python3
"""Aplica correções editoriais verificadas ao artigo e às fontes textuais da matriz.

Uso: python3 scripts/revisa_texto_final.py
As substituições são idempotentes: o script pode ser executado novamente sem duplicar
as correções. Nenhum valor fiscal, DOI ou dado bruto é alterado.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = "Ana Luiza Florêncio dos Santos"
TYPO_BREAK = "\\" * 2 + "\n      "


def replace_text(path: Path, pairs: list[tuple[str, str]]) -> int:
    text = path.read_text(encoding="utf-8")
    changed = 0
    for old, new in pairs:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            changed += n
        elif new not in text:
            raise RuntimeError(f"Trecho esperado não encontrado em {path.relative_to(ROOT)}: {old[:100]!r}")
    path.write_text(text, encoding="utf-8")
    return changed


text_fixes = {
    ROOT / "artigo" / "main.typ": [
        ('author: "Discente — matrícula 211059333"', f'author: "{AUTHOR} — matrícula 211059333"'),
        ("Professor Lucas Oliveira Gomes Ferreira " + TYPO_BREAK + "Matrícula: 211059333", "Professor Lucas Oliveira Gomes Ferreira " + TYPO_BREAK + AUTHOR + " " + TYPO_BREAK + "Matrícula: 211059333"),
        ("Em Chile, Corvalán", "No Chile, Corvalán"),
        ("O corpus contém 80 artigos de periódicos distintos,", "O corpus contém 80 artigos publicados em 57 periódicos,"),
        ("foram convertidos para os campos bibliometrix;", "foram convertidos para os campos exigidos pelo bibliometrix;"),
        ("e keywords vêm da OpenAlex", "e palavras-chave indexadas vêm da OpenAlex"),
        ("keywords da variável DE", "palavras-chave da variável DE"),
        ("Não se calculou co-citação", "Não se calcularam cocitações"),
        ("[Brasil: 2015 → 2023]", "[Brasil: 2015 → 2023; Chile: 2015 → 2024]"),
        ("A análise tampouco confirma ou rejeita causalmente o efeito flypaper.", "O desenho descritivo não permite confirmar nem rejeitar causalmente a hipótese do efeito flypaper."),
    ],
    ROOT / "README.md": [
        ("# P2 — Finanças do Setor Público — matrícula 211059333", f"# P2 — Finanças do Setor Público — {AUTHOR} — matrícula 211059333"),
        ("O artigo final em PDF será identificado pela matrícula.", f"Autora: {AUTHOR}. O artigo final em PDF identifica a autora e a matrícula 211059333."),
        ("Os materiais históricos de outro recorte foram mantidos sem alteração na cópia local de trabalho, mas não são incluídos no repositório desta análise, pois não são necessários para reproduzi-la.", "O material histórico de outro recorte permanece preservado na cópia local, mas está excluído deste repositório e não integra o painel, a análise ou a reprodução desta P2."),
        ("- `scripts/trata_base.py`: aplica as transformações documentadas, produz tabelas, gráficos e a planilha editável.\n", "- `scripts/trata_base.py`: aplica as transformações documentadas, produz tabelas, gráficos e a planilha editável.\n- `scripts/bibliometria.R`: consulta metadados por DOI, executa a análise com bibliometrix e gera as estatísticas e figuras bibliométricas.\n- `scripts/consolida_referencias.py`, `scripts/exporta_matriz_literatura.py` e `scripts/exporta_bibliografia.py`: consolidam o corpus e geram a matriz, a lista de referências e as macros de citação.\n- `scripts/revisa_texto_final.py`: aplica correções editoriais documentadas aos textos do artigo e às sínteses-fonte.\n"),
        ("agregado nacional municipal chileno", "agregado nacional das municipalidades chilenas"),
    ],
    ROOT / "docs" / "dicionario_variaveis.md": [
        ("O painel brasileiro tem 20 observações ente-ano:", "O painel brasileiro tem 20 observações município-ano:"),
        ("População per capita de 2023 permanece ausente", "Os indicadores per capita de 2023 permanecem ausentes"),
        ("percentual do PIB. | Mesmo conjunto DIPRES.", "percentual do PIB nacional. | Mesmo conjunto DIPRES."),
    ],
    ROOT / "analise" / "resultados_chave.md": [
        ("A dependência intergovernamental corrente, pela definição estreita documentada no dicionário, é menor em 2024 do que em 2015 nas duas cidades.", "A participação das transferências intergovernamentais correntes líquidas na receita líquida, conforme a definição estreita do dicionário, é menor em 2024 do que em 2015 nas duas cidades."),
        ("A queda da participação percentual não demonstra menor dependência causal, pois a receita total e suas demais rubricas também mudam.", "A queda dessa participação não demonstra, por si só, redução efetiva da dependência fiscal: a receita líquida e suas demais rubricas também mudam."),
        ("## Chile — agregado municipal, 2015 e 2024", "## Chile — agregado das municipalidades, 2015 e 2024"),
        ("`Ingresos tributarios netos` (% do PIB)", "`Ingresos tributarios netos` (% do PIB nacional)"),
        ("`Donaciones` (% do PIB)", "`Donaciones` (% do PIB nacional)"),
        ("`Gastos` (% do PIB)", "`Gastos` (% do PIB nacional)"),
    ],
    ROOT / "docs" / "registro_atualizacoes.md": [
        ("Os 20 município-ano têm status homologado ou retificado/revisado no extrato do Siconfi.", "As 20 observações município-ano têm declaração homologada ou retificada/revisada no extrato do Siconfi."),
    ],
}

for path, pairs in text_fixes.items():
    n = replace_text(path, pairs)
    print(f"{path.relative_to(ROOT)}: {n} substituições")

# Corrige apenas os resumos de achados nos arquivos-fonte JSON; títulos e metadados DOI ficam intactos.
source_pairs = [
    ("Santana do Livramento", "Sant'Ana do Livramento"),
    ("2009-2013", "2009–2013"),
    ("não é fiscalmente centralizado", "não é fiscalmente centralizada"),
    ("e não saúde ou educação", "sem aumento detectado nos gastos com saúde ou educação"),
    ("51,6% dos domicílios urbanos pagaram no período", "51,6% dos domicílios urbanos pagaram IPTU na POF 2017–2018"),
    ("estima que um aumento de 2% no imposto predial bastaria para equalizar orçamentos per capita", "os autores estimam, na formulação do estudo, que um aumento de 2% nos tributos sobre a propriedade bastaria para equalizar os orçamentos municipais per capita em Santiago; o resumo editorial não esclarece se a medida é variação relativa ou ponto percentual"),
    ("É evidência direta de desincentivo ao esforço próprio", "É um resultado compatível com a hipótese de que transferências afetem negativamente a eficiência da arrecadação"),
    ("incentivos perversos das transferências", "incentivos fiscais associados às transferências"),
    ("indicando incentivos perversos", "sugerindo uma mudança na composição do gasto associada às transferências"),
    ("conclui que os ganhos geram incentivos predominantemente perversos", "conclui que a receita adicional se associa sobretudo ao aumento de gastos administrativos e de esporte/lazer"),
]
source_changes = 0
for path in sorted((ROOT / "data" / "bibliometria").glob("eixo_*.txt")) + sorted((ROOT / "data" / "bibliometria").glob("complemento_*.json")):
    payload = json.loads(path.read_text(encoding="utf-8"))
    file_changes = 0
    for article in payload.get("articles", []):
        finding = article.get("finding_and_relevance")
        if not isinstance(finding, str):
            continue
        for old, new in source_pairs:
            n = finding.count(old)
            if n:
                finding = finding.replace(old, new)
                file_changes += n
        article["finding_and_relevance"] = finding
    if file_changes:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{path.relative_to(ROOT)}: {file_changes} correções nas sínteses-fonte")
        source_changes += file_changes
print(f"Total de correções nas sínteses-fonte: {source_changes}")
