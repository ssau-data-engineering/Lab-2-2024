import os
import numpy as np
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def get_input_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data/input')

def load_iris_data():
    input_dir = get_input_dir()
    iris_data = pd.read_csv(os.path.join(input_dir, 'iris.csv'))
    return iris_data

data = load_iris_data()

data = data.dropna()

label_encoders = {}
le = LabelEncoder()
data['species'] = le.fit_transform(data['species'])
label_encoders['species'] = le

X = data.drop(columns=['species']).values
y = data['species'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Обучающая выборка:", X_train.shape)
print("Тестовая выборка:", X_test.shape)

with open('prepared_iris_data.pkl', 'wb') as f:
    pickle.dump((X_train, X_test, y_train, y_test), f)
