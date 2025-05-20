# report/generator.py
from datetime import datetime

import base64
from datetime import datetime
from report.charts import generate_severity_pie, generate_severity_bar
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from io import BytesIO
import tempfile
import os

def generate_report(static_results, dynamic_results, app_meta=None, as_pdf=False):
    """
    Generates an HTML or PDF report from the analysis results.
    Includes app metadata, summary, chart images, and plain language descriptions.
    """
    def count_severity(results, sev):
        return sum(1 for v in results if v.get('severity', '').lower() == sev)
    static_results = static_results or []
    dynamic_results = dynamic_results or []
    all_results = static_results + dynamic_results
    total = len(all_results)
    high = count_severity(all_results, 'high')
    medium = count_severity(all_results, 'medium')
    low = count_severity(all_results, 'low')
    # Generate charts
    pie_img = base64.b64encode(generate_severity_pie(all_results)).decode('utf-8')
    bar_img = base64.b64encode(generate_severity_bar(all_results)).decode('utf-8')
    html = f"""
    <html><head><title>Vulnerability Report</title>
    <style>
    body {{ font-family: Arial, sans-serif; margin: 30px; }}
    h1 {{ color: #333; }}
    .meta, .summary {{ background: #f9f9f9; border: 1px solid #eee; padding: 10px; margin-bottom: 15px; }}
    .high {{ color: #c00; }} .medium {{ color: #e67e22; }} .low {{ color: #2980b9; }}
    li {{ margin-bottom: 10px; }}
    .chart-img {{ margin: 20px 0; }}
    </style></head><body>
    <h1>Mobile App Vulnerability Report</h1>
    <div class='meta'>
    <b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
    {f'<b>App Name:</b> {app_meta.get('filename')}<br/><b>Size:</b> {app_meta.get('size')}<br/><b>Type:</b> {app_meta.get('type')}' if app_meta else ''}
    </div>
    <div class='summary'>
    <b>Summary:</b><br/>
    Total Findings: <b>{total}</b> | <span class='high'>High: {high}</span> | <span class='medium'>Medium: {medium}</span> | <span class='low'>Low: {low}</span>
    <div class='chart-img'><b>Severity Distribution (Pie):</b><br><img src='data:image/png;base64,{pie_img}' width='300'/></div>
    <div class='chart-img'><b>Severity Distribution (Bar):</b><br><img src='data:image/png;base64,{bar_img}' width='400'/></div>
    </div>
    <h2>Static Analysis Results</h2>
    <ul>
    """
    if static_results:
        for v in static_results:
            sev = v.get('severity', 'info').lower()
            html += f"<li><b>{v['name']}</b> [<span class='{sev}'>{v['severity']}</span>]<br/>{plain_language(v)}</li>"
    else:
        html += "<li>No static vulnerabilities found.</li>"
    html += "</ul><h2>Dynamic Analysis Results</h2><ul>"
    if dynamic_results:
        for v in dynamic_results:
            sev = v.get('severity', 'info').lower()
            html += f"<li><b>{v['name']}</b> [<span class='{sev}'>{v['severity']}</span>]<br/>{plain_language(v)}</li>"
    else:
        html += "<li>No dynamic vulnerabilities found.</li>"
    html += "</ul></body></html>"
    if not as_pdf:
        return html
    # PDF export using reportlab
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        styleN = styles['BodyText']
        styleN.alignment = TA_LEFT
        styleH = styles['Heading1']
        styleH.alignment = TA_CENTER
        elements = []
        elements.append(Paragraph('Mobile App Vulnerability Report', styleH))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', styleN))
        if app_meta:
            elements.append(Paragraph(f'App Name: {app_meta.get("filename")}', styleN))
            elements.append(Paragraph(f'Size: {app_meta.get("size")}', styleN))
            elements.append(Paragraph(f'Type: {app_meta.get("type")}', styleN))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph('Summary:', styleH))
        elements.append(Paragraph(f'Total Findings: {total} | High: {high} | Medium: {medium} | Low: {low}', styleN))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph('Severity Distribution (Pie):', styleN))
        elements.append(Paragraph(f'<img src="data:image/png;base64,{pie_img}" width="300"/>', styleN))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph('Severity Distribution (Bar):', styleN))
        elements.append(Paragraph(f'<img src="data:image/png;base64,{bar_img}" width="400"/>', styleN))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph('Static Analysis Results:', styleH))
        if static_results:
            for v in static_results:
                sev = v.get('severity', 'info').lower()
                elements.append(Paragraph(f'{v["name"]} [{v["severity"]}]', styleN))
                elements.append(Paragraph(plain_language(v), styleN))
        else:
            elements.append(Paragraph('No static vulnerabilities found.', styleN))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph('Dynamic Analysis Results:', styleH))
        if dynamic_results:
            for v in dynamic_results:
                sev = v.get('severity', 'info').lower()
                elements.append(Paragraph(f'{v["name"]} [{v["severity"]}]', styleN))
                elements.append(Paragraph(plain_language(v), styleN))
        else:
            elements.append(Paragraph('No dynamic vulnerabilities found.', styleN))
        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
    except Exception:
        # If reportlab is not available, fallback to HTML
        return html

def plain_language(vuln):
    """
    Convert a vulnerability finding to a plain-language explanation.
    """
    name = vuln.get('name', '')
    desc = vuln.get('description', '')
    if 'hardcoded' in name.lower():
        return "Sensitive information is embedded directly in the app, which attackers can extract."
    if 'permission' in name.lower():
        return "The app requests or uses permissions that could expose user data or device features."
    if 'cryptography' in name.lower():
        return "Weak or outdated encryption methods make it easier for attackers to access data."
    if 'api call' in name.lower() or 'network' in name.lower():
        return "Data is sent over the network in an insecure way, which could be intercepted."
    if 'session' in name.lower():
        return "Session management is weak, making it easier for attackers to hijack user sessions."
    return desc or "See above."
