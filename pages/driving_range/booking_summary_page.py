"""
Driving Range Booking summary page object (Android).

A read-only summary of a booking: range name, the summary rows (player, date,
booking time, duration, bays, bay type), reservation notes, terms & conditions
(with a Show more/less toggle) and a time-based price breakdown.

Flutter app — values surface through ``content-desc``. Summary rows are a label
View next to a value View (read via the label's sibling); price rows are a
single View whose content-desc "\\n"-joins the label and amount(s).
XPaths come from locators/driving_range/booking_summary_locators.py.
"""
import re

from core.android_base_page import AndroidBasePage
from locators.driving_range.booking_summary_locators import (
    DrivingRangeBookingSummaryLocators as L,
)


def _amounts(text: str) -> list[str]:
    return re.findall(r"Rp\.\s?[\d.,]+", text or "")


class DrivingRangeBookingSummaryPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Booking summary screen not shown"
        self.capture_step("dr_booking_summary", "Booking summary screen is visible")

    def verify_range_name(self, name: str):
        assert self.is_visible_after_scroll(L.label_range_name % name), f"Range '{name}' not shown"
        self.capture_step("dr_summary_range", f"Range shown: {name}")

    # ================= readers =================
    def _value(self, label: str) -> str:
        """A summary value read from its label's sibling, scrolled into view."""
        return self.scroll_and_find(L.value_by_label % label).get_attribute("content-desc") or ""

    def _row(self, label: str) -> str:
        """A price row's full content-desc (label + amount), scrolled in."""
        return self.scroll_and_find(L.price_row_by_label % label).get_attribute("content-desc") or ""

    def _read(self, getter) -> str:
        """Run a getter, returning "" when the row isn't on screen."""
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
        """Reservation notes, e.g. 'No reservation notes'."""
        return self._value("Notes to driving range")

    def get_terms(self) -> str:
        """The terms & conditions body text (collapsed unless 'Show more' tapped)."""
        return self._value("Terms & conditions")

    # ================= price details =================
    def _last_amount(self, label: str) -> str:
        """The last Rp amount in a price row (the charged value, e.g. after a
        struck-through fee: 'Processing fee\\nRp. 10,000\\nRp. 0' -> 'Rp. 0')."""
        amounts = _amounts(self._row(label))
        return amounts[-1] if amounts else ""

    def get_processing_fee(self) -> str:
        return self._last_amount("Processing fee")

    def get_total_payment(self) -> str:
        return self._last_amount("Total payment")

    # ================= summary snapshot =================
    def get_summary(self) -> dict:
        """Snapshot every booking field on this screen. Keys match the booking
        confirmation / success / details summaries so screens can be compared."""
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
        self.capture_step(
            "dr_summary_verify",
            f"Player={self.get_player_name()} | Date={self.get_date()} | "
            f"Time={self.get_booking_time()} | Duration={self.get_duration()} | "
            f"Bays={self.get_bays()} | BayType={self.get_bay_type()} | "
            f"Total={self.get_total_payment()}",
        )
        if player_name is not None:
            assert player_name in self.get_player_name()
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
            assert total in self.get_total_payment()

    # ================= sections / actions =================
    def verify_notes_section(self):
        assert self.is_visible_after_scroll(L.label_notes, timeout=15), "Notes section not shown"
        self.capture_step("dr_summary_notes", "Notes section is visible")

    def verify_terms_section(self):
        assert self.is_visible_after_scroll(L.label_terms, timeout=15), "Terms & conditions not shown"
        self.capture_step("dr_summary_terms", "Terms & conditions section is visible")

    def verify_price_details_section(self):
        assert self.is_visible_after_scroll(L.label_price_details, timeout=15), \
            "Price details section not shown"
        self.capture_step("dr_summary_price", "Price details section is visible")

    def tap_show_more(self):
        self.click(L.button_show_more)
        self.capture_step("dr_summary_show_more", "Tapped Show more (terms)")

    def tap_show_less(self):
        self.click(L.button_show_less)
        self.capture_step("dr_summary_show_less", "Tapped Show less (terms)")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("dr_summary_back", "Tapped back")
