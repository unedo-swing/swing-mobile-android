class ChangeBookingLocators:
    # ================= header =================
    label_change_booking = '//android.view.View[@content-desc="Change Booking"]'
    button_back = '//android.view.View[@content-desc="Change Booking"]/preceding-sibling::android.widget.ImageView[1]'

    # ================= tabs =================
    # content-desc is "Reschedule\nTab 1 of 2" / "Cancellation\nTab 2 of 2"
    tab_reschedule = '//android.view.View[contains(@content-desc,"Tab 1 of 2")]'
    tab_cancellation = '//android.view.View[contains(@content-desc,"Tab 2 of 2")]'

    # ================= reschedule tab =================
    label_reschedule_policy = '//android.view.View[@content-desc="Reschedule policy"]'
    # "•  Reschedule anytime:\n•  Allowed for Rp. 15,000"
    label_policy_text = '//*[contains(@content-desc,"Reschedule anytime")]'
    # "Allowed for Rp. 15,000\n18:00, 12 Aug 2026\n(Booking date & time)"
    label_booking_datetime = '//*[starts-with(@content-desc,"Allowed for")]'
    # "You can reschedule now for Rp. 15,000"
    label_reschedule_now = '//*[contains(@content-desc,"reschedule now")]'

    button_continue_reschedule = '//android.widget.ImageView[@content-desc="Continue reschedule"]'

    # ================= cancellation tab =================
    label_cancellation_policy = '//android.view.View[@content-desc="Cancellation policy"]'
    # a refund tier by the text it starts with, e.g. "100% refund" / "50% refund"
    # (content-desc is "100% refund (with promo code)\n17:00, 12 Aug 2026")
    refund_tier_by_text = '//*[starts-with(@content-desc,"%s")]'
    # "You can cancel now and still get refund for 50%!"
    label_cancel_now = '//*[contains(@content-desc,"cancel now")]'

    button_continue_cancel = '//android.widget.ImageView[@content-desc="Continue cancel"]'
