import re

from core.android_base_page import AndroidBasePage
from locators.tee_time.booking_confirmed_locators import BookingConfirmedLocators as L


def _amount(text: str) -> str:
    m = re.search(r"Rp\.\s?[\d.,]+", text or "")
    return m.group(0) if m else ""


class BookingConfirmedPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Booking confirmed screen not shown"
        self.capture_step("booking_confirmed", "Booking confirmed ('You're confirmed!') is visible")

    def _desc(self, locator) -> str:
        return self.find(locator).get_attribute("content-desc") or ""

    # ---- readers ----
    def get_booking_id(self) -> str:
        text = self._desc(L.label_booking_id)
        return text.split("#", 1)[1].strip() if "#" in text else text.strip()

    def get_date(self) -> str:
        return self._desc(L.value_date)

    def get_session(self) -> str:
        return self._desc(L.value_session)

    def get_preferred_time(self) -> str:
        return self._desc(L.value_preferred_time)

    def get_no_of_players(self) -> str:
        return self._desc(L.value_no_of_players)

    def get_total(self) -> str:
        return _amount(self._desc(L.value_total))

    def get_payment_method(self) -> str:
        return self._desc(L.value_payment_method)

    def get_credits_earned(self) -> str:
        return self._desc(L.value_credits_earned)

    # ---- combined verify ----
    def verify_confirmed_details(self, course_name: str | None = None, date: str | None = None,
                                 session: str | None = None, preferred_time: str | None = None,
                                 no_of_players=None, total: str | None = None,
                                 payment_method: str | None = None) -> str:
        assert self.is_visible(L.label_title, timeout=20), "Booking confirmed screen not shown"
        if course_name is not None:
            assert self.is_visible(L.label_course_name % course_name), \
                f"Course '{course_name}' not shown on confirmed screen"

        booking_id = self.get_booking_id()
        actual_date = self.get_date()
        actual_session = self.get_session()
        actual_time = self.get_preferred_time()
        actual_players = self.get_no_of_players()
        actual_total = self.get_total()
        actual_payment = self.get_payment_method()
        self.capture_step(
            "confirmed_details",
            f"Booking #{booking_id} | {actual_date} | {actual_session} | "
            f"{actual_time} | {actual_players} | {actual_total} | {actual_payment}",
        )

        assert booking_id, "No booking id shown on confirmed screen"
        if date is not None:
            assert date in actual_date, f"Date '{actual_date}' != expected '{date}'"
        if session is not None:
            assert session in actual_session, f"Session '{actual_session}' != expected '{session}'"
        if preferred_time is not None:
            assert preferred_time in actual_time, f"Time '{actual_time}' != expected '{preferred_time}'"
        if no_of_players is not None:
            assert str(no_of_players) in actual_players, \
                f"Players '{actual_players}' != expected '{no_of_players}'"
        if total is not None:
            assert total in actual_total, f"Total '{actual_total}' != expected '{total}'"
        if payment_method is not None:
            assert payment_method in actual_payment, \
                f"Payment '{actual_payment}' != expected '{payment_method}'"
        return booking_id

    # ================= action steps =================
    def tap_finish(self):
        self.click(L.button_finish)
        self.capture_step("finish", "Tapped Finish")

    def tap_see_booking_details(self):
        self.click(L.button_see_booking_details)
        self.capture_step("see_booking_details", "Tapped See booking details")
