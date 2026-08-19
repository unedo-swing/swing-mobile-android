from core.android_base_page import AndroidBasePage
from locators.onboarding.find_out_source_locators import FindOutSourceLocators as L
import time


class FindOutSourcePage(AndroidBasePage):

    # every option the screen offers, in the order it renders them
    SOURCES = [
        "Social media",
        "Article or blogs",
        "Recommended by friends or family",
        "Web search",
        "Offline advertisement",
        "A Swing event",
        "Others",
    ]

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), \
            "'How did you find out about Swing?' screen not shown"
        self.capture_step("onboarding_find_out_source",
                          "'How did you find out about Swing?' screen is visible")

    def get_options(self) -> list:
        return [
            e.get_attribute("content-desc") or ""
            for e in self.find_all(L.options_all)
        ]

    def verify_options(self, expected: list | None = None):
        expected = expected or self.SOURCES
        actual = self.get_options()
        missing = [label for label in expected if label not in actual]
        self.capture_step(
            "onboarding_source_options",
            f"{len(actual)} source option(s) shown",
            data={"options": actual},
        )
        assert not missing, f"Source option(s) not shown: {missing}"

    def is_finish_enabled(self) -> bool:
        return self.is_enabled(L.button_finish)

    # ================= action steps =================
    def select_find_out_source(self, source: str):
        self.click(L.option_by_label % source)
        self.capture_step("onboarding_source_selected", f"Selected source '{source}'")

    def tap_finish(self):
        time.sleep(3)
        self.click(L.button_finish)
        self.capture_step("onboarding_finish", "Tapped Finish")

    def tap_previous(self):
        self.click(L.button_previous)
        self.capture_step("onboarding_previous", "Tapped Previous")
