"""
Android XPaths for the Swing Driving Range > Booking confirmation screen.

Opened after confirming the number of bays. Flutter app — elements surface
through ``content-desc`` / ``hint``. The promo picker and payment-method sheet
are the SAME screens as tee time, so their pages are reused
(pages/tee_time/promo_page.py, pages/tee_time/payment_method_page.py).
"""


class DrivingRangeBookingConfirmationLocators:
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    label_title = '//android.view.View[@content-desc="Booking confirmation"]'
    label_range_name = '//android.view.View[@content-desc="%s"]'

    # --- booking summary (content-desc is "<Label>\n<value>") ---
    label_player_name = '//android.view.View[starts-with(@content-desc,"Player name")]'
    label_date = '//android.view.View[starts-with(@content-desc,"Date")]'
    label_booking_time = '//android.view.View[starts-with(@content-desc,"Booking time")]'
    label_duration = '//android.view.View[starts-with(@content-desc,"Duration")]'
    label_number_of_bays = '//android.view.View[starts-with(@content-desc,"Number of bays")]'
    label_bay_type = '//android.view.View[starts-with(@content-desc,"Bay Type")]'

    # --- rentals / add-ons ("<Name>\nRp. <price> per item\n<count>") ---
    label_addons = '//android.view.View[@content-desc="Any rentals or add-ons?"]'
    addon_row_by_name = '//android.view.View[starts-with(@content-desc,"%s")]'
    addon_minus_by_name = '//android.view.View[starts-with(@content-desc,"%s")]/android.widget.ImageView[1]'
    addon_plus_by_name = '//android.view.View[starts-with(@content-desc,"%s")]/android.widget.ImageView[2]'

    # --- notes ---
    input_notes = '//android.widget.EditText'

    # --- reschedule & cancellation policy ---
    label_policy = '//android.view.View[contains(@content-desc,"Reschedule & cancellation policy")]'
    tab_reschedule = '//android.view.View[@content-desc="Reschedule"]'
    tab_cancellation = '//android.view.View[@content-desc="Cancellation"]'
    link_learn_more = '//android.widget.ImageView[@content-desc="Learn more"]'
    link_terms = '//android.view.View[@content-desc="Terms & Conditions"]'

    # --- price details (time-based) ---
    label_price_details = '//android.view.View[contains(@content-desc,"Price details")]'
    label_processing_fee = '//android.view.View[starts-with(@content-desc,"Processing fee")]'
    label_total_payment = '//android.view.View[starts-with(@content-desc,"Total payment")]'

    # --- promo (single, auto-applied for the booking) ---
    button_change_promo = '(//android.view.View[starts-with(@content-desc,"Total payment")]/ancestor::*/following-sibling::android.view.View)[1]'

    # --- swing credits ---
    switch_swing_credits = '//android.widget.Switch[contains(@content-desc,"Swing Credits")]'
    button_redeem_swing_credits = '//android.widget.ImageView[@content-desc="Redeem Swing Credits"]'

    # --- payment method ---
    label_payment_method = '//android.widget.Button[@content-desc="Select payment" or @content-desc="Change"]/parent::android.widget.ImageView'
    button_select_payment = '//android.widget.Button[@content-desc="Select payment" or @content-desc="Change"] '
    # button_change_payment = '//android.widget.Button[@content-desc="Select payment" or @content-desc="Change"]/parent::android.widget.ImageView'

    # --- bottom bar ---
    label_credits_earned = '//android.view.View[starts-with(@content-desc,"+ ")]'
    button_pay_now = '//android.widget.ImageView[@content-desc="Pay now"]'
