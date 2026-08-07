from core.android_base_page import AndroidBasePage
from locators.tee_time.redeem_swing_credits_locators import RedeemSwingCreditsLocators as L


class RedeemSwingCreditsPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.input_code, timeout=20), "Redeem Swing Credits sheet not shown"
        self.capture_step("redeem_swing_credits", "Redeem Swing Credits sheet is visible")

    def is_redeem_enabled(self) -> bool:
        return self.is_enabled(L.button_redeem)

    # ================= action steps =================
    def enter_code(self, code: str):
        self.fill(L.input_code, code)
        self.capture_step("redeem_code", f"Entered code '{code}'")

    def tap_redeem(self):
        self.click(L.button_redeem)
        self.capture_step("tap_redeem", "Tapped Redeem Swing Credits")

    def redeem(self, code: str):
        """Enter a code and submit in one step."""
        self.enter_code(code)
        self.tap_redeem()

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("redeem_back", "Tapped back")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("redeem_dismiss", "Dismissed Redeem Swing Credits sheet")
