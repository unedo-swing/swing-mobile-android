import re

from core.android_base_page import AndroidBasePage
from locators.tee_time.receipt_locators import ReceiptLocators as L


def _amount(text: str) -> str:
    m = re.search(r"Rp\.\s?[\d.,]+", text or "")
    return m.group(0) if m else ""


class ReceiptPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Receipt screen not shown"
        self.capture_step("receipt")

    def _desc(self, locator) -> str:
        return self.find(locator).get_attribute("content-desc") or ""

    # ---- readers ----
    def get_receipt_id(self) -> str:
        text = self._desc(L.label_title)
        return text.split("#", 1)[1].strip() if "#" in text else text.strip()

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
    def verify_receipt_details(self, course_name: str | None = None, booking_id: str | None = None,
                               date: str | None = None, session: str | None = None,
                               preferred_time: str | None = None, no_of_players=None,
                               total: str | None = None, payment_method: str | None = None) -> str:
        assert self.is_visible(L.label_title, timeout=20), "Receipt screen not shown"
        if course_name is not None:
            assert self.is_visible(L.label_course_name % course_name), \
                f"Course '{course_name}' not shown on receipt"

        receipt_id = self.get_receipt_id()
        actual_booking_id = self.get_booking_id()
        actual_date = self.get_date()
        actual_session = self.get_session()
        actual_time = self.get_preferred_time()
        actual_players = self.get_no_of_players()
        actual_total = self.get_total()
        actual_payment = self.get_payment_method()
        self.capture_step(
            "receipt_details",
            f"Receipt #{receipt_id} (Booking #{actual_booking_id}) | {actual_date} | "
            f"{actual_session} | {actual_time} | {actual_players} | {actual_total} | {actual_payment}",
        )

        assert receipt_id, "No receipt id shown on receipt screen"
        if booking_id is not None:
            assert booking_id in actual_booking_id, \
                f"Booking id '{actual_booking_id}' != expected '{booking_id}'"
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
        return receipt_id

    # ================= action steps =================
    def tap_contact_support(self):
        self.click(L.button_contact_support)
        self.capture_step("contact_support")

    def tap_send_receipt(self):
        self.click(L.button_send_receipt)
        self.capture_step("send_receipt")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("receipt_back")
