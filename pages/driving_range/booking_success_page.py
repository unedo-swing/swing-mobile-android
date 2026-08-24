from core.android_base_page import AndroidBasePage
from locators.driving_range.booking_success_locators import DrivingRangeBookingSuccessLocators as L


class DrivingRangeBookingSuccessPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        # payment settles behind a full-screen spinner before this screen draws
        self.wait_until_loaded(timeout=120)
        assert self.is_visible(L.label_confirmed, timeout=30), "Booking success screen not shown"
        self.capture_step("dr_booking_success")

    def verify_range_name(self, name: str):
        assert self.is_visible_after_scroll(L.label_range_name % name), f"Range '{name}' not shown"
        self.capture_step("dr_success_range", f"Range shown: {name}")

    def verify_booking_id(self):
        booking_id = self.get_booking_id()
        assert booking_id.startswith("Booking #"), f"Booking id not shown, got '{booking_id}'"
        self.capture_step("dr_booking_id", booking_id)
        return booking_id

    def get_booking_id(self) -> str:
        return self.scroll_and_find(L.label_booking_id).get_attribute("content-desc") or ""

    # a value read from its label's sibling, scrolled into view first
    def _value(self, label: str) -> str:
        return self.scroll_and_find(L.value_by_label % label).get_attribute("content-desc") or ""

    def _read(self, getter) -> str:
        try:
            print(f"Searching For : {getter}")
            return getter()
        except Exception:
            return ""

    def get_player_name(self) -> str:
        return self._value("Player name")

    def get_date(self) -> str:
        return self._value("Date")

    def get_booking_time(self) -> str:
        return self._value("Booking time")

    def get_duration(self) -> str:
        return self._value("Duration")

    def get_bays(self) -> str:
        return self._value("Bays")

    def get_bay_type(self) -> str:
        return self._value("Bay type")

    def get_total(self) -> str:
        return self._value("Total")

    def get_payment_method(self) -> str:
        return self._value("Payment method")

    def get_credits_earned(self) -> str:
        if not self.is_visible(L.value_by_label % "Swing Credits you earned", timeout=5, log=False):
            return ""
        return self._value("Swing Credits you earned")

    def get_summary(self, bay_type: str = "") -> dict:
        summary = {
            "player_name": self._read(self.get_player_name),
            "date": self._read(self.get_date),
            "booking_time": self._read(self.get_booking_time),
            "duration": self._read(self.get_duration),
            "bays": self._read(self.get_bays),
            "total": self._read(self.get_total),
            "payment_method": self._read(self.get_payment_method),
        }
        if bay_type != "":
            summary["bay_type"] = self._read(self.get_bay_type)

        swing_credit_earned = self.get_credits_earned()
        if swing_credit_earned != "":
            summary["credits_earned"] = swing_credit_earned
        self.capture_step(
            "dr_confirmed_summary",
            " | ".join(f"{k}={v}" for k, v in summary.items()),
        )
        return summary

    def verify_booking_summary(self, date=None, booking_time=None, duration=None,
                               bays=None, bay_type=None, total=None, payment_method=None):
        self.capture_step(
            "dr_success_summary",
            f"Booking={self.get_booking_id()} | Date={self.get_date()} | "
            f"Time={self.get_booking_time()} | Duration={self.get_duration()} | "
            f"Bays={self.get_bays()} | BayType={self.get_bay_type()} | "
            f"Total={self.get_total()} | Payment={self.get_payment_method()}",
        )
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
            assert payment_method in self.get_payment_method()

    # ================= action steps =================
    def tap_finish(self):
        self.click(L.button_finish)
        self.capture_step("dr_finish")

    def tap_see_booking_details(self):
        self.click(L.button_see_details)
        self.capture_step("dr_see_details")
