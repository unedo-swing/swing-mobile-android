from core.android_base_page import AndroidBasePage
from locators.swing_pass.billing_details_locators import BillingDetailsLocators as L


class BillingDetailsPage(AndroidBasePage):

    # The dict key each field label maps to in get_details().
    FIELDS = {
        "player_name": L.FIELD_PLAYER_NAME,
        "membership_id": L.FIELD_MEMBERSHIP_ID,
        "billing_duration": L.FIELD_BILLING_DURATION,
        "join_date": L.FIELD_JOIN_DATE,
        "renews_on": L.FIELD_RENEWS_ON,
        "payment_date": L.FIELD_PAYMENT_DATE,
        "total": L.FIELD_TOTAL,
        "payment_method": L.FIELD_PAYMENT_METHOD,
    }

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Billing Details screen not shown"
        self.capture_step("billing_details", "Billing Details screen is visible")

    def verify_labels(self):
        missing = [label for label in self.FIELDS.values()
                   if not self.is_visible(L.label_by_name % label)]
        self.capture_step("billing_details_labels", "All field labels are shown" if not missing
                          else f"missing: {', '.join(missing)}")
        assert not missing, f"Billing Details field(s) not shown: {missing}"

    def verify_field(self, label: str, expected: str):
        actual = self.get_field(label)
        assert actual == expected, f"'{label}' reads '{actual}', expected '{expected}'"

    def verify_details(self, **expected):
        unknown = [field for field in expected if field not in self.FIELDS]
        assert not unknown, f"Unknown Billing Details field(s): {unknown}"
        actual = self.get_details()
        mismatches = {
            field: (want, actual.get(field, ""))
            for field, want in expected.items()
            if want and want.strip().casefold() != (actual.get(field, "") or "").strip().casefold()
        }
        assert not mismatches, (
            "Billing Details do not match:\n"
            + "\n".join(
                f"  {field}: expected '{want}' but the screen reads '{got}'"
                for field, (want, got) in mismatches.items()
            )
        )

    # ================= reading =================
    def get_field(self, label: str) -> str:
        return self.scroll_and_find(L.value_by_label % label).get_attribute("content-desc") or ""

    def get_details(self) -> dict:
        details = {key: self.get_field(label) for key, label in self.FIELDS.items()}
        self.capture_step("billing_details_values",
                          f"{details['total']} on {details['payment_date']}", data=details)
        return details

    def get_membership_id(self) -> str:
        return self.get_field(L.FIELD_MEMBERSHIP_ID)

    def get_total(self) -> str:
        return self.get_field(L.FIELD_TOTAL)

    def get_payment_method(self) -> str:
        return self.get_field(L.FIELD_PAYMENT_METHOD)

    # ================= action steps =================
    def tap_contact_support(self):
        self.click(L.button_contact_support)
        self.capture_step("billing_contact_support", "Tapped Contact Swing Support")

    def tap_send_receipt(self):
        self.click(L.button_send_receipt)
        self.capture_step("billing_send_receipt", "Tapped Send receipt")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("billing_details_back", "Left the Billing Details screen")
