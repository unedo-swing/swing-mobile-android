from core.android_base_page import AndroidBasePage
from locators.swing_pass.pending_verification_locators import PendingVerificationLocators as L


class PendingVerificationPage(AndroidBasePage):

    def is_shown(self, timeout: int = 10) -> bool:
        return self.is_visible(L.label_title, timeout=timeout, log=False)

    def verify_sheet(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), \
            "Pending verification sheet not shown"
        assert self.is_visible(L.button_continue), \
            "No 'Continue to verification' button on the sheet"
        self.capture_step("pending_verification")

    def verify_not_shown(self):
        assert not self.is_shown(timeout=5), \
            "Pending verification sheet is shown but the Pass should be verified"
        self.capture_step("pending_verification_absent", "No pending verification sheet")

    def verify_description(self, expected: str = ""):
        description = self.get_description()
        assert description, "No description on the pending verification sheet"
        if expected:
            assert expected in description, \
                f"Description is '{description}', expected '{expected}'"

    def _desc(self, locator) -> str:
        return self.scroll_and_find(locator).get_attribute("content-desc") or ""

    def get_title(self) -> str:
        return self._desc(L.label_title)

    def get_description(self) -> str:
        return self._desc(L.label_description)

    def tap_continue_verification(self):
        self.click(L.button_continue)
        self.wait_until_loaded()
        self.capture_step("pending_verification_continue")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("pending_verification_dismiss")

    def dismiss_if_shown(self):
        if not self.is_shown(timeout=5):
            return False
        self.dismiss()
        return True
