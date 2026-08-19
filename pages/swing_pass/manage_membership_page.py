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

    # ================= verify steps =================
    def verify_sheet(self):
        self.wait_until_loaded()
        assert self.is_visible(L.row_cancel_membership, timeout=20), \
            "Manage membership sheet not shown"
        self.capture_step("manage_membership", "Manage membership sheet is visible")

    def verify_options(self):
        missing = [r for r in self.ROWS if not self.is_visible(L.row_by_label % r)]
        self.capture_step("manage_options", "All options are shown" if not missing
                          else f"missing: {', '.join(missing)}")
        assert not missing, f"Manage membership option(s) not shown: {missing}"

    # ================= action steps =================
    def open_billing_history(self):
        self.click(L.row_billing_history)
        self.capture_step("manage_billing_history", "Opened See billing history")

    def open_change_plan(self):
        self.click(L.row_change_plan)
        self.capture_step("manage_change_plan", "Opened Change billing plan")

    def open_change_method(self):
        self.click(L.row_change_method)
        self.capture_step("manage_change_method", "Opened Change billing method")

    def open_contact_support(self):
        self.click(L.row_contact_support)
        self.capture_step("manage_contact_support", "Opened Contact Swing Support")

    def open_cancel_membership(self):
        # Opens the cancellation flow (a confirmation screen follows — this
        # only taps the row, it does not cancel the membership).
        self.click(L.row_cancel_membership)
        self.capture_step("manage_cancel", "Opened Cancel Swing Pass membership")

    def open_option(self, label: str):
        self.click(L.row_by_label % label)
        self.capture_step("manage_option", f"Opened '{label}'")

    def tap_close(self):
        self.click(L.button_close)
        self.capture_step("manage_close", "Closed the Manage membership sheet")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("manage_dismiss", "Dismissed the Manage membership sheet")
