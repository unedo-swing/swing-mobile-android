"""
Country-code picker page object (Android).

Opened from the login screen's Country selector. Per-screen STEPS only
(actions + verifications), each recording evidence with capture_step. XPaths
come from locators/country_picker_locators.py.
"""
from core.android_base_page import AndroidBasePage
from locators.country_picker_locators import CountryPickerLocators as L


class CountryPickerPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=15), "Country picker screen not shown"
        self.capture_step("country_picker", "Country picker screen is visible")

    # ================= action steps =================
    def search(self, query: str):
        self.fill(L.input_search, query)
        self.capture_step("country_search", f"Searched country '{query}'")

    def select(self, label: str, exact: bool = False):
        """
        Pick a country by its visible label.

        ``label`` is the accessibility text, e.g. ``"+62 Indonesia"`` (exact)
        or ``"Indonesia"`` (contains, the default — handy after searching).
        """
        locator = (L.option_exact if exact else L.option_contains) % label
        self.click(locator)
        self.capture_step("country_selected", f"Selected country '{label}'")

    def search_and_select(self, query: str, label: str | None = None, exact: bool = False):
        """Type a query then tap the matching row (defaults to the query text)."""
        self.search(query)
        self.select(label or query, exact=exact)

    def go_back(self):
        self.click(L.button_back)
        self.capture_step("country_back", "Closed country picker")
