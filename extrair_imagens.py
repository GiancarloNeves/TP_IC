"""Extrai do images.zip apenas as imagens de selecao_imagens.csv.

Executar:
    python extrair_imagens.py /caminho/para/images.zip
"""

import csv
import zipfile
from pathlib import Path
from sys import argv


pasta = Path(__file__).parent
destino = pasta / "dataset"
arquivo_zip = Path(argv[1]) if len(argv) > 1 else pasta / "images.zip"

with (pasta / "selecao_imagens.csv").open(newline="", encoding="utf-8") as ficheiro:
    imagens = list(csv.DictReader(ficheiro))

with zipfile.ZipFile(arquivo_zip) as arquivo:
    for indice, linha in enumerate(imagens, 1):
        caminho_zip = linha["image_path"]
        caminho_saida = destino / linha["split"] / f"{int(linha['species_id']):04d}" / f"{linha['PN_hash']}.jpg"
        caminho_saida.parent.mkdir(parents=True, exist_ok=True)
        caminho_saida.write_bytes(arquivo.read(caminho_zip))
        if indice % 1000 == 0:
            print(f"Extraídas {indice} de {len(imagens)} imagens")

print(f"Concluído: {len(imagens)} imagens em {destino}")
