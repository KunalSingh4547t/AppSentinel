# Mobile App Security Assessment Tool

A comprehensive security assessment tool for mobile applications, providing a robust framework for identifying vulnerabilities and ensuring the security of mobile apps.

## Overview

This project aims to provide a user-friendly and efficient solution for mobile app security assessment, incorporating both static and dynamic analysis techniques. The tool is designed to be highly customizable and extensible, allowing users to easily integrate their own analysis tools and techniques.

## Features

* **Static Analysis**: Perform in-depth static analysis of mobile app code using MobSF
* **Dynamic Analysis**: Simulate dynamic analysis using sample data (future integration with ZAP/Burp Suite API planned)
* **Results Visualization**: View detailed results and severity breakdown in the GUI
* **HTML Reporting**: Generate downloadable HTML reports with app metadata, summary, and severity breakdown
* **Error Handling**: Robust error handling and helpful instructions for users

## Directory Structure

```
Mobile-App-Security-Assessment-Tool/
├── main.py
├── requirements.txt
├── sample_data/
│   └── dummy_dynamic.json
├── tmp/
├── .env
└── README.md
```

## Setup

1. **Install Requirements**: Run `pip install -r requirements.txt` to install dependencies
2. **Run the App**: Execute `streamlit run main.py` to start the application

## MobSF Integration (Optional)

To enable real static analysis using MobSF:

1. Run MobSF in API mode (see [MobSF Docs](https://github.com/MobSF/Mobile-Security-Framework-MobSF))
2. Set environment variables:
   ```bash
   MOBSF_API_URL=http://localhost:8000
   MOBSF_API_KEY=your_mobsf_api_key
   ```
   Use [python-dotenv](https://pypi.org/project/python-dotenv/) or export variables in your shell

## Usage

1. **Upload App**: Upload an APK or IPA file
2. **Start Scan**: Click 'Start Static Scan' or 'Start Dynamic Scan' (simulated)
3. **View Results**: View detailed results and download the HTML report

## Dependencies

* Python 3.7+
* See `requirements.txt` for dependencies, including `streamlit`, `requests`, `python-dotenv`, and `PyPDF2`

## Credits

This project was developed by Kunal Singh. For questions, feature requests, or to contribute to the project, please open an issue or contact the maintainer.
