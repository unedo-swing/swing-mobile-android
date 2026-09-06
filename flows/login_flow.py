from flows.base_flow import BaseFlow
from pages.login_page import LoginPage
from pages.country_picker_page import CountryPickerPage
from pages.notification_prompt_page import NotificationPromptPage
from pages.home_page import HomePage
from pages.account_page import AccountPage
from pages.tee_time.explore_page import ExplorePage
from pages.tee_time.golf_course_details_page import GolfCourseDetailsPage


class LoginFlow(BaseFlow):
    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.login = self.page(LoginPage)
        self.country = self.page(CountryPickerPage)
        self.notif = self.page(NotificationPromptPage)
        self.home = self.page(HomePage)
        self.account = self.page(AccountPage)
        self.explore = self.page(ExplorePage)
        self.course_details = self.page(GolfCourseDetailsPage)

    def open_login(self):
        self.login.verify_login_screen()
    
    def select_country(self, label: str):
        self.login.open_country_picker()
        self.country.verify_screen()
        self.country.search_and_select(label)
        self.login.verify_login_screen()
    
    def enter_phone_number(self, phone_number: str):
        self.login.enter_phone(phone_number)
    
    def select_method_verification_whatsapp(self):
        self.login.choose_whatsapp()
    
    def select_method_verification_sms(self):
        self.login.choose_sms()
    
    def tap_continue_method_verify(self):
        self.login.tap_continue()
    
    def input_otp(self):
        # otp = input("Input Your OTP : ")
        self.login.enter_code("000000")

    def verify_login_success(self):
        self.notif.verify_screen()

    def dismiss_notification(self):
        self.notif.do_it_later()

    def verify_home(self):
        self.home.verify_screen()

    def open_account(self):
        self.home.go_to_account()
        self.account.verify_screen()

    def open_tee_time_explore(self):
        self.home.open_tee_time()
        self.explore.verify_screen()

    def open_course_details(self, name: str):
        self.explore.open_course(name)
        self.course_details.verify_screen()

    def popup_reminder_handle(self):
        self.home.close_reminder_popup_ifany()
