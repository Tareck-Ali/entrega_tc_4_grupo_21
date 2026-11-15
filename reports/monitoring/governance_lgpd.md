# Governança, LGPD e Análise Causal

## 1. Objetivo

Este documento apresenta as diretrizes de governança, privacidade, segurança e responsabilidade aplicáveis ao projeto de monitoramento de um modelo de Machine Learning para previsão de inadimplência de crédito.

O projeto utiliza o dataset **Default of Credit Card Clients**, disponibilizado pelo UCI Machine Learning Repository, com 30.000 registros e 23 variáveis preditoras, além da variável-alvo `DEFAULT_NEXT_MONTH`.

O objetivo é demonstrar práticas de qualidade de dados, monitoramento de modelos, detecção de mudanças nas distribuições e avaliação de desempenho. O projeto possui finalidade acadêmica e experimental, não sendo utilizado para decisões reais de concessão ou recusa de crédito.

## 2. Dados utilizados e privacidade

O conjunto de dados contém informações relacionadas ao perfil dos clientes, limite de crédito, idade, histórico de pagamentos, valores de faturas e pagamentos anteriores.

Entre as variáveis disponíveis estão:

- `LIMIT_BAL`: limite de crédito.
- `SEX`: código de sexo.
- `EDUCATION`: nível de escolaridade.
- `MARRIAGE`: estado civil codificado.
- `AGE`: idade.
- `PAY_0` a `PAY_6`: histórico de atraso nos pagamentos.
- `BILL_AMT1` a `BILL_AMT6`: valores das faturas.
- `PAY_AMT1` a `PAY_AMT6`: valores pagos.
- `DEFAULT_NEXT_MONTH`: indicação de inadimplência no mês seguinte.

O dataset utilizado não possui uma coluna de identificação individual no arquivo empregado pelo projeto. Isso reduz a exposição direta de identificadores, mas não permite afirmar, por si só, que os dados estejam efetivamente anonimizados ou que não exista possibilidade de identificação indireta.

Para uma aplicação real, devem ser adotadas medidas de minimização de dados, limitação de finalidade e avaliação dos riscos de reidentificação.

As informações devem ser utilizadas exclusivamente para a finalidade documentada, com acesso restrito e sem divulgação de registros individuais desnecessários.

## 3. Base legal e enquadramento na LGPD

A Lei nº 13.709/2018 (Lei Geral de Proteção de Dados Pessoais — LGPD) estabelece regras para o tratamento de dados pessoais e princípios como finalidade, adequação, necessidade, transparência, segurança, prevenção e não discriminação.

Em um cenário real de análise de crédito, uma hipótese legal que pode ser pertinente é a **proteção do crédito**, prevista no artigo 7º, inciso X, da LGPD.

A aplicação dessa hipótese depende da finalidade efetiva do tratamento e do contexto da operação. Ela não representa autorização irrestrita para coletar ou utilizar qualquer dado pessoal.

Também podem existir outras bases legais, conforme a operação concreta, como a execução de contrato ou o cumprimento de obrigação legal ou regulatória. A escolha deve ser documentada e validada pelo controlador com apoio jurídico e de privacidade.

No contexto deste projeto acadêmico, o dataset é utilizado para experimentação e avaliação técnica. A existência de uma base legal para uma eventual operação comercial não deve ser presumida a partir deste exercício.

## 4. Direitos dos titulares e decisões automatizadas

Em uma aplicação real, os titulares devem ter seus direitos respeitados, conforme a LGPD, especialmente os previstos nos artigos 18 e 20.

Entre os direitos relevantes estão:

- Confirmação da existência de tratamento de dados.
- Acesso aos dados pessoais tratados.
- Correção de dados incompletos, inexatos ou desatualizados.
- Solicitação de anonimização, bloqueio ou eliminação de dados desnecessários ou tratados em desconformidade com a legislação, observadas as hipóteses legais de conservação.
- Informação sobre o tratamento e sobre o compartilhamento de dados, conforme aplicável.

O artigo 20 prevê o direito de solicitar a revisão de decisões tomadas unicamente com base em tratamento automatizado de dados pessoais que afetem os interesses do titular, incluindo decisões destinadas a definir seu perfil de crédito.

O controlador também deve fornecer, quando solicitado, informações claras e adequadas sobre os critérios e procedimentos utilizados na decisão, respeitados os segredos comercial e industrial nos termos da lei.

