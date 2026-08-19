class BookingSummaryLocators:
    # --- header ---
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    label_title = '//android.view.View[@content-desc="Booking summary" and @heading="true"]'

    # --- booking identity / summary rows ---
    # course name varies: label_course_name % "Rainbow Hills Golf"
    label_course_name = '//android.view.View[@content-desc="%s"]'
    value_date = '//android.view.View[@content-desc="Date"]/following-sibling::android.view.View[1]'
    value_session = '//android.view.View[@content-desc="Session"]/following-sibling::android.view.View[1]'
    value_preferred_time = '//android.view.View[@content-desc="Preferred time"]/following-sibling::android.view.View[1]'
    label_booking_type = '//android.view.View[@content-desc="Standard booking" or @content-desc="Group booking"]'

    # --- players summary list ---
    # e.g. player_card_by_name % "Andi Wijaya" -> "AW\nAndi Wijaya\nRp. 1,000,000\n..."
    # First match in doc order is the summary card (not the price-details row).
    player_card_by_name = '(//android.widget.ImageView[contains(@content-desc,"%s")])[1]'

    # --- notes ---
    label_notes_title = '//android.view.View[@content-desc="Notes to golf course"]'
    value_notes = '//android.view.View[@content-desc="Notes to golf course"]/following-sibling::android.view.View[1]'

    # --- terms & conditions ---
    link_terms = '//android.view.View[@content-desc="Terms & conditions"]'
    label_terms_body = '//android.view.View[@content-desc="Terms & conditions"]/following-sibling::android.view.View[1]'

    # --- price details ---
    label_price_details = '//android.view.View[@content-desc="Price details"]'
    # per-player breakdown row: price_line_by_name % "Andi Wijaya"
    # (last() picks the price-details row over the summary card, which also
    # contains the name but doesn't carry "Published rate").
    price_line_by_name = ('(//android.widget.ImageView[contains(@content-desc,"%s") '
                          'and contains(@content-desc,"Published rate")])[1]')
    label_processing_fee = '//android.view.View[starts-with(@content-desc,"Processing fee")]'
    label_total_payment = '//android.view.View[starts-with(@content-desc,"Total payment")]'
