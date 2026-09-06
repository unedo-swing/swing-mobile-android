import time
from core.android_base_page import AndroidBasePage
from locators.multisport.booking_confirmation_page_locators import (
    BookingConfirmationPageLocators as L,
)


class BookingConfirmationPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.header_booking_confirmation_page,
                               timeout=20),             "Booking confirmation page not shown"
        self.capture_step("booking_confirmation_screen",
                          "Booking confirmation screen is visible")

    def verify_total_player(self):
        self.wait_until_loaded()
        self.scroll_to_element(L.text_all_player_total)
        actual = len(self.find_all(L.text_all_player_total))
        assert actual >= 1, f"Player: expected more than 1, got {actual}"
        self.capture_step("count_player", f"Player count = {actual}")
        time.sleep(3)

    # ================= open payment =================
    def open_payment_method(self):
        self.click(L.button_select_payment)
        self.capture_step("open_payment_method", "Tapped Select payment")

    def click_add_player(self):
        self.click(L.button_add_player)
        self.capture_step("open_bottomsheet_add_player", "Tapped add player")

    def delete_player(self):
        self.scroll_to_element(L.text_all_player_total)
        before = len(self.find_all(L.text_all_player_total))
        self.click(L.button_delete_player % (before * 2))
        after = len(self.find_all(L.text_all_player_total))
        assert before > after
        self.capture_step("success_remove_player", "Player removed")

    def tap_pay_now(self):
        self.click(L.button_pay_now)
        self.capture_step("reg_pay_now", "Tapped 'Pay now'")

