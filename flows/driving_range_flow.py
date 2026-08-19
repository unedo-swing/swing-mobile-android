import re

from flows.base_flow import BaseFlow
from pages.home_page import HomePage
from pages.driving_range.explore_page import DrivingRangeExplorePage
from pages.driving_range.details_page import DrivingRangeDetailsPage
from pages.driving_range.select_bays_page import SelectBaysPage
from pages.driving_range.booking_confirmation_page import (
    NO_PROMO_LABEL,
    DrivingRangeBookingConfirmationPage,
)
from pages.driving_range.booking_success_page import DrivingRangeBookingSuccessPage
from pages.driving_range.booking_details_page import DrivingRangeBookingDetailsPage
from pages.activity_page import ActivityPage
from pages.driving_range.change_booking_page import DrivingRangeChangeBookingPage
from pages.driving_range.reschedule_booking_page import DrivingRangeRescheduleBookingPage
from pages.driving_range.confirm_reschedule_page import DrivingRangeConfirmReschedulePage
from pages.driving_range.reschedule_success_page import DrivingRangeRescheduleSuccessPage
from pages.driving_range.confirm_cancellation_page import DrivingRangeConfirmCancellationPage
from pages.driving_range.select_bank_page import SelectBankPage
from pages.driving_range.cancel_success_page import DrivingRangeCancelSuccessPage
from pages.driving_range.cancellation_details_page import DrivingRangeCancellationDetailsPage
from pages.tee_time.promo_page import PromoPage
from pages.tee_time.payment_method_page import PaymentMethodPage
from pages.tee_time.swing_credits_earnings_page import SwingCreditsEarningsPage
from pages.featured_promos_page import FeaturedPromosPage


# --- booking-confirmation vs confirmed-booking comparison -------------------
# The two screens word the same value differently ("60 min" vs "60 minutes",
# "2" vs "2 bay", "Rp. 40,000" vs "Rp 40.000"), so each field is compared on
# what it actually means rather than on the raw string.
_NUMBER_FIELDS = ("duration", "bays")
_AMOUNT_FIELDS = ("total",)
# promo and credits are only broken out on the confirmation screen, so there is
# nothing on the confirmed booking to compare them against
_CONFIRMATION_ONLY_FIELDS = ("promo", "credits_used", "credits_earned")


def _norm(value: str) -> str:
    return " ".join((value or "").split()).casefold()


def _digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def _first_number(value: str) -> str:
    match = re.search(r"\d+", value or "")
    return match.group() if match else ""


def _card_date(date_text: str) -> str:
    from datetime import datetime
    for fmt in ("%d %B %Y", "%d %b %Y"):
        try:
            dt = datetime.strptime((date_text or "").strip(), fmt)
            return f"{dt.day} {dt.strftime('%b')} {dt.year}"
        except (ValueError, AttributeError):
            continue
    return date_text


