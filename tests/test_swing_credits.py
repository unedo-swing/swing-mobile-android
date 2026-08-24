import pytest

from data.swing_credit_data import SwingCreditData as D
from utils.pdf_reporter import init_pdf, generate_pdf


@pytest.mark.android
class TestSwingCredits:

    @pytest.mark.app_state("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SC_001"])
    def test_verify_swing_credits_page(self, TC_ID, login_flow, onboarding_flow, swing_credits_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        login_flow.login_with_otp("Indonesia", "82165162549", "whatsapp")
        login_flow.allow_permissions()
        onboarding_flow.verify_whats_new()
        onboarding_flow.close_whats_new()
        onboarding_flow.verify_coach_marks()
        login_flow.verify_home()
        swing_credits_flow.open_swing_credits()
        balance = swing_credits_flow.verify_swing_credits_page()
        assert balance != "", "Swing Credits balance is not shown"
        swing_credits_flow.open_history()
        swing_credits_flow.leave_history()
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SC_002"])
    def test_verify_earn_credit_by_booking_code(self, TC_ID, login_flow, swing_credits_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        login_flow.verify_home()
        swing_credits_flow.open_swing_credits()
        swing_credits_flow.open_history()
        swing_credits_flow.verify_earned_credit(D.BOOKING_CODE, D.TOTAL_CREDIT)
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["SC_003"])
    def test_verify_used_credit_by_booking_code(self, TC_ID, login_flow, swing_credits_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        login_flow.verify_home()
        swing_credits_flow.open_swing_credits()
        swing_credits_flow.open_history()
        swing_credits_flow.verify_used_credit(D.BOOKING_CODE, D.TOTAL_CREDIT)
        generate_pdf(pdf)
