import pytest

from data.driving_range_data import DrivingRangeData as D


@pytest.mark.android
class TestDrivingRangeBooking:

    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["TC_DR_00002"], indirect=True)
    def test_end_to_end_booking_with_promo(self, TC_ID, login_flow, driving_range_flow):
        login_flow.verify_home()
        driving_range_flow.book_driving_range(
            D.REGION, D.DRIVING_RANGE_NAME, D.BOOKING_DATE, D.BAY_NAME,
            D.TIME_SLOT_START, D.TIME_SLOT_END, D.NUMBER_OF_BAYS,
        )
        driving_range_flow.apply_promo(D.PROMO_NAME)
        driving_range_flow.change_payment(D.PAYMENT_METHOD)
        confirmed = driving_range_flow.pay_and_get_confirmed_booking()

        assert confirmed["booking_id"].startswith("Booking #")
        assert D.PAYMENT_METHOD.casefold() in confirmed["payment_method"].casefold()

        driving_range_flow.open_booking_details()
        driving_range_flow.verify_booking_details(
            booking_id=confirmed["booking_id"], date=confirmed["date"],
            booking_time=confirmed["booking_time"], duration=confirmed["duration"],
            bays=confirmed["bays"], bay_type=confirmed["bay_type"], total=confirmed["total"],
        )

    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["TC_DR_00003"], indirect=True)
    def test_end_to_end_booking_with_auto_applied_promo(self, TC_ID, login_flow, driving_range_flow):
        login_flow.verify_home()
        driving_range_flow.book_driving_range(
            D.REGION, D.DRIVING_RANGE_NAME, D.BOOKING_DATE, D.BAY_NAME,
            D.TIME_SLOT_START, D.TIME_SLOT_END, D.NUMBER_OF_BAYS,
        )
        driving_range_flow.apply_promo(D.PROMO_NAME)
        driving_range_flow.change_payment(D.PAYMENT_METHOD)
        confirmed = driving_range_flow.pay_and_get_confirmed_booking()

        assert confirmed["booking_id"].startswith("Booking #")
        assert D.PAYMENT_METHOD.casefold() in confirmed["payment_method"].casefold()

        driving_range_flow.open_booking_details()
        driving_range_flow.verify_booking_details(
            booking_id=confirmed["booking_id"], date=confirmed["date"],
            booking_time=confirmed["booking_time"], duration=confirmed["duration"],
            bays=confirmed["bays"], bay_type=confirmed["bay_type"], total=confirmed["total"],
        )
    
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["TC_DR_00004"], indirect=True)
    def test_end_to_end_booking_without_promo(self, TC_ID, login_flow, driving_range_flow):
        login_flow.verify_home()
        driving_range_flow.book_driving_range(
            D.REGION, D.DRIVING_RANGE_NAME, D.BOOKING_DATE, D.BAY_NAME,
            D.TIME_SLOT_START, D.TIME_SLOT_END, D.NUMBER_OF_BAYS,
        )
        driving_range_flow.remove_promo()
        driving_range_flow.change_payment(D.PAYMENT_METHOD)
        confirmed = driving_range_flow.pay_and_get_confirmed_booking()

        assert confirmed["booking_id"].startswith("Booking #")
        assert D.PAYMENT_METHOD.casefold() in confirmed["payment_method"].casefold()

        driving_range_flow.open_booking_details()
        driving_range_flow.verify_booking_details(
            booking_id=confirmed["booking_id"], date=confirmed["date"],
            booking_time=confirmed["booking_time"], duration=confirmed["duration"],
            bays=confirmed["bays"], bay_type=confirmed["bay_type"], total=confirmed["total"],
        )

    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["TC_DR_00005"], indirect=True)
    def test_reschedule_booking(self, TC_ID, login_flow, driving_range_flow):
        # open the existing booking from the Activity screen
        login_flow.verify_home()
        driving_range_flow.open_activity()
        driving_range_flow.open_driving_range_card(
            D.DRIVING_RANGE_NAME, D.TIME_SLOT_START, D.BOOKING_DATE,
        )

        # reschedule — one step per screen
        driving_range_flow.open_reschedule()
        driving_range_flow.continue_reschedule()
        driving_range_flow.select_new_schedule(D.RESCHEDULE_DAY, D.RESCHEDULE_TIME)
        driving_range_flow.confirm_reschedule_reason(D.RESCHEDULE_REASON)
        driving_range_flow.submit_reschedule()
        driving_range_flow.verify_reschedule_success(D.DRIVING_RANGE_NAME)

        # the booking details now show the reschedule (Reschedule summary + history)
        driving_range_flow.reschedule_success.tap_see_booking_details()
        driving_range_flow.booking_details.verify_rescheduled()

    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_00006"], indirect=True)
    def test_cancel_booking(self, TC_ID, login_flow, driving_range_flow):
        # open the existing booking from the Activity screen
        login_flow.verify_home()
        driving_range_flow.open_activity()
        driving_range_flow.open_driving_range_card(
            D.DRIVING_RANGE_NAME, D.TIME_SLOT_START, D.BOOKING_DATE,
        )

        # cancel — one step per screen
        driving_range_flow.open_cancellation()
        driving_range_flow.continue_cancellation()
        driving_range_flow.select_cancellation_reason(D.CANCEL_REASON)
        driving_range_flow.set_refund_bank(
            D.BANK_NAME, D.BANK_ACCOUNT_NUMBER, D.BANK_ACCOUNT_NAME,
        )
        driving_range_flow.submit_cancellation()
        driving_range_flow.confirm_cancellation_dialog()
        driving_range_flow.verify_cancel_success(D.DRIVING_RANGE_NAME)

        # verify the refund/bank details on the cancellation details screen
        driving_range_flow.open_cancellation_details()
        driving_range_flow.cancellation_details.verify_refund_details(
            bank_name=D.BANK_NAME, account_number=D.BANK_ACCOUNT_NUMBER,
            account_holder_name=D.BANK_ACCOUNT_NAME,
        )
