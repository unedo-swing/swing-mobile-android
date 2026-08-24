import re
from decimal import Decimal, InvalidOperation

from core.android_base_page import AndroidBasePage
from locators.driving_range.booking_details_locators import (
    DrivingRangeBookingDetailsLocators as L,
)


AMOUNT_RE = re.compile(r"\b(RM|Rp)\.?\s*([\d.,]*\d)")


def _amounts(text: str) -> list[str]:
    return [match.group() for match in AMOUNT_RE.finditer(text or "")]

# ID: 1.500.000,00  |  MY: 1,500,000.00
_SEPARATORS = {"Rp": (".", ","), "RM": (",", ".")}


def parse_amount(text: str, default_symbol: str = "Rp") -> Decimal | None:
    if not text:
        return None
    m = AMOUNT_RE.search(text)
    if m:
        symbol, digits = m.group(1), m.group(2)
    else:
        m = re.search(r"[\d.,]*\d", text)
        if not m:
            return None
        symbol, digits = default_symbol, m.group()

    thousands, decimal = _SEPARATORS[symbol]
    digits = digits.replace(thousands, "").replace(decimal, ".")
    try:
        return Decimal(digits)
    except InvalidOperation:
        return None


def amounts_equal(expected: str, actual: str) -> bool:
    m = AMOUNT_RE.search(actual) or AMOUNT_RE.search(expected)
    symbol = m.group(1) if m else "Rp"
    a, b = parse_amount(expected, symbol), parse_amount(actual, symbol)
    return a is not None and a == b


class DrivingRangeBookingDetailsPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Booking details screen not shown"
        self.capture_step("dr_booking_details")

    def verify_booking_id(self) -> str:
        booking_id = self.get_booking_id()
        assert booking_id.startswith("Booking #"), f"Booking id not shown, got '{booking_id}'"
        self.capture_step("dr_details_booking_id", booking_id)
        return booking_id

    def verify_status(self, status: str):
        assert self.is_visible_after_scroll(L.label_status % status), f"Status '{status}' not shown"
        self.capture_step("dr_details_status", f"Status shown: {status}")

    # ================= readers =================
    def _value(self, label: str) -> str:
        return self.scroll_and_find(L.value_by_label % label).get_attribute("content-desc") or ""

    def _row(self, label: str) -> str:
        return self.scroll_and_find(L.payment_row_by_label % label).get_attribute("content-desc") or ""

    def _read(self, getter) -> str:
        try:
            return getter()
        except Exception:
            return ""

    def get_booking_id(self) -> str:
        return self.scroll_and_find(L.label_booking_id).get_attribute("content-desc") or ""

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

    # ================= payment summary =================
    def _last_amount(self, label: str) -> str:
        amounts = _amounts(self._row(label))
        return amounts[-1] if amounts else ""

    def get_subtotal(self) -> str:
        return self._last_amount("Subtotal")

    def get_processing_fee(self) -> str:
        return self._last_amount("Processing fee")

    def get_total_payment(self) -> str:
        return self._last_amount("Total payment")

    def get_credits_earned(self) -> str:
        return self._value("Swing Credits you earned")

    # ================= summary snapshot =================
    def get_summary(self) -> dict:
        self.scroll_to_top()
        summary = {
            "booking_id": self._read(self.get_booking_id),
            "player_name": self._read(self.get_player_name),
            "date": self._read(self.get_date),
            "booking_time": self._read(self.get_booking_time),
            "duration": self._read(self.get_duration),
            "bays": self._read(self.get_bays),
            "bay_type": self._read(self.get_bay_type),
            "total": self._read(self.get_total_payment),
        }
        self.capture_step(
            "dr_details_summary",
            " | ".join(f"{k}={v}" for k, v in summary.items()),
        )
        return summary

    def verify_booking_summary(self, booking_id=None, player_name=None, date=None,
                           booking_time=None, duration=None, bays=None,
                           bay_type=None, total=None):

        actual = {
            "Booking": self.get_booking_id(),
            "Player": self.get_player_name(),
            "Date": self.get_date(),
            "Time": self.get_booking_time(),
            "Duration": self.get_duration(),
            "Bays": self.get_bays(),
            "BayType": self._read(self.get_bay_type),
            "Total": self.get_total_payment(),
        }

        self.capture_step(
            "dr_details_verify",
            " | ".join(f"{k}={v}" for k, v in actual.items() if v),
        )

        expected = {
            "Booking": booking_id,
            "Player": player_name,
            "Date": date,
            "Time": booking_time,
            "Duration": duration,
            "Bays": bays,
            "BayType": bay_type,
            "Total": total,
        }

        AMOUNT_FIELDS = {"Total"}

        failures = []
        for key, exp in expected.items():
            if exp is None:
                continue
            act = actual[key]
            if key in AMOUNT_FIELDS:
                if not amounts_equal(exp, act):
                    failures.append(f"{key}: expected {exp!r}, got {act!r}")
            elif exp not in act:
                failures.append(f"{key}: expected {exp!r} in actual {act!r}")

        assert not failures, "Booking detail mismatch -> " + "; ".join(failures)

    # ================= history =================
    def verify_history_section(self):
        assert self.is_visible_after_scroll(L.label_history, timeout=15), "History section not shown"
        self.capture_step("dr_details_history")

    def verify_history_item(self, status: str):
        assert self.is_visible_after_scroll(L.history_item_by_status % status), \
            f"History entry '{status}' not shown"
        self.capture_step("dr_details_history_item", f"History entry shown: {status}")

    def get_history_item(self, status: str) -> str:
        return self.scroll_and_find(L.history_item_by_status % status).get_attribute("content-desc") or ""

    # ================= reschedule summary (present when the booking was rescheduled) =================
    # the History entry uses a capitalised status: "Booking Rescheduled"
    _RESCHEDULED_STATUS = "Booking Rescheduled"

    def is_rescheduled(self) -> bool:
        return self.find_anywhere(L.label_reschedule_summary) is not None

    def verify_reschedule_summary_section(self):
        assert self.is_visible_after_scroll(L.label_reschedule_summary, timeout=15), \
            "Reschedule summary section not shown"
        self.capture_step("dr_details_reschedule_summary")

    def get_reschedule_change(self) -> str:
        return self.scroll_and_find(L.label_reschedule_change).get_attribute("content-desc") or ""

    def get_reschedule_fee(self) -> str:
        return self._value("Reschedule fee")

    def get_price_difference(self) -> str:
        return self._value("Price difference")

    def get_reschedule_total(self) -> str:
        return self._value("Total")

    def tap_reschedule_see_details(self):
        self.click(L.button_reschedule_see_details)
        self.capture_step("dr_details_reschedule_see_details")

    def get_reschedule_summary(self) -> dict:
        summary = {
            "change": self._read(self.get_reschedule_change),
            "reschedule_fee": self._read(self.get_reschedule_fee),
            "price_difference": self._read(self.get_price_difference),
            "total": self._read(self.get_reschedule_total),
        }
        self.capture_step("dr_details_reschedule_snapshot", data=summary)
        return summary

    def verify_rescheduled(self):
        self.verify_reschedule_summary_section()
        self.verify_history_item(self._RESCHEDULED_STATUS)

    def get_rescheduled_entry(self) -> str:
        try:
            return self.get_history_item(self._RESCHEDULED_STATUS)
        except Exception:
            return ""

    # ================= action steps =================
    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("dr_details_back")

    def tap_see_breakdown(self):
        self.click(L.button_see_breakdown)
        self.capture_step("dr_details_breakdown")

    def tap_see_receipt(self):
        self.click(L.button_see_receipt)
        self.capture_step("dr_details_receipt")
    
    def tap_three_dots(self):
        self.click(L.button_three_dots)
        self.capture_step("Tap Three Dots")
    
    def tap_reschedule_booking(self):
        self.click(L.button_reschedule_booking)
        self.capture_step("Tap Reschedule Booking")
    
    def tap_cancel_booking(self):
        self.click(L.button_cancel_booking)
        self.capture_step("Tap Cancel Booking")
    
    def tap_contact_swing_support(self):
        self.click(L.button_contact_swing_support)
        self.capture_step("Tap Swing Support")
    
    def tap_close_bottom_sheet(self):
        self.click(L.button_close_bottom_sheet)
        self.capture_step("Close Bottom Sheet")
    
