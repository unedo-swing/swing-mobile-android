"""
Allure reporting — on for every run, side-by-side with the PDF evidence.

Every ``pytest`` invocation writes Allure results to ``reports/allure-results``
(``--no-allure`` / ``ALLURE=0`` opts out, ``--alluredir`` / ``ALLURE_DIR`` moves
them). Nothing here is required to run the tests, though: the whole module
degrades to no-ops when either

  * ``allure-pytest`` is not installed (import guard below) — a machine that
    hasn't installed it yet still runs the suite, it just gets no report, or
  * the run opted out, so conftest never calls ``activate()``.

How the pieces connect (no test or flow file has to know about Allure):

  * ``core/base_page.capture_step`` wraps every evidence step in ``step()`` and
    attaches the screenshot it already takes — so the Allure timeline mirrors
    the PDF's steps, step for step.
  * ``utils/pdf_reporter.init_pdf`` calls ``set_case()``, so a case shows up as
    "TT_001 — Book standard tee time" instead of
    ``test_book_standard_tee_time_full[TT_001]``.
  * ``conftest`` calls ``apply_labels()`` per test (feature/story/severity from
    the module, class and markers), attaches the PDF on failure, and writes
    ``environment.properties`` at the end of the run.

Rendering the results needs the Allure CLI (Java):

    pytest -m regression
    allure serve reports/allure-results
"""
import os
import re
from contextlib import contextmanager

try:  # allure-pytest is optional — the framework runs fine without it
    import allure
    from allure_commons.types import AttachmentType

    AVAILABLE = True
except ImportError:  # pragma: no cover - depends on the environment
    allure = None
    AttachmentType = None
    AVAILABLE = False


# Set by conftest.pytest_configure once the run really is writing results.
_state: dict = {"active": False, "results_dir": None}

# pytest marker -> Allure severity. Markers not listed here keep the default.
_SEVERITY_BY_MARKER = {
    "smoke": "critical",
    "regression": "normal",
    "manual": "minor",
}


def activate(results_dir: str):
    """Mark Allure as live for this run and remember where results go."""
    _state.update(active=bool(AVAILABLE and results_dir), results_dir=results_dir)


def active() -> bool:
    """True when this run is writing Allure results."""
    return bool(_state.get("active"))


def results_dir() -> str | None:
    return _state.get("results_dir")


def _humanize(raw: str) -> str:
    """A readable label from a module or class name.

    'test_driving_range_payment' -> 'Driving range payment'
    'TestDrivingRange'           -> 'Driving range'
    """
    text = (raw or "").removeprefix("test_").removeprefix("Test")
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)  # split CamelCase classes
    text = text.replace("_", " ").strip().lower()
    return text[:1].upper() + text[1:] if text else ""


@contextmanager
def step(title: str):
    """Wrap one evidence step. A plain pass-through when Allure is off."""
    if not active():
        yield
        return
    with allure.step(title):
        yield


def attach_png(path: str, name: str):
    """Attach a screenshot file to the current step."""
    if not active() or not path or not os.path.exists(path):
        return
    allure.attach.file(path, name=name, attachment_type=AttachmentType.PNG)


def attach_pdf(path: str, name: str = "PDF evidence"):
    """Attach the test's PDF report, so a failed case carries the full doc."""
    if not active() or not path or not os.path.exists(path):
        return
    allure.attach.file(path, name=name, attachment_type=AttachmentType.PDF)


def attach_text(name: str, body: str):
    if not active() or not body:
        return
    allure.attach(body, name=name, attachment_type=AttachmentType.TEXT)


def attach_step_data(data: dict | None, compare: dict | None):
    """Attach a step's structured data the same way the PDF renders it:
    ``data`` as a Field/Value list, ``compare`` as before/after with the
    mismatching fields called out."""
    if not active():
        return
    if data:
        attach_text("data", "\n".join(f"{k}: {v}" for k, v in data.items()))
    if compare:
        left = compare.get("left_label", "before")
        right = compare.get("right_label", "after")
        before = compare.get("before") or {}
        after = compare.get("after") or {}
        mismatch = set(compare.get("mismatch_fields") or [])
        lines = [f"{'field':<28}{left:<24}{right}"]
        for key in list(before) + [k for k in after if k not in before]:
            flag = "  <-- MISMATCH" if key in mismatch else ""
            lines.append(f"{key:<28}{str(before.get(key, '')):<24}{after.get(key, '')}{flag}")
        attach_text(f"{left} vs {right}", "\n".join(lines))


def set_case(test_name: str, tc_id: str | None = None, tc_name: str | None = None):
    """Title the Allure case from the data sheet instead of the pytest node id.

    Called from ``init_pdf`` — which every test opens with — so this needs no
    change in the test files. Runs even when PDF evidence is off.
    """
    if not active():
        return
    title = " — ".join(part for part in (tc_id, tc_name) if part) or test_name
    allure.dynamic.title(title)
    if tc_name:
        allure.dynamic.description(f"{test_name}\n\n{tc_name}")
    # Link the case back to a test management tool when one is configured, e.g.
    # ALLURE_TMS_URL="https://tms.example.com/case/{tc_id}". Left unset there is
    # no link — a bare TC ID would render as a dead URL.
    template = os.getenv("ALLURE_TMS_URL", "")
    if tc_id and "{tc_id}" in template:
        allure.dynamic.testcase(template.format(tc_id=tc_id), tc_id)


def apply_labels(item):
    """Feature/story/severity/tags for one test, derived from where it lives.

    Module -> feature ('test_driving_range.py' -> 'Driving range'), class ->
    story, and the suite markers map to severity via _SEVERITY_BY_MARKER.
    """
    if not active():
        return
    feature = _humanize(getattr(item.module, "__name__", "").rsplit(".", 1)[-1])
    if feature:
        allure.dynamic.feature(feature)
    cls = getattr(item, "cls", None)
    if cls is not None:
        story = _humanize(cls.__name__)
        if story:
            allure.dynamic.story(story)

    # Marker -> tag is allure-pytest's own default; only severity is ours.
    for name, severity in _SEVERITY_BY_MARKER.items():
        if item.get_closest_marker(name):
            allure.dynamic.severity(severity)
            break


def write_environment(values: dict):
    """Write results/environment.properties — the environment widget in the
    report (target build, package, device, app state, ...).

    Written at the end of the run: ``--clean-alluredir`` wipes the directory
    when the session starts, which would take the file with it.
    """
    folder = results_dir()
    if not active() or not folder:
        return None
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "environment.properties")
    with open(path, "w") as fh:
        for key, value in values.items():
            # properties files are key=value per line; keep values single-line
            fh.write(f"{key}={str(value).replace(chr(10), ' ')}\n")
    return path
