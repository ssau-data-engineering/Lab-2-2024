import argparse
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model
from datetime import datetime


def dice_coefficient(y_true, y_pred):
    y_true_f = tf.keras.backend.flatten(y_true)
    y_pred_f = tf.keras.backend.flatten(y_pred)
    intersection = tf.keras.backend.sum(y_true_f * y_pred_f)
    return (2 * intersection) / (
        tf.keras.backend.sum(y_true_f) + tf.keras.backend.sum(y_pred_f)
    )


def dice_coefficient_loss(y_true, y_pred):
    return -dice_coefficient(y_true, y_pred)


def customized_loss(y_true, y_pred):
    return 1 + dice_coefficient_loss(y_true, y_pred)


if __name__ == "__main__":
    start_time = datetime.now()
    output = f"Начало выполнения -> {start_time}\n"
    name_log = "log.txt"

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Путь к данным")
    parser.add_argument("--output", type=str, required=True, help="Путь к модели")

    args = parser.parse_args()

    file_directory = os.path.dirname(os.path.abspath(__file__))

    folder_path_input_data = os.path.join(file_directory, args.input[1:])
    folder_path_model = os.path.join(file_directory, args.output[1:])

    path_x = os.path.join(folder_path_input_data, "train_x.npy")
    path_y = os.path.join(folder_path_input_data, "train_y.npy")

    train_x = np.load(path_x)
    train_y = np.load(path_y)

    path_model = os.path.join(folder_path_model, "model.h5")
    model = load_model(path_model)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss=customized_loss,
        metrics=["accuracy", dice_coefficient],
    )
    history = model.fit(train_x, train_y, epochs=10, batch_size=10)

    for epoch, (loss, accuracy, dice) in enumerate(
        zip(
            history.history["loss"],
            history.history["accuracy"],
            history.history["dice_coefficient"],
        )
    ):
        output += f"Epoch {epoch + 1}: Loss = {loss:.4f}, accuracy = {accuracy:.4f}, Dice Coefficient = {dice:.4f}\n"
    end_time = datetime.now()
    output += f"Конец выполнения -> {end_time}\n"

    path_log_txt = os.path.join(file_directory, name_log)
    with open(path_log_txt, "a", encoding="utf-8") as f:
          f.write(output)
