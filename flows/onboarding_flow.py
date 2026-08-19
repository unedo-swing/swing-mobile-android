from flows.base_flow import BaseFlow
from pages.onboarding.profile_setup_page import ProfileSetupPage
from pages.onboarding.birthday_picker_page import BirthdayPickerPage
from pages.onboarding.nationality_picker_page import NationalityPickerPage
from pages.onboarding.gender_picker_page import GenderPickerPage
from pages.onboarding.find_out_source_page import FindOutSourcePage
from pages.onboarding.whats_new_page import WhatsNewPage
from pages.onboarding.coach_mark_page import CoachMarkPage
from pages.home_page import HomePage


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

    # ================= what's new (fresh install only) =================
    def verify_whats_new(self):
        self.whats_new.verify_screen()
        self.whats_new.verify_content()

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

    # ================= home coach marks (fresh install only) =================
    def verify_coach_marks(self):
        self.coach_mark.verify_sequence()
        self.home.verify_screen()

    def dismiss_coach_marks(self, timeout: int = 10) -> list:
        return self.coach_mark.dismiss_all(timeout=timeout)

    def verify_home(self):
        self.home.verify_screen()

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

