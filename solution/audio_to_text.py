#!/usr/bin/env python3
import requests
import sys
import json

API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Чтение входного аудиофайла, который передается как аргумент командной строки
input_file = sys.argv[1]
output_file = sys.argv[2]

# Открываем аудиофайл и отправляем его на обработку в модель Whisper
with open(input_file, "rb") as f:
    audio_data = f.read()

response = requests.post(API_URL, headers=headers, data=audio_data)

# Проверяем, успешно ли выполнен запрос
if response.status_code == 200:
    result = response.json()
    
    # Сохраняем результат в выходной файл
    with open(output_file, 'w') as f:
        json.dump(result, f)
else:
    print("Error:", response.text)
    sys.exit(1)
