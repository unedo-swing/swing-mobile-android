from core.android_base_page import AndroidBasePage
from locators.driving_range.booking_summary_locators import (
    DrivingRangeBookingSummaryLocators as L,
)
from utils.amounts import last_amount


class DrivingRangeBookingSummaryPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Booking summary screen not shown"
        self.capture_step("dr_booking_summary")

    def verify_range_name(self, name: str):
        assert self.is_visible_after_scroll(L.label_range_name % name), f"Range '{name}' not shown"
        self.capture_step("dr_summary_range", f"Range shown: {name}")

    # ================= readers =================
    def _value(self, label: str) -> str:
        return self.scroll_and_find(L.value_by_label % label).get_attribute("content-desc") or ""

    def _row(self, label: str) -> str:
        return self.scroll_and_find(L.price_row_by_label % label).get_attribute("content-desc") or ""

    def _read(self, getter) -> str:
        try:
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
        return self._value("Number of bays")

    def get_bay_type(self) -> str:
        return self._value("Bay type")

    def get_notes(self) -> str:
        return self._value("Notes to driving range")

    def get_terms(self) -> str:
        return self._value("Terms & conditions")

    # ================= price details =================
    def _last_amount(self, label: str) -> str:
        return last_amount(self._row(label))

    def get_processing_fee(self) -> str:
        return self._last_amount("Processing fee")

    def get_total_payment(self) -> str:
        return self._last_amount("Total payment")

    # ================= summary snapshot =================
    def get_summary(self) -> dict:
        self.scroll_to_top()
        summary = {
            "player_name": self._read(self.get_player_name),
            "date": self._read(self.get_date),
            "booking_time": self._read(self.get_booking_time),
            "duration": self._read(self.get_duration),
            "bays": self._read(self.get_bays),
            "bay_type": self._read(self.get_bay_type),
            "total": self._read(self.get_total_payment),
        }
        self.capture_step(
            "dr_summary_snapshot",
            " | ".join(f"{k}={v}" for k, v in summary.items()),
        )
        return summary

    def verify_booking_summary(self, range_name=None, player_name=None, date=None,
                           booking_time=None, duration=None, bays=None,
                           bay_type=None, total=None):

        if range_name is not None:
            self.verify_range_name(range_name)

        actual = {
            "Player": self.get_player_name(),
            "Date": self.get_date(),
            "Time": self.get_booking_time(),
            "Duration": self.get_duration(),
            "Bays": self.get_bays(),
            "BayType": self.get_bay_type(),
            "Total": self.get_total_payment(),
        }

        self.capture_step(
            "dr_summary_verify",
            " | ".join(f"{k}={v}" for k, v in actual.items()),
        )

        expected = {
            "Player": player_name,
            "Date": date,
            "Time": booking_time,
            "Duration": duration,
            "Bays": bays,
            "BayType": bay_type,
            "Total": total,
        }

        failures = [
            f"{k}: expected {exp!r} in actual {actual[k]!r}"
            for k, exp in expected.items()
            if exp is not None and exp not in actual[k]
        ]
        assert not failures, "Booking summary mismatch -> " + "; ".join(failures)

    # ================= sections / actions =================
    def verify_notes_section(self):
        assert self.is_visible_after_scroll(L.label_notes, timeout=15), "Notes section not shown"
        self.capture_step("dr_summary_notes")

    def verify_terms_section(self):
        assert self.is_visible_after_scroll(L.label_terms, timeout=15), "Terms & conditions not shown"
        self.capture_step("dr_summary_terms")

    def verify_price_details_section(self):
        assert self.is_visible_after_scroll(L.label_price_details, timeout=15), \
            "Price details section not shown"
        self.capture_step("dr_summary_price")

    def tap_show_more(self):
        self.click(L.button_show_more)
        self.capture_step("dr_summary_show_more")

    def tap_show_less(self):
        self.click(L.button_show_less)
        self.capture_step("dr_summary_show_less")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("dr_summary_back")
