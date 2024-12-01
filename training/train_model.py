import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.callbacks import CSVLogger



x_train = pd.read_csv('data/x_train.csv').values
x_test = pd.read_csv('data/x_test.csv').values
y_train = pd.read_csv('data/y_train.csv').values.ravel()
y_test = pd.read_csv('data/y_test.csv').values.ravel()

model = Sequential()
model.add(Dense(256, input_dim=5, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


model.fit(
    x_train,
    y_train,
    validation_data=(x_test, y_test),
    epochs=100, batch_size=32,
    callbacks=[CSVLogger('data/logs.csv', append=True)]
)
model.save('data/model.h5')
