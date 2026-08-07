class DrivingRangeBookingDetailsLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Booking details"]'
    button_back = '//android.view.View[@content-desc="Booking details"]/preceding-sibling::android.widget.ImageView[1]'
    button_three_dots = '//android.view.View[@content-desc="Booking details"]/following-sibling::android.widget.ImageView[1]'
    
    button_reschedule_booking = '//android.widget.ImageView[@content-desc="Reschedule booking"]'
    button_cancel_booking = '//android.widget.ImageView[@content-desc="Cancel booking"]'
    button_contact_swing_support = '//android.widget.ImageView[@content-desc="Contact Swing support"]'
    button_close_bottom_sheet = '//android.widget.Button'

    # ================= booking summary =================
    label_booking_summary = '//android.view.View[@content-desc="Booking summary"]'
    label_status = '//android.view.View[@content-desc="%s"]'          # e.g. "UPCOMING"
    label_booking_id = '//android.view.View[contains(@content-desc,"Booking #")]'

    # a summary value read from its label's sibling: value_by_label % "Date"
    value_by_label = '//android.view.View[@content-desc="%s"]/following-sibling::android.view.View[1]'

    button_see_breakdown = '//android.widget.Button[@content-desc="See complete breakdown"]'

    # ================= payment summary =================
    label_payment_summary = '//android.view.View[@content-desc="Payment summary"]'
    # a payment row by the label it starts with, e.g. "Subtotal", "Total payment".
    # Any class: the total row surfaces as an ImageView, others as Views.
    payment_row_by_label = '//*[starts-with(@content-desc,"%s")]'
    label_credits_earned = '//android.view.View[@content-desc="Swing Credits you earned"]'

    button_see_receipt = '//android.widget.Button[@content-desc="See receipt"]'

    # ================= reschedule summary (present when the booking was rescheduled) =================
    label_reschedule_summary = '//android.view.View[@content-desc="Reschedule summary"]'
    # original vs new date/time block (ImageView, "\n"-joined:
    # "Original date & time\n18:00, 13 Aug 2026\nNew date & time\n22:00, 5 Aug 2026")
    label_reschedule_change = '//*[starts-with(@content-desc,"Original date")]'
    label_reschedule_fee = '//android.view.View[@content-desc="Reschedule fee"]'
    label_price_difference = '//android.view.View[@content-desc="Price difference"]'
    # the reschedule summary's own action button
    button_reschedule_see_details = '//android.widget.Button[@content-desc="See details"]'

    # ================= history =================
    label_history = '//android.view.View[@content-desc="History"]'
    # a history entry by the status it starts with, e.g. "Booking confirmed"
    # (content-desc is "Booking confirmed\n11:32, 5 Aug 2026")
    history_item_by_status = '//*[starts-with(@content-desc,"%s")]'
