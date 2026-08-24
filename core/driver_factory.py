from appium import webdriver

from config import settings
from config.capabilities import android_options


def create_driver():
    driver = webdriver.Remote(
        command_executor=settings.APPIUM_SERVER_URL,
        options=android_options(),
    )
    driver.implicitly_wait(settings.IMPLICIT_WAIT)
    return driver
