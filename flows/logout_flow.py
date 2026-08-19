from flows.base_flow import BaseFlow
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from pages.home_page import HomePage

class LogoutFlow(BaseFlow):
    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.login = self.page(LoginPage)
        self.account = self.page(AccountPage)
        self.home = self.page(HomePage)
    
    def logout(self):
        self.home.go_to_account()
        self.account.verify_screen()
        self.account.tap_log_out()
        self.account.verify_bottom_sheet_log_out()
        self.account.tap_log_out_bottom_sheet()
        self.login.verify_login_screen()
    
    def cancel_logout(self):
        self.home.go_to_account()
        self.account.verify_screen()
        self.account.tap_log_out()
        self.account.verify_bottom_sheet_log_out()
        self.account.tap_cancel_log_out()
        self.account.verify_screen()
        