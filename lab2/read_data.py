import numpy as np
from sklearn.model_selection import train_test_split

X = np.load("/data/x_full.npy")
y = np.load("/data/y_full.npy")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, train_size=0.5, random_state=42)

np.save('/data/x_train.npy', X_train)
np.save('/data/x_val.npy', X_val)
np.save('/data/x_test.npy', X_test)
np.save('/data/y_train.npy', y_train)
np.save('/data/y_val.npy', y_val)
np.save('/data/y_test.npy', y_test)