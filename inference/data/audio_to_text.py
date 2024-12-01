import os
import sys
import requests

from dotenv import load_dotenv

load_dotenv()

API_URL="https://api-inference.huggingface.co/models/openai/whisper-small"
API_TOKEN=os.getenv("API_TOKEN")

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(filename):
   with open(filename, "rb") as f:
       data = f.read()
   response = requests.post(API_URL, headers=headers, data=data)
   return response.json()

output = query(sys.argv[1])

with open(sys.argv[2], 'w+') as f:
    f.write(output['text'])
