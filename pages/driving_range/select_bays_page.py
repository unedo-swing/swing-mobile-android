import re

from core.android_base_page import AndroidBasePage
from locators.driving_range.select_bays_locators import SelectBaysLocators as L


class SelectBaysPage(AndroidBasePage):

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "How many bays sheet not shown"
        self.capture_step("select_bays", "How many bays sheet is visible")

    def verify_confirm_enabled(self):
        assert self.is_enabled(L.button_confirm), "Confirm bays is disabled"
        self.capture_step("bays_confirm_enabled", "Confirm bays is enabled")

    def increment(self, times: int = 1):
        for _ in range(times):
            self.click(L.button_plus)
        self.capture_step("bays_plus", f"Incremented bays x{times}")

    def decrement(self, times: int = 1):
        for _ in range(times):
            self.click(L.button_minus)
        self.capture_step("bays_minus", f"Decremented bays x{times}")

    def confirm(self):
        self.click(L.button_confirm)
        self.capture_step("confirm_bays", "Tapped Confirm bays")

    def set_bays(self, count: int):
        for _ in range(max(0, count - 1)):
            self.click(L.button_plus)
        self.capture_step("set_bays", f"Set bays = {count}")
    
    # ================= minimum balls toaster =================
    @staticmethod
    def parse_minimum_balls(message: str) -> dict:
        """Pull the three figures out of "Minimum 4000 balls for booking with
        2 times and 20 bays". They are read positionally, so the parse survives
        the wording changing around them."""
        numbers = re.findall(r"[\d][\d,.]*", message or "")
        fields = ("balls", "times", "bays")
        parsed = {field: "" for field in fields}
        for field, value in zip(fields, numbers):
            parsed[field] = value
        parsed["message"] = message or ""
        return parsed

    def get_minimum_balls_message(self) -> str:
        """The toaster's text, or '' when it is not on screen."""
        if not self.is_visible(L.toaster_minimum_balls, timeout=5, log=False):
            return ""
        return self.find(L.toaster_minimum_balls).get_attribute("content-desc") or ""

    def verify_minimum_balls(self, balls: str = "", times: str = "", bays: str = ""):
        message = self.get_minimum_balls_message()
        assert message, "Minimum balls toaster not shown"
        parsed = self.parse_minimum_balls(message)
        expected = {"balls": balls, "times": times, "bays": bays}
        mismatches = {
            field: (want, parsed[field])
            for field, want in expected.items()
            if want and str(want).strip() != parsed[field]
        }
        assert not mismatches, (
            "Minimum balls toaster does not match:\n"
            + "\n".join(
                f"  {field}: expected '{want}' but toaster reads '{got}'"
                for field, (want, got) in mismatches.items()
            )
            + f"\n  toaster: '{message}'"
        )
        self.capture_step("bays_minimum_balls", message, data=parsed)
        return parsed

    def verify_no_minimum_balls(self):
        assert not self.is_visible(L.toaster_minimum_balls, timeout=2), \
            "Minimum balls toaster is shown"
        self.capture_step("bays_no_minimum_balls", "No minimum balls toaster")

    def verify_max_bays(self, max_bays: str):
        assert self.is_visible(L.toaster_maximum_bay % max_bays)
        self.capture_step(f"Maximum Bays : {max_bays}", f"Maximum Bays : {max_bays}")
