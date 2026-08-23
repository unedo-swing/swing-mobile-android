from core.android_base_page import AndroidBasePage
from locators.events.order_page_locators import OrderPageLocators as L


class OrderPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_success(self):
        assert self.is_visible(L.text_success, timeout=20), (
            "Order success screen ('See you on the event') not shown"
        )
        self.capture_step("order_success", "Registration confirmed (You're confirmed!)")

    # ================= action steps =================
    def tap_finish(self):
        self.click(L.button_finish)
        self.capture_step("order_finish", "Tapped 'Finish'")

    def tap_registration_details(self):
        self.click(L.button_registration_detail)
        self.capture_step("order_reg_details", "Tapped 'See registration details'")
