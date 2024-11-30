import sys
from fpdf import FPDF


pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=15)
with open(sys.argv[1], "r") as f:
    pdf.multi_cell(200, 10, txt=f.read(), align='C')
pdf.output(sys.argv[2])