from core.android_base_page import AndroidBasePage
from locators.swing_pass.verification_locators import VerificationLocators as L


class VerificationPage(AndroidBasePage):

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), \
            "Swing Pass verification screen not shown"
        self.capture_step("verification")

    def verify_content(self):
        missing = [name for name, locator in (("headline", L.label_headline),
                                              ("description", L.label_description),
                                              ("full name label", L.label_full_name),
                                              ("full name field", L.input_full_name),
                                              ("photo section", L.section_photo),
                                              ("Open camera button", L.button_open_camera),
                                              ("Submit verification button", L.button_submit))
                   if not self.is_visible_after_scroll(locator)]
        self.capture_step("verification_content", "All verification elements are shown"
                          if not missing else f"missing: {', '.join(missing)}")
        assert not missing, f"Verification element(s) not shown: {missing}"

    def verify_full_name(self, expected: str):
        actual = self.get_full_name()
        assert actual == expected, f"Full name is '{actual}', expected '{expected}'"

    def verify_submit_enabled(self, enabled: bool = True):
        actual = self.is_submit_enabled()
        assert actual == enabled, (
            f"'Submit verification' is {'enabled' if actual else 'disabled'}, "
            f"expected {'enabled' if enabled else 'disabled'}"
        )
        self.capture_step("verification_submit_state",
                          f"Submit is {'enabled' if actual else 'disabled'}")

    def verify_photo_hint(self, expected: str = ""):
        hint = self.get_photo_hint()
        assert hint, "No 'Take a picture of yourself' section on the screen"
        if expected:
            assert expected in hint, f"Photo hint is '{hint}', expected '{expected}'"

    def _desc(self, locator) -> str:
        return self.scroll_and_find(locator).get_attribute("content-desc") or ""

    def get_headline(self) -> str:
        return self._desc(L.label_headline)

    def get_description(self) -> str:
        return self._desc(L.label_description)

    def get_photo_hint(self) -> str:
        element = self.find_anywhere(L.section_photo)
        return element.get_attribute("content-desc") or "" if element is not None else ""

    def get_full_name(self) -> str:
        return self.scroll_and_find(L.input_full_name).get_attribute("text") or ""

    def is_submit_enabled(self) -> bool:
        return self.is_enabled(L.button_submit)

    def set_full_name(self, name: str):
        self.fill_verified(L.input_full_name, name)
        self.capture_step("verification_full_name", f"Full name set to '{name}'")

    def open_camera(self):
        self.click(L.button_open_camera)
        self.capture_step("verification_open_camera")

    def submit(self):
        assert self.is_submit_enabled(), \
            "'Submit verification' is disabled — name and photo are required first"
        self.click(L.button_submit)
        self.wait_until_loaded()
        self.capture_step("verification_submit")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("verification_back")
