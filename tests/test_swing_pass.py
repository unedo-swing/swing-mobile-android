import pytest

from data.swing_pass_data import SwingPassData as D


@pytest.mark.android
class TestSwingPass:

    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_001"])
    def test_open_swing_pass_from_home(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.check_membership()

    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_002"])
    def test_billing_history(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.check_membership()
        swing_pass_flow.check_history()

    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_003"])
    def test_plan_options_listed(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.open_manage()
        swing_pass_flow.open_change_plan()
        swing_pass_flow.check_plan_options()

    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_004"])
    def test_payment_methods_listed(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.open_manage()
        swing_pass_flow.open_change_method()
        swing_pass_flow.open_method_picker()
        swing_pass_flow.check_payment_methods()
        swing_pass_flow.select_method.verify_wallet_listed(D.EWALLET)

    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_005"])
    def test_change_billing_plan(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.change_billing_plan(D.NEW_PLAN)

    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_006"])
    def test_change_billing_method(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.change_billing_method(card_index=D.CARD_INDEX)

    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_007"])
    def test_cancel_needs_a_reason(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.cancel_membership(D.CANCEL_REASON, confirm=D.CONFIRM)

    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_008"])
    def test_stay_with_swing_pass(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.keep_membership()

    @pytest.mark.app_state('clear')
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["SP_009"])
    def test_join_landing_offers_swing_pass(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.open_join_swing_pass()
        swing_pass_flow.check_join_landing()

    @pytest.mark.app_state('clear')
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["SP_010"])
    def test_payment_options_offered(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.open_join_swing_pass()
        swing_pass_flow.open_payment_options()
        swing_pass_flow.payment_option.dismiss()

    @pytest.mark.app_state('clear')
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["SP_011"])
    def test_join_with_recurring_payment_stops_before_paying(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.join_swing_pass(
            D.PAYMENT_OPTION, D.BILLING_PLAN, card_index=D.CARD_INDEX, confirm=D.CONFIRM)

    @pytest.mark.app_state('clear')
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["SP_012"])
    def test_join_with_one_time_payment_stops_before_paying(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.join_swing_pass(
            D.PAYMENT_OPTION, D.BILLING_PLAN, card_index=D.CARD_INDEX, confirm=D.CONFIRM)

    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_013"])
    def test_pending_verification_after_relaunch(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.relaunch_app()
        swing_pass_flow.continue_pending_verification()
        swing_pass_flow.check_verification_form(D.FULL_NAME)
        swing_pass_flow.postpone_verification()

    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_014"])
    def test_verification_resumed_and_postponed(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.relaunch_app()
        swing_pass_flow.continue_pending_verification()
        swing_pass_flow.resume_verification()
        swing_pass_flow.verification.verify_submit_enabled(False)
        swing_pass_flow.postpone_verification()

    @pytest.mark.skip(
        reason="buys a Swing Pass for real with the saved billing method — the "
               "test account keeps the membership afterwards. Un-skip "
               "deliberately."
    )
    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_015"])
    def test_join_with_recurring_payment(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.join_swing_pass(
            D.PAYMENT_OPTION, D.BILLING_PLAN, card_index=D.CARD_INDEX, confirm=D.CONFIRM)
        swing_pass_flow.open_verification()
        swing_pass_flow.check_verification_form(D.FULL_NAME)
        swing_pass_flow.postpone_verification()

    @pytest.mark.skip(
        reason="buys a Swing Pass for real with a one time payment. Un-skip "
               "deliberately."
    )
    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_016"])
    def test_join_with_one_time_payment(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.join_swing_pass(
            D.PAYMENT_OPTION, D.BILLING_PLAN, card_index=D.CARD_INDEX, confirm=D.CONFIRM)
        swing_pass_flow.open_verification()
        swing_pass_flow.check_verification_form(D.FULL_NAME)
        swing_pass_flow.postpone_verification()

    @pytest.mark.skip(
        reason="submitting verification needs a camera capture the suite "
               "cannot produce — run the submit by hand, then this checks the "
               "result."
    )
    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_017"])
    def test_verification_submitted_state(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.check_verification_submitted()

    @pytest.mark.skip(
        reason="cancels the membership for real — the test account cannot get "
               "its Pass back except by buying one. Un-skip deliberately and "
               "run it last."
    )
    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_018"])
    def test_cancel_membership(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.cancel_membership(D.CANCEL_REASON, confirm=D.CONFIRM)

    @pytest.mark.skip(
        reason="needs an already-cancelled membership, and stops at the Renew "
               "tap — the purchase flow behind it has no page objects yet."
    )
    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SP_019"])
    def test_renew_after_cancel(self, TC_ID, login_flow, swing_pass_flow):
        D.load(TC_ID)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP)
        swing_pass_flow.open_swing_pass()
        swing_pass_flow.renew_membership()
