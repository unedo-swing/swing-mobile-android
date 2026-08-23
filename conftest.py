import os
import sys
import time
from dotenv import load_dotenv, dotenv_values

_ROOT = os.path.dirname(os.path.abspath(__file__))
_ENV = os.path.join(_ROOT, ".env")
_ENV_PROD = os.path.join(_ROOT, ".env.prod")

load_dotenv(_ENV, override=True)


def _wants_prod() -> bool:
    return (
        os.getenv("PROD", "").strip().casefold() in ("1", "true", "yes", "on")
        or "--prod" in sys.argv
    )


def _prefixed_keys(prefix: str) -> list:
    keys = []
    for path in (_ENV, _ENV_PROD):
        if os.path.exists(path):
            keys += [k for k in dotenv_values(path) if k.startswith(prefix + "_")]
    return keys


def _select_env(prod: bool) -> list:
    prefix = "PROD" if prod else "DEV"
    if prod and os.path.exists(_ENV_PROD):
        load_dotenv(_ENV_PROD, override=True)

    resolved = []
    for key in _prefixed_keys(prefix):
        value = os.environ.get(key)
        if value is not None:
            os.environ[key[len(prefix) + 1:]] = value
            resolved.append(key[len(prefix) + 1:])

    if prod and not resolved and not os.path.exists(_ENV_PROD):
        raise RuntimeError(
            "--prod/PROD=1 was given but no production config was found: no "
            f"PROD_* variables in {_ENV} and no {_ENV_PROD}. Refusing to run — "
            "without it the tests would silently hit the dev build instead."
        )
    return resolved


PROD = _wants_prod()
ENV_RESOLVED = _select_env(PROD)

import pytest

from config import settings
from core.driver_factory import create_driver
from data.driving_range_data import DrivingRangeData
from data.events_data import EventsData
from flows.login_flow import LoginFlow
from flows.onboarding_flow import OnboardingFlow
from flows.tee_time_flow import TeeTimeFlow
from flows.driving_range_flow import DrivingRangeFlow
from flows.swing_credits_flow import SwingCreditsFlow
from flows.swing_pass_flow import SwingPassFlow
from flows.logout_flow import LogoutFlow
from utils import clickup_reporter
from utils.pdf_reporter import (
    active_pdf_path,
    active_reporter,
    evidence_written,
    generate_pdf,
    register_flow,
    reset_evidence,
    
)

from flows.events_flow import EventsFlow
from utils.pdf_reporter import init_pdf, generate_pdf
from utils.excel_reader import find_rows
from data.driving_range_data import _DATA_PATH as _DR_PATH, _SHEET as _DR_SHEET


APP_STATES = ("force-stop", "clear", "reinstall")

SUITE_ORDER = [
    # "test_onboarding.py",
    # "test_login.py",
    # "test_driving_range_booking.py",
    # "test_driving_range_booking_regular_player.py",
    # "test_swing_credits.py"
    "test_driving_range_booking_regular_malaysia.py",
    "test_driving_range_booking_cross_country.py"
]

_UNMARKED_ORDER = 100


def pytest_addoption(parser):
    parser.addoption(
        "--pdf",
        action="store_true",
        default=False,
        help="Enable PDF evidence (init_pdf() will return a reporter).",
    )
    parser.addoption(
        "--clickup",
        action="store_true",
        default=False,
        help=(
            "Post a one-message run summary to the ClickUp channel configured in "
            ".env (CLICKUP_TOKEN / CLICKUP_WORKSPACE_ID / CLICKUP_CHANNEL_ID). "
            "Off by default so local runs stay quiet; same as CLICKUP_REPORT=1."
        ),
    )
    parser.addoption(
        "--no-clickup",
        action="store_true",
        default=False,
        help="Skip the ClickUp message for this run, even with CLICKUP_REPORT=1.",
    )
    parser.addoption(
        "--suites-only",
        action="store_true",
        default=False,
        help=(
            "Run only the files listed in SUITE_ORDER, in that order — anything "
            "unlisted is deselected. Off by default, so a newly added test file "
            "is never silently skipped just because nobody listed it."
        ),
    )
    parser.addoption(
        "--prod",
        action="store_true",
        default=False,
        help=(
            "Target the production (Play Store) app: layers .env.prod over .env. "
            "Equivalent to PROD=1. Consumed at conftest import time — registered "
            "here only so pytest accepts the flag."
        ),
    )
    parser.addoption(
        "--app-state",
        choices=APP_STATES,
        default=os.getenv("APP_STATE", "force-stop"),
        help=(
            "How to prepare the app before each test: "
            "'force-stop' (default) reopens the installed app, keeping login and "
            "the seen-it flags; 'clear' wipes the app data (adb pm clear) so the "
            "run behaves like a fresh install — What's new, the coach marks and "
            "onboarding come back, and so does the OTP login; 'reinstall' "
            "uninstalls first and lets Appium install the APK again. Can also be "
            "set with APP_STATE=<state>."
        ),
    )


