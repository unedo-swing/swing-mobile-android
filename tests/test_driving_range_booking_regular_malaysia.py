import pytest

from data.driving_range_data import DrivingRangeData as D, load_add_ons
from utils.pdf_reporter import init_pdf, generate_pdf


@pytest.mark.android
class TestDrivingRangeBookingRegularMalaysia:

    @pytest.mark.app_state("force-stop")
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["DR_MY_RP_001"])
    def test_end_to_end_booking_driving_range_without_promo_regular_malaysia(self,TC_ID, login_flow, driving_range_flow):
        D.load(TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        login_flow.verify_home()
        driving_range_flow.select_region(D.REGION)
        driving_range_flow.open_driving_range()
        driving_range_flow.search_and_open_range(D.DRIVING_RANGE_NAME)
        driving_range_flow.select_schedule(D.DRIVING_RANGE_NAME, D.BOOKING_DATE, D.BAY_NAME, D.TIME_SLOT_START, D.TIME_SLOT_END)
        driving_range_flow.book_and_set_bays(D.NUMBER_OF_BAYS)
        driving_range_flow.add_addons(ADD_ONS)
        driving_range_flow.remove_promo()
        driving_range_flow.change_payment(D.PAYMENT_METHOD)
        before = driving_range_flow.get_data_before_payment(D.BAY_NAME)
        confirmed = driving_range_flow.pay_and_get_confirmed_booking(before, D.BAY_NAME)
        print(confirmed["booking_id"])
        assert confirmed["booking_id"].startswith("Booking #")
        assert D.PAYMENT_METHOD.casefold() in confirmed["payment_method"].casefold()
        driving_range_flow.open_booking_details()
        driving_range_flow.verify_booking_details(
            booking_id=confirmed["booking_id"], date=confirmed["date"],
            booking_time=confirmed["booking_time"], duration=confirmed["duration"],
            bays=confirmed["bays"], bay_type=confirmed.get("bay_type"), total=confirmed["total"],
        )
        driving_range_flow.go_back_to_activity()

        generate_pdf(pdf)


    @pytest.mark.app_state("force-stop")
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["DR_MY_RP_003"])
    def test_end_to_end_booking_driving_range_with_redeem_promo_regular_malaysia(self,TC_ID, login_flow, driving_range_flow):
        D.load(TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        login_flow.verify_home()
        driving_range_flow.select_region(D.REGION)
        driving_range_flow.open_driving_range()
        driving_range_flow.search_and_open_range(D.DRIVING_RANGE_NAME)
        driving_range_flow.select_schedule(D.DRIVING_RANGE_NAME, D.BOOKING_DATE, D.BAY_NAME, D.TIME_SLOT_START, D.TIME_SLOT_END)
        driving_range_flow.book_and_set_bays(D.NUMBER_OF_BAYS)
        driving_range_flow.add_addons(ADD_ONS)
        driving_range_flow.change_promo_with_add_promo_code(D.PROMO_NAME, D.PROMO_CODE)
        driving_range_flow.change_payment(D.PAYMENT_METHOD)
        before = driving_range_flow.get_data_before_payment(D.BAY_NAME)
        confirmed = driving_range_flow.pay_and_get_confirmed_booking(before, D.BAY_NAME)
        assert confirmed["booking_id"].startswith("Booking #")
        assert D.PAYMENT_METHOD.casefold() in confirmed["payment_method"].casefold()
        driving_range_flow.open_booking_details()
        driving_range_flow.verify_booking_details(
            booking_id=confirmed["booking_id"], date=confirmed["date"],
            booking_time=confirmed["booking_time"], duration=confirmed["duration"],
            bays=confirmed["bays"], bay_type=confirmed.get("bay_type"), total=confirmed["total"],
        )
        driving_range_flow.go_back_to_activity()

        generate_pdf(pdf)
        
    @pytest.mark.app_state("force-stop")
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["DR_MY_RP_002"])
    def test_end_to_end_booking_driving_range_with_autoapplied_promo_regular_malaysia(self,TC_ID, login_flow, driving_range_flow):
        D.load(TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        login_flow.verify_home()
        driving_range_flow.select_region(D.REGION)
        driving_range_flow.open_driving_range()
        driving_range_flow.search_and_open_range(D.DRIVING_RANGE_NAME)
        driving_range_flow.select_schedule(D.DRIVING_RANGE_NAME, D.BOOKING_DATE, D.BAY_NAME, D.TIME_SLOT_START, D.TIME_SLOT_END)
        driving_range_flow.book_and_set_bays(D.NUMBER_OF_BAYS)
        driving_range_flow.add_addons(ADD_ONS)
        driving_range_flow.verify_promo_auto_applied(D.PROMO_NAME)
        driving_range_flow.change_payment(D.PAYMENT_METHOD)
        before = driving_range_flow.get_data_before_payment(D.BAY_NAME)
        confirmed = driving_range_flow.pay_and_get_confirmed_booking(before, D.BAY_NAME)
        assert confirmed["booking_id"].startswith("Booking #")
        assert D.PAYMENT_METHOD.casefold() in confirmed["payment_method"].casefold()
        driving_range_flow.open_booking_details()
        driving_range_flow.verify_booking_details(
            booking_id=confirmed["booking_id"], date=confirmed["date"],
            booking_time=confirmed["booking_time"], duration=confirmed["duration"],
            bays=confirmed["bays"], bay_type=confirmed.get("bay_type"), total=confirmed["total"],
        )
        driving_range_flow.go_back_to_activity()

        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_MY_RP_004"])
    def test_end_to_end_booking_driving_range_without_promo_used_credit_regular_malaysia(self,TC_ID, login_flow, driving_range_flow):
        D.load(TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        login_flow.verify_home()
        driving_range_flow.select_region(D.REGION)
        driving_range_flow.open_driving_range()
        driving_range_flow.search_and_open_range(D.DRIVING_RANGE_NAME)
        driving_range_flow.select_schedule(D.DRIVING_RANGE_NAME, D.BOOKING_DATE, D.BAY_NAME, D.TIME_SLOT_START, D.TIME_SLOT_END)
        driving_range_flow.book_and_set_bays(D.NUMBER_OF_BAYS)
        driving_range_flow.add_addons(ADD_ONS)
        driving_range_flow.remove_promo()
        driving_range_flow.change_payment(D.PAYMENT_METHOD)
        driving_range_flow.switch_on_swing_credits()
        before = driving_range_flow.get_data_before_payment(D.BAY_NAME, "used_credit")
        confirmed = driving_range_flow.pay_and_get_confirmed_booking(before, D.BAY_NAME)
        credit_used = confirmed.get("credit_used", "")
        assert confirmed["booking_id"].startswith("Booking #")
        assert D.PAYMENT_METHOD.casefold() in confirmed["payment_method"].casefold()
        driving_range_flow.open_booking_details()
        driving_range_flow.verify_booking_details(
            booking_id=confirmed["booking_id"], date=confirmed["date"],
            booking_time=confirmed["booking_time"], duration=confirmed["duration"],
            bays=confirmed["bays"], bay_type=confirmed.get("bay_type"), total=confirmed["total"],
        )
        driving_range_flow.go_back_to_activity()

        driving_range_flow.verify_swing_credit_usaged(confirmed["booking_id"], credit_used)

        generate_pdf(pdf)
