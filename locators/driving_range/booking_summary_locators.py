class DrivingRangeBookingSummaryLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Booking summary"]'
    button_back = '//android.view.View[@content-desc="Booking summary"]/preceding-sibling::android.widget.ImageView[1]'

    # range name shown at the top of the summary
    label_range_name = '//android.view.View[@content-desc="%s"]'

    # a summary value read from its label's sibling: value_by_label % "Date"
    value_by_label = '//android.view.View[@content-desc="%s"]/following-sibling::android.view.View[1]'

    # ================= notes / terms =================
    label_notes = '//android.view.View[@content-desc="Notes to driving range"]'
    label_terms = '//android.view.View[@content-desc="Terms & conditions"]'
    button_show_more = '//android.widget.ImageView[@content-desc="Show more"]'
    button_show_less = '//android.widget.ImageView[@content-desc="Show less"]'

    # ================= price details =================
    label_price_details = '//android.view.View[@content-desc="Price details (Time-based)"]'
    # a price row by the label it starts with, e.g. "Processing fee", "Total payment".
    # Any class: some rows surface as ImageViews, others as Views.
    price_row_by_label = '//*[starts-with(@content-desc,"%s")]'
