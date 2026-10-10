"""Treina três variações simples da CNN do HikeFlora.

Exemplos:
    py treinar_variacoes.py cnn_paragem
    py treinar_variacoes.py cnn_dropout
    py treinar_variacoes.py cnn_aumento
"""

import csv
import sys
from pathlib import Path

import tensorflow as tf


# Escolhe uma variação sem substituir os modelos anteriores.
opcoes = ("cnn_paragem", "cnn_dropout", "cnn_aumento")
if len(sys.argv) != 2 or sys.argv[1] not in opcoes:
    raise SystemExit("Usa: py treinar_variacoes.py cnn_paragem|cnn_dropout|cnn_aumento")

nome_modelo = sys.argv[1]
pasta = Path(__file__).parent
classes = ["0008", "0172", "0200", "0225", "0237"]
epocas = 15
tf.keras.utils.set_random_seed(42)

# Lê apenas treino e validação; o teste fica reservado para a avaliação final.
treino = tf.keras.utils.image_dataset_from_directory(
    pasta / "dataset" / "train",
    class_names=classes,
    image_size=(128, 128),
    batch_size=32,
    seed=42,
)
validacao = tf.keras.utils.image_dataset_from_directory(
    pasta / "dataset" / "val",
    class_names=classes,
    image_size=(128, 128),
    batch_size=32,
    shuffle=False,
)

# Mantém a CNN original e acrescenta as alterações escolhidas.
camadas = [tf.keras.Input(shape=(128, 128, 3))]
if nome_modelo == "cnn_aumento":
    camadas += [
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.05),
    ]
camadas += [
    tf.keras.layers.Rescaling(1.0 / 255),
    tf.keras.layers.Conv2D(16, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(2),
    tf.keras.layers.Conv2D(32, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation="relu"),
]
if nome_modelo in ("cnn_dropout", "cnn_aumento"):
    camadas.append(tf.keras.layers.Dropout(0.5))
camadas.append(tf.keras.layers.Dense(5, activation="softmax"))
modelo = tf.keras.Sequential(camadas)

# Usa os mesmos parâmetros em todas as variações.
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)
modelo.summary()
paragem = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss", patience=2, restore_best_weights=True
)
historico = modelo.fit(
    treino, validation_data=validacao, epochs=epocas,
    callbacks=[paragem], shuffle=False,
)

# Guarda a melhor época e o histórico completo desta experiência.
(pasta / "modelos").mkdir(exist_ok=True)
(pasta / "resultados").mkdir(exist_ok=True)
modelo.save(pasta / "modelos" / f"{nome_modelo}.keras")

with (pasta / "resultados" / f"{nome_modelo}_historico.csv").open(
    "w", newline="", encoding="utf-8"
) as ficheiro:
    escritor = csv.writer(ficheiro)
    escritor.writerow(["epoca", "loss", "accuracy", "val_loss", "val_accuracy"])
    for indice in range(len(historico.history["loss"])):
        escritor.writerow([
            indice + 1,
            historico.history["loss"][indice],
            historico.history["accuracy"][indice],
            historico.history["val_loss"][indice],
            historico.history["val_accuracy"][indice],
        ])

melhor_epoca = historico.history["val_loss"].index(
    min(historico.history["val_loss"])
) + 1
print(f"Treino concluído: {nome_modelo}; melhor época: {melhor_epoca}")
