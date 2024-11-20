import subprocess
import argparse

parser = argparse.ArgumentParser(description="Convert text file to PDF using pandoc")
parser.add_argument('--input', type=str, default= "summary.txt", required=False, help="Path to the input text file")
parser.add_argument('--output', type=str, default= "pdfka.pdf", required=False, help="Path to the output PDF file")
args = parser.parse_args()

subprocess.run(
    ['pandoc', args.input, '-o', args.output, '--pdf-engine=wkhtmltopdf'],
    check=True,
    capture_output=True,
    text=True
)
print(f"Successfully converted {args.input} to {args.output}")
