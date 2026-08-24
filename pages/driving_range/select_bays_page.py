import re

from core.android_base_page import AndroidBasePage
from locators.driving_range.select_bays_locators import SelectBaysLocators as L


class SelectBaysPage(AndroidBasePage):

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "How many bays sheet not shown"
        self.capture_step("select_bays")

    def verify_confirm_enabled(self):
        assert self.is_enabled(L.button_confirm), "Confirm bays is disabled"
        self.capture_step("bays_confirm_enabled")

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
        self.capture_step("confirm_bays")

    def set_bays(self, count: int):
        for _ in range(max(0, count - 1)):
            self.click(L.button_plus)
        self.capture_step("set_bays", f"Set bays = {count}")
    
    def verify_max_bays(self, max_bays: str):
        assert self.is_visible(L.toaster_maximum_bay % max_bays)
        self.capture_step(f"Maximum Bays : {max_bays}", f"Maximum Bays : {max_bays}")
