import json
import sys
import requests

API_KEY = 'API_KEY'

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
headers = {"Authorization": f"Bearer {API_KEY}"}

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "rb") as f:
    audio_data = f.read()

response = requests.post(API_URL, headers=headers, data=audio_data)


if response.status_code == 200:
    result = response.json()


    with open(output_file, 'w') as f:
        json.dump(result, f)
else:
    print("Error:", response.text)
    sys.exit(1)
