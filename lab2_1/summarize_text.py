import requests
API_URL = "https://api-inference.huggingface.co/models/slauw87/bart_summarisation"
API_TOKEN = ''
headers = {"Authorization": f"Bearer {API_TOKEN}"}


with open("/data/out/full.txt") as f:
    data = f.read()
response = requests.post(API_URL, headers=headers, data=data)
result = response.json()

with open('/data/out/summary.txt', 'w+') as f:
    f.write(result[0]['summary_text'])