import os
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization
from tensorflow.keras.callbacks import CSVLogger, EarlyStopping
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Путь к папке с предварительно обработанными данными
data_dir = '/data/lr2/opr'

# Загрузка данных из файлов
X_train = pd.read_csv(os.path.join(data_dir, 'X_train.csv')).values
X_test = pd.read_csv(os.path.join(data_dir, 'X_test.csv')).values
y_train = pd.read_csv(os.path.join(data_dir, 'y_train.csv')).values.ravel()
y_test = pd.read_csv(os.path.join(data_dir, 'y_test.csv')).values.ravel()

# Нормализация данных
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Преобразование меток в формат one-hot encoding
# Удаляем параметр 'sparse'
encoder = OneHotEncoder()  # sparse=False не требуется, по умолчанию уже False
y_train = encoder.fit_transform(y_train.reshape(-1, 1)).toarray()
y_test = encoder.transform(y_test.reshape(-1, 1)).toarray()

# Создание модели
model = Sequential([
    Dense(128, input_shape=(X_train.shape[1],), activation='relu'),  # Входной слой
    BatchNormalization(),
    Dense(64, activation='relu'),  # Скрытый слой
    BatchNormalization(),
    Dense(32, activation='relu'),  # Дополнительный скрытый слой
    Dense(3, activation='softmax')   # Выходной слой для 3 классов
])

# Компиляция модели
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Задаем директорию для сохранения логов обучения
log_dir = '/data/logs'
os.makedirs(log_dir, exist_ok=True)

# Определяем файл для записи логов обучения и создаем CSV логгер
log_file = os.path.join(log_dir, 'training_logs.csv')
csv_logger = CSVLogger(log_file, append=True)

# Ранняя остановка для предотвращения переобучения
early_stopping = EarlyStopping(monitor='val_loss', patience=50, restore_best_weights=True)

# Тренируем модель
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20,
          callbacks=[csv_logger, early_stopping])

# Сохраняем обученную модель в файл
model.save(os.path.join(log_dir, 'trained_model.h5'))

print("Обучение завершено и модель сохранена.")
