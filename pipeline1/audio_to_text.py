import requests
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
with open('token.txt', 'r') as token_file:
    API_TOKEN = token_file.read().strip()
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("audio.mp3")

print(f"output {output}")

with open('text_from_audio.txt', 'w+') as f:
    f.write(output['text'])