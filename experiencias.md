# HikeFlora — experiências de treino antes do teste final

A CNN original teve 72,09% de accuracy de validação na época 4. Na época 10,
teve 99,62% no treino e 70,55% na validação, com aumento da perda de validação.
As experiências abaixo procuram reduzir esse sobreajuste. A MLP e a CNN
originais continuam guardadas para comparação.

| Nome | Diferença em relação à CNN original | Motivo |
|---|---|---|
| `cnn_paragem` | Para se `val_loss` não melhorar durante 2 épocas e recupera os pesos da melhor época | Evitar guardar o modelo depois da degradação na validação |
| `cnn_dropout` | A mesma paragem e `Dropout(0.5)` entre as duas camadas Dense | Reduzir a dependência excessiva de alguns neurónios |
| `cnn_aumento` | A mesma paragem, dropout e rotação pequena mais inversão horizontal das imagens de treino | Apresentar pequenas variações das imagens sem alterar a espécie |

Os três modelos usam no máximo 15 épocas, Adam com taxa 0,001, batch 32,
imagens RGB de 128 × 128, a mesma semente 42 e os mesmos 8 800 exemplos de
treino e 1 100 de validação. O aumento de imagens só se aplica durante o treino.
A paragem pode terminar antes da época 15; por isso, os CSV podem ter menos
linhas. Cada experiência guarda o modelo com os pesos da época de menor
`val_loss` e um CSV com o histórico completo.

Na pasta do projeto, depois de instalar o script `treinar_variacoes.py`, usar o
Python do ambiente onde o TensorFlow funciona:

```powershell
& "$env:USERPROFILE\hfvenv\Scripts\python.exe" treinar_variacoes.py cnn_paragem
& "$env:USERPROFILE\hfvenv\Scripts\python.exe" treinar_variacoes.py cnn_dropout
& "$env:USERPROFILE\hfvenv\Scripts\python.exe" treinar_variacoes.py cnn_aumento
```

Comparar os três CSV em `resultados/` pela **menor `val_loss`** e consultar
também a `val_accuracy` da mesma época. Escolher a configuração antes de abrir
o conjunto `dataset/test`. O teste independente fica reservado para a
avaliação final dos modelos escolhidos, com as métricas do enunciado.
