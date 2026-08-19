import pytest

from data.tee_time_data import TeeTimeData as D, load_players
from utils.pdf_reporter import init_pdf, generate_pdf


@pytest.mark.android
class TestTeeTimeBooking:

    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_001"])
    def test_book_tee_time_standard_with_auto_applied_promo(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()
        tee_time_flow.verify_auto_applied_promo(D.HOST_NAME)
        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)

        player_display_names = [D.HOST_NAME]
        summary = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.CALENDAR_DATE,
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
    
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_005"])
    def test_book_tee_time_standard_with_change_promo(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()
        tee_time_flow.verify_auto_applied_promo(D.HOST_NAME)
        tee_time_flow.change_promo(D.HOST_NAME, D.PROMO_NAME)
        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)

        player_display_names = [D.HOST_NAME]
        summary = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.CALENDAR_DATE,
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
    
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_006"])
    def test_book_tee_time_standard_with_add_promo(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()
        tee_time_flow.verify_auto_applied_promo(D.HOST_NAME)
        tee_time_flow.change_promo_with_add_promo_code(D.HOST_NAME, D.PROMO_NAME, D.PROMO_CODE)
        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)

        player_display_names = [D.HOST_NAME]
        summary = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.CALENDAR_DATE,
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
    
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_007"])
    def test_book_tee_time_standard_1_player(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()
        tee_time_flow.verify_auto_applied_promo(D.HOST_NAME)
        tee_time_flow.change_promo(D.HOST_NAME, D.PROMO_NAME)
        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)

        player_display_names = [D.HOST_NAME]
        summary = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.CALENDAR_DATE,
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

    # --- add player scenarios -------------------------------------------------
    # Players come from the Tee_Time_Player sheet via load_players(TC_ID); the
    # flow's add_players() loops them, keeps the booking standard when the
    # "switch to group" prompt appears, verifies each name landed on the
    # confirmation, and applies (or removes) that player's promo.

    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_008"])
    def test_book_tee_time_add_1_player_manually(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        players = load_players(TC_ID)          # TT_008 -> one manual player
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

        tee_time_flow.add_players(players)
        tee_time_flow.verify_auto_applied_promo(D.HOST_NAME)
        tee_time_flow.change_promo(D.HOST_NAME, D.PROMO_NAME)
        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)

        player_display_names = [D.HOST_NAME] + tee_time_flow.display_names(players)
        summary = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.CALENDAR_DATE,
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
            no_of_players=len(player_display_names),
        )
        tee_time_flow.open_complete_breakdown()
        tee_time_flow.verify_booking_summary(
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
        )
        for name in player_display_names:
            tee_time_flow.verify_player_in_summary(name)
        tee_time_flow.go_back_to_booking_details()
        tee_time_flow.go_back_to_activity()

        generate_pdf(pdf)

    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_009"])
    def test_book_tee_time_add_1_player_by_search(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        # TT_003's sheet row is a manual player, so the friend to search comes
        # from the data class. Move it to the sheet (METHOD=search) if you want
        # this driven by Excel like the others.
        players = load_players(TC_ID)          # TT_009 -> one searched friend
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

        tee_time_flow.add_players(players)
        # TT_003 carries no promo — drop whatever was auto-applied to the host
        tee_time_flow.remove_promo(D.HOST_NAME)
        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)

        player_display_names = [D.HOST_NAME] + tee_time_flow.display_names(players)
        summary = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.CALENDAR_DATE,
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
            no_of_players=len(player_display_names),
        )
        tee_time_flow.open_complete_breakdown()
        tee_time_flow.verify_booking_summary(
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
        )
        for name in player_display_names:
            tee_time_flow.verify_player_in_summary(name)
        tee_time_flow.go_back_to_booking_details()
        tee_time_flow.go_back_to_activity()

        generate_pdf(pdf)

    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_010"])
    def test_book_tee_time_add_2_players_manual_and_search(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        # TT_010 -> Andi Wijaya (manual) + Tam Lembong (search)
        players = load_players(TC_ID)
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

        tee_time_flow.add_players(players)
        tee_time_flow.verify_auto_applied_promo(D.HOST_NAME)
        tee_time_flow.change_promo(D.HOST_NAME, D.PROMO_NAME)
        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)

        player_display_names = [D.HOST_NAME] + tee_time_flow.display_names(players)
        summary = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.CALENDAR_DATE,
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
            no_of_players=len(player_display_names),
        )
        tee_time_flow.open_complete_breakdown()
        tee_time_flow.verify_booking_summary(
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
        )
        for name in player_display_names:
            tee_time_flow.verify_player_in_summary(name)
        tee_time_flow.go_back_to_booking_details()
        tee_time_flow.go_back_to_activity()

        generate_pdf(pdf)

    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_004"])
    def test_book_tee_time_add_3_players_manual_and_search(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        # TT_004 -> Andi Wijaya (manual), Tam Lembong (search), Eka Kurniawan
        # (manual): a full flight of 4 with the host.
        players = load_players(TC_ID)
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

        tee_time_flow.add_players(players)
        tee_time_flow.verify_auto_applied_promo(D.HOST_NAME)
        tee_time_flow.change_promo(D.HOST_NAME, D.PROMO_NAME)
        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)

        player_display_names = [D.HOST_NAME] + tee_time_flow.display_names(players)
        summary = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.CALENDAR_DATE,
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
            no_of_players=len(player_display_names),
        )
        tee_time_flow.open_complete_breakdown()
        tee_time_flow.verify_booking_summary(
            course_name=D.COURSE_NAME,
            preferred_time=D.PREFERRED_TIME,
        )
        for name in player_display_names:
            tee_time_flow.verify_player_in_summary(name)
        tee_time_flow.go_back_to_booking_details()
        tee_time_flow.go_back_to_activity()

        generate_pdf(pdf)

    # --- add player + promo scenarios ----------------------------------------
    # These stop at the booking confirmation instead of paying: what they check
    # is the promo behaviour around adding a player. Append pay_now() and the
    # confirmed-booking block if you want them end to end.

    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_011"])
    def test_add_player_manually_then_change_promo(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        player = load_players(TC_ID)[0]        # TT_011 -> Citra Dewi (manual)
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()
        tee_time_flow.verify_auto_applied_promo(D.HOST_NAME)

        # add the player -> the card is on the confirmation
        player_name = tee_time_flow.add_player(player)

        # the new player gets a promo of their own, then we swap it
        tee_time_flow.verify_auto_applied_promo(player_name)
        tee_time_flow.change_promo(player_name, D.PROMO_NAME)
        tee_time_flow.verify_promo_applied(player_name, D.PROMO_NAME)

        # the host keeps its promo through all of that
        tee_time_flow.verify_promo_applied(D.HOST_NAME, D.PROMO_NAME)

        player_display_names = [D.HOST_NAME, player_name]
        tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.CALENDAR_DATE,
            preferred_time=D.PREFERRED_TIME,
            player_names=player_display_names,
            total_players=len(player_display_names),
        )
        generate_pdf(pdf)

    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_012"])
    def test_add_player_by_search_then_remove_promo(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        player = load_players(TC_ID)[0]        # TT_012 -> Tam Lembong (search)
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

        # add the friend by search -> the card is on the confirmation
        player_name = tee_time_flow.add_player(player)

        # a promo lands on the new player, then we take it off again
        tee_time_flow.verify_auto_applied_promo(player_name)
        tee_time_flow.remove_promo(player_name)
        tee_time_flow.verify_promo_removed(player_name)

        # TT_012 is the "without promo" case — clear the host's too
        tee_time_flow.remove_promo(D.HOST_NAME)
        tee_time_flow.verify_promo_removed(D.HOST_NAME)

        player_display_names = [D.HOST_NAME, player_name]
        tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.CALENDAR_DATE,
            preferred_time=D.PREFERRED_TIME,
            player_names=player_display_names,
            total_players=len(player_display_names),
        )
        generate_pdf(pdf)

    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_013"])
    def test_add_2_players_change_promo_on_one_remove_on_other(self, TC_ID, login_flow, tee_time_flow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID, tc_name=D.TC_NAME)
        # TT_013 -> Andi Wijaya (manual) + Tam Lembong (search)
        first_player, second_player = load_players(TC_ID)
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()
        tee_time_flow.verify_auto_applied_promo(D.HOST_NAME)

        # player 1 (manual) keeps a promo — the auto-applied one is swapped
        first_name = tee_time_flow.add_player(first_player)
        tee_time_flow.verify_auto_applied_promo(first_name)
        tee_time_flow.change_promo(first_name, D.PROMO_NAME)
        tee_time_flow.verify_promo_applied(first_name, D.PROMO_NAME)

        # player 2 (search) goes without — the auto-applied one is removed
        second_name = tee_time_flow.add_player(second_player)
        tee_time_flow.verify_auto_applied_promo(second_name)
        tee_time_flow.remove_promo(second_name)
        tee_time_flow.verify_promo_removed(second_name)

        # adding the second player left the first one's promo alone
        tee_time_flow.verify_promo_applied(first_name, D.PROMO_NAME)
        tee_time_flow.verify_promo_applied(D.HOST_NAME, D.PROMO_NAME)

        player_display_names = [D.HOST_NAME, first_name, second_name]
        tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.CALENDAR_DATE,
            preferred_time=D.PREFERRED_TIME,
            player_names=player_display_names,
            total_players=len(player_display_names),
        )
        generate_pdf(pdf)
