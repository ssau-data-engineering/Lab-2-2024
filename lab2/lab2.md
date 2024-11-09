# lab2 / Мисюрина И. / 6233-010402D

### inference  

DAG's tasks [lab2_1.py](1/lab2_1.py):
- 1 / wait_for_new_file / FileSensor ожидает поступления файла input.mp4
- 2 / extract_audio / достаем аудио часть из полученного файла ffmpeg-ом
  (скрипт - 1 строка bash прокидывается через command), на выходе mp3
- 3 / transform_audio_to_text  / запрос при помощи requests к модели
  whisper-small ([audio_2_text.py](1/audio_2_text.py)), 
  для тестов использовался небольшой фрагмент +- 30 сек.  
- 4 / summarize_text / запрос к bart_summarisation 
  ([summarization.py](1/summarization.py))
- 5 / save_to_pdf / простой конвертер fpdf-ом ([save_pdf.py](1/save_pdf.py))

[input.mp4](1/input.mp4)>>[audio.mp3](1/audio.mp3)>>
[fulltext.txt](1/fulltext.txt)>>[summary.txt](1/summary.txt)>>
[summary.pdf](1/summary.pdf)


Для шага 2 использовался докер-образ с ffmpeg:  
  ```
  FROM python:3.11-slim-bullseye

  ENV DEBIAN_FRONTEND=noninteractive

  # # #         ffmpeg        # # #
  RUN apt-get -y update; \
      apt-get install -y ffmpeg; \
      rm -rf /var/lib/apt/lists/*;
  ```
Для 3,4,5:  
  ```
  FROM python:3.11-slim-bullseye

  ENV DEBIAN_FRONTEND=noninteractive

  # # #      requests-pdf     # # #
  RUN pip install --upgrade pip; \
      pip install \
      \
      fpdf \
      requests;
  ```

### train  

Обучаем модель для классификации сцен (задача для НИР),
для распознавания есть снимки со спутника 256×256
5ти классов:
beach, buildings, chaparral, forest, river. Количество
train/test/val - 350/50.100.

DAG's tasks [lab2_2.py](2/lab2_2.py):
- 1 / check / датасет уже подготовленный, поэтому
  шаг просто проверяет что в train test val лежат
  одинаковые классы ([check.py](2/check.py))
- 2 / train / создается простая модель (keras.models.Sequential), 
  обучается 20 эпох, итоговые веса сохраняются ([train.py](2/train.py))

Докер-образ:  
  ```
  FROM python:3.11-slim-bullseye

  ENV DEBIAN_FRONTEND=noninteractive

  # # #          cnn          # # #
  RUN pip install --upgrade pip; \
      pip install \
      \
      numpy \
      tensorflow \
      keras;
  ```
Пример инференса [test_for_scene_classification.ipynb](2/test_for_scene_classification.ipynb).
В целом обучилось норм, иногда путает реку с морским побережьем (но там
фото действительно встречаются визуально близкие).  
Лог лосса [loss.txt](2/loss.txt), реализован через коллбэк.