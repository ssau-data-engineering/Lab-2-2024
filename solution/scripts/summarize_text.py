import json
import sys

import requests


API_KEY = 'API_KEY'

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {API_KEY}"}


input_file = sys.argv[1]
output_file = sys.argv[2]

# Чтение текста из входного файла
with open(input_file, 'r') as file:
    data = json.load(file)

# Извлечение текста
text = data.get('text', '')

payload = {"inputs": text}
response = requests.post(API_URL, headers=headers, json=payload)


if response.status_code == 200:
    result = response.json()


    with open(output_file, 'w') as f:
        for summary in result:
            f.write(summary['summary_text'] + '\n')
else:
    print("Error:", response.text)
    sys.exit(1)