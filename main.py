import streamlit as st
from analysis.static import run_static_analysis
from analysis.dynamic import run_dynamic_analysis
from report.generator import generate_report
import json
import os
import shutil

st.set_page_config(page_title="Mobile App Security Assessment Tool", layout="wide")

# --- Hidden backend stop mechanism ---
STOP_FLAG = ".stop_app"
if os.path.exists(STOP_FLAG):
    if os.path.exists("tmp"):
        shutil.rmtree("tmp", ignore_errors=True)
    os.remove(STOP_FLAG)
    st.stop()
# --------------------------------------

st.title("📱 AppSentinel: Mobile Security Scanner")
st.markdown(
    f"""
    <div style='padding:10px;background:linear-gradient(90deg,#2980b9,#6dd5fa);border-radius:8px;color:white;font-size:1.1em;'>
    <b>Welcome to AppSentinel: Mobile Security Scanner!</b><br>
    This tool allows you to upload an Android or iOS app, run static and dynamic scans, and download a detailed PDF report.<br>
    <b>How to use:</b><br>
    1. Upload an APK or IPA file.<br>
    2. Run static and dynamic scans to identify potential vulnerabilities.<br>
    3. Download the PDF report for a detailed analysis of the app's security.<br>
    </div>
    """,
    unsafe_allow_html=True
)

# State
if 'static_results' not in st.session_state:
    st.session_state['static_results'] = None
if 'dynamic_results' not in st.session_state:
    st.session_state['dynamic_results'] = None
if 'report' not in st.session_state:
    st.session_state['report'] = None
if 'report_pdf' not in st.session_state:
    st.session_state['report_pdf'] = None
if 'app_meta' not in st.session_state:
    st.session_state['app_meta'] = None

with st.container():
    uploaded_file = st.file_uploader("Upload APK or IPA file", type=["apk", "ipa"])
    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        if file_ext not in [".apk", ".ipa"]:
            st.error("Invalid file type. Please upload an APK or IPA file.")
        else:
            file_path = os.path.join("tmp", uploaded_file.name)
            os.makedirs("tmp", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state['app_meta'] = {
                'filename': uploaded_file.name,
                'size': f"{uploaded_file.size / 1024:.2f} KB",
                'type': "APK" if file_ext == ".apk" else "IPA"
            }

    # Static scan section
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='padding:20px 18px 16px 18px;background:#e3f2fd;border-radius:12px;margin-bottom:18px;border:2px solid #49a09d;box-shadow:0 2px 8px #49a09d22;'>
            <b style='font-size:1.15em;color:#000;'>🛡️ Static Analysis</b><br>
            <span style='font-size:1.01em;color:#000;'>Examines your app <i>without running it</i> for code-level issues such as hardcoded secrets, weak crypto, exported components, and more.</span><br>
            <span style='font-size:0.97em;color:#000;'>Tools: MobSF, Androguard, QARK</span>
        </div>
        """, unsafe_allow_html=True)
        static_scan = st.button("🔍 Start Static Scan", disabled=not uploaded_file, use_container_width=True)
    if uploaded_file and static_scan:
        with st.spinner("Running static analysis..."):
            try:
                st.session_state['static_results'] = run_static_analysis(file_path)
                st.success("Static analysis completed.")
            except Exception as e:
                st.error(f"Static analysis failed: {e}")
    with col2:
        st.markdown("""
        <div style='padding:20px 18px 16px 18px;background:#ffebee;border-radius:12px;margin-bottom:18px;border:2px solid #d81b60;box-shadow:0 2px 8px #d81b6022;'>
            <b style='font-size:1.15em;color:#000;'>🚦 Dynamic Analysis</b><br>
            <span style='font-size:1.01em;color:#000;'>Simulates app execution to find runtime issues such as insecure API calls, permission abuse, and more.</span><br>
            <span style='font-size:0.97em;color:#000;'>Tools: ZAP, Burp Suite, Device Automation</span>
        </div>
        """, unsafe_allow_html=True)
        dynamic_scan = st.button("⚡ Start Dynamic Scan", disabled=not uploaded_file, use_container_width=True)
    if uploaded_file and dynamic_scan:
        with st.spinner("Running dynamic analysis..."):
            try:
                st.session_state['dynamic_results'] = run_dynamic_analysis(file_path)
                st.success("Dynamic analysis completed.")
            except Exception as e:
                st.error(f"Dynamic analysis failed: {e}")

# Display app metadata
if st.session_state.get('app_meta'):
    st.info(f"**App Info:** Name: {st.session_state['app_meta']['filename']} | Size: {st.session_state['app_meta']['size']} | Type: {st.session_state['app_meta']['type']}")

# Display results
with st.container():
    if st.session_state['static_results']:
        st.subheader("🛡️ Static Analysis Results")
        if len(st.session_state['static_results']) == 0:
            st.success("No static vulnerabilities found!")
        else:
            for vuln in st.session_state['static_results']:
                st.markdown(f"**{vuln['name']}** | Severity: {vuln['severity']}\n- {vuln['description']}")
    if st.session_state['dynamic_results']:
        st.subheader("🚦 Dynamic Analysis Results")
        if len(st.session_state['dynamic_results']) == 0:
            st.success("No dynamic vulnerabilities found!")
        else:
            for vuln in st.session_state['dynamic_results']:
                st.markdown(f"**{vuln['name']}** | Severity: {vuln['severity']}\n- {vuln['description']}")

# Generate and download PDF report
if (st.session_state['static_results'] or st.session_state['dynamic_results']):
    if st.button("📝 Generate & Download PDF Report", type="primary"):
        with st.spinner("Generating PDF report..."):
            pdf_bytes = generate_report(
                st.session_state['static_results'],
                st.session_state['dynamic_results'],
                st.session_state.get('app_meta'),
                as_pdf=True
            )
            st.session_state['report_pdf'] = pdf_bytes
            st.success("PDF report generated!")

    if st.session_state['report_pdf']:
        st.download_button(
            label="⬇️ Download PDF Report",
            data=st.session_state['report_pdf'],
            file_name="vulnerability_report.pdf",
            mime="application/pdf"
        )

# Footer
st.markdown("""
    <div style='padding:10px;background:linear-gradient(90deg,#2980b9,#6dd5fa);border-radius:8px;color:white;font-size:1.1em;'>
    <b>AppSentinel: Mobile Security Scanner</b><br>
    Developed by Kunal<br>
    This tool is designed to help developers identify potential security vulnerabilities in their mobile apps.
    </div>
    """,
    unsafe_allow_html=True
)

# Cleanup temp files after session ends
if os.path.exists("tmp") and not uploaded_file:
    shutil.rmtree("tmp", ignore_errors=True)
