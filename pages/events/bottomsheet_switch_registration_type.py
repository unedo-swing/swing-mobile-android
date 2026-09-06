from core.android_base_page import AndroidBasePage
from locators.events.bottomsheet_switch_event_type_locators import BottomsheetSwitchEventTypeLocators as L
from locators.events.registration_confirmation_locators import RegistrationConfirmationLocators as R

class BottomsheetSwitchRegistrationType(AndroidBasePage):
        # ================= verify steps =================
    def verify_screen_switch_bottomsheet(self):
        assert self.is_visible(L.title_header, timeout=20), (
            "Switch bottomsheet not shown"
        )
        self.capture_step("switch_bottomsheet", "Switch bottomsheet shown")

    # ================= action steps =================
    def choose_switch_registration_type(self):
        self.click(L.button_switch_to)
        if self.is_visible(R.button_invite_friends) :
            self.press_back()
        self.capture_step("Switch_regis", "Switch registration type")