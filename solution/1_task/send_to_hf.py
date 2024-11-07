import requests
import os
from dotenv import load_dotenv, find_dotenv

# Загрузка токена из переменных окружения
load_dotenv(find_dotenv())
API_TOKEN = os.getenv("API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def send_request_to_hf(prompt):
    response = requests.post(API_URL, headers=headers, json={'inputs': prompt})
    if response.status_code == 200:
        result = response.json()
        generated_answer = result[0]['generated_text']
        print(generated_answer)
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")

if __name__ == "__main__":
    with open('/data/output.txt', 'r', encoding='utf-8') as f:
        prompt = f.read()
    send_request_to_hf(prompt)
