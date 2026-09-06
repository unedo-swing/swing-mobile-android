from core.android_base_page import AndroidBasePage
from locators.multisport.payment_method_locators import (
    PaymentMethodLocators as L,
)


class PaymentMethodPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.title_header, timeout=20),             "Payment method page not shown"
        self.capture_step("payment_method_screen",
                          "Payment method screen is visible")

    # ================= choose method =================
    def select_payment_method(self, method_name: str):
        locator = L.button_payment_type % method_name
        self.click(locator)
        self.capture_step("select_payment_method",
                          f"Selected payment method: {method_name}")
