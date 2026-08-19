from core.android_base_page import AndroidBasePage
from locators.driving_range.receipt_locators import DrivingRangeReceiptLocators as L


class DrivingRangeReceiptPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Receipt screen not shown"
        self.capture_step("dr_receipt", "Receipt screen is visible")

    def verify_receipt_id(self) -> str:
        receipt_id = self.get_receipt_id()
        assert receipt_id.startswith("Receipt #"), f"Receipt id not shown, got '{receipt_id}'"
        self.capture_step("dr_receipt_id", receipt_id)
        return receipt_id

    def verify_range_name(self, name: str):
        assert self.is_visible_after_scroll(L.label_range_name % name), f"Range '{name}' not shown"
        self.capture_step("dr_receipt_range", f"Range shown: {name}")

    # ================= readers =================
    def _value(self, label: str) -> str:
        return self.scroll_and_find(L.value_by_label % label).get_attribute("content-desc") or ""

    def _read(self, getter) -> str:
        try:
            return getter()
        except Exception:
            return ""

    def get_receipt_id(self) -> str:
        return self.find(L.label_title).get_attribute("content-desc") or ""

    def get_booking_id(self) -> str:
        return self.scroll_and_find(L.label_booking_id).get_attribute("content-desc") or ""

    def get_date(self) -> str:
        return self._value("Date")

    def get_booking_time(self) -> str:
        return self._value("Booking time")

    def get_duration(self) -> str:
        return self._value("Duration")

    def get_bays(self) -> str:
        return self._value("Number of bays")

    def get_bay_type(self) -> str:
        return self._value("Bay type")

    def get_total(self) -> str:
        return self._value("Total")

    def get_payment_method(self) -> str:
        return self._value("Payment method")

    def get_credits_earned(self) -> str:
        return self._value("Swing Credits you earned")

    # ================= summary snapshot =================
    def get_summary(self) -> dict:
        self.scroll_to_top()
        summary = {
            "booking_id": self._read(self.get_booking_id),
            "date": self._read(self.get_date),
            "booking_time": self._read(self.get_booking_time),
            "duration": self._read(self.get_duration),
            "bays": self._read(self.get_bays),
            "bay_type": self._read(self.get_bay_type),
            "total": self._read(self.get_total),
            "payment_method": self._read(self.get_payment_method),
        }
        self.capture_step(
            "dr_receipt_summary",
            " | ".join(f"{k}={v}" for k, v in summary.items()),
        )
        return summary

    def verify_booking_summary(self, booking_id=None, range_name=None, date=None,
                               booking_time=None, duration=None, bays=None,
                               bay_type=None, total=None, payment_method=None):
        if range_name is not None:
            self.verify_range_name(range_name)
        self.capture_step(
            "dr_receipt_verify",
            f"Receipt={self.get_receipt_id()} | Booking={self.get_booking_id()} | "
            f"Date={self.get_date()} | Time={self.get_booking_time()} | "
            f"Duration={self.get_duration()} | Bays={self.get_bays()} | "
            f"BayType={self.get_bay_type()} | Total={self.get_total()} | "
            f"Payment={self.get_payment_method()}",
        )
        if booking_id is not None:
            assert booking_id in self.get_booking_id()
        if date is not None:
            assert date in self.get_date()
        if booking_time is not None:
            assert booking_time in self.get_booking_time()
        if duration is not None:
            assert duration in self.get_duration()
        if bays is not None:
            assert bays in self.get_bays()
        if bay_type is not None:
            assert bay_type in self.get_bay_type()
        if total is not None:
            assert total in self.get_total()
        if payment_method is not None:
            assert payment_method.casefold() in self.get_payment_method().casefold()

    # ================= send receipt / actions =================
    def open_credits_earnings(self):
        self.click(L.label_credits_earned)
        self.capture_step("dr_receipt_open_credits", "Opened Swing Credits earnings")

    def tap_contact_support(self):
        self.click(L.button_contact_support)
        self.capture_step("dr_receipt_support", "Tapped Contact Swing support")

    def is_send_enabled(self) -> bool:
        return self.is_enabled(L.button_send_receipt)

    def tap_send_receipt(self):
        self.click(L.button_send_receipt)
        self.capture_step("dr_receipt_send", "Tapped Send receipt")

    def is_send_on_cooldown(self) -> bool:
        return self.find_anywhere(L.label_send_cooldown) is not None

    def get_send_cooldown(self) -> str:
        el = self.find_anywhere(L.label_send_cooldown)
        return "" if el is None else (el.get_attribute("content-desc") or "")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("dr_receipt_back", "Tapped back")
