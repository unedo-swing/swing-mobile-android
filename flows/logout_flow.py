from flows.base_flow import BaseFlow
from pages.home_page import HomePage
from pages.account_page import AccountPage


class LogoutFlow(BaseFlow):

    def __init__(self, driver, reporter=None):
        super().__init__(driver)
        self.home = self.page(HomePage)
        self.account = self.page(AccountPage)

    def open_account(self):
        self.home.go_to_account()
        self.account.verify_screen()

    def tap_log_out(self):
        self.account.tap_log_out()

    def confirm_logout(self):
        self.account.confirm_logout()

    def logout(self):
        self.open_account()
        self.tap_log_out()
        self.confirm_logout()
