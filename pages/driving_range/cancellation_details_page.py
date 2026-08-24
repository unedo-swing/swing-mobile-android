from core.android_base_page import AndroidBasePage
from locators.driving_range.cancellation_details_locators import (
    CancellationDetailsLocators as L,
)


class DrivingRangeCancellationDetailsPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Cancellation details screen not shown"
        self.capture_step("dr_cancellation_details")

    def verify_range_name(self, name: str):
        assert self.is_visible_after_scroll(L.label_range_name % name), f"Range '{name}' not shown"
        self.capture_step("dr_cancel_details_range", f"Range shown: {name}")

    # ================= readers =================
    def _value(self, label: str) -> str:
        return self.scroll_and_find(L.value_by_label % label).get_attribute("content-desc") or ""

    def get_booking_id(self) -> str:
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
        
        actual = {
        "Original": self.get_original_total(),
        "Refund": self.get_total_refund(),
        "Bank": self.get_bank_name(),
        "Acct": self.get_account_number(),
        "Holder": self.get_account_holder_name(),
        }

        self.capture_step(
            "dr_cancel_details_verify",
            " | ".join(f"{k}={v}" for k, v in actual.items()),
        )

        expected = {
            "Original": original_total,
            "Refund": total_refund,
            "Bank": bank_name,
            "Acct": account_number,
            "Holder": account_holder_name,
        }
        
        failures = [
            f"{k}: expected {exp!r} in actual {actual[k]!r}"
            for k, exp in expected.items()
            if exp is not None and exp not in actual[k]
        ]
        
        
        assert not failures, "Refund detail mismatch -> " + "; ".join(failures)

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("dr_cancel_details_back")
