import argparse
from transformers import (
    pipeline, 
    MBartForConditionalGeneration, 
    MBart50Tokenizer
)
import torch
import textwrap

def main():
    parser = argparse.ArgumentParser(description='Перевод и суммаризация текста')
    parser.add_argument('--input_file', type=str, required=True, 
                        help='Путь к входному файлу с текстом')
    parser.add_argument('--output_file', type=str, required=True, 
                        help='Путь к выходному файлу с конспектом')
    parser.add_argument('--source_lang', type=str, default='ru_RU', 
                        help='Исходный язык текста')
    parser.add_argument('--target_lang', type=str, default='en_XX', 
                        help='Целевой язык перевода')
    parser.add_argument('--max_length', type=int, default=1000, 
                        help='Максимальная длина сгенерированного резюме')
    parser.add_argument('--min_length', type=int, default=500, 
                        help='Минимальная длина сгенерированного резюме')
    args = parser.parse_args()

    model_name = "facebook/mbart-large-50-many-to-many-mmt"
    tokenizer = MBart50Tokenizer.from_pretrained(model_name)
    model = MBartForConditionalGeneration.from_pretrained(model_name)

    def translate_text(text, source_lang, target_lang):
        tokenizer.src_lang = source_lang
        encoded = tokenizer(text, return_tensors="pt")
        generated_tokens = model.generate(
            **encoded, 
            forced_bos_token_id=tokenizer.lang_code_to_id[target_lang]
        )
        return tokenizer.decode(generated_tokens[0], skip_special_tokens=True)

    def summarize_text(text, max_length, min_length):
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        text = text.strip()
        summary = summarizer(
            text, 
            max_length=max_length, 
            min_length=min_length, 
            do_sample=False
        )[0]["summary_text"]
        return summary

    with open(args.input_file, "r", encoding="utf-8") as f:
        text = f.read().strip()

    translated_text = translate_text(text, args.source_lang, args.target_lang)
    summary_english = summarize_text(translated_text, 
                                      max_length=args.max_length, 
                                      min_length=args.min_length)
    summary_russian = translate_text(
        summary_english, 
        "en_XX", 
        args.source_lang
    )

    # Обернуть текст в итоговом файле
    wrapped_summary = textwrap.fill(summary_russian, width=80)

    with open(args.output_file, "w", encoding="utf-8") as f:
        f.write(wrapped_summary)

    print("Конспект сохранен в", args.output_file)
    print("Содержимое конспекта:\n", wrapped_summary)

if __name__ == "__main__":
    main()
