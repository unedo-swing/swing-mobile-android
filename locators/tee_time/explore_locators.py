class ExploreLocators:
    # Back arrow — the first clickable ImageView (no id/desc on this screen).
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    # --- header ---
    search_bar = '//android.widget.ImageView[@content-desc="Search golf courses..."]'
    # After tapping search_bar the pill expands into a real text field (the only
    # EditText on screen, auto-focused).
    search_input = '//android.widget.EditText'
    # Clear "X" — the clickable ImageView right after the text field (only shown
    # once the field has text).
    button_clear_search = '//android.widget.EditText/following-sibling::android.widget.ImageView[@clickable="true"]'
    region_selector = '//android.view.View[@content-desc="ID"]'
    label_title = '//android.view.View[contains(@content-desc,"tee time")]'

    # --- search results ---
    # header, e.g. '1 golf course (s) found for "Rainbow Hills" in Indonesia'
    label_results_count = '//*[contains(@content-desc,"found for")]'

    # --- empty results state (0 courses found) ---
    # message uses curly apostrophes, so match on an apostrophe-free substring.
    label_no_results = '//*[contains(@content-desc,"Simply tell us")]'
    button_request_location = '//android.widget.Button[@content-desc="Request a location"]'

    # --- "Only show Swing Pass partners" filter ---
    toggle_swing_pass = '//android.widget.ImageView[@content-desc="Only show Swing Pass partners"]'
    switch_swing_pass = '//android.widget.ImageView[@content-desc="Only show Swing Pass partners"]//android.widget.Switch'

    # --- course cards ---
    # any card, or a specific one — pass a quoted string for %s:
    #   course_card_by_name % '"Klub Golf Bogor Raya"'
    course_card_any = '//android.view.View[contains(@content-desc,"cashback")]'
    course_card_by_name = '(//android.view.View[contains(@content-desc,"%s")])[last()]'
