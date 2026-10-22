// Artigo científico da P2 — fonte nativa Typst.
#import "report-theme.typ": report-accent, report-theme
#import "citacoes.typ": source_doi

#show: report-theme.with(
  title: "Finanças municipais, transferências e arrecadação própria: Bagé, Sant’Ana do Livramento e Chile (2015–2024)",
  author: "Ana Luiza Florêncio dos Santos — matrícula 211059333",
  rhythm: "report",
  running-header: false,
)

// Folha de rosto
#page(margin: (top: 25%, x: 2.2cm), numbering: none, header: none)[
  #set par(first-line-indent: 0em)
  #align(center)[
    #text(size: 25pt, weight: "bold", fill: report-accent)[Finanças municipais, transferências e arrecadação própria: Bagé, Sant’Ana do Livramento e Chile (2015–2024)]
    #v(1em)
    #text(size: 14pt, fill: luma(80))[Artigo científico — P2]
    #v(2em)
    #line(length: 40%, stroke: 0.5pt + luma(160))
    #v(2em)
    #text(size: 12pt)[
      Universidade de Brasília — UnB
      #linebreak()
      Finanças do Setor Público — CCA0169 — Turma 01 — 2026.2
      #linebreak()
      Professor Lucas Oliveira Gomes Ferreira
      #linebreak()
      Autora: Ana Luiza Florêncio dos Santos
      #linebreak()
      Matrícula: 211059333
      #linebreak()
      Brasília — DF — 2026
    ]
  ]
]

#counter(page).update(1)

#align(center)[#text(size: 12pt, weight: "bold")[Resumo]]

Este artigo descreve a evolução das receitas, das transferências intergovernamentais correntes, da arrecadação tributária própria e das despesas de Bagé e Sant’Ana do Livramento, no Rio Grande do Sul, entre 2015 e 2024, e apresenta como contexto uma série agregada das municipalidades do Chile. O painel brasileiro foi reconstruído a partir das Declarações das Contas Anuais do Siconfi/Tesouro Nacional e de dados do IBGE/SIDRA; a série chilena foi obtida da DIPRES. Os fluxos brasileiros são expressos em reais médios de 2024 e os indicadores per capita respeitam as lacunas de população e PIB. A participação das transferências correntes líquidas na receita líquida caiu nos dois municípios, embora o valor real transferido por habitante tenha diminuído em Bagé e aumentado em Sant’Ana do Livramento. A arrecadação tributária própria por habitante cresceu mais em Bagé, mas sua participação na receita permaneceu praticamente estável; em Sant’Ana do Livramento, a série é afetada por mudança classificatória em 2018. No Chile, `Ingresos`, tributos líquidos, `Donaciones` e `Gastos` são apresentados como proporção do PIB nacional; as participações de tributos líquidos e `Donaciones` na linha `Ingresos` descrevem a composição interna. Por ser um agregado nacional, a série não é diretamente comparável aos indicadores municipais brasileiros. A análise é descritiva e não identifica efeitos causais.

*Palavras-chave:* finanças municipais; transferências intergovernamentais; arrecadação própria; federalismo fiscal; efeito flypaper; Chile.

= Introdução

A descentralização fiscal distribui responsabilidades de arrecadação e gasto entre níveis de governo, mas a existência de competências locais não garante autonomia financeira. A capacidade de financiar serviços com tributos próprios, a composição das transferências e as regras de equalização condicionam a margem de decisão dos governos subnacionais. No Brasil, a Constituição de 1988 ampliou a participação dos municípios nas receitas, sem eliminar desequilíbrios entre competências, bases tributárias e necessidades de gasto; por isso, a receita total, isoladamente, não descreve a autonomia fiscal.

O ponto de partida teórico deste trabalho é a tese de Ferreira (2021), defendida no Programa de Pós-Graduação em Ciências Contábeis da Universidade de Brasília. A tese reúne três estudos sobre transferências constitucionais, ilusão fiscal e efeito flypaper: municípios brasileiros com mais de 50 mil habitantes entre 2005 e 2012; uma amostra nacional de 5.568 municípios entre 2006 e 2013; e séries de estados e municípios que chegam a 2018. Seus resultados apontam a presença do efeito flypaper e diferenças regionais, além de destacar alinhamento político e custo marginal dos recursos públicos. A tese emprega estratégias econométricas próprias; o presente artigo não as replica, porque observa apenas dois municípios e um agregado nacional chileno. O trabalho parte de seus conceitos e pergunta: como evoluíram a receita líquida, os tributos próprios, as transferências correntes intergovernamentais e a despesa liquidada de Bagé e Sant’Ana do Livramento entre 2015 e 2024, e o que a série agregada chilena acrescenta como contraste institucional?

