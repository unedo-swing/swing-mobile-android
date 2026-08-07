"""
Booking details page object (Android) — Tee Time.

Opened from "See booking details" on the confirmed screen. Holds the verify step
+ readers for the booking summary, payment summary and history, plus the footer
actions (See complete breakdown / See receipt). XPaths come from
locators/tee_time/booking_details_locators.py.
"""
import re

from core.android_base_page import AndroidBasePage
from locators.tee_time.booking_details_locators import BookingDetailsLocators as L


def _amounts(text: str) -> list[str]:
    """All 'Rp. <number>' amounts found in a string, in order."""
    return re.findall(r"Rp\.\s?[\d.,]+", text or "")


def _value_after_label(text: str) -> str:
    """For a '<Label>\\n<value>' content-desc, return the value (after newline)."""
    return text.split("\n", 1)[1].strip() if "\n" in (text or "") else (text or "")


class BookingDetailsPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Booking details screen not shown"
        self.capture_step("booking_details", "Booking details screen is visible")

    def _desc(self, locator) -> str:
        return self.find(locator).get_attribute("content-desc") or ""

    # ---- booking summary readers ----
    def get_status(self) -> str:
        """Booking status badge, e.g. 'UPCOMING'."""
        return self._desc(L.label_status)

    def get_booking_id(self) -> str:
        """The booking reference, e.g. 'HEPJB' (from 'Booking #HEPJB')."""
        text = self._desc(L.label_booking_id)
        return text.split("#", 1)[1].strip() if "#" in text else text.strip()

    def get_date(self) -> str:
        return self._desc(L.value_date)

    def get_session(self) -> str:
        return self._desc(L.value_session)

    def get_preferred_time(self) -> str:
        return self._desc(L.value_preferred_time)

    def get_no_of_players(self) -> str:
        """e.g. '4 players'."""
        return self._desc(L.value_no_of_players)

    # ---- payment summary readers ----
    def get_subtotal(self) -> str:
        """Subtotal amount, e.g. 'Rp. 3,000,000'."""
        amounts = _amounts(self._desc(L.row_subtotal))
        return amounts[-1] if amounts else ""

    def get_processing_fee(self) -> str:
        """Effective processing fee (the last amount on the row; the earlier one is
        the struck-through original), e.g. 'Rp. 0'."""
        amounts = _amounts(self._desc(L.row_processing_fee))
        return amounts[-1] if amounts else "Rp. 0"

    def get_processing_fee_original(self) -> str:
        """The struck-through original processing fee (first amount), e.g. 'Rp. 10,000'."""
        amounts = _amounts(self._desc(L.row_processing_fee))
        return amounts[0] if amounts else ""

    def get_total_payment(self) -> str:
        """Total payment amount, e.g. 'Rp. 3,000,000'."""
        amounts = _amounts(self._desc(L.row_total_payment))
        return amounts[-1] if amounts else ""

    def get_credits_earned(self) -> str:
        """Swing Credits earned, e.g. '+260,000'."""
        return self._desc(L.value_credits_earned)

    def get_confirmed_timestamp(self) -> str:
        """History 'Booking confirmed' timestamp, e.g. '16:50, 6 Aug 2026'."""
        return _value_after_label(self._desc(L.timeline_booking_confirmed))

    # ---- combined verify ----
    def verify_details(self, status: str | None = None, date: str | None = None,
                       session: str | None = None, preferred_time: str | None = None,
                       no_of_players=None, total_payment: str | None = None,
                       booking_id: str | None = None) -> str:
        """Assert the booking details screen and (optionally) its fields. Only
        non-None args are asserted; a booking id is always required. Returns the
        booking id."""
        assert self.is_visible(L.label_title, timeout=20), "Booking details screen not shown"
        actual_id = self.get_booking_id()
        actual_status = self.get_status()
        actual_date = self.get_date()
        actual_session = self.get_session()
        actual_time = self.get_preferred_time()
        actual_players = self.get_no_of_players()
        actual_total = self.get_total_payment()
        self.capture_step(
            "booking_details_summary",
            f"#{actual_id} [{actual_status}] | {actual_date} | {actual_session} | "
            f"{actual_time} | {actual_players} | total {actual_total}",
        )

        assert actual_id, "No booking id shown on booking details screen"
        if booking_id is not None:
            assert booking_id in actual_id, f"Booking id '{actual_id}' != expected '{booking_id}'"
        if status is not None:
            assert status in actual_status, f"Status '{actual_status}' != expected '{status}'"
        if date is not None:
            assert date in actual_date, f"Date '{actual_date}' != expected '{date}'"
        if session is not None:
            assert session in actual_session, f"Session '{actual_session}' != expected '{session}'"
        if preferred_time is not None:
            assert preferred_time in actual_time, f"Time '{actual_time}' != expected '{preferred_time}'"
        if no_of_players is not None:
            assert str(no_of_players) in actual_players, \
                f"Players '{actual_players}' != expected '{no_of_players}'"
        if total_payment is not None:
            assert total_payment in actual_total, \
                f"Total '{actual_total}' != expected '{total_payment}'"
        return actual_id

    # ================= action steps =================
    def tap_see_complete_breakdown(self):
        self.click(L.button_see_complete_breakdown)
        self.capture_step("see_complete_breakdown", "Tapped See complete breakdown")

    def tap_see_receipt(self):
        self.click(L.button_see_receipt)
        self.capture_step("see_receipt", "Tapped See receipt")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("booking_details_back", "Tapped back")
