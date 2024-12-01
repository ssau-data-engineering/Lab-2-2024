import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping

with open('prepared_iris_data.pkl', 'rb') as f:
    X_train, X_test, y_train, y_test = pickle.load(f)

model = models.Sequential([
    layers.Dense(10, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dense(10, activation='relu'),
    layers.Dense(3, activation='softmax')  # 3 класса для Iris
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

model.save('iris_model.h5')

with open('training_history.txt', 'w') as f:
    f.write("Epoch\tLoss\tVal Loss\tAccuracy\tVal Accuracy\n")
    for epoch in range(len(history.history['loss'])):
        f.write(f"{epoch+1}\t{history.history['loss'][epoch]}\t{history.history['val_loss'][epoch]}\t{history.history['accuracy'][epoch]}\t{history.history['val_accuracy'][epoch]}\n")
