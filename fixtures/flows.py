"""One fixture per flow.

They all go through ``flow()``, which registers the flow with the active PDF
reporter — that is what puts each step into the evidence, so build flows here
and never by calling the class directly. Registered from the root conftest via
``pytest_plugins``.
"""
import pytest

from flows.driving_range_flow import DrivingRangeFlow
from flows.events_flow import EventsFlow
from flows.login_flow import LoginFlow
from flows.logout_flow import LogoutFlow
from flows.onboarding_flow import OnboardingFlow
from flows.swing_credits_flow import SwingCreditsFlow
from flows.swing_pass_flow import SwingPassFlow
from flows.tee_time_flow import TeeTimeFlow
from flows.multisport_flow import MultisportFlow
from utils.pdf_reporter import register_flow


@pytest.fixture
def flow(driver, pdf_evidence):
    def _make(flow_class):
        return register_flow(flow_class(driver))
    return _make


@pytest.fixture
def login_flow(flow):
    return flow(LoginFlow)


@pytest.fixture
def logout_flow(flow):
    return flow(LogoutFlow)


@pytest.fixture
def onboarding_flow(flow):
    return flow(OnboardingFlow)


@pytest.fixture
def tee_time_flow(flow):
    return flow(TeeTimeFlow)


@pytest.fixture
def driving_range_flow(flow):
    return flow(DrivingRangeFlow)


@pytest.fixture
def swing_credits_flow(flow):
    return flow(SwingCreditsFlow)


@pytest.fixture
def swing_pass_flow(flow):
    return flow(SwingPassFlow)


@pytest.fixture
def events_flow(flow):
    return flow(EventsFlow)

@pytest.fixture
def multisport_flow(flow):
    return flow(MultisportFlow)