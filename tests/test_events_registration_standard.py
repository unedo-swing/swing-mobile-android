import pytest

from data.events_data import EventsData as E
from flows.login_flow import LoginFlow


@pytest.mark.android
class TestEventsRegistration:

    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["TC_E_002"], indirect=True)
    def test_event_registration_to_confirmation(
        self, TC_ID, driver, login_flow, events_flow, logout_flow
    ):
        login_flow.verify_home()

        events_flow.open_events()
        events_flow.select_event(E.EVENT_NAME)
        events_flow.verify_registration_state(E.REGISTRATION_TIME)
        events_flow.choose_registration(E.BOOKING_TYPE)

        if E.PLAYER_NAME:
            events_flow.add_player_by_name(E.PLAYER_NAME)

        events_flow.select_payment(E.PAYMENT_METHOD)
        events_flow.confirm.verify_screen()

        events_flow.pay_now()
        events_flow.finish()
        # logout_flow.logout()

    @pytest.mark.parametrize("TC_ID", ["TC_E_004"], indirect=True)
    def test_event_registration_switch_to_group(
        self, TC_ID, driver, login_flow, events_flow, logout_flow
    ):
        login_flow.verify_home()

        events_flow.open_events()
        events_flow.select_event(E.EVENT_NAME)
        events_flow.verify_registration_state(E.REGISTRATION_TIME)
        events_flow.choose_registration(E.BOOKING_TYPE)

        events_flow.edit_registartion_type(E.BOOKING_TYPE)
        events_flow.switch_registration(E.SWITCH_REGISTRATION_TYPE)
        events_flow.confirm_switch_registration()
        events_flow.verify_registration_type(E.SWITCH_REGISTRATION_TYPE)

        events_flow.select_payment(E.PAYMENT_METHOD)
        events_flow.confirm.verify_screen()

        events_flow.pay_now()
        events_flow.finish()
        # logout_flow.logout()
