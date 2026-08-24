from core.android_base_page import AndroidBasePage
from locators.tee_time.booking_method_locators import BookingMethodLocators as L


class BookingMethodPage(AndroidBasePage):

    # ================= chooser =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Booking method sheet not shown"
        self.capture_step("booking_method")

    def select_group_booking(self):
        self.click(L.option_group_booking)
        self.capture_step("group_booking")

    def select_standard_booking(self):
        self.click(L.option_standard_booking)
        self.capture_step("standard_booking")

    def tap_continue(self):
        self.click(L.button_continue)
        self.capture_step("booking_continue")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("booking_dismiss")

    # ================= "Booking method info" dialog =================
    def tap_learn_more(self):
        self.click(L.link_learn_more)
        self.capture_step("learn_more")

    def verify_info_dialog(self):
        assert self.is_visible(L.label_info_title, timeout=15), "Booking method info dialog not shown"
        self.capture_step("booking_info")

    def tap_got_it(self):
        self.click(L.button_got_it)
        self.capture_step("got_it")
