import numpy as np
import argparse
import os
from PIL import Image

if __name__ == "__main__":

     parser = argparse.ArgumentParser()
     parser.add_argument('--input', type=str, required=True, help='Путь к входной директории')
     parser.add_argument('--output', type=str, required=True, help='Путь к выходной директории')

     args = parser.parse_args()

     
     file_directory = os.path.dirname(os.path.abspath(__file__))

     path_input = os.path.join(file_directory, args.input[1:])
     path_output = os.path.join(file_directory, args.output[1:])

     folder_path_x = os.path.join(path_input, 'x')
     folder_path_y = os.path.join(path_input, 'y')
     
     file_names_x = os.listdir(folder_path_x)
     file_names_y = os.listdir(folder_path_y)

     train_x = []
     train_y = []

     for name_x, name_y in zip(file_names_x,file_names_y):

        path_to_x = os.path.join(folder_path_x, name_x)
        path_to_y = os.path.join(folder_path_y, name_y)

        img_x = Image.open(path_to_x)
        img_y = Image.open(path_to_y)

        img_x_array = np.expand_dims(np.array(img_x) / 255.0, axis=-1)
        img_y_array = np.array(img_y)

        img_y_one_hot = np.zeros((*img_y_array.shape, 2), dtype=np.float32)
        img_y_one_hot[..., 0] = (img_y_array == 0).astype(np.float32)
        img_y_one_hot[..., 1] = (img_y_array == 255).astype(np.float32)

        train_x.append(img_x_array)
        train_y.append(img_y_one_hot)

     train_x = np.array(train_x)
     train_y = np.array(train_y)
     
     os.makedirs(path_output, exist_ok=True)
     np.save(os.path.join(path_output, 'train_x.npy'), train_x)
     np.save(os.path.join(path_output, 'train_y.npy'), train_y)