A evidência brasileira e comparada mostra que transferências podem tanto ampliar a provisão local quanto alterar incentivos de arrecadação, composição do gasto e competição política. Estudos nacionais encontram heterogeneidade conforme regras, desenho da transferência, capacidade administrativa e alinhamento político; estudos chilenos, por sua vez, tratam de um regime unitário com responsabilidades locais e mecanismos próprios de equalização. A interpretação exige distinguir essas evidências causais ou de painel dos indicadores descritivos construídos para este exercício.

O objetivo é atualizar uma base fiscal reprodutível para 2015–2024, comparar as trajetórias dos dois municípios gaúchos e situar o comportamento do agregado municipal chileno sem forçar equivalência entre níveis de governo ou classificações contábeis. Como objetivos complementares, o artigo documenta as definições das variáveis e apresenta um estudo bibliométrico de 80 artigos científicos selecionados por DOI. O artigo está organizado em referencial teórico, metodologia, resultados — incluindo a página bibliométrica — e conclusão.

= Referencial Teórico

== Federalismo fiscal, descentralização e autonomia

O federalismo fiscal examina a atribuição de funções, a distribuição de receitas e os incentivos associados às decisões de gasto. Oates (1999) organiza os argumentos de eficiência e provisão local; Weingast (1995) enfatiza autonomia subnacional sujeita a limites institucionais críveis. Evidências comparadas mostram que a forma federativa não basta para explicar a descentralização efetiva: poder presidencial, trajetória de reformas e distribuição de competências também importam. Essa distinção aparece nos estudos latino-americanos de Escobar-Lemmon (2001), Garman, Haggard e Willis (2001) e Falleti (2005), enquanto Letelier (2005) testa determinantes da descentralização em painel internacional. Rodden (2002) relaciona dependência de transferências, instituições e desempenho fiscal; Sacchi e Salotti (2016) mostram que a composição da despesa descentralizada varia com fatores demográficos, econômicos e políticos. Rezende (1995) situa a expansão de receitas municipais no Brasil e os desequilíbrios que persistem, e Tsui (2005) documenta como regras tributárias e transferências podem distribuir de forma desigual a capacidade fiscal local. #source_doi("10.1257/jel.37.3.1120") #source_doi("10.1093/oxfordjournals.jleo.a036861") #source_doi("10.1093/oxfordjournals.pubjof.a004919") #source_doi("10.1353/wp.2001.0002") #source_doi("10.1017/s0003055405051695") #source_doi("10.1177/1091142104270910") #source_doi("10.2307/3088407") #source_doi("10.1080/00343404.2014.893387") #source_doi("10.1590/0101-31571995-0834") #source_doi("10.1016/j.jce.2004.11.003")

== Transferências, equalização e incentivos políticos

As transferências intergovernamentais cumprem funções distintas: podem devolver receitas arrecadadas em outra esfera, compensar externalidades, redistribuir recursos ou financiar políticas condicionadas. No Brasil, Baião, Cunha e Souza (2017) encontram efeitos de equalização diferentes entre FPM, Fundeb e transferências voluntárias; Costa et al. (2024) também distinguem modalidades e mostram resultados redistributivos heterogêneos. Santos (2023) discute limites do FPM e alternativas de equalização. A distribuição das transferências voluntárias não é necessariamente guiada apenas por necessidade: Soares e Melo (2016) destacam critérios políticos e técnicos, e Moutinho (2016) documenta a heterogeneidade dos convênios. Em eleições apertadas, Brollo e Nannicini (2012) identificam efeitos do alinhamento político sobre transferências discricionárias; Ferreira, Alves e Caldeira (2021) estudam a política de alocação dos recursos. Amorim Neto e Simonassi (2013) mostram a relevância de coalizões para a distribuição intergovernamental, e Bracco et al. (2015) interpretam grants como sinais políticos. #source_doi("10.21874/rsp.v68i3.1406") #source_doi("10.1590/0034-761220240010") #source_doi("10.1590/1982-3533.2023v32n3art09") #source_doi("10.1590/0034-7612138727") #source_doi("10.1590/0034-7612139003") #source_doi("10.1017/s0003055412000433") #source_doi("10.1111/deve.12265") #source_doi("10.1590/s0101-31572013000400010") #source_doi("10.1016/j.jpubeco.2014.11.007")

