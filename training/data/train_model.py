import os
import sys
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.callbacks import CSVLogger


def main(inp, out):
    x_train = pd.read_csv(os.path.join(inp, 'x_train.csv')).values
    x_test = pd.read_csv(os.path.join(inp, 'x_test.csv')).values
    y_train = pd.read_csv(os.path.join(inp, 'y_train.csv')).values.ravel()
    y_test = pd.read_csv(os.path.join(inp, 'y_test.csv')).values.ravel()

    model = Sequential()
    model.add(Dense(256, input_dim=8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    log_file = os.path.join(out, 'logs.csv')
    csv_logger = CSVLogger(log_file, append=True)

    model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=100, batch_size=32,
              callbacks=[csv_logger])
    model.save(os.path.join(out, 'model.h5'))


main(sys.argv[1], sys.argv[2])