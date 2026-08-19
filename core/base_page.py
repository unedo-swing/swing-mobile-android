import os
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy

from config import settings
from utils import allure_reporter
from utils.pdf_reporter import humanize_step


class BasePage:
    def __init__(self, driver, reporter=None):
        """
        :param driver:   the Appium driver
        :param reporter: optional PDFReporter. When None, evidence steps are
                         still logged/screenshotted but no PDF is produced.
        """
        self.driver = driver
        self.reporter = reporter
        self.wait = WebDriverWait(driver, settings.EXPLICIT_WAIT)

    def _resolve(self, locator) -> tuple:
        """
        Normalise a locator into a ``(by, value)`` tuple.

        A plain string (the common case) is treated as an XPath. A ready-made
        ``(by, value)`` tuple is passed through unchanged, so you can still use
        UiAutomator/accessibility-id strategies when you want to.
        """
        if isinstance(locator, str):
            return (AppiumBy.XPATH, locator)
        return locator

    # ------------------------------------------------------------------ #
    # Step logging — with `pytest -s` this prints the action + the xpath used
    # ------------------------------------------------------------------ #
    def _log(self, action: str, locator=None):
        if locator is not None:
            print(f"[step] {action:<14} xpath: {self._resolve(locator)[1]}")
        else:
            print(f"[step] {action}")

    # ------------------------------------------------------------------ #
    # Finding elements
    # ------------------------------------------------------------------ #
    def find(self, locator):
        """Wait until present and return a single element."""
        self._log("find", locator)
        return self.wait.until(EC.presence_of_element_located(self._resolve(locator)))

    def find_all(self, locator):
        """Return all matching elements (may be empty)."""
        self._log("find_all", locator)
        return self.driver.find_elements(*self._resolve(locator))

    def wait_visible(self, locator):
        self._log("wait_visible", locator)
        return self.wait.until(EC.visibility_of_element_located(self._resolve(locator)))

    def wait_clickable(self, locator):
        self._log("wait_clickable", locator)
        return self.wait.until(EC.element_to_be_clickable(self._resolve(locator)))

    def is_visible(self, locator, timeout: int = 5, log: bool = True) -> bool:
        """True if the element becomes visible within ``timeout`` seconds.

        ``log`` can be set False by tight polling loops to avoid log spam.
        """
        if log:
            self._log("is_visible", locator)
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self._resolve(locator))
            )
            return True
        except TimeoutException:
            return False

    # ------------------------------------------------------------------ #
    # Interactions  (each inlines its own wait so it logs exactly once)
    # ------------------------------------------------------------------ #
    def click(self, locator):
        self._log("click", locator)
        self.wait.until(EC.element_to_be_clickable(self._resolve(locator))).click()

    def type_text(self, locator, text: str, clear: bool = True):
        self._log("type_text", locator)
        element = self.wait.until(EC.visibility_of_element_located(self._resolve(locator)))
        # Flutter fields must be focused before they accept input, otherwise the
        # value never registers and dependent widgets (e.g. an enabled button)
        # don't update. Tapping the field first fixes this.
        element.click()
        if clear:
            element.clear()
        element.send_keys(text)

    def fill(self, locator, text: str, clear: bool = True):
        self.type_text(locator, text, clear)
        self.hide_keyboard()

    def type_text_verified(self, locator, text: str, clear: bool = True,
                           retries: int = 2, settle: float = 0.3) -> None:
        """type_text, but re-reads the field afterward and retries (re-focus +
        clear + resend) if the value didn't fully register.

        Numeric fields (phone numbers) are the ones most exposed to a Flutter
        input-connection race: switching to a numeric keypad from whatever
        keyboard the previous field used takes measurably longer to attach
        than staying on the same IME, and a digits-only input formatter can
        reject a bulk send_keys write that arrives before the connection is
        ready — silently dropping some or all of the keystrokes. Re-focusing
        and resending on mismatch absorbs that race instead of leaving a bad
        value in the field.
        """
        last_actual = None
        for attempt in range(1, retries + 1):
            self.type_text(locator, text, clear)
            time.sleep(settle)
            element = self.wait.until(EC.visibility_of_element_located(self._resolve(locator)))
            last_actual = element.get_attribute("text") or ""
            if last_actual == text:
                return
            self._log(
                f"type_text_verified: attempt {attempt}/{retries} got "
                f"{last_actual!r}, expected {text!r} — retrying"
            )
        raise AssertionError(
            f"type_text_verified: field never matched after {retries} attempt(s) — "
            f"got {last_actual!r}, expected {text!r} ({self._resolve(locator)[1]})"
        )

    def fill_verified(self, locator, text: str, clear: bool = True, retries: int = 2) -> None:
        self.type_text_verified(locator, text, clear, retries)
        self.hide_keyboard()

    def get_text(self, locator) -> str:
        self._log("get_text", locator)
        return self.wait.until(EC.visibility_of_element_located(self._resolve(locator))).text

    def is_enabled(self, locator) -> bool:
        """True when the element reports enabled='true'."""
        self._log("is_enabled", locator)
        return self.wait.until(
            EC.presence_of_element_located(self._resolve(locator))
        ).get_attribute("enabled") == "true"

    # ------------------------------------------------------------------ #
    # Gestures — overridden per platform where behaviour differs
    # ------------------------------------------------------------------ #
    def hide_keyboard(self):
        """No-op by default; platform bases override this."""
        pass

    # ------------------------------------------------------------------ #
    # Evidence
    # ------------------------------------------------------------------ #
    def take_screenshot(self, name: str) -> str:
        """Save a screenshot to reports/screenshots and return its path."""
        os.makedirs(settings.SCREENSHOTS_DIR, exist_ok=True)
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        path = os.path.join(
            settings.SCREENSHOTS_DIR, f"{safe}_{int(time.time() * 1000)}.png"
        )
        self.driver.save_screenshot(path)
        return path

    def capture_step(self, title: str, description: str = "", data=None, compare=None):
        print(f"[STEP] {title}" + (f" — {description}" if description else ""))
        path = self.take_screenshot(title)
        if self.reporter is not None:
            self.reporter.add_step(
                title=title, description=description, screenshot=path,
                data=data, compare=compare,
            )
        # Same step, second destination: the Allure timeline. No-op unless the
        # run was started with --allure (see utils/allure_reporter.py).
        with allure_reporter.step(f"{title} — {description}" if description else title):
            allure_reporter.attach_png(path, humanize_step(title))
            allure_reporter.attach_step_data(data, compare)
        return path

    def wait_for(self, times: int):
        time.sleep(times)
