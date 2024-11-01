# Лабораторная работа 2
# Читоркин Егор, группа 6233-010402D

## Получение прогноза модели

Пройдемся кратко по основным блокам DAG'а по получению прогноза модели.

1. Ожидание файла
```python
wait_for_new_file = FileSensor(
    task_id='wait_for_new_file',
    poke_interval=10,
    filepath=path_to_input,
    fs_conn_id='lab_connect',
    dag=dag,
)
```
Для создания данного элемента был создано ```Connection``` с id ```lab_connect``` через GUI Airflow. Отслеживается появление файлов в папке ```path_to_input```

2. Извлечение аудио
```py
extract_audio = DockerOperator(
    task_id='extract_audio',
    image='chitorkinegor/ffmpeg-image',
    command='ffmpeg -i /data/input.mp4 -vn /data/audio.wav',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)
```
Здесь был подготовлен образ ```ffmpeg-image``` (см. Dockerfile в соответствующем файле) - ubuntu в установленным ffmpeg. Оказалось, что просто создать образ локально недостаточно, надо его запушить в докерхаб)

3. Перевод аудио в текст
```py
transform_audio_to_text = DockerOperator(
    task_id='transform_audio_to_text',
    image='chitorkinegor/requests-image',
    command='python /data/audio_to_text.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)
```
Изначально я пытался собрать докер-образ с библиотекой ```transformers```, но почему-то при работе в airflow полностью игнорировалась либа ```torchaudio```, поэтому все же реализовал запросом. Здесь всплыл неприятный момент, что изначальный ролик длительностью 2 минуты система не переваривает, поэтому в итоге тестил на аудио около 10 секунд.
Для реализации исполняемого файла собрал новый образ (см. Dockerfile ```requests-image```).

4. Summary
```py
summarize_text = DockerOperator(
    task_id='summarize_text',
    image='chitorkinegor/requests-image',
    command='python /data/summarize_text.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)
```
Здесь аналогично прошлому пункту, только запрос к другой модельке

5. Сохранение в pdf
```py
save_to_pdf = DockerOperator(
    task_id='save_to_pdf',
    image='chitorkinegor/fpdf-image',
    command='python /data/save_to_pdf.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)
```
Здесь аналогично предыдущим пунктам был подготовлен docker-образ с либой ```fpdf``` (см. Dockerfile ```fpdf-image```)

Результаты работы пайплайна:
- считан файл ```input.mp4```
- извлечена звуковая дорожка ```audio.wav```
- звук переведен в текст ```full.txt```
- для текста создано summary ```summary.txt```
- текст сохранен в pdf-файл ```summary.pdf```

## Обучение модели

Здесь я решил обучить одну из моделей своей НИР. Если кратко, то она должна формировать изображение с распределением интенсивности электрического поля по заданному расположению цилиндров. DAG состоит из двух последовательных шагов:

1. Загрузка данных
```py
read_data = DockerOperator(
    task_id='read_data',
    image='chitorkinegor/read-data-image',
    command='python /data/read_data.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)
```
Здесь аналогично прошлому заданию я подготовил docker-образ (там стоит numpy, sklearn) - см. Dockerfile ```read_data_image```. В данном узле происходит чтение датасета и его деление на выборки.

2. Обучение модели
```py
train_model = DockerOperator(
    task_id='train_model',
    image='chitorkinegor/train-model-image',
    command='python /data/train_model.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)
```
Здесь подготовлен docker-образ с установленным keras (Dockerfile ```train_model_image```). Внутри происходит чтение обучающей выборки, обучение модели и ее сохранение в файл ```trained_model.keras```, логи записывались в текстовый файл с помощью колбэков.

Результаты инференса можно увидеть в файле ```test_net.ipynb```