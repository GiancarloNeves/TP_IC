"""Seleciona imagens do Pl@ntNet-300K-v2 para a Meta 1 do HikeFlora.

Colocar plantnet300K_metadata.csv na mesma pasta e executar:
    python selecionar_imagens.py
"""

import csv
import random
from pathlib import Path


pasta = Path(__file__).parent
ficheiro_origem = pasta / "plantnet300K_metadata.csv"
ficheiro_saida = pasta / "selecao_imagens.csv"

especies = {
    8: "Pelargonium zonale",
    172: "Lavandula angustifolia",
    200: "Papaver rhoeas",
    225: "Trifolium repens",
    237: "Fragaria vesca",
}

orgaos = {"flower", "leaf", "fruit", "habit"}
particoes = ("train", "val", "test")
imagens = {}

for especie_id in especies:
    for particao in particoes:
        imagens[(especie_id, particao)] = []

with ficheiro_origem.open(newline="", encoding="utf-8") as ficheiro:
    for linha in csv.DictReader(ficheiro):
        especie_id = int(linha["species_id"])
        if especie_id in especies and linha["organ"] in orgaos:
            imagens[(especie_id, linha["split"])].append(linha)

random.seed(42)
selecionadas = []

for especie_id in especies:
    for particao in particoes:
        candidatas = imagens[(especie_id, particao)]
        candidatas.sort(key=lambda linha: linha["PN_hash"])

        if particao == "train":
            quantidade = 1760
        else:
            quantidade = 220

        if len(candidatas) < quantidade:
            raise ValueError(
                f"Imagens insuficientes para {especie_id}/{particao}: "
                f"{len(candidatas)} disponíveis, {quantidade} necessárias."
            )

        random.shuffle(candidatas)
        for linha in candidatas[:quantidade]:
            linha["species_name"] = especies[especie_id]
            linha["image_path"] = (
                f"images/{particao}/{especie_id:04d}/{linha['PN_hash']}.jpg"
            )
            selecionadas.append(linha)

with ficheiro_saida.open("w", newline="", encoding="utf-8") as ficheiro:
    colunas = [
        "species_id", "species_name", "PN_observation_id", "organ",
        "author", "license", "split", "PN_hash", "image_path",
    ]
    escritor = csv.DictWriter(ficheiro, fieldnames=colunas)
    escritor.writeheader()
    escritor.writerows(selecionadas)

print(f"Seleção criada: {ficheiro_saida}")
print(f"Total: {len(selecionadas)} imagens")
for especie_id in especies:
    contagens = []
    for particao in particoes:
        quantidade = sum(
            1 for linha in selecionadas
            if int(linha["species_id"]) == especie_id
            and linha["split"] == particao
        )
        contagens.append(f"{particao}={quantidade}")
    print(f"{especie_id} {especies[especie_id]}: {', '.join(contagens)}")
