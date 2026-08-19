from core.android_base_page import AndroidBasePage
from locators.onboarding.coach_mark_locators import CoachMarkLocators as L


class CoachMarkPage(AndroidBasePage):

    # the tooltips in the order Home shows them, with the body each one carries
    SEQUENCE = [
        (L.TITLE_SPORT_MODE, L.body_sport_mode),
        (L.TITLE_COUNTRIES, L.body_countries),
    ]

    # ================= verify steps =================
    def is_shown(self, timeout: int = 10) -> bool:
        return self.is_visible(L.any_title, timeout=timeout, log=False)

    def get_title(self) -> str:
        elements = self.find_all(L.any_title)
        return (elements[0].get_attribute("content-desc") or "") if elements else ""

    def verify_coach_mark(self, title: str, body: str | None = None, timeout: int = 20):
        assert self.is_visible(L.label_title % title, timeout=timeout), \
            f"Coach mark '{title}' not shown"
        assert self.is_visible(L.button_got_it), \
            f"Coach mark '{title}' has no 'Got it!' button"
        if body:
            assert self.is_visible(body), f"Coach mark '{title}' body text not shown"
        self.capture_step("coach_mark", f"Coach mark '{title}' is visible")

    # ================= action steps =================
    def tap_got_it(self):
        self.click(L.button_got_it)
        self.capture_step("coach_mark_got_it", "Tapped Got it!")

    def dismiss(self, title: str, body: str | None = None):
        self.verify_coach_mark(title, body)
        self.tap_got_it()

    # ================= scenario =================
    def verify_sequence(self, sequence: list | None = None):
        for title, body in (sequence or self.SEQUENCE):
            self.dismiss(title, body)

    def dismiss_all(self, max_marks: int = 5, timeout: int = 10) -> list:
        dismissed = []
        for _ in range(max_marks):
            if not self.is_shown(timeout if not dismissed else 3):
                return dismissed
            title = self.get_title()
            self.capture_step("coach_mark", f"Coach mark '{title}' is visible")
            self.tap_got_it()
            dismissed.append(title)
        raise AssertionError(
            f"coach marks still on screen after dismissing {max_marks}: {dismissed}"
        )
