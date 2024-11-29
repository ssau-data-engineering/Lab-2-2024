import os
import zipfile
import shutil
from pathlib import Path
from PIL import Image
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
parser.add_argument('--data_type', type=str, required=True)
parser.add_argument('--use_test_data', type=bool, action=argparse.BooleanOptionalAction)
parser.add_argument('--input_data_as_zip', type=bool, action=argparse.BooleanOptionalAction)
parser.add_argument('--use_translate_to_yolo', type=bool, action=argparse.BooleanOptionalAction)
parser.add_argument('--continue_to_adding_data', type=bool, action=argparse.BooleanOptionalAction)
args = parser.parse_args()

path_to_data = args.input
path_to_dataset = args.output
data_type = args.data_type
use_test_data = args.use_test_data
input_data_as_zip = args.input_data_as_zip
use_translate_to_yolo = args.use_translate_to_yolo
continue_to_adding_data = args.continue_to_adding_data


# Разрешение входных изображений
resolution = (1920, 1080)

# Имена классов, ключи строго по порядку возрастания
class_names = {
    0: "bird",
    1: "cable",
    2: "tree",
    3: "animal",
    4: "drone",
    5: "pedestrian",
    6: "people",
    7: "bicycle",
    8: "car",
    9: "van",
    10: "truck",
    11: "bus",
    12: "motor",
}

visdrone_class_names = {
    0: "ignored regions",
    1: "pedestrian",
    2: "people",
    3: "bicycle",
    4: "car",
    5: "van",
    6: "truck",
    7: "tricycle",
    8: "awning-tricycle",
    9: "bus",
    10: "motor",
    11: "others",
}

# Возможные расширения изображений
images_extentions = {".png", ".jpeg", ".jpg"}

# Расширение файлов с лейблами
current_labels_ext = ".csv"
if data_type == "visdrone":
    current_labels_ext = ".txt"

# Разделитель не только в csv!!!
csv_delimeter = ","

# Название папок с изображениями в входных данных
images_dir_name = "images"

# Название папок с лейблами в входных данных
labels_dir_name = "labels"
if data_type == "visdrone":
    labels_dir_name = "annotations"

# Число знаков в новых названиях файлов, к примеру: 6 - 000001.png
num_of_signs_in_name = 6

# Распределение на учебную и валидационную выборки, 0.8 = 80% на 20%
train_val_split = 0.8

path_to_images = os.path.join(path_to_dataset, "images")
path_to_labels = os.path.join(path_to_dataset, "labels")

path_to_train_images = os.path.join(path_to_images, "train")
path_to_val_images = os.path.join(path_to_images, "val")
path_to_test_images = os.path.join(path_to_images, "test")

path_to_train_labels = os.path.join(path_to_labels, "train")
path_to_val_labels = os.path.join(path_to_labels, "val")
path_to_test_labels = os.path.join(path_to_labels, "test")


def transform_file_to_yolo(in_file):
    with in_file.open(mode="r+") as file:
        content = file.read()

        lines = content.split("\n")
        table = [line.split(csv_delimeter) for line in lines]

        yolo_table = []

        for row in table:
            class_name, up_left_x, up_left_y, down_right_x, down_right_y = row

            encoded_class_name = -1
            for key, val in class_names.items(): 
                if val == class_name: 
                    encoded_class_name = key 
                    break
            
            width = int(down_right_x) - int(up_left_x)
            height = int(down_right_y) - int(up_left_y)
            width_norm = round(width / float(resolution[0]), 6)
            height_norm = round(height / float(resolution[1]), 6)
            center_x = float(up_left_x) + width / 2.0
            center_y = float(up_left_y) + height / 2.0
            center_x_norm = round(center_x / float(resolution[0]), 6)
            center_y_norm = round(center_y / float(resolution[1]), 6)

            new_row = " ".join([str(encoded_class_name), str(center_x_norm), str(center_y_norm), str(width_norm), str(height_norm)])
            yolo_table.append(new_row)

        file.seek(0)

        file.write("\n".join(yolo_table))
    
    shutil.move(in_file.resolve(), os.path.join(os.path.split(in_file.resolve())[0], os.path.splitext(in_file.name)[0] + ".txt"))

