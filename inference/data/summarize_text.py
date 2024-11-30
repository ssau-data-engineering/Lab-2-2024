import requests
import sys


API_URL="https://api-inference.huggingface.co/models/slauw87/bart_summarisation"
API_TOKEN="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"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(filename):
    with open(filename) as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query(sys.argv[1])

with open(sys.argv[2], 'w+') as f:
    f.write(output[0]['summary_text'])
