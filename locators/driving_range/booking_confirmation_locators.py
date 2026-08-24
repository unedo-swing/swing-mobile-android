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

    # --- rentals / add-ons ("<Name>\nRp. <price>\n<count>", e.g. "10 balls\nRp. 10,000\n1").
    # Ball-based ranges show the same stepper rows under "How many balls?" instead, and a
    # BXGY promo inserts a bonus line: "100 balls\nRp. 75,000\n+ 100 balls\n2".
    # The stepper row is pinned by its +/- children so it cannot match the price-details
    # row further down the screen, which starts with the same name. ---
    label_addons = '//android.view.View[@content-desc="Any rentals or add-ons?"]'
    label_balls = '//android.view.View[@content-desc="How many balls?"]'
    addon_row_by_name = '//android.view.View[starts-with(@content-desc,"%s") and android.widget.ImageView]'
    addon_minus_by_name = addon_row_by_name + '/android.widget.ImageView[1]'
    addon_plus_by_name = addon_row_by_name + '/android.widget.ImageView[2]'

    # --- notes ---
    input_notes = '//android.widget.EditText'

    # --- reschedule & cancellation policy ---
    label_policy = '//android.view.View[contains(@content-desc,"Reschedule & cancellation policy")]'
    tab_reschedule = '//android.view.View[@content-desc="Reschedule"]'
    tab_cancellation = '//android.view.View[@content-desc="Cancellation"]'
    link_learn_more = '//android.widget.ImageView[@content-desc="Learn more"]'
    link_terms = '//android.view.View[@content-desc="Terms & Conditions"]'

    # --- price details, header reads "Price details (Time-based)" or "(Ball-based)" ---
    label_price_details = '//android.view.View[contains(@content-desc,"Price details")]'
    # breakdown rows carry no children, e.g. "100 balls x2\n+ 100 balls (max)\nRp. 150,000"
    price_row_by_name = '//android.view.View[starts-with(@content-desc,"%s") and not(*)]'
    label_processing_fee = '//android.view.View[starts-with(@content-desc,"Processing fee")]'
    label_total_payment = '//android.view.View[starts-with(@content-desc,"Total payment")]'
    # the applied promo also appears as a discount row inside the breakdown
    price_row_promo_by_name = '//android.view.View[@content-desc="%s" and not(*) and not(@clickable="true")]'

    # --- promo (single, auto-applied for the booking).
    # The promo card is the only clickable row in the scroll view with a leading icon and
    # a trailing chevron; it reads the promo name, or "Apply a promo" when none is set. ---
    button_change_promo = '//android.view.View[contains(@content-desc,"Price details")]/following-sibling::android.view.View[2]'

    # --- swing credits ---
    # once the toggle is on, the redeemed amount joins the price breakdown
    # as "Swing Credits\n- 75,000"
    label_swing_credits_used = '//android.view.View[starts-with(@content-desc,"Swing Credits")]'
    switch_swing_credits = '//android.widget.Switch[contains(@content-desc,"Swing Credits")]'
    button_redeem_swing_credits = '//android.widget.ImageView[@content-desc="Redeem Swing Credits"]'

    # --- payment method ---
    label_payment_method = '//android.widget.Button[@content-desc="Select payment" or @content-desc="Change"]/parent::android.widget.ImageView'
    button_select_payment = '//android.widget.Button[@content-desc="Select payment" or @content-desc="Change"] '
    # button_change_payment = '//android.widget.Button[@content-desc="Select payment" or @content-desc="Change"]/parent::android.widget.ImageView'

    # --- bottom bar ---
    label_credits_earned = '//android.view.View[starts-with(@content-desc,"+ ")]'
    button_pay_now = '//android.widget.ImageView[@content-desc="Pay now"]'
    
    toaster_minimum_balls = ('//android.widget.ImageView[contains(@content-desc,"Minimum") and contains(@content-desc,"for booking with")]')
    button_proceed_to_pay = '//android.widget.Button[@resource-id="proceed-button"]'
    label_verification_required = '//android.view.View[@content-desc="Verification required"]'
    label_pending_approval = '//android.view.View[@content-desc="Pending approval"]'
    