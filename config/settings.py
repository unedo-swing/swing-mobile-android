"""
Global settings for the (Android-only) automation framework.

Values can be overridden with environment variables so the same code runs
locally, on a device farm, or in CI without editing files.

    PDF_EVIDENCE=1 pytest        # force PDF on (same as --pdf flag)
"""
import os

# Fixed platform for this framework.
PLATFORM = "android"

# ---------------------------------------------------------------------------
# Appium server
# ---------------------------------------------------------------------------
APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")

# ---------------------------------------------------------------------------
# Default waits (seconds)
# ---------------------------------------------------------------------------
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "5"))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "20"))

# ---------------------------------------------------------------------------
# Evidence / reporting
# ---------------------------------------------------------------------------
# PDF evidence is ON by default — every test writes a PDF to reports/.
# Turn it off with PDF_EVIDENCE=0. The pytest `--pdf` flag also forces it on.
PDF_EVIDENCE = os.getenv("PDF_EVIDENCE", "1") == "1"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
