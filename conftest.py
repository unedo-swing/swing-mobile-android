"""
Pytest fixtures shared by all tests.

PDF evidence is ON by default: every test writes a PDF to reports/ (disable with
PDF_EVIDENCE=0). Each test opens its own report — ``init_pdf(...)`` on the first
line, ``generate_pdf(pdf)`` after the last step — and the autouse pdf_evidence
fixture below only clears the per-test state and covers the failure case (a test
that raises never reaches its own generate_pdf, so the fixture writes that
report stamped FAIL). See utils/pdf_reporter.py.

After the whole run, a regression summary is printed (and written to
reports/regression_summary.txt) listing each FAILED test with its last step and
last screenshot — see pytest_terminal_summary() below.

Environment variables are loaded from a local .env (if present) via python-dotenv
before anything reads os.getenv — see load_dotenv() below. Running with --prod
(or PROD=1) layers .env.prod on top, targeting the Play Store build instead of
the bundled dev APK.
"""
import os
import sys
from dotenv import load_dotenv, dotenv_values

_ROOT = os.path.dirname(os.path.abspath(__file__))
_ENV = os.path.join(_ROOT, ".env")
_ENV_PROD = os.path.join(_ROOT, ".env.prod")

# override=True so this project's .env wins over any stale exported vars leaked
# from a sibling project (e.g. Swing_Mobile's APP path). Must run before config/
# data modules read os.getenv.
load_dotenv(_ENV, override=True)


def _wants_prod() -> bool:
    """True when this run targets production.

    Read straight from argv rather than from a pytest option: the config
    modules read os.getenv at import time, which happens before pytest has
    parsed its own arguments. --prod is still registered in pytest_addoption()
    so pytest doesn't reject it.
    """
    return (
        os.getenv("PROD", "").strip().casefold() in ("1", "true", "yes", "on")
        or "--prod" in sys.argv
    )


def _prefixed_keys(prefix: str) -> list:
    """The <PREFIX>_* variable names defined in the env files (not the whole
    environment — a stray exported DEV_* from another project shouldn't leak in)."""
    keys = []
    for path in (_ENV, _ENV_PROD):
        if os.path.exists(path):
            keys += [k for k in dotenv_values(path) if k.startswith(prefix + "_")]
    return keys


def _select_env(prod: bool) -> list:
    """Point the plain variable names (APP, APP_PACKAGE, ...) at the chosen
    environment's values.

    Two layouts work, and they can be mixed:

      * one file, prefixed variables — DEV_APP_PACKAGE / PROD_APP_PACKAGE in
        .env, promoted here to APP_PACKAGE. Anything unprefixed is shared.
      * a separate .env.prod overlay, layered over .env.

    Prefixed values are applied last, so they win over both the shared defaults
    and the overlay.

    :returns: the plain names that were resolved from a prefix.
    """
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
from flows.login_flow import LoginFlow
from flows.onboarding_flow import OnboardingFlow
from flows.tee_time_flow import TeeTimeFlow
from flows.driving_range_flow import DrivingRangeFlow
from flows.swing_credits_flow import SwingCreditsFlow
from flows.swing_pass_flow import SwingPassFlow
from flows.logout_flow import LogoutFlow
from utils import allure_reporter
from utils.pdf_reporter import (
    active_pdf_path,
    active_reporter,
    discard_staged,
    evidence_written,
    generate_pdf,
    register_flow,
    reset_evidence,
)


APP_STATES = ("force-stop", "clear", "reinstall")


