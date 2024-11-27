from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=14)
with open('/data/out/summary.txt') as f:
    pdf.multi_cell(0, 10, txt=f.read(), align="C")
pdf.output("/data/out/summary.pdf")