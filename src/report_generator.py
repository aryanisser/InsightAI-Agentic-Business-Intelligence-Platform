from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import textwrap

def generate_ceo_pdf(report_text):
    os.makedirs("outputs/reports", exist_ok=True)

    file_path = "outputs/reports/ceo_business_report.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    y = height - 50

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "InsightAI CEO Business Report")

    y -= 40
    c.setFont("Helvetica", 11)

    lines = report_text.split("\n")

    for line in lines:
        wrapped_lines = textwrap.wrap(line, width=90)

        if not wrapped_lines:
            y -= 15
            continue

        for wrapped_line in wrapped_lines:
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 11)

            c.drawString(50, y, wrapped_line)
            y -= 15

    c.save()
    return file_path