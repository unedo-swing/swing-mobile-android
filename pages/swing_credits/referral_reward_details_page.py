from core.android_base_page import AndroidBasePage
from locators.swing_credits.referral_reward_details_locators import (
    ReferralRewardDetailsLocators as L,
)


class ReferralRewardDetailsPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), \
            "Referral reward details screen not shown"
        self.capture_step("referral_reward_details")

    # ================= reading values =================
    def _desc(self, locator) -> str:
        element = self.find_anywhere(locator)
        return "" if element is None else (element.get_attribute("content-desc") or "")

    def get_description(self) -> str:
        return self._desc(L.label_description)

    def get_amount(self) -> str:
        return self._desc(L.value_amount)

    def get_expiry(self) -> str:
        return self._desc(L.label_expiry).replace("Expired on", "").strip()

    def get_earned_on(self) -> str:
        return self._desc(L.label_earned_on).replace("Earned on", "").strip()

    def get_details(self) -> dict:
        details = {
            "description": self.get_description(),
            "amount": self.get_amount(),
            "expiry": self.get_expiry(),
            "earned_on": self.get_earned_on(),
        }
        self.capture_step("referral_reward_values", data=details)
        return details

    # ================= verify =================
    def verify_referrer(self, name: str):
        description = self.get_description()
        assert name.casefold() in description.casefold(), \
            f"Description '{description}' does not name '{name}'"
        self.capture_step("referral_referrer", f"Referral is from '{name}'")

    def verify_amount(self, expected: str):
        actual = self.get_amount()
        assert actual.strip() == expected.strip(), \
            f"Referral reward is '{actual}', expected '{expected}'"
        self.capture_step("referral_amount", f"Referral reward is {actual}")

    def verify_details(self, **expected):
        actual = self.get_details()
        mismatches = {}
        for field, want in expected.items():
            got = (actual.get(field, "") or "").strip()
            if not want:
                continue
            ok = (want.casefold() in got.casefold() if field == "description"
                  else want.strip().casefold() == got.casefold())
            if not ok:
                mismatches[field] = (want, got)
        assert not mismatches, (
            "Referral reward details do not match:\n"
            + "\n".join(
                f"  {field}: expected '{want}' but screen reads '{got}'"
                for field, (want, got) in mismatches.items()
            )
        )

    def verify_support_section(self):
        assert self.is_visible_after_scroll(L.label_have_question), \
            "'Have a question?' section not shown"
        assert self.is_visible(L.button_contact_support), \
            "'Contact Swing support' row not shown"
        self.capture_step("referral_support")

    # ================= action steps =================
    def tap_contact_support(self):
        self.click(L.button_contact_support)
        self.capture_step("referral_contact_support")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("referral_details_back")
