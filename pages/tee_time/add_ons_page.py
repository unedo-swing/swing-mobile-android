"""
Select add-ons page object (Android) — Tee Time.

The bottom sheet for adding extras (Stick, Shoes, Coach, ...) to a player, opened
from the booking confirmation. Per-screen STEPS only, each recording evidence
with capture_step. XPaths come from locators/tee_time/add_ons_locators.py.
"""
from core.android_base_page import AndroidBasePage
from locators.tee_time.add_ons_locators import AddOnsLocators as L


class AddOnsPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Select add-ons sheet not shown"
        self.capture_step("select_addons", "Select add-ons sheet is visible")

    def verify_addon(self, name: str):
        assert self.is_visible(L.addon_row_by_name % name), f"Add-on '{name}' not shown"
        self.capture_step("addon_row", f"Add-on shown: {name}")

    def get_addon_count(self, name: str) -> int:
        """Read the current quantity of an add-on (last line of its content-desc)."""
        desc = self.find(L.addon_row_by_name % name).get_attribute("content-desc") or ""
        last = desc.split("\n")[-1].strip()
        return int(last) if last.isdigit() else 0

    # ================= action steps =================
    def increment(self, name: str, times: int = 1):
        """Tap the + stepper for an add-on ``times`` times, e.g. 'Stick'."""
        for _ in range(times):
            self.click(L.addon_plus_by_name % name)
        self.capture_step("addon_plus", f"Incremented '{name}' x{times}")

    def decrement(self, name: str, times: int = 1):
        for _ in range(times):
            self.click(L.addon_minus_by_name % name)
        self.capture_step("addon_minus", f"Decremented '{name}' x{times}")

    def is_save_enabled(self) -> bool:
        return self.is_enabled(L.button_save)

    def tap_save(self):
        self.click(L.button_save)
        self.capture_step("save_addons", "Tapped Save add-ons")

    def tap_cancel(self):
        self.click(L.button_cancel)
        self.capture_step("cancel_addons", "Tapped Cancel")
