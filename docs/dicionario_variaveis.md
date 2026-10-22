# Dicionário de variáveis

## Unidades, período e convenções

O painel brasileiro tem 20 observações município-ano: Bagé/RS e Sant'Ana do Livramento/RS, 2015–2024. As contas fiscais vêm da Declaração das Contas Anuais (DCA) do Siconfi/Tesouro Nacional, anexos I-C (receitas) e I-D (despesas). Todos os 20 registros consultados têm declaração homologada ou retificada/revisada no extrato de entregas. A unidade monetária original é real corrente; os campos com sufixo `_real_2024_R$` são valores em reais médios de 2024.

As fontes do IBGE são a API SIDRA para população, PIB municipal e IPCA. Os indicadores per capita de 2023 permanecem ausentes por falta de estimativa municipal anual independente; PIB municipal de 2024 permanece ausente porque a série consultada termina em 2023. Nenhum desses campos é preenchido com zero ou interpolação. Para 2022, a população é a do Censo Demográfico e está identificada separadamente das estimativas de 1º de julho.

## Variáveis fiscais municipais brasileiras

| Variável | Definição e unidade | Fonte, período e fórmula/tratamento |
|---|---|---|
| `ano` | Exercício fiscal, ano-calendário. | DCA/Siconfi, 2015–2024. |
| `codigo_ibge`, `municipio` | Identificador IBGE e nome do município/RS. | Bagé: 4301602; Sant'Ana do Livramento: 4317103. |
| `receita_total_bruta_incl_intra_R$` | Receita total bruta reportada antes das deduções, incluindo receitas intraorçamentárias; R$. | DCA, linha agregada `TotalReceitas`, coluna `Receitas Brutas Realizadas`. |
| `deducoes_receita_total_R$` | Deduções lançadas na linha agregada da receita total; R$. | DCA, todas as colunas iniciadas por `Deduções - ` e `Outras Deduções da Receita` associadas a `TotalReceitas`. |
| `receita_intra_liquida_removida_R$` | Receita intraorçamentária líquida excluída da receita total para evitar dupla contagem; R$. | DCA. Usa o total agregado intra quando disponível ou os códigos raiz intra do layout antigo; quando esses não existem, reconcilia com a linha `ReceitasExcetoIntraOrcamentarias` ou com os grupos raiz não intra. |
| `receita_orcamentaria_liquida_R$` | Receita orçamentária líquida e sem intraorçamentárias; R$. | Fórmula: `receita_total_bruta_incl_intra_R$ − deducoes_receita_total_R$ − receita_intra_liquida_removida_R$`. No layout mais recente, a base de conferência é a linha `ReceitasExcetoIntraOrcamentarias`. |
| `transferencias_correntes_brutas_R$` | Receita bruta do agregado de transferências correntes, incluindo fontes que podem não ser intergovernamentais; R$. | DCA, linha `Transferências Correntes`. Preservada como referência ampla, mas não usada como medida central de dependência intergovernamental. |
| `transferencias_capital_brutas_R$` | Receita bruta de transferências de capital; R$. | DCA, linha `Transferências de Capital`. Mantida separada e excluída do indicador harmonizado, pois os anos antigos não identificam o nível de governo com comparabilidade suficiente. |
| `transferencias_correntes_e_capital_liquidas_amplas_R$` | Transferências correntes e de capital em sentido amplo, líquidas das deduções registradas nos respectivos agregados; R$. | Fórmula: transferências correntes brutas + transferências de capital brutas − deduções reportadas nos dois agregados. Não equivale ao indicador intergovernamental estrito. |
| `transferencias_intergovernamentais_correntes_brutas_R$` | Transferências correntes brutas identificadas como provenientes de governos; R$. | DCA: em 2015–2017, rubrica raiz 1.7.2, “Transferências Intergovernamentais”; em 2018–2024, soma das rubricas raiz 1.7.1 (União), 1.7.2 (estados/DF) e 1.7.3 (municípios). Exclui transferências de instituições privadas, categorias públicas residuais e transferências de capital. |
| `deducoes_transferencias_intergovernamentais_correntes_R$` | Deduções associadas às rubricas raiz intergovernamentais usadas; R$. | DCA, colunas de deduções reportadas nas mesmas rubricas-raiz; não soma simultaneamente linhas-pai e descendentes. |
| `transferencias_intergovernamentais_liquidas_R$` | Transferências intergovernamentais correntes líquidas; R$. | Fórmula: brutas menos deduções das mesmas rubricas-raiz. É o numerador usado nos indicadores de dependência fiscal e em valores per capita. |
| `receita_liquida_residual_apos_transferencias_intergovernamentais_R$` | Receita líquida menos transferências intergovernamentais correntes líquidas; R$. | Fórmula residual. Inclui receitas próprias e outras rubricas de transferências ou receitas que não estão no indicador estrito; não deve ser descrita como “receita própria”. |
| `receita_tributaria_propria_R$` | Arrecadação própria da rubrica tributária agregada, incluindo impostos, taxas e contribuições de melhoria quando assim classificados; R$. | DCA, `Receita Tributária` em 2015–2017 e `Impostos, Taxas e Contribuições de Melhoria` em 2018–2024. A mudança de rótulo/classificação e a elevação das taxas de serviços em Sant'Ana do Livramento em 2018 impõem cautela de comparabilidade. |
| `despesa_liquidada_R$` | Despesa liquidada no exercício; R$. | DCA, `TotalDespesas`, coluna `Despesas Liquidadas`. Representa estágio liquidado, não pagamento. |
| `populacao` | Número de residentes. | IBGE/SIDRA, tabela 6579, variável 9324, estimativa anual de 2015–2021 e 2024; tabela 4709, variável 93, Censo 2022. Ausente em 2023. |
| `pib_nominal_R$` | PIB municipal a preços correntes, convertido de R$ mil para R$; R$. | IBGE/SIDRA, tabela 5938, variável 37, 2015–2023. Ausente em 2024. |
| `ipca_indice_medio_anual` | Média aritmética dos 12 números-índice mensais do IPCA no ano. | IBGE/SIDRA, tabela 1737, variável 2266, 2015–2024. |
| `fator_deflacao_base_2024` | Fator para expressar fluxo anual em reais médios de 2024. | Fórmula: `IPCA médio anual de 2024 ÷ IPCA médio anual do ano`. Sem arredondamento intermediário. |
| `receita_liquida_real_2024_R$`, `transferencias_intergovernamentais_reais_2024_R$`, `receita_tributaria_real_2024_R$`, `despesa_liquidada_real_2024_R$` | Valores reais em R$ médios de 2024. | Respectivo fluxo nominal × `fator_deflacao_base_2024`. |
| `receita_real_per_capita_2024_R$`, `transferencia_intergovernamental_real_per_capita_2024_R$`, `tributos_reais_per_capita_2024_R$`, `despesa_real_liquidada_per_capita_2024_R$` | Fluxo real por residente; R$ médios de 2024 por pessoa. | Respectivo fluxo real ÷ população do mesmo exercício. Ausente quando a população anual falta, inclusive em 2023. |
| `participacao_transferencias_pct_receita` | Transferências intergovernamentais correntes líquidas como percentual da receita líquida. | Fórmula: `100 × transferencias_intergovernamentais_liquidas_R$ ÷ receita_orcamentaria_liquida_R$`. |
| `participacao_tributos_pct_receita` | Rubrica tributária própria como percentual da receita líquida. | Fórmula: `100 × receita_tributaria_propria_R$ ÷ receita_orcamentaria_liquida_R$`. |
| `receita_liquida_pct_PIB`, `tributos_pct_PIB`, `despesa_liquidada_pct_PIB` | Receita líquida, tributos ou despesa liquidada como percentual do PIB municipal nominal. | Respectivo valor nominal ÷ `pib_nominal_R$` × 100; disponíveis somente para 2015–2023. |