A literatura também associa transferências a transparência, endividamento e accountability. Alt e Lassen (2006) analisam transparência fiscal e dívida em países da OCDE; Benito e Bastida (2009) relacionam transparência, desempenho e participação eleitoral. Christensen e Garfias (2021) estudam infraestrutura fiscal e incentivos eleitorais na tributação da propriedade no Brasil. No Chile, Corvalán, Cox e Osorio (2018) encontram ciclos orçamentários indiretos associados às eleições municipais, enquanto Livert e Gainza (2018) investigam política distributiva e equidade espacial do investimento público. Alberti, Díaz-Rioseco e Riveros (2023) examinam o Fondo Común Municipal e mostram que a mensuração da parcela não tributária altera a interpretação dos efeitos eleitorais. Alves e Araujo (2024) usam descontinuidades do FPM para estimar mudanças na composição do gasto; Mendes (2005) discute captura de transferências, e de Almeida Mendes et al. (2020) mostram que desigualdades regionais correspondem a necessidades distintas de serviços. #source_doi("10.1016/j.euroecorev.2005.04.001") #source_doi("10.1111/j.1540-6210.2009.01988.x") #source_doi("10.1086/711902") #source_doi("10.1016/j.jdeveco.2018.01.001") #source_doi("10.1080/00343404.2017.1309013") #source_doi("10.1017/lap.2023.16") #source_doi("10.1016/j.jge.2024.100104") #source_doi("10.1590/s1413-80502005000300005") #source_doi("10.25222/larr.555")

== Efeito flypaper e ilusão fiscal

O efeito flypaper descreve a resposta desproporcional do gasto público local a transferências em comparação com aumentos equivalentes da renda privada. A literatura o interpreta por mecanismos de informação, preferências, regras orçamentárias e política. Brennan e Pincus (1996) demonstram que o padrão pode surgir mesmo em um modelo mínimo de grants; Bailey e Connolly (1998) revisam explicações e questões de identificação. Dollery e Worthington (1996), Heyndels e Smolders (1994) e Dell’Anno e Mourao (2012) discutem evidências e mensurações da ilusão fiscal. Sausgruber e Tyran (2005) testam a hipótese de Mill, enquanto Chetty, Looney e Kroft (2009) mostram por que a saliência tributária importa para as escolhas dos contribuintes; Gemmell, Morrissey e Pinar (2003) relacionam percepções tributárias à demanda por gasto. #source_doi("10.1016/0047-2727(95)01543-4") #source_doi("10.1023/a:1005053921709") #source_doi("10.1111/j.1467-6419.1996.tb00014.x") #source_doi("10.1007/bf01053224") #source_doi("10.1177/1091142111425226") #source_doi("10.1007/s11127-005-3992-4") #source_doi("10.1257/aer.99.4.1145") #source_doi("10.1016/s0176-2680(03)00037-5")

Os resultados empíricos não são uniformes. Para o Brasil, Mattos, Rocha e Arvate (2011) reexaminam o efeito flypaper considerando eficiência de arrecadação; Mattos, Cardim e Politi (2018) estudam o custo marginal dos recursos públicos; Postali (2015) encontra relação entre royalties e menor eficiência arrecadatória estimada. Mendes (2005) acrescenta a hipótese de captura política. Em outros contextos, Melo (2002) encontra efeito flypaper e assimetria na Colômbia, Dahlberg et al. (2008) usam uma regra descontínua para identificar efeitos sobre impostos e despesas, e Mehiriz e Marceau (2014) mostram assimetria em municípios de Quebec. Kjaergaard (2015) testa como instituições políticas moderam a resposta dinamarquesa; Liu e Zhao (2011) e Nicholson-Crotty (2008) analisam esforço tributário em províncias chinesas e estados norte-americanos; Masaki (2018) encontra mobilização de receitas locais após transferências na Tanzânia. Rios, Hortas-Rico e Pascual (2022) associam menor efeito flypaper a maior eficiência arrecadatória e força política local. Em conjunto, esses estudos recomendam tratar a dependência como indicador descritivo, não como prova de desincentivo ou de efeito flypaper. #source_doi("10.1590/s0101-41612011000200002") #source_doi("10.5935/0034-7140.20180023") #source_doi("10.1016/j.econ.2015.08.001") #source_doi("10.1023/a:1014964318685") #source_doi("10.1016/j.jpubeco.2007.05.004") #source_doi("10.1111/pbaf.12026") #source_doi("10.1080/03003930.2014.968708") #source_doi("10.1080/17487870.2011.591175") #source_doi("10.1177/153244000800800201") #source_doi("10.1016/j.worlddev.2018.01.026") #source_doi("10.1080/03003930.2020.1866555")

