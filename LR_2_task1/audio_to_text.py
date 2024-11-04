import os
import argparse
from io import BytesIO
import requests
from pydub import AudioSegment

API_TOKEN = "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" 
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(audio_segment):
    audio_bytes = BytesIO()
    audio_segment.export(audio_bytes, format="wav")
    audio_bytes.seek(0)
    response = requests.post(API_URL, headers=headers, data=audio_bytes)
    return response.json()

def split_audio(filename, chunk_length=30000):
    audio = AudioSegment.from_file(filename)
    chunks = []
    for i in range(0, len(audio), chunk_length):
        chunks.append(audio[i:i + chunk_length])
    return chunks

def transcribe_segments(chunks):
    transcriptions = []
    for chunk in chunks:
        transcription = query(chunk)
        transcriptions.append(transcription.get('text', ''))
    return " ".join(transcriptions)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Путь к данным")
    parser.add_argument("--output", type=str, required=True, help="Путь к модели")
    args = parser.parse_args()

    file_directory = os.path.dirname(os.path.abspath(__file__))
    path_input = os.path.join(file_directory, args.input)
    path_output = os.path.join(file_directory, args.output)

    audio_chunks = split_audio(path_input)
    print(audio_chunks)
    transcription = transcribe_segments(audio_chunks)
    print(transcription)
    with open(path_output, 'w', encoding='utf-8') as f:
        f.write(transcription)
