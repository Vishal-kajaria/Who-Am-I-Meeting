from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(content, company):

    pdf_file = f"{company.replace(' ', '_')}_meeting_brief.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    story = [
        Paragraph(f"{company} Meeting Brief", styles["Title"]),
        Paragraph(content.replace("\n", "<br/>"), styles["BodyText"])
    ]

    doc.build(story)

    return pdf_file