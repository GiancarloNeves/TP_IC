"""Treina uma MLP ou uma CNN com as cinco espécies do HikeFlora.

Exemplos:
    py treinar.py mlp
    py treinar.py cnn
"""

import csv
import sys
from pathlib import Path

import tensorflow as tf


# Escolhe o modelo indicado no terminal.
if len(sys.argv) != 2 or sys.argv[1] not in ("mlp", "cnn"):
    raise SystemExit("Usa: py treinar.py mlp  ou  py treinar.py cnn")

nome_modelo = sys.argv[1]
pasta = Path(__file__).parent
classes = ["0008", "0172", "0200", "0225", "0237"]
tamanho = (128, 128)
batch = 32
epocas = 10
tf.keras.utils.set_random_seed(42)

# Lê as imagens de treino e validação nas pastas preparadas na parte 1.
treino = tf.keras.utils.image_dataset_from_directory(
    pasta / "dataset" / "train",
    class_names=classes,
    image_size=tamanho,
    batch_size=batch,
    seed=42,
)
validacao = tf.keras.utils.image_dataset_from_directory(
    pasta / "dataset" / "val",
    class_names=classes,
    image_size=tamanho,
    batch_size=batch,
    shuffle=False,
)

# Define duas arquiteturas simples para comparar.
if nome_modelo == "mlp":
    modelo = tf.keras.Sequential([
        tf.keras.Input(shape=(128, 128, 3)),
        tf.keras.layers.Rescaling(1.0 / 255),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(5, activation="softmax"),
    ])
else:
    modelo = tf.keras.Sequential([
        tf.keras.Input(shape=(128, 128, 3)),
        tf.keras.layers.Rescaling(1.0 / 255),
        tf.keras.layers.Conv2D(16, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Conv2D(32, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(5, activation="softmax"),
    ])

# Usa os mesmos parâmetros de treino nos dois modelos.
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)
modelo.summary()
# O carregador já baralha o treino; a validação fica em ordem fixa.
historico = modelo.fit(
    treino, validation_data=validacao, epochs=epocas, shuffle=False
)

# Guarda o modelo treinado e os valores de cada época.
(pasta / "modelos").mkdir(exist_ok=True)
(pasta / "resultados").mkdir(exist_ok=True)
modelo.save(pasta / "modelos" / f"{nome_modelo}.keras")

with (pasta / "resultados" / f"{nome_modelo}_historico.csv").open(
    "w", newline="", encoding="utf-8"
) as ficheiro:
    escritor = csv.writer(ficheiro)
    escritor.writerow(["epoca", "loss", "accuracy", "val_loss", "val_accuracy"])
    for indice in range(epocas):
        escritor.writerow([
            indice + 1,
            historico.history["loss"][indice],
            historico.history["accuracy"][indice],
            historico.history["val_loss"][indice],
            historico.history["val_accuracy"][indice],
        ])

print(f"Treino concluído: {nome_modelo}")
