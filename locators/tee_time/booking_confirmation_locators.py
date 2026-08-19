class BookingConfirmationLocators:
    # --- header ---
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    label_title = '//android.view.View[@content-desc="Booking confirmation"]'
    # course name varies: label_course_name % '"Rainbow Hills Golf"'
    label_course_name = '//android.view.View[@content-desc="%s"]'

    # --- booking summary (content-desc is "<Label>\n<value>") ---
    label_date = '//android.view.View[starts-with(@content-desc,"Date")]'
    label_session = '//android.view.View[starts-with(@content-desc,"Session")]'
    label_preferred_time = '//android.view.View[starts-with(@content-desc,"Preferred Time")]'
    label_booking_type = '//android.view.View[@content-desc="Standard Booking" or @content-desc="Group Booking"]'

    # --- players list ---
    # player card carries "<Name> (Host)\n<tier>\nRp. <amount>" (or without Host).
    # First match in doc order is the players-list card (not the price line).
    player_card_by_name = '//android.widget.ImageView[contains(@content-desc,"%s")]'
    # every player card (host + invitees), used to count total players. Matches
    # any "Rp." ImageView that appears BEFORE "Price details" in doc order, so
    # the per-player Price-details rows (also "Rp.", but after that label)
    # aren't double-counted.
    all_player_cards = '//android.view.View[@content-desc="Price details"]/following-sibling::android.view.View//android.widget.ImageView'
    button_add_promo = '//android.widget.ImageView[contains(@content-desc,"%s")]/following-sibling::android.view.View[1]'
    button_add_add_ons = '//android.widget.ImageView[contains(@content-desc,"%s")]/following-sibling::android.view.View[2]'
    button_add_player = '//android.widget.ImageView[@content-desc="Add a player"]'
    button_change_player = '//android.widget.ImageView[@content-desc="Change player"]'
    button_remove_player = '//android.widget.ImageView[@content-desc="Remove player"]'

    # --- swing credits / add-ons / notes ---
    switch_swing_credits = '//android.widget.Switch[contains(@content-desc,"Swing Credits")]'
    button_redeem_swing_credits = '//android.widget.ImageView[@content-desc="Redeem Swing Credits"]'
    row_addons = '//android.view.View[contains(@content-desc,"add-ons")]'
    input_notes = '//android.widget.EditText'

    # --- terms ---
    link_terms = '//android.view.View[@content-desc="Terms & conditions"]'

    # --- price details ---
    label_price_details = '//android.view.View[@content-desc="Price details"]'
    label_processing_fee = '//android.view.View[starts-with(@content-desc,"Processing fee")]'
    label_total_payment = '//android.view.View[starts-with(@content-desc,"Total payment")]'
    # per-player breakdown line in Price details (has "Publish Rate"):
    #   price_line_by_name % '"QA Auto Mation"'
    price_line_by_name = '//android.widget.ImageView[contains(@content-desc,"%s") and contains(@content-desc,"Publish Rate")]'

    # --- payment method ---
    # before a method is picked:
    label_payment_method = '//android.view.View[contains(@content-desc,"payment selected")]'
    button_select_payment = '//android.widget.Button[@content-desc="Select payment" or @content-desc="Change"] '
    # after a method is picked, the row shows the method name (e.g. "OVO") and a
    # "Change" button:
    label_selected_payment = '//android.widget.ImageView[.//android.widget.Button[@content-desc="Change"]]'
    button_change_payment = '//android.widget.Button[@content-desc="Change"]'

    # --- bottom bar ---
    # Swing Credits earned (tap to open the "Swing Credits earnings" dialog):
    label_credits_earned = '//android.view.View[starts-with(@content-desc,"+ ")]'
    button_pay_now = '//android.widget.ImageView[@content-desc="Pay now"]'