Como boa prática de governança, recomenda-se manter um processo documentado para receber solicitações, verificar os dados utilizados, explicar os critérios relevantes e encaminhar casos que exijam análise adicional.

## 5. Segurança da informação e retenção

Para uma futura implementação em ambiente real, recomenda-se adotar os seguintes controles:

| Controle | Medida recomendada |
|---|---|
| Controle de acesso | Permissões conforme a necessidade de cada função |
| Armazenamento | Proteção dos arquivos e ambientes que armazenam dados |
| Criptografia | Proteção dos dados em trânsito e em repouso |
| Logs | Registro de acessos, alterações, execuções e decisões do modelo |
| Minimização | Utilização somente das variáveis necessárias à finalidade |
| Backup | Cópias protegidas e procedimento de recuperação |
| Auditoria | Revisão periódica dos acessos e dos processos de tratamento |

### Política de retenção proposta

Os dados pessoais devem ser mantidos somente pelo período necessário para cumprir a finalidade do tratamento, observadas as hipóteses legais de conservação previstas na LGPD.

Para uma operação real, a organização deverá estabelecer prazos documentados para:

- Dados de entrada utilizados pelo modelo.
- Registros de previsões e resultados.
- Relatórios de monitoramento e auditoria.
- Cópias de segurança.
- Registros necessários para cumprimento de obrigações legais ou exercício regular de direitos.

Ao término do período aplicável, os dados deverão ser eliminados ou anonimizados, quando cabível, respeitadas as obrigações legais de conservação.

Este projeto acadêmico não define um prazo universal de retenção para uma instituição financeira. A política definitiva dependerá da finalidade, dos requisitos regulatórios e da avaliação jurídica da organização responsável.

## 6. Monitoramento e rastreabilidade do modelo

O projeto implementa mecanismos de observabilidade para acompanhar a qualidade dos dados e o comportamento do modelo.

Os controles desenvolvidos incluem:

- **Pandera:** validação de contratos de dados e bloqueio de registros inválidos.
- **Scikit-learn:** treinamento e avaliação do modelo baseline de regressão logística.
- **Evidently:** comparação entre dados de referência e dados de produção simulados.
- **Logs de previsão:** registro de previsões, probabilidades, identificadores de lote e métricas operacionais.
- **Dashboard Streamlit:** visualização de indicadores de saúde do pipeline e resultados de monitoramento.

Entre os indicadores acompanhados estão:

- Volume de registros processados.
- Latência de processamento.
- Quantidade de previsões nulas.
- Quantidade de probabilidades nulas.
- Distribuição das previsões.
- Métricas de desempenho do modelo.
- Quantidade e proporção de variáveis com drift detectado.

Esses registros permitem rastrear execuções e investigar alterações no comportamento do pipeline.

Em produção real, os logs devem evitar a exposição desnecessária de dados pessoais. Recomenda-se registrar identificadores técnicos de lote e referências pseudonimizadas, quando necessárias, em vez de reproduzir dados pessoais completos.

## 7. Data Drift e Concept Drift

O projeto demonstra dois tipos de mudanças que podem afetar sistemas de Machine Learning.

### 7.1 Data Drift

Data Drift ocorre quando a distribuição das variáveis de entrada muda em relação aos dados de referência.

Na simulação desenvolvida, 60% dos registros de produção foram modificados em duas variáveis:

- `LIMIT_BAL`: redução simulada do limite de crédito.
- `AGE`: redução simulada da idade.

O relatório do Evidently identificou drift em duas das 23 variáveis analisadas:

| Variável | Distância de Wasserstein normalizada | Limite |
|---|---:|---:|
| AGE | 0,304496 | 0,1 |
| LIMIT_BAL | 0,230112 | 0,1 |

O resultado demonstra uma mudança nas distribuições das variáveis selecionadas.

### 7.2 Concept Drift

Concept Drift está relacionado à mudança na relação entre as variáveis de entrada (X) e a variável-alvo (Y).

Para demonstrar esse fenômeno de forma controlada, foi criada uma simulação que altera aleatoriamente os rótulos de 50% dos registros elegíveis, definidos por `PAY_0 >= 1`, sem modificar as variáveis de entrada.

Foram alterados 1.003 rótulos em 2.007 registros elegíveis.

A avaliação utilizou as mesmas previsões do modelo baseline e comparou o desempenho em relação aos rótulos originais e simulados.