== Capacidade tributária própria e tributação local

Receita própria depende da base econômica, do cadastro, da administração tributária, da estrutura dos tributos e do esforço de cobrança. Massardi e Abrantes (2015) relacionam dependência do FPM, esforço fiscal e desenvolvimento; Menezes, Ferreira e Gonçalves (2017) distinguem esforço observado e potencial de arrecadação. Sobrinho e Alencar (2019) estimam esforço do IPTU por fronteira estocástica; Vieira, Ávila e Lopes (2021) aplicam DEA para avaliar eficiência tributária. Castro e Afonso (2017) estimam potencial do IPTU com conjuntos fuzzy, e Carvalho Junior e De Cesare (2022) analisam incidência e distribuição do imposto predial no Brasil. Caldeira, Ehrl e Moreira (2023) estudam descentralização e cobrança do ITR. Aldunate, Diaz e Truffa (2025) investigam a influência de partidos na tributação da propriedade; López-Morales, Herrera e Garretón (2024) oferecem uma leitura crítica da tributação imobiliária e segregação em Santiago. #source_doi("10.5700/rege564") #source_doi("10.18829/rp3.v0i09.21252") #source_doi("10.32586/rcda.v17i1.456") #source_doi("10.4270/ruc.2020320") #source_doi("10.1590/0034-7612160295") #source_doi("10.1016/j.landusepol.2022.106235") #source_doi("10.1016/j.ejpoleco.2023.102396") #source_doi("10.1371/journal.pone.0319994") #source_doi("10.1177/0308518x241276871")

Na tributação de serviços, De Angeli Neto e Martinez (2016) não encontram aumento per capita do ISS após a adoção da nota fiscal eletrônica nos municípios estudados, ao passo que Couto e Jorge (2022) identificam associação positiva em municípios baianos médios e grandes. Carrillo, Castro e Scartascini (2021) mostram que a provisão de bens públicos pode afetar o cumprimento do imposto predial; Ramírez, Díaz e Bedoya (2017) relacionam a arrecadação predial à pobreza multidimensional na Colômbia. Costa et al. (2025) identificam determinantes socioeconômicos da capacidade fiscal municipal; Mahdavi e Westerlund (2018) estudam capacidade e esforço subnacionais; Paula e Pinho (2023) propõem o custo da autonomia municipal. Caetano, Ávila e Tavares (2017) não encontram associação automática entre autonomia financeira e indicador educacional, e Marconato, Parré e Coelho (2021) mostram que a dinâmica financeira municipal varia com porte, estrutura produtiva e despesas de pessoal. #source_doi("10.11606/rco.v10i26.107117") #source_doi("10.61673/ren.2022.1317") #source_doi("10.1016/j.jpubeco.2021.104422") #source_doi("10.1016/j.worlddev.2017.02.005") #source_doi("10.1590/0034-761220240085") #source_doi("10.1016/j.econmod.2018.03.016") #source_doi("10.1590/1678-6971/eramf230196.en") #source_doi("10.1590/0034-7612174433") #source_doi("10.1590/0034-761220200041")

== Despesas públicas, eficiência e o caso chileno

O volume de despesa não mede, por si só, a qualidade ou a eficiência da provisão. Faria, Jannuzzi e Silva (2008) relacionam gasto municipal em saúde e educação a indicadores de serviço; Motta e Moreira (2009) examinam fatores políticos e eficiência da despesa; Varela, Martins e Fávero (2010) estudam eficiência e financiamento da saúde em municípios pequenos. Rosano-Peña, Albuquerque e Carvalho (2012) usam DEA para mapear ineficiência educacional, enquanto Rosano-Peña, Albuquerque e Daher (2012) analisam produtividade ao longo do tempo. Rodrigues, Gontijo e Gonçalves (2021) avaliam eficiência robusta em atenção primária, e Kroth e Guimarães (2021) relacionam eficiência de gestão a vulnerabilidade em saúde. Park (2022) mostra que descentralização pode alterar a composição dos gastos. #source_doi("10.1590/s0034-76122008000100008") #source_doi("10.1590/s1413-80502009000400001") #source_doi("10.1007/s10729-009-9114-y") #source_doi("10.1590/s1413-80502012000300004") #source_doi("10.1590/s1415-65552012000600006") #source_doi("10.1590/1413-81232021269.2.04342020") #source_doi("10.1590/1414-462x202199010297") #source_doi("10.1177/10911421221093142")

