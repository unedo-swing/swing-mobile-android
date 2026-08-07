class DrivingRangeExploreLocators:
    # Back arrow — the first clickable ImageView on this screen.
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    # --- header ---
    search_bar = '//android.widget.ImageView[@content-desc="Search driving range..."]'
    # After tapping search_bar the pill expands into a real EditText.
    search_input = '//android.widget.EditText'
    region_selector = '//android.view.View[@content-desc="ID"]'
    label_title = '//android.view.View[contains(@content-desc,"driving range")]'

    # --- recent searches (shown after tapping search, before typing) ---
    label_recent_searches = '//android.view.View[@content-desc="Your recent searches"]'
    # a recent-search item by name: recent_search_by_name % '"Rainbow Hills Golf"'
    recent_search_by_name = '//android.widget.ImageView[@content-desc="%s"]'

    # --- "Only show Swing Pass partners" filter ---
    toggle_swing_pass = '//android.widget.ImageView[@content-desc="Only show Swing Pass partners"]'
    switch_swing_pass = '//android.widget.ImageView[@content-desc="Only show Swing Pass partners"]//android.widget.Switch'

    # --- range cards ---
    # cards carry a price like "Rp. .../ 60 mins" or ".../ 100 balls".
    range_card_any = '//android.view.View[contains(@content-desc,"mins") or contains(@content-desc,"balls")]'
    # a specific range by name: range_card_by_name % '"Golf Indonesia updated"'
    range_card_by_name = '(//android.view.View[contains(@content-desc,"%s")])[last()]'
