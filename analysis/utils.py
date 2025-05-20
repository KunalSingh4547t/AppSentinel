# analysis/utils.py
import subprocess

def run_adb_command(args):
    """
    Run an adb command and return output.
    """
    try:
        result = subprocess.run(["adb"] + args, capture_output=True, text=True, timeout=30)
        return result.stdout
    except Exception as e:
        return str(e)

def run_xcode_command(args):
    """
    Run an xcodebuild/simctl command and return output.
    """
    try:
        result = subprocess.run(["xcrun"] + args, capture_output=True, text=True, timeout=30)
        return result.stdout
    except Exception as e:
        return str(e)
