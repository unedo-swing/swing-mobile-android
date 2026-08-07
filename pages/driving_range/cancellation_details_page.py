"""
Driving Range Cancellation details page object (Android).

Opened from the Booking cancelled screen ('See cancellation details') or My
Bookings. Read-only: booking summary, cancellation reason, refund destination
(bank account) and the refund breakdown.

Flutter app — values surface through ``content-desc``. Rows are a label View
next to a value View (read via the label's sibling).
XPaths come from locators/driving_range/cancellation_details_locators.py.
"""
from core.android_base_page import AndroidBasePage
from locators.driving_range.cancellation_details_locators import (
    CancellationDetailsLocators as L,
)


class DrivingRangeCancellationDetailsPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Cancellation details screen not shown"
        self.capture_step("dr_cancellation_details", "Cancellation details screen is visible")

    def verify_range_name(self, name: str):
        assert self.is_visible_after_scroll(L.label_range_name % name), f"Range '{name}' not shown"
        self.capture_step("dr_cancel_details_range", f"Range shown: {name}")

    # ================= readers =================
    def _value(self, label: str) -> str:
        return self.scroll_and_find(L.value_by_label % label).get_attribute("content-desc") or ""

    def get_booking_id(self) -> str:
        """e.g. '#GSHRC'."""
        return self._value("Booking ID")

    def get_cancellation_date_time(self) -> str:
        return self._value("Cancellation date & time")

    def get_cancellation_reason(self) -> str:
        return self._value("Cancellation reason")

    # ================= refund destination =================
    def get_bank_name(self) -> str:
        return self._value("Bank name")

    def get_account_number(self) -> str:
        return self._value("Account number")

    def get_account_holder_name(self) -> str:
        return self._value("Account holder name")

    # ================= refund details =================
    def get_original_total(self) -> str:
        return self.scroll_and_find(L.value_original_total).get_attribute("content-desc") or ""

    def get_total_refund(self) -> str:
        return self.scroll_and_find(L.value_total_refund).get_attribute("content-desc") or ""

    def get_refund_process_note(self) -> str:
        el = self.find_anywhere(L.label_refund_process)
        return "" if el is None else (el.get_attribute("content-desc") or "")

    # ================= summary snapshot =================
    def get_summary(self) -> dict:
        self.scroll_to_top()
        summary = {
            "booking_id": self.get_booking_id(),
            "cancellation_date_time": self.get_cancellation_date_time(),
            "cancellation_reason": self.get_cancellation_reason(),
            "bank_name": self.get_bank_name(),
            "account_number": self.get_account_number(),
            "account_holder_name": self.get_account_holder_name(),
            "original_total": self.get_original_total(),
            "total_refund": self.get_total_refund(),
        }
        self.capture_step("dr_cancel_details_summary", data=summary)
        return summary

    def verify_refund_details(self, original_total=None, total_refund=None,
                              bank_name=None, account_number=None, account_holder_name=None):
        self.capture_step(
            "dr_cancel_details_verify",
            f"Bank={self.get_bank_name()} | Acct={self.get_account_number()} | "
            f"Holder={self.get_account_holder_name()} | "
            f"Original={self.get_original_total()} | Refund={self.get_total_refund()}",
        )
        if original_total is not None:
            assert original_total in self.get_original_total()
        if total_refund is not None:
            assert total_refund in self.get_total_refund()
        if bank_name is not None:
            assert bank_name in self.get_bank_name()
        if account_number is not None:
            assert account_number in self.get_account_number()
        if account_holder_name is not None:
            assert account_holder_name in self.get_account_holder_name()

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("dr_cancel_details_back", "Tapped back")
