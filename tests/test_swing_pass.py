import pytest

from data.swing_pass_data import SwingPassData as D
from utils.pdf_reporter import init_pdf, generate_pdf


def _require_membership(swing_pass_flow):
    swing_pass_flow.home.verify_screen()
    if not swing_pass_flow.home.has_swing_pass():
        pytest.skip(
            "this account holds no Swing Pass — Home shows 'Join Swing Pass'. "
            "Run the suite with a member account."
        )


@pytest.mark.android
class TestSwingPass:

    @pytest.mark.regression
    def test_open_swing_pass_from_home(self, swing_pass_flow):
        _require_membership(swing_pass_flow)
        swing_pass_flow.open_swing_pass()
        summary = swing_pass_flow.check_membership()

        assert summary["card"]["pass_id"], "Membership card shows no Pass ID"
        assert summary["billing"]["price"], "Billing row shows no price"
        assert not summary["billing"]["cancelled"], \
            "Membership is already cancelled — the read-only suite needs an active Pass"

    @pytest.mark.regression
    def test_billing_history_matches_details(self, swing_pass_flow):
        _require_membership(swing_pass_flow)
        swing_pass_flow.open_swing_pass()
        card = swing_pass_flow.check_membership()["card"]

        history = swing_pass_flow.check_history()

        assert history["entries"], "No charges in the billing history"
        assert history["details"]["membership_id"] == card["pass_id"], (
            f"Billing Details names membership '{history['details']['membership_id']}' "
            f"but the card reads '{card['pass_id']}'"
        )

    @pytest.mark.regression
    def test_plan_options_listed(self, swing_pass_flow):
        _require_membership(swing_pass_flow)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.open_manage()
        swing_pass_flow.open_change_plan()
        options = swing_pass_flow.check_plan_options()

        current = options["current"]["duration"]
        assert current, "No 'Current plan' card on the screen"
        assert current not in [p["duration"] for p in options["plans"]], (
            f"The current plan '{current}' is offered as a selectable option — "
            "it should carry the 'Current plan' badge and no radio"
        )

    @pytest.mark.regression
    def test_payment_methods_listed(self, swing_pass_flow):
        _require_membership(swing_pass_flow)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.open_manage()
        swing_pass_flow.open_change_method()
        swing_pass_flow.open_method_picker()
        methods = swing_pass_flow.check_payment_methods()

        assert methods["cards"], "No saved cards listed"
        assert D.EWALLET in methods["wallets"], (
            f"E-wallet '{D.EWALLET}' not offered — screen lists {methods['wallets']}"
        )

    @pytest.mark.regression
    def test_cancel_needs_a_reason(self, swing_pass_flow):
        _require_membership(swing_pass_flow)
        swing_pass_flow.open_swing_pass()
        saved = swing_pass_flow.swing_pass.get_savings()["amount"]

        result = swing_pass_flow.cancel_membership(D.CANCEL_REASON, confirm=False)

        assert result["cancelled"] is False
        assert result["savings_quoted"] == saved, (
            f"The confirmation sheet quotes '{result['savings_quoted']}' but the "
            f"savings card reads '{saved}'"
        )
        assert result["details"]["ends_on"], "Cancellation form shows no end date"

    @pytest.mark.regression
    def test_stay_with_swing_pass(self, swing_pass_flow):
        _require_membership(swing_pass_flow)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.keep_membership()

    # ================= state-changing (reversible) =================
    @pytest.mark.regression
    def test_change_billing_plan(self, swing_pass_flow):
        _require_membership(swing_pass_flow)
        swing_pass_flow.open_swing_pass()
        result = swing_pass_flow.change_billing_plan(D.NEW_PLAN)

        assert result["confirmed"] is True
        assert D.NEW_PLAN in result["picked"]["duration"], (
            f"Confirmed plan reads '{result['picked']['duration']}', "
            f"expected it to be '{D.NEW_PLAN}'"
        )

    @pytest.mark.regression
    def test_change_billing_method(self, swing_pass_flow):
        _require_membership(swing_pass_flow)
        swing_pass_flow.open_swing_pass()
        result = swing_pass_flow.change_billing_method(card_index=D.CARD_INDEX)

        assert result["confirmed"] is True
        assert result["picked"], "No card label captured for the confirmed method"

    # ================= irreversible =================
    @pytest.mark.regression(
        reason="cancels the membership for real — the test account cannot get "
               "its Pass back except by buying one. Un-skip deliberately and "
               "run it last."
    )
    def test_cancel_membership(self, swing_pass_flow):
        _require_membership(swing_pass_flow)
        swing_pass_flow.open_swing_pass()
        result = swing_pass_flow.cancel_membership(D.CANCEL_REASON)

        assert result["cancelled"] is True
        swing_pass_flow.swing_pass.verify_ends_on(result["details"]["ends_on"])

    @pytest.mark.regression(
        reason="needs an already-cancelled membership, and stops at the Renew "
               "tap — the purchase flow behind it has no page objects yet."
    )
    def test_renew_after_cancel(self, swing_pass_flow):
        _require_membership(swing_pass_flow)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.renew_membership()
