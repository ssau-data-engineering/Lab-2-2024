import requests
API_URL = "https://api-inference.huggingface.co/models/slauw87/bart_summarisation"
API_TOKEN = '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'
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(filename):
    with open(filename) as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("/data/full.txt")

with open('/data/summary.txt', 'w+') as f:
    f.write(output[0]['summary_text'])