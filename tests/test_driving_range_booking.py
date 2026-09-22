import pytest

from data.driving_range_data import DrivingRangeData as D, load_add_ons
from flows.driving_range_flow import DrivingRangeFlow
from flows.login_flow import LoginFlow
from utils.pdf_reporter import init_pdf, generate_pdf


@pytest.mark.android
class TestDrivingRangeBooking:

    def _login(self, login_flow: LoginFlow):
        login_flow.login_with_otp("Indonesia", "82165162549", "whatsapp")
        login_flow.allow_permissions()
        login_flow.verify_whats_new()
        login_flow.close_whats_new()
        login_flow.verify_coach_marks()

    def _open_venue(self, login_flow: LoginFlow, driving_range_flow: DrivingRangeFlow):
        login_flow.verify_home(D.SPORT_TYPE, D.REGION)
        driving_range_flow.select_region(D.REGION)
        driving_range_flow.open_driving_range()
        driving_range_flow.open_search()
        driving_range_flow.search_driving_range(D.DRIVING_RANGE_NAME)
        driving_range_flow.open_result(D.DRIVING_RANGE_NAME)

    def _open_booking_card(self, login_flow: LoginFlow, driving_range_flow: DrivingRangeFlow):
        login_flow.verify_home(D.SPORT_TYPE, D.REGION)
        driving_range_flow.open_activity()
        driving_range_flow.open_driving_range_card(
            D.DRIVING_RANGE_NAME, D.TIME_SLOT_START, D.BOOKING_DATE,
        )

    @pytest.mark.app_state("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_SP_001"])
    def test_verify_driving_range_venue_details_swing_pass_member(self, TC_ID, login_flow: LoginFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow)
        self._open_venue(login_flow, driving_range_flow)
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_SP_002"])
    def test_verify_featured_promo_driving_range_venue_details_swing_pass_member(self, TC_ID, login_flow: LoginFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._open_venue(login_flow, driving_range_flow)
        driving_range_flow.verify_exclusive_featured_promo_swing_pass_member()
        driving_range_flow.open_featured_promos()
        driving_range_flow.verify_featured_promos()
        driving_range_flow.back_to_details()
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_SP_003"])
    def test_verify_maximum_bays_swing_pass_member(self, TC_ID, login_flow: LoginFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._open_venue(login_flow, driving_range_flow)
        driving_range_flow.choose_date(D.DRIVING_RANGE_NAME, D.BOOKING_DATE)
        driving_range_flow.choose_bay_type(D.BAY_NAME)
        driving_range_flow.choose_time(D.TIME_SLOT_START, D.TIME_SLOT_END)
        driving_range_flow.book_driving_range()
        driving_range_flow.verify_maximum_bays_driving_range(D.NUMBER_OF_BAYS)
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_SP_004"])
    def test_verify_minimum_balls_swing_pass_member(self, TC_ID, login_flow: LoginFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        self._open_venue(login_flow, driving_range_flow)
        driving_range_flow.choose_date(D.DRIVING_RANGE_NAME, D.BOOKING_DATE)
        driving_range_flow.choose_bay_type(D.BAY_NAME)
        driving_range_flow.choose_time(D.TIME_SLOT_START, D.TIME_SLOT_END)
        driving_range_flow.book_driving_range()
        driving_range_flow.set_bays(D.NUMBER_OF_BAYS)
        driving_range_flow.confirm_bays()
        driving_range_flow.set_items(ADD_ONS)
        driving_range_flow.choose_payment_method(D.PAYMENT_METHOD)
        driving_range_flow.pay_now()
        driving_range_flow.verify_minimum_balls()
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_SP_005", "DR_SP_006"])
    def test_end_to_end_booking_driving_range_without_promo_swing_pass_member(self, TC_ID, login_flow: LoginFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        self._open_venue(login_flow, driving_range_flow)
        driving_range_flow.choose_date(D.DRIVING_RANGE_NAME, D.BOOKING_DATE)
        driving_range_flow.choose_bay_type(D.BAY_NAME)
        driving_range_flow.choose_time(D.TIME_SLOT_START, D.TIME_SLOT_END)
        driving_range_flow.book_driving_range()
        driving_range_flow.set_bays(D.NUMBER_OF_BAYS)
        driving_range_flow.confirm_bays()
        driving_range_flow.set_items(ADD_ONS)
        driving_range_flow.remove_promo()
        driving_range_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = driving_range_flow.get_payment_information_before_payment(D.BAY_NAME)
        driving_range_flow.pay_now()
        driving_range_flow.proceed_to_pay()
        confirmed = driving_range_flow.verify_payment_success_driving_range(payment_information, D.BAY_NAME)
        assert confirmed["booking_id"].startswith("Booking #")
        assert D.PAYMENT_METHOD.casefold() in confirmed["payment_method"].casefold()
        driving_range_flow.open_booking_details()
        driving_range_flow.verify_booking_details(
            booking_id=confirmed["booking_id"], date=confirmed["date"],
            booking_time=confirmed["booking_time"], duration=confirmed["duration"],
            bays=confirmed["bays"], bay_type=confirmed.get("bay_type"), total=confirmed["total"],
        )
        driving_range_flow.back_to_activity()
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_SP_007", "DR_SP_008"])
    def test_end_to_end_booking_driving_range_with_autoapplied_promo_swing_pass_member(self, TC_ID, login_flow: LoginFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        self._open_venue(login_flow, driving_range_flow)
        driving_range_flow.choose_date(D.DRIVING_RANGE_NAME, D.BOOKING_DATE)
        driving_range_flow.choose_bay_type(D.BAY_NAME)
        driving_range_flow.choose_time(D.TIME_SLOT_START, D.TIME_SLOT_END)
        driving_range_flow.book_driving_range()
        driving_range_flow.set_bays(D.NUMBER_OF_BAYS)
        driving_range_flow.confirm_bays()
        driving_range_flow.set_items(ADD_ONS)
        driving_range_flow.verify_promo_auto_applied(D.PROMO_NAME)
        driving_range_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = driving_range_flow.get_payment_information_before_payment(D.BAY_NAME)
        driving_range_flow.pay_now()
        driving_range_flow.proceed_to_pay()
        confirmed = driving_range_flow.verify_payment_success_driving_range(payment_information, D.BAY_NAME)
        assert confirmed["booking_id"].startswith("Booking #")
        assert D.PAYMENT_METHOD.casefold() in confirmed["payment_method"].casefold()
        driving_range_flow.open_booking_details()
        driving_range_flow.verify_booking_details(
            booking_id=confirmed["booking_id"], date=confirmed["date"],
            booking_time=confirmed["booking_time"], duration=confirmed["duration"],
            bays=confirmed["bays"], bay_type=confirmed.get("bay_type"), total=confirmed["total"],
        )
        driving_range_flow.back_to_activity()
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_SP_009", "DR_SP_010"])
    def test_end_to_end_booking_driving_range_with_redeem_promo_swing_pass_member(self, TC_ID, login_flow: LoginFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        self._open_venue(login_flow, driving_range_flow)
        driving_range_flow.choose_date(D.DRIVING_RANGE_NAME, D.BOOKING_DATE)
        driving_range_flow.choose_bay_type(D.BAY_NAME)
        driving_range_flow.choose_time(D.TIME_SLOT_START, D.TIME_SLOT_END)
        driving_range_flow.book_driving_range()
        driving_range_flow.set_bays(D.NUMBER_OF_BAYS)
        driving_range_flow.confirm_bays()
        driving_range_flow.set_items(ADD_ONS)
        driving_range_flow.apply_and_redeem_promo(D.PROMO_NAME, D.PROMO_CODE)
        driving_range_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = driving_range_flow.get_payment_information_before_payment(D.BAY_NAME)
        driving_range_flow.pay_now()
        driving_range_flow.proceed_to_pay()
        confirmed = driving_range_flow.verify_payment_success_driving_range(payment_information, D.BAY_NAME)
        assert confirmed["booking_id"].startswith("Booking #")
        assert D.PAYMENT_METHOD.casefold() in confirmed["payment_method"].casefold()
        driving_range_flow.open_booking_details()
        driving_range_flow.verify_booking_details(
            booking_id=confirmed["booking_id"], date=confirmed["date"],
            booking_time=confirmed["booking_time"], duration=confirmed["duration"],
            bays=confirmed["bays"], bay_type=confirmed.get("bay_type"), total=confirmed["total"],
        )
        driving_range_flow.back_to_activity()
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_SP_011", "DR_SP_012"])
    def test_end_to_end_booking_driving_range_with_changed_promo_swing_pass_member(self, TC_ID, login_flow: LoginFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        self._open_venue(login_flow, driving_range_flow)
        driving_range_flow.choose_date(D.DRIVING_RANGE_NAME, D.BOOKING_DATE)
        driving_range_flow.choose_bay_type(D.BAY_NAME)
        driving_range_flow.choose_time(D.TIME_SLOT_START, D.TIME_SLOT_END)
        driving_range_flow.book_driving_range()
        driving_range_flow.set_bays(D.NUMBER_OF_BAYS)
        driving_range_flow.confirm_bays()
        driving_range_flow.set_items(ADD_ONS)
        driving_range_flow.apply_promo(D.PROMO_NAME)
        driving_range_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = driving_range_flow.get_payment_information_before_payment(D.BAY_NAME)
        driving_range_flow.pay_now()
        driving_range_flow.proceed_to_pay()
        confirmed = driving_range_flow.verify_payment_success_driving_range(payment_information, D.BAY_NAME)
        assert confirmed["booking_id"].startswith("Booking #")
        assert D.PAYMENT_METHOD.casefold() in confirmed["payment_method"].casefold()
        driving_range_flow.open_booking_details()
        driving_range_flow.verify_booking_details(
            booking_id=confirmed["booking_id"], date=confirmed["date"],
            booking_time=confirmed["booking_time"], duration=confirmed["duration"],
            bays=confirmed["bays"], bay_type=confirmed.get("bay_type"), total=confirmed["total"],
        )
        driving_range_flow.back_to_activity()
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_SP_013", "DR_SP_014"])
    def test_end_to_end_booking_driving_range_without_promo_used_credit_swing_pass_member(self, TC_ID, login_flow: LoginFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        self._open_venue(login_flow, driving_range_flow)
        driving_range_flow.choose_date(D.DRIVING_RANGE_NAME, D.BOOKING_DATE)
        driving_range_flow.choose_bay_type(D.BAY_NAME)
        driving_range_flow.choose_time(D.TIME_SLOT_START, D.TIME_SLOT_END)
        driving_range_flow.book_driving_range()
        driving_range_flow.set_bays(D.NUMBER_OF_BAYS)
        driving_range_flow.confirm_bays()
        driving_range_flow.set_items(ADD_ONS)
        driving_range_flow.remove_promo()
        driving_range_flow.choose_payment_method(D.PAYMENT_METHOD)
        driving_range_flow.use_swing_credits()
        payment_information = driving_range_flow.get_payment_information_before_payment(D.BAY_NAME, "used_credit")
        driving_range_flow.pay_now()
        driving_range_flow.proceed_to_pay()
        confirmed = driving_range_flow.verify_payment_success_driving_range(payment_information, D.BAY_NAME)
        credit_used = confirmed.get("credit_used", "")
        assert confirmed["booking_id"].startswith("Booking #")
        assert D.PAYMENT_METHOD.casefold() in confirmed["payment_method"].casefold()
        driving_range_flow.open_booking_details()
        driving_range_flow.verify_booking_details(
            booking_id=confirmed["booking_id"], date=confirmed["date"],
            booking_time=confirmed["booking_time"], duration=confirmed["duration"],
            bays=confirmed["bays"], bay_type=confirmed.get("bay_type"), total=confirmed["total"],
        )
        driving_range_flow.back_to_activity()
        driving_range_flow.open_swing_credits()
        driving_range_flow.open_swing_credit_history()
        driving_range_flow.verify_used_credit_booking_code(confirmed["booking_id"], credit_used)
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_SP_015", "DR_SP_016"])
    def test_end_to_end_booking_driving_range_with_promo_used_credit_swing_pass_member(self, TC_ID, login_flow: LoginFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        self._open_venue(login_flow, driving_range_flow)
        driving_range_flow.choose_date(D.DRIVING_RANGE_NAME, D.BOOKING_DATE)
        driving_range_flow.choose_bay_type(D.BAY_NAME)
        driving_range_flow.choose_time(D.TIME_SLOT_START, D.TIME_SLOT_END)
        driving_range_flow.book_driving_range()
        driving_range_flow.set_bays(D.NUMBER_OF_BAYS)
        driving_range_flow.confirm_bays()
        driving_range_flow.set_items(ADD_ONS)
        driving_range_flow.verify_promo_auto_applied(D.PROMO_NAME)
        driving_range_flow.choose_payment_method(D.PAYMENT_METHOD)
        driving_range_flow.use_swing_credits()
        payment_information = driving_range_flow.get_payment_information_before_payment(D.BAY_NAME, "used_credit")
        driving_range_flow.pay_now()
        driving_range_flow.proceed_to_pay()
        confirmed = driving_range_flow.verify_payment_success_driving_range(payment_information, D.BAY_NAME)
        credit_used = confirmed.get("credit_used", "")
        assert confirmed["booking_id"].startswith("Booking #")
        assert D.PAYMENT_METHOD.casefold() in confirmed["payment_method"].casefold()
        driving_range_flow.open_booking_details()
        driving_range_flow.verify_booking_details(
            booking_id=confirmed["booking_id"], date=confirmed["date"],
            booking_time=confirmed["booking_time"], duration=confirmed["duration"],
            bays=confirmed["bays"], bay_type=confirmed.get("bay_type"), total=confirmed["total"],
        )
        driving_range_flow.back_to_activity()
        driving_range_flow.open_swing_credits()
        driving_range_flow.open_swing_credit_history()
        driving_range_flow.verify_used_credit_booking_code(confirmed["booking_id"], credit_used)
        generate_pdf(pdf)

    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_SP_017", "DR_SP_018"])
    def test_reschedule_booking_swing_pass_member(self, TC_ID, login_flow: LoginFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._open_booking_card(login_flow, driving_range_flow)

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
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_SP_019"])
    def test_cancel_booking_swing_pass_member(self, TC_ID, login_flow: LoginFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._open_booking_card(login_flow, driving_range_flow)

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
