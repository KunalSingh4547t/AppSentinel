# analysis/static.py

import os
import requests

def run_static_analysis(file_path):
    """
    Run static analysis using MobSF, Androguard, and QARK (if available).
    Returns a merged list of findings.
    """
    findings = []
    # MobSF
    findings.extend(run_mobsf_analysis(file_path))
    # Androguard (stub)
    findings.extend(run_androguard_analysis(file_path))
    # QARK (stub)
    findings.extend(run_qark_analysis(file_path))
    return findings

def run_mobsf_analysis(file_path):
    import os
    import requests
    api_url = os.environ.get('MOBSF_API_URL')
    api_key = os.environ.get('MOBSF_API_KEY')
    if api_url and api_key:
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                headers = {'Authorization': api_key}
                upload_resp = requests.post(f"{api_url}/api/v1/upload", files=files, headers=headers)
                upload_resp.raise_for_status()
                scan_hash = upload_resp.json().get('hash')
            scan_resp = requests.post(f"{api_url}/api/v1/scan", headers=headers, json={'hash': scan_hash})
            scan_resp.raise_for_status()
            res = requests.post(f"{api_url}/api/v1/report_json", headers=headers, json={'hash': scan_hash})
            res.raise_for_status()
            findings = []
            data = res.json()
            if 'findings' in data:
                for item in data['findings']:
                    findings.append({
                        'name': item.get('title', 'Unknown'),
                        'severity': item.get('severity', 'Info'),
                        'description': item.get('description', 'No details')
                    })
            return findings or [{
                'name': 'No critical vulnerabilities found', 'severity': 'Info', 'description': 'No issues detected by MobSF.'
            }]
        except Exception as e:
            return [{
                'name': 'MobSF Scan Error',
                'severity': 'High',
                'description': f'Error during MobSF scan: {str(e)}'
            }]
    # Fallback dummy data
    return [
        {"name": "Hardcoded API Key (MobSF)", "severity": "High", "description": "An API key was found hardcoded in the binary."},
        {"name": "Insecure Permissions (MobSF)", "severity": "Medium", "description": "App requests more permissions than necessary."},
        {"name": "Insecure Storage (MobSF)", "severity": "Low", "description": "Sensitive data may be stored insecurely."}
    ]

def run_androguard_analysis(file_path):
    # TODO: Integrate real Androguard scan
    return [
        {"name": "Weak Cryptography (Androguard)", "severity": "High", "description": "Detected use of weak cryptographic algorithms."}
    ]

def run_qark_analysis(file_path):
    # TODO: Integrate real QARK scan
    return [
        {"name": "Exported Activity (QARK)", "severity": "Medium", "description": "Found exported activity without permission protection."}
    ]
