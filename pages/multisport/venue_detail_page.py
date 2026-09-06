from core.android_base_page import AndroidBasePage
from locators.multisport.venue_detail_page_locators import VenueDetailPageLocators as L


class VenueDetailPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self, venue_name: str):
        self.wait_until_loaded()
        assert self.is_visible(L.header_venue_details, timeout=20), "Venue detail page not shown"
        assert self.is_visible(L.text_venue_name % venue_name, timeout=3), "Selected venue doesn't match"
        self.capture_step("venue_detail_screen",
                          "Venue detail screen is visible")

    # ================= book =================
    def book_venue(self):
        self.click(L.button_book_venue)
        self.capture_step("book_venue", "Tapped Book Venue")
