"""
Android XPaths for the Swing Driving Range > Booking summary screen.

A read-only summary of a booking: range name, the summary rows
(player/date/time/duration/bays/bay type), reservation notes, terms & conditions
(with a Show more toggle) and a time-based price breakdown.

Flutter app — values surface through ``content-desc``. Summary rows are a label
View next to a value View (read via the label's following sibling); price rows
are single Views whose content-desc "\\n"-joins the label and amount(s).
"""


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
