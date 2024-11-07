# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /data

# Копируем все скрипты в контейнер
COPY audio_to_text.py summarize_text.py save_to_pdf.py ./

# Устанавливаем необходимые библиотеки
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    tensorflow \
    scikit-learn \
    fpdf \
    requests

# Определяем команду по умолчанию для контейнера (может меняться в зависимости от задачи)
CMD ["python"]
