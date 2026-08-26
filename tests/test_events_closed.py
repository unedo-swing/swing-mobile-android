import pytest

from data.events_data import EventsData as E
from utils.pdf_reporter import init_pdf, generate_pdf


@pytest.mark.android
class TestEvents:

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_E_001"])
    def test_event_registration_state(
        self, TC_ID, driver, login_flow, events_flow, logout_flow
    ):
        E.load(TC_ID)
        pdf = init_pdf(E.TC_NAME, tc_id=TC_ID)
        login_flow.verify_home()

        events_flow.open_events()
        events_flow.select_event(E.EVENT_NAME)
        events_flow.verify_registration_state(E.REGISTRATION_TIME)

        generate_pdf(pdf)
        # logout_flow.logout()
