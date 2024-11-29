from fpdf import FPDF
import sys


input_file = sys.argv[1]
output_file = sys.argv[2]

# Создание PDF-документа
pdf = FPDF()
pdf.add_page()
pdf.add_font("ArialUnicode", fname="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
pdf.set_font("ArialUnicode", size=12)

pdf.set_left_margin(20)
pdf.set_right_margin(20)

# Чтение текста из входного файла
with open(input_file, 'r') as f:
    text = f.read()


pdf.multi_cell(0, 10, text)

# Сохранение PDF в выходной файл
pdf.output(output_file)