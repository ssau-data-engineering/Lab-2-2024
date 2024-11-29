import os
import numpy as np
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer


def get_input_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data/input')

def join_data():
    input_dir = get_input_dir()
    df = pd.concat([pd.read_csv(os.path.join(input_dir, f'chunk{i}.csv')) for i in range(26)], axis=0)
    return df


data = join_data()

data = data.dropna()

label_encoders = {}
for column in ['country', 'designation', 'province', 'region_1', 
               'region_2', 'taster_name', 'taster_twitter_handle', 
               'variety', 'winery']:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

tfidf_vectorizer = TfidfVectorizer(max_features=5000) 
X_text = tfidf_vectorizer.fit_transform(data['description']).toarray()

X = pd.DataFrame(X_text)
for column in ['country', 'designation', 'province', 'region_1', 
               'region_2', 'taster_name', 'taster_twitter_handle', 
               'variety', 'winery']:
    X[column] = data[column].values

y = data['points'].values  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Обучающая выборка:", X_train.shape)
print("Тестовая выборка:", X_test.shape)

with open('prepared_data.pkl', 'wb') as f:
    pickle.dump((X_train, X_test, y_train, y_test), f)
