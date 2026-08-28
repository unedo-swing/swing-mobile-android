import pytest

from data.login_data import LoginData as D
from utils.pdf_reporter import init_pdf, generate_pdf


class TestLogin:

    @pytest.mark.app_state("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_LOGIN_001"])
    def test_verify_page_login(self, TC_ID, login_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.open_login()
        generate_pdf(pdf)

    @pytest.mark.app_state("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_LOGIN_002", "TC_LOGIN_004"])
    def test_verify_login_with_whatsapp(self, TC_ID, login_flow, logout_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.open_login()
        login_flow.select_country(D.COUNTRY)
        login_flow.enter_phone_number(D.PHONE_NUMBER)
        login_flow.tap_continue_method_verify()
        login_flow.select_verification_method(D.VERIFICATION_METHOD)
        login_flow.input_otp_code(D.OTP)
        login_flow.verify_page_sport_option()
        login_flow.select_sport(D.SPORT_TYPE)
        login_flow.allow_permissions()
        login_flow.verify_coach_marks()
        login_flow.verify_whats_new()
        login_flow.close_whats_new()
        login_flow.verify_home(D.SPORT_TYPE, D.REGION)
        logout_flow.logout()
        generate_pdf(pdf)

    @pytest.mark.app_state("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_LOGIN_003", "TC_LOGIN_005"])
    def test_verify_login_with_sms(self, TC_ID, login_flow, logout_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.open_login()
        login_flow.select_country(D.COUNTRY)
        login_flow.enter_phone_number(D.PHONE_NUMBER)
        login_flow.tap_continue_method_verify()
        login_flow.select_verification_method(D.VERIFICATION_METHOD)
        login_flow.input_otp_code(D.OTP)
        login_flow.verify_page_sport_option()
        login_flow.select_sport(D.SPORT_TYPE)
        login_flow.allow_permissions()
        login_flow.verify_coach_marks()
        login_flow.verify_whats_new()
        login_flow.close_whats_new()
        login_flow.verify_home(D.SPORT_TYPE,  D.REGION)
        logout_flow.logout()
        generate_pdf(pdf)

