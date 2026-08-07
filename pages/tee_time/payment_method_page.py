"""
Select payment method page object (Android) — Tee Time.

Opened from "Select payment" on the booking confirmation. Per-screen STEPS only,
each recording evidence with capture_step. XPaths come from
locators/tee_time/payment_method_locators.py.
"""
from core.android_base_page import AndroidBasePage
from locators.tee_time.payment_method_locators import PaymentMethodLocators as L


class PaymentMethodPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Select payment method sheet not shown"
        self.capture_step("payment_method", "Select payment method sheet is visible")

    def verify_payment_option(self, name: str):
        # the e-wallet list sits below the saved cards, so scroll it into view
        assert self.is_visible_after_scroll(L.ewallet_by_name % name), \
            f"Payment option '{name}' not shown"
        self.capture_step("payment_option", f"Payment option shown: {name}")

    # ================= credit cards =================
    def select_card(self, name: str):
        """Pick a saved card by its label, e.g. 'VISA 0014' (first match)."""
        self.click(L.card_by_name % name)
        self.capture_step("select_card", f"Selected card '{name}'")

    def select_card_by_index(self, name: str, index: int = 1):
        """Pick the nth card with a repeated label (1-based)."""
        self.click(L.card_by_index % (name, index))
        self.capture_step("select_card", f"Selected card '{name}' #{index}")

    def tap_add_credit_card(self):
        self.click(L.button_add_credit_card)
        self.capture_step("add_credit_card", "Tapped Add credit card")

    # ================= other methods =================
    def select_qris(self):
        self.click(L.option_qris)
        self.capture_step("select_qris", "Selected QRIS")

    def select_payment_method(self, name: str):
        self.click(L.ewallet_by_name % name)
        self.capture_step("select payment method", f"Selected payment method '{name}'")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("payment_back", "Tapped back")
