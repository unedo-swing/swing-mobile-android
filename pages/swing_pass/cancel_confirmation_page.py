from core.android_base_page import AndroidBasePage
from locators.swing_pass.cancel_confirmation_locators import CancelConfirmationLocators as L


class CancelConfirmationPage(AndroidBasePage):

    def verify_sheet(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), \
            "Cancellation confirmation sheet not shown"
        self.capture_step("cancel_confirm")

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

    @staticmethod
    def parse_savings_amount(desc: str) -> str:
        text = desc or ""
        if "Rp." not in text:
            return ""
        amount = text.split("Rp.", 1)[1]
        return ("Rp." + amount.split(".", 1)[0]).strip()

    def get_title(self) -> str:
        return self.find(L.label_title).get_attribute("content-desc") or ""

    def get_savings_amount(self) -> str:
        amount = self.parse_savings_amount(self.get_title())
        self.capture_step("cancel_confirm_savings", f"Sheet quotes {amount}")
        return amount

    def tap_stay(self):
        self.click(L.button_stay)
        self.capture_step("cancel_confirm_stay")

    def tap_proceed(self):
        self.click(L.button_proceed)
        self.capture_step("cancel_confirm_proceed")

    def tap_close(self):
        self.click(L.button_close)
        self.capture_step("cancel_confirm_close")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("cancel_confirm_dismiss")
