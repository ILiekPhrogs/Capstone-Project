from pathlib import Path
import datetime
import json
from reportlab.lib.pagesizes import LETTER, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak

def _add_metadata(doc, title="Security Scan Report"):
    doc.title = title
    doc.author = "Security Scan Assistant"
    doc.subject = "Automated vulnerability report"

def generate_report(text, parsed_results=None, output_file="report.pdf"):
    
    p = Path(output_file)
    p.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(str(p), pagesize=LETTER,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    _add_metadata(doc)

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    heading = styles["Heading1"]
    small = ParagraphStyle("small", parent=normal, fontSize=9, leading=11)
    mono = ParagraphStyle("mono", parent=normal, fontName="Courier", fontSize=8, leading=10)

    flow = []

    # Header
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    flow.append(Paragraph("Security Scan Report", heading))
    flow.append(Spacer(1, 6))
    flow.append(Paragraph(f"Generated: {ts}", small))
    flow.append(Spacer(1, 12))

    for block in text.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        
        if len(block) < 500:
            flow.append(Paragraph(block.replace("\n", "<br/>"), normal))
        else:
            flow.append(Preformatted(block, mono))
        flow.append(Spacer(1, 8))

    if parsed_results is not None:
        flow.append(PageBreak())
        flow.append(Paragraph("Appendix: Raw Scan Data (JSON)", heading))
        flow.append(Spacer(1, 8))
        json_text = json.dumps(parsed_results, indent=2, ensure_ascii=False)
        flow.append(Preformatted(json_text, mono))

    doc.build(flow)
    return str(p.resolve())


