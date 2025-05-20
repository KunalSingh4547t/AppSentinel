# report/charts.py
import matplotlib.pyplot as plt
import io


def generate_severity_pie(findings):
    labels = ['High', 'Medium', 'Low', 'Info']
    counts = [
        sum(1 for v in findings if v.get('severity', '').lower() == 'high'),
        sum(1 for v in findings if v.get('severity', '').lower() == 'medium'),
        sum(1 for v in findings if v.get('severity', '').lower() == 'low'),
        sum(1 for v in findings if v.get('severity', '').lower() not in ['high', 'medium', 'low'])
    ]
    fig, ax = plt.subplots()
    ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#c00', '#e67e22', '#2980b9', '#bbb'])
    ax.axis('equal')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def generate_severity_bar(findings):
    labels = ['High', 'Medium', 'Low', 'Info']
    counts = [
        sum(1 for v in findings if v.get('severity', '').lower() == 'high'),
        sum(1 for v in findings if v.get('severity', '').lower() == 'medium'),
        sum(1 for v in findings if v.get('severity', '').lower() == 'low'),
        sum(1 for v in findings if v.get('severity', '').lower() not in ['high', 'medium', 'low'])
    ]
    fig, ax = plt.subplots()
    ax.bar(labels, counts, color=['#c00', '#e67e22', '#2980b9', '#bbb'])
    ax.set_ylabel('Number of Findings')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf.read()
