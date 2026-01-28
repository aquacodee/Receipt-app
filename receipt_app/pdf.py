from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_receipt_pdf(receipt, file_path, watermark=False):
    c = canvas.Canvas(file_path, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, receipt.business.name)

    c.setFont("Helvetica", 10)
    c.drawString(50, 780, f"Receipt: {receipt.receipt_number}")
    c.drawString(50, 760, f"Date: {receipt.created_at.strftime('%Y-%m-%d')}")

    y = 720
    for item in receipt.items.all():
        c.drawString(50, y, f"{item.item_name} x{item.quantity}")
        c.drawString(400, y, f"GHS {item.total_price}")
        y -= 20

    c.drawString(50, y-20, f"Total: GHS {receipt.total}")

    if watermark:
        c.setFont("Helvetica-Bold", 40)
        c.setFillGray(0.9)
        c.drawCentredString(300, 400, "Powered by Aqua Receipts")

    c.save()
