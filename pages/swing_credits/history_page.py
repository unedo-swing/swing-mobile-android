from core.android_base_page import AndroidBasePage
from locators.swing_credits.history_locators import HistoryLocators as L
import re


class HistoryPage(AndroidBasePage):

    FILTERS = [L.FILTER_ALL, L.FILTER_EARNED, L.FILTER_USAGE]

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Swing Credits history screen not shown"
        self.capture_step("credits_history")

    def verify_filters(self):
        missing = [f for f in self.FILTERS if not self.is_visible(L.chip_by_label % f)]
        self.capture_step("history_filters", "Filter chips are shown" if not missing
                          else f"missing: {', '.join(missing)}")
        assert not missing, f"Filter chip(s) not shown: {missing}"
    
    def verify_credit_using_referral(self):
        assert self.is_visible(L.list_credit_by_reward_by_using_refferal), "Nothing Using The Refferal"

    def verify_not_visible_credit_using_referral(self):
        gone = self.is_not_visible(L.list_credit_by_reward_by_using_refferal)
        self.capture_step("history_no_credit_using_referral",
                          "No 'Reward for using' credit in the history" if gone
                          else "'Reward for using' credit is still listed")
        assert gone, "Credit for using the referral code is listed but should not be"
    
    def verify_credit_reward_for_referral(self):
        assert self.is_visible(L.list_credit_by_reward_for_refferal), "Nothing Using Your Referral"

    

    # ================= action steps =================
    def select_filter_all(self):
        self.click(L.chip_all)
        self.capture_step("Click Filter All History Swing Credit")
    
    def select_filter_earn(self):
        self.click(L.chip_earned)
        self.capture_step("Click Filter Credits Earned History Swing Credit")
    
    def select_filter_usage(self):
        self.click(L.chip_usage)
        self.capture_step("Click Filter Credits Usage History Swing Credit")

    @staticmethod
    def booking_code(booking_id: str) -> str:
        return (booking_id or "").split("#")[-1].strip()

    @staticmethod
    def credit_amount(total_credits: str) -> str:
        return re.sub(r"\s+", "", total_credits or "")

    def get_entry(self, booking_id: str) -> str:
        code = self.booking_code(booking_id)
        if not code:
            return ""
        element = self.find_anywhere(L.entry_by_booking_id % f"#{code}")
        return (element.get_attribute("content-desc") or "") if element is not None else ""

    def verify_credit(self, booking_id: str, total_credits: str = ""):
        code = self.booking_code(booking_id)
        credit = self.credit_amount(total_credits)
        assert code, f"No booking id to look up in the credit history, got {booking_id!r}"
        assert credit, f"No credits total to check for booking #{code}, got {total_credits!r}"

        element = self.find_anywhere(L.entry_by_booking_id_and_credit % (f"#{code}", credit))
        entry = (element.get_attribute("content-desc") or "") if element is not None else ""
        self.capture_step("history_credit",
                          f"#{code} {credit}: {entry.replace(chr(10), ' ') or 'no entry found'}")

        if element is None:
            listed = self.get_entry(code)
            assert listed, f"No credit history entry for booking #{code}"
            assert False, \
                f"Credit history entry for booking #{code} reads " \
                f"{listed.replace(chr(10), ' ')!r}, expected {total_credits!r}"
        return entry

    def open_entry(self, booking_id: str):
        self.click(L.entry_by_booking_id % booking_id)
        self.capture_step("history_open_entry", f"Opened history entry #{booking_id}")

    def open_referral_reward(self):
        self.click(L.entry_referral)
        self.capture_step("history_open_referral")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("history_back")
    
    def tap_filter_credit_used(self):
        self.click(L.chip_usage)
        self.capture_step("Click Filter Swing Used")
    
    def tap_filter_credit_earning(self):
        self.click(L.chip_earned)
        self.capture_step("Click Filter Swing Earn")
        
    
