import requests
API_URL = "https://api-inference.huggingface.co/models/slauw87/bart_summarisation"
with open('token.txt', 'r') as token_file:
    API_TOKEN = token_file.read().strip()
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(filename):
    with open(filename) as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("text_from_audio.txt")

with open('summary_text.txt', 'w+') as f:
    f.write(output[0]['summary_text'])