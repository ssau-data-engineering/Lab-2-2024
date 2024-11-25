# Лабораторная работа

## Выполнил: Гудков Сергей, группа 6233

---

## Цель работы

- Реализовать пайплайн для обработки видеофайла, извлечения аудио, преобразования аудио в текст и сохранения результата в PDF.
- Обучить нейронную сеть на датасете MNIST для распознавания рукописных цифр.

---

## Задание 1: Пайплайн обработки видео

### Описание DAG и задач

**Файл DAG:**

```python
import os
from datetime import datetime
from airflow import DAG
from docker.types import Mount
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 18),
    'retries': 1,
}

dag = DAG(
    'video_to_audio_to_text',
    default_args=default_args,
    description='Extract audio from video and convert it to text in PDF format',
    schedule_interval=None,
)

current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_input = os.path.join(current_dir, '..', 'data')

wait_for_new_file = FileSensor(
    task_id='wait_for_new_file',
    poke_interval=10,
    filepath=path_to_input,
    fs_conn_id='lab_connect',
    dag=dag,
)

extract_audio = DockerOperator(
    task_id='extract_audio',
    image='dekartvon/ffmpeg-image',
    command='ffmpeg -i /data/input.mp4 -vn /data/audio.wav',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

transform_audio_to_text = DockerOperator(
    task_id='transform_audio_to_text',
    image='dekartvon/requests-image',
    command='python /data/audio_to_text.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

summarize_text = DockerOperator(
    task_id='summarize_text',
    image='dekartvon/requests-image',
    command='python /data/summarize_text.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

save_to_pdf = DockerOperator(
    task_id='save_to_pdf',
    image='dekartvon/fpdf-image',
    command='python /data/save_to_pdf.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

wait_for_new_file >> extract_audio >> transform_audio_to_text >> summarize_text >> save_to_pdf
```

### Описание шагов пайплайна

1. **Ожидание нового файла (`wait_for_new_file`):**

   - Используется `FileSensor` для отслеживания появления нового файла в директории `data`.
   - Параметры:
     - `poke_interval=10`: проверка каждые 10 секунд.
     - `filepath=path_to_input`: путь к директории с входными данными.
     - `fs_conn_id='lab_connect'`: идентификатор подключения, настроенного в Airflow.

2. **Извлечение аудио из видео (`extract_audio`):**

   - Используется `DockerOperator` с образом `dekartvon/ffmpeg-image`.
   - Команда для извлечения аудио:
     ```bash
     ffmpeg -i /data/input.mp4 -vn /data/audio.wav
     ```
   - Монтирование директории `/data` для доступа к файлам.

3. **Преобразование аудио в текст (`transform_audio_to_text`):**

   - Используется `DockerOperator` с образом `dekartvon/requests-image`.
   - Запускается скрипт `audio_to_text.py`, который преобразует аудио в текст с помощью модели `whisper-small`.

4. **Суммаризация текста (`summarize_text`):**

   - Используется тот же Docker-образ `dekartvon/requests-image`.
   - Запускается скрипт `summarize_text.py`, который создает краткое содержание текста.

5. **Сохранение в PDF (`save_to_pdf`):**

   - Используется `DockerOperator` с образом `dekartvon/fpdf-image`.
   - Запускается скрипт `save_to_pdf.py`, который сохраняет текст и его суммаризацию в PDF-файл.

### Итоги работы пайплайна

- **Входной файл:** `input.mp4`.
- **Извлеченное аудио:** `audio.wav`.
- **Преобразованный текст:** `full_text.txt`.
- **Краткое содержание:** `summary.txt`.
- **Итоговый PDF-файл:** `summary.pdf`.

---

## Задание 2: Обучение нейронной сети на MNIST

### Описание DAG и задач

**Файл DAG:**

```python
from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 24),
    'retries': 1,
}

dag = DAG(
    'Data_eng_2.2',
    default_args=default_args,
    description='Training a neural network',
    schedule_interval=None,
)

read_data = DockerOperator(
    task_id='read_data',
    image='dekartvon/ml_container_3',
    command='python /data/read_data.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

train_model = DockerOperator(
    task_id='train_model',
    image='dekartvon/ml_container_3',
    command='python /data/train_model.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

read_data >> train_model
```

### Описание шагов пайплайна

1. **Подготовка данных (`read_data`):**

   - Используется `DockerOperator` с образом `dekartvon/ml_container_3`.
   - Запускается скрипт `read_data.py`, который:
     - Загружает данные из файлов `mnist_train.csv` и `mnist_test.csv`.
     - Ограничивает размер выборок для ускорения обучения.
     - Нормализует данные, деля значения на 255.
     - Кодирует метки классов с помощью `OneHotEncoder`.
     - Сохраняет подготовленные данные в файлы `X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv`.

2. **Обучение модели (`train_model`):**

   - Используется тот же Docker-образ `dekartvon/ml_container_3`.
   - Запускается скрипт `train_model.py`, который:
     - Загружает подготовленные данные.
     - Создает модель нейронной сети с использованием Keras.
     - Компилирует модель с оптимизатором Adam и функцией потерь `categorical_crossentropy`.
     - Обучает модель в течение 10 эпох с размером батча 128.
     - Логирует потери в файл `mnist_loss_log.txt` с помощью коллбэка `LambdaCallback`.
     - Сохраняет обученную модель в файл `new_mnist_trained_model.keras`.

