# HikeFlora — arquiteturas iniciais da parte 2

Os dois modelos recebem imagens RGB redimensionadas para 128 × 128 píxeis e
preveem uma de cinco espécies: IDs 8, 172, 200, 225 e 237. Os valores dos
píxeis são divididos por 255 antes de entrarem nas camadas de classificação.
São usados os mesmos conjuntos de treino (8 800 imagens) e validação (1 100)
nos dois treinos. O teste independente (1 100) fica reservado para a parte 3.

| Parâmetro | Valor nos dois modelos |
|---|---|
| Épocas | 10 |
| Imagens por batch | 32 |
| Algoritmo de treino | Adam |
| Taxa de aprendizagem | 0,001 |
| Função de perda | Sparse categorical crossentropy |
| Métrica durante o treino | Accuracy |
| Semente do treino e da leitura das imagens | 42 |

## MLP

`Rescaling → Flatten → Dense(64, ReLU) → Dense(5, softmax)`.

A camada `Flatten` transforma cada imagem em 49 152 valores. A camada oculta
tem 64 neurónios; a camada final fornece cinco probabilidades. O modelo tem
**3 146 117 parâmetros treináveis**.

## CNN

`Rescaling → Conv2D(16, 3×3, ReLU) → MaxPool(2×2) → Conv2D(32, 3×3, ReLU)
→ MaxPool(2×2) → Flatten → Dense(64, ReLU) → Dense(5, softmax)`.

As convoluções aprendem padrões locais, como contornos e formas de folhas e
flores. O modelo tem **1 848 677 parâmetros treináveis**.

## Execução no computador que contém `dataset/`

Colocar `treinar.py` na mesma pasta que `dataset/`. Instalar TensorFlow uma vez:

```powershell
py -m pip install tensorflow
```

Treinar cada solução:

```powershell
py treinar.py mlp
py treinar.py cnn
```

Os modelos são guardados em `modelos/` e as métricas de cada época em
`resultados/`. Depois de os dois treinos terminarem, usar os históricos de
validação para descrever diferenças e possíveis sinais de sobreajuste. Não
usar o conjunto `test` para escolher a arquitetura; ele será usado uma vez na
avaliação final.
