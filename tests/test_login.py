import pytest

from flows.login_flow import LoginFlow
from utils.pdf_reporter import init_pdf, generate_pdf



class TestLogin:
    @pytest.mark.smoke
    def test_login_with_whatsapp(
        self,
        driver
    ):
        pdf = init_pdf("test_login_screen_loads")
        login_flow = LoginFlow(driver, pdf)
        login_flow.open_login()
        login_flow.select_country("Indonesia")
        login_flow.enter_phone_number("82165162549")
        login_flow.tap_continue_method_verify()
        login_flow.select_method_verification_whatsapp()
        login_flow.input_otp()
        generate_pdf(pdf)
    