def transform_file_to_yolo_from_visdrone(in_file):
    with in_file.open(mode="r+") as file:
        content = file.read()

        lines = content.split("\n")
        table = [line.split(csv_delimeter) for line in lines]

        yolo_table = []

        lbl_dir_path, lbl_name = os.path.split(str(in_file))
        lbl_name_noext, _ = os.path.splitext(lbl_name)
        parent_dir_path, _ = os.path.split(lbl_dir_path)
        image_dir_path = os.path.join(parent_dir_path, images_dir_name)
        image_path = ""

        for f in Path(image_dir_path).rglob(f"{lbl_name_noext}.*"):
            image_path = str(f)
            break
        
        with Image.open(image_path) as img:
            resolution = img.size

        for row in table:
            try:
                up_left_x, up_left_y, width, height, _, class_name, _, _ = row
            except:
                continue

            if visdrone_class_names[int(class_name)] in ["ignored regions", "tricycle", "awning-tricycle", "others"]:
                continue
            
            for key, val in class_names.items(): 
                if val == visdrone_class_names[int(class_name)]: 
                    encoded_class_name = key 
                    break
            
            width_norm = round(float(width) / float(resolution[0]), 6)
            height_norm = round(float(height) / float(resolution[1]), 6)
            center_x = float(up_left_x) + float(width) / 2.0
            center_y = float(up_left_y) + float(height) / 2.0
            center_x_norm = round(center_x / float(resolution[0]), 6)
            center_y_norm = round(center_y / float(resolution[1]), 6)

            new_row = " ".join([str(encoded_class_name), str(center_x_norm), str(center_y_norm), str(width_norm), str(height_norm)])
            yolo_table.append(new_row)

        file.seek(0)

        file.write("\n".join(yolo_table))


