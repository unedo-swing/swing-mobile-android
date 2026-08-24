from core.android_base_page import AndroidBasePage
from locators.onboarding.profile_setup_locators import ProfileSetupLocators as L


class ProfileSetupPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_welcome, timeout=30), "Profile setup screen not shown"
        self.capture_step("onboarding_profile_setup")

    def is_next_enabled(self) -> bool:
        return self.is_enabled(L.button_next)

    def verify_next_enabled(self, expected: bool = True):
        actual = self.is_next_enabled()
        self.capture_step(
            "onboarding_next_state", f"Next enabled = {actual} (expected {expected})"
        )
        assert actual == expected, f"Next enabled={actual}, expected {expected}"

    def verify_message(self, text: str):
        assert self.is_visible_after_scroll(L.label_message % text), \
            f"Message '{text}' not shown"
        self.capture_step("onboarding_message", f"Message '{text}' is visible")

    # ================= reading values =================
    def _fill(self, locator, text: str):
        self.scroll_and_find(locator)
        self.fill(locator, text)

    def _value(self, locator) -> str:
        element = self.scroll_and_find(locator)
        return element.get_attribute("content-desc") or element.get_attribute("text") or ""

    def get_first_name(self) -> str:
        return self._value(L.input_first_name)

    def get_last_name(self) -> str:
        return self._value(L.input_last_name)

    def get_birthday(self) -> str:
        return self._value(L.field_birthday)

    def get_nationality(self) -> str:
        return self._value(L.field_nationality)

    def get_gender(self) -> str:
        return self._value(L.field_gender)

    def get_username(self) -> str:
        return self._value(L.input_username)

    def get_email(self) -> str:
        return self._value(L.input_email)

    # ================= action steps =================
    def enter_first_name(self, first_name: str):
        self._fill(L.input_first_name, first_name)
        self.capture_step("onboarding_first_name", f"Entered first name '{first_name}'")

    def enter_last_name(self, last_name: str):
        self._fill(L.input_last_name, last_name)
        self.capture_step("onboarding_last_name", f"Entered last name '{last_name}'")

    def enter_username(self, username: str):
        self._fill(L.input_username, username)
        self.capture_step("onboarding_username", f"Entered username '{username}'")

    def enter_email(self, email: str):
        self._fill(L.input_email, email)
        self.capture_step("onboarding_email", f"Entered email '{email}'")

    def enter_referral_code(self, code: str):
        self._fill(L.input_referral_code, code)
        self.capture_step("onboarding_referral", f"Entered referral code '{code}'")

    # ================= picker fields =================
    def open_birthday_picker(self):
        self.click(L.field_birthday)
        self.capture_step("onboarding_birthday_open")

    def open_nationality_picker(self):
        self.click(L.field_nationality)
        self.capture_step("onboarding_nationality_open")

    def open_gender_picker(self):
        self.click(L.field_gender)
        self.capture_step("onboarding_gender_open")

    # ================= submit =================
    def tap_next(self):
        self.hide_keyboard()
        self.click(L.button_next)
        self.capture_step("onboarding_next")

    def fill_names(self, first_name: str, last_name: str):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
