"""
Driving Range — verify pages.

Page-verification scenarios only: each drives from Home down to a screen and
checks it renders correctly. Booking/promo/payment scenarios live in
tests/test_driving_range_booking.py.

Test data comes from data/driving_range_data.xlsx (see DrivingRangeData).
"""
import pytest

from data.driving_range_data import DrivingRangeData as D


@pytest.mark.android
class TestDrivingRangeVerifyPages:

    @pytest.mark.skip
    def test_verify_home_page(self, login_flow):
        # user already logged in -> Home should be shown
        login_flow.verify_home()

    @pytest.mark.skip
    def test_verify_explore_driving_range(self, login_flow, driving_range_flow):
        login_flow.verify_home()
        driving_range_flow.select_region(D.REGION)
        driving_range_flow.open_driving_range()  # verifies the explore screen

    @pytest.mark.skip
    def test_verify_range_details(self, login_flow, driving_range_flow):
        login_flow.verify_home()
        driving_range_flow.select_region(D.REGION)
        driving_range_flow.open_driving_range()
        # searches, opens the range, verifies the details screen + range name
        driving_range_flow.search_and_open_range(D.DRIVING_RANGE_NAME)

    @pytest.mark.skip
    def test_verify_booking_confirmation(self, login_flow, driving_range_flow):
        login_flow.verify_home()
        driving_range_flow.book_driving_range(
            D.REGION, D.DRIVING_RANGE_NAME, D.BOOKING_DATE, D.BAY_NAME,
            D.TIME_SLOT_START, D.TIME_SLOT_END, D.NUMBER_OF_BAYS,
        )  # navigates + books -> verifies the booking confirmation screen

        # the confirmation must echo what was selected
        driving_range_flow.verify_booking_confirmation_details(
            date=D.BOOKING_DATE, time_start=D.TIME_SLOT_START, time_end=D.TIME_SLOT_END,
            bays=D.NUMBER_OF_BAYS, bay_type=D.BAY_NAME,
        )
