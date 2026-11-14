# Análise do Modelo Baseline

## Modelo
- Algoritmo: Regressão Logística
- Estratégia: `class_weight="balanced"`
- Dados de treinamento: 21.000 registros de referência
- Dados de avaliação: 9.000 registros de produção
- Variável-alvo: `DEFAULT_NEXT_MONTH`

## Resultados

| Métrica | Resultado |
|---|---:|
| Precision | 0,4921 |
| Recall | 0,5645 |
| F1-score | 0,5258 |
| ROC-AUC | 0,7635 |
| Balanced Accuracy | 0,6995 |

## Matriz de confusão

| | Previsto 0 | Previsto 1 |
|---|---:|---:|
| Real 0 | 5.849 | 1.160 |
| Real 1 | 867 | 1.124 |

## Interpretação

O modelo apresenta capacidade razoável de discriminação entre clientes inadimplentes e não inadimplentes, com ROC-AUC de aproximadamente 0,76.

O Recall de 56,45% indica que o modelo identificou pouco mais da metade dos casos positivos. Os 867 falsos negativos representam um ponto de atenção para o monitoramento do risco de crédito.

Este modelo será utilizado como baseline para acompanhar mudanças nas distribuições dos dados e no desempenho preditivo durante as simulações de produção.

## Limitações

Os resultados representam uma avaliação inicial, realizada com divisão aleatória e estratificada do dataset. Não demonstram, isoladamente, desempenho em um ambiente real de produção.