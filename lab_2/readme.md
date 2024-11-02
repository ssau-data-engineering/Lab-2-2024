# ML Пайплайны в Apache Airflow

В этом проекте реализованы два пайплайна для автоматизации процессов инференса и обучения моделей машинного обучения:

1. Пайплайн для преобразования видео в PDF-конспект с текстом и кратким содержанием.
2. Пайплайн для обучения модели, способной определять акт курения на изображениях.

## 1. Пайплайн преобразования видео в PDF

Этот пайплайн выполняет цепочку операций, начиная с мониторинга новых видеофайлов, затем извлекает из них аудио, преобразует аудио в текст, создает конспект текста и, наконец, сохраняет все в PDF-документе. 

### 1.1 Мониторинг новых файлов (FileSensor)
- Для автоматического запуска пайплайна настроен сенсор, который отслеживает появление новых видеофайлов в директории `/opt/airflow/data/videos`.
- Настроен `connection` в интерфейсе Airflow через раздел "Admins → Connections".

![Filesensor connection example](lab_2/images/image_1.jpg)


### 1.2 Извлечение аудио из видео
- Используем Docker-образ `jrottenberg/ffmpeg`, который преобразует видео в аудиофайл формата WAV.
- Настроены монтирования для нужных директорий:
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
- Используется модель `openai/whisper-small` для преобразования аудио в текст, реализованная через Docker-образ `vasser232/whisper`.
- Основные параметры скрипта:
    - `input_file`: путь к входному аудиофайлу.
    - `output_file`: путь к выходному текстовому файлу.
    - `max_length`: максимальная длина строки.
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
   
### 1.4 Создание конспекта текста
- Для получения краткого содержания текста используется модель `facebook/bart-large-cnn`, но так как она не поддерживает русский язык,
текст сначала переводится на английский, суммируется, а затем переводится обратно на русский.
- Модель для перевода — `facebook/mbart-large-50-many-to-many-mmt`.
- Основные параметры:
    - `source_lang` и `target_lang`: исходный и целевой языки.
    - `min_length` и `max_length`: минимальная и максимальная длина конспекта.
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
 
### 1.5 Генерация PDF-документа
- Финальный этап — сохранение текста и конспекта в PDF-документ, используя библиотеку `reportlab`. Немного изменил задание, в PDF-документ добавляются как полный текст,
так и сгенерированный конспект.
- Параметры скрипта:
    - `general_file`: путь к текстовому файлу с полным текстом.
    - `conspect_file`: путь к файлу с конспектом.
    - `out_pdf_file`: путь к итоговому PDF-документу.
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
Второй пайплайн предназначен для обучения нейронной сети, которая классифицирует изображения и определяет, изображен ли на них акт курения.

### 2.1 Подготовка данных
- Данные подготавливаются скриптом `neural_model/read_data/read_data.py`, который разделяет исходные данные на обучающую и валидационную выборки в пропорции 80/20 и
сохраняет их в соответствующей структуре.
- Основные параметры:
    - `source_dir`: исходная директория с данными.
    - `dataset_dir`: директория для сохранения разделенных данных.
    - `val_size`: процент данных для валидации.
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
 
### 2.2 Обучение модели
- Модель `convnextv2_tiny.fcmae_ft_in1k` из библиотеки `timm` используется в качестве основы, и ее выходной слой настроен для бинарной классификации.
- Ключевые гиперпараметры:
    - `Batch size`: 8
    - `Learning rate`: 0.001
    - `Количество эпох`: 10
- Результаты обучения (веса модели и логи) сохраняются в директорию `/checkpoints`.
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
