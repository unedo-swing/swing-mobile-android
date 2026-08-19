"""
Global settings for the (Android-only) automation framework.

Values can be overridden with environment variables so the same code runs
locally, on a device farm, or in CI without editing files.

    PDF_EVIDENCE=1 pytest        # force PDF on (same as --pdf flag)
    ALLURE=0 pytest              # skip the Allure results (they are on by default)
    ALLURE_DIR=/tmp/results pytest           # where Allure results are written
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

# Where that PDF ends up:
#   "allure"  -> attached to the Allure case only; no file left in reports/
#                (falls back to a file when the run isn't writing Allure results)
#   "reports" -> a file in reports/ only
#   "both"    -> attached AND kept as a file
PDF_OUTPUT = os.getenv("PDF_OUTPUT", "allure").strip().lower()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")

# Allure raw results (the JSON the Allure CLI renders into an HTML report).
# ON for every run — turn it off with ALLURE=0 or --no-allure.
ALLURE = os.getenv("ALLURE", "1") == "1"
ALLURE_DIR = os.getenv("ALLURE_DIR", os.path.join(REPORTS_DIR, "allure-results"))
# By default each run starts from an empty results directory, so the report
# shows that run. ALLURE_APPEND=1 (or --allure-append) accumulates instead —
# for splitting one logical run across several pytest invocations.
ALLURE_APPEND = os.getenv("ALLURE_APPEND", "0") == "1"
