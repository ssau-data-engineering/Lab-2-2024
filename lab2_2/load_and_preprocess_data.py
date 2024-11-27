import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

out_dir = '/data/out'
data = pd.read_csv('/data/in/Housing.csv')

#Кодируем категориальные значения
label_encoder = LabelEncoder()
data['mainroad'] = label_encoder.fit_transform(data['mainroad'])
data['guestroom'] = label_encoder.fit_transform(data['guestroom'])
data['basement'] = label_encoder.fit_transform(data['basement'])
data['hotwaterheating'] = label_encoder.fit_transform(data['hotwaterheating'])
data['airconditioning'] = label_encoder.fit_transform(data['airconditioning'])
data['prefarea'] = label_encoder.fit_transform(data['prefarea'])
data['furnishingstatus'] = label_encoder.fit_transform(data['furnishingstatus'])

#Разделяем данные на X и y
X = data.drop(columns=['bedrooms'])
y = data['bedrooms']

#Разделяем данные на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=123)

#Сохраняем обучающие и тестовые наборы данных
X_train.to_csv(os.path.join(out_dir, 'X_train.csv'), index=False)
X_test.to_csv(os.path.join(out_dir, 'X_test.csv'), index=False)
y_train.to_csv(os.path.join(out_dir, 'y_train.csv'), index=False)
y_test.to_csv(os.path.join(out_dir, 'y_test.csv'), index=False)