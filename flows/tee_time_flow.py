from flows.base_flow import BaseFlow
from pages.home_page import HomePage
from pages.tee_time.explore_page import ExplorePage
from pages.tee_time.golf_course_details_page import GolfCourseDetailsPage
from pages.tee_time.booking_method_page import BookingMethodPage
from pages.tee_time.booking_confirmation_page import BookingConfirmationPage
from pages.tee_time.booking_confirmed_page import BookingConfirmedPage
from pages.tee_time.booking_details_page import BookingDetailsPage
from pages.tee_time.booking_summary_page import BookingSummaryPage
from pages.tee_time.receipt_page import ReceiptPage
from pages.tee_time.add_player_page import AddPlayerPage
from pages.tee_time.payment_method_page import PaymentMethodPage
from pages.tee_time.promo_page import PromoPage
from pages.tee_time.switch_group_booking_page import SwitchGroupBookingPage
from pages.tee_time.swing_credits_earnings_page import SwingCreditsEarningsPage


class TeeTimeFlow(BaseFlow):
    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.home = self.page(HomePage)
        self.explore = self.page(ExplorePage)
        self.details = self.page(GolfCourseDetailsPage)
        self.booking_method = self.page(BookingMethodPage)
        self.booking_confirmation = self.page(BookingConfirmationPage)
        self.player = self.page(AddPlayerPage)
        self.payment_method = self.page(PaymentMethodPage)
        self.promo = self.page(PromoPage)
        self.switch_group = self.page(SwitchGroupBookingPage)
        self.credits = self.page(SwingCreditsEarningsPage)
        self.confirmed = self.page(BookingConfirmedPage)
        self.booking_details = self.page(BookingDetailsPage)
        self.booking_summary = self.page(BookingSummaryPage)
        self.receipt = self.page(ReceiptPage)

    # --- steps ---
    def select_region(self, region: str):
        self.home.tap_select_region()
        self.home.verify_bottom_sheet_select_region()
        self.home.select_region(region)

    def open_tee_time(self):
        self.home.open_tee_time()
        self.explore.verify_screen()

    def search_and_open_course(self, course_name: str):
        self.explore.search_course(course_name)
        self.explore.verify_results_shown(course_name)
        self.explore.open_course(course_name)
        self.details.verify_screen()
        self.details.verify_course_name(course_name)

    def pick_date_from_calendar(self, course_name: str, calendar_date: str):
        self.details.open_calendar(course_name)
        self.details.select_date_in_calendar(calendar_date)
    
    def select_preferred_time(self, preferred_time: str):
        self.details.select_time_slot(preferred_time)

    def start_standard_booking(self):
        self.details.tap_book()
        self.booking_method.verify_screen()
        self.booking_method.select_standard_booking()
        self.booking_confirmation.verify_screen()   # wait for the new page

    # --- add player (from the booking confirmation) ---
    def open_add_player(self):
        self.booking_confirmation.add_player()
        self.player.verify_screen()

    def add_player_manually(self, first_name: str, last_name: str, phone: str, email: str | None = None):
        self.open_add_player()
        self.player.select_add_manually_tab()
        self.player.fill_manually(first_name, last_name, phone, email)
        self.player.tap_save_player()

    def add_players(self, players: list[dict]):
        for player in players:
            method = player.get("method", "manual")
            if method == "search":
                name = player["name"]
                self.search_and_add_player(name)
            else:
                name = f'{player["first_name"]} {player["last_name"]}'
                self.add_player_manually(
                    player["first_name"],
                    player["last_name"],
                    player["phone"],
                    player.get("email"),
                )
            # keep a standard booking if adding a player prompts to switch to group
            self.handle_switch_group_prompt(switch=False)
            self.verify_player_added(name)   # verify each player was added
            # promo per player: apply the given one, or drop any auto-applied one.
            self.apply_or_remove_promo(name, player.get("promo"))

    def apply_or_remove_promo(self, player_name: str, promo: str | None = None):
        if promo:
            self.change_promo(player_name, promo)
        else:
            self.remove_promo(player_name)

    def verify_player_added(self, name: str):
        self.booking_confirmation.verify_player(name)

    def handle_switch_group_prompt(self, switch: bool = False):
        if self.switch_group.is_shown():
            if switch:
                self.switch_group.switch_to_group()
            else:
                self.switch_group.keep_standard()

    def search_and_add_player(self,friend_name: str):
        self.open_add_player()
        self.player.select_search_friend_tab()
        self.player.search_friend(friend_name)
        self.player.select_friend_result(friend_name)

    # --- change payment method (from the booking confirmation) ---
    def change_payment_card(self, card_name: str):
        self.booking_confirmation.tap_select_payment()
        self.payment_method.verify_screen()
        self.payment_method.select_card(card_name)
        self.booking_confirmation.verify_screen()   # wait for return

    def change_payment_method(self, payment_method: str):
        self.booking_confirmation.tap_select_payment()
        self.payment_method.verify_screen()
        self.payment_method.select_payment_method(payment_method)
        self.booking_confirmation.verify_screen()   # wait for return

    def change_payment_qris(self):
        self.booking_confirmation.tap_select_payment()
        self.payment_method.verify_screen()
        self.payment_method.select_qris()
        self.booking_confirmation.verify_screen()   # wait for return

    def change_promo(self, player_name: str, promo_name: str):
        promo_auto_applied = self.booking_confirmation.get_promo_auto_applied(player_name)
        if promo_name not in promo_auto_applied:
            self.booking_confirmation.open_promo(player_name)
            self.promo.verify_screen()
            self.promo.remove_promo()
            self.promo.search_promo(promo_name)
            self.promo.apply_promo(promo_name)
    
    def remove_promo(self, player_name: str):
        promo_auto_applied = self.booking_confirmation.get_promo_auto_applied(player_name)
        if promo_auto_applied != "Apply a promo":
            self.booking_confirmation.open_promo(player_name)
            self.promo.verify_screen()
            self.promo.remove_promo()

    def add_promo_code(self, player_name: str, code: str):
        self.booking_confirmation.open_promo(player_name)
        self.promo.verify_screen()
        self.promo.add_promo_code(code)

    def verify_auto_applied_promo(self, player_name: str) -> str:
        """Assert a promo is auto-applied to a player's card and return it."""
        promo = (self.booking_confirmation.get_promo_auto_applied(player_name) or "").strip()
        print(promo)
        assert promo, f"No promo auto-applied for '{player_name}'"
        self.booking_confirmation.capture_step(
            "verify_auto_promo", f"Auto-applied promo for {player_name}: {promo}"
        )
        return promo

    # --- verify: pre-payment booking confirmation screen ---
    def verify_booking_confirmation(self, date: str | None = None, session: str | None = None,
                                    preferred_time: str | None = None):
        """Assert the booking confirmation screen is shown and (optionally) that
        its summary matches the expected date / session / preferred time."""
        self.booking_confirmation.verify_screen()
        self.booking_confirmation.verify_booking_details(
            date=date, session=session, preferred_time=preferred_time
        )

    def verify_before_payment(self, venue_name: str | None = None, date: str | None = None,
                              session: str | None = None, preferred_time: str | None = None,
                              player_names: list[str] | None = None, total_players: int | None = None,
                              total_payment: str | None = None) -> dict:
        return self.booking_confirmation.verify_before_payment(
            venue_name=venue_name, date=date, session=session, preferred_time=preferred_time,
            player_names=player_names, total_players=total_players, total_payment=total_payment,
        )

    # --- pay ---
    def pay_now(self):
        """Pay the tee-time booking from the booking confirmation."""
        assert self.booking_confirmation.is_pay_now_enabled(), "Pay now is disabled"
        self.booking_confirmation.tap_pay_now()

    # --- verify: post-payment "You're confirmed!" screen ---
    def verify_confirmed_booking(self, course_name: str | None = None, date: str | None = None,
                                 session: str | None = None, preferred_time: str | None = None,
                                 no_of_players=None, total: str | None = None,
                                 payment_method: str | None = None) -> str:
        """Assert the confirmed ('You're confirmed!') screen and its summary.
        Only non-None fields are asserted; a booking id is always required.
        Returns the booking id."""
        self.confirmed.verify_screen()
        return self.confirmed.verify_confirmed_details(
            course_name=course_name, date=date, session=session,
            preferred_time=preferred_time, no_of_players=no_of_players,
            total=total, payment_method=payment_method,
        )

    def finish_confirmed_booking(self):
        """Tap Finish on the confirmed screen."""
        self.confirmed.tap_finish()

    def open_confirmed_booking_details(self):
        """Tap 'See booking details' on the confirmed screen -> Booking details."""
        self.confirmed.tap_see_booking_details()
        self.booking_details.verify_screen()

    # --- verify: Booking details screen (from 'See booking details') ---
    def verify_booking_details_screen(self, status: str | None = None, date: str | None = None,
                                      session: str | None = None, preferred_time: str | None = None,
                                      no_of_players=None, total_payment: str | None = None,
                                      booking_id: str | None = None) -> str:
        """Assert the Booking details screen and its summary. Only non-None fields
        are asserted; a booking id is always required. Returns the booking id."""
        self.booking_details.verify_screen()
        return self.booking_details.verify_details(
            status=status, date=date, session=session, preferred_time=preferred_time,
            no_of_players=no_of_players, total_payment=total_payment, booking_id=booking_id,
        )

    def open_complete_breakdown(self):
        """Tap 'See complete breakdown' on the Booking details screen -> Booking summary."""
        self.booking_details.tap_see_complete_breakdown()
        self.booking_summary.verify_screen()

    # --- verify: Booking summary screen (from 'See complete breakdown') ---
    def verify_booking_summary(self, course_name: str | None = None, date: str | None = None,
                               session: str | None = None, preferred_time: str | None = None,
                               booking_type: str | None = None, total_payment: str | None = None):
        """Assert the Booking summary screen and (optionally) its fields."""
        self.booking_summary.verify_screen()
        self.booking_summary.verify_summary_details(
            course_name=course_name, date=date, session=session, preferred_time=preferred_time,
            booking_type=booking_type, total_payment=total_payment,
        )

    def verify_player_in_summary(self, player_name: str):
        """Assert a player's card is shown on the Booking summary screen."""
        self.booking_summary.verify_player_summary(player_name)

    def open_receipt(self):
        """Tap 'See receipt' on the Booking details screen -> Receipt."""
        self.booking_details.tap_see_receipt()
        self.receipt.verify_screen()

    # --- verify: Receipt screen (from 'See receipt') ---
    def verify_receipt(self, course_name: str | None = None, booking_id: str | None = None,
                       date: str | None = None, session: str | None = None,
                       preferred_time: str | None = None, no_of_players=None,
                       total: str | None = None, payment_method: str | None = None) -> str:
        """Assert the Receipt screen and (optionally) its fields. Only non-None
        args are asserted; a receipt id is always required. Returns the receipt id."""
        self.receipt.verify_screen()
        return self.receipt.verify_receipt_details(
            course_name=course_name, booking_id=booking_id, date=date, session=session,
            preferred_time=preferred_time, no_of_players=no_of_players,
            total=total, payment_method=payment_method,
        )

    def send_receipt(self):
        """Tap 'Send receipt' on the Receipt screen."""
        self.receipt.tap_send_receipt()

    def contact_support(self):
        """Tap 'Contact Swing support' on the Receipt screen."""
        self.receipt.tap_contact_support()

    # --- credits ---
    def get_total_credits(self) -> str:
        """The total Swing Credits earned shown on the booking confirmation bar,
        e.g. '+ 100,000 (for all)'."""
        return self.booking_confirmation.get_credits_earned()

    def get_player_credits(self, player_name: str) -> str:
        """Open the Swing Credits earnings dialog, read a player's credits (e.g.
        '+50,000'), then close it."""
        self.booking_confirmation.open_credits_earnings()
        self.credits.verify_screen()
        amount = self.credits.get_player_credit(player_name)
        self.credits.tap_got_it()
        return amount
