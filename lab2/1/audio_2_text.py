import requests
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
API_TOKEN = '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'
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    print(response.json())
    return response.json()

output = query("/data/audio.mp3")

with open('/data/fulltext.txt', 'w+') as f:
    f.write(output['text'])