A literatura sobre municipalidades chilenas é particularmente útil para contextualizar o contraste institucional, mas não torna as unidades comparáveis. Letelier e Ormeño (2018) estudam educação municipal e financiamento; Letelier e Sáez-Lozano (2024) analisam descentralização fiscal e bem-estar subjetivo; Letelier (2011) investiga endividamento municipal sob restrições legais. Letelier e Mesa (2015) avaliam equalização segundo necessidades fiscais. Chavez e Paredes (2023) estimam economias de escala no gasto local, e Paredes e Rivera (2017) estudam tributos minerais e provisão de bens públicos. Esses trabalhos complementam a análise do agregado da DIPRES, que não identifica comunas específicas. #source_doi("10.1177/2399654418761888") #source_doi("10.1177/21582440241242649") #source_doi("10.1007/s11127-010-9596-7") #source_doi("10.4335/13.3.503-519(2015)") #source_doi("10.1016/j.seps.2023.101590") #source_doi("10.1016/j.resourpol.2017.07.007")

= Metodologia

== Desenho e fontes

O estudo é descritivo, longitudinal e comparativo, com duas unidades municipais brasileiras e uma unidade agregada nacional chilena. A janela fiscal é 2015–2024. O painel brasileiro reúne 20 observações município-ano. Os dados de receitas e despesas provêm das Declarações das Contas Anuais (DCA), anexos I-C e I-D, do Siconfi/Tesouro Nacional. O extrato de entregas identifica declarações homologadas (HO) ou retificadas/revisadas (RE); os 20 registros têm um desses status. População, PIB municipal e IPCA foram obtidos nas tabelas 6579, 4709, 5938 e 1737 do IBGE/SIDRA. Os arquivos brutos, as consultas e as transformações estão preservados no repositório.

A série chilena foi transcrita das *Estadísticas de las Finanzas Públicas* e dos arquivos do Estado de Operações das Municipalidades publicados pela Dirección de Presupuestos (DIPRES). O ano de 2015 corresponde à edição 2015–2024; 2016–2024 provêm da edição atualizada 2016–2025 consultada em 2026. O ano de 2025 foi excluído por estar marcado como provisório. A unidade é o setor municipal chileno agregado. As rubricas fiscais apresentadas como proporção usam o PIB nacional; as participações de tributos e `Donaciones` usam a linha `Ingresos` como denominador.

== Construção dos indicadores

A receita orçamentária líquida brasileira é calculada como receita bruta menos deduções menos receita intraorçamentária líquida, evitando dupla contagem. Para as transferências intergovernamentais correntes líquidas, usa-se a rubrica 1.7.2 do DCA em 2015–2017 e a soma das rubricas 1.7.1, 1.7.2 e 1.7.3 em 2018–2024, deduzindo os valores lançados nas mesmas rubricas-raiz. O indicador exclui transferências de capital e categorias residuais de outras instituições públicas. A participação das transferências é essa medida líquida dividida pela receita orçamentária líquida. Portanto, não representa todas as entradas de outras esferas.

A rubrica tributária própria agrega impostos, taxas e contribuições de melhoria conforme a classificação de cada edição do DCA. A nomenclatura muda entre 2015–2017 e 2018–2024; além disso, Sant’Ana do Livramento registra alteração expressiva nas taxas de serviços em 2018. A série é tratada como descritiva, sem interpretar a variação como efeito de uma reforma ou de maior esforço fiscal. A despesa usada é a liquidada, não a paga.

Os fluxos nominais brasileiros foram deflacionados para reais médios de 2024 pelo IPCA. Para cada ano, o fator é a média dos 12 números-índice mensais de 2024 dividida pela média anual do ano corrente, sem arredondamento intermediário. Os valores per capita resultam da divisão do fluxo real pela população do mesmo exercício. A população de 2022 é a censitária; a população municipal anual de 2023 e o PIB municipal de 2024 permanecem ausentes, sem imputação. Por isso, as séries per capita não incluem 2023 e os quocientes fiscais sobre o PIB terminam em 2023.

Para o Chile, mantêm-se os nomes das rubricas DIPRES: `Ingresos`, `Ingresos tributarios netos`, `Donaciones` e `Gastos`, apresentadas como proporção do PIB nacional. Além disso, as participações de tributos e `Donaciones` sobre a linha `Ingresos` medem a composição interna do agregado chileno. `Donaciones` não é equiparada à medida brasileira de transferências intergovernamentais; tampouco o indicador chileno sobre PIB nacional é comparado diretamente com o quociente municipal sobre PIB local.

