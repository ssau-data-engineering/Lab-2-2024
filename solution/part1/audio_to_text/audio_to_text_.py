import whisper
import textwrap
import argparse

parser = argparse.ArgumentParser(description="Transcribe audio to text using Whisper")
parser.add_argument("--audio_file", type=str, help="Path to the audio file")
parser.add_argument("--output_path", type=str, help="Path to save the transcribed text")
parser.add_argument("--width", type=int, default=80, help="Line width for text wrapping (default: 80)")

args = parser.parse_args()

model = whisper.load_model("base")

result = model.transcribe(args.audio_file, language='en')

transcribed_text = result["text"]
wrapped_text = textwrap.fill(transcribed_text, width=args.width)

with open(args.output_path, "w", encoding="utf-8") as f:
    f.write(wrapped_text)