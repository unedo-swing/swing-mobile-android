from flows.base_flow import BaseFlow
from pages.onboarding.profile_setup_page import ProfileSetupPage
from pages.onboarding.birthday_picker_page import BirthdayPickerPage
from pages.onboarding.nationality_picker_page import NationalityPickerPage
from pages.onboarding.gender_picker_page import GenderPickerPage
from pages.onboarding.find_out_source_page import FindOutSourcePage
from pages.onboarding.whats_new_page import WhatsNewPage
from pages.onboarding.coach_mark_page import CoachMarkPage
from pages.notification_prompt_page import NotificationPromptPage
from pages.location_prompt_page import LocationPromptPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.country_picker_page import CountryPickerPage
from pages.sport_option_page import SportOptionPage
from utils.api_client import ApiClient, ApiError, otp_code

import time


class OnboardingFlow(BaseFlow):
    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.whats_new = self.page(WhatsNewPage)
        self.coach_mark = self.page(CoachMarkPage)
        self.home = self.page(HomePage)
        self.profile = self.page(ProfileSetupPage)
        self.birthday = self.page(BirthdayPickerPage)
        self.nationality = self.page(NationalityPickerPage)
        self.gender = self.page(GenderPickerPage)
        self.source = self.page(FindOutSourcePage)
        self.notif = self.page(NotificationPromptPage)
        self.location = self.page(LocationPromptPage)
        self.login = self.page(LoginPage)
        self.country = self.page(CountryPickerPage)
        self.sport_option_page = self.page(SportOptionPage)
        self.phone_number = ""
        self.verification_method = "WHATSAPP"
        self.dial_code = ""

    # ================= login (copied from LoginFlow) =================
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

    # ================= sport option (copied from LoginFlow) =================
    def verify_page_sport_option(self):
        self.sport_option_page.verify_screen()

    def select_sport(self, sport: str):
        self.sport_option_page.select_sport(sport)

    # ================= what's new (fresh install only) =================
    def verify_whats_new(self):
        self.whats_new.verify_screen()
        # self.whats_new.verify_content()

    def close_whats_new(self):
        self.whats_new.tap_close()

    def dismiss_whats_new(self, timeout: int = 10) -> bool:
        return self.whats_new.dismiss_if_shown(timeout)

    # ================= profile setup screen =================
    def open_profile_setup(self):
        self.profile.verify_screen()

    def enter_name(self, first_name: str, last_name: str):
        self.profile.fill_names(first_name, last_name)

    def enter_username(self, username: str):
        self.profile.enter_username(username)

    def enter_email(self, email: str):
        self.profile.enter_email(email)

    def enter_referral_code(self, code: str):
        self.profile.enter_referral_code(code)

    # ================= pickers =================
    def select_birthday(self, birthdate: str):
        self.profile.open_birthday_picker()
        self.birthday.verify_screen()
        self.birthday.select_birthday(birthdate)
        self.profile.verify_screen()    # wait for return

    def select_nationality(self, country: str):
        self.profile.open_nationality_picker()
        self.nationality.verify_screen()
        self.nationality.search_and_select(country)
        self.profile.verify_screen()    # wait for return

    def select_gender(self, gender: str):
        self.profile.open_gender_picker()
        self.gender.verify_screen()
        self.gender.select_gender(gender)
        self.profile.verify_screen()    # wait for return

    # ================= verification =================
    def get_profile(self) -> dict:
        return {
            "first_name": self.profile.get_first_name(),
            "last_name": self.profile.get_last_name(),
            "birthday": self.profile.get_birthday(),
            "nationality": self.profile.get_nationality(),
            "gender": self.profile.get_gender(),
            "username": self.profile.get_username(),
            "email": self.profile.get_email(),
        }

    def verify_profile(self, **expected):
        actual = self.get_profile()
        mismatches = {
            field: (want, actual.get(field, ""))
            for field, want in expected.items()
            if want and want.casefold() not in (actual.get(field, "") or "").casefold()
        }
        self.profile.capture_step(
            "onboarding_profile_values",
            "Profile fields match what was entered" if not mismatches
            else f"{len(mismatches)} field(s) differ",
            data=actual,
        )
        assert not mismatches, (
            "Profile setup does not show what was entered:\n"
            + "\n".join(
                f"  {field}: expected '{want}' but field reads '{got}'"
                for field, (want, got) in mismatches.items()
            )
        )

    def verify_next_enabled(self, expected: bool = True):
        self.profile.verify_next_enabled(expected)

    # ================= submit =================
    def tap_next(self):
        self.profile.tap_next()

    # ================= how did you find out about Swing? =================
    def open_find_out_source(self):
        self.source.verify_screen()

    def verify_source_options(self, expected: list | None = None):
        self.source.verify_options(expected)

    def select_source(self, source: str):
        self.source.select_find_out_source(source)

    def tap_finish(self):
        self.source.tap_finish()

    def back_to_profile_setup(self):
        self.source.tap_previous()
        self.profile.verify_screen()

    def choose_source(self, source: str):
        self.open_find_out_source()
        self.verify_source_options()
        self.select_source(source)

    # ================= permission bottom sheets =================
    def verify_notification_prompt(self):
        self.notif.verify_screen()

    def enable_notification(self):
        self.notif.enable()

    def enable_notification_if_shown(self, timeout: int = 10) -> bool:
        return self.notif.enable_if_shown(timeout)

    def dismiss_notification_if_shown(self, timeout: int = 10) -> bool:
        return self.notif.dismiss_if_shown(timeout)

    def verify_location_prompt(self):
        self.location.verify_screen()

    def enable_location(self):
        self.location.enable()

    def enable_location_if_shown(self, timeout: int = 10) -> bool:
        return self.location.enable_if_shown(timeout)

    def dismiss_location_if_shown(self, timeout: int = 10) -> bool:
        return self.location.dismiss_if_shown(timeout)

    def allow_permissions(self, timeout: int = 10) -> list:
        """Grant whichever of the two bottom sheets show up, in the order the app asks."""
        granted = []
        if self.enable_notification_if_shown(timeout):
            granted.append("notification")
        if self.enable_location_if_shown(timeout):
            granted.append("location")
        return granted

    def skip_permissions(self, timeout: int = 10) -> list:
        """Tap "I'll do it later" on whichever of the two bottom sheets show up."""
        skipped = []
        if self.dismiss_notification_if_shown(timeout):
            skipped.append("notification")
        if self.dismiss_location_if_shown(timeout):
            skipped.append("location")
        return skipped

    # ================= home coach marks (fresh install only) =================
    def verify_coach_marks(self):
        self.coach_mark.verify_sequence()

    def dismiss_coach_marks(self, timeout: int = 10) -> list:
        return self.coach_mark.dismiss_all(timeout=timeout)

    def verify_home(self, sport_type: str, region: str):
        self.home.is_loaded_home_screen()
        self.home.verify_screen(sport_type, region)

    # ================= end-to-end scenario =================
    def fill_profile(self, first_name: str, last_name: str, birthdate: str,
                     nationality: str, gender: str, username: str, email: str,
                     referral_code: str | None = None):
        self.enter_name(first_name, last_name)
        self.select_birthday(birthdate)
        self.select_nationality(nationality)
        self.select_gender(gender)
        self.enter_username(username)
        self.enter_email(email)
        if referral_code:
            self.enter_referral_code(referral_code)
        self.profile.hide_keyboard()
        
        self.verify_next_enabled(True)

