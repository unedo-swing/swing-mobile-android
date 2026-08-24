from core.android_base_page import AndroidBasePage
from locators.tee_time.switch_group_booking_locators import SwitchGroupBookingLocators as L


class SwitchGroupBookingPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Switch to group booking prompt not shown"
        self.capture_step("switch_group_booking")

    def is_shown(self) -> bool:
        return self.is_visible(L.label_title, timeout=10)

    # ================= action steps =================
    def switch_to_group(self):
        self.click(L.button_switch_to_group)
        self.capture_step("switch_to_group")

    def keep_standard(self):
        self.click(L.button_keep_standard)
        self.capture_step("keep_standard")

    def tap_learn_more(self):
        self.click(L.link_learn_more)
        self.capture_step("learn_more")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("switch_dismiss")
