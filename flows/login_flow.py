from flows.base_flow import BaseFlow
from utils.api_client import ApiClient, ApiError, otp_code
from pages.login_page import LoginPage
from pages.country_picker_page import CountryPickerPage
from pages.notification_prompt_page import NotificationPromptPage
from pages.location_prompt_page import LocationPromptPage
from pages.home_page import HomePage
from pages.account_page import AccountPage
from pages.tee_time.explore_page import ExplorePage
from pages.tee_time.golf_course_details_page import GolfCourseDetailsPage
from pages.sport_option_page import SportOptionPage
from pages.onboarding.whats_new_page import WhatsNewPage
from pages.onboarding.coach_mark_page import CoachMarkPage

import time


class LoginFlow(BaseFlow):
    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.login = self.page(LoginPage)
        self.country = self.page(CountryPickerPage)
        self.notif = self.page(NotificationPromptPage)
        self.location = self.page(LocationPromptPage)
        self.home = self.page(HomePage)
        self.account = self.page(AccountPage)
        self.explore = self.page(ExplorePage)
        self.course_details = self.page(GolfCourseDetailsPage)
        self.sport_option_page = self.page(SportOptionPage)
        self.whats_new = self.page(WhatsNewPage)
        self.coach_mark = self.page(CoachMarkPage)
        self.phone_number = ""
        self.verification_method = "WHATSAPP"
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

    def enable_notification(self):
        self.notif.enable()

    def enable_notification_if_shown(self, timeout: int = 10) -> bool:
        return self.notif.enable_if_shown(timeout)

    def dismiss_notification_if_shown(self, timeout: int = 10) -> bool:
        return self.notif.dismiss_if_shown(timeout)

    def verify_location_prompt(self):
        self.location.verify_screen()

    def dismiss_location(self):
        self.location.do_it_later()

    def enable_location(self):
        self.location.enable()

    def enable_location_if_shown(self, timeout: int = 10) -> bool:
        return self.location.enable_if_shown(timeout)

    def dismiss_location_if_shown(self, timeout: int = 10) -> bool:
        return self.location.dismiss_if_shown(timeout)

    def allow_permissions(self, timeout: int = 10) -> list:
        granted = []
        if self.enable_notification_if_shown(timeout):
            granted.append("notification")
        if self.enable_location_if_shown(timeout):
            granted.append("location")
        return granted

    def skip_permissions(self, timeout: int = 10) -> list:
        skipped = []
        if self.dismiss_notification_if_shown(timeout):
            skipped.append("notification")
        if self.dismiss_location_if_shown(timeout):
            skipped.append("location")
        return skipped

    # ================= what's new (fresh install only) =================
    def verify_whats_new(self):
        self.whats_new.verify_screen()
        # self.whats_new.verify_content()

    def close_whats_new(self):
        self.whats_new.tap_close()

    def dismiss_whats_new(self, timeout: int = 10) -> bool:
        return self.whats_new.dismiss_if_shown(timeout)

    def check_whats_new(self, timeout: int = 10) -> bool:
        if not self.whats_new.is_shown(timeout):
            return False
        self.verify_whats_new()
        self.close_whats_new()
        return True

    def verify_coach_marks(self):
        self.coach_mark.verify_sequence()

    def open_account(self):
        self.home.go_to_account()
        self.account.verify_screen()

    def open_tee_time_explore(self):
        self.home.open_tee_time()
        self.explore.verify_screen()

    def open_course_details(self, name: str):
        self.explore.open_course(name)
        self.course_details.verify_screen()
    
    def verify_page_sport_option(self):
        self.sport_option_page.verify_screen()
    
    def select_sport(self, sport: str):
        self.sport_option_page.select_sport(sport)
    
    def verify_home(self, sport_type: str, region: str):
        self.wait_until_load_home_page()
        self.home.verify_screen(sport_type, region)
    
    def wait_until_load_home_page(self):
        self.home.is_loaded_home_screen()
        
