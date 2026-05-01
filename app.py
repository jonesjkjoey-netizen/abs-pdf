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

    # =========================
    # COMPANY OVERVIEW
    # =========================
    story.append(Paragraph("Company Overview", styles["Heading2"]))
    story.append(Paragraph(data.get("overview", "Unknown"), styles["Normal"]))
    story.append(Spacer(1, 12))

    # Contact Info
    story.append(Paragraph(data.get("address", "Unknown"), styles["Normal"]))
    story.append(Paragraph(data.get("phone", "Unknown"), styles["Normal"]))
    story.append(Paragraph(data.get("website", "Unknown"), styles["Normal"]))
    story.append(Spacer(1, 16))

    # =========================
    # EXECUTIVE SNAPSHOT
    # =========================
    story.append(Paragraph("Executive Snapshot", styles["Heading2"]))
    executives = data.get("executives", [])

    if executives:
        for e in executives:
            name = e.get("name", "Unknown")
            title = e.get("title", "Unknown")
            story.append(Paragraph(f"{name} — {title}", styles["Normal"]))
    else:
        story.append(Paragraph("No executive data available", styles["Normal"]))

    story.append(Spacer(1, 16))

    # =========================
    # SALES INTELLIGENCE
    # =========================
    story.append(Paragraph("Sales Intelligence", styles["Heading2"]))
    story.append(Paragraph(data.get("sales_intelligence", "Not available"), styles["Normal"]))
    story.append(Spacer(1, 16))

    # =========================
    # TECHNOLOGY INSIGHTS
    # =========================
    story.append(Paragraph("Technology Insights", styles["Heading2"]))
    story.append(Paragraph(data.get("technology_insights", "Not available"), styles["Normal"]))
    story.append(Spacer(1, 16))

    # =========================
    # PRINT ENVIRONMENT
    # =========================
    story.append(Paragraph("Print / Copier Environment", styles["Heading2"]))
    story.append(Paragraph(data.get("print_environment", "Not available"), styles["Normal"]))
    story.append(Spacer(1, 16))

    doc.build(story)

    return file_name


# 🔴 MAIN GENERATE ENDPOINT
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    file_name = generate_pdf(data)

    return {
        "file_url": f"https://abs-pdf.onrender.com/{file_name}"
    }


# 🔴 FILE DOWNLOAD ENDPOINT
@app.route('/<filename>')
def download_file(filename):
    return send_from_directory(os.getcwd(), filename)


if __name__ == "__main__":
    app.run()
