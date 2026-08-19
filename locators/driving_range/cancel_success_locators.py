class CancelSuccessLocators:
    label_title = '//android.view.View[@content-desc="Booking cancelled"]'
    label_subtitle = '//*[contains(@content-desc,"look forward to your next booking")]'

    label_range_name = '//android.view.View[@content-desc="%s"]'
    label_booking_id = '//android.view.View[contains(@content-desc,"Booking #")]'
    # value_by_label % "Booking ID" -> "#GSHRC", % "Cancellation date & time" -> "13:10, 6 Aug 2026"
    value_by_label = '//android.view.View[@content-desc="%s"]/following-sibling::android.view.View[1]'

    # "Total refunded (50%)" -> "Rp. 1,500,000" (percent varies)
    label_total_refunded = '//android.view.View[starts-with(@content-desc,"Total refund")]'
    value_total_refunded = '//android.view.View[starts-with(@content-desc,"Total refund")]/following-sibling::android.view.View[1]'
    label_refund_process = '//*[contains(@content-desc,"business days")]'

    button_finish = '//android.widget.Button[@content-desc="Finish"]'
    button_see_details = '//android.widget.Button[@content-desc="See cancellation details"]'
