from fpdf import FPDF
import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)

def main():
    args = parser.parse_args()

    file_path = Path(args.output)

    if not os.path.exists(args.output):
        file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        file_path.touch()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    text = ""
    with open(args.input, "r") as file:
        text = file.read()

    for line in text.split('.'):
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(file_path)

if __name__ == "__main__":
    main()
