import requests
import os
import argparse

def summarize_text(token):
    API_URL = "https://api-inference.huggingface.co/models/slauw87/bart_summarisation"
    headers = {"Authorization": f"Bearer {token}"}
    with open('/data/transcription.txt', "r") as f:
        text = f.read()
    response = requests.post(API_URL, headers=headers, data=text)
    summary = response.json()
    return summary

def save_text(text, output_file):
    with open(output_file, "w") as f:
        f.write(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", type=str, required=True, help="API_TOKEN")
    args = parser.parse_args()

    api_token = args.token
    output_file = '/data/summary.txt'

    result = summarize_text(api_token)[0]

    if 'summary_text' in result:
        save_text(result['summary_text'], output_file)
    else:
        print("Error: No text found in the response")