from flows.base_flow import BaseFlow
from utils.api_client import ApiClient, ApiError, otp_code
from pages.login_page import LoginPage
from pages.country_picker_page import CountryPickerPage
from pages.notification_prompt_page import NotificationPromptPage
from pages.home_page import HomePage
from pages.account_page import AccountPage
from pages.tee_time.explore_page import ExplorePage
from pages.tee_time.golf_course_details_page import GolfCourseDetailsPage

import time


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
        # remembered so the OTP endpoint is asked about this exact login
        self.phone_number = ""
        self.verification_method = "WHATSAPP"
        # filled by select_country() from the login screen itself
        self.dial_code = ""

    def open_login(self):
        self.login.verify_login_screen()
    
    def select_country(self, label: str) -> str:
        self.login.open_country_picker()
        self.country.verify_screen()
        self.country.search_and_select(label)
        self.login.verify_login_screen()
        self.dial_code = self.login.read_dial_code()
        return self.dial_code
    
    def enter_phone_number(self, phone_number: str):
        self.phone_number = str(phone_number or "")
        self.login.enter_phone(phone_number)
    
    def select_method_verification_whatsapp(self):
        self.login.choose_whatsapp()
    
    def select_method_verification_sms(self):
        self.login.choose_sms()
    
    def tap_continue_method_verify(self):
        self.login.tap_continue()
    
    def select_verification_method(self, method: str):
        """Pick the OTP channel named in the test data ("whatsapp" or "sms")."""
        self.verification_method = str(method or "whatsapp").strip().upper() or "WHATSAPP"
        if str(method).strip().casefold() == "sms":
            self.select_method_verification_sms()
        else:
            self.select_method_verification_whatsapp()

    def input_otp(self):
        otp = input("Input Your OTP : ")
        self.login.enter_code(otp)

    def input_otp_by_pass(self):
        otp = '000000'##input("Input Your OTP : ")
        self.login.enter_code(otp)

    def fetch_otp_from_api(self, phone: str = "", dial_code: str = "", method: str = "") -> str:
        time.sleep(5)
        number = str(phone or self.phone_number or "").strip()
        # the code read off the screen wins over the env default; an explicit
        # argument still overrides both
        code_prefix = str(dial_code or self.dial_code or "").strip()
        response = ApiClient.swing().request_otp(
            number, code_prefix, method or self.verification_method,
        )
        code = otp_code(response)
        self.login.capture_step(
            "otp_from_api",
            f"Requested the OTP for {code_prefix or '(default dial code)'} {number} — "
            + (f"got a {len(code)}-digit code back" if code else "no code in the response"),
            data={"status": response.status, "response": response.text[:500]},
        )
        return code

    def resolve_otp_code(self, otp: str = "", phone: str = "", dial_code: str = "") -> str:
        value = str(otp or "").strip()
        if value.casefold() in ("api", "auto"):
            code = self.fetch_otp_from_api(phone, dial_code)
            if not code:
                raise ApiError("the OTP endpoint answered without a code")
            return code
        if value:
            return value
        try:
            code = self.fetch_otp_from_api(phone, dial_code)
        except ApiError as exc:
            print(f"[otp] API call failed ({exc}) — falling back to manual entry")
            code = ""
        print(code)
        return code or input("Input Your OTP : ")

    def input_otp_code(self, otp: str = "", phone: str = "", dial_code: str = ""):
        self.login.enter_code(self.resolve_otp_code(otp, phone, dial_code))

    def login_with_otp(self, country: str, phone: str, method: str, otp: str = "",
                       dial_code: str = ""):
        """The whole sign-in leg, straight from one row of test data. The dial
        code is read off the screen by select_country(); pass one only to force
        a different code than the app shows."""
        self.open_login()
        self.select_country(country)
        self.enter_phone_number(phone)
        self.tap_continue_method_verify()
        self.select_verification_method(method)
        self.input_otp_code(otp, phone, dial_code)

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