## Variáveis do agregado municipal do Chile

| Variável | Definição e unidade | Fonte, período e fórmula/tratamento |
|---|---|---|
| `ano` | Exercício anual. | 2015–2024. |
| `receita_total_pct_PIB` | Linha DIPRES `Ingresos`, percentual do PIB nacional. | 2015: edição DIPRES 2015–2024, tabela municipal impressa na p. 55; 2016–2024: arquivo oficial EFP 2016–2025, aba `EOM%PIB`. Não é a linha `Total ingresos`. |
| `receita_tributaria_pct_PIB` | `Ingresos tributarios netos`, percentual do PIB nacional. | Mesmo conjunto e vintage de `receita_total_pct_PIB`. |
| `donaciones_pct_PIB` | Rubrica `Donaciones`, percentual do PIB nacional. | Mantida conforme o rótulo DIPRES; não equiparada diretamente às transferências intergovernamentais brasileiras. |
| `despesa_total_pct_PIB` | Linha `Gastos` do quadro de operações que afetam o patrimônio, percentual do PIB nacional. | Mesmo conjunto DIPRES. Não é a linha `Total gastos` nem inclui, por si só, as transações em ativos não financeiros. |
| `resultado_operativo_neto_pct_PIB` | Resultado operativo neto publicado, percentual do PIB. | Transcrito diretamente da linha DIPRES `RESULTADO OPERATIVO NETO`; não é reconstruído pela subtração de percentuais arredondados. |
| `receita_total_ampliada_pct_PIB`, `despesa_total_ampliada_pct_PIB` | Linhas `Total ingresos` e `Total gastos`, percentual do PIB. | Preservadas separadamente, conforme publicadas, para não confundir o quadro operacional com os totais que incluem transações em ativos não financeiros. |
| `participacao_tributos_pct_receita`, `participacao_donaciones_pct_receita` | Rubricas tributárias ou `Donaciones` como percentual da linha `Ingresos`. | Fórmula: rubrica ÷ `receita_total_pct_PIB` × 100. Indicadores de composição, não medidas de autonomia fiscal diretamente harmonizadas com o Brasil. |
| `origem_vintage`, `escopo` | Metadados da edição e da unidade observada. | 2015 é da edição 2015–2024; 2016–2024, da edição atualizada EFP 2016–2025 consultada em 2026. 2025 foi excluído por ser provisório. Unidade: agregado das municipalidades chilenas, não uma comuna específica. |

## Fontes principais

- API e metadados do Siconfi/STN: <https://apidatalake.tesouro.gov.br/docs/siconfi/>.
- IBGE/SIDRA população estimada: <https://apisidra.ibge.gov.br/values/t/6579/n6/4301602,4317103/v/9324/p/2015-2024?formato=json>.
- IBGE/SIDRA Censo 2022: <https://apisidra.ibge.gov.br/values/t/4709/n6/4301602,4317103/v/93/p/2022?formato=json>.
- IBGE/SIDRA PIB municipal: <https://apisidra.ibge.gov.br/values/t/5938/n6/4301602,4317103/v/37/p/2015-2023?formato=json>.
- IBGE/SIDRA IPCA: <https://apisidra.ibge.gov.br/values/t/1737/n1/1/v/2266/p/201501-202412?formato=json>.
- DIPRES Chile: <https://www.dipres.gob.cl/598/w3-propertyvalue-15407.html>.
