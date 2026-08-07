"""
Driving Range Booking rescheduled page object (Android).

The success screen shown after confirming a reschedule ("Booking rescheduled").
Shows the range/booking, the original vs new date & time, the total, the payment
method and Finish / See booking details actions.

Flutter app — values surface through ``content-desc``. The Total / Payment rows
are a label View next to a value View (read via the label's sibling).
XPaths come from locators/driving_range/reschedule_success_locators.py.
"""
from core.android_base_page import AndroidBasePage
from locators.driving_range.reschedule_success_locators import (
    DrivingRangeRescheduleSuccessLocators as L,
)


class DrivingRangeRescheduleSuccessPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        # the reschedule payment settles behind a spinner before this draws
        self.wait_until_loaded(timeout=120)
        assert self.is_visible(L.label_title, timeout=30), "Booking rescheduled screen not shown"
        self.capture_step("dr_reschedule_success", "Booking rescheduled screen is visible")

    def verify_range_name(self, name: str):
        assert self.is_visible_after_scroll(L.label_range_name % name), f"Range '{name}' not shown"
        self.capture_step("dr_reschedule_success_range", f"Range shown: {name}")

    def verify_booking_id(self) -> str:
        booking_id = self.get_booking_id()
        assert booking_id.startswith("Booking #"), f"Booking id not shown, got '{booking_id}'"
        self.capture_step("dr_reschedule_success_id", booking_id)
        return booking_id

    # ================= readers =================
    def _value(self, label: str) -> str:
        return self.scroll_and_find(L.value_by_label % label).get_attribute("content-desc") or ""

    def _read(self, getter) -> str:
        try:
            return getter()
        except Exception:
            return ""

    def get_booking_id(self) -> str:
        """e.g. 'Booking #A38OO'."""
        return self.scroll_and_find(L.label_booking_id).get_attribute("content-desc") or ""

    def get_change_block(self) -> str:
        """The original/new date & time block, e.g.
        'Original date & time\\n18:00, 13 Aug 2026\\nNew date & time\\n22:00, 5 Aug 2026'."""
        return self.scroll_and_find(L.label_change_block).get_attribute("content-desc") or ""

    def get_total(self) -> str:
        return self._value("Total")

    def get_payment_method(self) -> str:
        return self._value("Payment method")

    def get_summary(self) -> dict:
        self.scroll_to_top()
        summary = {
            "booking_id": self._read(self.get_booking_id),
            "change": self._read(self.get_change_block),
            "total": self._read(self.get_total),
            "payment_method": self._read(self.get_payment_method),
        }
        self.capture_step("dr_reschedule_success_summary", data=summary)
        return summary

    def verify_summary(self, booking_id=None, total=None, payment_method=None):
        self.capture_step(
            "dr_reschedule_success_verify",
            f"Booking={self.get_booking_id()} | Total={self.get_total()} | "
            f"Payment={self.get_payment_method()}",
        )
        if booking_id is not None:
            assert booking_id in self.get_booking_id()
        if total is not None:
            assert total in self.get_total()
        if payment_method is not None:
            assert payment_method.casefold() in self.get_payment_method().casefold()

    # ================= action steps =================
    def tap_finish(self):
        self.click(L.button_finish)
        self.capture_step("dr_reschedule_finish", "Tapped Finish")

    def tap_see_booking_details(self):
        self.click(L.button_see_details)
        self.capture_step("dr_reschedule_see_details", "Tapped See booking details")
