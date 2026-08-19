import re

from core.android_base_page import AndroidBasePage
from locators.driving_range.booking_confirmation_locators import (
    DrivingRangeBookingConfirmationLocators as L,
)


_BONUS_BALLS = re.compile(r"\+\s*([\d.,]+)\s*balls", re.IGNORECASE)


def _amounts(text: str) -> list[str]:
    return re.findall(r"Rp\.\s?[\d.,]+", text or "")


def _bonus_balls(text: str) -> str:
    """Pull "100" out of a BXGY bonus line such as "+ 100 balls" / "+ 100 balls (max)"."""
    match = _BONUS_BALLS.search(text or "")
    return match.group(1) if match else ""


# the promo row reads this when nothing is applied
NO_PROMO_LABEL = "Apply a promo"

# promo and credits only show up when they apply, so an empty one is left out
# of the summary entirely rather than reported as a blank field
_OPTIONAL_SUMMARY_FIELDS = ("promo", "credits_used", "credits_earned")


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

    # ================= price details =================
    def get_price_details_type(self) -> str:
        """"Time-based" or "Ball-based", from the "Price details (…)" header."""
        header = self._desc(L.label_price_details)
        match = re.search(r"\(([^)]+)\)", header)
        return match.group(1).strip() if match else ""

    def verify_price_details_type(self, expected: str):
        actual = self.get_price_details_type()
        assert actual.casefold() == expected.strip().casefold(), \
            f"Price details are '{actual}', expected '{expected}'"
        self.capture_step("dr_price_details_type", f"Price details ({actual})")

    def get_price_row(self, name: str) -> str:
        """Full breakdown row, e.g. "100 balls x2\\n+ 100 balls (max)\\nRp. 150,000"."""
        return self._desc(L.price_row_by_name % name).strip()

    def get_price_row_amount(self, name: str) -> str:
        amounts = _amounts(self.get_price_row(name))
        return amounts[-1] if amounts else ""

    def get_price_row_bonus_balls(self, name: str) -> str:
        return _bonus_balls(self.get_price_row(name))

    def get_processing_fee(self) -> str:
        # "Processing fee\nRp. 10,000\nRp. 0" — the last amount is what is actually charged
        amounts = _amounts(self._desc(L.label_processing_fee))
        return amounts[-1] if amounts else ""

    def get_total_payment(self) -> str:
        amounts = _amounts(self._desc(L.label_total_payment))
        return amounts[-1] if amounts else ""

    def get_credits_used(self) -> str:
        if not self.is_visible_after_scroll(L.label_swing_credits_used):
            return ""
        return _value_after_label(self._desc(L.label_swing_credits_used))

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
        self.scroll_up_to_element(L.label_player_name)
        summary = {
            "player_name": self._read(self.get_player_name),
            "date": self._read(self.get_date),
            "booking_time": self._read(self.get_booking_time),
            "duration": self._read(self.get_duration),
            "bays": self._read(self.get_number_of_bays),
            "bay_type": self._read(self.get_bay_type),
            "total": self._read(self.get_total_payment),
            "promo": self._read(self.get_promo_name),
            "credits_used": self._read(self.get_credits_used),
            "credits_earned": self._read(self.get_credits_earned),
            "payment_method": self._read(self.get_payment_method),
        }
        summary = {
            field: value for field, value in summary.items()
            if value or field not in _OPTIONAL_SUMMARY_FIELDS
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

    def verify_balls_section(self):
        """Ball-based ranges show "How many balls?" in place of the add-ons section."""
        assert self.is_visible_after_scroll(L.label_balls, timeout=15), \
            "'How many balls?' section not shown"
        self.capture_step("dr_balls", "'How many balls?' section is visible")

    def verify_addon(self, name: str):
        assert self.is_visible_after_scroll(L.addon_row_by_name % name), \
            f"Add-on '{name}' not shown"
        self.capture_step("dr_addon_row", f"Add-on shown: {name}")

    def get_addon_qty(self, name: str) -> int:
        # "10 balls\nRp. 10,000\n1", or with a BXGY bonus line in between:
        # "100 balls\nRp. 75,000\n+ 100 balls\n2" — the count is the last numeric line.
        digits = [
            line.strip()
            for line in self._desc(L.addon_row_by_name % name).splitlines()
            if line.strip().isdigit()
        ]
        return int(digits[-1]) if digits else 0

    def get_addon_bonus_balls(self, name: str) -> str:
        """Bonus balls granted by a BXGY promo on the "%s" stepper row ("" when none)."""
        return _bonus_balls(self._desc(L.addon_row_by_name % name))

    def verify_addon_bonus_balls(self, name: str, bonus: str):
        actual = self.get_addon_bonus_balls(name)
        assert actual == str(bonus).strip(), \
            f"'{name}' shows a bonus of '{actual}' balls, expected '{bonus}'"
        self.capture_step("dr_addon_bonus", f"'{name}' bonus: + {actual} balls")

    def set_addon_qty(self, name: str, target: int):
        current = self.get_addon_qty(name)
        button = L.addon_minus_by_name if target > current else L.addon_plus_by_name
        for _ in range(abs(target - current)):
            self.click(button % name)
            self.wait_for(2)
        actual = self.get_addon_qty(name)
        assert actual == target, \
            f"Add-on '{name}' quantity is {actual}, expected {target}"
        self.capture_step("dr_addon_qty", f"Add-on '{name}' quantity: {current} -> {target}")

    def increment_addon(self, name: str, times: int = 1):
        for _ in range(times):
            self.click(L.addon_plus_by_name % name)
            self.wait_for(2)
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
    def open_promo(self):
        self.click(L.button_change_promo)
        self.capture_step("dr_open_promo", "Opened promo picker")

    def verify_promo_auto_applied(self) -> str:
        promo = self._desc(L.button_change_promo).strip()
        self.capture_step("dr_promo_applied", f"Promo row: {promo or '(empty)'}")
        return promo

    def get_promo_name(self) -> str:
        promo = self._desc(L.button_change_promo).strip()
        return "" if promo == NO_PROMO_LABEL else promo

    def verify_promo_in_price_details(self, promo_name: str):
        """An applied promo is also listed as its own row inside the price breakdown."""
        assert self.is_visible_after_scroll(L.price_row_promo_by_name % promo_name), \
            f"Promo '{promo_name}' is not listed in the price details"
        self.capture_step("dr_promo_price_row", f"Price details list promo: {promo_name}")

    def verify_bxgy_promo(self, promo_name: str, ball_option: str,
                          bonus_balls: str, total: str | None = None):
        """Check a Buy-X-Get-Y promo end to end on this screen: the bonus balls on the
        stepper row, the same bonus in the price breakdown, the promo row itself, and
        (optionally) the total it produces."""
        self.verify_addon_bonus_balls(ball_option, bonus_balls)

        row_bonus = self.get_price_row_bonus_balls(ball_option)
        assert row_bonus == str(bonus_balls).strip(), (
            f"Price details show a bonus of '{row_bonus}' balls for '{ball_option}', "
            f"expected '{bonus_balls}'"
        )

        applied = self.get_promo_name()
        assert promo_name in applied, \
            f"Applied promo is '{applied}', expected '{promo_name}'"
        self.verify_promo_in_price_details(promo_name)

        actual_total = self.get_total_payment()
        if total is not None:
            assert total in actual_total, \
                f"Total payment is '{actual_total}', expected '{total}'"

        self.capture_step(
            "dr_bxgy_promo",
            f"BXGY '{promo_name}': {ball_option} + {bonus_balls} balls | "
            f"{self.get_price_row(ball_option).replace(chr(10), ' / ')} | "
            f"Total={actual_total}",
        )


    def is_swing_credits_on(self) -> bool:
        return self.find(L.switch_swing_credits).get_attribute("checked") == "true"

    def toggle_swing_credits(self):
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
        
    
    def get_minimum_balls_message(self) -> str:
        if not self.is_visible(L.toaster_minimum_balls, timeout=5, log=False):
            return ""
        return self.find(L.toaster_minimum_balls).get_attribute("content-desc") or ""

    def verify_minimum_balls(self, balls: str = "", times: str = "", bays: str = ""):
        message = self.get_minimum_balls_message()
        assert message, "Minimum balls toaster not shown"
        parsed = self.parse_minimum_balls(message)
        expected = {"balls": balls, "times": times, "bays": bays}
        mismatches = {
            field: (want, parsed[field])
            for field, want in expected.items()
            if want and str(want).strip() != parsed[field]
        }
        assert not mismatches, (
            "Minimum balls toaster does not match:\n"
            + "\n".join(
                f"  {field}: expected '{want}' but toaster reads '{got}'"
                for field, (want, got) in mismatches.items()
            )
            + f"\n  toaster: '{message}'"
        )
        self.capture_step("bays_minimum_balls", message, data=parsed)
        return parsed