def pytest_addoption(parser):
    parser.addoption(
        "--pdf",
        action="store_true",
        default=False,
        help="Enable PDF evidence (init_pdf() will return a reporter).",
    )
    parser.addoption(
        "--allure",
        action="store_true",
        default=False,
        help=(
            "Force Allure results on (they are on by default already). Fails the "
            "run when allure-pytest is missing, instead of quietly skipping it — "
            "use it in CI to make sure the report is really produced."
        ),
    )
    parser.addoption(
        "--no-allure",
        action="store_true",
        default=False,
        help="Skip Allure results for this run (same as ALLURE=0).",
    )
    parser.addoption(
        "--allure-append",
        action="store_true",
        default=False,
        help=(
            "Keep the results already in the Allure directory instead of "
            "clearing it, so several pytest runs render as one report. Same as "
            "ALLURE_APPEND=1."
        ),
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


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Let the --pdf flag turn on PDF evidence for init_pdf(), and point
    allure-pytest at reports/allure-results.

    tryfirst so the results-directory setup lands before the allure-pytest
    plugin's own pytest_configure, which reads that option to decide whether to
    register its listener (and whether to clear the directory first).
    """
    if config.getoption("--pdf"):
        settings.PDF_EVIDENCE = True
    _configure_allure(config)
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


# --------------------------------------------------------------------------- #
# Run order
# --------------------------------------------------------------------------- #
# Out of the box pytest runs whole files in collection order (alphabetical),
# and inside a file the tests top-to-bottom as written. That puts
# test_driving_range.py before test_login.py, which is the wrong way round for
# a suite that has to get an account signed in first. Two knobs fix it:
#
#   1. SUITE_ORDER below — which file runs first, second, ... Anything not
#      listed runs afterwards, in normal alphabetical order.
#   2. @pytest.mark.run_order(n) on a test — moves it within its own file.
#      Lower numbers first; anything unmarked sits at 100, so run_order(1) is
#      "first" and run_order(999) is "last".
#
# Ties keep collection order, so a file with no markers still runs top-to-bottom.
#
# This is ordering, not selection: an unlisted file still runs, it just runs
# last. Pass --suites-only to run *nothing but* the listed files.
#
# The order below follows the account's own life: register it (onboarding),
# sign in with it (login), then book with it — driving range first, then the
# rest of the booking suites.
SUITE_ORDER = [
    "test_onboarding.py",
    # "test_login.py",
    # "test_driving_range_booking.py",
]

_UNMARKED_ORDER = 100


def _run_order_key(item):
    file_name = os.path.basename(str(item.path))
    try:
        suite_rank = SUITE_ORDER.index(file_name)
    except ValueError:
        suite_rank = len(SUITE_ORDER)      # unlisted files run last
    marker = item.get_closest_marker("run_order")
    test_rank = marker.args[0] if marker and marker.args else _UNMARKED_ORDER
    return (suite_rank, test_rank)


def pytest_collection_modifyitems(config, items):
    """Sort the collected tests by SUITE_ORDER, then by @pytest.mark.run_order.

    With --suites-only, files missing from SUITE_ORDER are deselected as well,
    so the list becomes the whole run instead of just its running order.
    """
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


def _configure_allure(config):
    """Point allure-pytest at the results directory and tell the reporter module
    it is live.

    Allure results are ON for every run — like the PDF evidence, reporting is
    not something you should have to remember to ask for. Turn them off with
    ``--no-allure`` / ``ALLURE=0``; move them with ``--alluredir=<path>`` or
    ``ALLURE_DIR``.

    The directory is cleared at the start of each run (``--allure-append`` /
    ``ALLURE_APPEND=1`` keeps it), so a report always shows that run and not a
    pile-up of every run since the folder was last emptied. environment.properties
    is written at session finish for exactly this reason.
    """
    forced = config.getoption("--allure")
    if not allure_reporter.AVAILABLE:
        if forced:
            raise pytest.UsageError(
                "--allure needs the allure-pytest package: "
                "pip install -r requirements.txt (or pip install allure-pytest)."
            )
        # default-on must never break a run on a machine that hasn't installed
        # it yet — pytest_report_header says so out loud instead
        return
    if config.getoption("--no-allure") or (not settings.ALLURE and not forced):
        return

    # allure_report_dir is registered by allure-pytest; set unless --alluredir
    # was passed, in which case that path wins
    results_dir = getattr(config.option, "allure_report_dir", None) or settings.ALLURE_DIR
    config.option.allure_report_dir = results_dir
    if not config.getoption("--allure-append") and not settings.ALLURE_APPEND:
        config.option.clean_alluredir = True
    allure_reporter.activate(os.path.abspath(results_dir))


def _run_metadata(config) -> dict:
    """What this run is actually pointed at — which build, which device, which
    reset. Feeds both the terminal header and Allure's environment widget."""
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


def pytest_report_header(config):
    """Print what this run is actually pointed at — which build, which device,
    which reset. Cheap insurance against a prod run that looks like a dev one
    (and the reverse) after the fact, in the log and in CI."""
    lines = [f"{key:<11}: {value}" for key, value in _run_metadata(config).items()]
    if allure_reporter.active():
        lines.append(f"{'allure':<11}: {allure_reporter.results_dir()}")
    elif not allure_reporter.AVAILABLE:
        lines.append(
            f"{'allure':<11}: OFF — allure-pytest is not installed "
            "(pip install -r requirements.txt)"
        )
    else:
        lines.append(f"{'allure':<11}: off (--no-allure / ALLURE=0)")
    if PROD:
        lines.append(
            "WARNING    : live app — bookings and payments are real; do not run "
            "the booking/payment suites"
        )
    return lines


def pytest_sessionfinish(session, exitstatus):
    """Write Allure's environment.properties once the run is over — at session
    start it would be wiped by --clean-alluredir."""
    allure_reporter.write_environment(
        {key.replace(" ", "_"): value for key, value in _run_metadata(session.config).items()}
    )


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Expose each phase's result on the item so fixtures can read pass/fail."""
    rep = yield
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def TC_ID(request):
    tc_id = request.param
    DrivingRangeData.load(tc_id)
    return tc_id


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


@pytest.fixture
def app_state(request) -> str:
    """The app state for this test: an ``@pytest.mark.app_state(...)`` marker
    if the test carries one, otherwise the --app-state / APP_STATE setting."""
    marker = request.node.get_closest_marker("app_state")
    if marker is not None and marker.args:
        state = marker.args[0]
        if state not in APP_STATES:
            raise ValueError(f"unknown app_state '{state}' — expected one of {APP_STATES}")
        return state
    return request.config.getoption("--app-state")


@pytest.fixture
def driver(app_state):
    """A fresh Appium Android driver per test, quit automatically at the end.

    The app is prepared per ``app_state`` first — force-stopped by default, so
    each test reopens fresh at Home without a reinstall.
    """
    pkg = os.getenv("APP_PACKAGE", "app.getswing.dev")
    device = os.getenv("DEVICE_NAME", "emulator-5554")
    _prepare_app(app_state, pkg, device)

    drv = create_driver()
    yield drv
    drv.quit()


@pytest.fixture(autouse=True)
def pdf_evidence(request):
    """Per-test PDF bookkeeping around the test's own init_pdf()/generate_pdf().

    The test owns its report now: it opens one with ``init_pdf`` on the first
    line and writes it with ``generate_pdf`` after the last step. This fixture
    only does what a test cannot do for itself:

      * clears the previous test's registrations, so the flow fixtures below
        hand THIS test's flows to its ``init_pdf``;
      * acts as the safety net for a test that never reaches its
        ``generate_pdf`` line — an assert, a lost element, a timeout — writing
        that report stamped FAIL so the evidence (and the regression summary)
        still exists;
      * clears reports/screenshots once the PDF holds them.

    Autouse, and every flow fixture depends on it, so the ordering above holds
    even for a test that takes no flow at all.
    """
    reset_evidence()
    # feature/story/severity for the Allure case (no-op when Allure is off);
    # its title comes later, from the test's own init_pdf()
    allure_reporter.apply_labels(request.node)
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
    # the PDF is the full evidence doc — hang it off the Allure case, so a
    # failure in the report links straight to it
    allure_reporter.attach_pdf(pdf_path)
    # screenshots are embedded in the PDF now -> clear the folder once it's built
    if pdf_path:
        _empty_screenshots_dir()
    # PDF_OUTPUT=allure: the attachment IS the evidence, so the staged file goes
    # away and the summary points at the Allure case instead of a dead path
    location = discard_staged(pdf_path)
    if failed_rep is not None:
        _record_failure(request, pdf, failed_rep, location)


def _record_failure(request, pdf, rep, evidence):
    """Stash a failed test's last step + screenshot for pytest_terminal_summary.

    The screenshot file itself is deleted after the PDF is built, so we keep its
    name (it's the last image in the PDF) and point to the PDF as the evidence —
    a path when one was kept, otherwise where in Allure the attachment lives.
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


@pytest.fixture
def flow(driver, pdf_evidence):
    """Factory for the flow fixtures below: builds a flow on the shared driver
    and registers it, so the test's ``init_pdf()`` attaches the reporter to it.

    The flow starts with no reporter — a flow builds its page objects in
    __init__, before the test body has opened its report — and ``init_pdf``
    rewires those pages when the test calls it.
    """
    def _make(flow_class):
        return register_flow(flow_class(driver))
    return _make


@pytest.fixture
def login_flow(flow):
    """A ready LoginFlow wired with the shared driver."""
    return flow(LoginFlow)


@pytest.fixture
def logout_flow(flow):
    """A ready LogoutFlow wired with the shared driver."""
    return flow(LogoutFlow)


@pytest.fixture
def onboarding_flow(flow):
    """A ready OnboardingFlow (profile setup + its pickers) wired with the
    shared driver."""
    return flow(OnboardingFlow)


@pytest.fixture
def tee_time_flow(flow):
    return flow(TeeTimeFlow)


@pytest.fixture
def driving_range_flow(flow):
    return flow(DrivingRangeFlow)


@pytest.fixture
def swing_credits_flow(flow):
    """A ready SwingCreditsFlow (credits screen, history, cashbacks, redeem)."""
    return flow(SwingCreditsFlow)


@pytest.fixture
def swing_pass_flow(flow):
    """A SwingPassFlow (membership, billing history, plan / method changes,
    cancellation and renew)."""
    return flow(SwingPassFlow)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """After the whole run, print (and save) a regression summary: each failed
    test with its last step and last screenshot."""
    failures = getattr(config, "_regression_failures", [])
    if not failures:
        return

    tr = terminalreporter
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

