#!/usr/bin/env python3
import requests
import sys
import json

API_TOKEN = ""
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"  # Модель для резюмирования
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Получение входного текстового файла и имени выходного файла из аргументов командной строки
input_file = sys.argv[1]
output_file = sys.argv[2]

# Чтение текста из входного файла
with open(input_file, 'r') as f:
    text = f.read()

# Отправка запроса на API для создания резюме
payload = {"inputs": text}
response = requests.post(API_URL, headers=headers, json=payload)

# Проверяем, успешно ли выполнен запрос
if response.status_code == 200:
    result = response.json()
    
    # Сохраняем результат в выходной файл
    with open(output_file, 'w') as f:
        for summary in result:
            f.write(summary['summary_text'] + '\n')
else:
    print("Error:", response.text)
    sys.exit(1)
