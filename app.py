from flask import Flask, request
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
import base64

app = Flask(__name__)


def generate_pdf(data):
    file_name = f"{data['company_name'].replace(' ', '')}.pdf"
    doc = SimpleDocTemplate(file_name, pagesize=letter)
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


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    file_path = generate_pdf(data)

    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return {
        "file_name": file_path,
        "file_data": encoded
    }


if __name__ == "__main__":
    app.run()
