from core.android_base_page import AndroidBasePage
from locators.swing_pass.change_billing_method_locators import ChangeBillingMethodLocators as L


class ChangeBillingMethodPage(AndroidBasePage):

    # The dict key each membership field maps to in get_details().
    FIELDS = {
        "player_name": L.FIELD_PLAYER_NAME,
        "renew_date": L.FIELD_RENEW_DATE,
        "membership_id": L.FIELD_MEMBERSHIP_ID,
    }

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Change billing method screen not shown"
        self.capture_step("change_method", "Change billing method screen is visible")

    def verify_no_method_selected(self):
        method = self.get_selected_method()
        assert method == L.PLACEHOLDER_METHOD, \
            f"Expected no method picked, but the row reads '{method}'"
        self.capture_step("change_method_empty", "No billing method picked yet")

    def verify_selected_method(self, expected: str):
        actual = self.get_selected_method()
        assert actual == expected, f"Picked method is '{actual}', expected '{expected}'"
        self.capture_step("change_method_selected", f"Picked method: {actual}")

    def verify_terms_accepted(self, accepted: bool = True):
        actual = self.is_terms_accepted()
        assert actual == accepted, \
            f"Terms checkbox is {'on' if actual else 'off'}, expected {'on' if accepted else 'off'}"

    # ================= reading =================
    def _desc(self, locator) -> str:
        return self.scroll_and_find(locator).get_attribute("content-desc") or ""

    def get_field(self, label: str) -> str:
        return self._desc(L.value_by_label % label)

    def get_details(self) -> dict:
        details = {key: self.get_field(label) for key, label in self.FIELDS.items()}
        self.capture_step("change_method_details",
                          f"{details['membership_id']} renews {details['renew_date']}",
                          data=details)
        return details

    def get_selected_method(self) -> str:
        method = self._desc(L.row_method)
        self.capture_step("change_method_row", f"Billing method row: {method}")
        return method

    def has_method_selected(self) -> bool:
        return self.get_selected_method() != L.PLACEHOLDER_METHOD

    def is_terms_accepted(self) -> bool:
        return self.scroll_and_find(L.checkbox_terms).get_attribute("checked") == "true"

    # ================= action steps =================
    def open_method_picker(self):
        self.click(L.button_select)
        self.capture_step("change_method_picker", "Opened Select billing method")

    def toggle_terms(self):
        self.click(L.checkbox_terms)
        self.capture_step("change_method_terms_toggled", "Toggled the terms checkbox")

    def set_terms(self, accepted: bool = True):
        if self.is_terms_accepted() == accepted:
            self.capture_step("change_method_terms",
                              f"Terms already {'accepted' if accepted else 'not accepted'}")
            return
        self.toggle_terms()
        actual = self.is_terms_accepted()
        assert actual == accepted, f"Terms checkbox is {actual}, expected {accepted}"

    def accept_terms(self):
        self.set_terms(True)

    def open_terms(self):
        self.click(L.link_terms)
        self.capture_step("change_method_open_terms", "Opened Swing Pass terms & conditions")

    def slide_to_confirm(self):
        self.slide_to_end(L.slider_confirm, L.slider_thumb)
        self.wait_until_loaded()
        self.capture_step("change_method_confirm", "Slid to confirm the new billing method")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("change_method_back", "Left the Change billing method screen")
