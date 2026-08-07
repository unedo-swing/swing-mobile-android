"""
Android XPaths for the Swing Tee Time > Receipt screen.

Opened from "See receipt" on the Booking details screen. Flutter app — values
surface through ``content-desc``. Layout mirrors the "You're confirmed!" screen
(label and value are SEPARATE sibling ``View`` nodes, value read via the label's
following-sibling), plus a support section and a "Send receipt" footer button
instead of Finish / See booking details.
"""


class ReceiptLocators:
    # --- header ---
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    # header content-desc carries the receipt id, e.g. "Receipt #MU6NP"
    label_title = '//android.view.View[starts-with(@content-desc,"Receipt #") and @heading="true"]'

    # --- booking identity ---
    # course name varies: label_course_name % "Rainbow Hills Golf"
    label_course_name = '//android.view.View[@content-desc="%s"]'
    label_booking_id = '//android.view.View[starts-with(@content-desc,"Booking #")]'

    # --- summary rows: value = the View right after the label View ---
    value_date = '//android.view.View[@content-desc="Date"]/following-sibling::android.view.View[1]'
    value_session = '//android.view.View[@content-desc="Session"]/following-sibling::android.view.View[1]'
    value_preferred_time = '//android.view.View[@content-desc="Preferred time"]/following-sibling::android.view.View[1]'
    value_no_of_players = '//android.view.View[@content-desc="No. of players"]/following-sibling::android.view.View[1]'
    value_total = '//android.view.View[@content-desc="Total"]/following-sibling::android.view.View[1]'
    value_payment_method = '//android.view.View[@content-desc="Payment method"]/following-sibling::android.view.View[1]'

    # --- swing credits earned ---
    label_credits_title = '//android.view.View[@content-desc="Swing Credits you earned"]'
    value_credits_earned = '//android.view.View[@content-desc="Swing Credits you earned"]/following-sibling::android.view.View[1]'
    label_credits_note = '//android.view.View[contains(@content-desc,"Swing Credits will only be issued")]'

    # --- support ---
    label_help_title = '//android.view.View[@content-desc="Need a helping hand?"]'
    button_contact_support = '//android.view.View[@content-desc="Contact Swing support"]'

    # --- footer ---
    button_send_receipt = '//android.widget.Button[@content-desc="Send receipt"]'
