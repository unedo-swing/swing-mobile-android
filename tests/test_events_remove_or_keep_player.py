import pytest

from data.events_data import EventsData as E
from utils.pdf_reporter import init_pdf, generate_pdf

@pytest.mark.android
class TestEventsRemoveorKeep:

    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["TC_E_006"], indirect=True)
    def test_events_keep_player(
        self, TC_ID, driver, login_flow, events_flow, logout_flow
    ):
        E.load(TC_ID)
        pdf = init_pdf(E.TC_NAME, tc_id=TC_ID)
        login_flow.verify_home()

        events_flow.open_events()
        events_flow.select_event(E.EVENT_NAME)
        events_flow.verify_registration_state(E.REGISTRATION_TIME)
        events_flow.choose_registration(E.BOOKING_TYPE)

        if E.PLAYER_NAME:
            events_flow.add_player_by_name(E.PLAYER_NAME)

        events_flow.verify_total_player(2);
        events_flow.tap_remove_player_button(2);
        events_flow.confirm_keep_player();
        events_flow.verify_total_player(2);
        generate_pdf(pdf)

    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["TC_E_007"], indirect=True)
    def test_events_remove_player(
        self, TC_ID, driver, login_flow, events_flow, logout_flow
    ):
        E.load(TC_ID)
        pdf = init_pdf(E.TC_NAME, tc_id=TC_ID)
        login_flow.verify_home()

        events_flow.open_events()
        events_flow.select_event(E.EVENT_NAME)
        events_flow.verify_registration_state(E.REGISTRATION_TIME)
        events_flow.choose_registration(E.BOOKING_TYPE)

        if E.PLAYER_NAME:
            events_flow.add_player_by_name(E.PLAYER_NAME)

        events_flow.verify_total_player(2);
        events_flow.tap_remove_player_button(2);
        events_flow.confirm_remove_player();
        events_flow.verify_total_player(1);
        generate_pdf(pdf)