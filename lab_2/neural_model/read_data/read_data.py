import os
import shutil
import argparse
from sklearn.model_selection import train_test_split

def split_dataset(source_dir, dataset_dir, val_size):
    # Создание целевых директорий /train и /val
    for subset in ['train', 'val']:
        for class_name in os.listdir(source_dir):
            os.makedirs(os.path.join(dataset_dir, subset, class_name), exist_ok=True)

    # Разделение и копирование файлов
    for class_name in os.listdir(source_dir):
        class_path = os.path.join(source_dir, class_name)
        if os.path.isdir(class_path):
            files = os.listdir(class_path)
            train_files, val_files = train_test_split(files, test_size=val_size, random_state=42)
            
            # Копирование файлов в соответствующие каталоги
            for file in train_files:
                shutil.copy2(os.path.join(class_path, file), os.path.join(dataset_dir, 'train', class_name, file))
            for file in val_files:
                shutil.copy2(os.path.join(class_path, file), os.path.join(dataset_dir, 'val', class_name, file))

    print(f"Данные успешно разделены и сохранены в каталоге '{dataset_dir}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Разделение данных на тренировочную и валидационную выборки.")
    parser.add_argument("source_dir", type=str, help="Путь к исходному каталогу с данными.")
    parser.add_argument("dataset_dir", type=str, help="Путь для сохранения разделённого набора данных.")
    parser.add_argument("--val_size", type=float, default=0.2, help="Доля данных для валидации (по умолчанию 0.2).")

    args = parser.parse_args()
    
    # Вызов функции для разделения набора данных
    split_dataset(args.source_dir, args.dataset_dir, args.val_size)
