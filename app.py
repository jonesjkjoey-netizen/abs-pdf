from flask import Flask, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

def generate_pdf(data):
    file_name = f"{data['company_name'].replace(' ', '')}.pdf"
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("Company Overview", styles["Heading2"]))
    story.append(Paragraph(data["overview"], styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(data["address"], styles["Normal"]))
    story.append(Paragraph(data["phone"], styles["Normal"]))
    story.append(Paragraph(data["website"], styles["Normal"]))
    story.append(Spacer(1, 12))

    for e in data["executives"]:
        story.append(Paragraph(f"{e['name']} — {e['title']}", styles["Normal"]))

    doc.build(story)

    return file_name

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    file_path = generate_pdf(data)
    return send_file(file_path, as_attachment=True)
