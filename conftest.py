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
from utils import adb, clickup_reporter


# The fixtures live in their own modules so this file stays hooks-and-config
# only, and so a duplicate fixture is visible inside a short file instead of
# hiding 200 lines below the original. Imported after the env bootstrap above,
# which they depend on.
pytest_plugins = [
    "fixtures.driver",
    "fixtures.evidence",
    "fixtures.flows",
]

SUITE_ORDER = [
    "test_login.py",
    "test_onboarding.py",
    # "test_driving_range_booking.py",
    # "test_driving_range_booking_regular_player.py",
    # "test_swing_credits.py"
    # "test_driving_range_booking_regular_malaysia.py",
    # "test_driving_range_booking_cross_country.py"
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
        choices=settings.APP_STATES,
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
    from config.capabilities import resolved_app

    app = resolved_app()
    prefix = "PROD" if PROD else "DEV"
    return {
        "target": f"{'PRODUCTION' if PROD else 'dev'} ({prefix}_* from .env)",
        "package": os.getenv("APP_PACKAGE", "app.getswing.dev"),
        "apk": app or "none — using the build installed on the device",
        "device": adb.serial(),
        "app state": config.getoption("--app-state"),
        "appium": settings.APPIUM_SERVER_URL,
        "platform": settings.PLATFORM,
    }


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


def _write_regression_summary(failures, links=None) -> str:
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
