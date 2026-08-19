from flows.base_flow import BaseFlow
from pages.home_page import HomePage
from pages.swing_pass.swing_pass_page import SwingPassPage
from pages.swing_pass.manage_membership_page import ManageMembershipPage
from pages.swing_pass.billing_history_page import BillingHistoryPage
from pages.swing_pass.billing_details_page import BillingDetailsPage
from pages.swing_pass.change_billing_plan_page import ChangeBillingPlanPage
from pages.swing_pass.change_billing_method_page import ChangeBillingMethodPage
from pages.swing_pass.select_billing_method_page import SelectBillingMethodPage
from pages.swing_pass.cancel_confirmation_page import CancelConfirmationPage
from pages.swing_pass.cancel_swing_pass_page import CancelSwingPassPage


class SwingPassFlow(BaseFlow):
    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.home = self.page(HomePage)
        self.swing_pass = self.page(SwingPassPage)
        self.manage = self.page(ManageMembershipPage)
        self.billing_history = self.page(BillingHistoryPage)
        self.billing_details = self.page(BillingDetailsPage)
        self.change_plan = self.page(ChangeBillingPlanPage)
        self.change_method = self.page(ChangeBillingMethodPage)
        self.select_method = self.page(SelectBillingMethodPage)
        self.cancel_confirm = self.page(CancelConfirmationPage)
        self.cancel_pass = self.page(CancelSwingPassPage)

    # ================= open =================
    def open_swing_pass(self):
        self.home.verify_screen()
        self.home.open_swing_pass()
        self.swing_pass.verify_screen()

    def check_membership(self) -> dict:
        self.swing_pass.verify_active_membership()
        card = self.swing_pass.get_membership()
        billing = self.swing_pass.get_billing()
        self.swing_pass.capture_step(
            "swing_pass_summary",
            f"{card['pass_id']} — {billing['price']} / {billing['period']}",
            data={"card": card, "billing": billing},
        )
        return {"card": card, "billing": billing}

    def open_manage(self):
        self.swing_pass.open_manage()
        self.manage.verify_sheet()
        self.manage.verify_options()

    def leave_manage(self):
        self.manage.dismiss()
        self.swing_pass.verify_screen()

    # ================= billing history =================
    def open_billing_history(self):
        self.manage.open_billing_history()
        self.billing_history.verify_screen()

    def check_billing_history(self, expected_count: int | None = None) -> list:
        entries = self.billing_history.get_entries()
        assert entries, "Billing history is empty — expected at least one charge"
        if expected_count is not None:
            self.billing_history.verify_entry_count(expected_count)
        return entries

    def open_billing_entry(self, index: int = 1):
        self.billing_history.open_entry(index)
        self.billing_details.verify_screen()
        self.billing_details.verify_labels()

    def check_billing_details(self, **expected) -> dict:
        if expected:
            self.billing_details.verify_details(**expected)
        return self.billing_details.get_details()

    def leave_billing_details(self):
        self.billing_details.tap_back()
        self.billing_history.verify_screen()

    def leave_billing_history(self):
        self.billing_history.tap_back()
        self.swing_pass.verify_screen()

    def check_history(self, index: int = 1, expected_count: int | None = None,
                      **expected) -> dict:
        self.open_manage()
        self.open_billing_history()
        entries = self.check_billing_history(expected_count)
        row = entries[index - 1]
        self.open_billing_entry(index)
        details = self.check_billing_details(**expected)
        assert row["price"] == details["total"], (
            f"Billing history lists '{row['price']}' for this charge but the "
            f"details screen totals '{details['total']}'"
        )
        self.leave_billing_details()
        self.leave_billing_history()
        return {"entries": entries, "details": details}

    # ================= change billing plan =================
    def open_change_plan(self):
        self.manage.open_change_plan()
        self.change_plan.verify_screen()

    def check_plan_options(self) -> dict:
        plans = self.change_plan.get_plans()
        assert plans, "No selectable plans listed"
        current = self.change_plan.get_current_plan()
        return {"plans": plans, "current": current}

    def change_billing_plan(self, duration: str, confirm: bool = True) -> dict:
        self.open_manage()
        self.open_change_plan()
        options = self.check_plan_options()
        self.change_plan.verify_plan_listed(duration)
        self.change_plan.select_plan(duration)
        picked = self.change_plan.get_selected_plan()
        self.change_plan.accept_terms()
        if not confirm:
            self.change_plan.capture_step(
                "change_plan_dry_run", f"Stopped before confirming '{duration}'")
            return {**options, "picked": picked, "confirmed": False}
        self.change_plan.slide_to_confirm()
        self.swing_pass.verify_screen()
        self.swing_pass.verify_plan_updated(price=picked["price"], period=duration)
        return {**options, "picked": picked, "confirmed": True}

    # ================= change billing method =================
    def open_change_method(self):
        self.manage.open_change_method()
        self.change_method.verify_screen()

    def open_method_picker(self):
        self.change_method.open_method_picker()
        self.select_method.verify_screen()
        self.select_method.verify_sections()

    def check_payment_methods(self) -> dict:
        cards = self.select_method.get_cards()
        wallets = self.select_method.get_wallets()
        assert cards or wallets, "No payment methods listed"
        return {"cards": cards, "wallets": wallets}

    def change_billing_method(self, card_index: int = 1, confirm: bool = True) -> dict:
        self.open_manage()
        self.open_change_method()
        self.change_method.verify_no_method_selected()
        self.open_method_picker()
        methods = self.check_payment_methods()
        assert len(methods["cards"]) >= card_index, (
            f"Asked for saved card #{card_index} but only "
            f"{len(methods['cards'])} card(s) are listed"
        )
        picked = methods["cards"][card_index - 1]
        self.select_method.select_card(card_index)
        self.change_method.verify_screen()
        self.change_method.verify_selected_method(picked)
        self.change_method.accept_terms()
        if not confirm:
            self.change_method.capture_step(
                "change_method_dry_run", f"Stopped before confirming '{picked}'")
            return {**methods, "picked": picked, "confirmed": False}
        self.change_method.slide_to_confirm()
        self.swing_pass.verify_screen()
        self.swing_pass.verify_plan_updated(method=picked)
        return {**methods, "picked": picked, "confirmed": True}

    def connect_wallet(self, name: str):
        self.open_manage()
        self.open_change_method()
        self.open_method_picker()
        self.select_method.verify_wallet_listed(name)
        self.select_method.connect_wallet(name)

    # ================= cancel =================
    def open_cancel(self):
        self.manage.open_cancel_membership()
        self.cancel_confirm.verify_sheet()
        self.cancel_confirm.verify_options()

    def keep_membership(self):
        self.open_manage()
        self.open_cancel()
        self.cancel_confirm.tap_stay()
        self.swing_pass.verify_screen()
        self.swing_pass.verify_active_membership()

    def open_cancel_form(self) -> dict:
        self.open_cancel()
        savings = self.cancel_confirm.get_savings_amount()
        self.cancel_confirm.tap_proceed()
        self.cancel_pass.verify_screen()
        self.cancel_pass.verify_reasons()
        self.cancel_pass.verify_cancel_disabled()
        return {"savings_quoted": savings, "details": self.cancel_pass.get_details()}

    def cancel_membership(self, reason: str, confirm: bool = True) -> dict:
        self.open_manage()
        form = self.open_cancel_form()
        self.cancel_pass.select_reason(reason)
        self.cancel_pass.verify_cancel_enabled()
        if not confirm:
            self.cancel_pass.capture_step(
                "cancel_pass_dry_run", f"Stopped before cancelling ('{reason}')")
            return {**form, "cancelled": False}
        ends_on = form["details"]["ends_on"]
        self.cancel_pass.tap_cancel_membership()
        self.swing_pass.verify_screen()
        self.swing_pass.verify_cancelled(ends_on=ends_on)
        return {**form, "cancelled": True}

    # ================= renew =================
    def renew_membership(self):
        self.swing_pass.verify_screen()
        notice = self.swing_pass.get_cancellation_notice()
        assert notice, "Renew is only offered on a cancelled membership"
        self.swing_pass.tap_renew()
