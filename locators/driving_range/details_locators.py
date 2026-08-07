"""
Android XPaths for the Swing Driving Range > Details screen.

Opened by tapping a range card in the driving-range Explore. Flutter app —
elements surface through ``content-desc``. Dynamic bits (range name, date,
bay tab, time) use a ``contains`` / exact template.
"""


class DrivingRangeDetailsLocators:
    # --- header ---
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    label_title = '//android.view.View[@content-desc="Driving range details"]'
    button_share = '//android.view.View[@content-desc="Driving range details"]/following-sibling::android.widget.ImageView'

    # --- range info ---
    # exact range name: label_range_name % '"Albatross Driving Range"'
    label_range_name = '//android.view.View[@content-desc="%s"]'
    label_location = '//android.view.View[contains(@content-desc,"Indonesia")]'
    label_distance = '//android.view.View[contains(@content-desc,"km away")]'

    # --- promos (each card carries "<Promo>\nSwing Pass Exclusive") ---
    # promo_by_name % '"Promo Time Based DR"'
    promo_by_name = '//android.widget.ImageView[contains(@content-desc,"%s")]'
    badge_active = '//android.widget.ImageView[@content-desc="Active"]'
    banner_cashback = '//android.view.View[contains(@content-desc,"cashback on Swing Credits")]'
    
    button_calender = label_range_name + '/following-sibling::android.widget.ImageView[last()]'
    button_date_in_calender = '//android.view.View[contains(@content-desc,"%s")]'

    # --- date selector (content-desc is "<DAY>\n<dd Mon>") ---
    # pick by the date part: date_by_text % '"31 Jul"'
    date_by_text = '//android.view.View[contains(@content-desc,"%s")]'

    # --- bay tabs (content-desc is "<Name>\nTab N of 2") ---
    # bay_tab_by_name % '"Regular"' / '"QCorner"'
    bay_tab_by_name = '//android.view.View[starts-with(@content-desc,"%s")]'

    # --- time & duration ---
    label_select_time = '//android.view.View[@content-desc="Select time & duration"]'
    # a time by value: time_by_text % '"01:00"'
    time_by_text = '//android.view.View[@content-desc="%s"]'

    # --- duration selector (60 min / 120 min / 180 min) ---
    label_duration = '//android.view.View[@content-desc="Duration"]'
    # duration_by_text % '"60 min"'
    duration_by_text = '//android.view.View[@content-desc="%s"]'

    # --- rates & prices (time-based) ---
    label_rates_prices = '//android.view.View[contains(@content-desc,"Rates & prices")]'
    # a rate card by duration label (e.g. "60 minutes"):
    #   rate_card_by_duration % '"60 minutes"'
    rate_card_by_duration = '//android.widget.ImageView[contains(@content-desc,"%s")]'
    button_see_pricelist = '//android.widget.Button[@content-desc="See complete pricelist"]'

    # --- selected-booking summary bar (top) ---
    # e.g. "From Rp. 20,000\n80% saved\n30 Jul • 17:00 • 60 min\n+ 5% Cashback"
    label_booking_summary = '//android.widget.ImageView[starts-with(@content-desc,"From Rp.")]'

    # --- location ---
    label_location_section = '//android.view.View[@content-desc="Location"]'
    label_distance_from = '//android.view.View[contains(@content-desc,"from your location")]'
    button_view_on_maps = '//android.widget.ImageView[@content-desc="View on Google Maps"]'

    # --- book ---
    button_book = '//android.widget.Button[@content-desc="Book driving range"]'
