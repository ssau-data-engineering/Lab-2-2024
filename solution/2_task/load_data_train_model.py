import os
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import CSVLogger
import pandas as pd

# Путь к папке с предварительно обработанными данными
data_dir = '/data/lr2/opr'

# Загрузка данных из файлов
X_train = pd.read_csv(os.path.join(data_dir, 'X_train.csv')).values
X_test = pd.read_csv(os.path.join(data_dir, 'X_test.csv')).values
y_train = pd.read_csv(os.path.join(data_dir, 'y_train.csv')).values.ravel()
y_test = pd.read_csv(os.path.join(data_dir, 'y_test.csv')).values.ravel()

model = Sequential([
    Dense(30, input_shape=(X_train.shape[1],), activation='relu'),  # Входной слой с 30 нейронами и функцией активации ReLU
    Dense(15, activation='relu'),  # Скрытый слой с 15 нейронами и функцией активации ReLU
    Dense(1, activation='sigmoid')  # Выходной слой с 1 нейроном и сигмоидальной активацией для бинарной классификации
])

# Компилируем модель, указывая оптимизатор, функцию потерь и метрики для оценки
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Задаем директорию для сохранения логов обучения
log_dir = '/data/logs'
os.makedirs(log_dir, exist_ok=True) 

# Определяем файл для записи логов обучения и создаем CSV логгер
log_file = os.path.join(log_dir, 'training_logs.csv')
csv_logger = CSVLogger(log_file, append=True)

# Тренируем модель на обучающем наборе данных, указывая тестовые данные для проверки
# Используем csv_logger для записи метрик в файл на каждой эпохе
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=1000, callbacks=[csv_logger])

# Сохраняем обученную модель в файл в указанной директории
model.save(os.path.join(log_dir, 'trained_model.h5'))

print("Обучение завершено и модель сохранена.")