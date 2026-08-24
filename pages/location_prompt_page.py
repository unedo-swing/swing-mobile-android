
from core.android_base_page import AndroidBasePage
from locators.location_prompt_locators import LocationPromptLocators as L


class LocationPromptPage(AndroidBasePage):

    def verify_screen(self):
        assert self.is_visible(L.label_prompt, timeout=20), "Enable location prompt not shown"
        self.capture_step("location_prompt")

    def is_shown(self, timeout: int = 20) -> bool:
        return self.is_visible(L.label_prompt, timeout=timeout, log=False)

    def enable(self):
        self.click(L.button_enable)
        self.accept_permission()
        self.capture_step("location_enable")

    def do_it_later(self):
        self.click(L.button_later)
        self.capture_step("location_later")

    def enable_if_shown(self, timeout: int = 10) -> bool:
        if not self.is_shown(timeout):
            return False
        self.capture_step("location_prompt")
        self.enable()
        return True

    def dismiss_if_shown(self, timeout: int = 10) -> bool:
        if not self.is_shown(timeout):
            return False
        self.capture_step("location_prompt")
        self.do_it_later()
        return True
