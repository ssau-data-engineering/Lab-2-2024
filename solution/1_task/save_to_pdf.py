#!/usr/bin/env python3

from fpdf import FPDF
import sys

# Получение входного текстового файла и имени выходного PDF-файла из аргументов командной строки
input_file = sys.argv[1]
output_file = sys.argv[2]

# Создание PDF-документа
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Установка отступов
pdf.set_left_margin(20)
pdf.set_right_margin(20)

# Чтение текста из входного файла
with open(input_file, 'r') as f:
    text = f.read()

# Добавление текста в PDF с учетом ширины страницы
# Используем multi_cell для автоматического переноса текста
pdf.multi_cell(0, 10, text)

# Сохранение PDF в выходной файл
pdf.output(output_file)
