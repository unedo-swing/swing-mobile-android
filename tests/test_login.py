import pytest

from data.login_data import LoginData as D
from utils.pdf_reporter import init_pdf, generate_pdf


class TestLogin:

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_LOGIN_00001"])
    def test_verify_page_login(self, TC_ID, login_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.open_login()
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_LOGIN_00002"])
    def test_verify_login_with_whatsapp(self, TC_ID, login_flow, logout_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.open_login()
        login_flow.select_country(D.COUNTRY)
        login_flow.enter_phone_number(D.PHONE_NUMBER)
        login_flow.tap_continue_method_verify()
        login_flow.select_verification_method(D.VERIFICATION_METHOD)
        login_flow.input_otp_code(D.OTP)
        login_flow.verify_home()
        logout_flow.logout()
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_LOGIN_00003"])
    def test_verify_login_with_sms(self, TC_ID, login_flow, logout_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.open_login()
        login_flow.select_country(D.COUNTRY)
        login_flow.enter_phone_number(D.PHONE_NUMBER)
        login_flow.tap_continue_method_verify()
        login_flow.select_verification_method(D.VERIFICATION_METHOD)
        login_flow.input_otp_code(D.OTP)
        login_flow.verify_home()
        logout_flow.logout()
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_LOGIN_00004"])
    def test_verify_login_without_logout(self, TC_ID, login_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.login_with_otp(
            D.COUNTRY, D.PHONE_NUMBER, D.VERIFICATION_METHOD, D.OTP,
        )
        login_flow.verify_home()
        # no logout on purpose — the next test starts from a signed-in app
        generate_pdf(pdf)
