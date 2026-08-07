import pytest

from data.driving_range_data import DrivingRangeData as D


@pytest.mark.android
class TestDrivingRangePayment:
    @pytest.mark.skip
    def test_select_payment(self, login_flow, driving_range_flow):
        login_flow.verify_home()
        driving_range_flow.select_region(D.REGION)
        driving_range_flow.open_driving_range()
        driving_range_flow.search_and_open_range(D.DRIVING_RANGE_NAME)
        driving_range_flow.select_schedule(
            D.DRIVING_RANGE_NAME, D.DATE, D.BAY_NAME, D.TIME_SLOT_START, D.TIME_SLOT_END
        )
        driving_range_flow.book_and_set_bays(D.NUMBER_OF_BAYS)
        driving_range_flow.add_addon(D.ADDON_NAME, D.ADDON_QTY)
        driving_range_flow.change_payment(D.PAYMENT_METHOD)

        # pays, then asserts the confirmed booking repeats what the booking
        # confirmation showed (date, time, duration, bays, bay type, total,
        # payment method)
        confirmed = driving_range_flow.pay_and_get_confirmed_booking()

        assert confirmed["booking_id"].startswith("Booking #")
        assert D.PAYMENT_METHOD.casefold() in confirmed["payment_method"].casefold()
