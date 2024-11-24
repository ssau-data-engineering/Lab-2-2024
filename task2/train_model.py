import tensorflow as tf
import pandas as pd
import numpy as np

X_train = pd.read_csv('/data/input/X_train.csv').values
y_train = pd.read_csv('/data/input/y_train.csv').values.flatten()

model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=15, validation_split=0.2)

with open('/data/output/training_logs.txt', 'w') as f:
    f.write(str(history.history))

model.save('/data/output/model.h5')