import requests
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
API_TOKEN = ''
headers = {"Authorization": f"Bearer {API_TOKEN}"}


with open("/data/out/audio.wav", "rb") as f:
    data = f.read()
response = requests.post(API_URL, headers=headers, data=data)
result = response.json()

with open('/data/out/full.txt', 'w+') as f:
    f.write(result['text'])