import pytest

from data.tee_time_data import TeeTimeData as D, load_add_ons, load_players
from utils.pdf_reporter import init_pdf, generate_pdf


@pytest.mark.android
class TestTeeTimeBooking:
    
    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_001"])
    def test_standard_booking_host_only(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home(D.SPORT_TYPE, D.REGION)
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.BOOKING_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

        settled = tee_time_flow.setup_players(
            [],
            host_name=D.HOST_NAME,
            host_promo=D.EXPECTED_PROMO,
            promo_code=D.PROMO_CODE,
        )
        player_display_names = [D.HOST_NAME]
        assert list(settled) == player_display_names, \
            f"Players on the confirmation {list(settled)} != expected {player_display_names}"

        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)
        before = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.BOOKING_DATE,
            preferred_time=D.PREFERRED_TIME,
            player_names=player_display_names,
            total_players=len(player_display_names),
        )
        confirmed = tee_time_flow.pay_and_get_confirmed_booking(
            before,
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
            no_of_players=len(player_display_names),
            payment_method=D.PAYMENT_METHOD,
        )

        tee_time_flow.open_confirmed_booking_details()
        tee_time_flow.compare_payment_success_with_booking_details(confirmed)
        tee_time_flow.open_complete_breakdown()
        tee_time_flow.verify_player_in_summary(D.HOST_NAME)
        tee_time_flow.verify_booking_summary(
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
        )
        tee_time_flow.go_back_to_booking_details()
        tee_time_flow.go_back_to_activity()

        generate_pdf(pdf)
    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_002"])
    def test_standard_booking_with_added_players(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home(D.SPORT_TYPE, D.REGION)
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.BOOKING_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

        settled = tee_time_flow.setup_players(
            PLAYERS,
            host_name=D.HOST_NAME,
            host_promo=D.EXPECTED_PROMO,
            promo_code=D.PROMO_CODE,
        )
        player_display_names = [D.HOST_NAME] + tee_time_flow.display_names(PLAYERS)
        assert list(settled) == player_display_names, \
            f"Players on the confirmation {list(settled)} != expected {player_display_names}"

        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)
        before = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.BOOKING_DATE,
            preferred_time=D.PREFERRED_TIME,
            player_names=player_display_names,
            total_players=len(player_display_names),
        )
        confirmed = tee_time_flow.pay_and_get_confirmed_booking(
            before,
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
            no_of_players=len(player_display_names),
            payment_method=D.PAYMENT_METHOD,
        )

        tee_time_flow.open_confirmed_booking_details()
        tee_time_flow.compare_payment_success_with_booking_details(confirmed)
        tee_time_flow.open_complete_breakdown()
        for name in player_display_names:
            tee_time_flow.verify_player_in_summary(name)
        tee_time_flow.verify_booking_summary(
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
        )
        tee_time_flow.go_back_to_booking_details()
        tee_time_flow.go_back_to_activity()

        generate_pdf(pdf)
    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression_pdf
    @pytest.mark.parametrize("TC_ID", ["TT_003"])
    def test_standard_booking_with_added_players_host_pays_with_swing_credits(
        self, TC_ID, login_flow, tee_time_flow
    ):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home(D.SPORT_TYPE, D.REGION)
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.BOOKING_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

        settled = tee_time_flow.setup_players(
            PLAYERS,
            host_name=D.HOST_NAME,
            host_promo=D.EXPECTED_PROMO,
            promo_code=D.PROMO_CODE,
            used_credit = "used"
        )
        player_display_names = [D.HOST_NAME] + tee_time_flow.display_names(PLAYERS)
        assert list(settled) == player_display_names, \
            f"Players on the confirmation {list(settled)} != expected {player_display_names}"

        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)
        # tee_time_flow.use_swing_credits()
        before = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.BOOKING_DATE,
            preferred_time=D.PREFERRED_TIME,
            player_names=player_display_names,
            total_players=len(player_display_names),
        )
        confirmed = tee_time_flow.pay_and_get_confirmed_booking(
            before,
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
            no_of_players=len(player_display_names),
            payment_method=D.PAYMENT_METHOD,
        )

        tee_time_flow.open_confirmed_booking_details()
        tee_time_flow.compare_payment_success_with_booking_details(confirmed)
        tee_time_flow.open_complete_breakdown()
        for name in player_display_names:
            tee_time_flow.verify_player_in_summary(name)
        tee_time_flow.verify_booking_summary(
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
        )
        tee_time_flow.go_back_to_booking_details()
        tee_time_flow.go_back_to_activity()

        booking_id = confirmed["Booking"]
        credit_entry = tee_time_flow.check_used_credit(booking_id)
        assert credit_entry, \
            f"Booking #{booking_id} is not listed under Credits Usage"

        generate_pdf(pdf)
    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_004"])
    def test_verify_golf_course_details(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home(D.SPORT_TYPE, D.REGION)
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.verify_course_details()

        generate_pdf(pdf)
    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_005"])
    def test_verify_featured_promo_on_golf_course_details(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home(D.SPORT_TYPE, D.REGION)
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        promos = tee_time_flow.verify_featured_promo()
        assert promos, "Featured promos screen listed no promo"

        generate_pdf(pdf)
    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_006"])
    def test_standard_booking_keep_auto_applied_promo(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home(D.SPORT_TYPE, D.REGION)
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.BOOKING_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

        player_display_names = [D.HOST_NAME]
        kept = tee_time_flow.keep_auto_applied_promo(player_display_names)
        if D.EXPECTED_PROMO:
            assert D.EXPECTED_PROMO in kept[D.HOST_NAME], \
                f"Auto-applied promo is '{kept[D.HOST_NAME]}', expected '{D.EXPECTED_PROMO}'"

        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)
        before = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.BOOKING_DATE,
            preferred_time=D.PREFERRED_TIME,
            player_names=player_display_names,
            total_players=len(player_display_names),
        )
        confirmed = tee_time_flow.pay_and_get_confirmed_booking(
            before,
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
            no_of_players=len(player_display_names),
            payment_method=D.PAYMENT_METHOD,
        )

        tee_time_flow.open_confirmed_booking_details()
        tee_time_flow.compare_payment_success_with_booking_details(confirmed)
        tee_time_flow.go_back_to_activity()

        generate_pdf(pdf)

    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["TT_007"])
    def test_standard_booking_change_promo(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        if not D.PROMO_NAME:
            pytest.skip(f"{TC_ID}: fill PROMO_NAME in the Tee_Time sheet with the promo to switch to")
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home(D.SPORT_TYPE, D.REGION)
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.BOOKING_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

        player_display_names = [D.HOST_NAME]
        tee_time_flow.change_promo(D.HOST_NAME, D.PROMO_NAME)
        tee_time_flow.verify_promo_applied(D.HOST_NAME, D.PROMO_NAME)

        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)
        before = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.BOOKING_DATE,
            preferred_time=D.PREFERRED_TIME,
            player_names=player_display_names,
            total_players=len(player_display_names),
        )
        confirmed = tee_time_flow.pay_and_get_confirmed_booking(
            before,
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
            no_of_players=len(player_display_names),
            payment_method=D.PAYMENT_METHOD,
        )

        tee_time_flow.open_confirmed_booking_details()
        tee_time_flow.compare_payment_success_with_booking_details(confirmed)
        tee_time_flow.go_back_to_activity()

        generate_pdf(pdf)

    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["TT_008"])
    def test_standard_booking_redeem_promo_code(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        if not (D.PROMO_NAME and D.PROMO_CODE):
            pytest.skip(f"{TC_ID}: fill PROMO_NAME and PROMO_CODE in the Tee_Time sheet")
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home(D.SPORT_TYPE, D.REGION)
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.BOOKING_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

        player_display_names = [D.HOST_NAME]
        applied = tee_time_flow.redeem_promo(player_display_names, D.PROMO_NAME, D.PROMO_CODE)
        assert D.PROMO_NAME in applied[D.HOST_NAME], \
            f"Promo on the host is '{applied[D.HOST_NAME]}', expected '{D.PROMO_NAME}'"

        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)
        before = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.BOOKING_DATE,
            preferred_time=D.PREFERRED_TIME,
            player_names=player_display_names,
            total_players=len(player_display_names),
        )
        confirmed = tee_time_flow.pay_and_get_confirmed_booking(
            before,
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
            no_of_players=len(player_display_names),
            payment_method=D.PAYMENT_METHOD,
        )

        tee_time_flow.open_confirmed_booking_details()
        tee_time_flow.compare_payment_success_with_booking_details(confirmed)
        tee_time_flow.go_back_to_activity()

        generate_pdf(pdf)
    @pytest.mark.app_state("force-stop")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_009"])
    def test_standard_booking_with_added_players_and_add_ons(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home(D.SPORT_TYPE, D.REGION)
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.BOOKING_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

        settled = tee_time_flow.setup_players(
            PLAYERS,
            ADD_ONS,
            host_name=D.HOST_NAME,
            host_promo=D.EXPECTED_PROMO,
            promo_code=D.PROMO_CODE,
        )
        player_display_names = [D.HOST_NAME] + tee_time_flow.display_names(PLAYERS)
        assert list(settled) == player_display_names, \
            f"Players on the confirmation {list(settled)} != expected {player_display_names}"

        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)
        before = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.BOOKING_DATE,
            preferred_time=D.PREFERRED_TIME,
            player_names=player_display_names,
            total_players=len(player_display_names),
        )
        confirmed = tee_time_flow.pay_and_get_confirmed_booking(
            before,
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
            no_of_players=len(player_display_names),
            payment_method=D.PAYMENT_METHOD,
        )

        tee_time_flow.open_confirmed_booking_details()
        tee_time_flow.compare_payment_success_with_booking_details(confirmed)
        tee_time_flow.open_complete_breakdown()
        for name in player_display_names:
            tee_time_flow.verify_player_in_summary(name)
        tee_time_flow.verify_booking_summary(
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
        )
        tee_time_flow.go_back_to_booking_details()
        tee_time_flow.go_back_to_activity()

        generate_pdf(pdf)
