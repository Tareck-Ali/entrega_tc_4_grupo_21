# entrega_tc_4_grupo_21

## Tech Challenge 4 — 2026

**Tema:** Observabilidade Contínua, Detecção de Drift, Qualidade de Dados e Governança em Produção.

## 1. Sobre o projeto

Este projeto tem como objetivo desenvolver um fluxo de Machine Learning com mecanismos de qualidade de dados, monitoramento de previsões, detecção de Data Drift e avaliação de Concept Drift.

A solução utiliza um modelo de classificação para estimar a inadimplência de clientes de cartão de crédito e demonstra como acompanhar a qualidade dos dados e o comportamento de um modelo ao longo de diferentes etapas de processamento.

O projeto foi desenvolvido para fins acadêmicos e experimentais. As simulações de produção não representam uma operação financeira real.

## 2. Fonte de dados

Foi utilizado o dataset **Default of Credit Card Clients**, disponibilizado pelo UCI Machine Learning Repository.

- **Origem:** Taiwan.
- **Quantidade de registros:** 30.000.
- **Variáveis preditoras:** 23.
- **Tipo de problema:** classificação binária.
- **Variável-alvo:** inadimplência no mês seguinte (`DEFAULT_NEXT_MONTH`).

A variável-alvo possui duas classes:

- `0`: não houve inadimplência.
- `1`: houve inadimplência.

A distribuição original da variável-alvo é:

| Classe | Registros | Proporção |
|---|---:|---:|
| Não inadimplente (0) | 23.364 | 77,88% |
| Inadimplente (1) | 6.636 | 22,12% |

**Fonte oficial:**  
https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients

**Citação do dataset:**  
Yeh, I. (2009). *Default of Credit Card Clients*. UCI Machine Learning Repository. DOI: https://doi.org/10.24432/C55S3H.

**Licença:** Creative Commons Attribution 4.0 International (CC BY 4.0).

## 3. Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem principal |
| Pandas e NumPy | Manipulação e análise de dados |
| Scikit-learn | Pré-processamento, treinamento e avaliação |
| Pandera | Validação e contratos de dados |
| Evidently | Monitoramento e detecção de Data Drift |
| Streamlit | Dashboard de observabilidade |
| Plotly | Visualizações interativas |
| Matplotlib e Seaborn | Análise exploratória |
| Jupyter Notebook | Exploração dos dados |
| Pytest | Testes automatizados |
| Git e GitHub | Versionamento do projeto |

## 4. Estrutura do projeto

```text
entrega_tc_4_grupo_21/
│
├── .vscode/
│
├── artifacts/
│   └── models/
│       └── baseline_logistic_regression.joblib
│
├── data/
│   ├── raw/
│   ├── reference/
│   ├── production/
│   └── invalid/
│
├── notebooks/
│   └── 01_exploratory_analysis.ipynb
│
├── src/
│   ├── config.py
│   │
│   ├── data/
│   │   ├── download_dataset.py
│   │   ├── preprocessing.py
│   │   ├── validation.py
│   │   ├── test_validation.py
│   │   ├── create_invalid_batch.py
│   │   ├── test_invalid_batch.py
│   │   └── report_invalid_batch.py
│   │
│   ├── models/
│   │   ├── prepare_datasets.py
│   │   └── train_baseline.py
│   │
│   ├── monitoring/
│   │   ├── generate_prediction_logs.py
│   │   └── dashboard.py
│   │
│   └── drift/
│       ├── simulate_drift.py
│       ├── detect_drift.py
│       ├── simulate_concept_drift.py
│       └── evaluate_concept_drift.py
│
├── reports/
│   ├── drift/
│   │   ├── data_drift_report.html
│   │   └── data_drift_summary.json
│   │
│   └── monitoring/
│       ├── baseline_metrics.json
│       ├── prediction_logs.csv
│       ├── prediction_batch_summaries.jsonl
│       ├── invalid_batch_validation_report.csv
│       └── concept_drift_metrics.json
│
├── requirements.txt
├── .gitignore
└── README.md
```

*Observação: arquivos gerados durante a execução podem não estar versionados no Git, conforme as regras do `.gitignore`.*

## 5. Instalação e configuração

### Pré-requisitos

