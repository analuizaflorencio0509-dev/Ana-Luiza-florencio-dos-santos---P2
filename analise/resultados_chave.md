# Resultados descritivos — base fiscal P2

Cálculos reproduzidos por `scripts/trata_base.py` a partir dos arquivos brutos em `data/brutos/`.

## Cobertura

O painel brasileiro contém 20 registros município-ano (duas cidades × dez anos), sem receita ou despesa ausente. Os 20 exercícios têm entrega DCA classificada como homologada ou retificada/revisada. A população falta em 2023 para os dois municípios; o PIB municipal falta em 2024. Indicadores per capita de 2023 e indicadores fiscais/PIB de 2024 não são calculados. A série DIPRES reúne dez anos (2015–2024) do agregado chileno.

## Brasil — 2015 a 2024

Os valores por habitante são reais médios de 2024. Como 2023 não tem população municipal anual, as variações per capita comparam 2015 e 2024 (nove observações anuais disponíveis em 2015–2022 e 2024).

| Indicador | Bagé | Sant'Ana do Livramento |
|---|---:|---:|
| Receita líquida real por habitante, 2015 → 2024 | R$ 3.525,66 → R$ 4.798,28 (+36,1%) | R$ 3.172,21 → R$ 4.955,55 (+56,2%) |
| Transferências intergovernamentais correntes líquidas reais por habitante, 2015 → 2024 | R$ 2.001,95 → R$ 1.865,42 (−6,8%) | R$ 1.902,88 → R$ 2.366,93 (+24,4%) |
| Arrecadação tributária própria real por habitante, 2015 → 2024 | R$ 880,01 → R$ 1.187,89 (+35,0%) | R$ 720,46 → R$ 765,74 (+6,3%) |
| Despesa liquidada real por habitante, 2015 → 2024 | R$ 3.662,28 → R$ 5.592,81 (+52,7%) | R$ 3.811,34 → R$ 5.055,11 (+32,6%) |
| Transferências intergovernamentais líquidas / receita líquida, 2015 → 2024 | 56,78% → 38,88% | 59,99% → 47,76% |
| Arrecadação tributária / receita líquida, 2015 → 2024 | 24,96% → 24,76% | 22,71% → 15,45% |
| Receita líquida / PIB, 2015 → 2023 | 10,38% → 11,99% | 8,58% → 12,55% |

A participação das transferências intergovernamentais correntes líquidas na receita líquida, conforme a definição estreita do dicionário, é menor em 2024 do que em 2015 nas duas cidades. A composição, porém, não é uniforme: em Bagé as transferências reais por habitante caem ligeiramente entre os extremos; em Sant'Ana do Livramento crescem. A queda dessa participação não demonstra, por si só, redução efetiva da dependência fiscal: a receita líquida e suas demais rubricas também mudam.

Sant'Ana do Livramento apresenta uma elevação brusca na rubrica tributária entre 2017 e 2018. O próprio classificador passa de “Receita Tributária” para “Impostos, Taxas e Contribuições de Melhoria” em 2018, e a composição de taxas de serviço também muda. Por isso, a variação de 2015–2024 é apenas descritiva; não deve ser interpretada como uma elasticidade ou um efeito de política tributária.

## Chile — agregado das municipalidades, 2015 e 2024

| Indicador DIPRES | 2015 | 2024 |
|---|---:|---:|
| `Ingresos` (% do PIB nacional) | 3,6% | 4,09% |
| `Ingresos tributarios netos` (% do PIB nacional) | 1,5% | 1,74% |
| `Donaciones` (% do PIB nacional) | 1,4% | 1,39% |
| `Gastos` (% do PIB nacional) | 3,3% | 4,04% |
| `Resultado Operativo Neto` (% do PIB), linha publicada | 0,2% | 0,05% |
| Tributos / `Ingresos` | 41,7% | 42,5% |
| `Donaciones` / `Ingresos` | 38,9% | 34,1% |

O valor chileno de 2015 vem da edição DIPRES 2015–2024 e aparece arredondado a uma casa decimal. Os anos de 2016–2024 vêm da edição atualizada 2016–2025; 2025 foi excluído por ser provisório. A unidade é o setor municipal agregado do país. As rubricas fiscais são expressas como percentual do PIB nacional; as participações de tributos e `Donaciones` usam `Ingresos` como denominador. Portanto, os percentuais não são uma comparação homogênea com os dois municípios brasileiros. A rubrica `Donaciones` não é equiparada às transferências intergovernamentais brasileiras.

## Fontes de dados

- Siconfi/Tesouro Nacional — DCA e extrato de entregas: <https://apidatalake.tesouro.gov.br/docs/siconfi/>.
- IBGE/SIDRA — tabelas 6579 (população), 4709 (Censo 2022), 5938 (PIB municipal) e 1737 (IPCA); URLs específicas em `docs/dicionario_variaveis.md`.
- DIPRES — EFP e Estado de Operações das Municipalidades: <https://www.dipres.gob.cl/598/w3-propertyvalue-15407.html>.
