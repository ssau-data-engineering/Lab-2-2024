import argparse
import pandas as pd
import tensorflow as tf
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


import argparse
import pandas as pd
import tensorflow as tf
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


def train_and_save_model(input_path, output_path):
    # Загрузка подготовленных данных
    prepared_data_file = os.path.join(input_path, 'prepared_data.csv')
    data = pd.read_csv(prepared_data_file)
    print("Prepared data loaded successfully.")

    # Разделение на признаки и целевую переменную
    X = data.drop(columns=['target'])  # Замените 'target' на имя вашего столбца-цели
    y = data['target']

    # Стандартизация данных
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Разделение на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Создание улучшенной модели
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_dim=X_train.shape[1]),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.3),  # Уменьшает переобучение

        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.3),

        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.BatchNormalization(),

        tf.keras.layers.Dense(1, activation='linear')  # Для регрессии; замените на 'sigmoid' для классификации
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='mean_squared_error',
        metrics=['mae', 'mse']
    )

    # Callbacks
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    model_checkpoint = ModelCheckpoint(
    filepath=os.path.join(output_path, 'best_model.keras'),
    monitor='val_loss',
    save_best_only=True
    )


    # Обучение модели
    history = model.fit(
        X_train, y_train,
        epochs=100,
        batch_size=32,
        validation_data=(X_test, y_test),
        callbacks=[early_stopping, model_checkpoint]
    )

    # Сохранение модели
    os.makedirs(output_path, exist_ok=True)
    model.save(os.path.join(output_path, 'final_model.h5'))
    print(f"Trained model saved to {os.path.join(output_path, 'final_model.h5')}")

    # Сохранение метрик
    metrics_file = os.path.join(output_path, 'training_metrics.txt')
    with open(metrics_file, 'w') as f:
        f.write(str(history.history))
    print(f"Training metrics saved to {metrics_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a neural network model.")
    parser.add_argument('--input', required=True, help='Input directory with prepared data.')
    parser.add_argument('--output', required=True, help='Output directory for trained model and metrics.')
    args = parser.parse_args()

    train_and_save_model(args.input, args.output)