- Python instalado.
- Git instalado.
- Visual Studio Code ou outro editor compatível.

### Clonar o repositório

```bash
git clone https://github.com/Tareck-Ali/entrega_tc_4_grupo_21.git
cd entrega_tc_4_grupo_21
```

### Criar ambiente virtual

No Windows:

```bash
python -m venv .venv
```

Ativar o ambiente:

```bash
.venv\Scripts\activate
```

### Instalar dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Importante:** utilize o ambiente virtual do projeto para executar os comandos.

## 6. Execução do projeto

Os comandos abaixo devem ser executados no terminal, a partir da pasta raiz do projeto.

### 6.1 Aquisição dos dados

```bash
python -m src.data.download_dataset
```

O script realiza a aquisição do dataset utilizado no projeto e disponibiliza o arquivo na pasta de dados brutos.

### 6.2 Preparação dos dados

```bash
python -m src.models.prepare_datasets
```

Essa etapa realiza a preparação dos conjuntos de referência e produção, utilizando divisão estratificada.

Arquivos gerados:

- `data/reference/reference.csv`
- `data/production/production.csv`

### 6.3 Validação dos contratos de dados

A validação utiliza Pandera para verificar os contratos de dados, incluindo:

- Tipos de dados.
- Valores permitidos.
- Limites das variáveis.
- Valores nulos.
- Estrutura esperada do conjunto de dados.

Para executar os testes automatizados de validação:

```bash
python -m pytest -v src/data/test_validation.py
```

### 6.4 Simulação de lote inválido e bloqueio

Primeiro, gere o lote com dados inválidos:

```bash
python -m src.data.create_invalid_batch
```

Em seguida, execute os testes:

```bash
python -m pytest -v src/data/test_invalid_batch.py
```

O lote inválido introduz três violações intencionais:

- Valor negativo em `PAY_AMT1`.
- Valor inválido em `SEX`.
- Valor inválido em `DEFAULT_NEXT_MONTH`.

Para executar todos os testes de validação em conjunto:

```bash
python -m pytest -v src/data/test_validation.py src/data/test_invalid_batch.py
```

O objetivo é demonstrar que dados que não atendem ao contrato são identificados e bloqueados antes de seguirem pelo pipeline.

### 6.5 Treinamento do modelo baseline

```bash
python -m src.models.train_baseline
```

Foi utilizado um modelo de Regressão Logística, com:

- Padronização de variáveis numéricas.
- Codificação de variáveis categóricas.
- Balanceamento de classes por meio de `class_weight="balanced"`.
- Semente aleatória fixa para reprodutibilidade.

O modelo é treinado com os dados de referência e avaliado com os dados de produção.

### 6.6 Geração de logs de previsão

```bash
python -m src.monitoring.generate_prediction_logs
```

Essa etapa gera registros de previsões e indicadores operacionais, incluindo:

- Identificação do lote.
- Previsões realizadas.
- Probabilidades estimadas.
- Latência.
- Quantidade de previsões nulas.
- Resumo estatístico do processamento.

### 6.7 Simulação e detecção de Data Drift

Executar a simulação:

```bash
python -m src.drift.simulate_drift
```

Executar a detecção:

```bash
python -m src.drift.detect_drift
```

A simulação altera artificialmente as distribuições de `LIMIT_BAL` e `AGE` em parte dos registros de produção.

O Evidently compara os dados de referência com os dados modificados e gera relatórios para identificar alterações estatísticas.

### 6.8 Simulação e avaliação de Concept Drift

Executar a simulação:

```bash
python -m src.drift.simulate_concept_drift
```

Executar a avaliação:

```bash
python -m src.drift.evaluate_concept_drift
```

A simulação modifica artificialmente parte dos rótulos da variável-alvo, mantendo as variáveis de entrada inalteradas.

O objetivo é demonstrar como uma mudança na relação entre as entradas e o resultado pode afetar as métricas do modelo.

**Atenção:** trata-se de uma simulação controlada para fins acadêmicos, não de evidência de Concept Drift em dados reais.

### 6.9 Executar o dashboard

```bash
python -m streamlit run src/monitoring/dashboard.py
```

O dashboard apresenta indicadores de observabilidade e monitoramento, incluindo:

