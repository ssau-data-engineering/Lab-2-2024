import os
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder

data_train = pd.read_csv('/data/mnist_train.csv')
data_test = pd.read_csv('/data/mnist_test.csv')

# Ограничиваем размер выборок для ускорения обучения
data_train = data_train[:2000]
data_test = data_test[:400]

# Преобразуем данные в массивы NumPy
data_train_copy = data_train.copy()
data_test_copy = data_test.copy()

# Убираем столбец с метками классов
del data_train_copy['label']
del data_test_copy['label']

# Присваиваем новые переменные для данных
X_train = data_train_copy
X_test = data_test_copy

# Нормализация данных (делим на 255)
X_train /= 255
X_test /= 255

# Кодируем метки классов с помощью OneHotEncoder
encoding = OneHotEncoder(sparse_output=False, handle_unknown='error')
labels = pd.concat([data_train[['label']], data_test[['label']]])

# Преобразование меток классов в one-hot кодировку
encoding.fit(labels)
y_train = pd.DataFrame(encoding.transform(data_train[['label']]))
y_test = pd.DataFrame(encoding.fit_transform(data_test[['label']]))


# Сохраняем обучающие и тестовые наборы данных
X_train.to_csv(os.path.join('/data', 'X_train.csv'), index=False)
X_test.to_csv(os.path.join('/data', 'X_test.csv'), index=False)
y_train.to_csv(os.path.join('/data', 'y_train.csv'), index=False)
y_test.to_csv(os.path.join('/data', 'y_test.csv'), index=False)
