"""Avalia a MLP e a CNN escolhida nas imagens de teste do HikeFlora."""

from pathlib import Path

import numpy as np
import tensorflow as tf


pasta = Path(__file__).parent
classes = ["0008", "0172", "0200", "0225", "0237"]
nomes = ["Gerânio", "Alfazema", "Papoila", "Trevo-branco", "Morangueiro"]

# Lê o teste uma única vez, sem baralhar a ordem das imagens.
teste = tf.keras.utils.image_dataset_from_directory(
    pasta / "dataset" / "test",
    class_names=classes,
    image_size=(128, 128),
    batch_size=32,
    shuffle=False,
)
verdadeiros = np.concatenate([rotulos.numpy() for _, rotulos in teste])
linhas = []

for nome_modelo in ("mlp", "cnn_dropout"):
    # Obtém as probabilidades e a classe prevista pelo modelo guardado.
    modelo = tf.keras.models.load_model(pasta / "modelos" / f"{nome_modelo}.keras")
    probabilidades = modelo.predict(teste, verbose=0)
    previstos = np.argmax(probabilidades, axis=1)

    matriz = np.zeros((5, 5), dtype=int)
    for real, previsto in zip(verdadeiros, previstos):
        matriz[real, previsto] += 1

    recalls = []
    especificidades = []
    f1s = []
    aucs = []

    # Calcula as métricas para cada classe contra as outras quatro.
    for indice in range(5):
        vp = matriz[indice, indice]
        fn = matriz[indice, :].sum() - vp
        fp = matriz[:, indice].sum() - vp
        vn = matriz.sum() - vp - fn - fp
        recall = vp / (vp + fn)
        precisao = vp / (vp + fp) if vp + fp else 0
        f1 = 2 * precisao * recall / (precisao + recall) if precisao + recall else 0
        recalls.append(recall)
        especificidades.append(vn / (vn + fp))
        f1s.append(f1)

        # AUC: fração de pares em que a imagem da classe recebe maior probabilidade.
        positivos = probabilidades[verdadeiros == indice, indice]
        negativos = probabilidades[verdadeiros != indice, indice]
        aucs.append(
            np.mean(positivos[:, None] > negativos)
            + 0.5 * np.mean(positivos[:, None] == negativos)
        )

    linhas.append(f"Modelo: {nome_modelo}")
    linhas.append(f"Accuracy: {np.mean(verdadeiros == previstos):.4f}")
    linhas.append(f"Recall macro: {np.mean(recalls):.4f}")
    linhas.append(f"Especificidade macro: {np.mean(especificidades):.4f}")
    linhas.append(f"F1 macro: {np.mean(f1s):.4f}")
    linhas.append(f"AUC macro (um contra os restantes): {np.mean(aucs):.4f}")
    linhas.append("Por classe: recall | especificidade | F1 | AUC")
    for indice, nome in enumerate(nomes):
        linhas.append(
            f"{nome}: {recalls[indice]:.4f} | {especificidades[indice]:.4f} | "
            f"{f1s[indice]:.4f} | {aucs[indice]:.4f}"
        )
    linhas.append("Matriz de confusão: linhas reais, colunas previstas")
    linhas.append("classe," + ",".join(nomes))
    for indice, nome in enumerate(nomes):
        linhas.append(nome + "," + ",".join(str(valor) for valor in matriz[indice]))
    linhas.append("")

# Guarda todos os resultados num único ficheiro fácil de enviar e consultar.
(pasta / "resultados").mkdir(exist_ok=True)
saida = pasta / "resultados" / "avaliacao_teste.txt"
saida.write_text("\n".join(linhas), encoding="utf-8")
print("\n".join(linhas))
print(f"Resultados guardados em {saida}")
