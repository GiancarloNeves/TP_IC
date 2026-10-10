"""Confirma que as imagens selecionadas foram extraídas e podem ser abertas.

Executar depois de extrair as imagens:
    python verificar_dataset.py

Requer Pillow: python -m pip install Pillow
"""

import csv
from pathlib import Path

from PIL import Image


pasta = Path(__file__).parent
dataset = pasta / "dataset"
contagens = {}
erros = []

with (pasta / "selecao_imagens.csv").open(newline="", encoding="utf-8") as ficheiro:
    imagens = list(csv.DictReader(ficheiro))

for linha in imagens:
    especie = linha["species_id"]
    particao = linha["split"]
    chave = (especie, particao)
    contagens[chave] = contagens.get(chave, 0) + 1

    caminho = dataset / particao / f"{int(especie):04d}" / f"{linha['PN_hash']}.jpg"
    if not caminho.exists():
        erros.append(f"Em falta: {caminho}")
        continue

    try:
        with Image.open(caminho) as imagem:
            imagem.load()
    except Exception as erro:
        erros.append(f"Não abre: {caminho} ({erro})")

for especie in sorted({linha["species_id"] for linha in imagens}, key=int):
    print(
        especie,
        "treino:", contagens.get((especie, "train"), 0),
        "validação:", contagens.get((especie, "val"), 0),
        "teste:", contagens.get((especie, "test"), 0),
    )

print("Total esperado:", len(imagens))
print("Ficheiros em falta ou ilegíveis:", len(erros))
for erro in erros[:20]:
    print(erro)

if erros:
    raise SystemExit("A extração precisa de ser corrigida.")
