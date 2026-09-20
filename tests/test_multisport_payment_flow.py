import pytest

from data.multisport_data import MultisportData as M
from utils.pdf_reporter import init_pdf, generate_pdf

@pytest.mark.android
class TestMultisportFlowPayment:
    
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_008"])
    def test_multisport_end_to_end_payment(login_flow, multisport_flow, TC_ID):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)
        multisport_flow.view_all_venue()
        multisport_flow.select_venue(M.VENUE_NAME)
        multisport_flow.book_venue()
        multisport_flow.select_schedule_flow(M.TITLE_SCHEDULE, M.HOW_MUCH_SCHEDULE)
        multisport_flow.confirm_schedule()
        multisport_flow.add_player_by_name(M.PLAYER_NAME)
        multisport_flow.payment_method_flow(M.PAYMENT_METHOD)
        multisport_flow.pay_now()
        multisport_flow.finish()

        generate_pdf(pdf)