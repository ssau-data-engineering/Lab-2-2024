import pandas as pd
import numpy as np

data = pd.read_csv("/data/input/Iris.csv")
data['Species'] = data['Species'].replace({'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2})

X = data.drop('Species', axis=1).values
y = data['Species'].values

test_size = 0.2
num_test_samples = int(test_size * len(X))

np.random.seed(42)
indices = np.random.permutation(len(X))

train_indices = indices[num_test_samples:]
test_indices = indices[:num_test_samples]

X_train, X_test = X[train_indices], X[test_indices]
y_train, y_test = y[train_indices], y[test_indices]

mean = np.mean(X_train, axis=0)
std = np.std(X_train, axis=0)

std[std == 0] = 1

X_train = (X_train - mean) / std
X_test = (X_test - mean) / std

pd.DataFrame(X_train).to_csv('/data/input/X_train.csv', index=False)
pd.DataFrame(X_test).to_csv('/data/input/X_test.csv', index=False)
pd.DataFrame(y_train).to_csv('/data/input/y_train.csv', index=False)
pd.DataFrame(y_test).to_csv('/data/input/y_test.csv', index=False)