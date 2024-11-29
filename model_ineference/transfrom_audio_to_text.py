from pathlib import Path
import requests
import argparse
import os
from utils.api_keys_hub import HUG_API_TOKEN

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
headers = {"Authorization": f"Bearer {HUG_API_TOKEN}"}

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()

    response = requests.post(API_URL, headers=headers, data=data)

    return response.json()

def main():
    args = parser.parse_args()
    response = query(args.input)
    file_path = Path(args.output)

    if not os.path.exists(args.output):
        file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w+") as file:
        file.write(response['text'])

if __name__ == "__main__":
    main()