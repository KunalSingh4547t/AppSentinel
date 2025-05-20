# analysis/dynamic.py
import json
import os

def run_dynamic_analysis(file_path):
    """
    Run dynamic analysis using ZAP, Burp Suite, and device automation (ADB/Xcode).
    Returns a merged list of findings.
    """
    findings = []
    # ZAP
    findings.extend(run_zap_analysis(file_path))
    # Burp Suite
    findings.extend(run_burp_analysis(file_path))
    # Device automation (stub)
    findings.extend(run_device_automation(file_path))
    # Fallback to dummy data if all are empty
    if not findings:
        findings = load_dummy_dynamic_findings()
    return findings

def run_zap_analysis(file_path):
    # TODO: Integrate real ZAP API scan
    return [
        {"name": "Insecure API Call (ZAP)", "severity": "High", "description": "Detected API endpoint without HTTPS."}
    ]

def run_burp_analysis(file_path):
    # TODO: Integrate real Burp Suite scan
    return [
        {"name": "Broken Session Handling (Burp)", "severity": "High", "description": "Session tokens not invalidated on logout."}
    ]

def run_device_automation(file_path):
    # TODO: Use ADB/Xcode CLI to automate app and capture runtime issues
    return [
        {"name": "Permission Abuse (Device)", "severity": "Medium", "description": "Sensitive permission used during runtime."}
    ]

def load_dummy_dynamic_findings():
    sample_path = os.path.join(os.path.dirname(__file__), '../sample_data/dummy_dynamic.json')
    try:
        with open(sample_path, 'r') as f:
            return json.load(f)
    except Exception:
        return []
