from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

def generate_pdf(data, filename="startup_plan.pdf"):
    if not data:
        filename = "empty.pdf"
        c = canvas.Canvas(filename)
        c.drawString(100, 700, "No Data Available")
        c.save()
        return filename

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFillColor(HexColor("#38bdf8"))
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "🚀 Startup Report")

    y = height - 100

    for key, value in data.items():
        if not value:
            continue

        # Section Title
        c.setFillColor(HexColor("#0f172a"))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, key.upper())
        y -= 20

        # Content
        c.setFont("Helvetica", 10)
        for line in value.split("\n"):
            if y < 50:
                c.showPage()
                y = height - 50

            c.drawString(60, y, line[:90])
            y -= 14

        y -= 10

    c.save()
    return filename