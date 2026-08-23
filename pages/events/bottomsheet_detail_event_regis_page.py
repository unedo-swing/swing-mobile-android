from core.android_base_page import AndroidBasePage
from locators.events.registration_confirmation_locators import RegistrationConfirmationLocators as R
from locators.events.bottomsheet_detail_event_regis_locators import (
    BottomsheetDetailEventRegisLocators as L,
)


class BottomsheetDetailEventRegisPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.title_header, timeout=20), (
            "Register bottom sheet not shown"
        )
        self.capture_step("reg_bottomsheet", "Register-option bottom sheet shown")

    # ================= action steps =================
    def choose_registration_type(self, reg_type: str):
        self.click(L.button_option_registration % reg_type)
        if self.is_visible(R.button_invite_friends) :
            self.press_back()
        self.capture_step("reg_choose_type", f"Chose registration type: {reg_type}")

    def tap_details(self):
        self.click(L.button_details)
        self.capture_step("reg_tap_details", "Tapped Details on register bottom sheet")
