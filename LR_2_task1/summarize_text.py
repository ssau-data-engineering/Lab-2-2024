import os
import argparse
import requests

API_TOKEN = "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" 
API_URL = "https://api-inference.huggingface.co/models/slauw87/bart_summarisation"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(filename):
    with open(filename) as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Путь к данным")
    parser.add_argument("--output", type=str, required=True, help="Путь к модели")
    args = parser.parse_args()

    file_directory = os.path.dirname(os.path.abspath(__file__))
    path_input = os.path.join(file_directory, args.input)
    path_output = os.path.join(file_directory, args.output)

    output = query(path_input)

    with open(path_output, 'w') as f:
        f.write(output[0]['summary_text'])