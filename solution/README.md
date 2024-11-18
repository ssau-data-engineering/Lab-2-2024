# Engineering

## Ионов Артем группа 6231-010402D

Весь необходимый минимум для выполнения лабораторных работ был выполнен перед 1 лабораторной работой.

![image](https://github.com/user-attachments/assets/41eaed57-c69b-4a4a-aa2f-3ba4910b417f)

### Лабораторная работа №2 "Инференс и обучение НС"

## Часть 1 "Автоматическое распознавание речи"

В рамках данного задания предлагается построить пайплайн, который реализует систему "Автоматического распознавания речи" для видеофайлов.

Построенный пайплайн будет выполнять следующие действия поочередно:

1. Производить мониторинг целевой папки на предмет появления новых видеофайлов.
2. Извлекать аудиодорожку из исходного видеофайла.
3. Преобразовывать аудиодорожку в текст с помощью нейросетевой модели.
4. Формировать конспект на основе полученного текста.
5. Формировать выходной .pdf файл с конспектом.

Для начала нужно создать новое подключение в airflow. 

![image](https://github.com/user-attachments/assets/b855c085-be0a-48c2-ac47-e21dad3194ca)

Для 3 и 4 этапа у нас будут использоваться модельки с Hugging Face, поэтому нужно от туда взять API. Я ранее им пользовался, поэтому у меня API была под рукой так сказать.
Для 5 этапа можно использовать библиотеку fpdf. В докер файле нужно прописать установку данной библиотеки тоже, а так же для 
- Scikit-learn
- Numpy
- Pandas

Первой же бедой было, что
- Я по своей тупости я создал докер файл, который уже и так был создан и я долго не понимал почему у меня не видит импорт библиотек ._.

Содержимое моего докер файла

```
FROM python:3.10-slim

WORKDIR /data

COPY audio_to_text.py summarize_text.py save_to_pdf.py ./

RUN pip install --no-cache-dir \
    pandas \
    numpy \
    tensorflow \
    scikit-learn \
    fpdf2 \
    requests
```
Тут заметите, что появился fpdf2, оказалось, что докер файл все таки видело, и fpdf загружался, ошибка на ровном месте, стоило установить fpdf2 (та же самая библиотека) как ошибка пропала. 
Теперь произведем сборку, тегнем и запушим, с помощью ряда команд:

```
docker build . tf_container2
```

```
docker tag –t tf_container2 sat4h/tf_container2
```

```
docker push sat4h/tf_container2
```

С помощью можно посмотреть образ докера.
```
docker images
```

![image](https://github.com/user-attachments/assets/702a5844-33c1-4093-a6d0-e870d30d0be9)

[DAG](dag_1.py) был загружен в папке airflow/dags. И мы можем видеть его в airflow через некоторое время.

Я взял [одну из популярных фраз Таноса на англ. языке](input_video.mp4). Запускаем наш DAG и в конце получаем коспект по тексту в формате pdf.

![image](https://github.com/user-attachments/assets/378feaca-34e6-4c2b-aa6f-1ac763ee0ec9)

А вот и результат:

![image](https://github.com/user-attachments/assets/91514676-d37a-46e6-9186-920ec48f8da6)

## Часть 2 "Обучение нейросети"

DAG для 2 части находится [здесь](dag_2.py). И два .py файла [load_and_preprocess_data.py](load_and_preprocess_data.py) с предобработкой ![image](https://github.com/user-attachments/assets/2c166720-e9d2-4464-920c-dce7163f67d6)
 и файл [load_data_train_model.py](load_data_train_model.py) с обучением.

В качестве датасета я взял [Iris Dataset](https://gist.github.com/netj/8836201).

Все прошло успешно, предобработанный данные сохранились в /data/lr2/opr, а обученная модель и логи сохранились в папке /data/logs

![image](https://github.com/user-attachments/assets/b62b744a-a266-4117-9b2a-f83b967b14e2)

![image](https://github.com/user-attachments/assets/4b784ec8-ad06-42e6-8ff8-3c60e1599234)

Логи

![image](https://github.com/user-attachments/assets/bfd9f336-3c53-4c1e-b940-f70722167d9f)

[Файл ipynb](model.ipynb) с загрузкой обученной модели.
