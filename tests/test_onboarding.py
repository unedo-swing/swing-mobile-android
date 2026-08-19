import pytest

from data.onboarding_data import OnboardingData as D
from utils.pdf_reporter import init_pdf, generate_pdf


@pytest.mark.android
class TestOnboarding:

    @pytest.mark.app_state('reinstall')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_ONB_00001"])
    def test_onboarding_without_referreral_code(self, TC_ID, login_flow, onboarding_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP,
        )
        onboarding_flow.verify_profile()
        onboarding_flow.fill_profile(
            D.FIRST_NAME, D.LAST_NAME, D.BIRTH_DATE, D.NATIONALITY, D.GENDER,
            D.USERNAME, D.EMAIL, D.REFERRAL_CODE,
        )
        onboarding_flow.tap_next()
        onboarding_flow.choose_source(D.SOURCE)
        onboarding_flow.tap_finish()
        onboarding_flow.verify_whats_new()
        onboarding_flow.close_whats_new()
        onboarding_flow.verify_coach_marks()
        onboarding_flow.verify_home()
        generate_pdf(pdf)

    @pytest.mark.app_state('reinstall')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_ONB_00002"])
    def test_onboarding_with_referreral_code(self, TC_ID, login_flow, onboarding_flow,
                                             swing_credits_flow, logout_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP,
        )
        onboarding_flow.verify_profile()
        onboarding_flow.fill_profile(
            D.FIRST_NAME, D.LAST_NAME, D.BIRTH_DATE, D.NATIONALITY, D.GENDER,
            D.USERNAME, D.EMAIL, D.REFERRAL_CODE,
        )
        onboarding_flow.tap_next()
        onboarding_flow.choose_source(D.SOURCE)
        onboarding_flow.tap_finish()
        onboarding_flow.verify_whats_new()
        onboarding_flow.close_whats_new()
        onboarding_flow.verify_coach_marks()
        onboarding_flow.verify_home()
        swing_credits_flow.open_swing_credits()
        swing_credits_flow.open_history()
        swing_credits_flow.verify_referral_reward()
        swing_credits_flow.go_back_to_home()
        logout_flow.logout()
        generate_pdf(pdf)
