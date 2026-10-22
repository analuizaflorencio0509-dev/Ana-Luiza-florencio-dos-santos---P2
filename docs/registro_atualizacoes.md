# Registro de atualizações e correções

## Material anterior e delimitação do conjunto

O arquivo e o repositório anteriores recebidos foram preservados em `data/original/`. O repositório indicado pelo usuário trata de Japão, Garanhuns/PE e Santana/AP. A tabela de distribuição do enunciado, por sua vez, atribui à matrícula 211059333 o Chile, Bagé/RS e Sant'Ana do Livramento/RS. Como as unidades não coincidem, os resultados, gráficos e observações do material anterior não foram importados para o painel novo nem tratados como evidência do conjunto atual.

A análise fiscal brasileira e chilena foi reconstruída com dados oficiais, em conformidade com a instrução do professor para reconstruir a base quando o arquivo editável ou a base pertinente não estiver disponível. A cópia anterior e o relatório PDF não foram alterados.

## Mudanças aplicadas à base

1. **Cobertura fiscal.** Foram coletadas declarações anuais da DCA para Bagé e Sant'Ana do Livramento em 2015–2024, anexos I-C (receitas) e I-D (despesas). O manifesto registra a consulta e os dados brutos por município, exercício e anexo. As 20 observações município-ano têm declaração homologada ou retificada/revisada no extrato do Siconfi.
2. **Receita líquida sem dupla contagem.** O cálculo parte da receita total bruta, subtrai as deduções registradas e remove o valor líquido intraorçamentário. Para o layout mais recente usa-se a linha agregada “Receitas exceto intraorçamentárias”; para os layouts anteriores a rotina reconcilia os grupos raiz e as rubricas intra. As deduções de transferências constitucionais, FUNDEB e outras deduções foram incorporadas ao somatório aplicável.
3. **Transferências intergovernamentais.** A versão inicial tratava o agregado “Transferências Correntes” junto de “Transferências de Capital” como se fosse integralmente intergovernamental. Isso abrangia categorias residuais e podia incluir outros tipos de fonte. O indicador principal foi corrigido: 2015–2017 usa a linha raiz 1.7.2 (“Transferências Intergovernamentais”); 2018–2024 soma as linhas raiz 1.7.1 (União), 1.7.2 (estados/DF) e 1.7.3 (municípios), líquidas das deduções correspondentes. Transferências de capital e categorias de outras instituições públicas/privadas ficam fora do indicador harmonizado, mas os totais amplos correntes e de capital são preservados em colunas separadas.
4. **Arrecadação própria.** A rotina seleciona a rubrica agregada tributária do layout de cada ano: “Receita Tributária” em 2015–2017 e “Impostos, Taxas e Contribuições de Melhoria” em 2018–2024. O rótulo e a estrutura mudam em 2018; como há também forte variação registrada nas taxas de serviços de Sant'Ana do Livramento, a série não sustenta inferências causais e recebe ressalva de comparabilidade.
5. **Valores reais.** Fluxos monetários brasileiros são expressos em reais médios de 2024 pelo fator `IPCA médio anual de 2024 ÷ IPCA médio anual do exercício`, usando o IPCA mensal do IBGE. Não há arredondamento intermediário.
6. **População.** A série usa estimativas IBGE/SIDRA de 2015–2021 e 2024, o Censo 2022 para 2022 e ausência para 2023. O valor censitário de 2022 não é disfarçado como estimativa intercensitária. Os indicadores per capita de 2023 permanecem em branco.
7. **Atividade econômica municipal.** O PIB nominal dos municípios é incluído para 2015–2023. O ano de 2024 não é extrapolado; indicadores fiscais/PIB têm janela menor do que a série de receitas e despesas.
8. **Chile.** A série do DIPRES é o agregado de todas as municipalidades do Chile, não uma comuna. 2015 vem da edição oficial 2015–2024; 2016–2024, da edição EFP 2016–2025 atualizada consultada em 2026; 2025 foi excluído por estar provisório. As rubricas “Ingresos”, “Ingresos tributarios netos”, “Donaciones”, “Gastos” e “Resultado Operativo Neto” são transcritas do quadro operacional. `Donaciones` não é tratada como diretamente equivalente às transferências intergovernamentais brasileiras. O resultado operativo neto é transcrito do quadro, não calculado pela subtração de linhas percentuais arredondadas.

## Arquivos e reprodução

- `data/original/`: cópia preservada do repositório e do relatório anteriores fornecidos.
- `data/brutos/`: respostas de fontes oficiais, arquivos DIPRES e manifesto de coleta.
- `data/tratados/`: painéis, séries auxiliares, deflatores e status de entrega.
- `scripts/coleta_dados.py`: coleta e preserva as séries brasileiras, população, PIB, IPCA e metadados.
- `scripts/trata_base.py`: transformações, validações, estatísticas, gráficos e planilha editável.
- `base_atualizada_211059333.xlsx`: versão editável do painel tratado e dos metadados de homologação.
- `docs/dicionario_variaveis.md`: conceitos, unidades, fontes, cobertura e fórmulas.
- `docs/fontes_consultadas.md`: URLs e limites metodológicos das fontes.

Execute, na ordem, `python3 scripts/coleta_dados.py` e `python3 scripts/trata_base.py` para atualizar a base usando as APIs oficiais. O tratamento também pode ser reproduzido com os JSON preservados em `data/brutos/`. Os dados ausentes permanecem ausentes; nenhum zero, interpolação ou valor projetado foi criado.


## Auditoria final de apresentação e interpretação — 22/10/2026

- O artigo e a planilha exibem a autoria **Ana Luiza Florêncio dos Santos** e a matrícula **211059333**.
- A figura chilena foi refeita em dois painéis para não misturar participações calculadas sobre `Ingresos` com razões calculadas sobre o PIB nacional. O artigo, o dicionário, o resumo de resultados e a nota da planilha explicam os denominadores e as edições DIPRES usadas em 2015 e 2016–2024.
- Nove registros bibliográficos têm correções editoriais rastreadas em `data/bibliometria/metadados_revisados.json` e `docs/fontes_consultadas.md`. O DOI da RP3 permanece sem paginação porque a citação oficial consultada não informa esse campo; não foi inventado um intervalo de páginas.
- A figura de coocorrência usa oito nós de maior grau, conforme o comportamento de `networkPlot` do `bibliometrix`; a legenda não os descreve como os oito termos mais frequentes. O relatório bibliométrico também esclarece que a métrica de coautoria internacional não é interpretável quando as afiliações estão ausentes.
- A seleção contém 80 DOI distintos citados no texto; a referência metodológica de Baker, Larcker e Wang aparece duas vezes no corpo, sem aumentar o número de obras distintas.
