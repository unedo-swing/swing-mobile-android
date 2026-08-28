"""The device under test: what state the app is in, and the Appium session.

Registered from the root conftest via ``pytest_plugins``.
"""
import os

import pytest

from config import settings
from core.driver_factory import create_driver
from utils import adb


def _adb(device: str, *args) -> int:
    """Run one adb command against ``device``; never raises."""
    print(f"[app state] adb -s {device} {' '.join(args)}")
    try:
        return adb.run(*args, device=device).returncode
    except Exception as exc:
        print(f"[app state] adb failed, continuing: {str(exc).splitlines()[0]}")
        return 1


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

@pytest.fixture
def app_state(request) -> str:
    marker = request.node.get_closest_marker("app_state")
    if marker is not None and marker.args:
        state = marker.args[0]
        if state not in settings.APP_STATES:
            raise ValueError(f"unknown app_state '{state}' — expected one of {settings.APP_STATES}")
        return state
    return request.config.getoption("--app-state")

@pytest.fixture
def driver(app_state):
    pkg = os.getenv("APP_PACKAGE", "app.getswing.dev")
    device = adb.serial()
    _prepare_app(app_state, pkg, device)

    drv = create_driver()
    _wait_app_ready(drv, pkg, timeout=int(os.getenv("APP_READY_TIMEOUT", "90")))
    yield drv
    try:
        drv.quit()
    except Exception as exc:
        # A test that failed because the session died would otherwise get a
        # teardown ERROR stacked on top of its real failure — and the next test
        # starts from _prepare_app anyway.
        print(f"[driver] quit failed, continuing: {str(exc).splitlines()[0]}")
