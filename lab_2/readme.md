1) Пайплайн для инференса данных
  1.1) Filesensor
   Путь к папке для отслеживания новых файлов: `/opt/airflow/data/videos`.
   Создан connection в GUI airflow по пути admins -> connections.
   ![image](https://github.com/user-attachments/assets/46cb0138-5edf-4d6d-b8a4-51698790543a)
  1.2) Extract audio
   Видеозапись длинной 5 минут, для не слишком продолжительного времени выполнения нейронной сети.
   Для извлечения аудиозаписи из видео был использован `ffmpeg`, а  именно образ `jrottenberg/ffmpeg`.
   Прописаны пути к входному видеофайлу и выходному аудиофайлу в формате `wav`.
   Также были выбраны директории для временного монтирования образа.

    `extract_audio = DockerOperator(
    task_id='extract_audio',
    image='jrottenberg/ffmpeg',
    command='-i /data/videos/final.mp4 -vn /data/audios/audio.wav',
    mounts=[Mount(source='/data/videos', target='/data/videos', type='bind'),
            Mount(source='/data/audios', target='/data/audios', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    auto_remove=True,
    dag=dag,)`
   1.3) Transform_audio_to_text
   Для преобразования аудио в текст был написан py скрипт, с использованием библиотеки `transformers`,  модель `openai/whisper-small`.
   Сам py скрипт находится по пути `converting/audiototext/audio_to_text.py`. После того как написал py скрипт, для упаковки его в docker-образ, прописал Dockerfile `converting/audiototext/Dockerfile`
   После этого собрал docker-образ и запушил его в `docker hub` и уже в docker operator использовал образ `vasser232/whisper`.
   Были использованы следующие аргументы:
   `parser = argparse.ArgumentParser(description="Transcribe audio file to text using Whisper.")
parser.add_argument("--input_file", type=str, help="Path to the input audio file.")
parser.add_argument("--output_file", type=str, help="Path to save the output text file.")
parser.add_argument("--max_length", type=int, default=80, help="Maximum line length for wrapped text.")`

  1.4) Summarize_text
  Аналогично предыдущему docker operator, был написан скрипт для получения конспекта `converting/summarizetext/text_to_conspect.py`. В данном скрипте использовал следующие модели. 
  так как модель `facebook/bart-large-cnn` не поддерживает русский язык, была предпринята попытка исправить это путем перевода текста на русском языке на английский язык, выполнение преобразования на английском языке, а затем снова перевод на русский язык. Также для (уточню для чего !!) использовалась модель `facebook/mbart-large-50-many-to-many-mmt`.
  Использованы следующие аргументы:
  `    parser = argparse.ArgumentParser(description='Перевод и суммаризация текста')
    parser.add_argument('--input_file', type=str, required=True, 
                        help='Путь к входному файлу с текстом')
    parser.add_argument('--output_file', type=str, required=True, 
                        help='Путь к выходному файлу с конспектом')
    parser.add_argument('--source_lang', type=str, default='ru_RU', 
                        help='Исходный язык текста')
    parser.add_argument('--target_lang', type=str, default='en_XX', 
                        help='Целевой язык перевода')
    parser.add_argument('--max_length', type=int, default=1000, 
                        help='Максимальная длина сгенерированного резюме')
    parser.add_argument('--min_length', type=int, default=500, 
                        help='Минимальная длина сгенерированного резюме')
    args = parser.parse_args()`
  1.5) Save_to_pdf
  Также был написан скрипт для формирования pdf из txt файла `converting/savetopdf/txt_to_pdf.py`, с использованием библиотеки `reportlab`. Немного изменил задание -> pdf файл состоит не только из конспекта, но еще дополнительно добавил основной текст, для того, чтобы посмотреть насколько хорошо трансформеры выполнили необходимые преобразования.
  Аргументы следующие:
  `    parser = argparse.ArgumentParser(description='Преобразование текстовых файлов в PDF.')
    parser.add_argument('--general_file', type=str, help='Путь к основному текстовому файлу')
    parser.add_argument('--conspect_file', type=str, help='Путь к второстепенному текстовому файлу')
    parser.add_argument('--out_pdf_file', type=str, help='Путь к выходному PDF файлу')`

В итоге был получен pdf файл в котором содержится основной текст, распознанный в аудиофайле, а также конспект по данному тексту `conspect.pdf`.

2) Пайплайн для обучения модели:
Для выполнения этой части лабораторной работы была рассмотрена задача бинарной классификации изображений, а именно нужно было определить есть ли на снимках акт курения.
2.1) Для чтения набора файлов, в данном случае из локальной директории, был написан скрипт `neural_model/read_data/read_data.py`, который выполняет следующие действия:
   - читает исходную папку
   - копирует данные содержащиеся в каталогах == классах
   - разделяет их в соотношении 80/20 <=> train/val
   В итоге получаем готовый каталог к использованию нейросетевой модели.
   Прописаны следующие аргументы:
`    parser = argparse.ArgumentParser(description="Разделение данных на тренировочную и валидационную выборки.")
    parser.add_argument("source_dir", type=str, help="Путь к исходному каталогу с данными.")
    parser.add_argument("dataset_dir", type=str, help="Путь для сохранения разделённого набора данных.")
    parser.add_argument("--val_size", type=float, default=0.2, help="Доля данных для валидации (по умолчанию 0.2).")`
2.2) Для решения выбранной задачи была использована библиотека `timm`, сама модель `convnextv2_tiny.fcmae_ft_in1k`.
     Так как данная модель предобучена на большом количестве классов, то пришлось переписать последнии слои данной модели, для того чтобы она, учитывала только 2 новых класса.
     В связи с тем, что у меня видеокарта `rtx-2060-super`, были выбраны следующие параметры:
     - batch_size = 8
     - learning_rate = 0.001
     - epochs = 10 (так как выполнение самого скрипта в airflow занимает довольно продолжительное время)

     После выполнения скрипта в `/checkpoints` записываются: полученные веса, а также `training_logs.txt` в котором хронятся логи выполнения обучения.

     Аргументы:

     `    parser = argparse.ArgumentParser(description='Training script for image classification')
    
    # Пути к данным
    parser.add_argument('--train-dir', type=str, default='./dataset/train',
                        help='path to training directory')
    parser.add_argument('--val-dir', type=str, default='./dataset/test',
                        help='path to validation directory')
    
    # Параметры обучения
    parser.add_argument('--batch-size', type=int, default=8,
                        help='batch size for training (default: 16)')
    parser.add_argument('--epochs', type=int, default=5,
                        help='number of epochs to train (default: 10)')
    parser.add_argument('--lr', type=float, default=0.001,
                        help='learning rate (default: 0.001)')
    
    # Параметры модели
    parser.add_argument('--model-name', type=str, default='convnextv2_tiny.fcmae_ft_in1k',
                        help='name of the model from timm (default: convnextv2_tiny.fcmae_ft_in1k)')
    parser.add_argument('--num-workers', type=int, default=8,
                        help='number of data loading workers (default: 4)')
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu',
                        help='device to use for training (default: cuda if available, else cpu)')
    parser.add_argument('--output-dir', type=str, default='./checkpoints',
                        help='directory to save model checkpoints (default: ./checkpoints)')`
   

Вывод: были построены пайплайн для преобразования видео в pdf, а также построен пайплайн обучения трансформера для бинарной классификации изображений.

  
    
  
