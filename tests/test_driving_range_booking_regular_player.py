import pytest

from data.driving_range_data import DrivingRangeData as D, load_add_ons
from utils.pdf_reporter import init_pdf, generate_pdf


@pytest.mark.android
class TestDrivingRangeBookingRegularPlayer:
    @pytest.mark.app_state("clear")
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["DR_RP_001"])
    def test_verify_driving_range_venue_details_regular_player(self,TC_ID, login_flow, onboarding_flow, driving_range_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        login_flow.login_with_otp("Albania", "676777677710", "whatsapp")
        login_flow.allow_permissions()
        onboarding_flow.verify_whats_new()
        onboarding_flow.close_whats_new()
        onboarding_flow.verify_coach_marks()
        login_flow.verify_home()
        driving_range_flow.select_region(D.REGION)
        driving_range_flow.open_driving_range()
        driving_range_flow.search_and_open_range(D.DRIVING_RANGE_NAME)
        generate_pdf(pdf)
    
    @pytest.mark.app_state("force-stop")
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["DR_RP_003"])
    def test_verify_maximum_bays_regular_player(self,TC_ID, login_flow, driving_range_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        login_flow.verify_home()
        driving_range_flow.select_region(D.REGION)
        driving_range_flow.open_driving_range()
        driving_range_flow.search_and_open_range(D.DRIVING_RANGE_NAME)
        print(D.BOOKING_DATE)
        driving_range_flow.select_schedule(D.DRIVING_RANGE_NAME, D.BOOKING_DATE, D.BAY_NAME, D.TIME_SLOT_START, D.TIME_SLOT_END)
        driving_range_flow.verify_maximum_bays(D.NUMBER_OF_BAYS)
        generate_pdf(pdf)
    
    @pytest.mark.app_state("force-stop")
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["DR_RP_004"])
    def test_verify_minimum_balls_regular_player(self,TC_ID, login_flow, driving_range_flow):
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
        driving_range_flow.change_payment(D.PAYMENT_METHOD)
        driving_range_flow.pay_now()
        driving_range_flow.verify_minimum_balls(ADD_ONS)
        generate_pdf(pdf)
    
    
    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_RP_002"])
    def test_verify_featured_promo_driving_range_venue_details_regular_player(self,TC_ID, login_flow, driving_range_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        login_flow.verify_home()
        driving_range_flow.select_region(D.REGION)
        driving_range_flow.open_driving_range()
        driving_range_flow.search_and_open_range(D.DRIVING_RANGE_NAME)
        driving_range_flow.verify_featured_promo_exclusive_regular_member()
        generate_pdf(pdf)
    
    
    @pytest.mark.app_state("force-stop")
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["DR_RP_005", "DR_RP_006"])
    def test_end_to_end_booking_driving_range_without_promo_regular_player(self,TC_ID, login_flow, driving_range_flow):
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
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_RP_007", "DR_RP_008"])
    def test_end_to_end_booking_driving_range_with_autoapplied_promo_regular_player(self,TC_ID, login_flow, driving_range_flow):
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
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["DR_RP_009", "DR_RP_010"])
    def test_end_to_end_booking_driving_range_with_redeem_promo_regular_player(self,TC_ID, login_flow, driving_range_flow):
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
    @pytest.mark.parametrize("TC_ID", ["DR_RP_011", "DR_RP_012"])
    def test_end_to_end_booking_driving_range_with_changed_promo_regular_player(self,TC_ID, login_flow, driving_range_flow):
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
        driving_range_flow.apply_promo(D.PROMO_NAME)
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
    @pytest.mark.parametrize("TC_ID", ["DR_RP_013", "DR_RP_014"])
    def test_end_to_end_booking_driving_range_without_promo_used_credit_regular_player(self,TC_ID, login_flow, driving_range_flow):
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

    @pytest.mark.app_state("force-stop")
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["DR_RP_015", "DR_RP_016"])
    def test_end_to_end_booking_driving_range_with_promo_used_credit_regular_player(self,TC_ID, login_flow, driving_range_flow):
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

    @pytest.mark.app_state("force-stop")
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["DR_RP_017", "DR_RP_018"])
    def test_reschedule_booking_regular_player(self, TC_ID, login_flow, driving_range_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
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
    
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["DR_RP_019", "DR_RP_020"])
    def test_cancel_booking_regular_player(self, TC_ID, login_flow, driving_range_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
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
        generate_pdf(pdf)