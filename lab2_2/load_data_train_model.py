import os
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.callbacks import CSVLogger

data_dir = '/data/out'

#Загружаем обучающие и тестовые наборы данных
X_train = pd.read_csv(os.path.join(data_dir, 'X_train.csv')).values
X_test = pd.read_csv(os.path.join(data_dir, 'X_test.csv')).values
y_train = pd.read_csv(os.path.join(data_dir, 'y_train.csv')).values.ravel()
y_test = pd.read_csv(os.path.join(data_dir, 'y_test.csv')).values.ravel()

#Создаем простейшую полносвязную нс
model = Sequential()
model.add(Dense(256, input_dim=12, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

#Компилируем модель
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

log_file = os.path.join(data_dir, 'logs.csv')
csv_logger = CSVLogger(log_file, append=True)

#Тренируем модель
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=32, callbacks=[csv_logger])
#Сохраняем обученную модель
model.save(os.path.join(data_dir, 'model.h5'))