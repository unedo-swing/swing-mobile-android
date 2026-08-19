from core.android_base_page import AndroidBasePage
from locators.onboarding.whats_new_locators import WhatsNewLocators as L


class WhatsNewPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=30), "What's new screen not shown"
        self.capture_step("whats_new", "What's new screen is visible")

    def is_shown(self, timeout: int = 10) -> bool:
        return self.is_visible(L.label_title, timeout=timeout, log=False)

    def verify_content(self):
        missing = [
            name for name, locator in (
                ("headline", L.label_headline),
                ("subtitle", L.label_subtitle),
                ("see our updates", L.link_see_updates),
            )
            if not self.is_visible_after_scroll(locator)
        ]
        self.capture_step(
            "whats_new_content",
            "What's new content is complete" if not missing
            else f"missing: {', '.join(missing)}",
        )
        assert not missing, f"What's new screen is missing: {missing}"

    # ================= reading values =================
    def _desc(self, locator) -> str:
        return self.scroll_and_find(locator).get_attribute("content-desc") or ""

    def get_title(self) -> str:
        return self._desc(L.label_title)

    def get_headline(self) -> str:
        return self._desc(L.label_headline)

    # ================= action steps =================
    def tap_see_updates(self):
        self.click(L.link_see_updates)
        self.capture_step("whats_new_see_updates", "Tapped See our updates")

    def tap_close(self):
        self.click(L.button_close)
        self.capture_step("whats_new_close", "Closed the What's new screen")

    def dismiss_if_shown(self, timeout: int = 10) -> bool:
        if not self.is_shown(timeout):
            return False
        self.capture_step("whats_new", "What's new screen is visible")
        self.tap_close()
        return True
