import pytest

from data.onboarding_data import OnboardingData as D
from utils.pdf_reporter import init_pdf, generate_pdf


@pytest.mark.android
class TestOnboarding:

    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_ONB_001", "TC_ONB_005"])
    def test_onboarding_without_referreral_code(self, TC_ID, onboarding_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        onboarding_flow.login_with_otp(
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
        onboarding_flow.select_sport(D.SPORT_TYPE)
        onboarding_flow.allow_permissions()
        onboarding_flow.verify_coach_marks()
        onboarding_flow.verify_whats_new()
        onboarding_flow.close_whats_new()
        onboarding_flow.verify_home(D.SPORT_TYPE, D.REGION)
        generate_pdf(pdf)

    @pytest.mark.app_state('clear')
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_ONB_002", "TC_ONB_006"])
    def test_onboarding_with_referreral_code(self, TC_ID, onboarding_flow,
                                             swing_credits_flow, logout_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        onboarding_flow.login_with_otp(
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
        onboarding_flow.select_sport(D.SPORT_TYPE)
        onboarding_flow.allow_permissions()
        onboarding_flow.verify_coach_marks()
        onboarding_flow.verify_whats_new()
        onboarding_flow.close_whats_new()
        onboarding_flow.verify_home(D.SPORT_TYPE, D.REGION)
        swing_credits_flow.verify_history_credit_using_referral(D.REGION)
        logout_flow.logout()

        generate_pdf(pdf)
