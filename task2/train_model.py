import numpy as np
import pandas as pd
import tensorflow as tf

X_train = pd.read_csv('/data/X_train.csv').values
y_train = pd.read_csv('/data/y_train.csv').values.flatten()

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=5, validation_split=0.2)

with open('/data/training_logs.txt', 'w') as f:
    f.write(str(history.history))

model.save('/data/model.h5')