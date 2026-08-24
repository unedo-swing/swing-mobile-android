from core.android_base_page import AndroidBasePage
from locators.swing_pass.manage_membership_locators import ManageMembershipLocators as L


class ManageMembershipPage(AndroidBasePage):

    ROWS = [
        L.ROW_BILLING_HISTORY,
        L.ROW_CHANGE_PLAN,
        L.ROW_CHANGE_METHOD,
        L.ROW_CONTACT_SUPPORT,
        L.ROW_CANCEL_MEMBERSHIP,
    ]

    def verify_sheet(self):
        self.wait_until_loaded()
        assert self.is_visible(L.row_cancel_membership, timeout=20), \
            "Manage membership sheet not shown"
        self.capture_step("manage_membership")

    def verify_options(self):
        missing = [r for r in self.ROWS if not self.is_visible(L.row_by_label % r)]
        self.capture_step("manage_options", "All options are shown" if not missing
                          else f"missing: {', '.join(missing)}")
        assert not missing, f"Manage membership option(s) not shown: {missing}"

    def open_billing_history(self):
        self.click(L.row_billing_history)
        self.capture_step("manage_billing_history")

    def open_change_plan(self):
        self.click(L.row_change_plan)
        self.capture_step("manage_change_plan")

    def open_change_method(self):
        self.click(L.row_change_method)
        self.capture_step("manage_change_method")

    def open_contact_support(self):
        self.click(L.row_contact_support)
        self.capture_step("manage_contact_support")

    def open_cancel_membership(self):
        self.click(L.row_cancel_membership)
        self.capture_step("manage_cancel")

    def open_option(self, label: str):
        self.click(L.row_by_label % label)
        self.capture_step("manage_option", f"Opened '{label}'")

    def tap_close(self):
        self.click(L.button_close)
        self.capture_step("manage_close")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("manage_dismiss")
