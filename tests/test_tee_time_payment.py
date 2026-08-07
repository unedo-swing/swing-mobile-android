import pytest

from data.tee_time_data import TeeTimeData as D


@pytest.mark.android
class TestTeeTimePayment:
    """Tee time -> select payment method, with and without a promo."""

    @pytest.mark.skip
    @pytest.mark.parametrize(
        "TC_ID, use_promo",
        [("TT_002", True), ("TT_003", False)],
        ids=["with_promo", "without_promo"],
    )
    def test_select_payment(self, login_flow, tee_time_flow, TC_ID, use_promo):
        # load this test case's scenario data from the Tee_Time sheet
        D.load(TC_ID)

        # user already logged in
        login_flow.verify_home()

        # home -> tee time -> course -> date -> time -> standard booking
        tee_time_flow.select_region(D.REGION)
        tee_time_flow.open_tee_time()
        tee_time_flow.search_and_open_course(D.COURSE_NAME)
        tee_time_flow.pick_date_from_calendar(D.COURSE_NAME, D.CALENDAR_DATE)
        tee_time_flow.select_preferred_time(D.PREFERRED_TIME)
        tee_time_flow.start_standard_booking()

        # promo for the host: apply one, or remove the auto-applied one
        if use_promo:
            tee_time_flow.change_promo(D.HOST_NAME, D.PROMO_NAME)
        else:
            tee_time_flow.remove_promo(D.HOST_NAME)

        # select payment method
        tee_time_flow.change_payment_card(D.PAYMENT_CARD)
