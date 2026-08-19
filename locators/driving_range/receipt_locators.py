class DrivingRangeReceiptLocators:
    # ================= header =================
    label_title = '//android.view.View[contains(@content-desc,"Receipt #")]'
    button_back = '//android.view.View[contains(@content-desc,"Receipt #")]/preceding-sibling::android.widget.ImageView[1]'

    # ================= summary =================
    label_range_name = '//android.view.View[@content-desc="%s"]'
    label_booking_id = '//android.view.View[contains(@content-desc,"Booking #")]'

    # a value read from its label's sibling: value_by_label % "Date".
    # following-sibling::View[1] skips any icon (ImageView) between label and value,
    # e.g. the payment-method logo before "OVO".
    value_by_label = '//android.view.View[@content-desc="%s"]/following-sibling::android.view.View[1]'

    label_credits_earned = '//android.view.View[@content-desc="Swing Credits you earned"]'

    # ================= support =================
    label_support_prompt = '//android.view.View[@content-desc="Need a helping hand?"]'
    button_contact_support = '//android.view.View[@content-desc="Contact Swing support"]'

    # ================= send receipt =================
    button_send_receipt = '//android.widget.Button[@content-desc="Send receipt"]'
    # cooldown banner shown after sending, e.g.
    # "You can send the receipt again in 00:47\nReceipts can only be sent once every 1 minute."
    label_send_cooldown = '//*[contains(@content-desc,"send the receipt again")]'
