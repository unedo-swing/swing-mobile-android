"""
Driving Range Confirm cancellation page object (Android).

Opened from Change Booking > Cancellation tab > 'Continue cancel'. Shows the
booking summary, a cancellation-reason radio list, a refund destination (bank
account) and a refund breakdown, then 'Confirm & cancel' (disabled until a
reason + bank details are provided). Confirming opens a 'Confirm cancel booking?'
dialog (Confirm cancellation / Go back).

Flutter app — values surface through ``content-desc``; the bank fields expose a
``hint``. XPaths come from locators/driving_range/confirm_cancellation_locators.py.
"""
from core.android_base_page import AndroidBasePage
from locators.driving_range.confirm_cancellation_locators import (
    ConfirmCancellationLocators as L,
)


class DrivingRangeConfirmCancellationPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Confirm cancellation screen not shown"
        self.capture_step("dr_confirm_cancellation", "Confirm cancellation screen is visible")

    def verify_range_name(self, name: str):
        assert self.is_visible_after_scroll(L.label_range_name % name), f"Range '{name}' not shown"
        self.capture_step("dr_cancel_range", f"Range shown: {name}")

    # ================= readers =================
    def _value(self, label: str) -> str:
        return self.scroll_and_find(L.value_by_label % label).get_attribute("content-desc") or ""

    def get_booking_id(self) -> str:
        """e.g. '#GSHRC'."""
        return self._value("Booking ID")

    def get_cancellation_date_time(self) -> str:
        return self._value("Cancellation date & time")

    # ================= cancellation reason =================
    def verify_reason_section(self):
        assert self.is_visible_after_scroll(L.label_cancellation_reason, timeout=15), \
            "Cancellation reason section not shown"
        self.capture_step("dr_cancel_reason", "Cancellation reason section is visible")

    def select_reason(self, name: str):
        """Pick a cancellation reason, e.g. 'Bad weather', 'Wrong driving range booked'."""
        self.click(L.reason_by_name % name)
        self.capture_step("dr_cancel_pick_reason", f"Selected reason '{name}'")

    def is_reason_selected(self, name: str) -> bool:
        el = self.find_anywhere(L.reason_by_name % name)
        return el is not None and el.get_attribute("checked") == "true"

    # ================= refund destination =================
    def tap_select_bank(self):
        """Open the Select bank dialog."""
        self.click(L.button_select_bank)
        self.capture_step("dr_cancel_select_bank", "Tapped Select Bank")

    def enter_bank_account_number(self, number: str):
        self.type_text(L.input_bank_account_number, number)
        self.capture_step("dr_cancel_bank_number", f"Entered bank account number '{number}'")

    def enter_bank_account_name(self, name: str):
        self.type_text(L.input_bank_account_name, name)
        self.capture_step("dr_cancel_bank_name", f"Entered bank account name '{name}'")

    # ================= refund details =================
    def get_original_total(self) -> str:
        return self.scroll_and_find(L.value_original_total).get_attribute("content-desc") or ""

    def get_total_refunded(self) -> str:
        return self.scroll_and_find(L.value_total_refunded).get_attribute("content-desc") or ""

    def get_refund_process_note(self) -> str:
        """e.g. 'Refund process will take up to 3 business days'."""
        el = self.find_anywhere(L.label_refund_process)
        return "" if el is None else (el.get_attribute("content-desc") or "")

    def get_refund_summary(self) -> dict:
        summary = {
            "booking_id": self._value("Booking ID"),
            "cancellation_date_time": self._value("Cancellation date & time"),
            "original_total": self.get_original_total(),
            "total_refunded": self.get_total_refunded(),
        }
        self.capture_step("dr_cancel_refund_summary", data=summary)
        return summary

    # ================= confirm =================
    def is_confirm_enabled(self) -> bool:
        return self.is_enabled(L.button_confirm_cancel)

    def verify_confirm_enabled(self):
        assert self.is_confirm_enabled(), "Confirm & cancel is disabled"
        self.capture_step("dr_cancel_confirm_enabled", "Confirm & cancel is enabled")

    def tap_confirm_cancel(self):
        """Tap 'Confirm & cancel' -> opens the confirm dialog."""
        self.click(L.button_confirm_cancel)
        self.capture_step("dr_cancel_confirm", "Tapped Confirm & cancel")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("dr_cancel_back", "Tapped back")

    # ================= confirm dialog =================
    def verify_confirm_dialog(self):
        assert self.is_visible(L.dialog_title, timeout=15), "Confirm cancel dialog not shown"
        self.capture_step("dr_cancel_dialog", "Confirm cancel dialog is visible")

    def dialog_confirm(self):
        """Confirm on the 'Confirm cancel booking?' dialog."""
        self.click(L.dialog_button_confirm)
        self.capture_step("dr_cancel_dialog_confirm", "Tapped Confirm cancellation (dialog)")

    def dialog_go_back(self):
        self.click(L.dialog_button_go_back)
        self.capture_step("dr_cancel_dialog_back", "Tapped Go back (dialog)")
