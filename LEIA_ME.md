# HikeFlora — preparação do dataset da Meta 1

## Objetivo

Classificar uma fotografia de planta numa de cinco espécies e apresentar a espécie
provável. A apresentação prevê, em fases posteriores da aplicação, fichas sobre
ingestão e contacto, alternativas e resultado inconclusivo. O classificador de
imagens não determina por si só se uma planta é segura para consumo.

## Fonte

Pl@ntNet-300K-v2, versão 2.0, DOI 10.5281/zenodo.10419064:
https://zenodo.org/records/10419064

Os ficheiros `plantnet300K_metadata.csv` e `species_metadata.csv` são cópias dos
metadados oficiais. O arquivo `images.zip` oficial tem 41,8 GB e não está nesta
pasta. Os direitos de cada fotografia estão indicados na coluna `license` do
ficheiro de metadados.

## Classes e disponibilidade oficial

| ID | Nome científico | Nome usado | Treino | Validação | Teste | Total |
|---:|---|---|---:|---:|---:|---:|
| 8 | *Pelargonium zonale* | gerânio | 2 653 | 333 | 332 | 3 318 |
| 172 | *Lavandula angustifolia* | alfazema | 2 738 | 343 | 342 | 3 423 |
| 200 | *Papaver rhoeas* | papoila | 4 004 | 502 | 502 | 5 008 |
| 225 | *Trifolium repens* | trevo-branco | 3 353 | 420 | 420 | 4 193 |
| 237 | *Fragaria vesca* | morangueiro silvestre | 3 862 | 483 | 483 | 4 828 |

Total das cinco classes: **20 770** imagens. O morangueiro cultivado ID 641 foi
substituído pelo morangueiro silvestre ID 237 por decisão do grupo. O ID 641
corresponde a *Fragaria × ananassa* e tem apenas 343 imagens.

## Seleção proposta para os IDs escolhidos

O ficheiro `selecao_imagens.csv` contém os **11 000 caminhos exatos** escolhidos.
Foram mantidas imagens com etiqueta de órgão `flower`, `leaf`, `fruit` ou
`habit`; foram excluídas as etiquetas `bark`, `branch` e `other`, pouco úteis
para este problema. De cada uma das cinco classes foram escolhidas
2 200 imagens: 1 760 de treino, 220 de validação e 220 de teste. A seleção
aleatória usa a semente 42 e pode ser reproduzida com
`python selecionar_imagens.py`.

| Conjunto | Imagens |
|---|---:|
| Treino | 8 800 |
| Validação | 1 100 |
| Teste | 1 100 |
| **Total** | **11 000** |

As partições oficiais foram preservadas. Não há observações repetidas entre as
três partições selecionadas. As cinco classes têm a mesma dimensão (20% cada).
Os 11 000 caminhos foram confirmados no arquivo oficial. O tamanho comprimido
das imagens selecionadas é cerca de **1,49 GB**; o tamanho extraído pode variar.

## Como obter as imagens

1. Para escolher os ficheiros, bastam os dois CSV de metadados. O manifesto já
   foi produzido com eles; não foi necessário descarregar o arquivo completo.
2. O Zenodo publica as imagens num único `images.zip`, de 41,8 GB. O método
   simples para obter os ficheiros é descarregar esse arquivo uma vez para um
   computador com espaço suficiente. Não é necessário copiá-lo para esta pasta.
3. Executar `python extrair_imagens.py "/caminho/para/images.zip"`. O programa
   lê o manifesto e extrai
   apenas as imagens escolhidas para `dataset/train`, `dataset/val` e
   `dataset/test`. O arquivo completo pode ser removido depois de confirmada a
   extração.
4. Executar `python verificar_dataset.py` (instalar Pillow com
   `python -m pip install Pillow`, se necessário). O programa verifica se os
   11 000 ficheiros existem e se podem ser abertos.

Para trabalhar em conjunto sem transferir 41,8 GB pelo chat, basta dar acesso
à pasta com as imagens extraídas ou enviá-la em arquivos separados por classe.
O manifesto permite confirmar exatamente quais imagens são necessárias.

## Representação e cuidados

As fotografias originais têm dimensões variáveis. A entrada **proposta** para o
modelo é RGB a 128 × 128 píxeis, isto é, 49 152 valores antes da normalização.
As imagens só devem ser redimensionadas ao carregar os dados para o modelo;
não se devem mover imagens entre treino, validação e teste. A distribuição dos
órgãos é dominada por flores e folhas, e as etiquetas de órgão não garantem
qualidade visual: a amostra visual revelou fotografias de plantas no campo,
plantas em vasos e exemplares arrancados. É necessária uma revisão visual mais
extensa antes de considerar a seleção final.

## O que falta fechar nesta etapa

1. Obter as imagens, executar a extração e confirmar que os ficheiros abrem.
2. Rever amostras de cada classe e partição, corrigindo imagens incorretas,
   ilegíveis ou demasiado afastadas do uso em caminhadas.
3. Fechar a descrição dos dados e da limitação a cinco
   espécies no relatório; confirmar a aprovação do tema e pesquisar a
   comparação com o benchmark original sem confundir resultados de 1 000
   espécies com os desta seleção de cinco.

**Nota sobre o enunciado:** as quatro etapas do grupo são uma organização de
trabalho. A Meta I oficial também exige arquitetura, treino, teste e comparação
de modelos; por isso a entrega oficial não estará concluída só com este dataset.
