"""
"Switch to group booking" prompt page object (Android) — Tee Time.

Shown during a Standard booking when a Swing Pass member is added. Per-screen
STEPS only, each recording evidence with capture_step. XPaths come from
locators/tee_time/switch_group_booking_locators.py.
"""
from core.android_base_page import AndroidBasePage
from locators.tee_time.switch_group_booking_locators import SwitchGroupBookingLocators as L


class SwitchGroupBookingPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Switch to group booking prompt not shown"
        self.capture_step("switch_group_booking", "Switch to group booking prompt is visible")

    def is_shown(self) -> bool:
        return self.is_visible(L.label_title, timeout=10)

    # ================= action steps =================
    def switch_to_group(self):
        self.click(L.button_switch_to_group)
        self.capture_step("switch_to_group", "Tapped Switch to group booking")

    def keep_standard(self):
        """Dismiss the prompt and keep the Standard booking (secondary button)."""
        self.click(L.button_keep_standard)
        self.capture_step("keep_standard", "Kept Standard booking")

    def tap_learn_more(self):
        self.click(L.link_learn_more)
        self.capture_step("learn_more", "Tapped Learn more about booking methods")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("switch_dismiss", "Dismissed Switch to group booking prompt")