### Скрипт `read_data.py`

```python
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

data_train = pd.read_csv('/data/mnist_train.csv')
data_test = pd.read_csv('/data/mnist_test.csv')

# Ограничиваем размер выборок для ускорения обучения
data_train = data_train[:2000]
data_test = data_test[:400]

# Копируем данные
data_train_copy = data_train.copy()
data_test_copy = data_test.copy()

# Убираем столбец с метками классов
del data_train_copy['label']
del data_test_copy['label']

# Присваиваем новые переменные для данных
X_train = data_train_copy
X_test = data_test_copy

# Нормализация данных
X_train /= 255
X_test /= 255

# Кодируем метки классов с помощью OneHotEncoder
encoding = OneHotEncoder(sparse_output=False, handle_unknown='error')
labels = pd.concat([data_train[['label']], data_test[['label']]])

encoding.fit(labels)
y_train = pd.DataFrame(encoding.transform(data_train[['label']]))
y_test = pd.DataFrame(encoding.transform(data_test[['label']]))

# Сохраняем данные
X_train.to_csv(os.path.join('/data', 'X_train.csv'), index=False)
X_test.to_csv(os.path.join('/data', 'X_test.csv'), index=False)
y_train.to_csv(os.path.join('/data', 'y_train.csv'), index=False)
y_test.to_csv(os.path.join('/data', 'y_test.csv'), index=False)
```

### Скрипт `train_model.py`

```python
from keras.models import Model
from keras.layers import Dense, Dropout, Flatten, Input
from keras.layers import Conv2D, MaxPooling2D, Activation
from keras.optimizers import Adam
from keras.callbacks import LambdaCallback
import pandas as pd
import numpy as np

# Логирование потерь
def log_loss(epoch, logs):
    with open('/data/mnist_loss_log.txt', 'a') as file:
        file.write(f"Epoch {epoch+1}: loss = {logs['loss']}, val_loss = {logs['val_loss']}\n")

loss_logger = LambdaCallback(on_epoch_end=log_loss)

# Создание модели
def create_mnist_model(input_shape):
    inputs = Input(shape=input_shape)

    x = Conv2D(32, kernel_size=(3, 3), padding='same')(inputs)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Conv2D(64, kernel_size=(3, 3), padding='same')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Conv2D(128, kernel_size=(3, 3), padding='same')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Flatten()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    outputs = Dense(10, activation='softmax')(x)

    model = Model(inputs=inputs, outputs=outputs)
    return model

# Загрузка данных
X_train = pd.read_csv('/data/X_train.csv').to_numpy().astype('float32')
X_test = pd.read_csv('/data/X_test.csv').to_numpy().astype('float32')
y_train = pd.read_csv('/data/y_train.csv').to_numpy().astype('float32')
y_test = pd.read_csv('/data/y_test.csv').to_numpy().astype('float32')

# Преобразование входных данных
X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)

# Создание модели
model = create_mnist_model((28, 28, 1))

# Компиляция модели
model.compile(
    optimizer=Adam(learning_rate=1e-3),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Обучение модели
model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=10,
    batch_size=128,
    callbacks=[loss_logger]
)

# Сохранение модели
model.save('/data/new_mnist_trained_model.keras', save_format='tf')
```

### Результаты обучения

- **Логи обучения:** Сохранены в файле `mnist_loss_log.txt`.
- **Обученная модель:** Сохранена в файле `new_mnist_trained_model.keras`.
- **Точность модели:** В ходе обучения модель достигла определенного уровня точности на тестовой выборке (точные цифры можно посмотреть в логах).

---

## Заключение

В ходе лабораторной работы были выполнены следующие задачи:

- Реализован пайплайн для обработки видеофайла с использованием Apache Airflow и Docker:
  - Извлечение аудио из видео.
  - Преобразование аудио в текст.
  - Создание краткого содержания текста.
  - Сохранение результата в PDF-файл.
- Обучена нейронная сеть на датасете MNIST для распознавания рукописных цифр:
  - Подготовлены данные для обучения и тестирования.
  - Создана и обучена модель свёрточной нейронной сети с использованием Keras.
  - Проведено логирование процесса обучения.


## Приложения

### Dockerfile для образа `dekartvon/ffmpeg-image`

```Dockerfile
FROM ubuntu:latest
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg --fix-missing
```

### Dockerfile для образа `dekartvon/requests-image`

```Dockerfile
FROM python:3.11-alpine

RUN pip install requests
```

### Dockerfile для образа `dekartvon/fpdf-image`

```Dockerfile
FROM python:3.11-alpine

RUN pip install fpdf
```

### Dockerfile для образа `dekartvon/ml_container_3`

```Dockerfile
FROM python:3.11

RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install scikit-learn
RUN pip install numpy
RUN pip install keras
RUN pip install pandas
RUN pip install tensorflow
```

---

**Примечание:** Все Docker-образы были загружены в Docker Hub под именем `dekartvon` и доступны для использования в Airflow.
