"""adb, for the moments Appium cannot help.

Every Appium command is proxied to the UiAutomator2 instrumentation running on
the device. When that process crashes, all of them fail — screenshots included:

    'GET /screenshot' cannot be proxied to UiAutomator2 server because the
    instrumentation process is not running (probably crashed)

which is exactly the moment the failing step needs its evidence. adb talks to
the device directly, so it still works after the instrumentation is gone.
"""
import os
import subprocess

_PNG_MAGIC = b"\x89PNG"


def serial() -> str:
    """The device adb commands target — same default as the driver fixture."""
    return os.getenv("DEVICE_NAME", "emulator-5554")


def run(*args, device: str = "", timeout: int = 60, capture: bool = False):
    """Run one adb command against the device and return its CompletedProcess."""
    command = ["adb", "-s", device or serial(), *args]
    return subprocess.run(command, check=False, timeout=timeout, capture_output=capture)


def screencap(path: str, device: str = "") -> bool:
    """Write a PNG of the current screen to ``path``. True when one was saved.

    ``exec-out`` streams the raw bytes back, so nothing mangles the PNG on the
    way. Never raises: this is the fallback path, and a failure here must not
    replace the failure that asked for the screenshot.
    """
    try:
        result = run("exec-out", "screencap", "-p", device=device, timeout=30, capture=True)
    except (OSError, subprocess.SubprocessError):
        return False
    image = result.stdout or b""
    if result.returncode != 0 or not image.startswith(_PNG_MAGIC):
        return False
    try:
        with open(path, "wb") as fh:
            fh.write(image)
    except OSError:
        return False
    return True
