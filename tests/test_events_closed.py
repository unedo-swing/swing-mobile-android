import pytest

from data.events_data import EventsData as E
from flows.login_flow import LoginFlow


@pytest.mark.android
class TestEvents:

    @pytest.mark.parametrize("TC_ID", ["TC_E_001"], indirect=True)
    def test_event_registration_state(
        self, TC_ID, driver, login_flow, events_flow, logout_flow
    ):
        login_flow.verify_home()

        events_flow.open_events()
        events_flow.select_event(E.EVENT_NAME)
        events_flow.verify_registration_state(E.REGISTRATION_TIME)

        # logout_flow.logout()