def main():
    if not os.path.exists(path_to_dataset):
        os.makedirs(path_to_dataset)
        os.makedirs(path_to_train_images, exist_ok=True)
        os.makedirs(path_to_val_images, exist_ok=True)
        os.makedirs(path_to_train_labels, exist_ok=True)
        os.makedirs(path_to_val_labels, exist_ok=True)

        if use_test_data:
            os.makedirs(path_to_test_images, exist_ok=True)
            os.makedirs(path_to_test_labels, exist_ok=True)
        
        with open(os.path.join(path_to_dataset, "data.yaml"), "w") as file:
            file.write(f"path: {path_to_dataset}\n")
            file.write(f"train: {os.path.join('images', 'train')}\n")
            file.write(f"val: {os.path.join('images', 'val')}\n")

            if use_test_data:
                file.write(f"test: {os.path.join('images', 'test')}\n")

            file.write(f"\nnames:\n")

            for idx, name in class_names.items():
                file.write(f"    {idx}: {name}\n")

    global path_to_data
    path_to_zip = path_to_data
    path_to_data = "yolotemp"

    if input_data_as_zip and not os.path.exists("yolotemp"):
        os.makedirs(path_to_data, exist_ok=True)
        with zipfile.ZipFile(path_to_zip, 'r') as zip_ref:
            zip_ref.extractall(path_to_data)

    if data_type == 'synth':
        if use_translate_to_yolo:
            for file in Path("yolotemp").rglob(f"*{current_labels_ext}"):
                transform_file_to_yolo(file)

        dir_to_search = Path(path_to_data)

        # Сопоставление путей до изображений и путей до соответствующих лейблов
        img_lbl_matching = {}

        for folder in dir_to_search.rglob("*"):
            if folder.name != images_dir_name:
                continue

            for file in folder.rglob("*"):
                if file.suffix.lower() not in images_extentions:
                    continue
                
                # получаем путь папки с изображениями и имя изображения
                img_dir_path, img_name = os.path.split(file.resolve())
                # получаем путь родительской папки, где лежат images и labels
                parent_dir, _ = os.path.split(img_dir_path)
                # получаем путь папки с лейблами
                lbl_dir_path = os.path.join(parent_dir, labels_dir_name)
                # получаем имя лейбла, соответствующее изображению, строго по цифре в названии
                lbl_name = str(int(os.path.splitext(img_name)[0]))
                # добавляем в матчинг путь до изображения и путь до лейбла
                img_lbl_matching[str(file)] = os.path.join(lbl_dir_path, lbl_name + ".txt")

        print("Текущее сопоставление путей до изображений с путями до файлов разметки:\n")
        print(img_lbl_matching)

    if data_type == 'visdrone':
        if use_translate_to_yolo:
            for file in Path("yolotemp").rglob(f"*{current_labels_ext}"):
                transform_file_to_yolo_from_visdrone(file)

        dir_to_search = Path(path_to_data)
        # Сопоставление путей до изображений и путей до соответствующих лейблов
        img_lbl_matching = {}

        for folder in dir_to_search.rglob("*"):
            if folder.name != images_dir_name:
                continue

            for file in folder.rglob("*"):
                if file.suffix.lower() not in images_extentions:
                    continue
                
                # получаем путь папки с изображениями и имя изображения
                img_dir_path, img_name = os.path.split(str(file))
                # получаем путь родительской папки, где лежат images и labels
                parent_dir, _ = os.path.split(img_dir_path)
                # получаем путь папки с лейблами
                lbl_dir_path = os.path.join(parent_dir, labels_dir_name)
                # получаем имя лейбла, соответствующее изображению
                lbl_name = os.path.splitext(img_name)[0]
                # добавляем в матчинг путь до изображения и путь до лейбла
                img_lbl_matching[str(file)] = os.path.join(lbl_dir_path, lbl_name + ".txt")

        print("Текущее сопоставление путей до изображений с путями до файлов разметки:\n")
        print(img_lbl_matching)

    train_matching = {}
    val_matching = {}

    split_index = int(len(img_lbl_matching) * train_val_split)

    for idx, (p_img, p_lbl) in enumerate(img_lbl_matching.items()):
        if idx < split_index:
            train_matching[p_img] = p_lbl
        else:
            val_matching[p_img] = p_lbl

    print(len(train_matching))
    print(train_matching)
    print(len(val_matching))
    print(val_matching)

    train_max = len(train_matching)
    val_max = len(val_matching)

    train_names = []
    val_names = []

    # Если продолжаем добавлять, то нужно посчитать количество имеющихся данных и продолжить нумерацию
    if continue_to_adding_data:
        existing_train_num = sum([1 for file in Path(path_to_train_images).rglob("*")])
        existing_val_num = sum([1 for file in Path(path_to_val_images).rglob("*")])

        train_names = [str(i).zfill(num_of_signs_in_name) for i in range(existing_train_num, train_max + existing_train_num)]
        val_names = [str(i).zfill(num_of_signs_in_name) for i in range(existing_val_num, val_max + existing_val_num)]
    else:
        train_names = [str(i).zfill(num_of_signs_in_name) for i in range(train_max)]
        val_names = [str(i).zfill(num_of_signs_in_name) for i in range(val_max)]

    for idx, (p_img, p_lbl) in enumerate(train_matching.items()):
        shutil.copy(p_img, os.path.join(path_to_train_images, train_names[idx] + os.path.splitext(os.path.split(p_img)[1])[1]))
        shutil.copy(p_lbl, os.path.join(path_to_train_labels, train_names[idx] + os.path.splitext(os.path.split(p_lbl)[1])[1]))

    for idx, (p_img, p_lbl) in enumerate(val_matching.items()):
        shutil.copy(p_img, os.path.join(path_to_val_images, val_names[idx] + os.path.splitext(os.path.split(p_img)[1])[1]))
        shutil.copy(p_lbl, os.path.join(path_to_val_labels, val_names[idx] + os.path.splitext(os.path.split(p_lbl)[1])[1]))


    shutil.rmtree("yolotemp")


if __name__ == "__main__":
    main()