def pytest_configure(config):
    if config.getoption("--pdf"):
        settings.PDF_EVIDENCE = True
    config.addinivalue_line(
        "markers",
        "app_state(state): force this test's app state ('force-stop', 'clear' or "
        "'reinstall'), overriding --app-state.",
    )
    config.addinivalue_line(
        "markers",
        "run_order(n): run this test earlier or later inside its own file "
        "(lower runs first; unmarked tests are 100).",
    )
    # collects one entry per failed test for the end-of-run regression summary
    config._regression_failures = []
    # every evidence PDF this run wrote, for the ClickUp upload
    config._run_pdfs = []
    # one entry per test — name, status and its PDF — for the ClickUp report
    config._run_results = []


def pytest_collection_modifyitems(config, items):
    items.sort(key=_run_order_key)   # list.sort is stable: ties keep their place
    if not config.getoption("--suites-only"):
        return

    listed, unlisted = [], []
    for item in items:
        target = listed if os.path.basename(str(item.path)) in SUITE_ORDER else unlisted
        target.append(item)
    if not listed:
        raise pytest.UsageError(
            "--suites-only left nothing to run: none of the collected files are "
            f"in SUITE_ORDER ({', '.join(SUITE_ORDER) or 'empty'})."
        )
    if unlisted:
        config.hook.pytest_deselected(items=unlisted)
        items[:] = listed


