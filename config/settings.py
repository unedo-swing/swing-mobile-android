import os

PLATFORM = "android"

APP_STATES = ("force-stop", "clear", "reinstall")
APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")

IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "5"))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "20"))
PDF_EVIDENCE = os.getenv("PDF_EVIDENCE", "1") == "1"
PDF_CLEANUP = os.getenv("PDF_CLEANUP", "uploaded").strip().lower()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
CLICKUP_REPORT = os.getenv("CLICKUP_REPORT", "0") == "1"
