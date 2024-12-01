import requests
import os
import argparse
from io import BytesIO


def query(filename, token):
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
    headers = {"Authorization": f"Bearer {token}"}
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    return response.json()

def save_text(text, output_file):
    with open(output_file, "w") as f:
        f.write(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", type=str, required=True, help="API_TOKEN")
    input_file = "/data/audio.wav"
    output_file = "/data/transcription.txt"
    args = parser.parse_args()
    result = query(input_file, args.token)
    if 'text' in result:
        save_text(result['text'], output_file)
    else:
        print("Error: No text found in the response")
        print(f"Response: {result}")