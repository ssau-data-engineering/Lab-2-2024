from fpdf import FPDF

def txt_to_pdf(txt_file, pdf_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    with open(txt_file, "r", encoding="utf-8") as file:
        text = file.read()
    pdf.multi_cell(0, 10, txt=text)
    pdf.output(pdf_file)

txt_file = "/data/summary.txt"
pdf_file = "/data/output.pdf"
txt_to_pdf(txt_file, pdf_file)