| Métrica | Original | Simulada |
|---|---:|---:|
| Precision | 49,21% | 47,02% |
| Recall | 56,45% | 53,17% |
| F1-score | 52,58% | 49,91% |
| ROC-AUC | 76,35% | 74,08% |
| Balanced Accuracy | 69,95% | 67,92% |

Todas as métricas apresentaram redução após a alteração dos rótulos.

**Limitação importante:** essa simulação representa uma alteração sintética e controlada da relação entre as entradas e os rótulos. Ela demonstra o impacto de uma mudança na informação-alvo sobre a avaliação do modelo, mas não comprova a ocorrência de Concept Drift em uma população real.

Da mesma forma, a detecção de Data Drift não comprova, isoladamente, perda de desempenho ou mudança na relação entre as variáveis e o resultado.

## 8. Análise causal e riscos de viés

O modelo foi desenvolvido para identificar padrões estatísticos associados à inadimplência. Portanto, suas previsões não demonstram relações de causa e efeito.

Por exemplo, uma associação entre idade, limite de crédito e inadimplência não permite concluir que essas características causem o evento.

Uma análise causal adequada exigiria:

- Definição clara da pergunta causal.
- Identificação de possíveis fatores de confusão.
- Construção de hipóteses e diagramas causais.
- Escolha de métodos estatísticos apropriados.
- Avaliação da qualidade e representatividade dos dados.
- Validação das hipóteses com evidências adicionais.

Também existe risco de viés quando características demográficas ou variáveis correlacionadas com elas influenciam as previsões.

O dataset contém variáveis como sexo, idade, escolaridade e estado civil. Em uma aplicação real, seria necessário avaliar se essas variáveis são adequadas à finalidade, se produzem efeitos discriminatórios e se existem alternativas menos invasivas.

Recomenda-se realizar avaliações de desempenho por grupos relevantes, quando legalmente apropriado, considerando métricas como taxa de falsos positivos, taxa de falsos negativos, recall e precisão.

A exclusão de uma variável sensível ou demográfica não elimina automaticamente o risco de discriminação, pois outras variáveis podem funcionar como proxies.

## 9. Limitações e recomendações para produção

Este projeto possui finalidade acadêmica e apresenta limitações que impedem sua utilização direta em decisões reais de crédito:

1. O dataset é histórico e não representa necessariamente o comportamento atual de clientes ou instituições financeiras.
2. Os dados utilizados não foram coletados de uma operação brasileira atual.
3. As simulações de drift são artificiais e possuem parâmetros definidos para fins de demonstração.
4. A simulação de Concept Drift modifica rótulos de maneira controlada, não reproduzindo necessariamente um fenômeno econômico real.
5. O modelo baseline não foi submetido a um processo completo de validação regulatória, jurídica e de equidade.
6. O projeto não implementa um processo real de atendimento aos direitos dos titulares.

Antes de qualquer uso em produção, seriam necessários, no mínimo:

- Avaliação jurídica da finalidade e da base legal.
- Avaliação de impacto à proteção de dados, quando aplicável.
- Revisão de segurança e controle de acesso.
- Avaliação de vieses e discriminação.
- Validação do modelo com dados representativos da população de aplicação.
- Processo de revisão e contestação de decisões automatizadas.
- Política formal de retenção e descarte.
- Monitoramento contínuo e plano de resposta a incidentes.

## 10. Conclusão

A governança de modelos de Machine Learning deve contemplar não apenas a qualidade técnica das previsões, mas também privacidade, transparência, segurança, prevenção de discriminação e rastreabilidade.

Neste projeto, os mecanismos de validação de dados, monitoramento de drift, registro de previsões e avaliação de desempenho demonstram como estruturar controles técnicos para acompanhar um modelo ao longo de seu ciclo de vida.

A conformidade com a LGPD, entretanto, depende também de decisões organizacionais e jurídicas que não podem ser substituídas por ferramentas técnicas.

O modelo desenvolvido deve ser considerado um protótipo acadêmico, e qualquer aplicação real exigiria avaliações adicionais antes de seu uso.

## Referências

- BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- AUTORIDADE NACIONAL DE PROTEÇÃO DE DADOS (ANPD). Perguntas frequentes sobre proteção de dados pessoais. https://www.gov.br/anpd/pt-br/acesso-a-informacao/perguntas-frequentes
- UCI MACHINE LEARNING REPOSITORY. Default of Credit Card Clients. https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients
