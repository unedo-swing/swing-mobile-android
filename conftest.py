"""
Pytest fixtures shared by all tests.

PDF evidence is ON by default: every test writes a PDF to reports/ (disable with
PDF_EVIDENCE=0). See utils/pdf_reporter.py.

After the whole run, a regression summary is printed (and written to
reports/regression_summary.txt) listing each FAILED test with its last step and
last screenshot — see pytest_terminal_summary() below.

Environment variables are loaded from a local .env (if present) via python-dotenv
before anything reads os.getenv — see load_dotenv() below.
"""
import os
from dotenv import load_dotenv

# override=True so this project's .env wins over any stale exported vars leaked
# from a sibling project (e.g. Swing_Mobile's APP path). Must run before config/
# data modules read os.getenv.
load_dotenv(override=True)

import pytest
import re

from config import settings
import config as config_module
from core.driver_factory import create_driver
from data.driving_range_data import DrivingRangeData
from data.events_data import EventsData
from flows.login_flow import LoginFlow
from flows.tee_time_flow import TeeTimeFlow
from flows.driving_range_flow import DrivingRangeFlow
from flows.logout_flow import LogoutFlow
from flows.events_flow import EventsFlow
from utils.pdf_reporter import init_pdf, generate_pdf
from utils.excel_reader import find_rows
from data.driving_range_data import _DATA_PATH as _DR_PATH, _SHEET as _DR_SHEET


def pytest_addoption(parser):
    parser.addoption(
        "--pdf",
        action="store_true",
        default=False,
        help="Enable PDF evidence (init_pdf() will return a reporter).",
    )


def pytest_configure(config):
    """Let the --pdf flag turn on PDF evidence for init_pdf()."""
    if config.getoption("--pdf"):
        settings.PDF_EVIDENCE = True
    # collects one entry per failed test for the end-of-run regression summary
    config._regression_failures = []


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Expose each phase's result on the item so fixtures can read pass/fail."""
    rep = yield
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def TC_ID(request):
    """Load DrivingRangeData (D) for the parametrized TC_ID, so tests can use
    D.REGION, D.DRIVING_RANGE_NAME, ... for that test case. Drive it from a test:

        @pytest.mark.parametrize("TC_ID", ["TC_DR_00002"], indirect=True)
    """
    tc_id = request.param
    if find_rows(_DR_PATH, "TC_ID", tc_id, sheet=_DR_SHEET):
        DrivingRangeData.load(tc_id)   # TC is in the Driving_Range sheet
    EventsData.load(tc_id)             # TC is in the Events sheet (or empty)
    return tc_id


@pytest.fixture
def driver():
    """A fresh Appium Android driver per test, quit automatically at the end.

    Force-stops the app first so each test reopens fresh at Home (no reinstall)
    — i.e. "reopen with force close" between tests.
    """
    import os
    import subprocess

    pkg = os.getenv("APP_PACKAGE", "app.getswing.dev")
    device = os.getenv("DEVICE_NAME", "emulator-5554")
    subprocess.run(["adb", "-s", device, "shell", "am", "force-stop", pkg], check=False)

    drv = create_driver()
    yield drv
    drv.quit()


@pytest.fixture
def reporter(request):
    """One PDF reporter per test (per PDF_EVIDENCE, on by default). Written at the
    end with a PASS/FAIL status. Shared by all flow fixtures below. On failure it
    also records the last step + screenshot for the regression summary."""
    pdf = init_pdf(request.node.name)
    yield pdf
    rep_setup = getattr(request.node, "rep_setup", None)
    rep_call = getattr(request.node, "rep_call", None)
    failed_rep = next(
        (r for r in (rep_setup, rep_call) if r is not None and r.failed), None
    )
    pdf_path = generate_pdf(pdf, status="FAIL" if failed_rep is not None else "PASS")
    if failed_rep is not None:
        _record_failure(request, pdf, failed_rep, pdf_path)
    # screenshots are embedded in the PDF now -> clear the folder once it's built
    if pdf_path:
        _empty_screenshots_dir()


def _record_failure(request, pdf, rep, pdf_path):
    """Stash a failed test's last step + screenshot for pytest_terminal_summary.

    The screenshot file itself is deleted after the PDF is built, so we keep its
    name (it's the last image in the PDF) and point to the PDF as the evidence.
    """
    last = pdf.steps[-1] if (pdf is not None and pdf.steps) else None
    shot = last["screenshot"] if last else None
    message = ""
    if rep.longrepr is not None:
        crash = getattr(rep.longrepr, "reprcrash", None)
        message = (crash.message if crash is not None else str(rep.longrepr)) or ""
    request.config._regression_failures.append({
        "test": request.node.nodeid,
        "phase": rep.when,  # "setup" or "call"
        "last_step": last["title"] if last else "(no steps captured)",
        "last_description": last["description"] if last else "",
        "last_screenshot": os.path.basename(shot) if shot else None,
        "pdf": pdf_path,
        "error": message.strip().splitlines()[0] if message.strip() else "",
    })


