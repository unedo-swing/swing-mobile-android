from core.android_base_page import AndroidBasePage
from locators.events.payment_method_locators import PaymentMethodLocators as L


class PaymentMethodPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.title_header, timeout=20), (
            "Select payment method not shown"
        )
        self.capture_step("pay_method", "Select payment method screen shown")

    # ================= action steps =================
    def select_payment_method(self, method: str):
        self.click(L.button_payment_type % method)
        self.capture_step("pay_select", f"Selected payment method: {method}")
