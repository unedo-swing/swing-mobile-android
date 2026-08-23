from core.android_base_page import AndroidBasePage
from locators.events.registration_confirmation_locators import (
    RegistrationConfirmationLocators as L,
)


class RegistrationConfirmationPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.title_header, timeout=20), (
            "Registration confirmation not shown"
        )
        self.capture_step("reg_confirm", "Registration confirmation screen shown")

    def verify_event_title(self, name: str):
        assert self.is_visible(L.text_title_event % name, timeout=20), (
            f"Event title '{name}' not shown on confirmation"
        )
        self.capture_step("reg_event_title", f"Event title shown: {name}")

    def verify_payment_selected(self, method: str):
        assert self.is_visible(L.button_change_payment % method, timeout=20), (
            f"Payment '{method}' not selected"
        )
        self.capture_step("reg_payment", f"Payment method selected: {method}")

    # ================= action steps =================
    def tap_add_player(self):
        self.click(L.button_add_player)
        self.capture_step("reg_tap_add_player", "Tapped 'Add a player'")

    def tap_select_payment(self):
        self.click(L.button_select_payment)
        self.capture_step("reg_tap_select_payment", "Tapped 'Select payment'")

    def tap_pay_now(self):
        self.click(L.button_pay_now)
        self.capture_step("reg_pay_now", "Tapped 'Pay now'")
