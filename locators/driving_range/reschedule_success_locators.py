class DrivingRangeRescheduleSuccessLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Booking rescheduled"]'
    label_subtitle = '//android.view.View[@content-desc="See you on the driving range"]'

    # ================= summary =================
    label_range_name = '//android.view.View[@content-desc="%s"]'
    label_booking_id = '//android.view.View[contains(@content-desc,"Booking #")]'

    # original vs new date/time block (one View, "\n"-joined:
    # "Original date & time\n18:00, 13 Aug 2026\nNew date & time\n22:00, 5 Aug 2026")
    label_change_block = '//*[starts-with(@content-desc,"Original date")]'

    # a value read from its label's sibling (skips any logo ImageView between
    # the label and the value): value_by_label % "Total" / "Payment method"
    value_by_label = '//android.view.View[@content-desc="%s"]/following-sibling::android.view.View[1]'

    # ================= actions =================
    button_finish = '//android.widget.Button[@content-desc="Finish"]'
    button_see_details = '//android.widget.Button[@content-desc="See booking details"]'