As comparações usam níveis, participações e variações entre os extremos disponíveis. Não são estimados efeitos causais, elasticidades ou um modelo do efeito flypaper. Duas unidades brasileiras e uma série agregada chilena não fornecem grupo de controle, tratamento identificável nem unidade institucional homogênea. A referência metodológica Baker, Larcker e Wang (2022), indicada no comando da atividade, motiva a explicitação do escopo e das limitações de desenho; seus achados sobre diferenças-em-diferenças escalonadas não são evidência para as séries fiscais deste artigo. #source_doi("10.1016/j.jfineco.2022.01.004")

== Procedimento bibliométrico

Dos 91 artigos com DOI consolidados na triagem inicial, 80 foram selecionados para o corpus final, publicado em 57 periódicos; os 11 candidatos suplementares excluídos e os critérios estão documentados no repositório. A seleção preserva 67 obras dos dez eixos temáticos originais, incluindo a referência metodológica indicada pelo professor, e acrescenta oito estudos sobre tributação imobiliária municipal e cinco estudos brasileiros de capacidade ou eficiência tributária; o estudo sobre descentralização do ITR que aparece em dois eixos conta uma única vez. Cada DOI selecionado foi conferido na etapa de consolidação bibliográfica via Crossref. A bibliometria usa metadados consultados por DOI na OpenAlex e o pacote `bibliometrix` 5.5.0 em R, com `openalexR` 3.1.2. Os registros foram convertidos para os campos exigidos pelo bibliometrix; autoria e ano seguem a lista bibliográfica validada, enquanto resumos, contagem de citações, conceitos e palavras-chave indexadas vêm da OpenAlex quando disponíveis.

A produção anual foi tabulada entre o ano mais antigo e o mais recente do corpus, incluindo anos sem publicações. Frequências de periódicos e termos e uma rede de coocorrência foram produzidas com funções do `bibliometrix`; a visualização mostra os oito nós de maior grau na matriz. As palavras-chave da variável DE são termos indexados pela OpenAlex, não necessariamente palavras-chave declaradas pelos autores. Não se calcularam cocitações, pois os registros não continham referências citadas; afiliações foram omitidas por cobertura irregular. Trata-se de um mapa descritivo do corpus selecionado, não de revisão sistemática exaustiva. Baker, Larcker e Wang (2022) é empregado somente como referência de formato para contextualização bibliométrica, e não como fonte de evidência sobre os municípios. #source_doi("10.1016/j.jfineco.2022.01.004")

= Resultados

== Trajetórias dos municípios brasileiros

A Tabela 1 resume mudanças entre os extremos observados. Os valores per capita estão em reais médios de 2024. Para as séries per capita, 2023 é excluído por ausência de população municipal anual; para as razões sobre PIB, o último exercício disponível é 2023.

#set text(size: 8.3pt)
#table(
  columns: (1.75fr, 1fr, 1fr, 1fr, 1.35fr),
  inset: 4pt,
  stroke: 0.4pt + luma(205),
  [*Indicador*], [*Bagé*], [*Sant’Ana do Livramento*], [*Chile municipal*], [*Base temporal*],
  [Receita líquida real por habitante], [R\$ 3.526 → 4.798], [R\$ 3.172 → 4.956], [não comparável], [Brasil: 2015 → 2024],
  [Transferências / receita líquida], [56,8% → 38,9%], [60,0% → 47,8%], [Donaciones / ingresos: 38,9% → 34,1%], [2015 → 2024],
  [Tributos / receita líquida], [25,0% → 24,8%], [22,7% → 15,5%], [Tributos / ingresos: 41,7% → 42,5%], [2015 → 2024],
  [Receita líquida / PIB], [10,4% → 12,0%], [8,6% → 12,6%], [Ingresos / PIB nacional: 3,6% → 4,09%], [Brasil: 2015 → 2023; Chile: 2015 → 2024],
  [Despesa liquidada real por habitante], [R\$ 3.662 → 5.593], [R\$ 3.811 → 5.055], [Gastos / PIB nacional: 3,3% → 4,04%], [2015 → 2024],
)
#set text(size: 11pt)
#align(center)[#text(size: 8.5pt)[*Nota:* indicadores e denominadores diferem entre Brasil e Chile. O agregado chileno usa o PIB nacional para as rubricas expressas como percentual do PIB; as participações de tributos e `Donaciones` usam `Ingresos`. Fonte: elaboração própria com Siconfi/Tesouro Nacional, IBGE/SIDRA e DIPRES.]]

