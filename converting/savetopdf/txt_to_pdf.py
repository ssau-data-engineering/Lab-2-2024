import argparse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def txt_to_pdf(general_file, conspect_file, pdf_file):
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
    c.setFont('DejaVuSans', 12)

    y = height - 40
    line_height = 14

    c.setFont('DejaVuSans', 14) 
    c.drawString(20, y, "Основной текст")
    y -= line_height + 10 
    c.setFont('DejaVuSans', 12) 

    with open(general_file, 'r', encoding='utf-8') as f:
        for line in f:
            c.drawString(20, y, line.strip())
            y -= line_height

            if y < 40:
                c.showPage()
                c.setFont('DejaVuSans', 12)
                y = height - 40

    c.showPage() 

    c.setFont('DejaVuSans', 14) 
    y = height - 40 
    c.drawString(20, y, "Конспект")
    y -= line_height + 10      
    c.setFont('DejaVuSans', 12)

    with open(conspect_file, 'r', encoding='utf-8') as f:
        for line in f:
            c.drawString(20, y, line.strip())
            y -= line_height

            if y < 40:
                c.showPage()
                c.setFont('DejaVuSans', 12)
                y = height - 40

    c.save()
    print(f"PDF file '{pdf_file}' created successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Преобразование текстовых файлов в PDF.')
    parser.add_argument('--general_file', type=str, help='Путь к основному текстовому файлу')
    parser.add_argument('--conspect_file', type=str, help='Путь к второстепенному текстовому файлу')
    parser.add_argument('--out_pdf_file', type=str, help='Путь к выходному PDF файлу')

    args = parser.parse_args()
    txt_to_pdf(args.general_file, args.conspect_file, args.out_pdf_file)
