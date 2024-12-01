import numpy as np
import pandas as pd
from tensorflow.keras.datasets import mnist

(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(-1, 28*28) / 255.0
X_test = X_test.reshape(-1, 28*28) / 255.0

pd.DataFrame(X_train).to_csv('/data/X_train.csv', index=False)
pd.DataFrame(X_test).to_csv('/data/X_test.csv', index=False)
pd.DataFrame(y_train).to_csv('/data/y_train.csv', index=False)
pd.DataFrame(y_test).to_csv('/data/y_test.csv', index=False)