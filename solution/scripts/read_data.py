import argparse
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer


def read_and_preprocess(input_path, output_path):
    # Пример загрузки данных
    file_path = os.path.join(input_path, 'data.csv')

    # Чтение данных
    data = pd.read_csv(file_path)
    print("Data loaded successfully.")

    # Сохранение целевого столбца
    target = data['Survived']  # Используй имя столбца целевой переменной

    # Удаление дубликатов
    data = data.drop_duplicates()

    # Определение типов данных
    numeric_features = data.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = data.select_dtypes(include=['object']).columns

    # Удаляем целевой столбец из признаков
    numeric_features = numeric_features.drop('Survived', errors='ignore')

    # Предобработка числовых данных
    numeric_transformer = StandardScaler()

    # Предобработка категориальных данных
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    # Импьютер для заполнения пропусков
    imputer = SimpleImputer(strategy='mean')

    # Объединение всех трансформеров
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    # Заполнение пропусков
    data[numeric_features] = imputer.fit_transform(data[numeric_features])

    # Применение трансформеров
    processed_data = preprocessor.fit_transform(data).toarray()

    # Преобразование в DataFrame
    processed_data = pd.DataFrame(processed_data)

    # Добавляем целевой столбец
    processed_data['target'] = target.values

    # Сохранение подготовленных данных
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, 'prepared_data.csv')
    processed_data.to_csv(output_file, index=False)
    print(f"Prepared data saved to {output_file}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read and preprocess data.")
    parser.add_argument('--input', required=True, help='Input directory with raw data.')
    parser.add_argument('--output', required=True, help='Output directory for prepared data.')
    args = parser.parse_args()

    read_and_preprocess(args.input, args.output)
