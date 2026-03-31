from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(data, filename="startup_plan.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    y = 750

    for key, value in data.items():
        c.drawString(50, y, key)
        y -= 20
        for line in value.split("\n"):
            c.drawString(60, y, line)
            y -= 15

    c.save()
    return filename