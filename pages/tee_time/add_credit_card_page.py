from core.android_base_page import AndroidBasePage
from locators.tee_time.add_credit_card_locators import AddCreditCardLocators as L


class AddCreditCardPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.input_cardholder, timeout=20), "Add credit card form not shown"
        self.capture_step("add_credit_card", "Add credit card form is visible")

    def is_save_enabled(self) -> bool:
        return self.is_enabled(L.button_save)

    # ================= field entry =================
    def enter_cardholder(self, name: str):
        self.fill(L.input_cardholder, name)
        self.capture_step("cardholder", f"Entered cardholder '{name}'")

    def enter_card_number(self, number: str):
        self.fill(L.input_card_number, number)
        self.capture_step("card_number", "Entered card number")

    def enter_expiry(self, expiry: str):
        self.fill(L.input_expiry, expiry)
        self.capture_step("expiry", f"Entered expiry '{expiry}'")

    def enter_cvv(self, cvv: str):
        self.fill(L.input_cvv, cvv)
        self.capture_step("cvv", "Entered CVV")

    def fill_card(self, cardholder: str, number: str, expiry: str, cvv: str):
        self.enter_cardholder(cardholder)
        self.enter_card_number(number)
        self.enter_expiry(expiry)
        self.enter_cvv(cvv)

    # ================= options =================
    def set_as_primary(self):
        self.click(L.switch_set_primary)
        self.capture_step("set_primary", "Toggled Set as primary method")

    def is_primary_on(self) -> bool:
        return self.find(L.switch_set_primary).get_attribute("checked") == "true"

    def tap_terms(self):
        self.click(L.link_terms)
        self.capture_step("terms", "Tapped Terms & conditions")

    # ================= submit =================
    def tap_save(self):
        self.click(L.button_save)
        self.capture_step("save_card", "Tapped Save credit card")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("add_card_back", "Tapped back")
