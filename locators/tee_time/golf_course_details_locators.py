"""
Android XPaths for the Swing Tee Time > Golf course details screen.

Opened by tapping a course card in Explore. Flutter app — elements surface
through ``content-desc``. Dynamic bits (course name, date, time slot) use a
``contains`` / exact template. Names follow ``<type>_<what>``.
"""


class GolfCourseDetailsLocators:
    # --- header ---
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    label_title = '//android.view.View[@content-desc="Golf course details"]'
    button_share = '//android.view.View[@content-desc="Golf course details"]/following-sibling::android.widget.ImageView'

    # --- course info ---
    # exact course name: label_course_name % '"Rainbow Hills Golf"'
    label_course_name = '//android.view.View[@content-desc="%s"]'
    label_location = '//android.view.View[contains(@content-desc,"Indonesia")]'
    label_distance = '//android.view.View[contains(@content-desc,"km away")]'
    banner_promo = '//android.view.View[contains(@content-desc,"Promotional Cashback")]'
    label_offer_valid = '//android.view.View[contains(@content-desc,"Offer valid until")]'
    # calendar icon next to the course name — fill %s with the course name:
    #   button_calender % '"Rainbow Hills Golf"'
    button_calender = label_course_name + '/following-sibling::android.widget.ImageView[last() - 1 ]'
    # a day inside the opened calendar — fill %s with the date text:
    #   button_date_in_calender % '"29"'
    button_date_in_calender = '//android.view.View[contains(@content-desc,"%s")]'

    # --- date selector (content-desc is "<DAY>\n<dd Mon>") ---
    # pick by the date part: date_by_text % '"28 Jul"'
    date_by_text = '//android.view.View[contains(@content-desc,"%s")]'

    # --- session tabs ---
    tab_day_session = '//android.widget.ImageView[starts-with(@content-desc,"Day Session")]'
    tab_night_session = '//android.widget.ImageView[starts-with(@content-desc,"Night Session")]'

    # --- tee-time slots ---
    label_select_tee_time = '//android.view.View[@content-desc="Select preferred tee time"]'
    # slot content-desc is "<start> - <end>\n<status>\n<price> / pax"
    # pick by the time: time_slot_by_text % '"06:00 - 06:30"'
    time_slot_by_text = '//android.view.View[contains(@content-desc,"%s")]'
    time_slot_any = '//android.view.View[contains(@content-desc,"/ pax")]'

    # --- "Prices shown include:" section ---
    label_prices_include = '//*[@content-desc="Prices shown include:"]'
    price_green_fee = '//android.view.View[@content-desc="Green fee"]'
    price_cart = '//android.view.View[@content-desc="Cart"]'
    price_caddy = '//android.view.View[@content-desc="Caddy"]'
    price_insurance = '//android.view.View[@content-desc="Insurance"]'

    # --- Amenities section ---
    label_amenities = '//*[@content-desc="Amenities"]'
    # amenity tile by name: amenity_by_name % '"Shoe rental"'
    amenity_by_name = '//android.widget.ImageView[@content-desc="%s"]'

    # --- Location section ---
    label_location_section = '//android.view.View[@content-desc="Location"]'
    label_distance_from = '//android.view.View[contains(@content-desc,"from your location")]'
    button_view_on_maps = '//android.widget.ImageView[@content-desc="View on Google Maps"]'
    map_webview = '//android.webkit.WebView'

    # --- More information section (course stats) ---
    label_more_information = '//android.view.View[@content-desc="More information"]'
    # stat card by its label prefix (content-desc is "<Label>\n<value>"):
    #   stat_by_label % '"Holes"' , '"Par"' , '"Length"' , '"Established in"' ...
    stat_by_label = '//android.view.View[starts-with(@content-desc,"%s")]'

    # --- book bar (shown/enabled once a slot is selected) ---
    # selected-slot summary, e.g. "Rp. 1,000,000 / pax\n29 Jul  •  11:30 - 12:00"
    label_booking_summary = '//android.view.View[contains(@content-desc,"/ pax") and contains(@content-desc,"•")]'
    badge_cashback = '//android.widget.ImageView[contains(@content-desc,"Cashback")]'
    button_book = '//android.widget.Button[@content-desc="Book tee time"]'
