from core.android_base_page import AndroidBasePage
from locators.swing_credits.swing_credits_locators import SwingCreditsLocators as L


class SwingCreditsPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Swing Credits screen not shown"
        self.capture_step("swing_credits")

    def verify_redeem_section(self):
        assert self.is_visible_after_scroll(L.label_redeem_section), \
            "'Redeem your Swing Credits' section not shown"
        self.capture_step("credits_redeem_section")

    def verify_bottom_region_swing_credits(self):
        assert self.is_visible(L.label_select_country_swing_credit), "Bottom Sheet Select Region is not shown"
        self.capture_step("Verify Bottom Sheet Select Region")

    # ================= action steps =================
    def toggle_always_use(self):
        self.click(L.switch_always_use)
        self.capture_step("credits_always_use_toggled")

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
        self.capture_step("credits_open_redeem")

    def open_cashbacks(self):
        self.click(L.button_see_all_cashbacks)
        self.capture_step("credits_see_cashbacks")

    def open_learn_more(self):
        self.click(L.button_learn_more)
        self.capture_step("credits_learn_more")

    def open_history(self):
        self.click(L.button_see_history)
        self.capture_step("credits_see_history")

    def open_reward(self, name: str):
        self.click(L.reward_card_by_name % name)
        self.capture_step("credits_open_reward", f"Opened reward '{name}'")

    def change_region(self, region: str):
        self.click(L.button_region)
        self.verify_bottom_region_swing_credits()
        if region == "ID":
            country = "Indonesia"
        elif region == "MY":
            country = "Malaysia"
        else:
            country = "Indonesia"
        self.click(L.button_selected_region % region)
        self.capture_step(f"Select Region {country} Swing Credits ")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("credits_back")
