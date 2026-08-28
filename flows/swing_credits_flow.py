from flows.base_flow import BaseFlow
from pages.home_page import HomePage
from pages.swing_credits.swing_credits_page import SwingCreditsPage
from pages.swing_credits.history_page import HistoryPage
from pages.swing_credits.cashbacks_page import CashbacksPage
from pages.swing_credits.referral_reward_details_page import ReferralRewardDetailsPage
from pages.tee_time.redeem_swing_credits_page import RedeemSwingCreditsPage


class SwingCreditsFlow(BaseFlow):
    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.home = self.page(HomePage)
        self.credits = self.page(SwingCreditsPage)
        self.history = self.page(HistoryPage)
        self.referral_details = self.page(ReferralRewardDetailsPage)
        self.cashbacks = self.page(CashbacksPage)
        self.redeem = self.page(RedeemSwingCreditsPage)

    # ================= open =================
    def get_balance(self) -> str:
        return self.credits.get_balance()

    def verify_balance(self, expected: str):
        self.credits.verify_balance(expected)

    # ================= history =================
    def open_history(self):
        self.credits.open_history()
        self.history.verify_screen()
        self.history.verify_filters()

    def check_credits_earned(self, allow_empty: bool = False) -> list:
        self.history.select_filter(self.history.FILTERS[1])   # Credits Earned
        self.history.verify_all_entries_are("earned", allow_empty=allow_empty)
        return self.history.get_entries()

    def check_credits_used(self, allow_empty: bool = False) -> list:
        self.history.select_filter(self.history.FILTERS[2])   # Credits Usage
        self.history.verify_all_entries_are("used", allow_empty=allow_empty)
        return self.history.get_entries()

    # ================= referral signup reward =================
    def get_referral_reward(self) -> dict | None:
        return self.history.get_referral_reward()

    def verify_referral_reward(self, amount: str | None = None, referrer: str | None = None):
        self.history.verify_referral_reward(amount=amount, referrer=referrer)

    def check_referral_reward(self, amount: str | None = None,
                              referrer: str | None = None) -> dict | None:
        self.open_history()
        self.history.select_filter(self.history.FILTERS[1])   # Credits Earned
        self.verify_referral_reward(amount=amount, referrer=referrer)
        return self.get_referral_reward()

    def go_back_to_home(self):
        self.history.tap_back()
        self.credits.tap_back()

    def open_referral_reward_details(self):
        self.history.open_referral_reward()
        self.referral_details.verify_screen()

    def verify_referral_reward_details(self, amount: str | None = None,
                                       referrer: str | None = None,
                                       expiry: str | None = None,
                                       earned_on: str | None = None) -> dict:
        self.referral_details.verify_screen()
        if referrer:
            self.referral_details.verify_referrer(referrer)
        self.referral_details.verify_details(amount=amount, expiry=expiry, earned_on=earned_on)
        self.referral_details.verify_support_section()
        return self.referral_details.get_details()

    def check_referral_reward_details(self, amount: str | None = None,
                                      referrer: str | None = None,
                                      expiry: str | None = None,
                                      earned_on: str | None = None) -> dict:
        self.open_referral_reward_details()
        details = self.verify_referral_reward_details(
            amount=amount, referrer=referrer, expiry=expiry, earned_on=earned_on,
        )
        self.referral_details.tap_back()
        self.history.verify_screen()
        return details

    def check_all_history(self) -> list:
        self.history.select_filter(self.history.FILTERS[0])
        return self.history.get_entries()

    def verify_history_entry(self, booking_id: str, **expected):
        self.history.verify_entry(booking_id, **expected)

    def leave_history(self):
        self.history.tap_back()
        self.credits.verify_screen()

    # ================= cashbacks =================
    def open_cashbacks(self):
        self.credits.open_cashbacks()
        self.cashbacks.verify_screen()

    def leave_cashbacks(self):
        self.cashbacks.tap_back()
        self.credits.verify_screen()

    # ================= redeem a code =================
    def open_redeem_sheet(self):
        self.credits.open_redeem_sheet()
        self.redeem.verify_screen()

    def redeem_code(self, code: str):
        self.open_redeem_sheet()
        self.redeem.redeem(code)

    def verify_swing_credits_page(self) -> str:
        self.credits.verify_screen()
        balance = self.credits.get_balance()
        self.credits.verify_redeem_section()
        return balance

    def verify_earned_credit(self, booking_code: str, total_credits: str = ""):
        self.history.tap_filter_credit_earning()
        self.history.verify_credit(booking_code, total_credits)

    def verify_used_credit(self, booking_code: str, total_credits: str = ""):
        self.history.tap_filter_credit_used()
        self.history.verify_credit(booking_code, total_credits)

    def check_earned_credit(self, booking_code: str, total_credits: str = ""):
        self.open_swing_credits()
        self.open_history()
        self.verify_earned_credit(booking_code, total_credits)

    def check_used_credit(self, booking_code: str, total_credits: str = ""):
        self.open_swing_credits()
        self.open_history()
        self.verify_used_credit(booking_code, total_credits)

    def verify_credits(self, code_booking: str, tot_credits: str):
        self.verify_earned_credit(code_booking, tot_credits)
    
    def verify_history_credit_using_referral(self, region: str):
        self.home.open_swing_credits()
        self.credits.verify_screen()
        self.credits.open_history()
        self.history.select_filter_earn()
        self.history.verify_credit_using_referral()
        
        # check the other region will not have credit using referral
        self.history.tap_back()
        region_change = "MY" if region == "ID" else "ID"
        self.credits.change_region(region_change)
        self.credits.verify_screen()
        self.credits.open_history()
        self.history.select_filter_earn()
        self.history.verify_not_visible_credit_using_referral()
        self.history.tap_back()
        self.credits.tap_back()
        
    
