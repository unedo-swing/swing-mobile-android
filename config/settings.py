"""
Global settings for the (Android-only) automation framework.

Values can be overridden with environment variables so the same code runs
locally, on a device farm, or in CI without editing files.

    PDF_EVIDENCE=1 pytest        # force PDF on (same as --pdf flag)
    PDF_CLEANUP=never pytest     # keep the evidence PDFs in reports/ after the run
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
# PDF evidence is ON by default — every test builds one.
# Turn it off with PDF_EVIDENCE=0. The pytest `--pdf` flag also forces it on.
PDF_EVIDENCE = os.getenv("PDF_EVIDENCE", "1") == "1"

# Every PDF is written to reports/. What happens to the file after the run:
#   "uploaded" -> deleted once it has reached the ClickUp task that hosts the
#                 evidence; a file that was not uploaded (ClickUp off, upload
#                 failed, over the size cap) is kept, so evidence is never lost
#   "never"    -> always kept in reports/
#   "always"   -> deleted at the end of the run either way
PDF_CLEANUP = os.getenv("PDF_CLEANUP", "uploaded").strip().lower()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")

# ---------------------------------------------------------------------------
# ClickUp Chat reporting
# ---------------------------------------------------------------------------
# One message per run in a ClickUp channel — OFF by default, so a local
# debugging run never posts. Turn it on per run with --clickup, or for a whole
# environment (CI) with CLICKUP_REPORT=1. The token and ids it needs
# (CLICKUP_TOKEN / CLICKUP_WORKSPACE_ID / CLICKUP_CHANNEL_ID) are read at send
# time in utils/clickup_reporter.py — see .env.example.
CLICKUP_REPORT = os.getenv("CLICKUP_REPORT", "0") == "1"