def _duration_label(start: str, end: str) -> str:
    from datetime import datetime
    fmt = "%H:%M"
    delta = datetime.strptime(end.strip(), fmt) - datetime.strptime(start.strip(), fmt)
    minutes = int(delta.total_seconds() // 60)
    if minutes <= 0:  # start == end -> one 60-minute slot
        minutes = 60
    return f"{minutes} min"


def _same(field: str, before: str, after: str) -> bool:
    if field in _NUMBER_FIELDS:
        left, right = _first_number(before), _first_number(after)
    elif field in _AMOUNT_FIELDS:
        left, right = _digits(before), _digits(after)
    else:
        left, right = _norm(before), _norm(after)
    return bool(left) and left == right


def compare_booking(before: dict, after: dict) -> dict:
    return {
        field: (before.get(field, ""), after.get(field, ""))
        for field in before
        if field not in _CONFIRMATION_ONLY_FIELDS
        and not _same(field, before.get(field, ""), after.get(field, ""))
    }


class DrivingRangeFlow(BaseFlow):
    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.home = self.page(HomePage)
        self.explore = self.page(DrivingRangeExplorePage)
        self.details = self.page(DrivingRangeDetailsPage)
        self.bays = self.page(SelectBaysPage)
        self.booking_confirmation = self.page(DrivingRangeBookingConfirmationPage)
        self.success = self.page(DrivingRangeBookingSuccessPage)
        self.booking_details = self.page(DrivingRangeBookingDetailsPage)
        self.activity = self.page(ActivityPage)
        self.change_booking = self.page(DrivingRangeChangeBookingPage)
        self.reschedule_booking = self.page(DrivingRangeRescheduleBookingPage)
        self.confirm_reschedule = self.page(DrivingRangeConfirmReschedulePage)
        self.reschedule_success = self.page(DrivingRangeRescheduleSuccessPage)
        self.confirm_cancellation = self.page(DrivingRangeConfirmCancellationPage)
        self.select_bank = self.page(SelectBankPage)
        self.cancel_success = self.page(DrivingRangeCancelSuccessPage)
        self.cancellation_details = self.page(DrivingRangeCancellationDetailsPage)
        self.promo = self.page(PromoPage)               
        self.payment_method = self.page(PaymentMethodPage)  
        self.credits = self.page(SwingCreditsEarningsPage)
        self.featured_promos = self.page(FeaturedPromosPage)  

    # --- steps ---
    def select_region(self, region: str):
        self.home.tap_select_region()
        self.home.verify_bottom_sheet_select_region()
        self.home.select_region(region)

    def open_driving_range(self):
        self.home.open_driving_range()
        self.explore.verify_screen()

    def search_and_open_range(self, range_name: str):
        self.explore.search_range(range_name)
        self.explore.verify_results_loaded()
        self.explore.open_range(range_name)
        self.details.verify_screen()
        self.details.verify_range_name(range_name)
    
    def verify_featured_promo(self):
        self.details.tap_see_all_promo()
        self.featured_promos.verify_auto_claim_banner()
        self.featured_promos.get_promo_names()
        self.featured_promos.tap_back()
    
    def verify_maximum_bays(self, bays: str):
        self.details.tap_book()
        self.bays.verify_screen()
        self.bays.set_bays(bays)
        self.bays.verify_max_bays(bays)
    
    def verify_minimum_balls(self, addons: list[dict]):
        self.add_addons(addons)
        self.booking_confirmation.verify_minimum_balls()

    def select_schedule(self, name: str, date: str, bay_name: str,
                        time_start: str, time_end: str):
        self.details.select_date(name, date)
        self.details.verify_slots_loaded()
        self.details.select_bay_tab(bay_name)
        self.details.verify_slots_loaded()
        self.details.select_time(time_start, time_end)
        self.details.verify_book_enabled()

    def book_and_set_bays(self, bays: int):
        self.details.tap_book()
        self.bays.verify_screen()
        self.bays.set_bays(bays)
        self.bays.verify_confirm_enabled()
        self.bays.confirm()
        self.booking_confirmation.verify_screen()

    def verify_booking_confirmation_details(self, date: str, time_start: str,
                                            time_end: str, bays: int, bay_type: str):
        self.booking_confirmation.verify_booking_details(
            date=date, booking_time=time_start,
            duration=_duration_label(time_start, time_end),
            number_of_bays=str(bays), bay_type=bay_type,
        )

    # --- booking confirmation actions ---
    def add_addons(self, addons: list[dict]):
        if addons:
            for addon in addons:
                name = addon["add_ons_name"]
                quantity = addon["add_ons_qty"]
                self.booking_confirmation.verify_addon(name)
                self.booking_confirmation.set_addon_qty(name, quantity)
    
    def switch_on_swing_credits(self):
        self.booking_confirmation.toggle_swing_credits()

    def pay_now(self):
        self.booking_confirmation.verify_pay_now_enabled()
        self.booking_confirmation.tap_pay_now()
        self.success.verify_screen()

    def pay_and_get_confirmed_booking(self) -> dict:
        before = self.booking_confirmation.get_summary()
        self.pay_now()
        after = self.success.get_summary()

        mismatches = compare_booking(before, after)
        self.success.capture_step(
            "dr_compare_booking",
            "Confirmation matches confirmed booking" if not mismatches
            else f"{len(mismatches)} field(s) differ",
            compare={
                "left_label": "Booking confirmation",
                "right_label": "Confirmed booking",
                "before": before,
                "after": after,
                "mismatch_fields": list(mismatches.keys()),
            },
        )
        assert not mismatches, (
            "Confirmed booking does not match the booking confirmation:\n"
            + "\n".join(
                f"  {field}: confirmation='{b}' vs confirmed='{a}'"
                for field, (b, a) in mismatches.items()
            )
        )

        after["booking_id"] = self.success.verify_booking_id()
        return after

    # --- booking details (after "See booking details") ---
    def open_booking_details(self):
        self.success.tap_see_booking_details()
        self.booking_details.verify_screen()

    def verify_booking_details(self, booking_id: str | None = None, date: str | None = None,
                               booking_time: str | None = None, duration: str | None = None,
                               bays: str | None = None, bay_type: str | None = None,
                               total: str | None = None):
        self.booking_details.verify_screen()
        self.booking_details.verify_booking_id()
        self.booking_details.verify_booking_summary(
            booking_id=booking_id, date=date, booking_time=booking_time,
            duration=duration, bays=bays, bay_type=bay_type, total=total,
        )
    
    def go_back_to_activity(self):
        self.booking_details.tap_back()

    def open_and_verify_booking_details(self, confirmed: dict) -> dict:
        self.open_booking_details()
        self.verify_booking_details(
            booking_id=confirmed.get("booking_id"),
            date=confirmed.get("date"),
            booking_time=confirmed.get("booking_time"),
            duration=confirmed.get("duration"),
            bays=confirmed.get("bays"),
            bay_type=confirmed.get("bay_type"),
            total=confirmed.get("total"),
        )
        return self.booking_details.get_summary()

    def verify_confirmed(self, range_name: str | None = None, date: str | None = None,
                         booking_time: str | None = None, duration: str | None = None,
                         bays: str | None = None, bay_type: str | None = None,
                         total: str | None = None, payment_method: str | None = None):
        self.success.verify_screen()
        assert self.success.get_booking_id().startswith("Booking #"), "Booking id not shown"
        if range_name:
            self.success.verify_range_name(range_name)
        self.success.verify_booking_summary(
            date=date, booking_time=booking_time, duration=duration,
            bays=bays, bay_type=bay_type, total=total, payment_method=payment_method,
        )

    def get_credits_earned(self) -> str:
        self.booking_confirmation.open_credits_earnings()
        self.credits.verify_screen()
        amount = self.credits.get_player_credit(self.booking_confirmation.get_player_name())
        self.credits.tap_got_it()
        return amount

    def change_payment_card(self, card_name: str):
        self.booking_confirmation.tap_select_payment()
        self.payment_method.verify_screen()
        self.payment_method.select_card(card_name)
        self.booking_confirmation.verify_screen()   # wait for return

    def change_payment(self, payment_method: str):
        self.booking_confirmation.tap_select_payment()
        self.payment_method.verify_screen()
        self.payment_method.verify_payment_option(payment_method)
        self.payment_method.select_payment_method(payment_method)
        self.booking_confirmation.verify_payment_method(payment_method)

    def apply_promo(self, promo_name: str):
        applied_promo = self.booking_confirmation.verify_promo_auto_applied()
        if promo_name not in applied_promo:
            self.booking_confirmation.open_promo()
            self.promo.verify_screen()
            self.promo.apply_promo(promo_name)
            self.booking_confirmation.verify_screen()   # wait for return
        
    def change_promo_with_add_promo_code(self, promo_name: str, promo_code: str):
        applied_promo = self.booking_confirmation.verify_promo_auto_applied()
        if applied_promo != NO_PROMO_LABEL:
            self.booking_confirmation.open_promo()
            self.promo.verify_screen()
            self.promo.remove_promo()
        else:
            self.booking_confirmation.open_promo()
            self.promo.verify_screen()
        self.promo.add_promo_code(promo_code)
        self.promo.search_promo(promo_name)
        self.promo.apply_promo(promo_name)

    def remove_promo(self):
        applied_promo = self.booking_confirmation.verify_promo_auto_applied()
        if applied_promo != NO_PROMO_LABEL:
            self.booking_confirmation.open_promo()
            self.promo.verify_screen()
            self.promo.remove_promo()
            self.promo.tap_back()
            self.booking_confirmation.verify_screen()   # wait for return

    def verify_bxgy_promo(self, promo_name: str, ball_option: str, ball_qty: int,
                          bonus_balls: str, total: str | None = None):
        self.booking_confirmation.verify_balls_section()
        self.booking_confirmation.set_addon_qty(ball_option, ball_qty)
        self.apply_promo(promo_name)
        self.booking_confirmation.verify_price_details_type("Ball-based")
        self.booking_confirmation.verify_bxgy_promo(
            promo_name=promo_name, ball_option=ball_option,
            bonus_balls=bonus_balls, total=total,
        )

    def verify_promo_auto_applied(self, promo_name: str):
        self.booking_confirmation.open_promo()
        self.promo.verify_screen()
        self.promo.verify_promo(promo_name)
        assert self.promo.is_promo_applied(), \
            f"Promo '{promo_name}' is not auto-applied"
        self.promo.tap_back()
        self.booking_confirmation.verify_screen()   # wait for return

    def verify_promo_not_applied(self, promo_name: str):
        self.booking_confirmation.open_promo()
        self.promo.verify_screen()
        assert not self.promo.is_promo_applied(), \
            f"Promo '{promo_name}' is still applied"
        self.promo.tap_back()
        self.booking_confirmation.verify_screen()   # wait for return

    # --- end-to-end scenario ---
    def book_driving_range(self, region: str, range_name: str, date: str,
                           bay_name: str, time_start: str, time_end: str, bays: int):
        self.select_region(region)
        self.open_driving_range()
        self.search_and_open_range(range_name)
        self.select_schedule(range_name, date, bay_name, time_start, time_end)
        self.book_and_set_bays(bays)

    # ========================================================================
    # Activity — open a driving-range booking from the Activity screen.
    # Each step is its own function (compose them in the test; no single
    # end-to-end wrapper).
    # ========================================================================
    def open_activity(self):
        self.home.go_to_activity()
        self.activity.verify_screen()

    def open_driving_range_card(self, name: str, time_start: str, booking_date: str):
        self.activity.click_filter_activity("Driving range")
        # the card shows the date abbreviated ("11 Aug 2026"), the data is full
        # month ("11 August 2026") -> convert for the contains-match
        self.activity.click_card_activity(name, time_start, _card_date(booking_date))
        self.booking_details.verify_screen()

    # ========================================================================
    # Reschedule — one function per step.
    # ========================================================================
    def open_reschedule(self):
        self.booking_details.tap_three_dots()
        self.booking_details.tap_reschedule_booking()
        self.change_booking.verify_screen()

    def continue_reschedule(self):
        self.change_booking.select_reschedule_tab()
        self.change_booking.tap_continue_reschedule()
        self.reschedule_booking.verify_screen()

    def select_new_schedule(self, date, time_text: str):
        self.reschedule_booking.select_date(date)
        self.reschedule_booking.select_time(time_text)
        self.reschedule_booking.verify_confirm_enabled()
        self.reschedule_booking.tap_confirm_new_date()
        self.confirm_reschedule.verify_screen()

    def confirm_reschedule_reason(self, reason: str):
        self.confirm_reschedule.select_reason(reason)
        self.confirm_reschedule.verify_confirm_enabled()
        self.confirm_reschedule.tap_confirm_pay()
        self.confirm_reschedule.verify_confirm_dialog()

    def submit_reschedule(self):
        self.confirm_reschedule.dialog_confirm()
        self.reschedule_success.verify_screen()

    def verify_reschedule_success(self, range_name: str | None = None):
        self.reschedule_success.verify_screen()
        self.reschedule_success.verify_booking_id()
        if range_name:
            self.reschedule_success.verify_range_name(range_name)

    # ========================================================================
    # Cancellation — one function per step.
    # ========================================================================
    def open_cancellation(self):
        self.booking_details.tap_three_dots()
        self.booking_details.tap_cancel_booking()
        self.change_booking.verify_screen()

    def continue_cancellation(self):
        self.change_booking.select_cancellation_tab()
        self.change_booking.tap_continue_cancel()
        self.confirm_cancellation.verify_screen()
    

    def select_cancellation_reason(self, reason: str):
        self.confirm_cancellation.verify_reason_section()
        self.confirm_cancellation.select_reason(reason)

    def set_refund_bank(self, bank_name: str, account_number: str, account_name: str):
        self.confirm_cancellation.tap_select_bank()
        self.select_bank.verify_screen()
        self.select_bank.choose_bank(bank_name)
        self.confirm_cancellation.verify_screen()   # wait for return
        self.confirm_cancellation.enter_bank_account_number(account_number)
        self.confirm_cancellation.enter_bank_account_name(account_name)
        self.confirm_cancellation.hide_keyboard()

    def submit_cancellation(self):
        self.confirm_cancellation.verify_confirm_enabled()
        self.confirm_cancellation.tap_confirm_cancel()
        self.confirm_cancellation.verify_confirm_dialog()

    def confirm_cancellation_dialog(self):
        self.confirm_cancellation.dialog_confirm()
        self.cancel_success.verify_screen()

    def verify_cancel_success(self, range_name: str | None = None):
        self.cancel_success.verify_screen()
        self.cancel_success.verify_booking_id()
        if range_name:
            self.cancel_success.verify_range_name(range_name)

    def open_cancellation_details(self):
        self.cancel_success.tap_see_cancellation_details()
        self.cancellation_details.verify_screen()
