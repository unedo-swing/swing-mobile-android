"""
Desired capabilities for Android (UiAutomator2).

Keeping these in one place means when the device / app / version changes you edit
here only, never the driver code or the tests.

Anything can be overridden from the environment, e.g.:

    DEVICE_NAME="emulator-5554" APP_PACKAGE="app.getswing.dev" pytest

You can point at EITHER an already-installed app (APP_PACKAGE + APP_ACTIVITY)
OR install a build from an .apk (set APP to the apk path). By default this
framework installs the bundled apps/app.apk on first run and reuses it after.
"""
import os

from appium.options.android import UiAutomator2Options

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_APK = os.path.join(_BASE_DIR, "apps", "app.apk")


def android_options() -> UiAutomator2Options:
    """Build the Android (UiAutomator2) capabilities."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = os.getenv("DEVICE_NAME", "emulator-5554")

    platform_version = os.getenv("PLATFORM_VERSION")
    if platform_version:
        options.platform_version = platform_version

    # App target: an .apk path wins; otherwise use the installed package.
    # A relative APP is resolved against this project's dir (not Appium's cwd),
    # and a missing/foreign path falls back to the bundled build.
    app = os.getenv("APP", "").strip()
    if app and not os.path.isabs(app):
        app = os.path.join(_BASE_DIR, app)
    if not app or not os.path.exists(app):
        app = _DEFAULT_APK if os.path.exists(_DEFAULT_APK) else ""
    if app:
        options.app = app
    options.app_package = os.getenv("APP_PACKAGE", "app.getswing.dev")
    options.app_activity = os.getenv("APP_ACTIVITY", "app.getswing.MainActivity")
    options.set_capability("appWaitActivity", os.getenv("APP_WAIT_ACTIVITY", "*"))

    options.no_reset = os.getenv("NO_RESET", "true") == "true"
    options.full_reset = os.getenv("FULL_RESET", "false") == "true"
    options.new_command_timeout = 120
    options.set_capability("autoGrantPermissions", True)
    # Flutter/Compose surfaces render into a single view — give UiAutomator2 a
    # moment and don't wait on an idle app that keeps ticking (FPS overlay etc).
    options.set_capability("waitForIdleTimeout", 100)
    return options
