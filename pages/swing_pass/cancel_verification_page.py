from core.android_base_page import AndroidBasePage
from locators.swing_pass.cancel_verification_locators import CancelVerificationLocators as L


class CancelVerificationPage(AndroidBasePage):

    def verify_sheet(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), \
            "Cancel verification sheet not shown"
        self.capture_step("cancel_verification")

    def verify_options(self):
        missing = [name for name, locator in (("Continue verification", L.button_continue),
                                              ("Do verification later", L.button_later))
                   if not self.is_visible(locator)]
        self.capture_step("cancel_verification_options", "Both buttons are shown" if not missing
                          else f"missing: {', '.join(missing)}")
        assert not missing, f"Cancel verification button(s) not shown: {missing}"

    def verify_description(self, expected: str = ""):
        description = self.get_description()
        assert description, "No description on the cancel verification sheet"
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
        self.capture_step("cancel_verification_continue")

    def tap_do_later(self):
        self.click(L.button_later)
        self.wait_until_loaded()
        self.capture_step("cancel_verification_later")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("cancel_verification_dismiss")
