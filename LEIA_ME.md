# HikeFlora — guia do projeto

Este é o único ficheiro de notas da raiz. O relatório académico está em
`entrega/relatorio_meta1.pdf` e a versão editável em
`entrega/relatorio_meta1.docx`. A organização interna do grupo em quatro etapas
corresponde à **Meta I oficial** do enunciado.

## Dados e seleção

A fonte é o Pl@ntNet-300K-v2, DOI 10.5281/zenodo.10419064:
https://zenodo.org/records/10419064. Os metadados originais são
`species_metadata.csv` e `plantnet300K_metadata.csv` (este último é grande e
fica fora do Git). O arquivo original `images.zip` tem cerca de 41,8 GB.

| ID | Espécie | Fonte: treino | Fonte: validação | Fonte: teste | Fonte: total | Escolhidas |
|---:|---|---:|---:|---:|---:|---:|
| 8 | Gerânio (*Pelargonium zonale*) | 2 653 | 333 | 332 | 3 318 | 2 200 |
| 172 | Alfazema (*Lavandula angustifolia*) | 2 738 | 343 | 342 | 3 423 | 2 200 |
| 200 | Papoila (*Papaver rhoeas*) | 4 004 | 502 | 502 | 5 008 | 2 200 |
| 225 | Trevo-branco (*Trifolium repens*) | 3 353 | 420 | 420 | 4 193 | 2 200 |
| 237 | Morangueiro silvestre (*Fragaria vesca*) | 3 862 | 483 | 483 | 4 828 | 2 200 |
| | **Total** | **16 610** | **2 081** | **2 079** | **20 770** | **11 000** |

O ID 641 (*Fragaria × ananassa*) foi substituído pelo ID 237 porque tinha
apenas 343 imagens. `selecao_imagens.csv` contém os caminhos exatos das
11 000 fotografias, com 1 760 imagens de treino, 220 de validação e 220 de
teste por espécie. Foram preservadas as partições oficiais. A seleção usa
semente 42 e aceita os órgãos `flower`, `leaf`, `fruit` e `habit`. O manifesto
regista também o autor e a licença de cada fotografia. As imagens selecionadas
ocupam cerca de 1,49 GB dentro do ZIP original. O tamanho depois da extração
pode variar.

### Obter ou verificar as imagens

`dataset/` não entra no Git. Quem já recebeu a pasta `dataset/` deve colocá-la
junto dos scripts, com `train/`, `val/` e `test/`, e verificar as 11 000 imagens.
Quem tiver o `images.zip` original pode extrair apenas os caminhos do manifesto:

```powershell
& "$env:USERPROFILE\hfvenv\Scripts\python.exe" extrair_imagens.py "C:\caminho\images.zip"
& "$env:USERPROFILE\hfvenv\Scripts\python.exe" verificar_dataset.py
```

A saída esperada da verificação é **11 000** imagens e **0** ficheiros em falta
ou ilegíveis. `selecionar_imagens.py` só é necessário para refazer a seleção a
partir dos metadados oficiais; não o executar para substituir o manifesto sem
conferir se os caminhos continuam iguais.

## Código, modelos e resultados

`treinar.py` implementa a MLP e a CNN iniciais. Ambas recebem RGB 128 × 128,
usam Adam 0,001, batch 32 e 10 épocas. A MLP tem 3 146 117 parâmetros; a CNN
inicial, 1 848 677. `treinar_variacoes.py` implementa três experiências da
mesma CNN: paragem antecipada, paragem com dropout 0,5 e paragem com dropout e
aumento de dados. As três usam até 15 épocas e escolhem os pesos pela menor
`val_loss`. A documentação detalhada das camadas está no relatório.

A CNN inicial mostrou sobreajuste: na época 10, accuracy de treino de 99,62%,
accuracy de validação de 70,55% e val_loss de 1,4487. Entre as variações, a
CNN com dropout teve a menor val_loss, 0,7386, na época 6, com val_accuracy
72,18%. A escolha foi feita pela validação, antes da avaliação no teste.
Os históricos completos estão em `resultados/*_historico.csv`.

`avaliar_teste.py` avalia `modelos/mlp.keras` e
`modelos/cnn_dropout.keras` nas 1 100 imagens de `dataset/test` e guarda as
métricas e matrizes em `resultados/avaliacao_teste.txt`. No teste já realizado,
a MLP obteve 47,55% de accuracy e a CNN com dropout 74,00%. Consultar esse
ficheiro e o relatório para os valores por classe e a discussão dos erros. Para
consultar os resultados existentes não é necessário repetir treino ou teste.

Quem quiser executar os scripts precisa de Python 3.12 e das bibliotecas em
`requirements.txt`. Os modelos `.keras` estão no Git para partilha entre o
grupo; as imagens ficam fora do Git. Uma nova avaliação requer `dataset/test`
além dos modelos. Com o ambiente Python preparado:

```powershell
& "$env:USERPROFILE\hfvenv\Scripts\python.exe" -m pip install -r requirements.txt
& "$env:USERPROFILE\hfvenv\Scripts\python.exe" avaliar_teste.py
```

Os treinos só precisam de ser repetidos para uma nova experiência. Os comandos
são `treinar.py mlp`, `treinar.py cnn` e `treinar_variacoes.py` com
`cnn_paragem`, `cnn_dropout` ou `cnn_aumento`.

## Documentos e revisão

`entrega/HikeFlora_MetaI.zip` é a versão de trabalho do pacote de submissão.
Inclui o relatório, a apresentação, o anexo de IAG, o código, o manifesto e os
resultados. Contém `LEIA_PRIMEIRO.md` com instruções para quem receber apenas
o ZIP. Não inclui `dataset/`, `images.zip` nem os modelos `.keras`.

O relatório tem atualmente 6 páginas e contém trechos iniciados por **REVER**
para o grupo confirmar ou ajustar. O anexo de IAG contém propostas para o
campo «Minha análise», que devem ser revistas pelo grupo. Após alterar DOCX
ou PPTX, exportar novamente os PDFs e recriar o ZIP: estes ficheiros não se
atualizam automaticamente.

O enunciado oficial pede caso de estudo, dados, arquitetura e parâmetros,
treino, avaliação em teste independente, matriz de confusão, accuracy,
recall, especificidade, F1, AUC, comparação crítica, conclusões e referências.
O relatório final deve ter no máximo 10 páginas. As quatro etapas usadas pelo
grupo são apenas uma forma de organizar este trabalho.
