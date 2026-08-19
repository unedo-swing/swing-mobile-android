from core.android_base_page import AndroidBasePage
from locators.account_locators import AccountLocators as L


class AccountPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.link_edit_personal_info, timeout=20), "Account screen not shown"
        self.capture_step("account_screen", "Account screen is visible")

    def is_loaded(self) -> bool:
        return self.is_visible(L.link_edit_personal_info, timeout=20)

    def verify_name(self, name: str):
        assert self.is_visible(L.label_name_by_text % name), f"Name '{name}' not shown"
        self.capture_step("account_name", f"Name shown: {name}")

    def get_username(self) -> str:
        return self.find(L.label_username).get_attribute("content-desc") or ""

    # ================= action steps =================
    def tap_edit_personal_info(self):
        self.click(L.link_edit_personal_info)
        self.capture_step("edit_personal_info", "Tapped Edit my personal information")

    def tap_refer_friend(self):
        self.click(L.button_refer_friend)
        self.capture_step("refer_friend", "Tapped Refer a friend")

    # --- Account section rows ---
    def open_saved_credit_cards(self):
        self.click(L.menu_saved_credit_cards)
        self.capture_step("saved_credit_cards", "Opened Saved credit cards")

    def open_notifications_settings(self):
        self.click(L.menu_notifications_settings)
        self.capture_step("notifications_settings", "Opened Notifications settings")

    def open_my_receipts(self):
        self.click(L.menu_my_receipts)
        self.capture_step("my_receipts", "Opened My receipts")

    # --- Support section rows ---
    def open_give_us_feedback(self):
        self.click(L.menu_give_us_feedback)
        self.capture_step("give_us_feedback", "Opened Give us feedback")

    def open_contact_support(self):
        self.click(L.menu_contact_support)
        self.capture_step("contact_support", "Opened Contact Swing support")

    def open_delete_account(self):
        # Opens the delete-account flow (a confirmation screen follows — this
        # only taps the menu row, it does not confirm deletion).
        self.click(L.menu_delete_account)
        self.capture_step("delete_account", "Opened Delete my account")

    # --- Legal section rows ---
    def open_terms(self):
        self.click(L.menu_terms)
        self.capture_step("terms", "Opened Terms & conditions")

    def open_privacy_policy(self):
        self.click(L.menu_privacy_policy)
        self.capture_step("privacy_policy", "Opened Privacy policy")

    # --- log out ---
    def tap_log_out(self):
        self.click(L.button_log_out)
        self.capture_step("log_out", "Tapped Log out")
    
    def verify_bottom_sheet_log_out(self):
        assert self.is_visible(L.label_logout)
        self.capture_step("Open Bottom Sheet Logout")
    
    def tap_log_out_bottom_sheet(self):
        self.click(L.button_log_out_bottom_sheet)
        self.capture_step("Click Log out")
    
    def tap_cancel_log_out(self):
        self.click(L.button_cancel_logout)
        self.capture_step("Cancel Logout")
    
    def close_bottom_sheet_log_out(self):
        self.click(L.button_close_bottom_sheet)
        self.capture_step("Close Bottom Sheet Logout")
        

    def open_menu(self, label: str):
        self.click(L.menu_item % label)
        self.capture_step("account_menu", f"Opened '{label}'")

    # ================= bottom navigation =================
    def go_to_home(self):
        self.click(L.tab_home)
        self.capture_step("nav_home", "Navigated to Home tab")

    def go_to_activity(self):
        self.click(L.tab_activity)
        self.capture_step("nav_activity", "Navigated to Activity tab")