- Volume de registros processados.
- Latência.
- Previsões nulas.
- Distribuição das previsões.
- Comparação entre previsões e resultados reais.
- Métricas do modelo baseline.
- Resultados de Data Drift.

## 7. Resultados obtidos

### 7.1 Modelo baseline

O modelo de Regressão Logística apresentou os seguintes resultados na avaliação original:

| Métrica | Resultado |
|---|---:|
| Precision | 49,21% |
| Recall | 56,45% |
| F1-score | 52,58% |
| ROC-AUC | 76,35% |
| Balanced Accuracy | 69,95% |

As métricas foram selecionadas para avaliar diferentes aspectos do desempenho, considerando o desbalanceamento entre as classes.

### 7.2 Data Drift

A simulação alterou duas variáveis:

| Variável | Média original | Média simulada | Variação |
|---|---:|---:|---:|
| LIMIT_BAL | 167.449,74 | 137.650,11 | -17,79% |
| AGE | 35,62 | 32,63 | -8,39% |

O Evidently identificou drift em duas das 23 variáveis analisadas:

- `AGE`: distância de Wasserstein normalizada de 0,304496.
- `LIMIT_BAL`: distância de Wasserstein normalizada de 0,230112.

O limite individual utilizado na análise foi 0,1.

### 7.3 Concept Drift

Na simulação de Concept Drift:

- Registros de produção: 9.000.
- Registros elegíveis: 2.007.
- Rótulos alterados: 1.003.

As métricas do modelo apresentaram redução quando avaliadas contra os rótulos simulados.

| Métrica | Original | Simulada |
|---|---:|---:|
| Precision | 49,21% | 47,02% |
| Recall | 56,45% | 53,17% |
| F1-score | 52,58% | 49,91% |
| ROC-AUC | 76,35% | 74,08% |
| Balanced Accuracy | 69,95% | 67,92% |

Os resultados demonstram o impacto de uma alteração sintética na variável-alvo sobre a avaliação do modelo.

## 8. Observabilidade e monitoramento

A solução implementa mecanismos para acompanhar a saúde do pipeline e identificar possíveis problemas.

Os principais indicadores monitorados são:

| Indicador | Objetivo |
|---|---|
| Volume de registros | Acompanhar a quantidade de dados processados |
| Latência | Monitorar o tempo de processamento |
| Previsões nulas | Identificar falhas na geração de previsões |
| Probabilidades nulas | Identificar falhas na geração de probabilidades |
| Distribuição das previsões | Acompanhar o comportamento do modelo |
| Data Drift | Identificar mudanças nas distribuições das variáveis |
| Métricas de desempenho | Acompanhar a qualidade preditiva |

Os relatórios são armazenados nas pastas `reports/drift/` e `reports/monitoring/`.

## 9. Governança, LGPD e responsabilidade

O projeto possui um documento específico de governança:

`reports/monitoring/governance_lgpd.md`

O documento aborda:

- Privacidade e utilização dos dados.
- Bases legais previstas na LGPD.
- Direitos dos titulares.
- Segurança da informação.
- Política de retenção.
- Rastreabilidade das previsões.
- Riscos de viés e discriminação.
- Limitações da análise causal.

A utilização de modelos de Machine Learning em decisões de crédito exige cuidados com transparência, finalidade, necessidade, segurança e prevenção de discriminação.

Este protótipo não deve ser utilizado diretamente para decisões reais de concessão ou recusa de crédito.

## 10. Limitações do projeto

- O dataset é histórico e representa clientes de cartão de crédito em Taiwan.
- As simulações de Data Drift e Concept Drift são artificiais.
- A alteração de distribuições não comprova perda de desempenho do modelo.
- A alteração de rótulos não comprova que uma mudança semelhante ocorreu em uma população real.
- Associações estatísticas não demonstram causalidade.
- O modelo não passou por validação regulatória ou operacional para uso em produção.

## 11. Autoria

**Projeto:** Tech Challenge 4 — 2026  
**Repositório:** `entrega_tc_4_grupo_21`

Desenvolvido como projeto acadêmico de Machine Learning, com foco em qualidade de dados, observabilidade contínua, detecção de drift e governança.

