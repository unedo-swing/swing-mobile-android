from core.android_base_page import AndroidBasePage
from locators.multisport.all_venue_list_page import AllVenueListPage as L


class AllVenueListPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.header_all_venue_list_page, timeout=20),             "All venue list page not shown"
        self.capture_step("all_venue_list_screen",
                          "All venue list screen is visible")

    # ================= choose venue =================
    def choose_venue(self, venue_name: str):
        locator = L.button_card_venue % venue_name
        self.click(locator)
        self.capture_step("choose_venue", f"Chosen venue: {venue_name}")