Entre 2015 e 2024, a receita líquida real por habitante aumentou de R\$ 3.525,66 para R\$ 4.798,28 em Bagé (+36,1%) e de R\$ 3.172,21 para R\$ 4.955,55 em Sant’Ana do Livramento (+56,2%). A despesa liquidada real por habitante também cresceu: +52,7% em Bagé e +32,6% em Sant’Ana do Livramento. Essas variações descrevem fluxos por residente; não demonstram melhora ou piora de eficiência, qualidade dos serviços ou equilíbrio fiscal, pois não incorporam resultados, necessidades locais, restos a pagar nem mudanças de composição.

A participação das transferências intergovernamentais correntes líquidas na receita líquida caiu de 56,78% para 38,88% em Bagé e de 59,99% para 47,76% em Sant’Ana do Livramento. A queda da razão não equivale a uma redução uniforme do montante transferido: em valores reais por habitante, a rubrica passou de R\$ 2.001,95 para R\$ 1.865,42 em Bagé (−6,8%), mas subiu de R\$ 1.902,88 para R\$ 2.366,93 em Sant’Ana do Livramento (+24,4%). O denominador também mudou, e outras receitas compõem a receita líquida. Assim, os dados não permitem inferir que as cidades ficaram menos dependentes por causa de maior esforço próprio ou de uma política específica.

A receita tributária própria real por habitante avançou 35,0% em Bagé (R\$ 880,01 para R\$ 1.187,89) e 6,3% em Sant’Ana do Livramento (R\$ 720,46 para R\$ 765,74). Sua participação na receita líquida ficou praticamente estável em Bagé, de 24,96% para 24,76%, e diminuiu em Sant’Ana do Livramento, de 22,71% para 15,45%. A diferença de trajetória deve ser lida com a ressalva classificatória: o agregado tributário muda de nome a partir de 2018, e o registro de Sant’Ana do Livramento apresenta um salto nas receitas tributárias e nas taxas de serviço nesse exercício. Não se atribui esse movimento a maior esforço arrecadatório.

A receita líquida como proporção do PIB municipal aumentou nos dois casos entre 2015 e 2023: de 10,38% para 11,99% em Bagé e de 8,58% para 12,55% em Sant’Ana do Livramento. O PIB local não está disponível para 2024 na série consultada, de modo que o último ponto não coincide com o final do painel fiscal. A ausência da população em 2023 também impede a comparação per capita desse ano; lacunas não foram convertidas em zero ou preenchidas por interpolação.

#grid(
  columns: (1fr, 1fr),
  gutter: 0.35cm,
  [#figure(image("../figuras/receita_per_capita_real.png", width: 100%), caption: [Receita orçamentária líquida real por habitante. R\$ médios de 2024; 2023 não calculado por ausência de população municipal anual.])],
  [#figure(image("../figuras/dependencia_transferencias.png", width: 100%), caption: [Transferências intergovernamentais correntes líquidas como proporção da receita líquida.])],
)

== Agregado municipal do Chile

Na série DIPRES, `Ingresos` avançou de 3,6% para 4,09% do PIB nacional entre 2015 e 2024; `Ingresos tributarios netos` passou de 1,5% para 1,74%, enquanto `Donaciones` variou de 1,4% para 1,39%. Como proporção de `Ingresos`, os tributos passaram de 41,7% para 42,5% e `Donaciones` de 38,9% para 34,1%. A linha publicada de `Gastos` foi de 3,3% para 4,04% do PIB, e o `Resultado Operativo Neto` publicado, sem reconstrução a partir de percentuais arredondados, passou de 0,2% para 0,05%.

A leitura é de composição do setor municipal agregado, não de uma comuna ou municipalidade média. As linhas `Ingresos`, `Ingresos tributarios netos`, `Donaciones` e `Gastos` são percentuais do PIB nacional; as participações internas de tributos e `Donaciones` usam a linha `Ingresos` como denominador. `Donaciones` permanece com a definição da DIPRES. Além disso, o valor de 2015 está arredondado a uma casa decimal e vem de uma edição anterior; 2016–2024 pertencem à edição atualizada. A figura separa as duas bases de cálculo e não oferece uma comparação homogênea com as contas individuais de Bagé e Sant’Ana do Livramento.

#figure(
  image("../figuras/chile_municipalidades_contexto.png", width: 88%),
  caption: [Painéis com denominadores distintos: tributos líquidos e `Donaciones` como proporção de `Ingresos`; `Gastos` como proporção do PIB nacional. Série do agregado das municipalidades chilenas; 2015 vem da edição DIPRES 2015–2024 e 2016–2024 da edição atualizada. Não é comparável diretamente às contas municipais brasileiras.],
)

