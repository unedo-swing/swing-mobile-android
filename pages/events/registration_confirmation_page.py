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

    def tap_edit_registration_type(self, reg_type: str):
        self.click(L.button_change_event_type % reg_type)
        self.capture_step("edit_regis_type", "Tapped 'edit registration type'")

    def verify_registration_type_inside_confirmation_page(self, reg_type: str):
        assert self.is_visible(L.button_change_event_type % reg_type),  (f"registation type '{reg_type}' not changed")

    def verify_remove_player_count(self, expected: int):
        self.scroll_to_element(L.button_add_player)
        actual = len(self.find_all(L.button_remove_player_all))
        assert actual == expected, f"Remove player: expected {expected}, got {actual}"
        self.capture_step("count_remove", f"Remove player count = {actual}")

    def tap_remove_player(self, player_num: int):
        self.click(L.button_remove_player_specific % player_num)
        self.capture_step("remove_player_type", "Tapped 'remove player button'")

    def verify_bottomsheet_remove_player(self):
        assert self.is_visible(L.title_header_bottomsheet_remove_friends), ( "Title header inside bottomsheet remove player not found" )
        assert self.is_visible(L.button_remove_player_bottomsheet), ( "Button remove player inside bottomsheet remove player not found" )
        assert self.is_visible(L.button_keep_player_bottomsheet), ( "Button keep player inside bottomsheet remove player not found" )
        self.capture_step("bottomsheet_remove_player", "bottomsheet remove player opened")

    def tap_confirm_remove_player(self):
        self.click(L.button_remove_player_bottomsheet)
        self.capture_step("confirm_remove_player", "Tapped 'confirm remove player button'")

    def tap_confirm_keep_player(self):
        self.click(L.button_keep_player_bottomsheet)
        self.capture_step("confirm_keep_player", "Tapped 'confirm keep player button'")