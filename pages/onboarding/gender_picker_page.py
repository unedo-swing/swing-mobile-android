from core.android_base_page import AndroidBasePage
from locators.onboarding.gender_picker_locators import GenderPickerLocators as L


class GenderPickerPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.option_not_specified, timeout=20), "Gender sheet not shown"
        self.capture_step("gender_picker", "Gender sheet is visible")

    # ================= action steps =================
    def select_gender(self, gender: str):
        self.click(L.option_by_label % gender)
        self.capture_step("gender_selected", f"Selected gender '{gender}'")

    def tap_confirm(self):
        self.click(L.button_confirm)
        self.capture_step("gender_confirm", "Confirmed gender")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("gender_dismiss", "Dismissed gender sheet")
