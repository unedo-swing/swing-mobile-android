from core.android_base_page import AndroidBasePage
from locators.multisport.sport_option_page_locators import SportOptionPageLocators as L


class SportOptionPage(AndroidBasePage):

    # ================= enter from home app bar =================
    def navigate_from_home(self):
        """Tap the app-bar 'Select sport' button to open this page."""
        self.click(L.button_global_to_sport_option_page)
        self.capture_step("click_button_to_sport_option_page",
                          "Tapped app-bar Select sport → Sport option screen is visible")


    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.hedaer_sport_option_page, timeout=20), "Sport option page not shown"
        self.capture_step("sport_option_screen",
                          "Sport option screen is visible")

    # ================= choose sport =================
    def choose_sport(self, sport_name: str):
        locator = L.button_choose_sport % sport_name
        self.click(locator)
        self.capture_step("choose_sport", f"Chosen sport: {sport_name}")
