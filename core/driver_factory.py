"""
Creates the Appium Android driver.

The rest of the framework never touches capabilities directly — it just asks
the factory for a driver.
"""
from appium import webdriver

from config import settings
from config.capabilities import android_options


def create_driver():
    """Return a started Appium Android driver."""
    driver = webdriver.Remote(
        command_executor=settings.APPIUM_SERVER_URL,
        options=android_options(),
    )
    driver.implicitly_wait(settings.IMPLICIT_WAIT)
    return driver
