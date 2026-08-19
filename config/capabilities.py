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
# Fallback builds, in preference order, used when APP names a file that isn't
# there. app-dev.apk is the current name; app.apk is what it used to be called.
_DEFAULT_APKS = [
    os.path.join(_BASE_DIR, "apps", name) for name in ("app-dev.apk", "app.apk")
]

# APP values that mean "don't install anything — drive the build that's already
# on the device". That's the only way to test a Play Store (production) install:
# there is no APK to hand Appium, and installing one would replace the very
# build under test.
_USE_INSTALLED = ("none", "installed", "off", "false")


def resolved_app() -> str:
    """The .apk Appium should install, or "" to use the installed package.

    A relative APP is resolved against this project's dir (not Appium's cwd).
    APP=none (see _USE_INSTALLED) opts out of installing altogether; any other
    missing/foreign path falls back to the bundled build.
    """
    app = os.getenv("APP", "").strip()
    if app.casefold() in _USE_INSTALLED:
        return ""
    if app and not os.path.isabs(app):
        app = os.path.join(_BASE_DIR, app)
    if app and os.path.exists(app):
        return app
    return next((path for path in _DEFAULT_APKS if os.path.exists(path)), "")


def android_options() -> UiAutomator2Options:
    """Build the Android (UiAutomator2) capabilities."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = os.getenv("DEVICE_NAME", "emulator-5554")

    platform_version = os.getenv("PLATFORM_VERSION")
    if platform_version:
        options.platform_version = platform_version

    # App target: an .apk path wins; APP=none uses whatever is installed
    # (production builds from the Play Store) — see resolved_app().
    app = resolved_app()
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
