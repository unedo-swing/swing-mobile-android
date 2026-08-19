from core.android_base_page import AndroidBasePage
from locators.swing_pass.cancel_confirmation_locators import CancelConfirmationLocators as L


class CancelConfirmationPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_sheet(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), \
            "Cancellation confirmation sheet not shown"
        self.capture_step("cancel_confirm", "Cancellation confirmation sheet is visible")

    def verify_options(self):
        missing = [name for name, locator in (("Stay with Swing Pass", L.button_stay),
                                              ("Proceed to cancel", L.button_proceed))
                   if not self.is_visible(locator)]
        self.capture_step("cancel_confirm_options", "Both buttons are shown" if not missing
                          else f"missing: {', '.join(missing)}")
        assert not missing, f"Button(s) not shown: {missing}"

    def verify_savings_amount(self, expected: str):
        actual = self.get_savings_amount()
        assert actual == expected, f"Sheet quotes '{actual}', expected '{expected}'"

    # ================= reading =================
    @staticmethod
    def parse_savings_amount(desc: str) -> str:
        text = desc or ""
        if "Rp." not in text:
            return ""
        amount = text.split("Rp.", 1)[1]
        # the amount runs up to the full stop that ends the first sentence
        return ("Rp." + amount.split(".", 1)[0]).strip()

    def get_title(self) -> str:
        return self.find(L.label_title).get_attribute("content-desc") or ""

    def get_savings_amount(self) -> str:
        amount = self.parse_savings_amount(self.get_title())
        self.capture_step("cancel_confirm_savings", f"Sheet quotes {amount}")
        return amount

    # ================= action steps =================
    def tap_stay(self):
        self.click(L.button_stay)
        self.capture_step("cancel_confirm_stay", "Tapped Stay with Swing Pass")

    def tap_proceed(self):
        self.click(L.button_proceed)
        self.capture_step("cancel_confirm_proceed", "Tapped Proceed to cancel")

    def tap_close(self):
        self.click(L.button_close)
        self.capture_step("cancel_confirm_close", "Closed the cancellation sheet")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("cancel_confirm_dismiss", "Dismissed the cancellation sheet")
