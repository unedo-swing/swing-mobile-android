class DrivingRangeBookingSuccessLocators:
    # apostrophe-free substring for "You're confirmed!"
    label_confirmed = '//android.view.View[contains(@content-desc,"confirmed")]'
    label_subtitle = '//android.view.View[@content-desc="See you on the driving range"]'
    label_range_name = '//android.view.View[@content-desc="%s"]'
    label_booking_id = '//android.view.View[contains(@content-desc,"Booking #")]'

    # a summary value read from its label's sibling: value_by_label % "Date"
    value_by_label = '//android.view.View[@content-desc="%s"]/following-sibling::android.view.View[1]'

    button_finish = '//android.widget.Button[@content-desc="Finish"]'
    button_see_details = '//android.widget.Button[@content-desc="See booking details"]'
