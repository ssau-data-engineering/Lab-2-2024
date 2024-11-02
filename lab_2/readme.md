# ML Пайплайны в Apache Airflow

В данном проекте реализованы два основных пайплайна:
1. Пайплайн преобразования видео в PDF-конспект
2. Пайплайн обучения модели для бинарной классификации изображений

## 1. Пайплайн преобразования видео в PDF

### 1.1 Мониторинг файлов (FileSensor)
- Отслеживание новых файлов в директории `/opt/airflow/data/videos`
- Настроен connection через GUI Airflow в разделе "Admins → Connections"

![Filesensor connection example](lab_2/images/image_1.jpg)

### 1.2 Извлечение аудио
- Используется Docker-образ `jrottenberg/ffmpeg`
- Конвертация видео в аудио формата WAV
- Настроено монтирование директорий:
  ```python
  extract_audio = DockerOperator(
      task_id='extract_audio',
      image='jrottenberg/ffmpeg',
      command='-i /data/videos/final.mp4 -vn /data/audios/audio.wav',
      mounts=[
          Mount(source='/data/videos', target='/data/videos', type='bind'),
          Mount(source='/data/audios', target='/data/audios', type='bind')
      ],
      docker_url="tcp://docker-proxy:2375",
      auto_remove=True,
      dag=dag
  )
  ```

### 1.3 Преобразование аудио в текст
- Использует модель `openai/whisper-small`
- Реализовано в виде Docker-образа `vasser232/whisper`
- Параметры скрипта:
  - `input_file`: путь к входному аудиофайлу
  - `output_file`: путь к выходному текстовому файлу
  - `max_length`: максимальная длина строки
  ```python
  transform_audio_to_text = DockerOperator(
      task_id='transform_audio_to_text',
      image='vasser232/whisper',
      command='--input_file /data/input/audio.wav --output_file /data/output/transcript.txt --max_length 80',
      mounts=[Mount(source='/data/audios', target='/data/input', type='bind'),
              Mount(source='/data/texts', target='/data/output', type='bind')],
      docker_url="tcp://docker-proxy:2375",
      auto_remove=True,
      dag=dag,
  )
  ```

### 1.4 Создание конспекта
- Использует модели:
  - `facebook/bart-large-cnn` для суммаризации
  - `facebook/mbart-large-50-many-to-many-mmt` для перевода
- Реализован двойной перевод для работы с русским языком (RU → EN → RU)
- Основные параметры:
  - Исходный и целевой языки
  - Мин/макс длина конспекта
  - Пути к входным/выходным файлам
  ```python
  summarize_text = DockerOperator(
      task_id='summarize_text',
      image='vasser232/text-summarizer',
      command='--input_file /data/input/transcript.txt --output_file /data/output/summary.txt --max_length 1000 --min_length 500',
      mounts=[Mount(source='/data/texts', target='/data/input', type='bind'),
              Mount(source='/data/texts', target='/data/output', type='bind')],
      docker_url="tcp://docker-proxy:2375",
      auto_remove=True,
      dag=dag,
  )
  ```

### 1.5 Генерация PDF
- Использует библиотеку `reportlab`
- Создает PDF-документ, содержащий:
  - Исходный распознанный текст
  - Сгенерированный конспект
- Параметры:
  - `general_file`: путь к основному тексту
  - `conspect_file`: путь к конспекту
  - `out_pdf_file`: путь к выходному PDF
  ```python
  save_to_pdf = DockerOperator(
      task_id='save_to_pdf',
      image='vasser232/save-to-pdf',
      command=[
          "python", "/data/txt_to_pdf.py", 
          "--general_file", "/data/input/transcript.txt",
          "--conspect_file", "/data/input/summary.txt",
          "--out_pdf_file", "/data/output/result.pdf"
      ],
      mounts=[
          Mount(source='/data/texts', target='/data/input', type='bind'),
          Mount(source='/data/texts', target='/data/output', type='bind')
      ],
      docker_url="tcp://docker-proxy:2375",
      auto_remove=True,
      dag=dag,
  )
  ```

## 2. Пайплайн обучения модели

### 2.1 Подготовка данных
- Задача: бинарная классификация изображений (определение акта курения)
- Скрипт `neural_model/read_data/read_data.py`:
  - Разделение данных на train/val (80/20)
  - Сохранение в структурированном виде
  - Параметры:
    - `source_dir`: исходная директория
    - `dataset_dir`: директория для сохранения
    - `val_size`: размер валидационной выборки
  ```python
  read_data = DockerOperator(
      task_id='read_data',
      image='vasser232/read-data',
      command='/app/input/data /app/output/prepared_data',
      mounts=[
          Mount(source='/data/neural_model', target='/app/input', type='bind'),
          Mount(source='/data/neural_model', target='/app/output', type='bind')
      ],
      auto_remove=True,
      docker_url="tcp://docker-proxy:2375",
      dag=dag,
  )
  ```

### 2.2 Обучение модели
- Используется модель `convnextv2_tiny.fcmae_ft_in1k` из библиотеки `timm`
- Модификация выходного слоя под бинарную классификацию
- Параметры обучения:
  - Batch size: 8
  - Learning rate: 0.001
  - Epochs: 10
- Результаты сохраняются в `/checkpoints`:
  - Веса модели
  - Логи обучения (training_logs.txt)
  ```python
  train_model = DockerOperator(
      task_id='train_model',
      image='vasser232/train-model',
      command=[
          '--train-dir', '/data/input/prepared_data/train',  
          '--val-dir', '/data/input/prepared_data/val',      
          '--output-dir', '/data/output/checkpoints',         
          '--batch-size', '8',
          '--num-workers', '4',
          '--epochs', '10',
      ],
      mounts=[
          Mount(
              source='/data/neural_model',  
              target='/data/input',         
              type='bind'
          ),
          Mount(
              source='/data/neural_model',  
              target='/data/output',        
              type='bind'
          )
      ],
      auto_remove=True,
      docker_url="tcp://docker-proxy:2375",
      dag=dag,
  )
  ```