def _empty_screenshots_dir():
    """Delete every screenshot file in reports/screenshots (they now live in the
    PDFs). Leaves the folder itself in place."""
    folder = settings.SCREENSHOTS_DIR
    if not os.path.isdir(folder):
        return
    for name in os.listdir(folder):
        fp = os.path.join(folder, name)
        try:
            if os.path.isfile(fp):
                os.remove(fp)
        except OSError:
            pass  # best-effort cleanup; never fail a test over this


@pytest.fixture
def login_flow(driver, reporter):
    """A ready LoginFlow wired with the shared driver + reporter."""
    return LoginFlow(driver, reporter)


@pytest.fixture
def tee_time_flow(driver, reporter):
    return TeeTimeFlow(driver, reporter)


@pytest.fixture
def logout_flow(driver):
    return LogoutFlow(driver)


@pytest.fixture
def events_flow(driver, reporter):
    return EventsFlow(driver, reporter)


@pytest.fixture
def driving_range_flow(driver, reporter):
    return DrivingRangeFlow(driver, reporter)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """After the whole run, print (and save) a regression summary: each failed
    test with its last step and last screenshot."""
    failures = getattr(config, "_regression_failures", [])
    tr = terminalreporter

    if os.getenv("CLICKUP_SYNC") == "1":
        try:
            from utils.clickup_sync import sync_results
            from config.clickup_map import TC_TO_TASK

            pdf_lines = getattr(config_module, "_clickup_pdf_paths", [])

            results = []
            for st in ("passed", "failed", "error"):
                for rep in terminalreporter.stats.get(st, []):
                    tc = _tc_from_nodeid(rep.nodeid)
                    err = ""
                    if st in ("failed", "error") and getattr(rep, "longrepr", None):
                        crash = getattr(rep.longrepr, "reprcrash", None)
                        err = (crash.message if crash else str(rep.longrepr) or "").strip().splitlines()[0]
                    pdf = ""

                    slug = tc
                    if "::" in rep.nodeid:
                        slug = rep.nodeid.split("::")[-1]
                    slug = slug.split("[")[0]
                    if slug.startswith("test_"):
                        slug = slug[5:]

                    for p in pdf_lines:
                        if slug and slug in os.path.basename(p):
                            pdf = p
                            break

                    if not pdf and pdf_lines:
                        pdf = max(pdf_lines, key=lambda x: os.path.getmtime(x))
                    results.append({
                        "tc_id": tc,
                        "nodeid": rep.nodeid,
                        "status": "PASS" if st == "passed" else "FAIL",
                        "error": err,
                        "pdf": pdf,
                    })
            sync_results(results, TC_TO_TASK)
            tr.write_line("[clickup] done sync")
        except Exception as e:
            tr.write_line(f"[clickup] failed to sync (skipped)): {e}")

    if not failures:
        return

    tr.write_sep("=", f"REGRESSION SUMMARY — {len(failures)} FAILED", red=True, bold=True)
    for f in failures:
        tr.write_line(f"FAIL  {f['test']}  (in {f['phase']})", red=True, bold=True)
        tr.write_line(f"      last step  : {f['last_step']}")
        if f["last_description"]:
            tr.write_line(f"      detail     : {f['last_description']}")
        tr.write_line(f"      screenshot : {f['last_screenshot'] or '(none)'} (in PDF)")
        tr.write_line(f"      evidence   : {f['pdf'] or '(no PDF)'}")
        if f["error"]:
            tr.write_line(f"      error      : {f['error']}")

    path = _write_regression_summary(failures)
    tr.write_line("")
    tr.write_line(f"Regression summary written to: {path}")


def _write_regression_summary(failures) -> str:
    """Persist the failure summary as a plain-text file in reports/."""
    from datetime import datetime

    os.makedirs(settings.REPORTS_DIR, exist_ok=True)
    path = os.path.join(settings.REPORTS_DIR, "regression_summary.txt")
    lines = [
        "Regression summary",
        f"Generated : {datetime.now():%Y-%m-%d %H:%M:%S}",
        f"Failed    : {len(failures)}",
        "=" * 60,
    ]
    for f in failures:
        lines += [
            f"FAIL  {f['test']}  (in {f['phase']})",
            f"      last step  : {f['last_step']}",
        ]
        if f["last_description"]:
            lines.append(f"      detail     : {f['last_description']}")
        lines.append(f"      screenshot : {f['last_screenshot'] or '(none)'} (in PDF)")
        lines.append(f"      evidence   : {f['pdf'] or '(no PDF)'}")
        if f["error"]:
            lines.append(f"      error      : {f['error']}")
        lines.append("-" * 60)
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    return path

def _tc_from_nodeid(nid):
    m = re.search(r"\[([^\]]+)\]", nid)
    if m:
        return m.group(1).split("-")[0].strip()
    
    return nid.split("::")[-1]