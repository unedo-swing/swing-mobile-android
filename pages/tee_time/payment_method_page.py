from core.android_base_page import AndroidBasePage
from locators.tee_time.payment_method_locators import PaymentMethodLocators as L


class PaymentMethodPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Select payment method sheet not shown"
        self.capture_step("payment_method")

    def verify_payment_option(self, name: str):
        # the e-wallet list sits below the saved cards, so scroll it into view
        assert self.is_visible_after_scroll(L.ewallet_by_name % name), \
            f"Payment option '{name}' not shown"
        self.capture_step("payment_option", f"Payment option shown: {name}")

    # ================= credit cards =================
    def select_card(self, name: str):
        self.click(L.card_by_name % name)
        self.capture_step("select_card", f"Selected card '{name}'")

    def select_card_by_index(self, name: str, index: int = 1):
        self.click(L.card_by_index % (name, index))
        self.capture_step("select_card", f"Selected card '{name}' #{index}")

    def tap_add_credit_card(self):
        self.click(L.button_add_credit_card)
        self.capture_step("add_credit_card")

    # ================= other methods =================
    def select_qris(self):
        self.click(L.option_qris)
        self.capture_step("select_qris")

    def select_payment_method(self, name: str):
        self.click(L.ewallet_by_name % name)
        self.capture_step("select payment method", f"Selected payment method '{name}'")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("payment_back")
