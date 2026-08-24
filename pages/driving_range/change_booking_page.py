from core.android_base_page import AndroidBasePage
from locators.driving_range.change_booking_locators import ChangeBookingLocators as L


class DrivingRangeChangeBookingPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_change_booking, timeout=20), "Change Booking screen not shown"
        self.capture_step("dr_change_booking")

    # ================= tabs =================
    def select_reschedule_tab(self):
        self.click(L.tab_reschedule)
        self.capture_step("dr_change_tab_reschedule")

    def select_cancellation_tab(self):
        self.click(L.tab_cancellation)
        self.capture_step("dr_change_tab_cancellation")

    def is_reschedule_tab_selected(self) -> bool:
        el = self.find_anywhere(L.tab_reschedule)
        return el is not None and el.get_attribute("selected") == "true"

    # ================= reschedule tab =================
    def verify_reschedule_policy(self):
        assert self.is_visible_after_scroll(L.label_reschedule_policy, timeout=15), \
            "Reschedule policy section not shown"
        self.capture_step("dr_reschedule_policy")

    def get_policy_text(self) -> str:
        return self.scroll_and_find(L.label_policy_text).get_attribute("content-desc") or ""

    def get_booking_datetime(self) -> str:
        return self.scroll_and_find(L.label_booking_datetime).get_attribute("content-desc") or ""

    def get_reschedule_now_text(self) -> str:
        el = self.find_anywhere(L.label_reschedule_now)
        return "" if el is None else (el.get_attribute("content-desc") or "")

    # ================= cancellation tab =================
    def is_cancellation_tab_selected(self) -> bool:
        el = self.find_anywhere(L.tab_cancellation)
        return el is not None and el.get_attribute("selected") == "true"

    def verify_cancellation_policy(self):
        assert self.is_visible_after_scroll(L.label_cancellation_policy, timeout=15), \
            "Cancellation policy section not shown"
        self.capture_step("dr_cancellation_policy")

    def get_refund_tier(self, starts_with: str) -> str:
        return self.scroll_and_find(L.refund_tier_by_text % starts_with).get_attribute("content-desc") or ""

    def get_cancel_now_text(self) -> str:
        el = self.find_anywhere(L.label_cancel_now)
        return "" if el is None else (el.get_attribute("content-desc") or "")

    def tap_continue_cancel(self):
        self.click(L.button_continue_cancel)
        self.capture_step("dr_continue_cancel")

    # ================= actions =================
    def is_continue_enabled(self) -> bool:
        return self.is_enabled(L.button_continue_reschedule)

    def tap_continue_reschedule(self):
        self.click(L.button_continue_reschedule)
        self.capture_step("dr_continue_reschedule")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("dr_change_booking_back")
