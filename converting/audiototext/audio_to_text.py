from transformers import WhisperProcessor, WhisperForConditionalGeneration, pipeline
import librosa
import textwrap
import argparse

parser = argparse.ArgumentParser(description="Transcribe audio file to text using Whisper.")
parser.add_argument("--input_file", type=str, help="Path to the input audio file.")
parser.add_argument("--output_file", type=str, help="Path to save the output text file.")
parser.add_argument("--max_length", type=int, default=80, help="Maximum line length for wrapped text.")

args = parser.parse_args()

audio, sr = librosa.load(args.input_file, sr=16000)

asr = pipeline("automatic-speech-recognition", model="openai/whisper-small")
result = asr(audio, chunk_length_s=5)
text = result["text"]

wrapper_text = "\n".join(textwrap.wrap(text, args.max_length))

with open(args.output_file, "w", encoding="utf-8") as f:
    f.write(wrapper_text)

print(wrapper_text)
