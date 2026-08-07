import re

from core.android_base_page import AndroidBasePage
from locators.driving_range.booking_confirmation_locators import (
    DrivingRangeBookingConfirmationLocators as L,
)


def _amounts(text: str) -> list[str]:
    return re.findall(r"Rp\.\s?[\d.,]+", text or "")


def _value_after_label(text: str) -> str:
    return text.split("\n", 1)[1].strip() if "\n" in (text or "") else (text or "")


class DrivingRangeBookingConfirmationPage(AndroidBasePage):

    # ================= verify / readers =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Booking confirmation screen not shown"
        self.capture_step("dr_booking_confirmation", "Booking confirmation screen is visible")

    def verify_range_name(self, name: str):
        assert self.is_visible_after_scroll(L.label_range_name % name), f"Range '{name}' not shown"
        self.capture_step("dr_confirm_range", f"Range shown: {name}")

    def verify_payment_method(self, name: str):
        selected = self.get_payment_method()
        assert name.casefold() in selected.casefold(), \
            f"Payment method is '{selected}', expected '{name}'"
        self.capture_step("dr_verify_payment", f"Payment method: {selected}")

    def verify_pay_now_enabled(self):
        assert self.is_pay_now_enabled(), "Pay now is disabled"
        self.capture_step("dr_pay_now_enabled", "Pay now is enabled")

    def _desc(self, locator) -> str:
        # this screen is long — scroll the row into view before reading it
        return self.scroll_and_find(locator).get_attribute("content-desc") or ""

    def _read(self, getter) -> str:
        """Run a getter, returning "" when the row isn't on screen.

        A missing row must not blow up mid-snapshot — get_summary() collects
        every field first so the comparison can report all of them at once.
        """
        try:
            return getter()
        except Exception:
            return ""

    def get_player_name(self) -> str:
        return _value_after_label(self._desc(L.label_player_name))

    def get_date(self) -> str:
        return _value_after_label(self._desc(L.label_date))

    def get_booking_time(self) -> str:
        return _value_after_label(self._desc(L.label_booking_time))

    def get_duration(self) -> str:
        return _value_after_label(self._desc(L.label_duration))

    def get_number_of_bays(self) -> str:
        return _value_after_label(self._desc(L.label_number_of_bays))

    def get_bay_type(self) -> str:
        return _value_after_label(self._desc(L.label_bay_type))

    def verify_booking_details(self, date=None, booking_time=None, duration=None,
                               number_of_bays=None, bay_type=None):
        self.capture_step(
            "dr_booking_summary",
            f"Date={self.get_date()} | Time={self.get_booking_time()} | "
            f"Duration={self.get_duration()} | Bays={self.get_number_of_bays()} | "
            f"BayType={self.get_bay_type()}",
        )
        if date is not None:
            assert date in self.get_date()
        if booking_time is not None:
            assert booking_time in self.get_booking_time()
        if duration is not None:
            assert duration in self.get_duration()
        if number_of_bays is not None:
            assert number_of_bays in self.get_number_of_bays()
        if bay_type is not None:
            assert bay_type in self.get_bay_type()

    def get_total_payment(self) -> str:
        amounts = _amounts(self._desc(L.label_total_payment))
        return amounts[-1] if amounts else ""

    def get_credits_earned(self) -> str:
        return self._desc(L.label_credits_earned)

    def open_credits_earnings(self):
        self.click(L.label_credits_earned)
        self.capture_step("dr_open_credits", "Opened Swing Credits earnings")

    def get_selected_payment(self) -> str:
        el = self.find_anywhere(L.label_payment_method)
        return "" if el is None else (el.get_attribute("content-desc") or "")

    def get_payment_method(self) -> str:
        for part in (p.strip() for p in self.get_selected_payment().split("\n")):
            if part and "payment selected" not in part.casefold():
                return part
        return ""

    def get_summary(self) -> dict:
        # start from the top so the fields below read in screen order
        self.scroll_to_top()
        summary = {
            "player_name": self._read(self.get_player_name),
            "date": self._read(self.get_date),
            "booking_time": self._read(self.get_booking_time),
            "duration": self._read(self.get_duration),
            "bays": self._read(self.get_number_of_bays),
            "bay_type": self._read(self.get_bay_type),
            "total": self._read(self.get_total_payment),
            "payment_method": self._read(self.get_payment_method),
        }
        self.capture_step(
            "dr_confirmation_summary",
            " | ".join(f"{k}={v}" for k, v in summary.items()),
        )
        return summary

    # ================= rentals / add-ons =================
    def verify_addons_section(self):
        assert self.is_visible_after_scroll(L.label_addons, timeout=15), \
            "Rentals/add-ons section not shown"
        self.capture_step("dr_addons", "Rentals/add-ons section is visible")

    def verify_addon(self, name: str):
        assert self.is_visible_after_scroll(L.addon_row_by_name % name), \
            f"Add-on '{name}' not shown"
        self.capture_step("dr_addon_row", f"Add-on shown: {name}")

    def increment_addon(self, name: str, times: int = 1):
        for _ in range(times):
            self.click(L.addon_plus_by_name % name)
        self.capture_step("dr_addon_plus", f"Incremented '{name}' x{times}")

    def decrement_addon(self, name: str, times: int = 1):
        for _ in range(times):
            self.click(L.addon_minus_by_name % name)
        self.capture_step("dr_addon_minus", f"Decremented '{name}' x{times}")

    # ================= notes / policy =================
    def add_notes(self, text: str):
        self.fill(L.input_notes, text)
        self.capture_step("dr_notes", f"Added notes: {text}")

    def select_reschedule_tab(self):
        self.click(L.tab_reschedule)
        self.capture_step("dr_reschedule_tab", "Selected Reschedule tab")

    def select_cancellation_tab(self):
        self.click(L.tab_cancellation)
        self.capture_step("dr_cancellation_tab", "Selected Cancellation tab")

    def tap_learn_more(self):
        self.click(L.link_learn_more)
        self.capture_step("dr_learn_more", "Tapped Learn more")

    # ================= promo / credits =================
    def change_promo(self):
        self.click(L.button_change_promo)
        self.capture_step("dr_open_promo", "Opened promo picker")
    
    def verify_promo_auto_applied(self):
        return self.get_text(L.button_change_promo)
    
    def is_swing_credits_on(self) -> bool:
        return self.find(L.switch_swing_credits).get_attribute("checked") == "true"

    def toggle_swing_credits(self):
        # the Switch bounds cover the card with a "Redeem" child in the middle,
        # so tap the toggle at the top-right instead of the element centre.
        self.scroll_to_element(L.switch_swing_credits)
        r = self.find(L.switch_swing_credits).rect
        x = r["x"] + r["width"] - max(30, int(r["width"] * 0.08))
        y = r["y"] + max(30, int(r["height"] * 0.14))
        self.driver.execute_script("mobile: clickGesture", {"x": x, "y": y})
        self.capture_step("dr_swing_credits", "Toggled Use Swing Credits")

    def open_redeem_swing_credits(self):
        self.click(L.button_redeem_swing_credits)
        self.capture_step("dr_open_redeem", "Opened Redeem Swing Credits")

    # ================= payment / pay =================
    def tap_select_payment(self):
        self.click(L.button_select_payment)
        self.capture_step("dr_select_payment", "Tapped Select payment")

    def tap_change_payment(self):
        self.click(L.button_change_payment)
        self.capture_step("dr_change_payment", "Tapped Change payment")

    def is_pay_now_enabled(self) -> bool:
        return self.is_enabled(L.button_pay_now)

    def tap_pay_now(self):
        self.click(L.button_pay_now)
        self.capture_step("dr_pay_now", "Tapped Pay now")
