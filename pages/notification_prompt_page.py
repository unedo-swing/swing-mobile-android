
from core.android_base_page import AndroidBasePage
from locators.notification_prompt_locators import NotificationPromptLocators as L


class NotificationPromptPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_prompt, timeout=20), "Enable notifications prompt not shown"
        self.capture_step("notif_prompt", "Enable notifications prompt is visible")

    def is_shown(self) -> bool:
        return self.is_visible(L.label_prompt, timeout=20)

    # ================= action steps =================
    def enable(self):
        self.click(L.button_enable)
        self.capture_step("notif_enable", "Tapped Enable notifications")

    def do_it_later(self):
        self.click(L.button_later)
        self.capture_step("notif_later", "Tapped I'll do it later")
