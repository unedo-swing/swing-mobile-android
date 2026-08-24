from core.android_base_page import AndroidBasePage
from locators.driving_range.cancel_success_locators import CancelSuccessLocators as L


class DrivingRangeCancelSuccessPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        # the cancellation settles behind a spinner before this draws
        self.wait_until_loaded(timeout=120)
        assert self.is_visible(L.label_title, timeout=30), "Booking cancelled screen not shown"
        self.capture_step("dr_cancel_success")

    def verify_range_name(self, name: str):
        assert self.is_visible_after_scroll(L.label_range_name % name), f"Range '{name}' not shown"
        self.capture_step("dr_cancel_success_range", f"Range shown: {name}")

    def verify_booking_id(self) -> str:
        booking_id = self.get_booking_id()
        assert booking_id.startswith("Booking #"), f"Booking id not shown, got '{booking_id}'"
        self.capture_step("dr_cancel_success_id", booking_id)
        return booking_id

    # ================= readers =================
    def _value(self, label: str) -> str:
        return self.scroll_and_find(L.value_by_label % label).get_attribute("content-desc") or ""

    def get_booking_id(self) -> str:
        return self.scroll_and_find(L.label_booking_id).get_attribute("content-desc") or ""

    def get_cancellation_date_time(self) -> str:
        return self._value("Cancellation date & time")

    def get_total_refunded(self) -> str:
        return self.scroll_and_find(L.value_total_refunded).get_attribute("content-desc") or ""

    def get_refund_process_note(self) -> str:
        el = self.find_anywhere(L.label_refund_process)
        return "" if el is None else (el.get_attribute("content-desc") or "")

    def get_summary(self) -> dict:
        self.scroll_to_top()
        summary = {
            "booking_id": self.get_booking_id(),
            "cancellation_date_time": self.get_cancellation_date_time(),
            "total_refunded": self.get_total_refunded(),
        }
        self.capture_step("dr_cancel_success_summary", data=summary)
        return summary

    # ================= action steps =================
    def tap_finish(self):
        self.click(L.button_finish)
        self.capture_step("dr_cancel_finish")

    def tap_see_cancellation_details(self):
        self.click(L.button_see_details)
        self.capture_step("dr_cancel_see_details")
