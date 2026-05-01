from flask import Flask, request, send_from_directory
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
import os

app = Flask(__name__)


def generate_pdf(data):
    file_name = f"{data['company_name'].replace(' ', '')}.pdf"
    file_path = os.path.join(os.getcwd(), file_name)

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []

    # Company Overview
    story.append(Paragraph("Company Overview", styles["Heading2"]))
    story.append(Paragraph(data.get("overview", "Unknown"), styles["Normal"]))
    story.append(Spacer(1, 12))

    # Address / Contact
    story.append(Paragraph(data.get("address", "Unknown"), styles["Normal"]))
    story.append(Paragraph(data.get("phone", "Unknown"), styles["Normal"]))
    story.append(Paragraph(data.get("website", "Unknown"), styles["Normal"]))
    story.append(Spacer(1, 12))

    # Executives
    story.append(Paragraph("Executive Snapshot", styles["Heading2"]))
    executives = data.get("executives", [])

    if executives:
        for e in executives:
            name = e.get("name", "Unknown")
            title = e.get("title", "Unknown")
            story.append(Paragraph(f"{name} — {title}", styles["Normal"]))
    else:
        story.append(Paragraph("No executive data available", styles["Normal"]))

    doc.build(story)

    return file_name


# 🔴 MAIN PDF GENERATION ENDPOINT
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    file_name = generate_pdf(data)

    return {
        "file_url": f"https://abs-pdf.onrender.com/{file_name}"
    }


# 🔴 FILE SERVING ENDPOINT (REQUIRED FOR DOWNLOAD)
@app.route('/<filename>')
def download_file(filename):
    return send_from_directory(os.getcwd(), filename)


if __name__ == "__main__":
    app.run()
