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

    # ================================================================== #
    # Additions from the latest details-screen dump
    # ================================================================== #

    # --- hero image gallery (top carousel) ---
    gallery = '//android.widget.ScrollView/android.view.View[1]'
    gallery_image = gallery + '//android.widget.ImageView'
    # the little page-indicator dots sitting right under the carousel
    gallery_indicator = gallery + '/following-sibling::android.view.View[1]'

    # --- location line: "<City>, <Country>" • "<n>km away" ---
    label_city = '//android.view.View[contains(@content-desc,", Indonesia")]'
    button_distance = '//android.view.View[contains(@content-desc,"km away") and @clickable="true"]'

    # --- promos ---
    # every promo card carries "<Promo>\nSwing Pass Exclusive"
    promo_cards = '//android.widget.ImageView[contains(@content-desc,"Swing Pass Exclusive")]'
    button_promo_by_name = promo_by_name + '/ancestor::android.view.View[@clickable="true"][1]'
    badge_active_by_promo = promo_by_name + '//android.widget.ImageView[@content-desc="Active"]'
    badge_join_by_promo = promo_by_name + '//android.widget.ImageView[@content-desc="Join"]'
    button_see_all_featured_promo = '//android.widget.ImageView[@content-desc="See all"]'
    # the promo strip scrolls horizontally — anchor it on the cards it holds.
    # "See all" is the tile past the last promo, so it only renders after the
    # strip is swiped left.
    promo_carousel = promo_cards + '/ancestor::android.view.View[@scrollable="true"][1]'
    list_featured_promo = '//android.view.View[@content-desc="%s"]/following-sibling::android.view.View//android.view.View/android.widget.ImageView'

    # --- date strip (content-desc is "<DAY>\n<dd Mon>") ---
    dates_all = (
        '//android.view.View['
        'starts-with(@content-desc,"MON") or starts-with(@content-desc,"TUE") or '
        'starts-with(@content-desc,"WED") or starts-with(@content-desc,"THU") or '
        'starts-with(@content-desc,"FRI") or starts-with(@content-desc,"SAT") or '
        'starts-with(@content-desc,"SUN")]'
    )
    # date_by_day % 'TUE'
    date_by_day = '//android.view.View[starts-with(@content-desc,"%s")]'

    # --- bay tabs (content-desc is "<Name>\nTab N of 2") ---
    bay_tabs_all = '//android.view.View[contains(@content-desc,"Tab ")]'
    bay_tab_selected = '//android.view.View[contains(@content-desc,"Tab ") and @selected="true"]'
    # bay_tab_selected_by_name % 'Regular'
    bay_tab_selected_by_name = '//android.view.View[starts-with(@content-desc,"%s") and @selected="true"]'

    # --- time slots, scoped to the "Select time & duration" section so they
    #     can never collide with a time printed in the summary bar ---
    time_slots_container = label_select_time + '/following-sibling::android.view.View[1]'
    time_slots_all = time_slots_container + '//android.view.View[@content-desc]'
    # time_slot_by_text % '01:00'
    time_slot_by_text = time_slots_container + '//android.view.View[@content-desc="%s"]'

    # --- book ---
    button_book_disabled = button_book + '[@enabled="false"]'