def pytest_report_header(config):
    lines = [f"{key:<11}: {value}" for key, value in _run_metadata(config).items()]
    if PROD:
        lines.append(
            "WARNING    : live app — bookings and payments are real; do not run "
            "the booking/payment suites"
        )
    return lines


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    rep = yield
    setattr(item, "rep_" + rep.when, rep)
    return rep


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Close the run: report it to ClickUp (upload the evidence PDFs, post the
    message, delete the uploaded files), then print and save the regression
    summary — each failed test with its last step, screenshot and evidence."""
    failures = getattr(config, "_regression_failures", [])
    tr = terminalreporter

    # ClickUp first: it uploads the evidence PDFs and hands back a
    # {local path: clickup url} map, so everything printed below can point at a
    # link that outlives the local file (which cleanup_pdfs then removes).
    note, links = _report_to_clickup(tr, config, failures)
    clickup_reporter.cleanup_pdfs(getattr(config, "_run_pdfs", []), links)

    if failures:
        tr.write_sep("=", f"REGRESSION SUMMARY — {len(failures)} FAILED", red=True, bold=True)
        for f in failures:
            tr.write_line(f"FAIL  {f['test']}  (in {f['phase']})", red=True, bold=True)
            tr.write_line(f"      last step  : {f['last_step']}")
            if f["last_description"]:
                tr.write_line(f"      detail     : {f['last_description']}")
            tr.write_line(f"      screenshot : {f['last_screenshot'] or '(none)'} (in PDF)")
            tr.write_line(f"      evidence   : {_evidence(f, links)}")
            if f["error"]:
                tr.write_line(f"      error      : {f['error']}")

        path = _write_regression_summary(failures, links)
        tr.write_line("")
        tr.write_line(f"Regression summary written to: {path}")

    if note:
        tr.write_line("")
        tr.write_line(note)


@pytest.fixture
def app_state(request) -> str:
    marker = request.node.get_closest_marker("app_state")
    if marker is not None and marker.args:
        state = marker.args[0]
        if state not in APP_STATES:
            raise ValueError(f"unknown app_state '{state}' — expected one of {APP_STATES}")
        return state
    return request.config.getoption("--app-state")


@pytest.fixture
def driver(app_state):
    pkg = os.getenv("APP_PACKAGE", "app.getswing.dev")
    device = os.getenv("DEVICE_NAME", "emulator-5554")
    _prepare_app(app_state, pkg, device)

    drv = create_driver()
    _wait_app_ready(drv, pkg, timeout=int(os.getenv("APP_READY_TIMEOUT", "90")))
    yield drv
    drv.quit()


@pytest.fixture(autouse=True)
def pdf_evidence(request):
    reset_evidence()
    yield

    rep_setup = getattr(request.node, "rep_setup", None)
    rep_call = getattr(request.node, "rep_call", None)
    failed_rep = next(
        (r for r in (rep_setup, rep_call) if r is not None and r.failed), None
    )
    pdf = active_reporter()
    pdf_path = active_pdf_path()
    if failed_rep is not None and not evidence_written():
        pdf_path = generate_pdf(pdf, status="FAIL")
    # screenshots are embedded in the PDF now -> clear the folder once it's built
    if pdf_path:
        _empty_screenshots_dir()
    # the ClickUp reporter uploads these at the end of the run and links each one
    # next to its test case, then deletes the local file (see PDF_CLEANUP)
    on_disk = pdf_path if (pdf_path and os.path.exists(pdf_path)) else None
    if on_disk:
        request.config._run_pdfs.append(on_disk)
    skipped = any(r is not None and r.skipped for r in (rep_setup, rep_call))
    request.config._run_results.append({
        "test": request.node.nodeid,
        "tc_id": getattr(pdf, "tc_id", "") or "",
        "name": (getattr(pdf, "tc_name", "") or getattr(pdf, "test_name", "")
                 or request.node.name),
        "status": "FAILED" if failed_rep is not None else ("SKIPPED" if skipped else "PASSED"),
        "pdf": on_disk,
    })
    if failed_rep is not None:
        _record_failure(request, pdf, failed_rep, on_disk)


@pytest.fixture
def flow(driver, pdf_evidence):
    def _make(flow_class):
        return register_flow(flow_class(driver))
    return _make


@pytest.fixture
def login_flow(flow):
    return flow(LoginFlow)


@pytest.fixture
def logout_flow(flow):
    return flow(LogoutFlow)


@pytest.fixture
def onboarding_flow(flow):
    return flow(OnboardingFlow)


@pytest.fixture
def tee_time_flow(flow):
    return flow(TeeTimeFlow)


@pytest.fixture
def driving_range_flow(flow):
    return flow(DrivingRangeFlow)


@pytest.fixture
def swing_credits_flow(flow):
    return flow(SwingCreditsFlow)


@pytest.fixture
def swing_pass_flow(flow):
    return flow(SwingPassFlow)


def _run_order_key(item):
    file_name = os.path.basename(str(item.path))
    try:
        suite_rank = SUITE_ORDER.index(file_name)
    except ValueError:
        suite_rank = len(SUITE_ORDER)      # unlisted files run last
    marker = item.get_closest_marker("run_order")
    test_rank = marker.args[0] if marker and marker.args else _UNMARKED_ORDER
    return (suite_rank, test_rank)


def _run_metadata(config) -> dict:
    """What this run is actually pointed at — which build, which device, which
    reset. Feeds both the terminal header and the ClickUp run report."""
    from config.capabilities import resolved_app

    app = resolved_app()
    prefix = "PROD" if PROD else "DEV"
    return {
        "target": f"{'PRODUCTION' if PROD else 'dev'} ({prefix}_* from .env)",
        "package": os.getenv("APP_PACKAGE", "app.getswing.dev"),
        "apk": app or "none — using the build installed on the device",
        "device": os.getenv("DEVICE_NAME", "emulator-5554"),
        "app state": config.getoption("--app-state"),
        "appium": settings.APPIUM_SERVER_URL,
        "platform": settings.PLATFORM,
    }


def _adb(device: str, *args) -> int:
    """Run one adb command against ``device``; never raises."""
    import subprocess

    command = ["adb", "-s", device, *args]
    print(f"[app state] {' '.join(command)}")
    return subprocess.run(command, check=False).returncode


def _prepare_app(state: str, pkg: str, device: str):
    """Put the app in the requested state before the driver starts.

    force-stop : close the running app, keep its data (the default — fastest,
                 and what the existing suites expect: still logged in, no
                 first-run screens).
    clear      : wipe the app's data, so the next launch behaves like a fresh
                 install (What's new, coach marks, onboarding — and the login
                 has to be done again).
    reinstall  : uninstall it, so Appium installs the APK from the caps again.
                 The heaviest reset; needed when the build itself changed.
                 Refused when there is no APK to reinstall from (APP=none, i.e.
                 a Play Store build) — it would uninstall the app under test
                 and leave the device with nothing.
    """
    from config.capabilities import resolved_app

    if state == "reinstall" and not resolved_app():
        raise RuntimeError(
            "--app-state reinstall needs an APK, but APP=none (using the installed "
            f"build of '{pkg}'). Uninstalling it could not be undone from here — "
            "reinstall it from the Play Store, or use --app-state clear instead."
        )
    _adb(device, "shell", "am", "force-stop", pkg)
    if state == "clear":
        _adb(device, "shell", "pm", "clear", pkg)
    elif state == "reinstall":
        _adb(device, "uninstall", pkg)


# query_app_state() codes we care about: 4 is "running in foreground".
_APP_IN_FOREGROUND = 4


def _wait_app_ready(drv, pkg: str, timeout: int = 90) -> bool:
    """Block until the app has finished starting after force-stop / clear.

    Appium returns as soon as the activity is up, which on this Flutter build is
    still the splash: the first find() then races the real first screen. Here we
    wait for the app to be in the foreground AND for its view tree to stop
    growing, so tests start against a rendered screen instead of a splash.

    Never raises: a run that times out continues and fails on the screen's own
    verify_screen(), which says what was expected instead of "element not found".
    """
    import time

    deadline = time.time() + timeout
    previous, stable_since, reason = "", None, "app never reached the foreground"
    while time.time() < deadline:
        try:
            if drv.query_app_state(pkg) != _APP_IN_FOREGROUND:
                previous, stable_since = "", None
                reason = "app is not in the foreground yet"
            else:
                source = drv.page_source
                if f'package="{pkg}"' not in source:
                    previous, stable_since = "", None
                    reason = "app is in the foreground but nothing is rendered yet"
                elif source == previous:
                    if time.time() - stable_since >= 1.0:
                        print(f"[app state] app '{pkg}' is ready")
                        return True
                else:
                    previous, stable_since = source, time.time()
                    reason = "the screen is still rendering"
        except Exception as exc:                      # driver hiccup while booting
            previous, stable_since = "", None
            reason = str(exc).splitlines()[0]
        time.sleep(0.5)

    print(f"[app state] app '{pkg}' not ready after {timeout}s — {reason}")
    return False


def _record_failure(request, pdf, rep, evidence):
    """Stash a failed test's last step + screenshot for pytest_terminal_summary.

    The screenshot file itself is deleted after the PDF is built, so we keep its
    name (it's the last image in the PDF) and point to the PDF as the evidence.
    The path is swapped for the file's ClickUp link once it has been uploaded.
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
        "pdf": evidence,
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


def _evidence(failure, links) -> str:
    """Where this failure's PDF can be read — its ClickUp link once uploaded,
    otherwise the local file."""
    path = failure.get("pdf")
    return links.get(path) or path or "(no PDF)"


def _report_to_clickup(terminalreporter, config, failures):
    """Post the run to the channel. Returns (terminal line, {pdf path: url})."""
    if not clickup_reporter.enabled(config):
        return "", {}

    stats = terminalreporter.stats
    counts = {
        key: len(stats.get(key, []))
        for key in ("passed", "failed", "error", "skipped", "xfailed", "xpassed")
    }
    started = getattr(terminalreporter, "_sessionstarttime", None)
    duration = (time.time() - started) if started else None

    return clickup_reporter.send({
        "title": f"Swing Mobile{' — PRODUCTION' if PROD else ' - DEV'}",
        "counts": counts,
        "duration": duration,
        "metadata": _run_metadata(config),
        "marker": config.getoption("markexpr", "") or "",
        "failures": failures,
        "results": getattr(config, "_run_results", []),
        "pdfs": getattr(config, "_run_pdfs", []),
    })


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
        lines.append(f"      evidence   : {_evidence(f, links or {})}")
        if f["error"]:
            lines.append(f"      error      : {f['error']}")
        lines.append("-" * 60)
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    return path
