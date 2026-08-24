from core.android_base_page import AndroidBasePage
from locators.swing_pass.join_success_locators import JoinSuccessLocators as L


class JoinSuccessPage(AndroidBasePage):

    FIELDS = {
        "player_name": L.FIELD_PLAYER_NAME,
        "join_date": L.FIELD_JOIN_DATE,
        "ends_on": L.FIELD_ENDS_ON,
        "membership_id": L.FIELD_MEMBERSHIP_ID,
        "billing_amount": L.FIELD_BILLING_AMOUNT,
        "billing_method": L.FIELD_BILLING_METHOD,
    }

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Membership acquired screen not shown"
        assert self.is_visible(L.label_subtitle), "'Welcome to Swing Pass' not shown"
        self.capture_step("join_success")

    def verify_labels(self):
        missing = [label for label in self.FIELDS.values()
                   if not self.is_visible(L.label_by_name % label)]
        self.capture_step("join_success_labels", "All field labels are shown" if not missing
                          else f"missing: {', '.join(missing)}")
        assert not missing, f"Membership acquired field(s) not shown: {missing}"

    def verify_field(self, label: str, expected: str):
        actual = self.get_field(label)
        assert actual == expected, f"'{label}' reads '{actual}', expected '{expected}'"

    def verify_details(self, **expected):
        unknown = [field for field in expected if field not in self.FIELDS]
        assert not unknown, f"Unknown Membership acquired field(s): {unknown}"
        actual = self.get_details()
        mismatches = {
            field: (want, actual.get(field, ""))
            for field, want in expected.items()
            if want and want.strip().casefold() != (actual.get(field, "") or "").strip().casefold()
        }
        assert not mismatches, (
            "Membership details do not match:\n"
            + "\n".join(
                f"  {field}: expected '{want}' but the screen reads '{got}'"
                for field, (want, got) in mismatches.items()
            )
        )

    def verify_billing(self, price: str = "", period: str = ""):
        billing = self.get_billing()
        for label, want, got in (("price", price, billing["price"]),
                                 ("period", period, billing["period"])):
            if want:
                assert want == got, f"Billing {label} is '{got}', expected '{want}'"

    def verify_verification_pending(self):
        note = self.get_verification_note()
        assert note, "No verification notice on the screen"
        assert self.is_visible(L.button_continue_verification), \
            "No 'Continue to verification' button on the screen"
        self.capture_step("join_success_verification", note)

    @staticmethod
    def parse_billing(desc: str) -> dict:
        price, sep, period = (desc or "").partition("/")
        return {
            "price": price.strip(),
            "period": period.strip() if sep else "",
            "label": desc or "",
        }

    def get_field(self, label: str) -> str:
        return self.scroll_and_find(L.value_by_label % label).get_attribute("content-desc") or ""

    def get_details(self) -> dict:
        details = {key: self.get_field(label) for key, label in self.FIELDS.items()}
        self.capture_step("join_success_details",
                          f"{details['membership_id']} — {details['billing_amount']}",
                          data=details)
        return details

    def get_membership_id(self) -> str:
        return self.get_field(L.FIELD_MEMBERSHIP_ID)

    def get_join_date(self) -> str:
        return self.get_field(L.FIELD_JOIN_DATE)

    def get_ends_on(self) -> str:
        return self.get_field(L.FIELD_ENDS_ON)

    def get_billing_method(self) -> str:
        return self.get_field(L.FIELD_BILLING_METHOD)

    def get_billing(self) -> dict:
        billing = self.parse_billing(self.get_field(L.FIELD_BILLING_AMOUNT))
        self.capture_step("join_success_billing",
                          f"{billing['price']} / {billing['period']}", data=billing)
        return billing

    def get_verification_note(self) -> str:
        element = self.find_anywhere(L.label_verification_note)
        return element.get_attribute("content-desc") or "" if element is not None else ""

    def tap_continue_verification(self):
        self.click(L.button_continue_verification)
        self.wait_until_loaded()
        self.capture_step("join_success_continue")
