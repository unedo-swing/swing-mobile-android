from core.android_base_page import AndroidBasePage
from locators.multisport.billiard_page_locators import BilliardPageLocators as L


class BilliardPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.header_billiard_page, timeout=20),             "Billiard explore page not shown"
        self.capture_step("billiard_explore_screen",
                          "Billiard explore screen is visible")

    # ================= navigation =================
    def go_to_all_venue(self):
        self.click(L.button_see_all_venue)
        self.capture_step("go_to_all_venue", "Tapped See All Venue")
