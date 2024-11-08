from fpdf import FPDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
with open('/data/summary.txt') as f:
    pdf.multi_cell(0, 10, txt=f.read(), align="C")
pdf.output("/data/summary.pdf")