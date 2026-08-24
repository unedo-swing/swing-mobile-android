import pytest

from data.tee_time_data import TeeTimeData as D, load_add_ons, load_players
from utils.pdf_reporter import init_pdf, generate_pdf

@pytest.mark.android
class TestTeeTimeBooking:


    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["TT_014"])
    def test_verify_golf_course_details(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.verify_course_details()

        generate_pdf(pdf)

    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["TT_015"])
    def test_verify_featured_promo_on_golf_course_details(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.verify_featured_promo()

        generate_pdf(pdf)

    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_016"])
    def test_standard_booking_host_only_without_promo(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.BOOKING_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()
        tee_time_flow.remove_promo(D.HOST_NAME)
        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)
        player_display_names = [D.HOST_NAME]
        summary = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.BOOKING_DATE,
            preferred_time=D.PREFERRED_TIME,
            player_names=player_display_names,
            total_players=len(player_display_names),
        )
        tee_time_flow.pay_now()
        tee_time_flow.verify_confirmed_booking(
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
            payment_method=D.PAYMENT_METHOD,
        )

        # See booking details -> verify -> See complete breakdown -> verify
        tee_time_flow.open_confirmed_booking_details()
        tee_time_flow.verify_booking_details_screen(
            preferred_time=D.PREFERRED_TIME,
        )
        tee_time_flow.open_complete_breakdown()
        tee_time_flow.verify_booking_summary(
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
        )
        tee_time_flow.go_back_to_booking_details()
        tee_time_flow.go_back_to_activity()

        generate_pdf(pdf)
