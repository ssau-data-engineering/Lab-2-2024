import argparse
from transformers import pipeline
import textwrap

def parse_args():
    parser = argparse.ArgumentParser(description="Составление конспекта из текста")
    
    parser.add_argument("--input_file", type=str, help="Path to input text file")
    parser.add_argument("--output_file", type=str, help="Path to output text file")
    parser.add_argument("--max_length", type=int, default=150, help="Maximum length of notes")
    parser.add_argument("--min_length", type=int, default=50, help="Minimum length of notes")
    
    return parser.parse_args()

def summarize_text(args):
    
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    with open(args.input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    summary = summarizer(text, max_length=args.max_length, min_length=args.min_length, do_sample=False)
    summary_text = summary[0]['summary_text']
    
    wrapped_text = textwrap.fill(summary_text, width=80)
    
    with open(args.output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(wrapped_text)
    
    print(f"Конспект сохранен в файл: {args.output_file}")

if __name__ == "__main__":
    
    args = parse_args()
    summarize_text(args)    

