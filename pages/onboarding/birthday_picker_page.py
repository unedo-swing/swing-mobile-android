import time

from appium.webdriver.common.appiumby import AppiumBy

from config import settings
from core.android_base_page import AndroidBasePage
from locators.onboarding.birthday_picker_locators import BirthdayPickerLocators as L


class BirthdayPickerPage(AndroidBasePage):

    MONTHS = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]

    # A wheel swipe covers a few entries at a time; keep it slow enough that the
    # momentum scroll doesn't overshoot past the value we're hunting for.
    WHEEL_SWIPE_PERCENT = 0.4
    WHEEL_SWIPE_SPEED = 500
    WHEEL_SETTLE = 0.6

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Select birthday dialog not shown"
        self.capture_step("birthday_picker", "Select birthday dialog is visible")

    # ================= wheel plumbing =================
    def _find_now(self, locator):
        self.driver.implicitly_wait(0)
        try:
            found = self.driver.find_elements(*self._resolve(locator))
            return found[0] if found else None
        finally:
            self.driver.implicitly_wait(settings.IMPLICIT_WAIT)

    def _rendered_values(self, wheel_index: int) -> list:
        self.driver.implicitly_wait(0)
        try:
            elements = self.driver.find_elements(
                AppiumBy.XPATH, L.options_in_wheel % wheel_index
            )
            return [e.get_attribute("content-desc") or "" for e in elements]
        finally:
            self.driver.implicitly_wait(settings.IMPLICIT_WAIT)

    def _swipe_wheel(self, wheel_index: int, direction: str):
        wheel = self.find(L.wheel % wheel_index)
        self.driver.execute_script(
            "mobile: swipeGesture",
            {
                "elementId": wheel.id,
                "direction": direction,
                "percent": self.WHEEL_SWIPE_PERCENT,
                "speed": self.WHEEL_SWIPE_SPEED,
            },
        )
        time.sleep(self.WHEEL_SETTLE)

    def _order_key(self, value: str, order: list | None):
        try:
            return order.index(value) if order else int(value)
        except (ValueError, AttributeError):
            return None

    def _direction_towards(self, target: str, wheel_index: int, order: list | None) -> str:
        target_key = self._order_key(target, order)
        keys = [k for k in (self._order_key(v, order) for v in self._rendered_values(wheel_index))
                if k is not None]
        if target_key is None or not keys:
            return "up"
        return "down" if target_key < min(keys) else "up"

    def _select_in_wheel(self, wheel_index: int, value: str, order: list | None = None,
                         max_swipes: int = 15):
        locator = L.option_in_wheel % (wheel_index, value)
        for _ in range(max_swipes):
            element = self._find_now(locator)
            if element is not None:
                element.click()
                time.sleep(self.WHEEL_SETTLE)
                return
            self._swipe_wheel(wheel_index, self._direction_towards(value, wheel_index, order))
        raise AssertionError(
            f"'{value}' not reachable in wheel {wheel_index} after {max_swipes} swipes"
        )

    # ================= action steps =================
    def select_month(self, month: str):
        self._select_in_wheel(L.WHEEL_MONTH, month, order=self.MONTHS)
        self.capture_step("birthday_month", f"Selected month '{month}'")

    def select_day(self, day):
        self._select_in_wheel(L.WHEEL_DAY, str(day))
        self.capture_step("birthday_day", f"Selected day '{day}'")

    def select_year(self, year):
        self._select_in_wheel(L.WHEEL_YEAR, str(year))
        self.capture_step("birthday_year", f"Selected year '{year}'")

    def tap_confirm(self):
        self.click(L.button_confirm)
        self.capture_step("birthday_confirm", "Tapped Confirm")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("birthday_back", "Closed birthday picker")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("birthday_dismiss", "Dismissed birthday picker")

    # ================= scenario =================
    @staticmethod
    def parse_birthdate(birthdate: str) -> tuple:
        from datetime import datetime

        text = (birthdate or "").strip()
        for fmt in ("%d %B %Y", "%d %b %Y"):
            try:
                dt = datetime.strptime(text, fmt)
            except ValueError:
                continue
            return dt.strftime("%B"), str(dt.day), str(dt.year)
        raise ValueError(
            f"birthdate '{birthdate}' is not in 'DD Month YYYY' form (e.g. '02 September 1998')"
        )

    def select_birthday(self, birthdate: str, confirm: bool = True):
        month, day, year = self.parse_birthdate(birthdate)
        self.select_month(month)
        self.select_day(day)
        self.select_year(year)
        if confirm:
            self.tap_confirm()
