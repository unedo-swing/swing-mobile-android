from core.android_base_page import AndroidBasePage
from locators.driving_range.confirm_reschedule_locators import (
    DrivingRangeConfirmRescheduleLocators as L,
)


class DrivingRangeConfirmReschedulePage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Confirm reschedule screen not shown"
        self.capture_step("dr_confirm_reschedule", "Confirm reschedule screen is visible")

    def verify_range_name(self, name: str):
        assert self.is_visible_after_scroll(L.label_range_name % name), f"Range '{name}' not shown"
        self.capture_step("dr_reschedule_range", f"Range shown: {name}")

    # ================= readers =================
    def _value(self, label: str) -> str:
        return self.scroll_and_find(L.value_by_label % label).get_attribute("content-desc") or ""

    def _read(self, getter) -> str:
        try:
            return getter()
        except Exception:
            return ""

    def get_player_name(self) -> str:
        return self._value("Player name")

    def get_booking_id(self) -> str:
        return self._value("Booking ID")

    def get_request_date_time(self) -> str:
        return self._value("Request date & time")

    def get_duration(self) -> str:
        return self._value("Duration")

    def get_bays(self) -> str:
        return self._value("Bays")

    def get_bay_type(self) -> str:
        return self._value("Bay type")

    def get_change_block(self) -> str:
        return self.scroll_and_find(L.label_change_block).get_attribute("content-desc") or ""

    # ================= reschedule reason =================
    def verify_reason_section(self):
        assert self.is_visible_after_scroll(L.label_reschedule_reason, timeout=15), \
            "Reschedule reason section not shown"
        self.capture_step("dr_reschedule_reason", "Reschedule reason section is visible")

    def select_reason(self, name: str):
        self.click(L.reason_by_name % name)
        self.capture_step("dr_reschedule_pick_reason", f"Selected reason '{name}'")

    def is_reason_selected(self, name: str) -> bool:
        el = self.find_anywhere(L.reason_by_name % name)
        return el is not None and el.get_attribute("checked") == "true"

    # ================= reschedule details / payment =================
    def get_reschedule_fee(self) -> str:
        return self._value("Reschedule fee")

    def get_price_difference(self) -> str:
        return self.scroll_and_find(L.value_price_difference).get_attribute("content-desc") or ""

    def tap_price_difference(self):
        self.click(L.button_price_difference)
        self.capture_step("dr_reschedule_price_diff", "Tapped Price difference")

    def get_payment_method(self) -> str:
        return self.scroll_and_find(L.value_payment_method).get_attribute("content-desc") or ""

    def tap_change_payment(self):
        self.click(L.value_payment_method)
        self.capture_step("dr_reschedule_change_payment", "Tapped payment method")

    # ================= summary snapshot =================
    def get_summary(self) -> dict:
        self.scroll_to_top()
        summary = {
            "booking_id": self._read(self.get_booking_id),
            "player_name": self._read(self.get_player_name),
            "request_date_time": self._read(self.get_request_date_time),
            "duration": self._read(self.get_duration),
            "bays": self._read(self.get_bays),
            "bay_type": self._read(self.get_bay_type),
            "reschedule_fee": self._read(self.get_reschedule_fee),
            "price_difference": self._read(self.get_price_difference),
            "payment_method": self._read(self.get_payment_method),
        }
        self.capture_step("dr_reschedule_summary", data=summary)
        return summary

    # ================= confirm =================
    def is_confirm_enabled(self) -> bool:
        return self.is_enabled(L.button_confirm_pay)

    def verify_confirm_enabled(self):
        assert self.is_confirm_enabled(), "Confirm reschedule & pay is disabled"
        self.capture_step("dr_reschedule_confirm_enabled", "Confirm reschedule & pay is enabled")

    def tap_confirm_pay(self):
        self.click(L.button_confirm_pay)
        self.capture_step("dr_reschedule_confirm", "Tapped Confirm reschedule & pay")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("dr_reschedule_back", "Tapped back")

    # ================= confirm dialog =================
    def verify_confirm_dialog(self):
        assert self.is_visible(L.dialog_title, timeout=15), "Confirm reschedule dialog not shown"
        self.capture_step("dr_reschedule_dialog", "Confirm reschedule dialog is visible")

    def dialog_confirm(self):
        self.click(L.dialog_button_confirm)
        self.capture_step("dr_reschedule_dialog_confirm", "Tapped Confirm reschedule (dialog)")

    def dialog_go_back(self):
        self.click(L.dialog_button_go_back)
        self.capture_step("dr_reschedule_dialog_back", "Tapped Go back (dialog)")
