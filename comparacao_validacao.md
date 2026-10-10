# HikeFlora — comparação das três variações da CNN

Os três modelos foram treinados com 8 800 imagens e avaliados durante o treino
com 1 100 imagens de validação. A seleção foi feita pela menor `val_loss`,
definida antes destas experiências. A accuracy indicada é a da mesma época.

| Modelo | Épocas executadas | Época guardada | `val_loss` | `val_accuracy` |
|---|---:|---:|---:|---:|
| `cnn_paragem` | 5 | 3 | 0,7782 | 70,82% |
| `cnn_dropout` | 8 | 6 | **0,7386** | **72,18%** |
| `cnn_aumento` | 7 | 5 | 0,7748 | 70,64% |

O `cnn_dropout` obteve a menor perda de validação. Também apresentou a maior
accuracy na época guardada. A sua accuracy máxima no histórico foi 72,64% na
época 5, mas o modelo guardado contém os pesos da época 6, escolhida pela
menor perda de validação.

A adição de dropout reduziu a diferença entre treino e validação observada
na CNN original. O aumento de imagens não melhorou os resultados nesta
experiência. Estas conclusões referem-se apenas à validação: o conjunto
`dataset/test` ainda não foi usado.

Na avaliação independente, comparar a MLP original com `cnn_dropout` usando
as 1 100 imagens de teste. Reportar accuracy, recall, especificidade, F1 e AUC
macro, os valores por classe e as matrizes de confusão. Os ficheiros de modelo
necessários são `modelos/mlp.keras` e `modelos/cnn_dropout.keras`.
