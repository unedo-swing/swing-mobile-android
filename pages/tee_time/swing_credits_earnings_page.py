import re

from core.android_base_page import AndroidBasePage
from locators.tee_time.swing_credits_earnings_locators import SwingCreditsEarningsLocators as L


class SwingCreditsEarningsPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Swing Credits earnings dialog not shown"
        self.capture_step("credits_earnings", "Swing Credits earnings dialog is visible")

    def get_player_credit(self, name: str) -> str:
        desc = self.find(L.player_credit_by_name % name).get_attribute("content-desc") or ""
        m = re.search(r"\+[\d.,]+", desc)
        return m.group(0) if m else ""

    def get_player_credit_line(self, name: str) -> str:
        return self.find(L.player_credit_by_name % name).get_attribute("content-desc") or ""

    # ================= action steps =================
    def tap_got_it(self):
        self.click(L.button_got_it)
        self.capture_step("credits_got_it", "Tapped Got it! on Swing Credits earnings")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("credits_dismiss", "Dismissed Swing Credits earnings dialog")
