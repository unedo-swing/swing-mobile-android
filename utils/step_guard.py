"""Evidence for the step that failed: screenshot it, then let the test end.

One "step" is one public method of a flow (``flows/base_flow.py`` wraps them all
with :func:`guard`), which is exactly one line in a test file. When a step
raises, the guard screenshots the screen as it was at the failure and records it
in the PDF as a FAILED step — then re-raises, so the test stops there and pytest
moves on to the next test.

Without this, a failure was only ever reported against the last *successful*
``capture_step``: the PDF's final screenshot was of a screen that worked, and
nothing named the step that actually broke.

Stateless on purpose — the failed step lives in the reporter, as the last step of
the test's PDF.
"""
import functools


def _first_line(exc: BaseException) -> str:
    text = str(exc).strip()
    first = text.splitlines()[0] if text else ""
    return f"{type(exc).__name__}: {first}" if first else type(exc).__name__


def _fatal_types() -> tuple:
    """Exceptions to re-raise without touching the screen.

    pytest's own outcomes (skip/fail/exit) mean the test asked to stop, and once
    the session itself is gone the app is no longer under our control — the
    screen has moved on, so a screenshot would show the wrong thing. Imported
    lazily so this module stays importable outside a pytest run.
    """
    types = []
    try:
        from _pytest.outcomes import OutcomeException

        types.append(OutcomeException)
    except ImportError:
        pass
    try:
        from selenium.common.exceptions import InvalidSessionIdException, NoSuchDriverException

        types += [InvalidSessionIdException, NoSuchDriverException]
    except ImportError:
        pass
    return tuple(types)


def guard(func):
    """Wrap a flow method so its failure is screenshotted on the way out."""
    if getattr(func, "_guarded", False):
        return func

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except _fatal_types():
            raise
        except Exception as exc:
            capture_failure(self, func.__name__, exc)
            raise

    wrapper._guarded = True
    return wrapper


def capture_failure(flow, step: str, exc: Exception):
    if getattr(exc, "_step_captured", False):
        return
    error = _first_line(exc)
    print(f"[FAILED STEP] {step} — {error}")
    try:
        exc._step_captured = True
    except AttributeError:          # exceptions with __slots__
        pass
    page = getattr(flow, "_evidence_page", None)
    if page is None:
        return
    try:
        page.capture_step(step, error, status="FAIL")
    except Exception as capture_error:   # a dead screen must not mask the real failure
        print(f"[FAILED STEP] could not capture evidence for {step}: "
              f"{_first_line(capture_error)}")
