# Análise de Concept Drift

## Objetivo

Avaliar o impacto de uma mudança sintética na relação entre as características dos clientes (X) e a variável-alvo de inadimplência (Y).

## Metodologia

- Conjunto utilizado: `data/production/production.csv`.
- Registros avaliados: 9.000.
- Variável-alvo: `DEFAULT_NEXT_MONTH`.
- Critério de seleção: clientes com `PAY_0 >= 1`.
- Rótulos invertidos aleatoriamente: 1.003 (50% dos clientes elegíveis, aproximadamente).
- As variáveis de entrada foram preservadas integralmente.
- O mesmo modelo baseline foi utilizado nas duas avaliações.

## Resultados

| Métrica | Original | Simulada |
|---|---:|---:|
| Precision | 49,21% | 47,02% |
| Recall | 56,45% | 53,17% |
| F1-score | 52,58% | 49,91% |
| ROC-AUC | 76,35% | 74,08% |
| Balanced Accuracy | 69,95% | 67,92% |

Todas as cinco métricas apresentaram redução após a alteração dos rótulos.

## Conclusão

A simulação demonstrou como uma mudança na relação entre as características de entrada e a variável-alvo pode prejudicar o desempenho de um modelo de classificação.

O experimento representa uma demonstração controlada de Concept Drift, não uma evidência de que essa mudança ocorreu na população real de clientes.

## Artefatos gerados

- `data/production/production_concept_drift.csv`
- `reports/monitoring/concept_drift_metrics.json`
- `src/drift/simulate_concept_drift.py`
- `src/drift/evaluate_concept_drift.py`