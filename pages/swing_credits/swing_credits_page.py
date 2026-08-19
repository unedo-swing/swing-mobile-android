from core.android_base_page import AndroidBasePage
from locators.swing_credits.swing_credits_locators import SwingCreditsLocators as L


class SwingCreditsPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Swing Credits screen not shown"
        self.capture_step("swing_credits", "Swing Credits screen is visible")

    def verify_redeem_section(self):
        assert self.is_visible_after_scroll(L.label_redeem_section), \
            "'Redeem your Swing Credits' section not shown"
        self.capture_step("credits_redeem_section", "Redeem your Swing Credits section is visible")

    # ================= reading values =================
    def _desc(self, locator) -> str:
        return self.scroll_and_find(locator).get_attribute("content-desc") or ""

    def get_balance(self) -> str:
        balance = self._desc(L.value_balance)
        self.capture_step("credits_balance", f"Balance: {balance}")
        return balance

    def verify_balance(self, expected: str):
        actual = self.get_balance()
        assert actual == expected, f"Balance is '{actual}', expected '{expected}'"

    def is_always_use_enabled(self) -> bool:
        switch = self.scroll_and_find(L.switch_always_use)
        return switch.get_attribute("checked") == "true"

    def get_reward_names(self) -> list:
        return [
            e.get_attribute("content-desc") or ""
            for e in self.find_all(L.reward_card_any)
        ]

    # ================= action steps =================
    def toggle_always_use(self):
        self.click(L.switch_always_use)
        self.capture_step("credits_always_use_toggled", "Toggled Always use Swing Credits")

    def set_always_use(self, on: bool):
        if self.is_always_use_enabled() == on:
            self.capture_step(
                "credits_always_use", f"Always use Swing Credits already {'on' if on else 'off'}"
            )
            return
        self.toggle_always_use()
        actual = self.is_always_use_enabled()
        assert actual == on, f"Always use Swing Credits is {actual}, expected {on}"

    def open_redeem_sheet(self):
        self.click(L.button_redeem_credits)
        self.capture_step("credits_open_redeem", "Opened Redeem Swing Credits sheet")

    def open_cashbacks(self):
        self.click(L.button_see_all_cashbacks)
        self.capture_step("credits_see_cashbacks", "Tapped See all cashbacks")

    def open_learn_more(self):
        self.click(L.button_learn_more)
        self.capture_step("credits_learn_more", "Tapped Learn more")

    def open_history(self):
        self.click(L.button_see_history)
        self.capture_step("credits_see_history", "Tapped See history")

    def open_reward(self, name: str):
        self.click(L.reward_card_by_name % name)
        self.capture_step("credits_open_reward", f"Opened reward '{name}'")

    def change_region(self, code: str = "ID"):
        self.click(L.button_region_by_code % code)
        self.capture_step("credits_region", f"Tapped region '{code}'")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("credits_back", "Left the Swing Credits screen")
