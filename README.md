# P2 — Finanças do Setor Público — Ana Luiza Florêncio dos Santos — matrícula 211059333

Projeto individual da disciplina **Finanças do Setor Público — CCA0169, Turma 01, 2026.2**, Universidade de Brasília. O conjunto atribuído à matrícula é Chile, Bagé/RS e Sant'Ana do Livramento/RS. A série fiscal brasileira cobre 2015–2024; a cobertura do PIB municipal termina em 2023. Autora: Ana Luiza Florêncio dos Santos. O artigo final em PDF identifica a autora e a matrícula 211059333.

## Conteúdo do repositório

- `artigo/`: fonte Typst e PDF do artigo.
- `base_atualizada_211059333.xlsx`: painel fiscal editável e planilhas de apoio.
- O material histórico de outro recorte permanece preservado na cópia local, mas está excluído deste repositório e não integra o painel, a análise ou a reprodução desta P2.
- `data/brutos/`: respostas brutas das APIs oficiais e arquivos DIPRES, com manifesto de coleta.
- `data/tratados/`: painel brasileiro, série das municipalidades do Chile, população, PIB, deflator IPCA e status das declarações.
- `analise/`: estatísticas descritivas e verificações de cobertura.
- `figuras/`: gráficos reproduzidos pelo código.
- `scripts/coleta_dados.py`: coleta dados brasileiros nas APIs oficiais do Siconfi/STN e IBGE/SIDRA.
- `scripts/trata_base.py`: aplica as transformações documentadas, produz tabelas, gráficos e a planilha editável.
- `scripts/bibliometria.R`: consulta metadados por DOI, executa a análise com bibliometrix e gera as estatísticas e figuras bibliométricas.
- `scripts/consolida_referencias.py`, `scripts/exporta_matriz_literatura.py` e `scripts/exporta_bibliografia.py`: consolidam o corpus e geram a matriz, a lista de referências e as macros de citação.
- `scripts/revisa_texto_final.py`: aplica correções editoriais documentadas aos textos do artigo e às sínteses-fonte.
- `data/bibliometria/metadados_revisados.json`: correções de metadados de nove registros bibliográficos confirmadas em fontes editoriais e documentadas em `docs/fontes_consultadas.md`; o exportador mantém intactos os metadados brutos do Crossref.
- `docs/dicionario_variaveis.md`: conceitos, unidades, fontes, cobertura, fórmulas e tratamento de ausências.
- `docs/fontes_consultadas.md`: registro de fontes e limites metodológicos.
- `docs/registro_atualizacoes.md`: comparação com o material anterior e histórico das correções.
- `requirements.txt`: versões das bibliotecas Python empregadas.

## Reconstrução e diferenças em relação ao trabalho anterior

O material anterior indicado pelo link fornecido trata de Japão, Garanhuns/PE e Santana/AP, enquanto a distribuição da P2 atribui a esta matrícula Chile, Bagé/RS e Sant'Ana do Livramento/RS. Os arquivos históricos foram preservados localmente, mas não integram este pacote de reprodução; seus dados e conclusões não foram misturados ao novo painel. Como o conjunto anterior não corresponde às unidades da P2, a base desta análise foi reconstruída com dados oficiais; os detalhes estão no registro de atualizações.

No painel brasileiro, a receita líquida exclui deduções e receitas intraorçamentárias. O indicador central de transferências soma apenas as rubricas correntes identificadas como intergovernamentais, com deduções dos mesmos grupos. Transferências de capital e outras instituições públicas permanecem separadas. Valores fiscais nominais foram convertidos para reais médios de 2024 pelo IPCA anual médio.

A população de 2022 é a do Censo Demográfico, não uma estimativa intercensitária. Não há estimativa municipal anual independente para 2023 na fonte consultada, e a população desse ano permanece ausente. O PIB municipal consultado termina em 2023. Não se imputam zeros, interpolações ou projeções.

A série do Chile é o agregado consolidado das municipalidades, não uma comuna. As rubricas fiscais em percentual do PIB usam o PIB nacional; as participações internas de tributos e `Donaciones` usam a linha `Ingresos`. Nenhuma dessas razões é tratada como equivalente às medidas municipais brasileiras. O ano de 2025 foi excluído porque aparece como provisório na edição mais recente consultada.

## Reprodução

Com Python 3.12 ou compatível e acesso à internet:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/coleta_dados.py
python3 scripts/trata_base.py
python3 scripts/revisa_texto_final.py
python3 scripts/consolida_referencias.py
python3 scripts/exporta_matriz_literatura.py
python3 scripts/exporta_bibliografia.py
```

A coleta consulta as fontes oficiais e preserva os dados em `data/brutos/`. O tratamento também pode ser reproduzido a partir dos dados brutos já incluídos no repositório, sem repetir as chamadas de rede:

```bash
python3 scripts/trata_base.py
```

Para compilar o artigo, instale o Typst CLI e execute:

```bash
typst compile --root . artigo/main.typ artigo/main.pdf
```

A análise bibliométrica usa R, `bibliometrix` e `openalexR`. Se as dependências ainda não estiverem instaladas, execute `Rscript -e 'install.packages(c("openalexR", "bibliometrix"))'` e depois `Rscript scripts/bibliometria.R`. O script consulta a OpenAlex por DOI, usa `data/bibliometria/openalex_records.rds` como cache quando a lista de DOI não mudou e gera estatísticas e figuras em `data/bibliometria/` e `figuras/`. Acrescente `--refresh` para atualizar os metadados remotos. A versão do pacote e o escopo dos metadados estão em `data/bibliometria/bibliometrix_summary.txt`.

## Fontes principais

- Siconfi/Tesouro Nacional — <https://apidatalake.tesouro.gov.br/docs/siconfi/>.
- IBGE/SIDRA — população, PIB municipal e IPCA, conforme os links e códigos no [dicionário de variáveis](docs/dicionario_variaveis.md).
- DIPRES — estatísticas de finanças públicas do Chile, conforme o [registro de fontes](docs/fontes_consultadas.md).
- Tese de partida indicada pelo professor — Lucas Oliveira Gomes Ferreira, Universidade de Brasília, 2021, <https://repositorio.unb.br/handle/10482/42292>.

## Limite de interpretação

A série descritiva de duas cidades e o agregado nacional das municipalidades chilenas não identificam causalidade nem reproduzem o teste econométrico de efeito flypaper da tese indicada. As diferenças de moeda, escala, população, classificação contábil e nível de governo são explicitadas no artigo e nos metadados.
