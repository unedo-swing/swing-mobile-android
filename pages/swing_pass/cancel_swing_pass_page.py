from core.android_base_page import AndroidBasePage
from locators.swing_pass.cancel_swing_pass_locators import CancelSwingPassLocators as L


class CancelSwingPassPage(AndroidBasePage):

    # The dict key each membership field maps to in get_details().
    FIELDS = {
        "player_name": L.FIELD_PLAYER_NAME,
        "cancel_date": L.FIELD_CANCEL_DATE,
        "ends_on": L.FIELD_ENDS_ON,
        "membership_id": L.FIELD_MEMBERSHIP_ID,
    }

    REASONS = [
        L.REASON_NO_VALUE,
        L.REASON_TOO_EXPENSIVE,
        L.REASON_CANNOT_USE_UP,
        L.REASON_DIDNT_KNOW_AUTORENEW,
        L.REASON_RARELY_USED,
        L.REASON_OTHER_PROVIDER,
        L.REASON_NO_PERKS,
    ]

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Cancel Swing Pass screen not shown"
        self.capture_step("cancel_pass", "Cancel Swing Pass screen is visible")

    def verify_reasons(self):
        missing = [r for r in self.REASONS
                   if self.find_anywhere(L.reason_by_text % r) is None]
        self.capture_step("cancel_pass_reasons", "All reasons are offered" if not missing
                          else f"missing: {', '.join(missing)}")
        assert not missing, f"Cancellation reason(s) not offered: {missing}"

    def verify_cancel_disabled(self):
        assert not self.is_cancel_enabled(), \
            "'Cancel membership' is enabled with no reason picked"
        self.capture_step("cancel_pass_disabled", "Cancel membership is disabled")

    def verify_cancel_enabled(self):
        assert self.is_cancel_enabled(), "'Cancel membership' is still disabled"
        self.capture_step("cancel_pass_enabled", "Cancel membership is enabled")

    def verify_reason_selected(self, reason: str):
        actual = self.get_selected_reason()
        assert reason.casefold() in actual.casefold(), \
            f"Selected reason is '{actual}', expected one containing '{reason}'"
        self.capture_step("cancel_pass_reason", f"Selected reason: {actual}")

    def verify_ends_on(self, expected: str):
        actual = self.get_field(L.FIELD_ENDS_ON)
        assert actual == expected, f"Pass ends '{actual}', expected '{expected}'"

    # ================= reading =================
    def get_field(self, label: str) -> str:
        return self.scroll_and_find(L.value_by_label % label).get_attribute("content-desc") or ""

    def get_details(self) -> dict:
        details = {key: self.get_field(label) for key, label in self.FIELDS.items()}
        self.capture_step("cancel_pass_details",
                          f"{details['membership_id']} ends {details['ends_on']}",
                          data=details)
        return details

    def get_reasons(self) -> list:
        reasons = [
            e.get_attribute("content-desc") or ""
            for e in self.find_all(L.reason_any)
        ]
        self.capture_step("cancel_pass_reason_list", f"{len(reasons)} reason(s) shown",
                          data={"reasons": reasons})
        return reasons

    def get_selected_reason(self) -> str:
        element = self.find_anywhere(L.reason_selected)
        return element.get_attribute("content-desc") or "" if element is not None else ""

    def is_reason_selected(self, reason: str) -> bool:
        radio = self.scroll_and_find(L.reason_by_text % reason)
        return radio.get_attribute("checked") == "true"

    def is_cancel_enabled(self) -> bool:
        return self.is_enabled(L.button_cancel_membership)

    # ================= action steps =================
    def select_reason(self, reason: str):
        self.click(L.reason_by_text % reason)
        assert self.is_reason_selected(reason), \
            f"Tapped reason '{reason}' but its radio did not turn on"
        self.capture_step("cancel_pass_select_reason", f"Selected reason '{reason}'")

    def tap_cancel_membership(self):
        self.click(L.button_cancel_membership)
        self.wait_until_loaded()
        self.capture_step("cancel_pass_confirm", "Tapped Cancel membership")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("cancel_pass_back", "Left the Cancel Swing Pass screen")