#pagebreak()

== Estudo bibliométrico

// A compact bibliometric page keeps the corpus summary and both analytical figures together.
#set text(size: 9.5pt)
O corpus reúne 80 artigos publicados entre 1994 e 2025 em 57 periódicos. A produção anual é irregular, com sete trabalhos selecionados em 2021 e seis em cada um dos anos de 2017 e 2018. São frequências do corpus intencional deste estudo, não estimativas do universo completo de pesquisas.

Entre os termos indexados pela OpenAlex, “fiscal decentralization” aparece em 24 artigos, “intergovernmental transfers” em 20 e “fiscal federalism” em 19; “local government finance” ocorre em 12 e “Brazilian municipalities” em 11. A rede aponta conexões entre descentralização fiscal, transferências e finanças locais. Como os metadados não fornecem referências citadas e a cobertura de afiliações é irregular, não se calculam co-citações nem colaboração internacional; os termos tampouco equivalem necessariamente às palavras-chave declaradas pelos autores. O resultado é um mapa descritivo do corpus, não uma revisão exaustiva.

#align(center)[#figure(image("../figuras/bibliometria_top_keywords.png", width: 66%), caption: [Termos indexados mais frequentes no corpus.])]
#align(center)[#figure(image("../figuras/bibliometria_rede_palavras.png", width: 66%), caption: [Rede de coocorrência dos oito nós de maior grau; keywords indexadas pela OpenAlex.])]
#set text(size: 11pt)
#pagebreak()

= Conclusão

A reconstrução produziu um painel anual consistente para Bagé e Sant’Ana do Livramento entre 2015 e 2024 e uma série separada para o agregado municipal chileno. Nos dois municípios gaúchos, a participação das transferências correntes intergovernamentais na receita líquida diminuiu entre os extremos. O movimento não foi igual em valores reais por habitante: houve pequena redução em Bagé e aumento em Sant’Ana do Livramento. A receita tributária própria por habitante cresceu mais em Bagé, mas a participação tributária na receita quase não mudou; em Sant’Ana do Livramento, a queda dessa participação e o aumento abrupto de 2018 exigem cautela pela mudança de classificação.

O contraste chileno mostra aumento da razão de tributos sobre `Ingresos` e redução da participação de `Donaciones`, dentro do agregado nacional das municipalidades. Como os denominadores, os níveis de agregação, as classificações e as edições de publicação diferem, essa série é contexto institucional e não ranking ou comparação direta com os municípios brasileiros. O desenho descritivo não permite confirmar nem rejeitar causalmente a hipótese do efeito flypaper. Esse fenômeno exige identificação do choque de transferência, comparação adequada e medida de resposta de gasto; proporções de receita em duas cidades não satisfazem esses requisitos.

A principal contribuição é documental e descritiva: definições, fontes, lacunas, ajustes de inflação e scripts deixam a atualização auditável e reproduzível. A extensão do trabalho pode incorporar outras municipalidades, decompor transferências por modalidade e explorar estratégias de identificação compatíveis com as perguntas sobre esforço fiscal e despesa. Neste recorte, as conclusões permanecem limitadas às séries observadas e às ressalvas contábeis explicitadas.

#include "referencias.typ"

== Documento de partida e fontes de dados

Ferreira, Lucas Oliveira Gomes. *Constitutional tax transfers in Brazilian municipalities: the fiscal illusion and the flypaper effect*. 2021. 96 f. Tese (Doutorado em Ciências Contábeis) — Universidade de Brasília, Brasília, 2021. [Registro institucional](https://repositorio.unb.br/handle/10482/42292).

Siconfi/Tesouro Nacional. Declaração das Contas Anuais, anexos I-C e I-D, e extrato de entregas. [Documentação da API](https://apidatalake.tesouro.gov.br/docs/siconfi/).

IBGE/SIDRA. Tabelas 6579 (estimativas populacionais), 4709 (Censo Demográfico 2022), 5938 (PIB dos Municípios) e 1737 (IPCA). Consultas e variáveis estão detalhadas em `docs/dicionario_variaveis.md`.

DIPRES. *Estadísticas de las Finanzas Públicas* e Estado de Operações das Municipalidades. [Portal oficial](https://www.dipres.gob.cl/598/w3-propertyvalue-15407.html).
