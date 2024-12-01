import sys
from fpdf import FPDF


pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=15)
f = open(sys.argv[1], "r")
pdf.multi_cell(200, 10, txt=f.read(), align='C')
pdf.output(sys.argv[2])
f.close()