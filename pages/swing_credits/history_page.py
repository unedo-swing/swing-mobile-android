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

    @staticmethod
    def parse_entry(desc: str) -> dict:
        lines = [line.strip() for line in (desc or "").split("\n") if line.strip()]
        entry = {"type": "", "booking_id": "", "time": "", "amount": "", "direction": "",
                 "label": desc or ""}
        if lines:
            entry["type"] = lines[0]
        if len(lines) >= 2:
            middle = lines[1]
            if "•" in middle:
                left, _, right = middle.partition("•")
                entry["booking_id"] = left.strip().lstrip("#")
                entry["time"] = right.strip()
            else:
                entry["time"] = middle
        if len(lines) >= 3:
            entry["amount"] = lines[2]
        if len(lines) >= 4:
            entry["direction"] = lines[3]
        return entry

    # ================= reading =================
    def get_entries(self) -> list:
        entries = [
            self.parse_entry(e.get_attribute("content-desc") or "")
            for e in self.find_all(L.entry_any)
        ]
        self.capture_step("history_entries", f"{len(entries)} entr(y/ies) listed",
                          data={"entries": entries})
        return entries

    def get_dates(self) -> list:
        return [
            e.get_attribute("content-desc") or ""
            for e in self.find_all(L.group_any)
        ]

    def get_entry(self, booking_id: str) -> dict:
        element = self.find_anywhere(L.entry_by_booking_id % booking_id)
        assert element is not None, f"No history entry for booking '{booking_id}'"
        entry = self.parse_entry(element.get_attribute("content-desc") or "")
        self.capture_step("history_entry", f"Entry #{booking_id}", data=entry)
        return entry

    def get_entries_for_date(self, date: str) -> list:
        return [
            self.parse_entry(e.get_attribute("content-desc") or "")
            for e in self.find_all(L.entries_in_group % date)
        ]

    def get_referral_reward(self) -> dict | None:
        element = self.find_anywhere(L.entry_referral_reward)
        if element is None:
            return None
        entry = self.parse_entry(element.get_attribute("content-desc") or "")
        self.capture_step("history_referral", data=entry)
        return entry

    # ================= verify =================
    def verify_entry(self, booking_id: str, **expected):
        actual = self.get_entry(booking_id)
        mismatches = {
            field: (want, actual.get(field, ""))
            for field, want in expected.items()
            if want and want.strip().casefold() != (actual.get(field, "") or "").strip().casefold()
        }
        assert not mismatches, (
            f"History entry #{booking_id} does not match:\n"
            + "\n".join(
                f"  {field}: expected '{want}' but entry reads '{got}'"
                for field, (want, got) in mismatches.items()
            )
        )

    def verify_all_entries_are(self, direction: str, allow_empty: bool = False):
        entries = self.get_entries()
        if not entries:
            if allow_empty:
                self.capture_step("history_empty", f"No '{direction}' entries listed (allowed)")
                return
            raise AssertionError("No history entries listed")
        wrong = [e for e in entries if e["direction"].casefold() != direction.casefold()]
        assert not wrong, (
            f"{len(wrong)} of {len(entries)} entries are not '{direction}': "
            + ", ".join(f"#{e['booking_id'] or '?'} ({e['direction']})" for e in wrong)
        )

    def verify_referral_reward(self, amount: str | None = None, referrer: str | None = None):
        entry = self.get_referral_reward()
        assert entry is not None, "No referral reward entry in the credits history"

    def verify_date_group(self, date: str):
        assert self.find_anywhere(L.group_by_date % date) is not None, \
            f"Date group '{date}' not shown"
        self.capture_step("history_date_group", f"Date group '{date}' is shown")

    # ================= action steps =================
    def select_filter(self, label: str):
        self.click(L.chip_by_label % label)
        self.wait_until_loaded()
        self.capture_step("history_filter", f"Selected filter '{label}'")

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
        
    @staticmethod
    def booking_code(value: str) -> str:
        match = re.search(r"#([A-Za-z0-9_-]+)", value or "")
        code = match.group(1) if match else (value or "").strip()
        return f"#{code}" if code else ""

    def verify_credit(self, code_booking: str, tot_credits: str = ""):
        code = self.booking_code(code_booking)
        assert code, f"No booking code to look for in '{code_booking}'"
        entry = L.list_credit_by_booking_code % code
        assert self.is_visible(entry), f"No Swing Credits entry for booking '{code}'"
        desc = self._desc(entry)
        self.capture_step("history_credit_entry", f"{code} | {desc}")
        if tot_credits:
            assert tot_credits in desc, (
                f"Entry for '{code}' reads '{desc}', expected credits '{tot_credits}'"
            )
    
    def verify_credit_using_referral(self):
        assert self.is_visible(L.list_credit_by_reward_by_using_refferal), "Nothing Using The Refferal"
    
    def verify_credit_reward_for_referral(self):
        assert self.is_visible(L.list_credit_by_reward_for_refferal), "Nothing Using Your Referral"
