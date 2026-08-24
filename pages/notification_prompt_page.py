
from core.android_base_page import AndroidBasePage
from locators.notification_prompt_locators import NotificationPromptLocators as L


class NotificationPromptPage(AndroidBasePage):

    def verify_screen(self):
        assert self.is_visible(L.label_prompt, timeout=20), "Enable notifications prompt not shown"
        self.capture_step("notif_prompt")

    def is_shown(self, timeout: int = 20) -> bool:
        return self.is_visible(L.label_prompt, timeout=timeout, log=False)

    def enable(self):
        self.click(L.button_enable)
        self.accept_permission()
        self.capture_step("notif_enable")

    def do_it_later(self):
        self.click(L.button_later)
        self.capture_step("notif_later")

    def enable_if_shown(self, timeout: int = 10) -> bool:
        if not self.is_shown(timeout):
            return False
        self.capture_step("notif_prompt")
        self.enable()
        return True

    def dismiss_if_shown(self, timeout: int = 10) -> bool:
        if not self.is_shown(timeout):
            return False
        self.capture_step("notif_prompt")
        self.do_it_later()
        return True
