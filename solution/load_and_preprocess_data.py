import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Путь к папке с данными
data_dir = '/data/lab2'
output_dir = '/data/lab2/goy'  # Папка для сохранения обработанных данных
os.makedirs(output_dir, exist_ok=True)  # Создаем папку, если её нет

def load_and_preprocess_data():
    # Загружаем все файлы CSV из data_dir и объединяем в один DataFrame
    data_frames = []
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(data_dir, file_name)
            df = pd.read_csv(file_path)
            data_frames.append(df)

    # Объединяем все данные в один DataFrame
    full_data = pd.concat(data_frames, ignore_index=True)

    # Кодируем категориальные значения меток (diagnosis)
    label_encoder = LabelEncoder()
    full_data['diagnosis'] = label_encoder.fit_transform(full_data['diagnosis'])

    # Разделяем данные на X и y
    X = full_data.drop(columns=['diagnosis'])  # Признаки
    y = full_data['diagnosis']                 # Метки

    # Разделяем данные на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Сохраняем обучающие и тестовые наборы данных
    X_train.to_csv(os.path.join(output_dir, 'X_train.csv'), index=False)
    X_test.to_csv(os.path.join(output_dir, 'X_test.csv'), index=False)
    y_train.to_csv(os.path.join(output_dir, 'y_train.csv'), index=False)
    y_test.to_csv(os.path.join(output_dir, 'y_test.csv'), index=False)
    
    print("Предобработанные данные сохранены в папке:", output_dir)

if __name__ == "__main__":
    load_and_preprocess_data()
