import re

from core.android_base_page import AndroidBasePage
from locators.tee_time.booking_summary_locators import BookingSummaryLocators as L


AMOUNT_RE = re.compile(r"\b(?:Rp|RM)\.?\s*\d[\d.,]*(?<![.,])")

def _amounts(text: str) -> list[str]:
    return AMOUNT_RE.findall(text or "")


class BookingSummaryPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Booking summary screen not shown"
        self.capture_step("booking_summary")

    def _desc(self, locator) -> str:
        # scroll_and_find (not find): long scrollable screen (identity, players,
        # notes, terms, Price details) and Flutter builds lazily, so anything
        # below the fold is absent from the tree until scrolled into view.
        return self.scroll_and_find(locator).get_attribute("content-desc") or ""

    # ---- booking identity / summary readers ----
    def verify_course_name(self, name: str):
        assert self.is_visible_after_scroll(L.label_course_name % name), \
            f"Course '{name}' not shown on booking summary"

    def get_date(self) -> str:
        return self._desc(L.value_date)

    def get_session(self) -> str:
        return self._desc(L.value_session)

    def get_preferred_time(self) -> str:
        return self._desc(L.value_preferred_time)

    def get_booking_type(self) -> str:
        return self._desc(L.label_booking_type)

    # ---- players summary ----
    def verify_player_summary(self, name: str):
        assert self.is_visible_after_scroll(L.player_card_by_name % name), \
            f"Player '{name}' not shown on booking summary"
        self.capture_step("verify_player_summary", f"Player shown: {name}")

    def get_player_summary_amount(self, name: str) -> str:
        amounts = _amounts(self._desc(L.player_card_by_name % name))
        return amounts[-1] if amounts else ""

    # ---- notes ----
    def get_notes(self) -> str:
        return self._desc(L.value_notes)

    # ---- terms & conditions ----
    def get_terms_body(self) -> str:
        return self._desc(L.label_terms_body)

    def open_terms(self):
        self.click(L.link_terms)
        self.capture_step("open_terms")

    # ---- price details ----
    def get_price_breakdown(self, name: str) -> str:
        return self._desc(L.price_line_by_name % name)

    def get_processing_fee(self) -> str:
        amounts = _amounts(self._desc(L.label_processing_fee))
        return amounts[-1] if amounts else "Rp. 0"

    def get_total_payment(self) -> str:
        amounts = _amounts(self._desc(L.label_total_payment))
        return amounts[-1] if amounts else ""

    # ---- combined verify ----
    def verify_summary_details(self, course_name: str | None = None, date: str | None = None,
                               session: str | None = None, preferred_time: str | None = None,
                               booking_type: str | None = None,
                               total_payment: str | None = None):
        assert self.is_visible(L.label_title, timeout=20), "Booking summary screen not shown"
        if course_name is not None:
            self.verify_course_name(course_name)

        actual_date = self.get_date()
        actual_session = self.get_session()
        actual_time = self.get_preferred_time()
        actual_type = self.get_booking_type()
        actual_total = self.get_total_payment()
        self.capture_step(
            "summary_details",
            f"{actual_date} | {actual_session} | {actual_time} | {actual_type} | "
            f"total {actual_total}",
        )

        if date is not None:
            assert date in actual_date, f"Date '{actual_date}' != expected '{date}'"
        if session is not None:
            assert session in actual_session, f"Session '{actual_session}' != expected '{session}'"
        if preferred_time is not None:
            assert preferred_time in actual_time, f"Time '{actual_time}' != expected '{preferred_time}'"
        if booking_type is not None:
            assert booking_type in actual_type, f"Booking type '{actual_type}' != expected '{booking_type}'"
        if total_payment is not None:
            assert total_payment in actual_total, \
                f"Total '{actual_total}' != expected '{total_payment}'"

    # ================= action steps =================
    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("booking_summary_back")
