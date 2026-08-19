class DrivingRangeConfirmRescheduleLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Confirm reschedule"]'
    button_back = '//android.view.View[@content-desc="Confirm reschedule"]/preceding-sibling::android.widget.ImageView[1]'

    # ================= booking summary =================
    label_range_name = '//android.view.View[@content-desc="%s"]'
    # a value read from its label's sibling: value_by_label % "Duration"
    value_by_label = '//android.view.View[@content-desc="%s"]/following-sibling::android.view.View[1]'
    # "Booking ID" -> "#A38OO", "Request date & time" -> "13:53, 5 Aug 2026", etc.

    # original vs new date/time block (one View, "\n"-joined:
    # "Original date & time\n18:00, 13 August 2026\nNew date & time\n22:00, 05 Aug 2026")
    label_change_block = '//*[starts-with(@content-desc,"Original date")]'

    # ================= reschedule reason =================
    label_reschedule_reason = '//android.view.View[@content-desc="Reschedule reason"]'
    # a reason radio by its label, e.g. "Bad weather", "Traffic jam"
    reason_by_name = '//android.widget.RadioButton[@content-desc="%s"]'

    # ================= reschedule details =================
    label_reschedule_details = '//android.view.View[@content-desc="Reschedule details"]'
    label_reschedule_fee = '//android.view.View[@content-desc="Reschedule fee"]'
    # "Price difference" surfaces as a clickable ImageView; its amount is the next View
    button_price_difference = '//android.widget.ImageView[@content-desc="Price difference"]'
    value_price_difference = '//android.widget.ImageView[@content-desc="Price difference"]/following-sibling::android.view.View[1]'

    # ================= payment =================
    label_payment_details = '//android.view.View[@content-desc="Payment details"]'
    # the chosen payment method (ImageView) sits right after the Payment details label
    value_payment_method = '//android.view.View[@content-desc="Payment details"]/following-sibling::android.widget.ImageView[1]'
    payment_method_by_name = '//android.widget.ImageView[@content-desc="%s"]'

    # ================= confirm =================
    # an ImageView (enabled=false until a reason is selected)
    button_confirm_pay = '//*[@content-desc="Confirm reschedule & pay"]'

    # ================= confirm dialog (after Confirm reschedule & pay) =================
    dialog_title = '//android.view.View[@content-desc="Confirm reschedule booking?"]'
    dialog_button_confirm = '//android.widget.Button[@content-desc="Confirm reschedule"]'
    dialog_button_go_back = '//android.widget.Button[@content-desc="Go back"]'
