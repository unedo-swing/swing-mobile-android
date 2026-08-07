import pytest

from data.tee_time_data import TeeTimeData as D, load_players


@pytest.mark.android
class TestTeeTime:

    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["TT_001"])
    def test_book_standard_tee_time_full(self, TC_ID, login_flow, tee_time_flow, reporter):
        # load this test case's scenario data from the Tee_Time sheet
        D.load(TC_ID)
        # put the real TC ID / TC Name (from the sheet) on the PDF's cover page
        if reporter is not None:
            reporter.set_test_case(TC_ID, D.TC_NAME)

        # home -> tee time -> search course -> verify golf course details
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)

        # choose date -> preferred time -> standard booking
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

        # host promo: check the auto-applied promo, then change it
        # (use tee_time_flow.remove_promo(D.HOST_NAME) instead to drop it)
        tee_time_flow.verify_auto_applied_promo(D.HOST_NAME)
        tee_time_flow.change_promo(D.HOST_NAME, D.PROMO_NAME)

        # add the 3 invitee players from the Tee_Time_Player sheet (by TC_ID),
        # looped + verified per player (promo per player handled inside)
        players = load_players(TC_ID)
        tee_time_flow.add_players(players)

        # change payment method (e-wallet, e.g. Gopay)
        tee_time_flow.change_payment_method(D.PAYMENT_METHOD)

        # capture/verify everything on the booking confirmation before paying:
        # venue, date/time, total players, total payment, per-player payment,
        # and Swing Credits earned (if any)
        player_display_names = [D.HOST_NAME] + [
            p.get("name") or f'{p["first_name"]} {p["last_name"]}' for p in players
        ]
        summary = tee_time_flow.verify_before_payment(
            venue_name=D.COURSE_NAME,
            date=D.CALENDAR_DATE,
            preferred_time=D.PREFERRED_TIME,
            player_names=player_display_names,
            total_players=len(player_display_names),
        )
        print(f"Before payment summary: {summary}")

        tee_time_flow.pay_now()

        # verify the "You're confirmed!" success screen
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

    @pytest.mark.skip
    def test_book_standard_tee_time(self, login_flow, tee_time_flow):
        login_flow.verify_home()
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

    @pytest.mark.skip
    def test_book_tee_time_with_players_and_payment(self, login_flow, tee_time_flow):
        # user already logged in -> just verify home
        login_flow.verify_home()

        # home -> tee time -> search course -> details
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)

        # date (via calendar) + preferred time
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)

        # book -> standard booking
        tee_time_flow.start_standard_booking()

        #add players 1-3 (mix of manual + search)
        tee_time_flow.add_player_manually(
            D.PLAYER_FIRST_NAME, D.PLAYER_LAST_NAME, D.PLAYER_PHONE, D.PLAYER_EMAIL
        )
        tee_time_flow.search_and_add_player(D.PLAYER_FRIEND_NAME)
        tee_time_flow.verify_player_added(D.PLAYER_FRIEND_NAME)  # verify after search
        # tee_time_flow.add_player_manually(
        #     D.PLAYER3_FIRST_NAME, D.PLAYER3_LAST_NAME, D.PLAYER3_PHONE, D.PLAYER3_EMAIL
        # )

        # select payment method
        tee_time_flow.change_payment_card(D.PAYMENT_CARD)
