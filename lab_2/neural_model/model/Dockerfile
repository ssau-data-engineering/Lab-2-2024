FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создание рабочей директории
WORKDIR /data

# Копирование скрипта обучения
COPY model.py .

# Создание директорий для данных и выходных файлов
RUN mkdir -p /data/input /data/output

# Точка входа
ENTRYPOINT ["python", "model.py"]