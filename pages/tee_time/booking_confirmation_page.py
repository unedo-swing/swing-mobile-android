"""
Booking confirmation page object (Android) — Tee Time.

Opened after choosing a booking method. Holds the per-screen STEPS and a few
readers for the money/summary values. XPaths come from
locators/tee_time/booking_confirmation_locators.py.
"""
import re

from core.android_base_page import AndroidBasePage
from locators.tee_time.booking_confirmation_locators import BookingConfirmationLocators as L


def _amounts(text: str) -> list[str]:
    """All 'Rp. <number>' amounts found in a string, in order."""
    return re.findall(r"Rp\.\s?[\d.,]+", text or "")


def _value_after_label(text: str) -> str:
    """For a '<Label>\\n<value>' content-desc, return the value (after newline)."""
    return text.split("\n", 1)[1].strip() if "\n" in (text or "") else (text or "")


class BookingConfirmationPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Booking confirmation screen not shown"
        self.capture_step("booking_confirmation", "Booking confirmation screen is visible")

    def _desc(self, locator) -> str:
        # scroll_and_find (not find): this is a long scrollable screen (players,
        # notes, terms, Price details) and Flutter builds lazily, so anything
        # below the fold is simply absent from the tree until scrolled into view.
        return self.scroll_and_find(locator).get_attribute("content-desc") or ""

    # ---- booking summary: date / session / preferred time ----
    def get_date(self) -> str:
        return _value_after_label(self._desc(L.label_date))

    def get_session(self) -> str:
        return _value_after_label(self._desc(L.label_session))

    def get_preferred_time(self) -> str:
        return _value_after_label(self._desc(L.label_preferred_time))

    def verify_booking_details(self, date: str | None = None, session: str | None = None,
                               preferred_time: str | None = None):
        """Assert the summary matches the expected date / session / preferred time."""
        actual_date = self.get_date()
        actual_session = self.get_session()
        actual_time = self.get_preferred_time()
        self.capture_step(
            "booking_summary",
            f"Date={actual_date} | Session={actual_session} | Time={actual_time}",
        )
        if date is not None:
            assert date in actual_date, f"Date '{actual_date}' != expected '{date}'"
        if session is not None:
            assert session in actual_session, f"Session '{actual_session}' != expected '{session}'"
        if preferred_time is not None:
            assert preferred_time in actual_time, f"Time '{actual_time}' != expected '{preferred_time}'"

    # ---- full pre-payment summary ----
    def verify_before_payment(self, venue_name: str | None = None, date: str | None = None,
                              session: str | None = None, preferred_time: str | None = None,
                              player_names: list[str] | None = None, total_players: int | None = None,
                              total_payment: str | None = None) -> dict:
        assert self.is_visible(L.label_title, timeout=20), "Booking confirmation screen not shown"
        self.scroll_to_top()
        actual_date = self.get_date()
        actual_session = self.get_session()
        actual_time = self.get_preferred_time()
        actual_total_players = self.get_total_players()
        actual_total_payment = self.get_total_payment()
        actual_processing_fee = self.get_processing_fee()
        actual_payment_method = self.get_selected_payment()
        actual_credits = self.get_credits_earned()

        player_payments = {}
        if player_names:
            for name in player_names:
                player_payments[name] = self.get_player_payment(name)

        self.capture_step(
            "before_payment_summary",
            f"Date={actual_date} | Session={actual_session} | Time={actual_time} | "
            f"Players={actual_total_players} | Total={actual_total_payment} "
            f"(fee {actual_processing_fee}) | Payment={actual_payment_method or 'not selected'} | "
            f"Credits={actual_credits or 'none'}"
            + (f" | PerPlayer={player_payments}" if player_payments else ""),
        )

        if date is not None:
            assert date in actual_date, f"Date '{actual_date}' != expected '{date}'"
        if session is not None:
            assert session in actual_session, f"Session '{actual_session}' != expected '{session}'"
        if preferred_time is not None:
            assert preferred_time in actual_time, f"Time '{actual_time}' != expected '{preferred_time}'"
        if total_players is not None:
            assert actual_total_players == total_players, \
                f"Total players {actual_total_players} != expected {total_players}"
        if total_payment is not None:
            assert total_payment in actual_total_payment, \
                f"Total payment '{actual_total_payment}' != expected '{total_payment}'"

        return {
            "venue_name": venue_name,
            "date": actual_date,
            "session": actual_session,
            "preferred_time": actual_time,
            "total_players": actual_total_players,
            "total_payment": actual_total_payment,
            "processing_fee": actual_processing_fee,
            "payment_method": actual_payment_method,
            "credits_earned": actual_credits,
            "player_payments": player_payments,
        }

    # ---- money readers ----
    def get_total_payment(self) -> str:
        """Total payment amount, e.g. 'Rp. 1,000,000'."""
        amounts = _amounts(self._desc(L.label_total_payment))
        return amounts[-1] if amounts else ""

    def get_player_payment(self, name: str) -> str:
        """The amount charged to a given host/player card, e.g. 'Rp. 500,000'."""
        amounts = _amounts(self._desc(L.player_card_by_name % name))
        return amounts[-1] if amounts else ""

    def get_price_breakdown(self, name: str) -> str:
        """The full Price-details line for a player (publish rate, promo, net)."""
        return self._desc(L.price_line_by_name % name)

    def get_processing_fee(self) -> str:
        amounts = _amounts(self._desc(L.label_processing_fee))
        return amounts[-1] if amounts else "Rp. 0"

    def get_credits_earned(self) -> str:
        """Swing Credits earned shown on the bottom bar, e.g. '+ 100,000 (for all)'.
        Returns '' if no credits bar is shown (e.g. no promo applies) — the bar
        is optional, so this never raises."""
        if not self.is_visible_after_scroll(L.label_credits_earned, timeout=3):
            return ""
        return self._desc(L.label_credits_earned)

    def get_selected_payment(self) -> str:
        """The chosen payment method's name, e.g. 'OVO' (empty if none picked)."""
        if not self.is_visible_after_scroll(L.label_selected_payment, timeout=3):
            return ""
        return self._desc(L.label_selected_payment)

    def get_total_players(self) -> int:
        self.scroll_and_find(L.label_price_details)
        return len(self.find_all(L.all_player_cards))

    # ================= action steps =================
    def open_credits_earnings(self):
        """Tap the credits-earned bar to open the 'Swing Credits earnings' dialog."""
        self.click(L.label_credits_earned)
        self.capture_step("open_credits", "Opened Swing Credits earnings")

    def tap_change_payment(self):
        self.click(L.button_change_payment)
        self.capture_step("change_payment", "Tapped Change payment")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("confirmation_back", "Tapped back")

    def add_player(self):
        self.click(L.button_add_player)
        self.capture_step("add_player", "Tapped Add a player")

    def verify_player(self, name: str):
        assert self.is_visible(L.player_card_by_name % name, timeout=15), f"Player '{name}' not added"
        self.capture_step("verify_player", f"Player added: {name}")

    def change_player(self):
        self.click(L.button_change_player)
        self.capture_step("change_player", "Tapped Change player")

    def remove_player(self):
        self.click(L.button_remove_player)
        self.capture_step("remove_player", "Tapped Remove player")

    def toggle_swing_credits(self):
        self.scroll_to_element(L.switch_swing_credits)
        el = self.find(L.switch_swing_credits)
        r = el.rect  # {'x','y','width','height'}
        x = r["x"] + r["width"] - max(30, int(r["width"] * 0.08))
        y = r["y"] + max(30, int(r["height"] * 0.14))
        self.driver.execute_script("mobile: clickGesture", {"x": x, "y": y})
        self.capture_step("swing_credits", "Toggled Use Swing Credits (tapped toggle)")

    def is_swing_credits_on(self) -> bool:
        return self.find(L.switch_swing_credits).get_attribute("checked") == "true"

    def open_redeem_swing_credits(self):
        self.click(L.button_redeem_swing_credits)
        self.capture_step("open_redeem", "Opened Redeem Swing Credits")

    def tap_redeem_swing_credits(self):
        self.click(L.button_redeem_swing_credits)
        self.capture_step("redeem_swing_credit", "Tap Redeem Swing Credits")

    def open_addons(self):
        self.click(L.row_addons)
        self.capture_step("open_addons", "Opened Select add-ons")
    
    def get_promo_auto_applied(self, player_name: str) -> str:
        promo_name = self._desc(L.button_add_promo % player_name).strip()
        print(f"Promo Name: {promo_name!r} \n xpath {L.button_add_promo % player_name}")
        return promo_name

    def open_promo(self, player_name: str):
        self.click(L.button_add_promo % player_name)
        self.capture_step("open_promo", f"Opened promo picker for '{player_name}'")

    def add_notes(self, text: str):
        self.fill(L.input_notes, text)
        self.capture_step("add_notes", f"Added notes: {text}")

    def tap_select_payment(self):
        self.click(L.button_select_payment)
        self.capture_step("select_payment", "Tapped Select payment")

    def is_pay_now_enabled(self) -> bool:
        return self.is_enabled(L.button_pay_now)

    def tap_pay_now(self):
        self.click(L.button_pay_now)
        self.capture_step("pay_now", "Tapped Pay now")
