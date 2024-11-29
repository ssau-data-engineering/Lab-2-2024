import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
      
        
with open('prepared_data.pkl', 'rb') as f:
    X_train, X_test, y_train, y_test = pickle.load(f)

model = Sequential()
model.add(Dense(128, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dropout(0.2))  
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

model.save('wine_model.h5')

with open('training_history.txt', 'w') as f:
    f.write("Epoch\tLoss\tVal Loss\n")
    for epoch in range(len(history.history['loss'])):
        f.write(f"{epoch+1}\t{history.history['loss'][epoch]}\t{history.history['val_loss'][epoch]}\n")
        
        