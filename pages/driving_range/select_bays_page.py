"""
"How many bays?" page object (Android) — Driving Range.

Opened after "Book driving range". Per-screen STEPS only, each recording
evidence with capture_step. XPaths come from
locators/driving_range/select_bays_locators.py.
"""
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
        """Set the number of bays by tapping + from the default of 1."""
        for _ in range(max(0, count - 1)):
            self.click(L.button_plus)
        self.capture_step("set_bays", f"Set bays = {count}")
