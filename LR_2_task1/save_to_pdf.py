import os
import argparse
from fpdf import FPDF


if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Путь к данным")
    parser.add_argument("--output", type=str, required=True, help="Путь к модели")
    args = parser.parse_args()

    file_directory = os.path.dirname(os.path.abspath(__file__))
    path_input = os.path.join(file_directory, args.input)
    path_output = os.path.join(file_directory, args.output)


    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=14)

    with open(path_input, 'r', encoding='utf-8') as file:
        data = file.read()
        pdf.multi_cell(0, 15, txt=data, align="C")
    pdf.output(path_output)