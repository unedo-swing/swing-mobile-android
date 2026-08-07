"""
Android XPaths for the Swing Tee Time > Booking confirmed ("You're confirmed!")
screen.

Shown after a successful payment on the booking confirmation screen. Flutter app
— values surface through ``content-desc``. Unlike the pre-payment confirmation
screen (where a summary row is one "Label\\nvalue" node), here each label and its
value are SEPARATE sibling ``View`` nodes, so a value is read via its label's
following-sibling. The following-sibling axis targets ``android.view.View``
explicitly, so a non-View sibling (e.g. the payment-method icon) is skipped.
"""


class BookingConfirmedLocators:
    # --- success header ---
    # NOTE: curly apostrophe (U+2019) in "You're confirmed!" — matched exactly.
    label_title = '//android.view.View[@content-desc="You’re confirmed!"]'
    label_subtitle = '//android.view.View[@content-desc="See you on the golf course"]'

    # --- booking identity ---
    # course name varies: label_course_name % "Rainbow Hills Golf"
    label_course_name = '//android.view.View[@content-desc="%s"]'
    label_booking_id = '//android.view.View[starts-with(@content-desc,"Booking #")]'

    # --- summary rows: value = the View right after the label View ---
    value_date = '//android.view.View[@content-desc="Date"]/following-sibling::android.view.View[1]'
    value_session = '//android.view.View[@content-desc="Session"]/following-sibling::android.view.View[1]'
    value_preferred_time = '//android.view.View[@content-desc="Preferred tee time"]/following-sibling::android.view.View[1]'
    value_no_of_players = '//android.view.View[@content-desc="No. of players"]/following-sibling::android.view.View[1]'
    value_total = '//android.view.View[@content-desc="Total"]/following-sibling::android.view.View[1]'
    value_payment_method = '//android.view.View[@content-desc="Payment method"]/following-sibling::android.view.View[1]'

    # --- swing credits earned ---
    label_credits_title = '//android.view.View[@content-desc="Swing Credits you earned"]'
    value_credits_earned = '//android.view.View[starts-with(@content-desc,"+ ")]'
    label_credits_note = '//android.view.View[contains(@content-desc,"Swing Credits will only be issued")]'

    # --- footer buttons ---
    button_finish = '//android.widget.Button[@content-desc="Finish"]'
    button_see_booking_details = '//android.widget.Button[@content-desc="See booking details"]'
