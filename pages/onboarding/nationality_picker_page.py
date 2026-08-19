from core.android_base_page import AndroidBasePage
from locators.onboarding.nationality_picker_locators import NationalityPickerLocators as L


class NationalityPickerPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Select nationality dialog not shown"
        self.capture_step("nationality_picker", "Select nationality dialog is visible")

    def is_option_shown(self, name: str) -> bool:
        return self.is_visible(L.option_exact % name, timeout=5)

    # ================= action steps =================
    def search(self, query: str):
        self.fill(L.input_search, query)
        self.capture_step("nationality_search", f"Searched country '{query}'")

    def select(self, name: str, exact: bool = True):
        locator = (L.option_exact if exact else L.option_contains) % name
        self.click(locator)
        self.capture_step("nationality_selected", f"Selected nationality '{name}'")

    def search_and_select(self, query: str, name: str | None = None, exact: bool = True):
        self.search(query)
        self.select(name or query, exact=exact)

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("nationality_back", "Closed nationality picker")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("nationality_dismiss", "Dismissed nationality picker")
